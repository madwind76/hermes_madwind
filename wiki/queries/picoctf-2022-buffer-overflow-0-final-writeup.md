---
title: buffer overflow 0 — picoCTF 2022 pwn writeup
created: 2026-06-24
updated: 2026-06-24
type: query
tags: [ctf, picoctf, picoctf2022, pwn, buffer-overflow, stack-overflow, sigsegv]
sources: [https://raw.githubusercontent.com/Cajac/picoCTF-Writeups/main/picoCTF_2022/Binary_Exploitation/buffer_overflow_0.md, https://github.com/Cajac/picoCTF-Writeups/blob/main/picoCTF_2022/Binary_Exploitation/buffer_overflow_0.md]
confidence: medium
---

# buffer overflow 0 — picoCTF 2022 pwn writeup

## 참고 URL
- [Cajac raw writeup](https://raw.githubusercontent.com/Cajac/picoCTF-Writeups/main/picoCTF_2022/Binary_Exploitation/buffer_overflow_0.md)
- [Cajac blob writeup](https://github.com/Cajac/picoCTF-Writeups/blob/main/picoCTF_2022/Binary_Exploitation/buffer_overflow_0.md)

## 핵심 요약
`gets()`와 더 작은 내부 버퍼 조합으로 스택을 쉽게 넘길 수 있는 입문용 버퍼 오버플로우 문제입니다.
이 문제는 오버플로우 자체보다 `SIGSEGV` 핸들러가 플래그를 출력한다는 점이 핵심이므로, 충분히 길게 입력해 충돌을 유도하면 됩니다.

## 풀이 메모
1. `buf1`과 `buf2`의 크기 차이를 확인합니다.
2. `gets()`에 충분히 긴 문자열을 넣어 `strcpy()` 경로에서 오버플로우를 유도합니다.
3. 세그폴트가 나면 핸들러가 플래그를 출력합니다.

## 같이 보면 좋은 페이지
- [[picoctf-2022-pwn-survey]]
- [[picoctf-2022-pwn-family-hub]]
- [[picoctf-2022-topic-map]]
