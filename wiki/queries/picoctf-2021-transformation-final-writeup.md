---
title: Transformation — picoCTF 2021 Reverse Engineering writeup
created: 2026-06-24
updated: 2026-06-24
type: query
tags: [ctf, picoctf, picoctf2021, reverse-engineering, writeup]
sources: [https://raw.githubusercontent.com/HHousen/PicoCTF-2021/master/Reverse%20Engineering/Transformation/README.md, https://raw.githubusercontent.com/vivian-dai/PicoCTF2021-Writeup/main/Reverse%20Engineering/Transformation/README.md]
confidence: medium
---

# Transformation — picoCTF 2021 Reverse Engineering writeup

## 참고 URL
- [공개 writeup / 원문](https://raw.githubusercontent.com/HHousen/PicoCTF-2021/master/Reverse%20Engineering/Transformation/README.md)
- [대체 참고 자료](https://raw.githubusercontent.com/vivian-dai/PicoCTF2021-Writeup/main/Reverse%20Engineering/Transformation/README.md)

## 핵심 요약
I wonder what this really is... enc `''.join([chr((ord(flag[i]) << 8) + ord(flag[i + 1])) for i in range(0, len(flag), 2)])`

## 풀이 메모
1. cat enc: 灩捯䍔䙻ㄶ形楴獟楮獴㌴摟潦弸弲㘶㠴挲ぽ
2. The python code in the challenge text is the program used to encode the original flag. It is the program that we need to reverse.
3. The program shifts the bits for every other letter of the flag left by 8 bits (1 byte). Then, it adds the next latter of the flag to the shifted value. In other words, each letter is represented as a byte and they are joined together in pairs of two.
4. We can reverse this (see script.py) by looping through the encoded flag and for each loop we:

## 같이 보면 좋은 페이지
- [[picoctf-2021-reverse-engineering-survey]]
- [[picoctf-2021-reverse-engineering-family-hub]]
- [[picoctf-2021-topic-map]]
