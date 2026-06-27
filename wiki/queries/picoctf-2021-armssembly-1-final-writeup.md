---
title: ARMssembly 1 — picoCTF 2021 Reverse Engineering writeup
created: 2026-06-24
updated: 2026-06-24
type: query
tags: [ctf, picoctf, picoctf2021, reverse-engineering, writeup]
sources: [https://raw.githubusercontent.com/tayadavison/PicoCTF_2021/main/ReverseEngineering/ReverseEngineering.md]
confidence: medium
---

# ARMssembly 1 — picoCTF 2021 Reverse Engineering writeup

## 참고 URL
- [공개 writeup / 원문](https://raw.githubusercontent.com/tayadavison/PicoCTF_2021/main/ReverseEngineering/ReverseEngineering.md)

## 핵심 요약
For what argument does this program print `win` with variables `68`, `2` and `3`? File: chall_1.S Flag format: picoCTF{XXXXXXXX} -> (hex, lowercase, no 0x, and 32 bits. ex. 5614267 would be picoCTF{0055aabb}) Hint: Shifts

## 풀이 메모
1. The assembly code give has the following important lines in the main function:
2. bl func cmp w0, 0 bne .L4 adrp x0, .LC0
3. .LC0 has the string "You win!" So we know that we want `adrp x0, .LC0` to execute. That means that we need the value returned from func in w0 needs to be 0.

## 같이 보면 좋은 페이지
- [[picoctf-2021-reverse-engineering-survey]]
- [[picoctf-2021-reverse-engineering-family-hub]]
- [[picoctf-2021-topic-map]]
