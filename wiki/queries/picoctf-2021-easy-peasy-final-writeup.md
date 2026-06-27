---
title: Easy Peasy — picoCTF 2021 Cryptography writeup
created: 2026-06-24
updated: 2026-06-24
type: query
tags: [ctf, picoctf, picoctf2021, crypto, writeup]
sources: [https://raw.githubusercontent.com/HHousen/PicoCTF-2021/master/Cryptography/Easy%20Peasy/README.md]
confidence: medium
---

# Easy Peasy — picoCTF 2021 Cryptography writeup

## 참고 URL
- [공개 writeup / 원문](https://raw.githubusercontent.com/HHousen/PicoCTF-2021/master/Cryptography/Easy%20Peasy/README.md)

## 핵심 요약
A one-time pad is unbreakable, but can you manage to recover the flag? (Wrap with picoCTF{}) nc mercury.picoctf.net 20266 otp.py

## 풀이 메모
1. As stated in the description, this is a one-time pad challenge. One of the criteria of a one-time pad is that the key is never reused in part or in whole. We can modify the program so that it does not meet this requirement.
2. The significant bug in the otp.py script appears on lines 34-36:
3. Generate a pwntools template with pwn template --host mercury.picoctf.net --port 20266 otp.py.
4. The solve script is commented and explains the solution. In brief, since we know a clear text message and an encrypted message, we can find the key (as explained in this Computer Science StackExchange answer) and then decrypt the flag.

## 같이 보면 좋은 페이지
- [[picoctf-2021-cryptography-survey]]
- [[picoctf-2021-cryptography-family-hub]]
- [[picoctf-2021-topic-map]]
