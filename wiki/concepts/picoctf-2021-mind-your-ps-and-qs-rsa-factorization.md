---
title: Mind your Ps and Qs — picoCTF 2021 RSA factorization concept
created: 2026-06-22
updated: 2026-06-22
type: concept
tags: [ctf, picoctf, crypto, survey, writeup]
sources: [https://github.com/vivian-dai/PicoCTF2021-Writeup/blob/main/Cryptography/Mind%20your%20Ps%20and%20Qs/README.md]
confidence: medium
---

# Mind your Ps and Qs — picoCTF 2021 RSA factorization concept

## 참고 URL
- [GitHub writeup](https://github.com/vivian-dai/PicoCTF2021-Writeup/blob/main/Cryptography/Mind%20your%20Ps%20and%20Qs/README.md)

## 1. 핵심
이 문제는 **RSA modulus의 소인수분해**가 가능하다는 점을 이용합니다.

## 2. 풀이 포인트
- 공개된 `n`이 작거나 구조가 약한지 확인합니다.
- `p`와 `q`를 복원한 뒤 개인키를 계산합니다.
- `Dachshund Attacks`와 함께 보면 RSA 약점의 서로 다른 축을 비교할 수 있습니다.

## 3. 같이 보면 좋은 페이지
- [[picoctf-2021-crypto-survey]]
- [[picoctf-2021-crypto-rsa-bundle]]
- [[mind-your-ps-and-qs-final-writeup]]
