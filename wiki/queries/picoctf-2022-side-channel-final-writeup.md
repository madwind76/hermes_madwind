---
title: SideChannel — picoCTF 2022 forensics writeup
created: 2026-06-24
updated: 2026-06-24
type: query
tags: [ctf, picoctf, picoctf2022, forensics]
sources: [https://raw.githubusercontent.com/noamgariani11/picoCTF-2022-Writeup/main/Forensics/SideChannel/SideChannel.md, https://github.com/noamgariani11/picoCTF-2022-Writeup/tree/main/Forensics/SideChannel/SideChannel.md]
confidence: medium
---

# SideChannel — picoCTF 2022 forensics writeup

## 참고 URL
- [GitHub raw writeup](https://raw.githubusercontent.com/noamgariani11/picoCTF-2022-Writeup/main/Forensics/SideChannel/SideChannel.md)
- [GitHub directory](https://github.com/noamgariani11/picoCTF-2022-Writeup/tree/main/Forensics/SideChannel/SideChannel.md)

## 핵심 요약
There's something fishy about this PIN-code checker, can you figure out the PIN and get the flag?

## 풀이 메모
1. Then
2. Changed:
3. You can see that the time changes between a valid 8 digit pin that has most digits wrong, to one with at least one digit correct. Once I had this realisation I was able to create the python script below to automate this process and find the pin.

## 같이 보면 좋은 페이지
- [[picoctf-2022-forensics-survey]]
- [[picoctf-2022-forensics-family-hub]]
- [[picoctf-2022-topic-map]]
