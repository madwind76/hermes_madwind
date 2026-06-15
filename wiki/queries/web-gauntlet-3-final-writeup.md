---
title: Web Gauntlet 3 — picoCTF 2021 web writeup
created: 2026-06-15
updated: 2026-06-15
type: query
tags: [ctf, web, sqli, sqlite, filter-bypass, picoctf]
sources: [https://github.com/ZeroDayTea/PicoCTF-2021-Killer-Queen-Writeups/blob/main/WebExploitation/WebGauntlet3.md, https://github.com/HHousen/PicoCTF-2021/blob/master/Web%20Exploitation/Web%20Gauntlet%203/README.md, https://ctftime.org/task/15217, https://ctftime.org/writeup/27104]
confidence: high
---

# Web Gauntlet 3 — picoCTF 2021 web writeup

> `Web Gauntlet 3`는 **SQLite SQL Injection + 필터 우회 + 짧은 길이 제한** 문제입니다. 핵심은 `Web Gauntlet 2`와 같은 우회가 그대로 통하고, 이번에는 **25 characters total** 제한까지 만족해야 한다는 점입니다.

## 1. 한 줄 요약
- 로그인 폼이 SQL 쿼리를 직접 만듭니다.
- 필터는 `or`, `and`, `true`, `false`, `union`, `like`, `=`, `>`, `<`, `;`, `--`, `/*`, `*/`, `admin`을 막습니다.
- `Web Gauntlet 2`에서 쓴 SQLite 우회 페이로드가 그대로 통합니다.
- 최종 목표는 `admin`으로 로그인한 뒤 `filter.php`에서 flag를 보는 것입니다.

## 2. 문제 흐름
| 단계 | 관찰 | 의미 |
|------|------|------|
| 1 | 로그인 폼이 있음 | SQLi 가능성 |
| 2 | `filter.php`에 차단 목록이 표시됨 | 필터 우회가 핵심 |
| 3 | 입력 총 길이가 25자로 제한됨 | 짧은 payload 필요 |
| 4 | SQLite 전용 연산자 사용 가능 | DBMS 특화 우회 가능 |
| 5 | 로그인 성공 후 `filter.php` 접근 | flag가 소스 주석에 있음 |

## 3. 핵심 분석
이 문제는 `Web Gauntlet 2`의 연장선입니다. 차이점은 **입력 길이 제한**이 더 빡빡하다는 점뿐이고, 해결 아이디어는 같습니다.

- `||` 는 문자열 연결에 사용됩니다.
- `IS NOT` 는 `=` 없이도 참 조건을 만들 수 있습니다.
- `admin` 문자열은 `ad'||'min`처럼 쪼개서 복원합니다.
- 전체 payload 길이를 짧게 유지해야 합니다.

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
- `OR`/`AND` 없이도 로그인 조건을 통과할 수 있습니다.

### 4.3 조합 예시
```text
username: ad'||'min
password: a' IS NOT 'b
```

## 5. 공격자 관점
1. 필터 목록을 확인합니다.
2. `admin`을 문자열 연결로 분해합니다.
3. 비교 연산은 `IS NOT`으로 대체합니다.
4. 길이 제한 안에서 payload를 맞춥니다.
5. 로그인 성공 후 `filter.php`를 열어 flag를 확인합니다.

## 6. 방어자 관점
- 블랙리스트 필터는 우회되기 쉽습니다.
- Prepared Statement를 사용합니다.
- DBMS별 문법 차이를 고려한 테스트가 필요합니다.
- 로그인 성공 여부와 플래그 표시 로직을 분리해야 합니다.

## 7. 같이 보면 좋은 페이지
- [[web-gauntlet-2-3-sqlite-survey]]
- [[web-gauntlet-2-final-writeup]]
- [[sqlite-sqli-filter-bypass-ctf-patterns]]
- [[sql-injection]]
- [[parameter-tampering-ctf-patterns]]

## 8. 참고 소스
- [ZeroDayTea — WebGauntlet3](https://github.com/ZeroDayTea/PicoCTF-2021-Killer-Queen-Writeups/blob/main/WebExploitation/WebGauntlet3.md)
- [HHousen — Web Gauntlet 3](https://github.com/HHousen/PicoCTF-2021/blob/master/Web%20Exploitation/Web%20Gauntlet%203/README.md)
- [CTFtime task 15217](https://ctftime.org/task/15217)
- [CTFtime writeup 27104](https://ctftime.org/writeup/27104)
