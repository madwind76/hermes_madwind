---
title: Intentional crash / signal handler — CTF patterns
created: 2026-06-15
updated: 2026-06-15
type: concept
tags: [ctf, pwn, signal-handler, intentional-crash, segfault, buffer-overflow, gets, strcpy]
sources: [https://medium.com/@muranyi.levente/picoctf-2022-buffer-overflow-0-f26e5fc9b31e, https://dev.to/shalintha/exploiting-buffer-overflow-0-step-by-step-picoctf-walkthrough-p83, https://medium.com/@hchilcote/picoctf-buffer-overflow-0-write-up-82dc8ea3bea0]
confidence: high
---

# Intentional crash / signal handler — CTF patterns

## Step 1. 단어 풀이
- **Intentional crash**: 프로그램을 일부러 비정상 종료시키는 것입니다.
- **Signal handler**: SIGSEGV 같은 예외 신호가 오면 실행되는 함수입니다.
- **Segfault**: 잘못된 메모리 접근으로 나는 크래시입니다.

## 한 문장 정의
이 패턴은 **제어 흐름을 직접 빼앗는 대신, 크래시를 유도해 예외 처리 코드가 flag를 출력하도록 만드는 문제 유형**입니다.

## 핵심 흐름
```text
overflow -> segfault -> signal handler -> flag
```

## 전문 설명
일부 CTF 바이너리는 예외를 잡는 핸들러를 가지고 있습니다. 공격자는 입력을 길게 보내 크래시를 발생시키고, 그 크래시를 계기로 정상 실행 경로가 아닌 예외 처리 경로가 flag를 출력하도록 유도합니다.

## 공격자 관점
- 입력 길이를 늘려 overflow를 유도합니다.
- 정확한 오프셋 대신 크래시 자체를 목표로 합니다.
- signal handler가 민감 정보를 출력하는지 확인합니다.

## 방어자 관점
- signal handler에서 민감한 데이터를 출력하지 않습니다.
- unsafe API를 제거합니다.
- 크래시 후 상태가 안전하게 복구되는지 점검합니다.

## 관련 writeup
- [[buffer-overflow-0-final-writeup]]

## 같이 보면 좋은 개념
- [[saved-return-address-control-ctf-patterns]]
- [[stack-canary-bruteforce-ctf-patterns]]
