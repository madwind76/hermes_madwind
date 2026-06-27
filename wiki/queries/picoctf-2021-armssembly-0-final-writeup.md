---
title: ARMssembly 0 — picoCTF 2021 Reverse Engineering writeup
created: 2026-06-24
updated: 2026-06-24
type: query
tags: [ctf, picoctf, picoctf2021, reverse-engineering, writeup]
sources: [https://raw.githubusercontent.com/HHousen/PicoCTF-2021/master/Reverse%20Engineering/ARMssembly%200/README.md]
confidence: medium
---

# ARMssembly 0 — picoCTF 2021 Reverse Engineering writeup

## 참고 URL
- [공개 writeup / 원문](https://raw.githubusercontent.com/HHousen/PicoCTF-2021/master/Reverse%20Engineering/ARMssembly%200/README.md)

## 핵심 요약
What integer does this program print with arguments 182476535 and 3742084308? File: chall.S Flag format: picoCTF{XXXXXXXX} -> (hex, lowercase, no 0x, and 32 bits. ex. 5614267 would be picoCTF{0055aabb})

## 풀이 메모
1. We could either solve this challenge by manually reading the assembly and figuring out what it does or we could compile the assembly and run it. If you understand ARM assembly, reading it is probably easier than compiling and running it, but I don't have a good understanding of assembly so I'm going to compile it.
2. The following resources are useful to learn about how ARM assembly works:
3. ARM Instruction Set Tutorial
4. Arm Architecture Reference Manual

## 같이 보면 좋은 페이지
- [[picoctf-2021-reverse-engineering-survey]]
- [[picoctf-2021-reverse-engineering-family-hub]]
- [[picoctf-2021-topic-map]]
