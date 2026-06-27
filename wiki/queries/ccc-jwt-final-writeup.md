---
title: ccc — CSICTF 2020 JWT writeup
created: 2026-06-19
updated: 2026-06-19
type: query
tags: [ctf, web, writeup, jwt, token-forgery, auth, broken-auth, login, lfi]
sources: [https://raw.githubusercontent.com/team0se7en/CTF-Writeups/master/csictf2020/web/ccc/README.md]
confidence: high
---

# ccc — CSICTF 2020 JWT writeup

> JWT payload를 읽고, LFI로 `.env`의 secret을 찾아, admin:true 토큰을 직접 서명해 우회하는 writeup입니다.

## 참고 URL
- [raw source](https://raw.githubusercontent.com/team0se7en/CTF-Writeups/master/csictf2020/web/ccc/README.md)


## 1. 한 줄 요약
- login 후 JWT가 발급됩니다.
- `/adminNames`와 `getFile` 흐름을 따라가면 LFI가 드러납니다.
- `.env`에서 JWT secret을 읽고, admin 클레임을 가진 새 토큰을 만듭니다.

## 2. 문제 구조
| 항목 | 내용 |
|---|---|
| 플랫폼 | CSICTF 2020 |
| 난이도 | Web |
| 핵심 아이디어 | JWT secret exposure, token forgery, LFI |
| 관련 개념 | [[jwt-secret-exposure-ctf-patterns]], [[broken-auth]], [[web-ctf-writeup-family-hub]] |
| 관련 survey | [[jwt-auth-bypass-writeup-survey]] |

## 3. 공격면 정리
1. dummy credentials로 로그인하여 JWT 구조를 관찰합니다.
2. `/adminNames`가 파일 경로를 유도하는지 확인합니다.
3. `getFile`의 LFI로 `.env`를 읽습니다.
4. `JWT_SECRET`을 사용해 `admin:true` 토큰을 서명합니다.

## 4. 풀이 흐름
```bash
# 1) secret이 들어 있는 .env를 읽습니다.
# 예상 결과: JWT_SECRET 값이 출력됩니다.
GET /getFile?file=../.env

# 2) jwt.io 또는 로컬 스크립트로 새 토큰을 만듭니다.
# 예상 결과: admin:true 클레임을 포함한 JWT가 생성됩니다.
```

## 5. 왜 취약한가
- JWT 비밀키가 서버 파일에 평문으로 존재합니다.
- LFI가 인증 경계 너머의 비밀을 노출합니다.
- admin 여부가 서명된 클레임 하나에만 의존합니다.

## 6. 방어 관점
- `.env` 같은 secret 파일은 웹 루트 밖에 두고 직접 노출을 막습니다.
- JWT secret은 강하고 회전 가능한 값으로 관리합니다.
- 토큰 검증 외에도 server-side authorization을 추가합니다.

## 7. 다음 연결
- [[jwt-auth-bypass-writeup-survey]]
- [[jwt-secret-exposure-ctf-patterns]]
- [[broken-auth]]
