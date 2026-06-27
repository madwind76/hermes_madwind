---
title: Weird File — picoCTF 2021 Forensics writeup
created: 2026-06-24
updated: 2026-06-24
type: query
tags: [ctf, picoctf, picoctf2021, forensics, writeup]
sources: [https://raw.githubusercontent.com/HHousen/PicoCTF-2021/master/Forensics/Weird%20File/README.md, https://raw.githubusercontent.com/vivian-dai/PicoCTF2021-Writeup/main/Forensics/Weird%20File/README.md]
confidence: medium
---

# Weird File — picoCTF 2021 Forensics writeup

## 참고 URL
- [공개 writeup / 원문](https://raw.githubusercontent.com/HHousen/PicoCTF-2021/master/Forensics/Weird%20File/README.md)
- [대체 참고 자료](https://raw.githubusercontent.com/vivian-dai/PicoCTF2021-Writeup/main/Forensics/Weird%20File/README.md)

## 핵심 요약
What could go wrong if we let Word documents run programs? (aka "in-the-clear"). Download file.

## 풀이 메모
1. Download the file and open it in Word or LibreOffice. In LibreOffice, go to Tools > Marcos > Edit Macros. Then, on the left, navigate to weird.docm > Project > Document Objects > ThisDocument. Here, you will see the Python program that prints the string cGljb0NURnttNGNyMHNfcl9kNG5nM3IwdXN9.
2. Putting the above string into CyberChef and using the magic block produces the flag.

## 같이 보면 좋은 페이지
- [[picoctf-2021-forensics-survey]]
- [[picoctf-2021-forensics-family-hub]]
- [[picoctf-2021-topic-map]]
