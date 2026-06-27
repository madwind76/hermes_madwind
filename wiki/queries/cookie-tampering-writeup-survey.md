---
title: Cookie Tampering Writeup Survey
created: 2026-06-19
updated: 2026-06-21
type: query
tags: [ctf, web, cookie, tampering, auth, session, survey, writeup, parameter-tampering, flask-session, cbc, bit-flipping, encoding]
sources: [https://github.com/Yahyahcini/hacker101-ctf-writeups/blob/main/postbook/README.md, https://github.com/Denis-Krueger-labs/writeups/blob/main/medium/ctf-collection-vol-2/report.md, https://github.com/Yahyahcini/hacker101-ctf-writeups/blob/main/README.md, https://ctftime.org/writeup/27377, https://medium.com/@Kamal_S/picoctf-web-exploitation-cookies-c85d0df3f1d6, https://github.com/ZeroDayTea/PicoCTF-2021-Killer-Queen-Writeups/blob/main/WebExploitation/Cookies.md, https://ctftime.org/writeup/32830, https://github.com/arvindshima/PicoCTF-2022/blob/main/Web%20Exploitation/power-cookie.md, https://github.com/wasi-master/picoCTF-2022/blob/main/web_exploitation/power_cookie.md, https://github.com/HHousen/PicoCTF-2021/blob/master/Web%20Exploitation/More%20Cookies/README.md, https://github.com/apoirrier/CTFs-writeups/blob/master/PicoCTF/Web/MostCookies.md, https://medium.com/@Kamal_S/picoctf-web-exploitation-cookie-monster-secret-recipe-4c1776da9251]
confidence: high
---

# Cookie Tampering Writeup Survey

> 목적: **쿠키/세션 값이 클라이언트에 노출되어 있고, 서버가 이를 신뢰하는 구조**를 비교합니다.
> 핵심 질문: “쿠키를 바꾸면 권한/상태가 바뀌는가?”

## 참고 URL
- [Original writeup](https://github.com/Yahyahcini/hacker101-ctf-writeups/blob/main/postbook/README.md)
- [Original writeup](https://github.com/Denis-Krueger-labs/writeups/blob/main/medium/ctf-collection-vol-2/report.md)
- [Original writeup](https://github.com/Yahyahcini/hacker101-ctf-writeups/blob/main/README.md)
- [CTFtime writeup](https://ctftime.org/writeup/27377)
- [medium.com](https://medium.com/@Kamal_S/picoctf-web-exploitation-cookies-c85d0df3f1d6)
- [Original writeup](https://github.com/ZeroDayTea/PicoCTF-2021-Killer-Queen-Writeups/blob/main/WebExploitation/Cookies.md)
- [CTFtime writeup](https://ctftime.org/writeup/32830)
- [Original writeup](https://github.com/arvindshima/PicoCTF-2022/blob/main/Web%20Exploitation/power-cookie.md)
- [Original writeup](https://github.com/wasi-master/picoCTF-2022/blob/main/web_exploitation/power_cookie.md)
- [Original writeup](https://github.com/HHousen/PicoCTF-2021/blob/master/Web%20Exploitation/More%20Cookies/README.md)
- [Original writeup](https://github.com/apoirrier/CTFs-writeups/blob/master/PicoCTF/Web/MostCookies.md)
- [medium.com](https://medium.com/@Kamal_S/picoctf-web-exploitation-cookie-monster-secret-recipe-4c1776da9251)


## 비교 대상

| Source | Primitive | What changed | Takeaway |
| --- | --- | --- | --- |
| `Postbook` | Predictable session cookie | `id` 쿠키가 사용자 ID의 MD5 해시 | 세션값이 예측 가능하면 곧바로 관리자 위장이 됩니다. |
| `Cookies` | Cookie enumeration | `name=0` → `name=1..n` | 쿠키를 상태값으로 쓰면 열거만으로 숨은 분기를 찾습니다. |
| `Power Cookie` | Client-side auth flag | `isAdmin=0` → `isAdmin=1` | 숫자 플래그를 쿠키에 두면 한 글자 변경으로 우회됩니다. |
| `More Cookies` | CBC bit flipping | 암호문 일부 비트 조작 | 암호화만으로는 무결성이 보장되지 않습니다. |
| `Most Cookies` | Flask session forgery | weak secret key brute-force | 서명 키가 약하면 세션 전체를 위조할 수 있습니다. |
| `Cookie Monster Secret Recipe` | URL/Base64 decoding | `secret_recipe` 쿠키 복원 | 인코딩된 쿠키도 읽을 수 있으므로 민감정보 저장은 부적절합니다. |
| `CTF Collection Vol.2` | Cookie tampering + hidden HTML + header abuse | 쿠키 조작, 페이지 소스 확인, 커스텀 요청 생성 | 쿠키는 다른 작은 논리 결함과 함께 자주 이어집니다. |
| `Hacker101 writeups repo` | Broken auth / cookie tampering index | 다양한 auth/session writeup 묶음 | 개별 문제보다 재사용 가능한 패턴을 찾는 데 유리합니다. |

## 공통 패턴

1. **서버가 클라이언트 상태를 너무 믿습니다.**
   - `user_id`, `role`, `is_admin` 같은 값이 브라우저 쪽에 있으면 우선 의심합니다.
2. **예측 가능한 인코딩/서명/암호화가 보입니다.**
   - MD5, Base64, 단순 숫자 ID, 약한 secret key는 변조 실험이 쉽습니다.
3. **Cookie tampering은 보통 다른 결함과 같이 나옵니다.**
   - IDOR, hidden field manipulation, HTTP method abuse, encoding confusion, CBC malleability와 연결됩니다.

## writeup별 메모

### 1) Postbook
- `user_id`가 hidden field로 들어가고, 쿠키 `id`는 사용자 ID의 MD5입니다.
- 핵심은 **클라이언트가 보낸 값이 서버 인증 로직에 직접 반영되는지**입니다.
- 좋은 연습 포인트:
  - hidden field 수정
  - 쿠키 값 교체
  - IDOR와 cookie tampering의 차이 구분

### 2) Cookies
- `snickerdoodle` 입력이 `name=0` 설정으로 이어집니다.
- 핵심은 **쿠키를 상태값처럼 열거할 수 있는지**입니다.
- 좋은 연습 포인트:
  - 쿠키 값을 순차적으로 바꾸며 응답 비교
  - flag 위치 찾기

### 3) Power Cookie
- `isAdmin=0` 플래그를 `1`로 바꾸는 전형적인 클라이언트 신뢰 오류입니다.
- 좋은 연습 포인트:
  - Burp 또는 DevTools로 쿠키 수정
  - 권한 분기 확인

### 4) More Cookies
- 암호화되어 있어도 CBC bit flipping으로 평문 일부를 바꿀 수 있습니다.
- 좋은 연습 포인트:
  - Base64 층과 암호문 층 분리
  - 무결성 부재 확인

### 5) Most Cookies
- Flask signed session cookie의 secret key가 약하면 세션 위조가 가능합니다.
- 좋은 연습 포인트:
  - 언서명/재서명
  - admin payload 변경

### 6) Cookie Monster Secret Recipe
- 브라우저 쿠키에서 URL decode → Base64 decode 순서로 비밀 값을 복원합니다.
- 좋은 연습 포인트:
  - 클라이언트 저장소 확인
  - 인코딩은 보안이 아니라는 점 확인

## 관련 개념

- [[cookie-client-storage-ctf-patterns]]
- [[flask-signed-session-cookie-ctf-patterns]]
- [[broken-auth]]
- [[broken-access-control]]
- [[parameter-tampering-ctf-patterns]]
- [[base64-decoding-ctf-patterns]]
- [[cbc-bit-flipping-ctf-patterns]]
- [[web-ctf-writeup-auth-session]]
- [[cookie-monster-secret-recipe-final-writeup]]
- [[most-cookies-final-writeup]]
- [[more-cookies-final-writeup]]
- [[power-cookie-final-writeup]]
- [[cookies-final-writeup]]

## 다음 읽을 거리

- [[cookie-monster-secret-recipe-final-writeup]]
- [[most-cookies-final-writeup]]
- [[more-cookies-final-writeup]]
- [[power-cookie-final-writeup]]
- [[cookies-final-writeup]]
- [[web-ctf-writeup-family-hub]]
