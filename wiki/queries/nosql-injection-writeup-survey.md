---
title: NoSQL injection writeup survey
created: 2026-06-19
updated: 2026-06-21
type: query
tags: [ctf, web, survey, writeup, nosql, mongodb, injection, auth]
sources: [https://blog.qz.sg/picoctf-2024-web-exploitation-writeups/, https://blog.0daylabs.com/2016/09/05/mongo-db-password-extraction-mmactf-100/]
confidence: high
---

# NoSQL injection writeup survey

## 참고 URL
- [blog.qz.sg](https://blog.qz.sg/picoctf-2024-web-exploitation-writeups/)
- [blog.0daylabs.com](https://blog.0daylabs.com/2016/09/05/mongo-db-password-extraction-mmactf-100/)


## 1. 목적
MongoDB NoSQL injection이 SQL injection과 어떻게 다른지, JSON 객체 기반 쿼리 우회를 비교합니다.

## 2. 비교 대상
| 문제 | 주된 primitive | 보조 primitive | 한 줄 요약 |
|---|---|---|---|
| No SQL Injection (picoCTF 2024) | MongoDB $ne operator bypass | token decode | `{"$ne": null}`로 로그인을 우회하고 응답의 token을 Base64 디코딩합니다. |
| MMACTF 2016 flag-shop | blind NoSQL injection | password extraction | MongoDB regex injection으로 비밀번호를 한 글자씩 추출합니다. |

## 3. 공통 관찰
1. NoSQL injection은 SQL 문법을 깨는 게 아니라, JSON operator 객체를 주입하는 방식입니다.
2. `$ne`, `$regex`, `$gt` 등 MongoDB 연산자가 공격에 사용됩니다.
3. SQL과 달리 쿼리 오브젝트가 그대로 전달될 때 주입이 성립합니다.

## 4. 관련 개념
- [[nosql-injection-ctf-patterns]]
- [[sql-injection]]
- [[web-ctf-writeup-auth-session]]
- [[web-ctf-writeup-family-hub]]
- [[no-sql-injection-final-writeup]]

## 5. 다음 읽을 거리
- [[no-sql-injection-final-writeup]]
