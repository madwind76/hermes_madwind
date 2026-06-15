---
title: SQLite SQLi filter bypass — CTF patterns
created: 2026-06-15
updated: 2026-06-15
type: concept
tags: [ctf, web, sqlite, sqli, filter-bypass, parameter-tampering]
sources: [https://ctftime.org/writeup/27015, https://ctf.zeyu2001.com/2021/picoctf/startup-company-180, https://github.com/Dvd848/CTFs/blob/master/2021_picoCTF/Web_Gauntlet_2.md]
confidence: high
---

# SQLite SQLi filter bypass — CTF patterns

## 1. 정의
**SQLite SQLi filter bypass**는 입력 필터가 따옴표, 공백, 특정 키워드만 막는 상황에서 SQLite 문법과 함수(`||`, `GROUP_CONCAT`, 서브쿼리, `sqlite_master`)를 이용해 필터를 우회하는 공격 패턴입니다.

## 2. 왜 중요한가
- SQLite는 메타데이터 테이블 `sqlite_master`가 매우 유용합니다.
- 짧은 payload로도 테이블명, 컬럼명, 데이터 덤프가 가능합니다.
- 숫자 입력, CAPTCHA, 길이 제한 등과 함께 자주 등장합니다.

## 3. 대표 우회 기법
1. 문자열 연결 연산자 `||` 활용
2. `GROUP_CONCAT()`로 다중 행 합치기
3. `sqlite_master`에서 테이블/스키마 열거
4. `LIMIT/OFFSET`로 레코드 분리 추출
5. `UNION` 대신 서브쿼리 기반 덤프

## 4. picoCTF 2021 `Startup Compagny`에서의 적용
이 문제는 숫자 입력처럼 보이는 필드를 `text`로 바꾸고, SQLite injection으로 `sqlite_master`와 `GROUP_CONCAT()`를 이용해 데이터를 빼내는 전형적인 예시입니다.

## 5. 같이 보면 좋은 페이지
- [[web-gauntlet-final-writeup]]
- [[startup-compagny-final-writeup]]
- [[web-gauntlet-2-final-writeup]]
- [[web-gauntlet-3-final-writeup]]
- [[sqlite-union-based-sqli-ctf-patterns]]

## 6. 방어 관점
- 문자열 결합 쿼리를 사용하지 않습니다.
- 서버에서 숫자/문자 형식을 재검증합니다.
- `sqlite_master`를 통한 내부 메타데이터 노출을 최소화합니다.
