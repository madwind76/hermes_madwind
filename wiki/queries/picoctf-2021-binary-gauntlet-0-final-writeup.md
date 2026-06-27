---
title: Binary Gauntlet 0 — picoCTF 2021 Binary Exploitation writeup
created: 2026-06-24
updated: 2026-06-24
type: query
tags: [ctf, picoctf, picoctf2021, binary-exploitation, writeup]
sources: [https://raw.githubusercontent.com/HHousen/PicoCTF-2021/master/Binary%20Exploitation/Binary%20Gauntlet%200/README.md]
confidence: medium
---

# Binary Gauntlet 0 — picoCTF 2021 Binary Exploitation writeup

## 참고 URL
- [공개 writeup / 원문](https://raw.githubusercontent.com/HHousen/PicoCTF-2021/master/Binary%20Exploitation/Binary%20Gauntlet%200/README.md)

## 핵심 요약
This series of problems has to do with binary protections and how they affect exploiting a very simple program. How far can you make it in the gauntlet? gauntlet nc mercury.picoctf.net 37752

## 풀이 메모
1. Decompile the binary using Ghidra.
2. As you can see, if the program crashes the flag will be printed. We can cause a crash by overflowing the the local_88 when local_10 is copied into in the strcpy function. We control local_10
3. So send one a for the first fgets and then send more than 108 as for the second fgets so those 108+ as get copied into a variable with a size of 108 and thus overflow and cause a crash.

## 같이 보면 좋은 페이지
- [[picoctf-2021-binary-exploitation-survey]]
- [[picoctf-2021-binary-exploitation-family-hub]]
- [[picoctf-2021-topic-map]]
