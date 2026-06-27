---
title: WinAntiDbg 0x100 — picoCTF 2024 reverse engineering writeup
created: 2026-06-24
updated: 2026-06-24
type: query
tags: [ctf, picoctf, picoctf2024, reverse-engineering, windows, malware]
sources: [https://github.com/noamgariani11/picoCTF-2024-Writeup/blob/main/Reverse%20Engineering/WinAntiDbg0x100.md, https://picoctfsolutions.com/picoctf-2024-winantidbg0x100]
confidence: high
---

# WinAntiDbg 0x100 — picoCTF 2024 reverse engineering writeup

## 참고 URL
- [GitHub writeup](https://github.com/noamgariani11/picoCTF-2024-Writeup/blob/main/Reverse%20Engineering/WinAntiDbg0x100.md)
- [picoCTF Solutions](https://picoctfsolutions.com/picoctf-2024-winantidbg0x100)

## 핵심 요약
This challenge will introduce you to 'Anti-Debugging.' Malware developers don't like it when you attempt to

## 풀이 메모
1. wget https://artifacts.picoctf.net/c_titan/84/WinAntiDbg0x100.zip
2. picoctf
3. 00FA1602 | 85C0                     | test eax,eax                            |
00FA1604 | 74 15                    | je winantidbg0x100.FA161B               |
00FA1606 | 68 C835FA00              | push winantidbg0x100.FA35C8             | FA35C8:L"### Oops! The debugger was detected. Try to bypass this check to get the flag!\n"

## 같이 보면 좋은 페이지
- [[picoctf-2024-reverse-engineering-survey]]
- [[picoctf-2024-reverse-engineering-family-hub]]
- [[picoctf-2024-topic-map]]
