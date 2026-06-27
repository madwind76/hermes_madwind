---
title: What's your input? — picoCTF 2021 Binary Exploitation writeup
created: 2026-06-24
updated: 2026-06-24
type: query
tags: [ctf, picoctf, picoctf2021, binary-exploitation, writeup]
sources: [https://raw.githubusercontent.com/HHousen/PicoCTF-2021/master/Binary%20Exploitation/What%27s%20your%20input%3F/README.md]
confidence: medium
---

# What's your input? — picoCTF 2021 Binary Exploitation writeup

## 참고 URL
- [공개 writeup / 원문](https://raw.githubusercontent.com/HHousen/PicoCTF-2021/master/Binary%20Exploitation/What%27s%20your%20input%3F/README.md)

## 핵심 요약
We'd like to get your input on a couple things. Think you can answer my questions correctly? in.py nc mercury.picoctf.net 39137.

## 풀이 메모
1. Look at the in.py file, which is executed using Python 2.
2. The Python 2 input function is vulnerable. More info on GeesForGeeks.
3. We can enter the variable name city as the city input parameter which will essentially set res = city.

## 같이 보면 좋은 페이지
- [[picoctf-2021-binary-exploitation-survey]]
- [[picoctf-2021-binary-exploitation-family-hub]]
- [[picoctf-2021-topic-map]]
