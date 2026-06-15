---
title: format string 2 — picoCTF 2024 pwn writeup
created: 2026-06-15
updated: 2026-06-15
type: query
tags: [ctf, pwn, format-string, arbitrary-write, global-variable, picoctf]
sources: [https://systemweakness.com/format-string-2-picoctf-2024-deep-dive-into-the-logic-behind-payload-construction-3acb72ea6cd8, https://hackmd.io/@Zzzzek/r14x13FRp, https://github.com/Cajac/picoCTF-Writeups/blob/main/picoCTF_2024/Binary_Exploitation/format_string_2.md]
confidence: high
---

# format string 2 — picoCTF 2024 pwn writeup

> `format string 2`는 **`printf(buf)`와 `%n`을 이용해 전역 변수 `sus`를 바꾸는 문제**입니다.

## 핵심 요약
- `sus` 초기값은 `0x21737573`입니다.
- 목표 값은 `0x67616c66`입니다.
- PIE가 없어서 전역 변수 주소는 고정입니다.

## 공격 흐름
1. `sus`의 주소를 확인합니다.
2. format string offset을 찾습니다.
3. `%n` 계열 write로 `sus` 값을 덮습니다.
4. 조건문이 참이 되면 flag를 출력합니다.

## 학습 포인트
- format string은 읽기뿐 아니라 쓰기도 가능합니다.
- `%n`, `%hn`, `%hhn`은 강력하지만 매우 위험합니다.

## 방어 관점
- `printf(user_input)`를 쓰지 않습니다.
- 전역 상태를 사용자 입력으로 바꾸지 않도록 합니다.

## 재현 절차
1. 출력과 쓰기 모두 가능한지 확인합니다.
2. `%n` 계열을 쓸 수 있는지 테스트합니다.
3. 글로벌 변수나 플래그 조건을 원하는 값으로 맞춥니다.

```bash
# 포맷 문자열 입력으로 읽기/쓰기 동작을 확인합니다.
./format-string-2

# 예시: 포맷 문자열을 stdin으로 전달합니다.
printf '%%p %%p %%n
' | ./format-string-2
```

## 관련 개념
- [[format-string-ctf-patterns]]
