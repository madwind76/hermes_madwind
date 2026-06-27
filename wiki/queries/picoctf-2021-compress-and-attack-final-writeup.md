---
title: Compress and Attack — picoCTF 2021 Cryptography writeup
created: 2026-06-24
updated: 2026-06-24
type: query
tags: [ctf, picoctf, picoctf2021, crypto, writeup]
sources: [https://raw.githubusercontent.com/HHousen/PicoCTF-2021/master/Cryptography/Compress%20and%20Attack/README.md]
confidence: medium
---

# Compress and Attack — picoCTF 2021 Cryptography writeup

## 참고 URL
- [공개 writeup / 원문](https://raw.githubusercontent.com/HHousen/PicoCTF-2021/master/Cryptography/Compress%20and%20Attack/README.md)

## 핵심 요약
Your goal is to find the flag. compress_and_attack.py `nc mercury.picoctf.net 50899`

## 풀이 메모
1. Searching for the encryption used (Salsa20) suggests that there are no published attacks, so we'll need to look for a different attack vector.
2. Searching online for "compression and encryption" finds this StackOverflow question. Basically, since compression is applied before encryption and we control part of the text that is encrypted, we can strategically send payloads until the resulting cipher text length decreases. This idea is the basis for the CRIME exploit, which the StackOverflow question mentions.
3. Searching for "crime exploit python" reveals this amazing GitHub repository: EiNSTeiN-/compression-oracle. My slightly modified version of this script along with the solution to the challenge is in the solution script. The solution script needs to be run with Python 2 because EiNSTeiN-/compression-oracle is a very old repository. You can read more about the attack in the EiNSTeiN-/compression-oracle README.
4. Running the solution script produces the following output:

## 같이 보면 좋은 페이지
- [[picoctf-2021-cryptography-survey]]
- [[picoctf-2021-cryptography-family-hub]]
- [[picoctf-2021-topic-map]]
