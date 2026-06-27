---
title: WebSocket writeup survey
created: 2026-06-19
updated: 2026-06-21
type: query
tags: [ctf, web, survey, writeup, websocket, tampering, auth, client-side]
sources: [https://medium.com/@mihasha/websockfish-picoctf-2025-write-up-e7d4711ecfd3, https://ctftime.org/writeup/32568, https://ctftime.org/writeup/32495]
confidence: high
---

# WebSocket writeup survey

## 참고 URL
- [medium.com](https://medium.com/@mihasha/websockfish-picoctf-2025-write-up-e7d4711ecfd3)
- [CTFtime writeup](https://ctftime.org/writeup/32568)
- [CTFtime writeup](https://ctftime.org/writeup/32495)


## 1. 목적
WebSocket이 단순 통신 채널이 아니라 인증, 상태값, 게임 점수 같은 로직 입력점이 될 때 어떤 식으로 공격이 성립하는지 비교합니다.

## 2. 비교 대상
| 문제 | 주된 primitive | 보조 primitive | 한 줄 요약 |
|---|---|---|---|
| WebSockFish | score tampering | game-state manipulation | WebSocket 메시지의 eval 값을 바꿔 fish AI 항복을 유도합니다. |
| UTCTF 2022 Websockets | websocket login | brute-force PIN | WebSocket 인증 루틴을 스크립트로 자동화해 3자리 PIN을 맞춥니다. |

## 3. 공통 관찰
1. WebSocket은 HTTP와 달리 장기 연결이므로, 메시지 하나가 곧 서버 상태를 바꿉니다.
2. 메시지 내부 값(`eval`, `pass`, `user`)이 서버 측에서 재검증되지 않으면 조작이 가능합니다.
3. 로그인·게임·채팅처럼 실시간 응답이 필요한 기능은 WebSocket으로 쉽게 전환되지만, 검증이 느슨하면 공격 표면이 넓어집니다.

## 4. 관련 개념
- [[websocket-message-tampering-ctf-patterns]]
- [[websocket]]
- [[tampering]]
- [[web-ctf-writeup-client-side]]
- [[web-ctf-writeup-family-hub]]
- [[websockfish-final-writeup]]
- [[utctf-2022-websockets-final-writeup]]

## 5. 다음 읽을 거리
- [[websockfish-final-writeup]]
- [[utctf-2022-websockets-final-writeup]]
