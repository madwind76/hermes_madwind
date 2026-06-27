---
title: Client-side secret exposure — picoCTF pattern
created: 2026-06-14
updated: 2026-06-21
type: concept
tags: [ctf, web, client-side, javascript, source-inspection, base64, secrets]
sources: [https://medium.com/@ahmednarmer1/ctf-day-37-9587a06c6498, https://medium.com/@Kamal_S/picoctf-web-exploitation-get-ahead-fb9fa30d8f3d, https://medium.com/@Kamal_S/picoctf-web-exploitation-includes-10228bf124c8]
confidence: high
---

# Client-side secret exposure — picoCTF pattern

## 참고 URL
- [medium.com](https://medium.com/@ahmednarmer1/ctf-day-37-9587a06c6498)
- [medium.com](https://medium.com/@Kamal_S/picoctf-web-exploitation-get-ahead-fb9fa30d8f3d)
- [medium.com](https://medium.com/@Kamal_S/picoctf-web-exploitation-includes-10228bf124c8)

## Step 1. 한 줄 정의
이 패턴은 **HTML, JavaScript, CSS 같은 클라이언트 측 리소스 안에 자격 증명, flag 조각, 숨은 토큰이 들어 있어, source inspection만으로도 비밀을 찾을 수 있는 Web CTF 유형**입니다.

## Step 2. 비유
- **비유**: 가게 문 앞에 잠금장치가 있는 것처럼 보여도, 비밀번호 메모를 유리문에 붙여 둔 것과 같습니다.
- **이미지**: 사용자는 로그인 폼만 보지만, 브라우저가 이미 내려받은 JS 안에 답이 숨어 있습니다.
- **전문 설명**: 클라이언트로 전달된 코드는 누구나 열어볼 수 있으므로, 민감한 정보는 절대 그 안에 넣으면 안 됩니다. Base64는 암호화가 아니라 인코딩이므로, 숨김 효과가 거의 없습니다.
- **예시**: `Local Authority`처럼 `secure.js`나 `login.php`에 하드코딩된 자격 증명과 관리자 해시가 있으면, 브라우저만으로도 바로 노출됩니다.

## 핵심 흐름
```text
login form / simple UI -> view-source / devtools -> JS/CSS/HTML 확인 -> Base64 또는 문자열 분해 발견 -> decode -> credentials 또는 flag 획득
```

## 공격자 관점
1. UI가 단순하면 먼저 page source를 봅니다.
2. JavaScript 파일과 인라인 스크립트를 확인합니다.
3. Base64처럼 보이는 문자열을 디코딩합니다.
4. `admin`, `password`, `flag` 조각이 분산돼 있는지 찾습니다.
5. 발견한 값으로 로그인하거나 추가 엔드포인트를 확인합니다.

## 방어자 관점
- 민감한 값은 클라이언트 자원에 넣지 않습니다.
- Base64로 숨기는 방식은 보안이 아닙니다.
- 인증 관련 로직은 서버에서 검증합니다.
- 소스맵, 주석, 테스트용 문자열에 자격 증명을 남기지 않습니다.

## 같이 보면 좋은 페이지
- [[source-inspection-minification-ctf-patterns]]
- [[base64-decoding-ctf-patterns]]
- [[web-ctf-writeup-client-side]]
- [[login-final-writeup]]
- [[local-authority-final-writeup]]

## 참고 소스
- [Ahmed Narmer — picoCTF Web Exploitation: login](https://medium.com/@ahmednarmer1/ctf-day-37-9587a06c6498)
- [Kamal S — picoCTF Web Exploitation: GET aHEAD](https://medium.com/@Kamal_S/picoctf-web-exploitation-get-ahead-fb9fa30d8f3d)
- [Kamal S — picoCTF Web Exploitation: Includes](https://medium.com/@Kamal_S/picoctf-web-exploitation-includes-10228bf124c8)
