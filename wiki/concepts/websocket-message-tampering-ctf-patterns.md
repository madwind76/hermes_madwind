---
title: WebSocket Message Tampering — 보안 용어 해설과 Web CTF 패턴
created: 2026-06-14
updated: 2026-06-14
type: concept
tags: [security, glossary, web, ctf, request-manipulation, input-validation, api]
sources: [https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API, https://portswigger.net/web-security/websockets, https://portswigger.net/burp/documentation/desktop/testing-workflow/vulnerabilities/websockets/manipulating-websocket-messages, https://medium.com/@mihasha/websockfish-picoctf-2025-write-up-e7d4711ecfd3]
confidence: high
---

# WebSocket Message Tampering — 보안 용어 해설과 Web CTF 패턴

## Step 1. 단어 직역과 쉬운 비유

### 1) 단어 풀이
- **[[websocket|WebSocket]]**: 브라우저와 서버가 한 번 연결을 맺은 뒤 양방향으로 계속 메시지를 주고받는 웹 통신 방식입니다.
- **Message**: 연결 위에서 오가는 개별 데이터 조각입니다. 채팅 문장, 게임 상태, 점수, 명령 등이 될 수 있습니다.
- **[[tampering|Tampering]]**: 값을 몰래 바꾸거나 조작하는 행위입니다.
- **WebSocket Message Tampering**: WebSocket 연결로 오가는 메시지의 필드나 값을 애플리케이션이 예상하지 않은 방식으로 바꾸는 테스트/공격 패턴입니다.

### 2) 한 문장 정의
**WebSocket Message Tampering**은 실시간 WebSocket 통신에서 클라이언트가 보낸 메시지 값을 바꿔 서버 로직이 그 값을 신뢰하는지 확인하는 기법입니다.

### 3) 쉬운 비유
WebSocket은 식당 주방과 홀 직원 사이에 계속 열려 있는 **무전기 채널**과 같습니다. 손님 주문이 들어올 때마다 새 전화를 거는 것이 아니라, 무전기로 계속 “테이블 3번 주문 추가요”라고 말합니다. 그런데 누군가 중간에서 “체스 점수 -13”이라는 말을 “체스 점수 -130000000000”으로 바꾸었는데 주방이 그대로 믿어버리면, 시스템은 조작된 상태를 진짜로 착각합니다.

## Step 2. 시각화

> `image_generate` 도구는 PNG 형식을 반환하므로, 시각화 이미지는 PNG URL로 임베드합니다.

![WebSocket 메시지 변조 시각화 — 지속 연결에서 클라이언트 값 검증 필요](https://v3b.fal.media/files/b/0a9e37d1/dEgSLzW0bdBlMsTagXKjE_jfRpSFwj.png)

그림은 브라우저와 서버 사이의 지속 연결 터널에서 `move`, `eval 점수`, `game state` 메시지가 오가고, 중간 검증 지점에서 `eval=-13`이 극단값으로 바뀌는 상황을 보여줍니다. 핵심은 WebSocket이라고 해서 HTTP보다 안전한 것이 아니라, 메시지 내부 값을 서버가 다시 검증해야 한다는 점입니다.

## Step 3. 전문 설명

MDN Web Docs는 WebSocket API를 브라우저와 서버 사이에 양방향 interactive communication session을 열 수 있게 하는 API로 설명합니다. 일반적인 [[http|HTTP]] 요청/응답과 달리 WebSocket은 연결을 유지한 상태에서 클라이언트와 서버가 비동기적으로 메시지를 주고받을 수 있습니다.

PortSwigger Web Security Academy는 WebSocket 보안 테스트에서 메시지와 연결을 애플리케이션이 예상하지 않은 방식으로 조작하는 것이 핵심이라고 설명합니다. Burp Suite 같은 프록시 도구를 사용하면 WebSocket history에서 메시지를 확인하고, Repeater로 보내 수정·재전송할 수 있습니다.

보안 관점에서 WebSocket 메시지는 일반 [[http|HTTP]] 파라미터와 동일하게 신뢰할 수 없는 입력입니다. 게임 점수, 사용자 ID, 권한, 상태값, 가격, 명령어 같은 값이 WebSocket 메시지에 포함된다면 서버는 이를 그대로 믿지 말고 서버 측 상태와 규칙으로 재계산하거나 검증해야 합니다.

## 공격자 관점

1. 브라우저 개발자 도구 또는 프록시에서 `ws://`, `wss://` 연결을 찾습니다.
2. WebSocket history에서 클라이언트→서버 메시지와 서버→클라이언트 메시지를 분리합니다.
3. `score`, `[[eval|eval]]`, `role`, `user`, `state`, `price`, `move`처럼 서버 로직에 영향을 줄 수 있는 필드를 찾습니다.
4. 값을 조금씩 바꿔 응답 차이를 확인합니다.
5. 서버가 클라이언트 값을 신뢰하면 극단값, 경계값, 타입 변경을 테스트합니다.

```text
# WebSockFish 계열 CTF에서 관찰 가능한 메시지 변조 예시입니다.
# 예상 결과: 서버가 eval 값을 신뢰하면 게임 상태나 응답 문구가 비정상적으로 바뀝니다.
eval -13

eval -130000000000
```

## 방어자 관점

- WebSocket 메시지는 반드시 서버 측 schema validation을 통과해야 합니다.
- 점수, 승패, 가격, 권한처럼 중요한 값은 클라이언트가 아니라 서버가 계산합니다.
- 메시지 타입별 허용 필드, 자료형, 범위, 상태 전이를 검증합니다.
- 인증/인가 정보는 WebSocket handshake와 메시지 처리 단계 모두에서 확인합니다.
- WebSocket 트래픽도 로깅·모니터링·rate limiting 대상에 포함합니다.

## Web CTF 패턴

`picoCTF 2025 WebSockFish`에서는 체스 게임을 실제로 이기는 것보다 [[websocket|WebSocket]] 메시지의 `[[eval|eval]]` 값을 조작하는 것이 핵심입니다. 공개 writeup들은 Stockfish로 정상 승리해도 flag가 나오지 않았고, Burp Suite나 브라우저 도구로 WebSocket 메시지를 관찰한 뒤 `eval` 값을 극단적인 음수로 바꾸자 fish가 항복하며 flag가 노출되었다고 설명합니다.

관련 writeup: [[websockfish-final-writeup]]

## 관련 용어 링크

- [[websocket]] — 지속 양방향 웹 통신 프로토콜
- [[http]] — WebSocket 핸드셰이크와 비교되는 요청/응답 프로토콜
- [[tampering]] — 메시지·파라미터 값 조작 개념
- [[eval]] — WebSockFish에서 조작 대상이 된 평가값/코드 실행 함수명

## 관련 위키 링크

- [[web-ctf-writeup-client-side]] — 클라이언트/브라우저 상태와 실시간 통신 계열 Web CTF 허브
- [[web-ctf-writeup-auth-session]] — 클라이언트 제공 값을 서버가 신뢰하는 패턴 비교
- [[parameter-tampering-ctf-patterns]] — HTTP 파라미터 변조와 WebSocket 메시지 변조의 공통점
- [[api-security]] — API 입력 검증과 상태 관리
- [[web-ctf-master-checklist]] — Web CTF 공통 점검 목록

## 참고 소스

- [MDN WebSocket API](https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API)
- [PortSwigger — Testing for WebSockets security vulnerabilities](https://portswigger.net/web-security/websockets)
- [PortSwigger — Manipulating WebSocket messages with Burp Suite](https://portswigger.net/burp/documentation/desktop/testing-workflow/vulnerabilities/websockets/manipulating-websocket-messages)
- [mihasha — WebSockFish PicoCTF 2025 Write-up](https://medium.com/@mihasha/websockfish-picoctf-2025-write-up-e7d4711ecfd3)

## 후속 분리 후보

- `handshake`
- `schema validation`
- `input validation`
- `rate limiting`
