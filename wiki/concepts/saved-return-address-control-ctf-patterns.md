---
title: Saved return address control — CTF patterns
created: 2026-06-15
updated: 2026-06-15
type: concept
tags: [ctf, pwn, ret2win, stack-overflow, saved-return-address, buffer-overflow, nx, pie]
sources: [https://colej.net/picoctf-2022-buffer-overflow-1, https://medium.com/@muranyi.levente/picoctf-2022-buffer-overflow-1-3e48f4a61876, https://ctftime.org/writeup/32919]
confidence: high
---

# Saved return address control — CTF patterns

## Step 1. 단어 풀이
- **Saved return address**: 함수가 끝난 뒤 돌아갈 주소입니다.
- **Control**: 이 값을 공격자가 원하는 주소로 바꾸는 것입니다.
- **Ret2win**: 반환 주소를 `win()` 함수로 바꿔 flag를 얻는 기법입니다.

## 한 문장 정의
이 패턴은 **입력 버퍼를 overflow해 saved return address를 덮고, 숨겨진 `win()` 또는 `flag()` 함수로 흐름을 돌리는 가장 기본적인 pwn 유형**입니다.

## 핵심 흐름
```text
overflow -> saved return address overwrite -> win() -> flag
```

## 전문 설명
32-bit든 64-bit든, 함수의 리턴 주소를 공격자가 제어하면 실행 흐름을 원하는 곳으로 보낼 수 있습니다. 보호 장치가 없거나 약하면 가장 먼저 시도하는 기본형 exploit입니다.

## 공격자 관점
- 오프셋을 찾아 saved return address까지 도달합니다.
- `win()` 주소를 넣습니다.
- 필요하면 리턴 직후의 정렬 문제나 인자 배치도 확인합니다.

## 방어자 관점
- `gets`, `strcpy`, `scanf %s` 같은 위험 API를 사용하지 않습니다.
- canary, PIE, NX를 함께 적용합니다.
- 코드 리뷰 시 반환 주소를 덮을 수 있는 입력 경로를 우선 찾습니다.

## 관련 writeup
- [[buffer-overflow-1-final-writeup]]

## 같이 보면 좋은 개념
- [[ret2win-with-arguments-ctf-patterns]]
- [[ret2win-64bit-stack-alignment-ctf-patterns]]
- [[stack-canary-bruteforce-ctf-patterns]]
