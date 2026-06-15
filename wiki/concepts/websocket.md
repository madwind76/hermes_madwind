---
title: WebSocket — 보안 용어 해설
created: 2026-06-14
updated: 2026-06-14
type: concept
tags: [security, glossary, web, protocol, api, client-side]
sources: [https://ko.wikipedia.org/wiki/웹소켓, https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API, https://portswigger.net/web-security/websockets]
confidence: high
---

# WebSocket — 보안 용어 해설

## Step 1. 단어 직역과 쉬운 비유

### 1) 단어 풀이
- **Web**: 브라우저와 웹 서버가 연결되는 웹 환경입니다.
- **Socket**: 네트워크 프로그램끼리 데이터를 주고받기 위한 통신 끝점입니다.
- **WebSocket**: 웹 환경에서 브라우저와 서버가 하나의 연결을 오래 유지하며 양방향 메시지를 주고받는 통신 방식입니다.

### 2) 한 문장 정의
**WebSocket**은 브라우저와 서버가 한 번 연결한 뒤, 연결을 계속 열어 두고 실시간으로 메시지를 주고받게 하는 웹 통신 프로토콜입니다.

### 3) 쉬운 비유
일반 [[http]]가 식당에서 주문할 때마다 직원을 새로 부르는 방식이라면, WebSocket은 주방과 홀 사이에 켜 둔 **무전기 채널**입니다. 한 번 채널을 열어 두면 “새 주문”, “상태 변경”, “게임 점수 변경” 같은 메시지를 양쪽에서 바로 말할 수 있습니다.

## Step 2. 시각화

> `image_generate` 도구는 PNG 형식을 반환하므로, 시각화 이미지는 PNG URL로 임베드합니다.

![WebSocket 시각화 — 브라우저와 서버 사이의 지속 연결 무전기 채널](https://v3b.fal.media/files/b/0a9e3a15/OdBLXuKOSPjukwf88cLJD_VGDHIiXX.png)

그림은 브라우저와 서버 사이에 지속 연결 터널이 열리고, `ws://` 또는 `wss://` 경로로 실시간 메시지가 오가는 구조를 보여줍니다. 핵심은 연결이 유지된다는 점이며, 메시지 값 자체는 여전히 서버 측 검증 대상입니다.

## Step 3. 전문 설명

한국어 위키백과는 웹소켓을 단일 TCP 연결로 동시양방향통신 채널을 제공하는 통신 프로토콜로 설명합니다. 웹소켓은 HTTP와 구별되지만 HTTP 호환 핸드셰이크를 사용해 연결을 시작하며, RFC 6455로 표준화되었습니다.

MDN Web Docs는 WebSocket API가 브라우저와 서버 사이의 two-way interactive communication session을 열어 polling 없이 메시지를 보내고 받을 수 있게 한다고 설명합니다. 일반적인 `WebSocket` 인터페이스는 널리 지원되지만 backpressure를 직접 제공하지 않으므로, 메시지 처리 속도와 메모리 사용량을 설계 단계에서 고려해야 합니다.

PortSwigger는 WebSocket이 HTTP로 시작되고 장기간 유지되는 양방향 통신 채널이며, 일반 HTTP 애플리케이션에서 발생하는 취약점이 WebSocket 통신에서도 발생할 수 있다고 설명합니다.

## 공격자 관점

- 브라우저 개발자 도구나 Burp Suite WebSockets history에서 `ws://`, `wss://` 연결을 찾습니다.
- 메시지 안의 `role`, `score`, `price`, `state`, `eval` 같은 필드가 서버 로직에 영향을 주는지 확인합니다.
- [[tampering]] 관점에서 메시지를 바꾸고, [[websocket-message-tampering-ctf-patterns]]처럼 서버 반응을 비교합니다.

## 방어자 관점

- WebSocket 메시지는 일반 HTTP 요청과 같은 신뢰할 수 없는 입력입니다.
- 연결 수립 시 인증뿐 아니라 메시지 처리 단계의 권한·상태 전이도 검증해야 합니다.
- 메시지 schema, type, range, rate limit, audit log를 적용합니다.
- 민감한 판정 값은 클라이언트가 아니라 서버에서 계산합니다.

## 관련 용어 링크

- [[http]] — WebSocket 연결 시작에 쓰이는 요청/응답 프로토콜
- [[tampering]] — WebSocket 메시지 값을 바꾸는 행위
- [[eval]] — WebSockFish에서 변조 대상 이름으로 등장한 평가값
- [[websocket-message-tampering-ctf-patterns]] — Web CTF 적용 패턴
- [[tcp]] — WebSocket이 일반적으로 사용하는 전송 계층 프로토콜

## 후속 분리 후보

- `handshake`
- `schema validation`
- `backpressure`
- `wss`

## 참고 소스

- [한국어 위키백과 — 웹소켓](https://ko.wikipedia.org/wiki/웹소켓)
- [MDN — WebSocket API](https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API)
- [PortSwigger — WebSockets security vulnerabilities](https://portswigger.net/web-security/websockets)
