---
title: Environment / command abuse — CTF patterns
created: 2026-06-15
updated: 2026-06-15
type: concept
sources: [queries/vne-final-writeup.md]
confidence: medium
tags: [ctf, pwn, environment, shell, command-abuse]
---

# Environment / command abuse — CTF patterns

> 환경 변수, 셸, 상대경로 호출을 악용하는 패턴입니다.

## 핵심 아이디어
- `system()`은 셸을 호출하므로 환경 변수의 영향을 받습니다.
- PATH 우선순위가 높으면 같은 이름의 명령을 가로챌 수 있습니다.
- setuid 프로그램은 특히 환경 변수 검증이 중요합니다.

## 자주 보이는 형태
- 가짜 `ls`, `cat`, `md5sum` 실행 파일로 가로채기
- `PATH` 조작
- `SHELL`, `IFS` 등의 환경 변수 의존
- `popen()`/`system()` 호출 우회

## picoCTF 예시
- [[vne-final-writeup]]

## 방어
- 절대경로를 사용합니다.
- 필요 없는 환경 변수를 제거합니다.
- 셸 실행 대신 직접 exec 계열 호출을 사용합니다.
