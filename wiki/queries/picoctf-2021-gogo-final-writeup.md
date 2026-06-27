---
title: gogo — picoCTF 2021 Reverse Engineering writeup
created: 2026-06-24
updated: 2026-06-24
type: query
tags: [ctf, picoctf, picoctf2021, reverse-engineering, writeup]
sources: [https://raw.githubusercontent.com/HHousen/PicoCTF-2021/master/Reverse%20Engineering/gogo/README.md]
confidence: medium
---

# gogo — picoCTF 2021 Reverse Engineering writeup

## 참고 URL
- [공개 writeup / 원문](https://raw.githubusercontent.com/HHousen/PicoCTF-2021/master/Reverse%20Engineering/gogo/README.md)

## 핵심 요약
Hmmm this is a weird file... enter_password. There is a instance of the service running at `mercury.picoctf.net:48728`.

## 풀이 메모
1. We can decompile the program using Ghidra and check out the main functions. There is a checkPassword function, which is shown below:
2. The checkPassword function runs a loop that XORs two characters and compares the result to another variable. The loop in assembly is shown below:
3. We can use GDB and set a breakpoint at 0x080d4b28 so we have access to the values that our input is XORed with and the values that the result of the XOR operation is compared with.
4. We launch the program in gdb with gdb ./enter_password and create the breakpoint with b* 0x080d4b28. We run the program with r and enter 32 as since the decompiled code shows that the loop runs 0x20 times. You can generate a string of 32 as for copy-pasting by running python -c "print('a'*32)". According to the disassembly, our input should be at $ecx. If we run x /32 $ecx, sure enough we see our input:

## 같이 보면 좋은 페이지
- [[picoctf-2021-reverse-engineering-survey]]
- [[picoctf-2021-reverse-engineering-family-hub]]
- [[picoctf-2021-topic-map]]
