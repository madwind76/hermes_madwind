---
title: MSB — picoCTF 2023 forensics writeup
created: 2026-06-24
updated: 2026-06-24
type: query
tags: [ctf, picoctf, picoctf2023, forensics, steganography]
sources: [https://raw.githubusercontent.com/noamgariani11/picoCTF-2023-Writeup/main/Forensics/MSB/MSB.md, https://github.com/noamgariani11/picoCTF-2023-Writeup/tree/main/Forensics/MSB]
confidence: medium
---

# MSB — picoCTF 2023 forensics writeup

## 참고 URL
- [GitHub raw writeup](https://raw.githubusercontent.com/noamgariani11/picoCTF-2023-Writeup/main/Forensics/MSB/MSB.md)
- [GitHub directory](https://github.com/noamgariani11/picoCTF-2023-Writeup/tree/main/Forensics/MSB)

## 핵심 요약
This image passes LSB statistical analysis, but we can't help but think there must be something to the visual artifacts present in this image... Download the image here

## 풀이 메모
1. wget http://www.caesum.com/handbook/Stegsolve.jar -O stegsolve.jar
2. It will be a small pop-up in top left so just expand the window. Then go to file then open and then find the file "Ninja-and-Prince-Genji-Ukiyoe-Utagawa-Kunisada.flag.png" to put into stegsolve.
3. After running this command I found this:

## 같이 보면 좋은 페이지
- [[picoctf-2023-forensics-survey]]
- [[picoctf-2023-forensics-family-hub]]
- [[picoctf-2023-topic-map]]
