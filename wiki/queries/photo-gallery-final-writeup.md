---
title: Photo Gallery — Hacker101 CTF writeup
created: 2026-06-19
updated: 2026-06-19
type: query
tags: [ctf, web, writeup, sql-injection, command-injection, source-inspection, rce]
sources: [https://raw.githubusercontent.com/Yahyahcini/hacker101-ctf-writeups/main/photo-gallery/README.md]
confidence: high
---

# Photo Gallery — Hacker101 CTF writeup

> SQL injection으로 DB 값을 읽고, 이어서 서버가 파일명 목록을 쉘 명령에 넣는 지점을 이용해 command injection까지 이어지는 Web writeup입니다.

## 참고 URL
- [raw source](https://raw.githubusercontent.com/Yahyahcini/hacker101-ctf-writeups/main/photo-gallery/README.md)


## 1. 한 줄 요약
- `/fetch?id=` 입력이 SQL injection에 취약합니다.
- DB에서 읽어온 파일명이 서버의 `du` 명령으로 전달됩니다.
- 결과적으로 source leak과 command injection이 같은 체인으로 연결됩니다.

## 2. 문제 구조
| 항목 | 내용 |
|---|---|
| 플랫폼 | Hacker101 CTF |
| 난이도 | Moderate |
| 핵심 아이디어 | SQL injection, source code leak, command injection |
| 관련 개념 | [[sql-injection]], [[command-injection-ctf-patterns]], [[source-inspection-minification-ctf-patterns]] |
| 관련 survey | [[hacker101-web-writeup-survey]] |

## 3. 공격면 정리
1. 첫 화면에서 `/fetch?id=1` 형태의 이미지 조회 요청을 확인합니다.
2. `id=3`에서 500 오류가 나면 입력이 SQL query에 직접 연결된 신호입니다.
3. `UNION SELECT 'main.py'`로 서버 소스를 읽어들입니다.
4. 소스에서 DB 값이 `shell=True` 명령에 들어가는 지점을 확인합니다.

## 4. 풀이 흐름
```sql
-- 1) SQL injection으로 파일명 대신 source 파일명을 반환하게 만듭니다.
/fetch?id=-1 UNION SELECT 'main.py' --

-- 2) 읽은 소스에서 command injection 경로를 확인합니다.
-- 예상 결과: 사진 파일명이 그대로 shell command에 들어갑니다.
```

## 5. 왜 취약한가
- SQL query가 문자열 결합으로 만들어집니다.
- DB에서 읽은 값이 쉘 명령 인자로 들어갑니다.
- `shell=True`는 작은 입력 오염도 전체 명령 실행으로 확장합니다.

## 6. 방어 관점
- prepared statements를 사용합니다.
- DB 결과를 쉘 문자열로 합치지 않습니다.
- command execution이 필요한 경우 `shell=False`와 allowlist를 사용합니다.

## 7. 다음 연결
- [[hacker101-web-writeup-survey]]
- [[sql-injection]]
- [[command-injection-ctf-patterns]]
- [[web-ctf-writeup-topic-map]]
