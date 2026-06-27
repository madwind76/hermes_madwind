---
title: Signed HTML Email — 보안 용어 해설과 Web CTF 패턴
created: 2026-06-14
updated: 2026-06-21
type: concept
tags: [security, glossary, web, ctf, email, mime, smime, xss]
sources: [https://corgi.rip/posts/secure-email-service/, https://hackmd.io/@hibwyli/rJ8K23JT1x, https://blog.qz.sg/picoctf-2025-web-exploitation-writeups/, https://datatracker.ietf.org/doc/html/rfc2045, https://datatracker.ietf.org/doc/html/rfc2047, https://datatracker.ietf.org/doc/html/rfc5751]
confidence: high
---

# Signed HTML Email — 보안 용어 해설과 Web CTF 패턴

## 참고 URL
- [corgi.rip](https://corgi.rip/posts/secure-email-service/)
- [hackmd.io](https://hackmd.io/@hibwyli/rJ8K23JT1x)
- [blog.qz.sg](https://blog.qz.sg/picoctf-2025-web-exploitation-writeups/)
- [datatracker.ietf.org](https://datatracker.ietf.org/doc/html/rfc2045)
- [datatracker.ietf.org](https://datatracker.ietf.org/doc/html/rfc2047)
- [datatracker.ietf.org](https://datatracker.ietf.org/doc/html/rfc5751)

## Step 1. 단어 직역과 쉬운 비유

### 1) 단어 풀이
- **Signed email**: 발신자가 만든 내용이 바뀌지 않았음을 증명하기 위해 서명을 붙인 이메일입니다.
- **HTML email**: 텍스트가 아니라 HTML로 렌더링되는 이메일입니다.
- **MIME**: 이메일 본문을 여러 파트로 나누어 표현하는 표준 포맷입니다.
- **S/MIME**: 이메일 메시지에 암호학적 서명/암호화를 붙이는 표준입니다.

### 2) 한 문장 정의
**Signed HTML Email**은 “무결성이 검증된 이메일”이 “안전한 HTML”이라는 뜻은 아니라는 점을 악용할 수 있는 이메일 렌더링 패턴입니다.

### 3) 쉬운 비유
서명이 붙은 편지는 “누가 보냈는지”와 “중간에 바뀌지 않았는지”를 알려줍니다. 하지만 편지 안에 HTML이 들어 있고, 그 HTML을 브라우저가 그대로 실행하면 편지가 곧 웹페이지가 됩니다. 즉, *봉인된 편지*와 *실행되는 웹 콘텐츠*가 충돌하는 지점이 공격면이 됩니다.

## Step 2. 핵심 흐름 시각화

```text
header injection -> MIME boundary control -> signed HTML email -> browser sink -> XSS -> secret exfiltration
```

이 패턴은 메일 파서가 해석한 결과와 브라우저가 렌더링한 결과가 달라질 수 있다는 점을 이용합니다.

## Step 3. 전문 설명

이 패턴은 다음 요소가 겹칠 때 자주 나타납니다.

- **헤더 인젝션**: `Subject`, `From`, `To` 같은 헤더에 개행이 섞여 들어가면 새로운 헤더나 파트가 생길 수 있습니다.
- **MIME multipart 구조**: 본문이 여러 파트로 분리되므로 boundary 값이 중요합니다.
- **encoded-word**: RFC 2047 형식의 인코딩은 사람이 보기에는 문자열처럼 보여도 파서 입장에서는 다른 의미를 가질 수 있습니다.
- **S/MIME 검증**: 서명은 원본 일치성을 보장하지만, 렌더링 안전성까지 보장하지는 않습니다.
- **HTML sink**: 검증된 HTML을 `innerHTML` 또는 Shadow DOM의 HTML 삽입으로 넘기면 XSS가 발생할 수 있습니다.

즉, 이 문제는 “메일이 맞는가?”와 “브라우저에 안전한가?”를 같은 질문으로 취급하면 안 된다는 것을 보여줍니다.

### 짧은 코드 예시
```js
// 서명 검증은 무결성 확인일 뿐, HTML 안전성 보장과는 다릅니다.
if (parsed.html && signed) {
  const shadow = content.attachShadow({ mode: 'closed' });
  shadow.innerHTML = html; // HTML sink: sanitize 없이 넣으면 XSS 위험이 있습니다.
}
```

## 공격자 관점

1. 이메일 입력값에서 헤더 인젝션이 가능한지 확인합니다.
2. multipart boundary를 예측하거나 조작할 수 있는지 봅니다.
3. 메일 파서가 HTML로 인식하는 구조를 만듭니다.
4. 렌더링 시 브라우저 sink에 도달하도록 만들어 JavaScript 실행을 노립니다.

## 방어자 관점

1. 헤더 입력에 CR/LF가 들어가지 않도록 차단합니다.
2. MIME 구조를 사용자 입력과 분리하고, raw 이메일 조립을 최소화합니다.
3. HTML 메일은 반드시 sanitization 후 렌더링합니다.
4. 서명 검증 성공 여부를 렌더링 허용 조건으로 단독 사용하지 않습니다.
5. admin bot이나 자동화 클라이언트에는 민감정보를 브라우저 저장소에 두지 않습니다.

## Web CTF 패턴

`secure-email-service`는 이 패턴의 대표 예시입니다.

- 공격자는 메일 전송 기능에서 구조를 흔듭니다.
- 서버는 S/MIME로 서명된 HTML을 생성하거나 검증합니다.
- 클라이언트는 `shadow.innerHTML` 류의 sink로 HTML을 넣습니다.
- 결과적으로 admin bot이 가진 `localStorage` flag가 노출됩니다.

관련 writeup: [[secure-email-service-final-writeup]]

## 관련 위키 링크

- [[xss]] — 최종 실행면인 브라우저 sink
- [[csrf]] — 자동화된 브라우저 동작과 결합되는 패턴
- [[broken-auth]] — 신뢰 경계가 잘못되었을 때의 상위 개념
- [[web-ctf-writeup-client-side]] — 브라우저 렌더링 중심 Web CTF 허브
- [[web-ctf-writeup-auth-session]] — 자동화 봇과 세션 흐름
- [[web-ctf-writeup-parser-template]] — 파서/템플릿/검증기 차이
- [[secure-email-service-final-writeup]] — 이 패턴의 실전 writeup
- [[heap-dump-ctf-patterns]] — 다른 저장 경로에서 비밀이 노출되는 비교 사례

## 참고 소스

- [Web/Secure-Email-Service; PicoCTF 2025 — corgi.rip](https://corgi.rip/posts/secure-email-service/)
- [Secure Email Service — HackMD](https://hackmd.io/@hibwyli/rJ8K23JT1x)
- [PicoCTF 2025 - Web Exploitation Writeups — qz.sg](https://blog.qz.sg/picoctf-2025-web-exploitation-writeups/)
- [RFC 2045 — MIME Part One](https://datatracker.ietf.org/doc/html/rfc2045)
- [RFC 2047 — MIME Part Three: Message Header Extensions for Non-ASCII Text](https://datatracker.ietf.org/doc/html/rfc2047)
- [RFC 5751 — S/MIME 3.2 Message Specification](https://datatracker.ietf.org/doc/html/rfc5751)
