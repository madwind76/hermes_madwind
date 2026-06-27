---
title: New Caesar — picoCTF 2021 Cryptography writeup
created: 2026-06-24
updated: 2026-06-24
type: query
tags: [ctf, picoctf, picoctf2021, crypto, writeup]
sources: [https://raw.githubusercontent.com/HHousen/PicoCTF-2021/master/Cryptography/New%20Caesar/README.md, https://raw.githubusercontent.com/vivian-dai/PicoCTF2021-Writeup/main/Cryptography/New%20Caesar/README.md]
confidence: medium
---

# New Caesar — picoCTF 2021 Cryptography writeup

## 참고 URL
- [공개 writeup / 원문](https://raw.githubusercontent.com/HHousen/PicoCTF-2021/master/Cryptography/New%20Caesar/README.md)
- [대체 참고 자료](https://raw.githubusercontent.com/vivian-dai/PicoCTF2021-Writeup/main/Cryptography/New%20Caesar/README.md)

## 핵심 요약
We found a brand new type of encryption, can you break the secret code? (Wrap with picoCTF{}) `kjlijdliljhdjdhfkfkhhjkkhhkihlhnhghekfhmhjhkhfhekfkkkjkghghjhlhghmhhhfkikfkfhm` new_caesar.py

## 풀이 메모
1. Let's reverse the new_caesar.py program.
2. See comments in the solution script for a detailed explanation. We reverse the encoding mechanism, then try the possible offsets, and print the possible flags.

## 같이 보면 좋은 페이지
- [[picoctf-2021-cryptography-survey]]
- [[picoctf-2021-cryptography-family-hub]]
- [[picoctf-2021-topic-map]]
