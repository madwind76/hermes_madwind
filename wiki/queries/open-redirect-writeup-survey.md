---
title: Open Redirect writeup survey
created: 2026-06-19
updated: 2026-06-21
type: query
tags: [ctf, web, survey, writeup, ssrf, jwt, broken-auth, parameter-tampering]
sources: [https://ctftime.org/writeup/35801, https://ctftime.org/writeup/9187, https://medium.com/@0xMuhammet/open-redirect-vulnerability-ctf-based-922fa40d36ff]
confidence: high
---

# Open Redirect writeup survey

## 참고 URL
- [CTFtime writeup](https://ctftime.org/writeup/35801)
- [CTFtime writeup](https://ctftime.org/writeup/9187)
- [medium.com](https://medium.com/@0xMuhammet/open-redirect-vulnerability-ctf-based-922fa40d36ff)


## 1. 목적
Open redirect가 단독으로 끝나는 경우와, JWT/SSRF/XSS 같은 체인으로 이어지는 경우를 비교합니다.

## 2. 비교 대상
| 문제 | 주된 primitive | 보조 primitive | 한 줄 요약 |
|---|---|---|---|
| Issues | open redirect | JWT token forgery | redirect 가능한 issuer를 이용해 공격자 키를 주입합니다. |
| H1-2006 | redirect-based SSRF | internal service access | redirect가 내부 서비스 접근 브리지 역할을 하며 토큰/로그 노출과 결합됩니다. |

## 3. 공통 관찰
1. open redirect는 단독 취약점보다 **체인 연결점**일 때 위험도가 커집니다.
2. `Location:` 헤더나 `redirect=` 파라미터가 외부 URL을 허용하면 SSRF/JWT 키 주입으로 이어질 수 있습니다.
3. 응답 status가 302여도 실제 위험은 **어디로 재지정되는지**와 **그 이후 무엇이 신뢰되는지**에 달려 있습니다.

## 4. 관련 개념
- [[ssrf-ctf-patterns]]
- [[parameter-tampering-ctf-patterns]]
- [[broken-auth]]
- [[web-ctf-writeup-internal-service]]
- [[web-ctf-writeup-family-hub]]
- [[issues-final-writeup]]
- [[h1-2006-final-writeup]]

## 5. 다음 읽을 거리
- [[issues-final-writeup]]
- [[h1-2006-final-writeup]]
