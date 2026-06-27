---
title: RTFM — Hacker101 CTF writeup
created: 2026-06-19
updated: 2026-06-19
type: query
tags: [ctf, web, writeup, ssrf, internal-service, api, api-security, broken-auth]
sources: [https://raw.githubusercontent.com/Yahyahcini/hacker101-ctf-writeups/main/RTFM/README.md]
confidence: high
---

# RTFM — Hacker101 CTF writeup

> `/api/v1/`와 `/api/v2/` 사이의 인증 불일치, hidden config, SSRF, 세션/토큰 재사용을 엮는 API writeup입니다.

## 참고 URL
- [raw source](https://raw.githubusercontent.com/Yahyahcini/hacker101-ctf-writeups/main/RTFM/README.md)


## 1. 한 줄 요약
- `/api/v2/swagger.json`으로 endpoint를 찾습니다.
- `/api/v1/config`와 `/api/v1/secrets`의 보안 경계를 확인합니다.
- `avatar` 필드가 SSRF 트리거가 되어 internal secret을 읽게 됩니다.
- 버전 간 token/session 재사용이 추가 공격면이 됩니다.

## 2. 문제 구조
| 항목 | 내용 |
|---|---|
| 플랫폼 | Hacker101 CTF |
| 난이도 | Moderate |
| 핵심 아이디어 | SSRF, API version mismatch, auth reuse, hidden endpoints |
| 관련 개념 | [[ssrf-ctf-patterns]], [[api-security-core]], [[broken-auth]], [[web-ctf-writeup-family-hub]] |
| 관련 survey | [[ssrf-internal-service-writeup-survey]] |

## 3. 공격면 정리
1. `ffuf`로 root와 `/api/v1/`, `/api/v2/`를 fuzz합니다.
2. Swagger와 config endpoint에서 내부 구조를 파악합니다.
3. `avatar` 필드에 URL을 넣어 SSRF를 유도합니다.
4. 버전마다 다른 토큰 헤더를 재사용해 관리자 기능을 찾습니다.

## 4. 풀이 흐름
```bash
# 1) endpoint 열거
ffuf -u https://LABURL/FUZZ -w /usr/share/seclists/Discovery/Web-Content/api/api-endpoints.txt

# 2) SSRF 유도
# 예상 결과: avatar=https://LABURL/api/v1/secrets 형태가 내부 요청으로 처리됩니다.
```

## 5. 왜 취약한가
- API 버전별 인증 규칙이 일관되지 않습니다.
- 내부 요청용 필드에 URL allowlist가 없습니다.
- 토큰/세션 헤더를 재사용할 수 있습니다.

## 6. 방어 관점
- 버전 간 인증 정책을 통합합니다.
- 서버가 외부 URL을 가져오는 필드는 엄격히 allowlist합니다.
- 민감 API는 내부 요청 차단과 role check를 모두 둡니다.

## 7. 다음 연결
- [[ssrf-internal-service-writeup-survey]]
- [[ssrf-ctf-patterns]]
- [[api-security-core]]
