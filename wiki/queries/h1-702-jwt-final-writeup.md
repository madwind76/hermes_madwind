---
title: h1-702 — HackerOne CTF JWT writeup
created: 2026-06-19
updated: 2026-06-21
type: query
tags: [ctf, web, writeup, jwt, token-forgery, auth, login, broken-auth, lfi]
sources: [https://gist.github.com/JMdoubleU/705819866852690d34e34aee2074a65c]
confidence: high
---

# h1-702 — HackerOne CTF JWT writeup

> JWT와 RPC 흐름을 함께 분석해, 숨은 flag가 들어 있는 note를 찾는 writeup입니다.

## 참고 URL
- [Gist](https://gist.github.com/JMdoubleU/705819866852690d34e34aee2074a65c)


## 1. 한 줄 요약
- RPC endpoint와 JWT 인증 구조를 먼저 파악합니다.
- note 접근 흐름을 따라가며 토큰과 파일 경계를 확인합니다.
- 인증/인가가 약한 지점을 중심으로 flag가 있는 데이터를 찾습니다.

## 2. 문제 구조
| 항목 | 내용 |
|---|---|
| 플랫폼 | HackerOne H1-702 CTF |
| 핵심 아이디어 | JWT auth bypass, file read, RPC enumeration |
| 관련 개념 | [[jwt-secret-exposure-ctf-patterns]], [[broken-auth]], [[web-ctf-writeup-family-hub]] |
| 관련 survey | [[jwt-auth-bypass-writeup-survey]] |

## 3. 공격면 정리
1. `/rpc.php`와 notes API 동작을 이해합니다.
2. JWT payload와 signature 구조를 확인합니다.
3. JWT secret을 찾거나 검증 우회 가능성을 조사합니다.
4. 접근 가능한 note metadata를 늘려 flag note를 찾습니다.

## 4. 풀이 흐름
```python
# 1) RPC 요청에 사용할 JWT를 준비합니다.
# 예상 결과: Authorization 헤더로 notes API 호출이 가능해집니다.

# 2) metadata와 note 조회를 반복합니다.
# 예상 결과: flag가 포함된 note를 찾습니다.
```

## 5. 왜 취약한가
- 인증된 사용자에게 너무 많은 RPC 기능이 열려 있습니다.
- 토큰 검증과 note 권한 검사가 느슨합니다.
- note id / metadata 노출이 탐색을 쉽게 만듭니다.

## 6. 방어 관점
- RPC 메서드별 권한을 분리합니다.
- JWT 검증 실패 시 모든 하위 기능을 차단합니다.
- note의 소유권을 서버에서 강제합니다.

## 7. 다음 연결
- [[jwt-auth-bypass-writeup-survey]]
- [[jwt-secret-exposure-ctf-patterns]]
- [[broken-auth]]
