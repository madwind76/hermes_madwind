---
title: Lookey Here — picoCTF 2022 forensics writeup
created: 2026-06-24
updated: 2026-06-24
type: query
tags: [ctf, picoctf, picoctf2022, forensics]
sources: [https://raw.githubusercontent.com/noamgariani11/picoCTF-2022-Writeup/main/Forensics/Lookey%20Here/LookeyHere.md, https://github.com/noamgariani11/picoCTF-2022-Writeup/tree/main/Forensics/Lookey%20Here/LookeyHere.md]
confidence: medium
---

# Lookey Here — picoCTF 2022 forensics writeup

## 참고 URL
- [GitHub raw writeup](https://raw.githubusercontent.com/noamgariani11/picoCTF-2022-Writeup/main/Forensics/Lookey%20Here/LookeyHere.md)
- [GitHub directory](https://github.com/noamgariani11/picoCTF-2022-Writeup/tree/main/Forensics/Lookey%20Here/LookeyHere.md)

## 핵심 요약
Attackers have hidden information in a very large mass of data in the past, maybe they are still doing it.

## 풀이 메모
1. I initially did
2. The "-e" is to dictate the script, the "s/" and "/g" is just how sed starts and end in a script. The "^" denotes the start of the line, then the " " denotes what at the start of the line, lastly the "\*" denotes all of the spaces at the start of the line. After the "*" there is a / which after you could put something to replace all the spaces at the begining with. In this case I want it to be deleted so I put nothing there. So this is basically replacing all the spaces at the beginning of the line with nothing.
3. Then I used cut with a space as the delimiter to look at the 7th field to get just the flag itself.

## 같이 보면 좋은 페이지
- [[picoctf-2022-forensics-survey]]
- [[picoctf-2022-forensics-family-hub]]
- [[picoctf-2022-topic-map]]
