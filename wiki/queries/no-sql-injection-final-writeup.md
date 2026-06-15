---
title: No SQL Injection — picoCTF 2024 web writeup
created: 2026-06-15
updated: 2026-06-15
type: query
tags: [ctf, web, nosql, mongodb, injection, auth, picoctf]
sources: [https://blog.qz.sg/picoctf-2024-web-exploitation-writeups/, https://github.com/noamgariani11/picoCTF-2024-Writeup/blob/main/Web%20Exploitation/No-Sql-Injection.md, https://hack.nikkei.com/blog/ctf_pico202403/, https://medium.com/@ahmednarmer1/ctf-day-34-8334270d207b, https://infosecwriteups.com/picoctf-2024-write-up-web-992348f48b99]
confidence: high
---

# No SQL Injection — picoCTF 2024 web writeup

> `No SQL Injection`은 **MongoDB NoSQL injection**으로 로그인 검증을 우회하고, 응답에 노출된 토큰 값을 Base64 디코딩해 플래그를 얻는 picoCTF 2024 Web 문제입니다.

## 1. 한 줄 요약
- 로그인 핸들러가 사용자 입력을 **JSON 객체로 해석**합니다.
- MongoDB `find()` 쿼리에 들어가는 값이 문자열이 아니라 **연산자 객체**가 될 수 있습니다.
- `{"$ne": null}` 또는 비슷한 payload로 인증을 우회할 수 있습니다.
- 로그인 후 응답에 포함된 `token` 필드가 Base64 인코딩된 플래그를 담고 있습니다.

## 2. 취약 흐름
| 단계 | 관찰 | 의미 |
|------|------|------|
| 1 | 소스가 TypeScript / MongoDB(mongoose) 기반 | NoSQL 쿼리 오브젝트가 후보 |
| 2 | 로그인 입력이 `{...}` 형태면 JSON.parse 됨 | 문자열이 아니라 객체가 됨 |
| 3 | `find({ email: ..., password: ... })`에 객체가 그대로 전달됨 | MongoDB operator injection 가능 |
| 4 | `token` 필드가 응답에 노출됨 | 인증 후 플래그 회수 가능 |
| 5 | Base64 decode | 최종 flag 획득 |

## 3. 핵심 분석
### 3.1 왜 취약한가
NoSQL injection은 SQL 문법을 깨는 방식이 아니라, **JSON 기반 쿼리 객체 자체를 조작**하는 방식입니다. MongoDB에서 `{ "$ne": null }` 같은 객체는 “null이 아닌 값”을 의미하므로, 로그인 조건이 느슨하면 곧바로 인증 우회로 이어집니다.

### 3.2 공격 예시
```ts
// 서버 측 개념 예시입니다.
// email/password가 "{...}" 형태면 JSON 객체로 해석되어 find()에 들어갈 수 있습니다.
const users = await User.find({
  email: email.startsWith("{") && email.endsWith("}") ? JSON.parse(email) : email,
  password: password.startsWith("{") && password.endsWith("}") ? JSON.parse(password) : password
});
```

```json
// 로그인 폼에 넣는 대표 payload 예시입니다.
{"$ne": null}
```

## 4. 공격자 관점
1. 소스에서 DB 종류를 확인합니다.
2. 입력이 JSON으로 해석되는지 봅니다.
3. `find()` 또는 유사 쿼리에 객체를 주입합니다.
4. 로그인 우회가 되면 응답의 `token` 필드를 확인합니다.
5. Base64 디코딩으로 플래그를 복원합니다.

## 5. 방어자 관점
- 로그인 입력은 문자열로 엄격히 검증해야 합니다.
- `{...}` 형태를 JSON으로 자동 파싱하지 않는 편이 안전합니다.
- MongoDB 쿼리에는 허용된 스키마만 전달해야 합니다.
- 인증 로직과 데이터 조회 로직을 분리해야 합니다.

## 6. 같이 보면 좋은 페이지
- [[web-ctf-writeup-auth-session]]
- [[nosql-injection-ctf-patterns]]
- [[sql-injection]]
- [[base64-decoding-ctf-patterns]]
- [[parameter-tampering-ctf-patterns]]

## 7. 참고 소스
- [PicoCTF 2024 — Web Exploitation Writeups](https://blog.qz.sg/picoctf-2024-web-exploitation-writeups/)
- [noamgariani11/picoCTF-2024-Writeup — No-Sql-Injection.md](https://github.com/noamgariani11/picoCTF-2024-Writeup/blob/main/Web%20Exploitation/No-Sql-Injection.md)
- [HACK The Nikkei — picoCTF 2024 Writeup](https://hack.nikkei.com/blog/ctf_pico202403/)
- [CTF Day(34) — picoCTF Web Exploitation: No Sql Injection](https://medium.com/@ahmednarmer1/ctf-day-34-8334270d207b)
