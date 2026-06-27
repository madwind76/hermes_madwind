---
title: It's Not My Fault 1 — picoCTF 2021 Cryptography writeup
created: 2026-06-24
updated: 2026-06-24
type: query
tags: [ctf, picoctf, picoctf2021, crypto, writeup]
sources: [https://raw.githubusercontent.com/HHousen/PicoCTF-2021/master/Cryptography/It%27s%20Not%20My%20Fault%201/README.md]
confidence: medium
---

# It's Not My Fault 1 — picoCTF 2021 Cryptography writeup

## 참고 URL
- [공개 writeup / 원문](https://raw.githubusercontent.com/HHousen/PicoCTF-2021/master/Cryptography/It%27s%20Not%20My%20Fault%201/README.md)

## 핵심 요약
What do you mean RSA with CRT has an attack that's not a fault attack? Connect with nc mercury.picoctf.net 26695. not_my_fault.py

## 풀이 메모
1. The first step of this problem is to get past the MD5 proof-of-work. We need to find a string that starts with a random 5 character long string and creates an MD5 hash that ends with a string of 6 random hex characters. This can be bruteforced with a simple script.
2. After we complete the md5 proof-of-work section, we are shown the public modulus and a clue, which is the public exponent. There is a function called get_flag that is called and will print the flag if we pass in p+q in less than 15 minutes. The public exponent, e, was generated using the two Chinese Remainder Theorem (CRT) exponents, d_p and d_q. d_p is at most 20 bits (a number between 1 and 1048576).
3. We can try to bruteforce d_p and thus find p and q using the approach discussed at Attacking RSA for fun and CTF points – part 4, which I found by searching "rsa crt small dp bruteforce". However, searching for "rsa crt attack -fault" finds this answer on MathOverflow, which discusses a much more complicated bruteforce that will execute much faster. This method is described on page 506 of Galbraith's book "Mathematics of Public Key Cryptography", where it is attributed to Pinch.
4. Since the math behind Pinch method is complicated, I'm going to be implementing the basic brute force approach from here. You can learn more about the bruteforce on that page, but the important part is this code:

## 같이 보면 좋은 페이지
- [[picoctf-2021-cryptography-survey]]
- [[picoctf-2021-cryptography-family-hub]]
- [[picoctf-2021-topic-map]]
