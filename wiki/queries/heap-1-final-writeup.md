---
title: heap 1 — picoCTF 2024 pwn writeup
created: 2026-06-15
updated: 2026-06-15
type: query
tags: [ctf, pwn, heap-overflow, safe_var, adjacent-chunk, picoctf]
sources: [https://github.com/snwau/picoCTF-2024-Writeup/blob/main/Binary%20Exploitation/heap%201/heap%201.md, https://qiita.com/colza_/items/7d4176034f15c4d208fd, https://yun.ng/c/ctf/picoctf/pwn/heap-1]
confidence: high
---

# heap 1 — picoCTF 2024 pwn writeup

> `heap 1`는 `heap 0`의 변형으로, **heap overflow로 `safe_var`를 정확히 `pico`로 맞춰야 하는 문제**입니다.

## 핵심 요약
- `input_data`와 `safe_var`가 인접한 heap chunk로 배치됩니다.
- 32바이트를 넘기면 `safe_var`가 덮입니다.
- 목표는 `safe_var == "pico"` 입니다.

## 공격 흐름
1. 메뉴로 heap 상태를 확인합니다.
2. 패턴 입력으로 경계를 찾습니다.
3. 32바이트 뒤에 `pico`를 정확히 넣습니다.
4. flag 메뉴를 선택합니다.

## 학습 포인트
- 64-bit 환경에서는 오프셋 파악이 중요합니다.
- “힙은 안전하다”는 가정이 깨지는 대표 예시입니다.

## 방어 관점
- 길이 검사 없는 입력을 쓰지 않습니다.
- 검증 변수와 사용자 버퍼를 인접하게 배치하지 않습니다.

## 재현 절차
1. 인접한 힙 버퍼와 제어 변수의 배치를 확인합니다.
2. 덮어써야 하는 정확한 길이를 계산합니다.
3. 조건 만족 값으로 `safe_var`를 바꾸는 입력을 재현합니다.

```bash
# 힙 레이아웃과 입력 길이를 확인합니다.
./heap-1

# 디버깅 시 malloc/free 흐름을 관찰합니다.
gdb -q ./heap-1
```

## 관련 개념
- [[heap-overflow-adjacent-chunk-overwrite-ctf-patterns]]
