---
title: BugDB v1 — Hacker101 CTF writeup
created: 2026-06-19
updated: 2026-06-19
type: query
tags: [ctf, web, writeup, api, api-security, broken-access-control, authorization, injection]
sources: [https://raw.githubusercontent.com/Yahyahcini/hacker101-ctf-writeups/main/BugDB%20v1/README.md]
confidence: high
---

# BugDB v1 — Hacker101 CTF writeup

> GraphQL introspection으로 schema를 읽고, 권한 없는 bug listing query로 모든 bug를 덤프하는 writeup입니다.

## 참고 URL
- [raw source](https://raw.githubusercontent.com/Yahyahcini/hacker101-ctf-writeups/main/BugDB%20v1/README.md)


## 1. 한 줄 요약
- GraphQL endpoint를 찾습니다.
- introspection으로 `Query` 타입과 bug 관련 필드를 확인합니다.
- `allBugs`/`bugs` 계열 query로 flag가 들어 있는 text를 읽습니다.

## 2. 문제 구조
| 항목 | 내용 |
|---|---|
| 플랫폼 | Hacker101 CTF |
| 난이도 | Easy |
| 핵심 아이디어 | introspection, over-permissive query, missing authorization |
| 관련 개념 | [[api-security-defense]], [[broken-access-control-defense]], [[web-ctf-writeup-family-hub]] |
| 관련 survey | [[graphql-api-writeup-survey]] |

## 3. 공격면 정리
1. 브라우저 개발자 도구나 Burp로 `POST /graphql` 요청을 찾습니다.
2. introspection query를 보내 schema를 확인합니다.
3. `Query` 타입에서 bug 관련 field를 찾습니다.
4. 전체 bug를 반환하는 query를 호출해 hidden flag를 찾습니다.

## 4. 풀이 흐름
```graphql
# 1) schema 탐색용 introspection query
{
  __schema {
    queryType { name }
    types { name }
  }
}

# 2) bug 목록을 읽는 query
{
  allBugs {
    id
    title
    text
    reporter { username }
  }
}
```

## 5. 왜 취약한가
- schema가 노출되어 공격자가 field를 빠르게 찾습니다.
- query 결과에 권한 검사가 부족합니다.
- 민감한 text가 일반 bug 데이터와 함께 반환됩니다.

## 6. 방어 관점
- GraphQL introspection을 운영 환경에서 제한합니다.
- resolver마다 object-level authorization을 넣습니다.
- 민감 데이터는 별도 권한 경로로 분리합니다.

## 7. 다음 연결
- [[graphql-api-writeup-survey]]
- [[api-security-defense]]
- [[broken-access-control-defense]]
