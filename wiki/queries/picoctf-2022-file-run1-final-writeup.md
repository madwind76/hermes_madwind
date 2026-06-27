---
title: file-run1 — picoCTF 2022 reverse engineering writeup
created: 2026-06-24
updated: 2026-06-24
type: query
tags: [ctf, picoctf, picoctf2022, reverse-engineering]
sources: [https://raw.githubusercontent.com/noamgariani11/PicoCTF-2022-Writeup/main/Reverse%20Engineering/file-run1/file-run1.md, https://raw.githubusercontent.com/noamgariani11/PicoCTF-2022-Writeup/tree/main/Reverse%20Engineering/file-run1]
confidence: medium
---

# file-run1 — picoCTF 2022 reverse engineering writeup

## 참고 URL
- [GitHub raw writeup](https://raw.githubusercontent.com/noamgariani11/PicoCTF-2022-Writeup/main/Reverse%20Engineering/file-run1/file-run1.md)
- [GitHub directory](https://raw.githubusercontent.com/noamgariani11/PicoCTF-2022-Writeup/tree/main/Reverse%20Engineering/file-run1)

## 핵심 요약
A program has been provided to you, what happens if you try <br> to run it on the command line? <br>

## 풀이 메모
1. After getting the file, you can run file to see what type of file it is.
2. You'll see that it is a "ELF 64-bit LSB pie executable", so change the permissions to add the ability to execute the file.
3. The with "./" then the file name you can run the file.

## 같이 보면 좋은 페이지
- [[picoctf-2022-reverse-engineering-survey]]
- [[picoctf-2022-reverse-engineering-family-hub]]
- [[picoctf-2022-topic-map]]
