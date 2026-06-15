---
title: HTTP — 보안 용어 해설
created: 2026-06-14
updated: 2026-06-14
type: concept
tags: [security, glossary, web, protocol, api]
sources: [https://ko.wikipedia.org/wiki/HTTP, https://developer.mozilla.org/en-US/docs/Web/HTTP]
confidence: high
---

# HTTP — 보안 용어 해설

## Step 1. 단어 직역과 쉬운 비유

### 1) 약자 풀이
- **H**yper**T**ext: 링크로 연결되는 웹 문서와 하이퍼미디어입니다.
- **T**ransfer: 데이터를 주고받는 전송입니다.
- **P**rotocol: 서로 통신하기 위해 정한 규칙입니다.

### 2) 한 문장 정의
**HTTP(HyperText Transfer Protocol)**는 웹 브라우저와 웹 서버가 요청과 응답 형식으로 웹 문서, 이미지, API 데이터를 주고받기 위한 응용 계층 프로토콜입니다.

### 3) 쉬운 비유
HTTP는 웹의 **주문서 양식**입니다. 브라우저가 “이 URL의 페이지를 주세요”라는 주문서를 보내면, 서버는 “200 OK, 여기 본문입니다” 또는 “404 Not Found, 없습니다” 같은 응답서를 돌려줍니다. 주문이 끝나면 기본적으로 이전 주문을 기억하지 않기 때문에, 상태가 필요하면 쿠키나 세션 같은 보조 장치가 붙습니다.

## Step 2. 시각화

> `image_generate` 도구는 PNG 형식을 반환하므로, 시각화 이미지는 PNG URL로 임베드합니다.

![HTTP 시각화 — 클라이언트 요청과 서버 응답 주문서 구조](https://v3b.fal.media/files/b/0a9e3a1b/0WlLmExbZvlQtXWO4fLxl_iqg5Iy8I.png)

그림은 클라이언트가 메서드, URL, 헤더, 본문을 담은 요청을 보내고 서버가 상태 코드, 헤더, 본문으로 응답하는 흐름을 보여줍니다. HTTP는 무상태(stateless)이므로 인증·세션·쿠키 설계가 보안상 중요합니다.

## Step 3. 전문 설명

한국어 위키백과는 HTTP를 W3 상에서 정보를 주고받는 통신 프로토콜로 설명하며, 주로 HTML 문서 전송에 쓰이고 클라이언트-서버 간 요청-응답 방식으로 동작한다고 설명합니다. 일반적으로 TCP를 사용하지만 HTTP/3부터는 UDP 기반 QUIC를 사용합니다.

MDN은 HTTP를 HTML 같은 hypermedia documents를 전송하기 위한 application-layer protocol로 설명합니다. HTTP는 브라우저-서버 통신뿐 아니라 API와 machine-to-machine 통신에도 사용되며, 기본적으로 클라이언트가 연결을 열고 요청을 보낸 뒤 서버 응답을 기다리는 모델을 따릅니다.

보안 관점에서 HTTP는 메서드, 헤더, 쿠키, 본문, 상태 코드, 리다이렉트 등 많은 공격면을 포함합니다. Web CTF에서는 요청 파라미터 변조, 쿠키 검사, 인증 우회, [[ssrf]], [[xss]], [[cors-misconfig]] 같은 패턴이 HTTP 위에서 자주 등장합니다.

## 공격자 관점

- 메서드 변경(`GET` ↔ `POST`), 헤더 추가, 쿠키 수정, 파라미터 삭제·중복을 확인합니다.
- 상태 코드, 리다이렉트, 에러 메시지 차이를 근거로 서버 로직을 추론합니다.
- Burp Suite 같은 프록시로 [[parameter-tampering-ctf-patterns]]를 수행합니다.

## 방어자 관점

- 모든 요청 값은 서버 측에서 검증합니다.
- 인증·인가 검사는 화면이 아니라 API와 HTTP 핸들러 단에서 수행합니다.
- 안전한 쿠키 속성, CSRF 방어, CORS 정책, 보안 헤더를 함께 설계합니다.
- 로그에는 메서드, 경로, 사용자, 상태 코드, 실패 원인을 남깁니다.

## 관련 용어 링크

- [[websocket]] — HTTP 핸드셰이크로 시작하는 지속 연결 프로토콜
- [[cookie-client-storage-ctf-patterns]] — HTTP 쿠키 기반 CTF 패턴
- [[parameter-tampering-ctf-patterns]] — 요청 파라미터 변조
- [[api-security]] — API 입력 검증과 접근 제어
- [[tcp]] / [[udp]] — HTTP 버전에 따라 쓰이는 전송 계층

## 후속 분리 후보

- `HTTPS`
- `HTTP method`
- `HTTP header`
- `status code`
- `cookie`

## 참고 소스

- [한국어 위키백과 — HTTP](https://ko.wikipedia.org/wiki/HTTP)
- [MDN — HTTP](https://developer.mozilla.org/en-US/docs/Web/HTTP)
