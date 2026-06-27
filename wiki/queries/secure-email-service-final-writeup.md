---
title: secure-email-service — picoCTF 2025 web writeup
created: 2026-06-14
updated: 2026-06-21
type: query
tags: [ctf, web, research, writeup, xss, csrf, broken-auth, mime, smime]
sources: [https://corgi.rip/posts/secure-email-service/, https://hackmd.io/@hibwyli/rJ8K23JT1x, https://blog.qz.sg/picoctf-2025-web-exploitation-writeups/]
confidence: high
---

# secure-email-service — picoCTF 2025 web writeup

> **핵심 요약**: 이 문제는 *MIME/메일 파서*, *S/MIME 서명 검증*, *브라우저 렌더링 sink*를 한 체인으로 엮습니다. 공격자는 헤더 인젝션과 MIME 구조 조작으로 HTML 메일을 만들고, 최종적으로 admin bot의 `localStorage` flag를 빼내는 XSS를 완성해야 합니다.

## 참고 URL
- [corgi.rip](https://corgi.rip/posts/secure-email-service/)
- [hackmd.io](https://hackmd.io/@hibwyli/rJ8K23JT1x)
- [blog.qz.sg](https://blog.qz.sg/picoctf-2025-web-exploitation-writeups/)


## 1. 문제 한 줄 정의

- `secure-email-service`는 **“서명된 HTML 메일만 렌더링되는 이메일 뷰어”** 를 악용해, **관리자 봇이 보는 메일 안에서 JavaScript를 실행**시키는 문제입니다.
- 단순 XSS가 아니라 **메일 포맷 조작 + 서명 우회 + 브라우저 DOM sink**가 모두 필요합니다.
- 난이도는 picoCTF 2025 Web 챌린지 중에서도 상위권이며, 공개 writeup에서도 매우 어려운 문제로 분류됩니다.

연결 개념: [[xss]], [[csrf]], [[broken-auth]], [[web-ctf-writeup-client-side]], [[web-ctf-writeup-auth-session]], [[web-ctf-writeup-parser-template]], [[signed-html-email-ctf-patterns]]

## 2. 빠른 결론

1. 서버는 사용자의 입력으로 이메일을 만들고, 일부 계정은 **HTML 메일을 S/MIME로 서명**해서 전송합니다.
2. 클라이언트는 메일을 열 때 `parsed.html` 이 있으면 **서명 검증 후 `shadow.innerHTML`** 로 렌더링합니다.
3. 따라서 공격자는 **HTML 메일이 되도록 메일 구조를 조작**하고, **admin bot이 그 메일을 열게 만들어** XSS를 실행해야 합니다.
4. 이 체인은 보통 다음 축으로 설명됩니다.
   - **header injection**
   - **predictable MIME boundary**
   - **signed HTML email rendering**
   - **XSS → localStorage flag exfiltration**

## 3. 문제 흐름

1. 사용자는 로그인 후 메일함을 봅니다.
2. admin bot은 첫 메일을 열고 reply 동작을 수행합니다.
3. 메일 뷰어는 텍스트/HTML 여부를 판별합니다.
4. HTML 메일이면 S/MIME 서명을 검증합니다.
5. 검증이 통과하면 HTML이 `shadow.innerHTML` 로 들어갑니다.
6. 공격자는 이 sink를 통해 admin bot 환경에서 JS를 실행하고 flag를 빼냅니다.

## 4. 기술적 원인

### 4.1 HTML 렌더링 sink 존재

메일 뷰어의 핵심 문제는 **검증된 HTML을 `innerHTML` 계열 sink에 넣는 것**입니다.

- 텍스트 메일은 `innerText` 또는 `pre` 로 표시됩니다.
- HTML 메일은 서명 검증이 성공하면 렌더링됩니다.
- 즉, “서명된 메일 = 안전한 메일”이라는 가정이 깨지면 그대로 XSS로 이어집니다.

### 4.2 메일 구조를 신뢰하는 파서 경계

이 문제는 단순 문자열 필터가 아니라 **MIME 구조 자체**를 공격 대상으로 봐야 합니다.

- `Subject` 나 본문에 대한 입력 검증만으로는 부족합니다.
- 개행 문자, encoded-word, multipart boundary 같은 요소가 파서의 해석을 바꿀 수 있습니다.
- 파서가 해석한 결과와 브라우저가 렌더링한 결과가 달라질 수 있습니다.

### 4.3 관리자 봇의 자동화된 행동

admin bot은 메일을 열고 reply하는 고정 동작을 수행합니다.

- 공격자는 봇의 흐름을 예측할 수 있습니다.
- 따라서 메일 내용과 구조를 봇의 렌더링/응답 흐름에 맞춰 설계할 수 있습니다.
- 이 점이 일반적인 self-XSS보다 훨씬 위험합니다.

## 5. 공격 체인 정리

### 공격자 관점 흐름

1. 공격자는 메일 전송 기능의 입력 지점에서 **헤더 인젝션 가능성**을 찾습니다.
2. 메일 생성 로직이 multipart 메시지를 만들 때 **예측 가능한 boundary** 를 쓰는지 확인합니다.
3. 메일 파서가 HTML로 인식하도록 MIME 구조를 조작합니다.
4. 서명 검증을 통과하는 형태로 메일을 구성합니다.
5. admin bot이 그 메일을 열도록 유도합니다.
6. 메일 뷰어의 `shadow.innerHTML` 에서 JS가 실행됩니다.
7. `localStorage.flag` 를 읽어 외부로 전송합니다.

### 방어자 관점 흐름

1. 헤더 값에 개행이 들어가지 않도록 강제합니다.
2. 사용자 입력으로 MIME 구조가 바뀌지 않도록 이메일 생성 방식을 단순화합니다.
3. HTML 메일은 무조건 sanitize 후 렌더링합니다.
4. 서명 검증 성공 여부와 렌더링 허용을 직접 연결하지 않습니다.
5. admin bot에 저장된 민감정보를 `localStorage` 같은 브라우저 저장소에 두지 않습니다.

## 6. 핵심 관찰 포인트

### 6.1 서명 검증이 있어도 안전하지 않습니다

- 서명은 **무결성**을 보장할 뿐, **안전한 HTML** 을 보장하지 않습니다.
- 공격자가 서명 가능한 구조를 만들거나, 구조 자체를 오도하면 렌더링 단계에서 문제가 발생합니다.

### 6.2 MIME boundary는 공격면이 될 수 있습니다

- multipart boundary가 예측 가능하면 파서 분기 조작 가능성이 생깁니다.
- 이메일 본문이 단순 텍스트라고 가정하면, 경계 조작을 놓치기 쉽습니다.

### 6.3 브라우저 렌더링은 최종 신뢰 경계입니다

- 서버에서 정상이더라도 브라우저 DOM sink에서 취약점이 터질 수 있습니다.
- 이 문제는 그 경계를 정확히 노린 전형적인 Web CTF 체인입니다.

## 7. 문제에서 배울 점

- 이메일은 문자열이 아니라 **구조화된 프로토콜**입니다.
- “검증됨”과 “안전함”은 같은 뜻이 아닙니다.
- `innerHTML` 은 항상 최후의 공격면으로 봐야 합니다.
- 관리자 봇이 있으면, 사용자의 입력이 **자동화된 신뢰 경로**로 연결되는지 먼저 봐야 합니다.
- Web CTF에서는 한 취약점보다 **취약점 간 연결**이 더 중요합니다.

## 8. 방어 관점 체크리스트

- `Subject`, `From`, `To` 등 헤더 값에 CR/LF 삽입을 차단합니다.
- HTML 메일 렌더링 전에 sanitization을 강제합니다.
- 서명 검증은 무결성 검증으로만 사용하고, 렌더링 허용 조건으로 단독 사용하지 않습니다.
- 브라우저에 민감정보를 저장하지 않습니다.
- admin bot은 가능한 한 별도 격리 환경에서 실행합니다.

## 9. 같이 보면 좋은 페이지

- [[xss]] — 최종 공격면인 브라우저 sink
- [[csrf]] — 자동화된 브라우저 행동과 결합되는 패턴
- [[broken-auth]] — 신뢰 경계가 잘못된 경우의 상위 개념
- [[web-ctf-writeup-client-side]] — 브라우저 렌더링 기반 문제 허브
- [[web-ctf-writeup-auth-session]] — 인증/세션 흐름과 bot 동작 패턴
- [[web-ctf-writeup-parser-template]] — 파서/템플릿/검증기 우회 패턴

## 10. 참고 소스

- [Web/Secure-Email-Service; PicoCTF 2025 — corgi.rip](https://corgi.rip/posts/secure-email-service/)
- [Secure Email Service — HackMD](https://hackmd.io/@hibwyli/rJ8K23JT1x)
- [PicoCTF 2025 - Web Exploitation Writeups — qz.sg](https://blog.qz.sg/picoctf-2025-web-exploitation-writeups/)
