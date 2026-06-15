---
title: More SQLi — picoCTF 2023 web writeup
created: 2026-06-15
updated: 2026-06-15
type: query
tags: [ctf, web, sqli, sqlite, union-based-sqli, picoctf]
sources: [https://siunam321.github.io/ctf/picoCTF-2023/Web-Exploitation/More-SQLi/, https://github.com/DanArmor/picoCTF-2023-writeup/blob/main/Web%20Exploitation/More%20SQLi/More-SQLi.md, https://medium.com/@ha2755_16946/picoctf-more-sqli-write-up-9fa0c802051c, https://zarrarkolachi.medium.com/more-sqli-7a78e411fac5]
confidence: high
---

# More SQLi — picoCTF 2023 web writeup

> `More SQLi`는 **SQLite 기반 SQL injection**으로 로그인 우회를 시작한 뒤, `UNION SELECT`와 `sqlite_master`를 이용해 스키마를 열거하고 플래그 테이블에서 값을 추출하는 picoCTF 2023 Web 문제입니다.

## 1. 한 줄 요약
- 로그인 폼이 SQL에 직접 연결됩니다.
- `OR 1=1` 계열 payload로 인증을 우회할 수 있습니다.
- 이후 검색 기능에서 `UNION SELECT`를 사용해 추가 컬럼을 맞춥니다.
- `sqlite_version()`으로 DBMS가 SQLite임을 확인합니다.
- `sqlite_master`에서 테이블 구조를 읽고, `more_table`의 `flag`를 추출합니다.

## 2. 취약 흐름
| 단계 | 관찰 | 의미 |
|------|------|------|
| 1 | 로그인 응답이 SQL 쿼리 형태를 암시 | SQLi 후보 |
| 2 | `OR 1=1`로 로그인 우회 가능 | 인증 우회 |
| 3 | 검색 기능이 3개 컬럼 출력 | UNION SELECT 준비 |
| 4 | `sqlite_version()` 응답 | SQLite 확인 |
| 5 | `sqlite_master` 조회 | 스키마 열거 |
| 6 | `more_table.flag` 추출 | 최종 flag 획득 |

## 3. 핵심 분석
### 3.1 왜 취약한가
이 문제는 단순히 로그인만 뚫는 것이 아니라, **로그인 이후의 검색 기능까지 같은 SQLi 공격면**을 공유합니다. 즉, 인증 우회는 시작점이고, 진짜 핵심은 **UNION-based enumeration**입니다.

### 3.2 대표 payload
```sql
-- 로그인 우회 예시입니다.
' OR 1=1-- -
```

```sql
-- SQLite 여부를 확인합니다.
' UNION ALL SELECT sqlite_version(), NULL, NULL-- -
```

```sql
-- 테이블 구조를 확인합니다.
' UNION SELECT sql, NULL, NULL FROM sqlite_master-- -
```

```sql
-- flag가 들어 있는 테이블에서 값을 꺼냅니다.
' UNION SELECT id, flag, NULL FROM more_table-- -
```

## 4. 공격자 관점
1. 로그인 쿼리의 문자열 결합 여부를 확인합니다.
2. `OR 1=1`로 인증 우회를 먼저 시도합니다.
3. 출력 컬럼 수를 맞추기 위해 `NULL`을 사용합니다.
4. `sqlite_version()`으로 DBMS를 식별합니다.
5. `sqlite_master`에서 테이블과 컬럼 정의를 읽습니다.
6. 관심 테이블에서 flag 컬럼을 직접 조회합니다.

## 5. 방어자 관점
- 로그인과 검색 모두 **prepared statement**를 사용해야 합니다.
- 사용자 입력을 문자열 이어붙이기로 SQL에 넣지 말아야 합니다.
- UNION 기반 열거를 막으려면 에러 메시지를 최소화해야 합니다.
- DBMS 식별이 쉬운 응답을 줄이면 공격 난이도가 올라갑니다.

## 6. 같이 보면 좋은 페이지
- [[sql-injection]]
- [[sqlite-union-based-sqli-ctf-patterns]]
- [[web-ctf-writeup-parser-template]]
- [[web-gauntlet-2-final-writeup]]
- [[web-gauntlet-3-final-writeup]]

## 7. 참고 소스
- [siunam — More SQLi](https://siunam321.github.io/ctf/picoCTF-2023/Web-Exploitation/More-SQLi/)
- [DanArmor — More SQLi](https://github.com/DanArmor/picoCTF-2023-writeup/blob/main/Web%20Exploitation/More%20SQLi/More-SQLi.md)
- [HARI KISHAN REDDY ABBASANI — PicoCTF — More SQLi Write-Up](https://medium.com/@ha2755_16946/picoctf-more-sqli-write-up-9fa0c802051c)
- [Zarar Ahmed — More SQLI](https://zarrarkolachi.medium.com/more-sqli-7a78e411fac5)
