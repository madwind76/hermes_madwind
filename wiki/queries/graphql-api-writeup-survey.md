---
title: GraphQL API writeup survey
created: 2026-06-19
updated: 2026-06-19
type: query
tags: [ctf, web, survey, writeup, api, api-security, authorization, broken-access-control, injection]
sources: [https://raw.githubusercontent.com/Yahyahcini/hacker101-ctf-writeups/main/BugDB%20v1/README.md, https://raw.githubusercontent.com/Yahyahcini/hacker101-ctf-writeups/main/BugDB%20v2/README.md]
confidence: high
---

# GraphQL API writeup survey

## 참고 URL
- [raw source](https://raw.githubusercontent.com/Yahyahcini/hacker101-ctf-writeups/main/BugDB%20v1/README.md)
- [raw source](https://raw.githubusercontent.com/Yahyahcini/hacker101-ctf-writeups/main/BugDB%20v2/README.md)


## 1. 목적
GraphQL 기반 CTF writeup 2건을 비교해, introspection, query abuse, mutation abuse가 어떻게 권한 경계를 무너뜨리는지 정리합니다.

## 2. 비교 대상
| 문제 | 주된 primitive | 보조 primitive | 한 줄 요약 |
|---|---|---|---|
| BugDB v1 | GraphQL introspection | missing authorization | schema를 읽고 제한 없는 query로 모든 bug를 덤프합니다. |
| BugDB v2 | GraphQL mutation abuse | predictable IDs | mutation으로 private bug를 공개로 바꾸고 flag를 읽습니다. |

## 3. 공통 관찰
1. GraphQL은 endpoint가 하나여도 **schema 공개**가 곧 공격면이 됩니다.
2. `Query`와 `Mutation` 둘 다 권한 검사가 약하면 데이터 열람과 수정이 동시에 깨집니다.
3. 내부 ID가 예측 가능하면, 숨겨진 객체를 찾는 난이도가 급격히 낮아집니다.

## 4. 관련 개념
- [[api-security-defense]]
- [[broken-access-control-defense]]
- [[web-ctf-writeup-family-hub]]
- [[bugdb-v1-final-writeup]]
- [[bugdb-v2-final-writeup]]

## 5. 다음 읽을 거리
- [[bugdb-v1-final-writeup]]
- [[bugdb-v2-final-writeup]]
