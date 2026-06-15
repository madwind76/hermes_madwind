---
title: HTTP method manipulation — picoCTF 패턴
created: 2026-06-14
updated: 2026-06-14
type: concept
tags: [ctf, web, http, methods, request-manipulation, proxy, burp]
sources: [https://medium.com/@ahmednarmer1/ctf-day-13-2ad289797f14, https://medium.com/@Kamal_S/picoctf-web-exploitation-get-ahead-fb9fa30d8f3d]
confidence: high
---

# HTTP method manipulation — picoCTF 패턴

## Step 1. 한 줄 정의
이 패턴은 **GET, HEAD, POST 같은 HTTP 메서드를 바꿔서 서버가 숨겨 둔 다른 동작이나 응답 헤더를 드러내는 Web CTF 유형**입니다.

## Step 2. 비유
- **비유**: 같은 창구에 가더라도 “서류를 달라(GET)”와 “서류는 보내지 말고 접수 기록만 보여 달라(HEAD)”라고 말하면, 창구 반응이 달라지는 상황입니다.
- **이미지**: 브라우저가 보내는 요청의 겉모습은 비슷해도, 메서드 한 글자 차이로 서버의 분기점이 바뀝니다.
- **전문 설명**: HTTP 메서드는 리소스를 읽을지, 생성할지, 헤더만 돌려줄지 등을 서버에 알리는 신호입니다. Web CTF에서는 메서드 자체가 입력값이므로, 메서드 변경이 곧 공격 벡터가 됩니다.

## 핵심 흐름
```text
page source / 버튼 동작 관찰 -> Burp로 요청 가로채기 -> GET/POST/HEAD 차이 확인 -> 메서드 변경 -> 응답 헤더/본문에서 flag 또는 힌트 확인
```

## 공격자 관점
1. UI가 단순하면 먼저 요청 메서드를 봅니다.
2. Burp Suite, curl, browser devtools로 요청을 캡처합니다.
3. `GET`만 보인다면 `HEAD`나 `POST`로 바꿔봅니다.
4. 응답 본문이 비어도 **헤더**를 확인합니다.
5. 메서드별로 서버가 다르게 처리하는 분기점을 찾습니다.

## 방어자 관점
- 메서드별 허용 동작을 명확히 제한합니다.
- `HEAD` 요청에도 민감한 정보를 노출하지 않습니다.
- 인증·인가 로직을 메서드에 의존하지 않습니다.
- 테스트 단계에서 `GET`, `HEAD`, `OPTIONS`, `POST`를 모두 확인합니다.

## 같이 보면 좋은 페이지
- [[http]]
- [[parameter-tampering-ctf-patterns]]
- [[web-ctf-writeup-client-side]]
- [[get-ahead-final-writeup]]

## 참고 소스
- [Ahmed Narmer — GET aHEAD writeup](https://medium.com/@ahmednarmer1/ctf-day-13-2ad289797f14)
- [Kamal S — GET aHEAD writeup](https://medium.com/@Kamal_S/picoctf-web-exploitation-get-ahead-fb9fa30d8f3d)
