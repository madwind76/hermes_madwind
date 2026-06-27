---
title: ARMssembly 3 — picoCTF 2021 Reverse Engineering writeup
created: 2026-06-24
updated: 2026-06-24
type: query
tags: [ctf, picoctf, picoctf2021, reverse-engineering, writeup]
sources: [https://raw.githubusercontent.com/HHousen/PicoCTF-2021/master/Reverse%20Engineering/ARMssembly%203/README.md]
confidence: medium
---

# ARMssembly 3 — picoCTF 2021 Reverse Engineering writeup

## 참고 URL
- [공개 writeup / 원문](https://raw.githubusercontent.com/HHousen/PicoCTF-2021/master/Reverse%20Engineering/ARMssembly%203/README.md)

## 핵심 요약
What integer does this program print with argument 2541039191? File: chall_3.S Flag format: picoCTF{XXXXXXXX} -> (hex, lowercase, no 0x, and 32 bits. ex. 5614267 would be picoCTF{0055aabb})

## 풀이 메모
1. This challenge can be solved using the exact same method as ARMssembly 0.
2. Note that the output was Result: 57. Converting this to hexadecimal produces 39. However, the instructions say that the flag is 32 bits, so we can simply pad out the hexadecimal to 00000039.

## 같이 보면 좋은 페이지
- [[picoctf-2021-reverse-engineering-survey]]
- [[picoctf-2021-reverse-engineering-family-hub]]
- [[picoctf-2021-topic-map]]
