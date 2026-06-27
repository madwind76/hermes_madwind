---
title: Dachshund Attacks — picoCTF 2021 Cryptography writeup
created: 2026-06-24
updated: 2026-06-24
type: query
tags: [ctf, picoctf, picoctf2021, crypto, writeup]
sources: [https://raw.githubusercontent.com/HHousen/PicoCTF-2021/master/Cryptography/Dachshund%20Attacks/README.md, https://raw.githubusercontent.com/vivian-dai/PicoCTF2021-Writeup/main/Cryptography/Dachshund%20Attacks/README.md]
confidence: medium
---

# Dachshund Attacks — picoCTF 2021 Cryptography writeup

## 참고 URL
- [공개 writeup / 원문](https://raw.githubusercontent.com/HHousen/PicoCTF-2021/master/Cryptography/Dachshund%20Attacks/README.md)
- [대체 참고 자료](https://raw.githubusercontent.com/vivian-dai/PicoCTF2021-Writeup/main/Cryptography/Dachshund%20Attacks/README.md)

## 핵심 요약
What if d is too small? Connect with nc mercury.picoctf.net 31133.

## 풀이 메모
1. I tried using RsaCtfTool, but for some reason it would not solve this one even if I specified --attack wiener.
2. Instead, we can use the owiener Python package in the solution script.
3. We can then decrypt the ciphertext using an approach from RosettaCode.

## 같이 보면 좋은 페이지
- [[picoctf-2021-cryptography-survey]]
- [[picoctf-2021-cryptography-family-hub]]
- [[picoctf-2021-topic-map]]
