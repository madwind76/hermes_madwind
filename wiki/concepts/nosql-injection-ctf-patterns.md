---
title: NoSQL injection — CTF patterns
created: 2026-06-15
updated: 2026-06-21
type: concept
tags: [ctf, web, nosql, mongodb, injection, auth]
sources: [https://blog.qz.sg/picoctf-2024-web-exploitation-writeups/, https://github.com/noamgariani11/picoCTF-2024-Writeup/blob/main/Web%20Exploitation/No-Sql-Injection.md, https://medium.com/@ahmednarmer1/ctf-day-34-8334270d207b]
confidence: high
---

# NoSQL injection — CTF patterns

## 참고 URL
- [blog.qz.sg](https://blog.qz.sg/picoctf-2024-web-exploitation-writeups/)
- [Original source](https://github.com/noamgariani11/picoCTF-2024-Writeup/blob/main/Web%20Exploitation/No-Sql-Injection.md)
- [medium.com](https://medium.com/@ahmednarmer1/ctf-day-34-8334270d207b)

## 1. 정의
**NoSQL injection**은 MongoDB 같은 NoSQL 백엔드에서, 문자열이 아니라 **JSON/객체 쿼리**를 주입해 인증이나 조회 조건을 바꾸는 패턴입니다. SQL injection과 목적은 비슷하지만, 문법과 오퍼레이터가 다릅니다.

## 2. 쉬운 비유
보통은 “아이디와 비밀번호를 적으세요”라고 적는 칸에 숫자 대신 **조건문**을 넣어 버리는 것과 비슷합니다. 서버가 그 값을 그냥 글자로 보지 않고, **검색 조건**으로 해석하면 로그인 문 자체가 느슨해집니다.

## 3. 자주 보이는 단서
| 단서 | 의미 |
|------|------|
| `JSON.parse()`가 로그인 입력에 붙어 있음 | 객체 주입 가능성 |
| `find()`, `findOne()`, `aggregate()`가 직접 호출됨 | 쿼리 오브젝트가 공격면 |
| `{"$ne": ...}`, `{"$gt": ...}` 같은 연산자 | 대표적인 우회 payload |
| `mongoose`, `MongoDB` | NoSQL injection 후보 |
| 인증 후 토큰/프로필이 응답에 바로 노출 | 우회 후 회수 지점 존재 |

## 4. 자주 쓰는 오퍼레이터
| 오퍼레이터 | 의미 | CTF에서의 용도 |
|------------|------|----------------|
| `$ne` | not equal | 거의 항상 참인 조건 만들기 |
| `$gt` | greater than | 비교식 우회 |
| `$regex` | 정규식 | 부분 일치 / 오라클 구성 |
| `$or` | OR | 조건 분기 우회 |
| `$where` | JavaScript 평가 | 일부 MongoDB 취약점에서 코드 실행 |

## 5. 기본 풀이 루프
```text
1) 백엔드가 MongoDB인지 확인합니다.
2) 입력이 문자열로 고정되는지, JSON으로 파싱되는지 봅니다.
3) 조건을 객체로 바꿀 수 있으면 `$ne`부터 시도합니다.
4) 로그인 우회가 되면 응답에 노출된 토큰/프로필을 확인합니다.
5) Base64/hex/URL decode가 필요한지 추가로 봅니다.
```

## 6. 공격자 관점
1. 입력 필드가 그대로 쿼리로 이어지는지 확인합니다.
2. 문자열 검증만 있을 때 객체를 넣어봅니다.
3. `email`이나 `password` 중 하나가 아닌 **둘 다** 조건을 우회해야 할 수 있습니다.
4. 인증 후 응답 바디와 헤더를 끝까지 확인합니다.

## 7. 방어자 관점
- 사용자 입력을 JSON 오브젝트로 자동 변환하지 않습니다.
- ORM의 쿼리 바인딩 규칙을 명확히 강제합니다.
- 허용되지 않은 MongoDB operator를 거부합니다.
- 인증 결과와 민감한 토큰을 같은 응답에 넣지 않습니다.

## 8. 같이 보면 좋은 페이지
- [[no-sql-injection-final-writeup]]
- [[web-ctf-writeup-auth-session]]
- [[sql-injection]]
- [[parameter-tampering-ctf-patterns]]
- [[base64-decoding-ctf-patterns]]
