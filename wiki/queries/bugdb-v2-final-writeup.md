---
title: BugDB v2 — Hacker101 CTF writeup
created: 2026-06-19
updated: 2026-06-19
type: query
tags: [ctf, web, writeup, api, api-security, broken-access-control, authorization, login, tampering]
sources: [https://raw.githubusercontent.com/Yahyahcini/hacker101-ctf-writeups/main/BugDB%20v2/README.md]
confidence: high
---

# BugDB v2 — Hacker101 CTF writeup

> GraphQL mutation을 악용해 private bug의 상태를 바꾸고, 다시 query해서 flag를 읽는 writeup입니다.

## 참고 URL
- [raw source](https://raw.githubusercontent.com/Yahyahcini/hacker101-ctf-writeups/main/BugDB%20v2/README.md)


## 1. 한 줄 요약
- schema에서 `Mutation` root를 확인합니다.
- hidden bug의 ID 패턴을 추론합니다.
- `modifyBug` 계열 mutation으로 private 값을 false로 바꿉니다.
- 다시 query하여 flag를 읽습니다.

## 2. 문제 구조
| 항목 | 내용 |
|---|---|
| 플랫폼 | Hacker101 CTF |
| 난이도 | Easy |
| 핵심 아이디어 | GraphQL mutation abuse, predictable IDs, broken authorization |
| 관련 개념 | [[api-security-defense]], [[broken-access-control-defense]], [[web-ctf-writeup-family-hub]] |
| 관련 survey | [[graphql-api-writeup-survey]] |

## 3. 공격면 정리
1. GraphQL UI 또는 introspection으로 `Query`와 `Mutation` root를 확인합니다.
2. 보이는 bug의 ID 패턴을 decode해 내부 ID 형식을 유추합니다.
3. 다른 bug에 대해 `private: false` mutation을 시도합니다.
4. 다시 bug listing query를 실행해 flag가 들어 있는 record를 읽습니다.

## 4. 풀이 흐름
```graphql
# 1) 보이는 bug와 user를 확인합니다.
{
  allUsers { id username }
  allBugs { id text private }
}

# 2) private 플래그를 바꾸는 mutation
mutation {
  modifyBug(id: 2, private: false) {
    ok
  }
}
```

## 5. 왜 취약한가
- mutation에 object-level authorization이 없습니다.
- 내부 ID가 예측 가능하면 숨은 object를 찾기 쉽습니다.
- private flag가 비즈니스 로직의 핵심인데 검증이 약합니다.

## 6. 방어 관점
- mutation마다 소유권과 role 체크를 수행합니다.
- 내부 ID는 예측 불가능한 식별자를 사용합니다.
- 민감 상태 변경은 별도 검증 레이어를 둡니다.

## 7. 다음 연결
- [[graphql-api-writeup-survey]]
- [[api-security-defense]]
- [[broken-access-control-defense]]
