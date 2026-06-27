---
title: BoomShop
created: 2026-06-13
updated: 2026-06-21
type: query
tags: [ctf, web, research]
sources: [https://github.com/atomicmemory/llm-wiki/blob/main/examples/boomshop-final-writeup.md, https://github.com/Yahyahcini/hacker101-ctf-writeups/blob/main/petshop-pro/README.md]
confidence: medium
---

# BoomShop

## 참고 URL
- [Original writeup](https://github.com/atomicmemory/llm-wiki/blob/main/examples/boomshop-final-writeup.md)
- [Original writeup](https://github.com/Yahyahcini/hacker101-ctf-writeups/blob/main/petshop-pro/README.md)


## 1. 요약
- 플랫폼: Example CTF
- 문제 URL: http://challenge.local
- 목표: admin flag
- 현재 상태: 로그인 우회와 서버측 요청 흐름을 함께 검증 중

## 2. 공격면
| Route | Method | Auth | Input | Output | Notes |
|------|------|------|------|------|------|
| /api/profile | GET | Yes | user_id | JSON | IDOR 가능성 |
| /api/fetch | POST | No | url | text | SSRF 가능성 |
| /admin/export | GET | Yes | format | file | 접근 제어 확인 필요 |

## 3. 가설
- 가설 A: `/api/fetch` 는 서버측 URL fetch 함수입니다.
- 가설 B: `user_id` 는 서버에서 강하게 검증되지 않습니다.
- 가설 C: `/admin/export` 는 권한 검사 누락 가능성이 있습니다.

## 4. 실험 로그
### 시도 1
- payload: `http://127.0.0.1:80`
- 관찰: timeout 발생
- 해석: 내부 요청 가능성 또는 egress filter 가능성
- 다음 가설: redirect 우회 또는 다른 스킴 테스트

### 시도 2
- payload: `user_id=2`
- 관찰: 다른 사용자 JSON 반환
- 해석: IDOR 가능성
- 다음 가설: 세션/권한 기준이 서버에서 일관적인지 확인

## 5. 연결된 개념
- [[ssrf]]
- [[idor]]
- [[broken-access-control]]

## 6. 다음 액션
- [ ] redirect 우회 여부 확인
- [ ] access control 체크 재검증
- [ ] admin export 응답 헤더 확인
