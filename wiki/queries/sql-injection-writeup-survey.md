---
title: SQL injection writeup survey
created: 2026-06-19
updated: 2026-06-21
type: query
tags: [ctf, web, survey, writeup, sql-injection, sqlite, sqli, injection]
sources: [https://github.com/NoamGariani/picoCTF-2024-writeup, https://github.com/DanArmor/picoCTF-2023-writeup]
confidence: high
---

# SQL injection writeup survey

## 참고 URL
- [NoamGariani/picoCTF-2024-writeup](https://github.com/NoamGariani/picoCTF-2024-writeup)
- [DanArmor/picoCTF-2023-writeup](https://github.com/DanArmor/picoCTF-2023-writeup)


## 1. 목적
SQLite SQL injection 계열 writeup을 비교해, 인증 우회와 `UNION`/`sqlite_master` 열거가 어떻게 연결되는지 정리합니다.

## 2. 비교 대상
| 문제 | 주된 primitive | 보조 primitive | 한 줄 요약 |
|---|---|---|---|
| More SQLi | union-based SQLite SQLi | login bypass | 로그인 우회 후 `sqlite_master`를 덤프합니다. |
| Startup Compagny | filter bypass SQLite SQLi | parameter tampering | HTML number 제한을 깨고 `GROUP_CONCAT`로 데이터를 회수합니다. |

## 3. 공통 관찰
1. UI에서 숫자만 받는다고 해도 서버가 검증하지 않으면 SQLi가 됩니다.
2. SQLite는 `sqlite_master`와 `GROUP_CONCAT()` 덕분에 짧은 payload로도 많은 정보를 뺄 수 있습니다.
3. 인증 우회와 데이터 열거는 별개의 단계가 아니라 같은 공격 흐름의 앞뒤입니다.

## 4. 관련 개념
- [[sql-injection]]
- [[sqlite-sqli-filter-bypass-ctf-patterns]]
- [[sqlite-union-based-sqli-ctf-patterns]]
- [[web-ctf-writeup-family-hub]]
- [[more-sqli-final-writeup]]
- [[startup-compagny-final-writeup]]

## 5. 다음 읽을 거리
- [[more-sqli-final-writeup]]
- [[startup-compagny-final-writeup]]
