---
title: H1-2006 2020 CTF writeup
created: 2026-06-19
updated: 2026-06-19
type: query
tags: [ctf, web, writeup, ssrf, internal-service, auth, token-forgery, xss, login]
sources: [https://raw.githubusercontent.com/Louzogh/CTF-Writeup/master/2020/H1-2006-CTF/README.md]
confidence: high
---

# H1-2006 2020 CTF writeup

> SSRF, open redirect, token reuse, internal API access, and final CSS exfiltration까지 이어지는 복합 web chain입니다.

## 참고 URL
- [raw source](https://raw.githubusercontent.com/Louzogh/CTF-Writeup/master/2020/H1-2006-CTF/README.md)


## 1. 한 줄 요약
- `*.bountypay.h1ctf.com`에서 여러 서브도메인을 찾습니다.
- redirect 기반 SSRF로 내부 서비스에 접근합니다.
- 로그와 토큰 노출을 통해 계정과 2FA 정보를 회수합니다.
- 최종적으로 내부/관리자 경로를 따라가 flag를 얻습니다.

## 2. 문제 구조
| 항목 | 내용 |
|---|---|
| 플랫폼 | HackerOne H1-2006 CTF |
| 핵심 아이디어 | SSRF, internal service access, token reuse, auth bypass |
| 관련 개념 | [[ssrf-ctf-patterns]], [[api-security-core]], [[broken-auth]], [[web-ctf-writeup-family-hub]] |
| 관련 survey | [[ssrf-internal-service-writeup-survey]] |

## 3. 공격면 정리
1. `www`, `api`, `app`, `staff`, `software` 서브도메인을 열거합니다.
2. `api/redirect?url=` 흐름으로 internal service로 이동합니다.
3. `app`의 log exposure에서 credentials와 2FA answer를 회수합니다.
4. 인증/세션을 이어 붙여 staff/admin 흐름으로 이동합니다.

## 4. 풀이 흐름
```text
# 1) redirect 기반 internal access
api/redirect?url=https://software.bountypay.h1ctf.com/
# 예상 결과: 내부 전용 서비스로 이어지는 경로를 찾습니다.

# 2) 로그에서 credential 회수
bp_web_trace.log
# 예상 결과: username / password / challenge_answer가 보입니다.
```

## 5. 왜 취약한가
- redirect가 사실상 SSRF 브리지 역할을 합니다.
- 로그에 민감 정보가 남습니다.
- 인증 흐름이 여러 서비스에 분산되어 일관성이 없습니다.

## 6. 방어 관점
- redirect target을 allowlist로 제한합니다.
- 로그에서 credential/2FA answer를 제거합니다.
- 내부 서비스는 네트워크 레벨에서 직접 차단합니다.

## 7. 다음 연결
- [[ssrf-internal-service-writeup-survey]]
- [[ssrf-ctf-patterns]]
- [[broken-auth]]
