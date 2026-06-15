---
title: ret2win with arguments — CTF patterns
created: 2026-06-15
updated: 2026-06-15
type: concept
tags: [ctf, pwn, ret2win, function-arguments, x86, stack-layout, cdecl]
sources: [https://ctftime.org/writeup/32814, https://qiita.com/housu_jp/items/5e05dcb71901a3ca2604, https://musyokaian.medium.com/buffer-overflow-2-picoctf-2022-590cf7b7961f]
confidence: high
---

# ret2win with arguments — CTF patterns

## Step 1. 단어 풀이
- **ret2win**: 리턴 주소를 덮어 숨겨진 `win()` 함수로 보내는 기법입니다.
- **function arguments**: 호출할 함수에 넘기는 인자입니다.
- **stack layout**: 함수 호출 시 스택에 값이 배치되는 순서입니다.

## 한 문장 정의
이 패턴은 **함수 주소만 덮는 것으로 끝나지 않고, 스택에 인자 값까지 정확히 배치해야 flag가 나오는 문제 유형**입니다.

## 핵심 흐름
```text
overflow -> saved EIP overwrite -> place arguments -> win(arg1, arg2) -> flag
```

## 전문 설명
32-bit x86의 cdecl 호출 규약에서는 인자가 스택에 놓입니다. 그래서 `win()`의 주소로 돌아가는 것만으로는 부족하고, 리턴 주소 뒤에 `arg1`, `arg2`를 올바른 순서로 배치해야 합니다. 경우에 따라 filler 값이나 saved EBP 정렬용 값이 추가로 필요합니다.

## 공격자 관점
- 오프셋을 계산해 saved EIP 위치를 찾습니다.
- `win()` 함수 주소를 덮습니다.
- `arg1`, `arg2`를 리턴 주소 뒤에 붙입니다.
- 필요하면 filler를 넣어 스택 레이아웃을 맞춥니다.

## 방어자 관점
- 입력 길이 검증과 safe API 사용이 핵심입니다.
- `win()` 같은 검증 함수가 스택 인자만으로 동작하면 위험합니다.
- PIE, canary, NX를 함께 적용합니다.

## 관련 writeup
- [[buffer-overflow-2-final-writeup]]

## 같이 보면 좋은 개념
- [[stack-leak-ret2win-ctf-patterns]]
- [[ret2win-64bit-stack-alignment-ctf-patterns]]
- [[stack-canary-bruteforce-ctf-patterns]]
