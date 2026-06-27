---
title: Tampering — 보안 용어 해설
created: 2026-06-14
updated: 2026-06-21
type: concept
tags: [security, glossary, request-manipulation, parameter-tampering, input-validation, web]
sources: [https://portswigger.net/web-security/logic-flaws/examples, https://portswigger.net/web-security/websockets, https://owasp.org/www-project-top-ten/]
confidence: high
---

# Tampering — 보안 용어 해설

## 참고 URL
- [portswigger.net](https://portswigger.net/web-security/logic-flaws/examples)
- [portswigger.net](https://portswigger.net/web-security/websockets)
- [owasp.org](https://owasp.org/www-project-top-ten/)

## Step 1. 단어 직역과 쉬운 비유

### 1) 단어 풀이
- **Tamper**: 허가 없이 만지거나, 몰래 고치거나, 원래 상태를 바꾸는 행위입니다.
- **Tampering**: 데이터, 요청, 메시지, 파일, 상태값을 중간에서 조작하는 행위입니다.

### 2) 한 문장 정의
**Tampering**은 클라이언트가 보낸 값이나 통신 중인 데이터를 의도와 다르게 바꿔 서버 로직이 그 조작을 신뢰하는지 확인하는 보안 테스트/공격 개념입니다.

### 3) 쉬운 비유
온라인 주문서에 “수량 1개, 가격 10,000원”이라고 적혀 있었는데, 누군가 계산대로 가기 전에 가격을 “100원”으로 고쳤다고 생각하면 됩니다. 계산대가 주문서를 다시 확인하지 않고 그대로 결제하면 문제가 됩니다. 웹에서는 이 주문서가 [[http]] 요청, JSON 필드, 쿠키, [[websocket]] 메시지가 됩니다.

## Step 2. 시각화

> `image_generate` 도구는 PNG 형식을 반환하므로, 시각화 이미지는 PNG URL로 임베드합니다.

![Tampering 시각화 — 클라이언트 값이 중간에서 변조되고 서버 검증으로 차단되는 흐름](https://v3b.fal.media/files/b/0a9e3a16/-G90zs3fOmhzZ2oelCu-8_qEUXU8rf.png)

그림은 클라이언트가 보낸 `role=user`, `price=100` 같은 값이 프록시나 도구를 통해 `role=admin`, `price=1`로 바뀌는 상황을 보여줍니다. 방어의 핵심은 서버가 클라이언트 값을 그대로 믿지 않는 것입니다.

## Step 3. 전문 설명

PortSwigger Web Security Academy는 비즈니스 로직 취약점의 공통 원인 중 하나로 client-side controls에 대한 과도한 신뢰를 설명합니다. 공격자는 Burp Proxy와 Repeater 같은 도구로 브라우저가 보낸 데이터를 서버 로직에 도달하기 전에 변경할 수 있으며, 이 경우 클라이언트 측 제한은 무력화됩니다.

PortSwigger WebSocket 보안 문서도 WebSocket 취약점 탐지는 애플리케이션이 예상하지 않은 방식으로 메시지와 연결을 조작하는 과정이라고 설명합니다. 즉 tampering은 HTTP 요청뿐 아니라 WebSocket 메시지, handshake, 쿠키, JSON body 등 다양한 입력 채널에 적용됩니다.

OWASP Top 10 관점에서는 tampering이 Broken Access Control, Injection, Security Misconfiguration 같은 여러 위험과 결합됩니다. 조작된 입력을 서버가 검증하지 않으면 권한 우회, 가격 변조, 상태 전이 우회, XSS/SQLi 같은 취약점으로 이어질 수 있습니다.

## 공격자 관점

- 클라이언트에서 제한한 값이 서버에서도 제한되는지 확인합니다.
- `role`, `uid`, `price`, `quantity`, `score`, `eval`, `state`처럼 서버 로직에 영향을 주는 값을 바꿉니다.
- [[parameter-tampering-ctf-patterns]]와 [[websocket-message-tampering-ctf-patterns]]처럼 작은 변화부터 극단값까지 반응 차이를 비교합니다.

## 방어자 관점

- 클라이언트 값은 모두 신뢰할 수 없는 입력으로 취급합니다.
- 서버 측에서 인증, 권한, 상태 전이, 숫자 범위, 자료형, 서명 검증을 수행합니다.
- 중요한 값은 클라이언트가 보내지 않게 하거나, 서버가 재계산합니다.
- 변조 의심 이벤트를 로깅하고 rate limiting을 적용합니다.

## 관련 용어 링크

- [[parameter-tampering-ctf-patterns]] — HTTP 파라미터 변조 패턴
- [[websocket-message-tampering-ctf-patterns]] — WebSocket 메시지 변조 패턴
- [[websocket]] — 실시간 메시지 채널
- [[http]] — 요청/응답 기반 변조 대상
- [[broken-access-control]] — 변조가 권한 우회로 이어지는 대표 영역

## 후속 분리 후보

- `input validation`
- `schema validation`
- `business logic vulnerability`
- `server-side validation`

## 참고 소스

- [PortSwigger — Examples of business logic vulnerabilities](https://portswigger.net/web-security/logic-flaws/examples)
- [PortSwigger — Testing for WebSockets security vulnerabilities](https://portswigger.net/web-security/websockets)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
