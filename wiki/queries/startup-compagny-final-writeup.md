---
title: Startup Compagny — picoCTF 2021 web writeup
created: 2026-06-15
updated: 2026-06-15
type: query
tags: [ctf, web, sqlite, sqli, filter-bypass, parameter-tampering, picoctf]
sources: [https://ctftime.org/writeup/27015, https://ctftime.org/writeup/27374, https://ctf.zeyu2001.com/2021/picoctf/startup-company-180]
confidence: high
---

# Startup Compagny — picoCTF 2021 web writeup

> `Startup Compagny`는 숫자 입력을 **HTML `number` 타입에만 의존**하게 만들어 둔 뒤, 브라우저 개발자도구로 `text`로 바꾸고 SQLite SQL injection을 수행하는 picoCTF 2021 Web 문제입니다. 핵심은 **클라이언트 측 제한은 방어가 아니다**라는 점과, SQLite에서 `GROUP_CONCAT`/서브쿼리를 이용해 데이터를 빠르게 덤프하는 방법입니다.

## 1. 한 줄 요약
- 겉보기에는 숫자만 넣을 수 있는 입력입니다.
- 하지만 HTML 속성은 클라이언트에서 얼마든지 바꿀 수 있습니다.
- 입력을 SQL 문자열에 그대로 붙이면 SQLite injection이 됩니다.

## 2. 문제 흐름
| 단계 | 관찰 | 의미 |
|------|------|------|
| 1 | `moneys` 같은 숫자 입력 필드가 있음 | 숫자만 받는 것처럼 보임 |
| 2 | DevTools에서 input type을 `text`로 변경 가능 | 클라이언트 제한 우회 |
| 3 | `' || ... || '` 형태로 문자열 연결이 먹힘 | SQLite injection 가능 |
| 4 | `sqlite_master`에서 테이블명 추출 가능 | 스키마 열거 가능 |
| 5 | `GROUP_CONCAT()`로 컬럼/데이터 덤프 | flag 위치 확인 가능 |

## 3. 핵심 분석
### 3.1 왜 주입이 되나
```sql
-- 숫자 입력처럼 보여도, 서버가 문자열을 그대로 SQL에 연결하면 취약합니다.
-- 예상 결과: 따옴표와 concatenation을 이용해 쿼리 구조를 바꿀 수 있습니다.
' || (SELECT GROUP_CONCAT(tbl_name) FROM sqlite_master) || '
```

### 3.2 SQLite에서 자주 쓰는 함수
```sql
-- 예상 결과: 여러 행을 한 번에 합쳐 출력합니다.
GROUP_CONCAT(tbl_name)
```

```sql
-- 예상 결과: 스키마 SQL을 모아서 컬럼명까지 볼 수 있습니다.
SELECT GROUP_CONCAT(sql) FROM sqlite_master WHERE type!='meta' AND sql NOT NULL
```

### 3.3 대표 페이로드 흐름
1. 입력 타입을 `text`로 바꿉니다.
2. 짧은 문자열 조합으로 반응을 확인합니다.
3. `sqlite_master`를 이용해 테이블명을 확인합니다.
4. `GROUP_CONCAT(sql)`로 테이블 구조를 봅니다.
5. 최종적으로 사용자/비밀번호 컬럼에서 flag를 찾습니다.

## 4. 공격자 관점
- 숫자 제한, maxlength, client-side validation은 보안 경계가 아닙니다.
- SQLite는 페이로드가 짧아도 강력한 메타데이터 접근이 가능합니다.
- `GROUP_CONCAT`는 데이터가 여러 행으로 나뉘어도 한 번에 회수하는 데 유용합니다.

## 5. 방어자 관점
- 입력 타입은 UI일 뿐이므로 서버에서 형식을 다시 검증해야 합니다.
- SQL은 반드시 prepared statement로 작성합니다.
- 클라이언트에서 숫자 입력만 받더라도 서버는 문자열 삽입을 경계해야 합니다.
- SQLite 메타데이터 접근을 허용하지 않는 구조로 쿼리를 설계합니다.

## 6. 같이 보면 좋은 페이지
- [[sqlite-sqli-filter-bypass-ctf-patterns]]
- [[sqlite-union-based-sqli-ctf-patterns]]
- [[web-gauntlet-2-final-writeup]]
- [[web-gauntlet-3-final-writeup]]

## 7. 참고 소스
- [CTFtime — Startup Compagny](https://ctftime.org/writeup/27015)
- [CTFtime — Startup Compagny](https://ctftime.org/writeup/27374)
- [Zeyu CTFs — Startup Company](https://ctf.zeyu2001.com/2021/picoctf/startup-company-180)
