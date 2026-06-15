---
title: PATH hijacking / system() abuse — CTF patterns
created: 2026-06-15
updated: 2026-06-15
type: concept
tags: [ctf, binary-exploitation, path-hijack, system-abuse, setuid, shell, environment]
sources: [https://hackmd.io/@sal/HJtUdR5n1e, https://zenn.dev/tetsurou/articles/6fe4d41a3f6f48, https://medium.com/@erichdryn/hash-only-picoctf-writeup-e97779e8ee87]
confidence: high
---

# PATH hijacking / system() abuse — CTF patterns

## Step 1. 단어 풀이
- **PATH**: 셸이 실행 파일을 찾을 때 참조하는 디렉터리 목록입니다.
- **Hijacking**: 원래 실행되어야 할 프로그램 대신 공격자가 준비한 프로그램이 먼저 실행되도록 가로채는 행위입니다.
- **system()**: 셸을 호출해 문자열 명령을 실행하는 C 라이브러리 함수입니다.

## 한 문장 정의
이 패턴은 **setuid 또는 권한 상승 컨텍스트에서 `system()`이 절대경로 없는 명령을 실행할 때, `PATH`나 셸 동작을 이용해 공격자가 만든 프로그램을 먼저 실행시키는 문제 유형**입니다.

## 핵심 흐름
```text
privileged binary -> system("cmd") -> shell PATH lookup -> attacker-controlled binary/script -> unexpected action -> flag / shell
```

## 전문 설명
이 유형은 메모리 취약점이 없어도 발생할 수 있습니다.

1. `system()`이 셸을 띄웁니다.
2. 명령 문자열에 절대경로가 없으면 셸이 `PATH`를 검색합니다.
3. 공격자가 `md5sum`, `cat`, `sh`, `ls` 같은 이름의 프로그램을 앞에 배치할 수 있습니다.
4. setuid 권한이 유지되면, 공격자의 코드가 권한 컨텍스트 안에서 실행될 수 있습니다.

## 공격자 관점
- 먼저 프로그램이 어떤 명령을 실행하는지 확인합니다.
- `strace`, `gdb`, 문자열 검색, Ghidra로 `system()` 호출을 찾습니다.
- 실행 파일 이름이 절대경로인지 확인합니다.
- `PATH=.:$PATH` 또는 래퍼 스크립트로 우회 가능한지 봅니다.
- restricted shell(`rbash`)이 있으면 `sh`, `bash`, `busybox` 같은 대체 진입점을 찾습니다.

## 방어자 관점
- `system()` 사용을 피하고, `execve()` 계열로 바꿉니다.
- 명령은 반드시 **절대경로**로 지정합니다.
- setuid 바이너리에서는 환경변수를 초기화합니다.
- shell command composition 자체를 최소화합니다.

## 관련 패턴
- `hash-only-1` — 단순 PATH hijacking
- `hash-only-2` — PATH 제한 + restricted shell 우회
- `PATH`에 의존하는 백업 스크립트, cron, helper binary도 동일 계열입니다.

## 참고 링크
- [[hash-only-1-final-writeup]]
