---
title: Binary Gauntlet 1 — picoCTF 2021 Binary Exploitation writeup
created: 2026-06-24
updated: 2026-06-24
type: query
tags: [ctf, picoctf, picoctf2021, binary-exploitation, writeup]
sources: [https://raw.githubusercontent.com/HHousen/PicoCTF-2021/master/Binary%20Exploitation/Binary%20Gauntlet%201/README.md]
confidence: medium
---

# Binary Gauntlet 1 — picoCTF 2021 Binary Exploitation writeup

## 참고 URL
- [공개 writeup / 원문](https://raw.githubusercontent.com/HHousen/PicoCTF-2021/master/Binary%20Exploitation/Binary%20Gauntlet%201/README.md)

## 핵심 요약
Okay, time for a challenge. gauntlet nc mercury.picoctf.net 32853

## 풀이 메모
1. Decompile the binary using Ghidra:
2. Alright, so same program as "Binary Gauntlet 0" except the flag is not printed on a crash and the memory address of local_78 is printed at the beginning of the program.
3. We can write some shellcode to local_78, pad out to the return address, and overwrite the return address with the address of local_78 that is printed at the beginning.
4. Run the solution script and then run cat flag.txt to get the flag.

## 같이 보면 좋은 페이지
- [[picoctf-2021-binary-exploitation-survey]]
- [[picoctf-2021-binary-exploitation-family-hub]]
- [[picoctf-2021-topic-map]]
