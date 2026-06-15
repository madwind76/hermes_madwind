---
title: Web Gauntlet 2 — picoCTF 2021 web writeup
created: 2026-06-15
updated: 2026-06-15
type: query
tags: [ctf, web, sqli, sqlite, filter-bypass, picoctf]
sources: [https://github.com/Dvd848/CTFs/blob/master/2021_picoCTF/Web_Gauntlet_2.md, https://github.com/ZeroDayTea/PicoCTF-2021-Killer-Queen-Writeups/blob/main/WebExploitation/WebGauntlet2.md, https://hackmd.io/@fearnot/picoCTF_Web, https://ctftime.org/task/15218]
confidence: high
---

# Web Gauntlet 2 — picoCTF 2021 web writeup

> `Web Gauntlet 2`는 **SQLite SQL Injection + 필터 우회** 문제입니다. 단순한 `' OR 1=1`이 아니라, 차단된 키워드와 연산자를 피하면서 `admin` 조건을 만족시키는 것이 핵심입니다.

## 1. 한 줄 요약
- 로그인 폼이 SQL 쿼리를 직접 만듭니다.
- 필터는 `or`, `and`, `true`, `false`, `union`, `like`, `=`, `>`, `<`, `;`, `--`, `/*`, `*/`, `admin`을 막습니다.
- SQLite 전용 연산자 `||`, `glob`, `IS NOT`를 써서 우회합니다.

## 2. 문제 흐름
| 단계 | 관찰 | 의미 |
|------|------|------|
| 1 | 로그인 폼이 있음 | SQLi 가능성 |
| 2 | `filter.php`에 차단 목록이 표시됨 | 필터 우회가 핵심 |
| 3 | SQL query가 출력됨 | 구조 확인 가능 |
| 4 | `admin` 문자열이 막힘 | 문자열 분해 필요 |
| 5 | SQLite 연산자 사용 가능 | DBMS 특화 페이로드 가능 |
| 6 | `filter.php`에서 소스 확인 | flag가 주석에 있음 |

## 3. 핵심 분석
SQLite는 다른 DBMS와 문법 차이가 있어서, **표준 SQLi 페이로드가 막히는 상황에서도 대체 연산자**로 우회할 수 있습니다.

- `||` 는 문자열 연결에 사용됩니다.
- `glob` 는 패턴 매칭 연산자입니다.
- `IS NOT` 는 필터가 `=` 를 막아도 참 조건을 만들 수 있습니다.
- 제한된 길이 때문에 payload를 짧게 유지해야 합니다.

## 4. 대표 페이로드
### 4.1 사용자명 우회
```text
ad'||'min
```

- `admin` 문자열을 쪼개서 필터를 피합니다.
- SQLite에서 연결되면 `admin`이 됩니다.

### 4.2 비밀번호 조건 우회
```text
a' IS NOT 'b
```

- `=` 없이 참 조건을 만듭니다.
- 일반적인 `OR` 기반 우회보다 짧고 필터를 덜 건드립니다.

### 4.3 조합 예시
```text
username: ad'||'min
password: a' IS NOT 'b
```

## 5. 공격자 관점
1. 필터 문자열을 확인합니다.
2. 금지된 연산자를 대체할 SQLite 문법을 찾습니다.
3. username에서 `admin` 문자열을 분해합니다.
4. password는 `IS NOT` 같은 조건으로 우회합니다.
5. 로그인 성공 후 `filter.php`를 열어 flag를 확인합니다.

## 6. 방어자 관점
- 필터링만으로 SQLi를 막을 수 없습니다.
- Prepared Statement를 사용합니다.
- DBMS별 특수 연산자까지 고려한 화이트리스트 검증이 필요합니다.
- 인증 쿼리와 플래그 출력 로직을 분리합니다.

## 7. 같이 보면 좋은 페이지
- [[web-gauntlet-2-3-sqlite-survey]]
- [[sql-injection]]
- [[sqlite-sqli-filter-bypass-ctf-patterns]]
- [[parameter-tampering-ctf-patterns]]
- [[web-ctf-writeup-auth-session]]

## 8. 참고 소스
- [Dvd848 — Web Gauntlet 2](https://github.com/Dvd848/CTFs/blob/master/2021_picoCTF/Web_Gauntlet_2.md)
- [ZeroDayTea — WebGauntlet2](https://github.com/ZeroDayTea/PicoCTF-2021-Killer-Queen-Writeups/blob/main/WebExploitation/WebGauntlet2.md)
- [Fearnot — picoCTF Web writeup](https://hackmd.io/@fearnot/picoCTF_Web)
- [CTFtime task page](https://ctftime.org/task/15218)
