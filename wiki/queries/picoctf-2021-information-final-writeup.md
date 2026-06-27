---
title: Information — picoCTF 2021 Forensics writeup
created: 2026-06-24
updated: 2026-06-24
type: query
tags: [ctf, picoctf, picoctf2021, forensics, writeup]
sources: [https://raw.githubusercontent.com/HHousen/PicoCTF-2021/master/Forensics/information/README.md, https://raw.githubusercontent.com/vivian-dai/PicoCTF2021-Writeup/main/Forensics/information/README.md]
confidence: medium
---

# Information — picoCTF 2021 Forensics writeup

## 참고 URL
- [공개 writeup / 원문](https://raw.githubusercontent.com/HHousen/PicoCTF-2021/master/Forensics/information/README.md)
- [대체 참고 자료](https://raw.githubusercontent.com/vivian-dai/PicoCTF2021-Writeup/main/Forensics/information/README.md)

## 핵심 요약
Files can always be changed in a secret way. Can you find the flag? cat.jpg

## 풀이 메모
1. Download the image and use exiftool cat.jpg. The license field looks suspicious:
2. We can decode this string using CyberChef. Paste in the string and drag in the magic block into the recipe.

## 같이 보면 좋은 페이지
- [[picoctf-2021-forensics-survey]]
- [[picoctf-2021-forensics-family-hub]]
- [[picoctf-2021-topic-map]]
