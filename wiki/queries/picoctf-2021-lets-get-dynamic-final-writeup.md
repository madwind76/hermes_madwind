---
title: Let's get dynamic — picoCTF 2021 Reverse Engineering writeup
created: 2026-06-24
updated: 2026-06-24
type: query
tags: [ctf, picoctf, picoctf2021, reverse-engineering, writeup]
sources: [https://raw.githubusercontent.com/HHousen/PicoCTF-2021/master/Reverse%20Engineering/Let%27s%20get%20dynamic/README.md]
confidence: medium
---

# Let's get dynamic — picoCTF 2021 Reverse Engineering writeup

## 참고 URL
- [공개 writeup / 원문](https://raw.githubusercontent.com/HHousen/PicoCTF-2021/master/Reverse%20Engineering/Let%27s%20get%20dynamic/README.md)

## 핵심 요약
Can you tell what this file is reading? chall.S

## 풀이 메모
1. First, compile the program: gcc -g chall.S -o chall. The -g flag compiles with debugging symbols.
2. If we run the program and enter some text, we get Correct! You entered the flag., which doesn't seem correct.
3. I decompiled the chall binary using Ghidra to look at a c representation. There is a memcmp instruction which looks like it compares our input to the flag.
4. We can run the binary in gdb with gdb chall to debug it. I placed a breakpoint at the memcmp statement with b memcmp and then ran the program with r. We reach the breakpoint and now we can look at the source index and destination index registers, which are rsi and rdi respectively. We can view the source index as a string like so: printf "%s\n", $rsi, which prints the flag.

## 같이 보면 좋은 페이지
- [[picoctf-2021-reverse-engineering-survey]]
- [[picoctf-2021-reverse-engineering-family-hub]]
- [[picoctf-2021-topic-map]]
