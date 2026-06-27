---
title: Mini RSA — picoCTF 2021 Cryptography writeup
created: 2026-06-24
updated: 2026-06-24
type: query
tags: [ctf, picoctf, picoctf2021, crypto, writeup]
sources: [https://raw.githubusercontent.com/HHousen/PicoCTF-2021/master/Cryptography/Mini%20RSA/README.md]
confidence: medium
---

# Mini RSA — picoCTF 2021 Cryptography writeup

## 참고 URL
- [공개 writeup / 원문](https://raw.githubusercontent.com/HHousen/PicoCTF-2021/master/Cryptography/Mini%20RSA/README.md)

## 핵심 요약
What happens if you have a small exponent? There is a twist though, we padded the plaintext so that (M ** e) is just barely larger than N. Let's decrypt this: ciphertext

## 풀이 메모
1. I spent a while (2 hours) searching for resources to solve this. However, this Cryptography StackExchange comment is where I found the solution. Other helpful resources include: RSA Padding Schemes - Wikipedia#Padding_schemes), Cryptography StackExchange 1, Cryptography StackExchange 2, and Cryptography StackExchange 3
2. Without padding, encryption of m is m^e mod n: the message m is interpreted as an integer, then raised to exponent e, and the result is reduced modulo n. If e = 3 and m is short, then m^3 could be an integer which is smaller than n, in which case the modulo operation is a no-operation. In that case, you can just compute the cube root of the value you have. However, we cannot simply compute c^(1/3) (where c is the ciphertext) because there is a slight amount of padding to the message to make m^e larger than n, which makes the modulo operation take effect.
3. With a short m slightly wider than n^(1/e), which is what we have, we are given c = m^e mod n and can find by enumeration k such that k * n + c is an eth power: then m = (k * n + c)^(1/e).
4. We can use python and write a solution script to search though thousnads of values for k until we find one that contains the start of the flag. When we find the padding amount, we can increase the precision and rerun the calculation to get the entire flag. Keeping the precision high enough just to see the beginning of the flag speeds up the enumeration of k.

## 같이 보면 좋은 페이지
- [[picoctf-2021-cryptography-survey]]
- [[picoctf-2021-cryptography-family-hub]]
- [[picoctf-2021-topic-map]]
