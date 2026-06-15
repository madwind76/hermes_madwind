---
title: Web Gauntlet 2/3 — SQLite SQLi Survey
created: 2026-06-15
updated: 2026-06-15
type: query
tags: [ctf, web, sqli, sqlite, filter-bypass, survey, picoctf]
sources: [https://github.com/Dvd848/CTFs/blob/master/2021_picoCTF/Web_Gauntlet_2.md, https://github.com/ZeroDayTea/PicoCTF-2021-Killer-Queen-Writeups/blob/main/WebExploitation/WebGauntlet2.md, https://github.com/ZeroDayTea/PicoCTF-2021-Killer-Queen-Writeups/blob/main/WebExploitation/WebGauntlet3.md, https://github.com/HHousen/PicoCTF-2021/blob/master/Web%20Exploitation/Web%20Gauntlet%203/README.md, https://ctftime.org/task/15217, https://ctftime.org/task/15218]
confidence: high
---

# Web Gauntlet 2/3 — SQLite SQLi Survey

> `Web Gauntlet 2`와 `Web Gauntlet 3`는 같은 계열의 **SQLite SQL Injection + 필터 우회** 문제입니다. 3번은 2번의 풀이를 거의 그대로 쓰되, **더 짧은 입력 제한**이 추가된 형태로 보면 이해가 쉽습니다.

> 연결 허브: [[web-ctf-writeup-curation]] · [[web-ctf-writeup-topic-map]]

## 1. 빠른 결론

- 두 문제 모두 `admin` 문자열 차단과 일반적인 SQL 키워드 차단을 동시에 건드립니다.
- 핵심 우회는 `||` 문자열 연결과 `IS NOT` 조건입니다.
- `Web Gauntlet 3`는 `Web Gauntlet 2`보다 **입력 총 길이 제한**이 더 빡빡합니다.
- 따라서 2번의 풀이를 먼저 이해하고, 3번은 "같은 풀이를 더 짧게 압축한 버전"으로 보면 됩니다.

## 2. 문제별 비교

| 페이지 | 핵심 패턴 | 추가 제약 | 풀이 포인트 |
|------|-----------|-----------|------------|
| [[web-gauntlet-2-final-writeup]] | SQLite SQLi / filter bypass | `admin` 차단, 일반 SQL 키워드 차단 | `ad'||'min` + `a' IS NOT 'b` |
| [[web-gauntlet-3-final-writeup]] | SQLite SQLi / filter bypass | 25 characters total | 2번과 같은 우회를 더 짧게 적용 |

## 3. 왜 같은 풀이가 통하나

1. 두 문제 모두 `SQLite`를 사용합니다.
2. 필터는 `or`, `and`, `union`, `like`, `=` 같은 흔한 키워드를 막습니다.
3. `admin` 문자열은 `ad'||'min`처럼 분해해 복원할 수 있습니다.
4. `IS NOT`은 `=` 없이도 참 조건을 만드는 데 유용합니다.
5. 결과적으로 2번의 해결책이 3번에서도 동작합니다.

## 4. 권장 풀이 순서

1. **Web Gauntlet 2**를 먼저 풉니다.
2. 필터 목록과 SQLite 특성을 이해합니다.
3. 같은 페이로드가 **Web Gauntlet 3**에서 길이 제한에 걸리는지 확인합니다.
4. 필요한 경우 payload 길이를 줄이는 방식으로 재사용합니다.

## 5. 같이 보면 좋은 페이지

- [[web-gauntlet-2-final-writeup]]
- [[web-gauntlet-3-final-writeup]]
- [[sqlite-sqli-filter-bypass-ctf-patterns]]
- [[sql-injection]]
- [[parameter-tampering-ctf-patterns]]

## 6. 참고 소스

- [Dvd848 — Web Gauntlet 2](https://github.com/Dvd848/CTFs/blob/master/2021_picoCTF/Web_Gauntlet_2.md)
- [ZeroDayTea — WebGauntlet2](https://github.com/ZeroDayTea/PicoCTF-2021-Killer-Queen-Writeups/blob/main/WebExploitation/WebGauntlet2.md)
- [ZeroDayTea — WebGauntlet3](https://github.com/ZeroDayTea/PicoCTF-2021-Killer-Queen-Writeups/blob/main/WebExploitation/WebGauntlet3.md)
- [HHousen — Web Gauntlet 3](https://github.com/HHousen/PicoCTF-2021/blob/master/Web%20Exploitation/Web%20Gauntlet%203/README.md)
- [CTFtime task 15217](https://ctftime.org/task/15217)
- [CTFtime task 15218](https://ctftime.org/task/15218)
