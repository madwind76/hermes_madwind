---
title: Most Cookies — picoCTF 2021 web writeup
created: 2026-06-15
updated: 2026-06-15
type: query
tags: [ctf, web, cookies, flask-session, session-forgery, picoctf]
sources: [https://ctftime.org/writeup/26978, https://ctftime.org/writeup/27376, https://picoctf2021.haydenhousen.com/web-exploitation/most-cookies, https://medium.com/@rwsimpson99/picoctf-most-cookies-f50eb44548ff]
confidence: high
---

# Most Cookies — picoCTF 2021 web writeup

> `Most Cookies`는 **Flask의 signed session cookie를 서버가 약한 secret key로 서명하고, 그 키를 추측하면 세션을 위조할 수 있다는 점**을 보여주는 picoCTF 2021 Web 문제입니다. 핵심은 쿠키를 “읽는” 것이 아니라, **서명 키를 찾아서 올바른 세션 쿠키를 다시 만들어내는 것**입니다.

## 1. 한 줄 요약
- 페이지는 Flask 세션 쿠키를 사용합니다.
- 서버는 짧은 비밀키 후보 목록 중 하나로 쿠키에 서명합니다.
- 공개된 소스나 힌트로 후보 목록을 알 수 있습니다.
- `flask-unsign` 같은 도구로 키를 브루트포스한 뒤 쿠키를 재서명합니다.

## 2. 문제 흐름
| 단계 | 관찰 | 의미 |
|------|------|------|
| 1 | 접속 시 세션 쿠키가 설정됨 | Flask signed session cookie 사용 |
| 2 | 페이지가 관리자 상태가 아님 | 세션 위조가 목표 |
| 3 | 소스에서 secret key 후보군이 짧음 | 브루트포스 가능성 큼 |
| 4 | 기존 쿠키를 언서명/디코딩 | 페이로드 구조 파악 |
| 5 | 후보 키를 순회하며 검증 | 올바른 secret key 탐색 |
| 6 | 관리자용 payload로 재서명 | flag 경로 접근 |

## 3. 핵심 분석
### 3.1 왜 이 문제가 중요한가
이 문제는 **쿠키가 있어도 안전하지 않다**는 점을 보여줍니다. 쿠키가 암호화되지 않아도, 서명 키가 약하면 결국 **세션 자체를 위조**할 수 있습니다.

### 3.2 실전 확인 포인트
```bash
# 세션 쿠키를 추출한 뒤 flask-unsign으로 언서명/검증을 시도합니다.
# 예상 결과: 후보 secret key 중 하나가 맞아떨어집니다.
```

```bash
# 올바른 키를 찾은 뒤 관리자 세션 payload를 다시 서명합니다.
# 예상 결과: admin 권한이 부여되고 flag 페이지로 이동합니다.
```

### 3.3 풀이 흐름
1. 브라우저에서 문제 페이지를 열고 쿠키를 확인합니다.
2. 세션 쿠키를 복사합니다.
3. `flask-unsign` 또는 동등한 도구로 secret key 후보를 브루트포스합니다.
4. 서명된 세션의 구조를 확인합니다.
5. 관리자 권한이 되도록 payload를 수정합니다.
6. 새 쿠키를 적용하고 flag를 확인합니다.

## 4. 공격자 관점
- Flask session cookie는 내용이 보인다고 끝이 아니라, **서명 키가 안전한지**가 핵심입니다.
- 단순 Base64 디코딩이 아니라 **서명 검증**이 필요합니다.
- 소스에 키 후보가 짧게 들어 있으면 거의 브루트포스 문제입니다.

## 5. 방어자 관점
- Flask secret key는 충분히 길고 예측 불가능해야 합니다.
- 세션에 들어가는 민감 권한은 최소화해야 합니다.
- 서버는 클라이언트가 만든 세션 값을 그대로 신뢰하면 안 됩니다.

## 6. 같이 보면 좋은 페이지
- [[cookie-client-storage-ctf-patterns]]
- [[flask-signed-session-cookie-ctf-patterns]]
- [[web-ctf-writeup-auth-session]]
- [[power-cookie-final-writeup]]
- [[more-cookies-final-writeup]]

## 7. 참고 소스
- [CTFtime — Most Cookies](https://ctftime.org/writeup/26978)
- [CTFtime — Most Cookies](https://ctftime.org/writeup/27376)
- [PicoCTF-2021 Writeup — Most Cookies](https://picoctf2021.haydenhousen.com/web-exploitation/most-cookies)
- [Robert Simpson — PicoCTF 2021 Most Cookies](https://medium.com/@rwsimpson99/picoctf-most-cookies-f50eb44548ff)
