---
title: Cookie client storage — Web CTF patterns
created: 2026-06-14
updated: 2026-06-21
type: concept
tags: [ctf, web, session, storage, client-side]
sources: [https://github.com/snwau/picoCTF-2025-Writeup/blob/main/Web%20Exploitation/Cookie%20Monster%20Secret%20Recipe/Cookie%20Monster%20Secret%20Recipe.md, https://medium.com/@Kamal_S/picoctf-web-exploitation-cookie-monster-secret-recipe-4c1776da9251, https://blog.qz.sg/picoctf-2025-web-exploitation-writeups/]
confidence: high
---

# Cookie client storage — Web CTF patterns

## 참고 URL
- [Original source](https://github.com/snwau/picoCTF-2025-Writeup/blob/main/Web%20Exploitation/Cookie%20Monster%20Secret%20Recipe/Cookie%20Monster%20Secret%20Recipe.md)
- [medium.com](https://medium.com/@Kamal_S/picoctf-web-exploitation-cookie-monster-secret-recipe-4c1776da9251)
- [blog.qz.sg](https://blog.qz.sg/picoctf-2025-web-exploitation-writeups/)

## 1. 정의
**Cookie client storage**는 브라우저가 서버 도메인별로 저장·전송하는 쿠키 값을 CTF 공격면으로 보는 패턴입니다. 쿠키 자체는 정상 기능이지만, CTF에서는 플래그·역할·세션 상태가 쿠키에 그대로 또는 인코딩된 형태로 저장되는 경우가 많습니다.

## 2. 쉬운 비유
쿠키는 웹사이트가 사용자의 브라우저에 붙여 둔 **작은 메모지**와 같습니다. 서버가 매번 “이 사람이 누구였지?”를 다시 묻지 않도록 메모지를 확인합니다. 문제는 그 메모지에 비밀 레시피나 관리자 표시를 그대로 써 두면, 사용자가 브라우저 개발자 도구로 쉽게 읽거나 바꿀 수 있다는 점입니다.

## 3. 관찰 포인트
1. 로그인 실패·페이지 이동·버튼 클릭 후 쿠키가 새로 생기는지 확인합니다.
2. 쿠키 이름이 `secret`, `recipe`, `admin`, `role`, `session`, `token`처럼 의미를 드러내는지 봅니다.
3. 값이 URL 인코딩(`%3D`) 또는 Base64(`A-Z`, `a-z`, `0-9`, `+`, `/`, `=` 패턴)인지 확인합니다.
4. 값 수정이 필요한 문제인지, 읽고 디코딩만 하면 되는 문제인지 분리합니다.

## 4. 기본 풀이 루프
```text
# 1) 브라우저 개발자 도구에서 Application/Storage/Cookies를 확인합니다.
# 예상 결과: 현재 도메인에 설정된 쿠키 이름과 값이 표시됩니다.

# 2) 수상한 값을 URL decode → Base64 decode 순서로 확인합니다.
# 예상 결과: 숨겨진 문자열, JSON, flag 형식 등이 복원됩니다.

# 3) 세션·권한 값이면 변조 가능성을 별도로 테스트합니다.
# 예상 결과: 서버가 클라이언트 값을 신뢰하는지 판단할 수 있습니다.
```

## 5. Cookie Monster Secret Recipe에서의 적용
picoCTF 2025 `Cookie Monster Secret Recipe`는 로그인 우회 문제가 아니라 **쿠키 검사 문제**입니다. 임의 자격 증명으로 로그인하면 `Access Denied` 응답과 함께 “Have you checked your cookies lately?”라는 힌트가 나오고, 브라우저 쿠키 저장소에 `secret_recipe` 값이 남습니다. 이 값은 URL 인코딩과 Base64 인코딩이 겹쳐 있어 `URL decode → Base64 decode` 순서로 읽으면 flag 형식 문자열이 복원됩니다.

관련 정리: [[cookies-final-writeup]], [[cookie-monster-secret-recipe-final-writeup]], [[power-cookie-final-writeup]], [[more-cookies-final-writeup]]

추가 survey: [[cookie-tampering-writeup-survey]]

leaf writeup: [[postbook-final-writeup]]

## 6. 방어 관점
- 민감 정보는 클라이언트 쿠키에 평문 또는 단순 인코딩으로 저장하지 않습니다.
- 쿠키에 상태를 담아야 한다면 서버 측 서명·무결성 검증·만료 시간을 적용합니다.
- `HttpOnly`, `Secure`, `SameSite`는 노출·전송 위험을 줄이는 속성이지만, **서버가 쿠키 값 자체를 민감 정보 저장소로 쓰는 설계 문제**를 해결하지는 못합니다.
- 권한과 사용자 식별은 서버 측 세션 저장소 또는 검증 가능한 토큰으로 처리합니다.

## 7. 관련 위키 링크
- [[web-ctf-writeup-auth-session]] — 인증·세션 계열 Web CTF 허브
- [[base64-decoding-ctf-patterns]] — Base64 인코딩 판별과 디코딩 패턴
- [[web-ctf-master-checklist]] — Web CTF 공통 점검 목록
- [[broken-auth]] — 인증 설계 결함과 방어 관점

## 8. 참고 소스
- [snwau GitHub writeup](https://github.com/snwau/picoCTF-2025-Writeup/blob/main/Web%20Exploitation/Cookie%20Monster%20Secret%20Recipe/Cookie%20Monster%20Secret%20Recipe.md)
- [Kamal S Medium writeup](https://medium.com/@Kamal_S/picoctf-web-exploitation-cookie-monster-secret-recipe-4c1776da9251)
- [qz.sg picoCTF 2025 Web Exploitation writeups](https://blog.qz.sg/picoctf-2025-web-exploitation-writeups/)
