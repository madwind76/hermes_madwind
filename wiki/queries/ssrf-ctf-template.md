---
title: SSRF CTF Template
created: 2026-06-13
updated: 2026-06-21
type: query
tags: [ctf, web, ssrf]
sources: [https://github.com/muhashali/writeup-SSRF, https://github.com/jdonsec/allthingsssrf, https://github.com/orangetw/My-CTF-Web-Challenges]
confidence: medium
---

# SSRF CTF Template

## 참고 URL
- [muhashali/writeup-SSRF](https://github.com/muhashali/writeup-SSRF)
- [jdonsec/allthingsssrf](https://github.com/jdonsec/allthingsssrf)
- [orangetw/My-CTF-Web-Challenges](https://github.com/orangetw/My-CTF-Web-Challenges)


## 1. 요약
- 플랫폼:
- 문제명:
- URL:
- 목표:
- 현재 상태:

## 2. 입력점
| Route | Method | Auth | Input | Output | Notes |
|------|------|------|------|------|------|
| | | | url / host / redirect / webhook | | SSRF 후보 입력점 |

## 3. 가설
- 가설 1: 서버가 외부 URL을 직접 요청한다.
- 가설 2: redirect 또는 scheme 우회가 가능하다.
- 가설 3: 내부 메타데이터 접근이 가능하다.

## 4. 실험 기록
### 시도 1
- payload:
- 관찰:
- 해석:
- 다음 가설:

### 시도 2
- payload:
- 관찰:
- 해석:
- 다음 가설:

## 5. 연결된 개념
- [[ssrf]]
- [[ssrf-core]]
- [[ssrf-defense]]
- [[broken-access-control]]
- [[proxy-mirror-final-writeup]]
## 6. 회고
- 막힌 지점:
- 우회 포인트:
- 다음에 먼저 볼 것:
- 재사용 체크리스트:
  - [ ] redirect 우회
  - [ ] allowlist 우회
  - [ ] 내부 호스트 접근
