---
title: Hurry up! Wait! — picoCTF 2021 Reverse Engineering writeup
created: 2026-06-24
updated: 2026-06-24
type: query
tags: [ctf, picoctf, picoctf2021, reverse-engineering, writeup]
sources: [https://raw.githubusercontent.com/HHousen/PicoCTF-2021/master/Reverse%20Engineering/Hurry%20up%21%20Wait%21/README.md]
confidence: medium
---

# Hurry up! Wait! — picoCTF 2021 Reverse Engineering writeup

## 참고 URL
- [공개 writeup / 원문](https://raw.githubusercontent.com/HHousen/PicoCTF-2021/master/Reverse%20Engineering/Hurry%20up%21%20Wait%21/README.md)

## 핵심 요약
svchost.exe

## 풀이 메모
1. First, I decompiled the binary using Ghidra. I then clicked though all of the functions until I came across this:
2. The first function that FUN_0010298a calls is ada__calendar__delays__delay_for, which seems to create a long delay that prevents us from being able to simply run the program. However, the next functions that are called all look basically the same:
3. Each function calls ada__text_io__put__4, but with different arguments. The first and last arguments differ each time ada__text_io__put__4 is invoked, but they are equal within each call.
4. Double click on DAT_00102cd8 in FUN_00102616 to see that it is p. The next global value, DAT_00102cd1, in FUN_001024aa is i. DAT_00102ccb (from FUN_00102372) is c and DAT_00102cd7 (from FUN_001025e2) is o. So, it seems that each function prints a character of the flag where each character is stored as a global variable.

## 같이 보면 좋은 페이지
- [[picoctf-2021-reverse-engineering-survey]]
- [[picoctf-2021-reverse-engineering-family-hub]]
- [[picoctf-2021-topic-map]]
