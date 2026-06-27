---
title: Issues — SekaiCTF 2022 open redirect + JWT writeup
created: 2026-06-19
updated: 2026-06-21
type: query
tags: [ctf, web, jwt, token-forgery, broken-auth, parameter-tampering]
sources: [https://ctftime.org/writeup/35801, https://github.com/RaccoonNinja/Project-SEKAI-CTF-2022/blob/main/web/Issues.md]
confidence: high
---

# Issues — SekaiCTF 2022 open redirect + JWT writeup

> JWT `issuer` 검증이 redirect 가능한 URL과 결합되어 있어, open redirect로 서명키를 외부에서 주입하고 관리자 토큰을 위조하는 문제입니다.

## 참고 URL
- [CTFtime writeup](https://ctftime.org/writeup/35801)
- [Original writeup](https://github.com/RaccoonNinja/Project-SEKAI-CTF-2022/blob/main/web/Issues.md)


## 1. 한 줄 요약
- JWT 헤더의 `issuer`를 서버가 신뢰합니다.
- `logout?redirect=`가 open redirect로 동작합니다.
- 공격자는 자기 호스트의 `jwks.json`으로 서버를 유도해 토큰 검증을 우회합니다.

## 2. 문제 흐름
| 단계 | 관찰 | 의미 |
|---|---|---|
| 1 | `/api/flag`는 admin만 접근 가능 | 권한 상승 필요 |
| 2 | `issuer` 헤더의 netloc 검증이 존재 | 겉보기엔 안전해 보임 |
| 3 | `logout?redirect=`가 외부 URL로 이동 | open redirect 확보 |
| 4 | 외부 호스트에 `/.well-known/jwks.json` 배치 | 서버가 공격자 키를 읽게 함 |
| 5 | admin용 JWT를 위조 | flag 접근 성공 |

## 3. 핵심 payload 개념
```python
# 예상 결과: 서버가 공격자 호스트의 JWKS를 읽게 됨
headers={"issuer": "http://localhost:8080/logout?redirect=https://attacker.example"}
```

## 4. 연결 개념
- [[ssrf-ctf-patterns]]
- [[parameter-tampering-ctf-patterns]]
- [[broken-auth]]
- [[web-ctf-writeup-family-hub]]
- [[h1-2006-final-writeup]]

## 5. 참고 소스
- [CTFtime writeup 35801](https://ctftime.org/writeup/35801)
- [Original writeup](https://github.com/RaccoonNinja/Project-SEKAI-CTF-2022/blob/main/web/Issues.md)
