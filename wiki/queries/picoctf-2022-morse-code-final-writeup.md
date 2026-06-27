---
title: morse-code — picoCTF 2022 crypto writeup
created: 2026-06-24
updated: 2026-06-24
type: query
tags: [ctf, picoctf, picoctf2022, crypto]
sources: [https://raw.githubusercontent.com/noamgariani11/picoCTF-2022-Writeup/main/Cryptography/morse-code/morse-code.md, https://github.com/noamgariani11/picoCTF-2022-Writeup/tree/main/Cryptography/morse-code/morse-code.md]
confidence: medium
---

# morse-code — picoCTF 2022 crypto writeup

## 참고 URL
- [GitHub raw writeup](https://raw.githubusercontent.com/noamgariani11/picoCTF-2022-Writeup/main/Cryptography/morse-code/morse-code.md)
- [GitHub directory](https://github.com/noamgariani11/picoCTF-2022-Writeup/tree/main/Cryptography/morse-code/morse-code.md)

## 핵심 요약
Morse code is well known. Can you decrypt this? Download the file here.

## 풀이 메모
1. I used this site to decode the morse code:
2. The first part uses tr to subsitute all spaces for underscores. Then "^" in sed dictates start of line and I added picoCTF{ with that part. Then "$" dictating the end of line with sed I added "}" to the line.
3. wget https://artifacts.picoctf.net/c/79/morse_chal.wav

## 같이 보면 좋은 페이지
- [[picoctf-2022-crypto-survey]]
- [[picoctf-2022-crypto-family-hub]]
- [[picoctf-2022-topic-map]]
