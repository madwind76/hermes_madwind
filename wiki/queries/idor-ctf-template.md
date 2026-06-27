---
title: IDOR CTF Template
created: 2026-06-13
updated: 2026-06-21
type: query
tags: [ctf, web, idor]
sources: [https://raw.githubusercontent.com/Yahyahcini/hacker101-ctf-writeups/main/petshop-pro/README.md, https://github.com/atomicmemory/llm-wiki/blob/main/examples/boomshop-final-writeup.md]
confidence: medium
---

# IDOR CTF Template

## 참고 URL
- [raw source](https://raw.githubusercontent.com/Yahyahcini/hacker101-ctf-writeups/main/petshop-pro/README.md)
- [Original writeup](https://github.com/atomicmemory/llm-wiki/blob/main/examples/boomshop-final-writeup.md)


## 1. 요약
- 플랫폼:
- 문제명:
- URL:
- 목표:
- 현재 상태:

## 2. 입력점
| Route | Method | Auth | Input | Output | Notes |
|------|------|------|------|------|------|
| | | | user_id / account_id / doc_id | | 객체 참조 후보 |

## 3. 가설
- 가설 1: 객체 식별자가 서버에서 강하게 검증되지 않는다.
- 가설 2: 수평 권한 상승이 가능하다.
- 가설 3: 접근 제어가 클라이언트에만 의존한다.

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
- [[idor]]
- [[broken-access-control]]
- [[privilege-escalation]]

## 6. 회고
- 막힌 지점:
- 우회 포인트:
- 다음에 먼저 볼 것:
- 재사용 체크리스트:
  - [ ] 동일 사용자의 객체 범위 확인
  - [ ] 수직/수평 권한 구분
  - [ ] 엔드포인트별 authorization 재검증
