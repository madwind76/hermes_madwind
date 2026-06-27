---
title: Shop — picoCTF 2021 Reverse Engineering writeup
created: 2026-06-24
updated: 2026-06-24
type: query
tags: [ctf, picoctf, picoctf2021, reverse-engineering, writeup]
sources: [https://raw.githubusercontent.com/HHousen/PicoCTF-2021/master/Reverse%20Engineering/Shop/README.md, https://raw.githubusercontent.com/vivian-dai/PicoCTF2021-Writeup/main/Reverse%20Engineering/Shop/README.md]
confidence: medium
---

# Shop — picoCTF 2021 Reverse Engineering writeup

## 참고 URL
- [공개 writeup / 원문](https://raw.githubusercontent.com/HHousen/PicoCTF-2021/master/Reverse%20Engineering/Shop/README.md)
- [대체 참고 자료](https://raw.githubusercontent.com/vivian-dai/PicoCTF2021-Writeup/main/Reverse%20Engineering/Shop/README.md)

## 핵심 요약
Best Stuff - Cheap Stuff, Buy Buy Buy... Store Instance: source. The shop is open for business at `nc mercury.picoctf.net 42159`.

## 풀이 메모
1. Choose an option to buy, and buy a large negative amount of them so the program gives them to you instead of you paying for them.
2. Then, buy 1 fruitful flag to have the program print the flag.
3. The complete program input and output is as follows:
4. We can decode this from decimal to ascii using Python like so python -c 'print("".join([chr(x) for x in [112, 105, 99, 111, 67, 84, 70, 123, 98, 52, 100, 95, 98, 114, 111, 103, 114, 97, 109, 109, 101, 114, 95, 55, 57, 55, 98, 50, 57, 50, 99, 125]]))' to get the flag.

## 같이 보면 좋은 페이지
- [[picoctf-2021-reverse-engineering-survey]]
- [[picoctf-2021-reverse-engineering-family-hub]]
- [[picoctf-2021-topic-map]]
