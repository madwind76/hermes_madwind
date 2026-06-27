---
title: bloat.py — picoCTF 2022 reverse engineering writeup
created: 2026-06-24
updated: 2026-06-24
type: query
tags: [ctf, picoctf, picoctf2022, reverse-engineering]
sources: [https://raw.githubusercontent.com/noamgariani11/PicoCTF-2022-Writeup/main/Reverse%20Engineering/bloat.py/bloat.py.md, https://raw.githubusercontent.com/noamgariani11/PicoCTF-2022-Writeup/tree/main/Reverse%20Engineering/bloat.py]
confidence: medium
---

# bloat.py — picoCTF 2022 reverse engineering writeup

## 참고 URL
- [GitHub raw writeup](https://raw.githubusercontent.com/noamgariani11/PicoCTF-2022-Writeup/main/Reverse%20Engineering/bloat.py/bloat.py.md)
- [GitHub directory](https://raw.githubusercontent.com/noamgariani11/PicoCTF-2022-Writeup/tree/main/Reverse%20Engineering/bloat.py)

## 핵심 요약
Can you get the flag? Run this Python program in the same directory as this encrypted flag.

## 풀이 메모
1. First thing I did was
2. a = "!\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ"+ \
3. Then using sed to get the second line in output which would be just the flag.

## 같이 보면 좋은 페이지
- [[picoctf-2022-reverse-engineering-survey]]
- [[picoctf-2022-reverse-engineering-family-hub]]
- [[picoctf-2022-topic-map]]
