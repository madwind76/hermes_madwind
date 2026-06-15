---
title: format string 1 — picoCTF 2024 pwn writeup
created: 2026-06-15
updated: 2026-06-15
type: query
tags: [ctf, pwn, format-string, stack-leak, endianness, picoctf]
sources: [https://github.com/snwau/picoCTF-2024-Writeup/blob/main/Binary%20Exploitation/format%20string%201/format%20string%201.md, https://hackmd.io/@Zzzzek/r14x13FRp, https://medium.com/@kenjikun/picoctf-binary-exploitation-2024-f5125b8874be]
confidence: high
---

# format string 1 — picoCTF 2024 pwn writeup

> `format string 1`는 전형적인 **format string leak** 문제입니다. `printf(user_input)`로 인해 스택 값을 읽어내고, 그중 flag가 들어 있는 값을 재조립합니다.

## 핵심 요약
- 프로그램은 여러 문자열을 메모리에 올려둡니다.
- 사용자 입력이 `printf()`의 포맷 문자열이 됩니다.
- `%p`를 반복하면 스택 위 값들을 덤프할 수 있습니다.

## 공격 흐름
1. `%p`를 여러 개 넣어 스택 출력 패턴을 봅니다.
2. flag가 섞여 있는 값의 위치를 찾습니다.
3. 출력된 hex 조각을 endian-aware하게 복원합니다.

## 학습 포인트
- `printf()`는 포맷 문자열 취약점의 대표 사례입니다.
- 64-bit 환경에서는 바이트 순서가 중요합니다.

## 방어 관점
- 사용자 입력을 포맷 문자열로 쓰지 않습니다.
- `printf("%s", user_input)`처럼 고정 포맷을 사용합니다.

## 재현 절차
1. 출력에 노출되는 포인터/주소가 있는지 확인합니다.
2. `%p` 같은 포맷을 이용해 메모리 누출을 재현합니다.
3. 누출된 값을 바탕으로 다음 단계 입력을 구성합니다.

```bash
# 포맷 문자열 입력을 직접 넣어 누출 여부를 확인합니다.
./format-string-1

# 필요하면 stdin으로 포맷 문자열을 전달합니다.
printf '%%p %%p %%p
' | ./format-string-1
```

## 관련 개념
- [[format-string-ctf-patterns]]
