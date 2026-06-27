---
title: transposition-trial — picoCTF 2022 crypto writeup
created: 2026-06-24
updated: 2026-06-24
type: query
tags: [ctf, picoctf, picoctf2022, crypto]
sources: [https://raw.githubusercontent.com/noamgariani11/picoCTF-2022-Writeup/main/Cryptography/transposition-trial/transposition-trial.md, https://github.com/noamgariani11/picoCTF-2022-Writeup/tree/main/Cryptography/transposition-trial/transposition-trial.md]
confidence: medium
---

# transposition-trial — picoCTF 2022 crypto writeup

## 참고 URL
- [GitHub raw writeup](https://raw.githubusercontent.com/noamgariani11/picoCTF-2022-Writeup/main/Cryptography/transposition-trial/transposition-trial.md)
- [GitHub directory](https://github.com/noamgariani11/picoCTF-2022-Writeup/tree/main/Cryptography/transposition-trial/transposition-trial.md)

## 핵심 요약
Our data got corrupted on the way here. Luckily, nothing got replaced, but every block of 3 got scrambled around! The first

## 풀이 메모
1. First it is needed to understand what is happening and how the file is encoded.
2. Based on the description it is known that there is mutliple blocks of three that are scrambled. It is also given that the first word is three letters long.
3. Explaination of python script:

## 같이 보면 좋은 페이지
- [[picoctf-2022-crypto-survey]]
- [[picoctf-2022-crypto-family-hub]]
- [[picoctf-2022-topic-map]]
