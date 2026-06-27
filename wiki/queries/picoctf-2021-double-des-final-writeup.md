---
title: Double DES — picoCTF 2021 Cryptography writeup
created: 2026-06-24
updated: 2026-06-24
type: query
tags: [ctf, picoctf, picoctf2021, crypto, writeup]
sources: [https://raw.githubusercontent.com/HHousen/PicoCTF-2021/master/Cryptography/Double%20DES/README.md]
confidence: medium
---

# Double DES — picoCTF 2021 Cryptography writeup

## 참고 URL
- [공개 writeup / 원문](https://raw.githubusercontent.com/HHousen/PicoCTF-2021/master/Cryptography/Double%20DES/README.md)

## 핵심 요약
I wanted an encryption service that's more secure than regular DES, but not as slow as 3DES... The flag is not in standard format. nc mercury.picoctf.net 1903 ddes.py

## 풀이 메모
1. Connect to get the encrypted flag: nc mercury.picoctf.net 1903 to get 6f745ccee635f76746be185541b9f9c046b8d707f93d0522e2325fb041c59ec7bbbaa818d7c51381. For this challenge we will need a set of plaintext and ciphertext strings so I encrypt 13371337 and get 8f45ca8a9264c2aa back as the encrypted data.
2. Regular DES is vulnerable to bruteforce since it only uses an 8 byte key. Triple DES is used to remedy this, but it too is now insecure. Since we are able to obtain a set of plaintext and ciphertext, we will probably be using a known plaintext attack.
3. Double DES is vulnerable to a meet-in-the-middle attack. This StackExchange answer explains the attack perfectly. Basically, you start with the plain text, and then you bruteforce every possible key, encrypt the plain text, and store the results in a dictionary. Then, you take the original encrypted data (8f45ca8a9264c2aa in this case) and bruteforce decrypt it using every possible key, storing the results as you go. Then, you find the intersection between the encrypted and decrypted values. The keys corresponding to the overlapping value are the two keys used in the Double DES algorithm.
4. This challenge makes the above attack even easier because it only uses 6 bytes (instead of the standard 8 used in DES) and simply uses padding (aka two spaces) for the last 2 bytes. The solve script bruteforces the first and second key using the aforementioned exploit. Then it finds the intersection using Python's set class. Finally, now that both keys are known, the encrypted flag is decrypted.

## 같이 보면 좋은 페이지
- [[picoctf-2021-cryptography-survey]]
- [[picoctf-2021-cryptography-family-hub]]
- [[picoctf-2021-topic-map]]
