---
title: interencdec — picoCTF 2024 crypto writeup
created: 2026-06-22
updated: 2026-06-22
type: query
tags: [ctf, picoctf, crypto, encoding, writeup]
sources: [https://picoctfsolutions.com/picoctf-2024-interencdec, https://github.com/noamgariani11/picoCTF-2024-Writeup/blob/main/Cryptography/interencdec.md]
confidence: medium
---

# interencdec — picoCTF 2024 crypto writeup

> `interencdec`는 **중첩 인코딩(Base64 → Base64 → ROT/Caesar)**을 거꾸로 푸는 문제입니다.
> 핵심은 “암호”보다도 **인코딩을 몇 겹 쌓았는지 식별하는 눈**입니다.

## 참고 URL
- [picoCTF Solutions](https://picoctfsolutions.com/picoctf-2024-interencdec)
- [README source](https://github.com/noamgariani11/picoCTF-2024-Writeup/blob/main/Cryptography/interencdec.md)

## 1. 핵심 요약
- 입력은 Base64 문자열처럼 보입니다.
- 한 번 디코딩하면 `b'...'` 형태의 Python byte literal이 나옵니다.
- 다시 Base64를 풀면 Caesar/ROT 계열 문자열이 등장합니다.
- 마지막으로 ROT13 또는 Caesar brute-force로 flag를 얻습니다.

## 2. 공격 흐름
1. `enc_flag`를 확인합니다.
2. Base64를 한 번 풉니다.
3. 바깥의 `b'...'` 래퍼를 제거합니다.
4. 안쪽 Base64를 다시 풉니다.
5. ROT/Caesar를 적용해 `picoCTF{...}`를 찾습니다.

## 3. 같이 보면 좋은 페이지
- [[picoctf-2024-crypto-family-hub]]
- [[picoctf-2024-crypto-survey]]
- [[base64-decoding-ctf-patterns]]
