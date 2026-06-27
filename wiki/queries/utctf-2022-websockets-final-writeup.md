---
title: UTCTF 2022 Websockets writeup
created: 2026-06-19
updated: 2026-06-21
type: query
tags: [ctf, web, websocket, authentication, brute-force, login]
sources: [https://ctftime.org/writeup/32568, https://ctftime.org/writeup/32495, https://blog.daanbreur.systems/2022/03/15/UTCTF2022-Websockets.html]
confidence: high
---

# UTCTF 2022 Websockets writeup

> 로그인 검증이 일반 HTTP가 아니라 WebSocket으로 구현되어 있어, 3자리 PIN을 브루트포스로 맞추는 문제입니다.

## 참고 URL
- [CTFtime writeup](https://ctftime.org/writeup/32568)
- [CTFtime writeup](https://ctftime.org/writeup/32495)
- [blog.daanbreur.systems](https://blog.daanbreur.systems/2022/03/15/UTCTF2022-Websockets.html)


## 1. 한 줄 요약
- 로그인 폼의 `login.js`가 `/internal/ws` WebSocket을 엽니다.
- 사용자명 `admin`이 존재함을 에러 메시지로 확인할 수 있습니다.
- 3자리 PIN(`000`~`999`)을 스크립트로 자동 시도해 세션 토큰을 받습니다.

## 2. 문제 흐름
| 단계 | 관찰 | 의미 |
|---|---|---|
| 1 | 소스에 `/internal/login`, `/internal/ws`가 노출됨 | 비공개 경로가 힌트로 새어 나옴 |
| 2 | 에러 메시지로 유효 사용자명 판별 | username enumeration 가능 |
| 3 | `pass (\d{3}|\d{16})` 패턴 노출 | 3자리 PIN 브루트포스 가능 |
| 4 | WebSocket `begin` / `user` / `pass` 메시지 전송 | HTTP 폼이 아니라 WS 인증 루틴 |
| 5 | `session <token>` 수신 | 로그인 성공 후 flag 페이지 접근 |

## 3. 핵심 메시지 예시
```javascript
// 예상 동작: WebSocket으로 begin → user → pass 전송
const socket = new WebSocket("ws://host/internal/ws");
// 예상 결과: session 토큰 또는 badpass 응답
```

## 4. 연결 개념
- [[websocket-message-tampering-ctf-patterns]]
- [[websocket]]
- [[tampering]]
- [[web-ctf-writeup-client-side]]
- [[web-ctf-writeup-family-hub]]

## 5. 참고 소스
- [CTFtime writeup 32568](https://ctftime.org/writeup/32568)
- [CTFtime writeup 32495](https://ctftime.org/writeup/32495)
- [Original writeup](https://blog.daanbreur.systems/2022/03/15/UTCTF2022-Websockets.html)
