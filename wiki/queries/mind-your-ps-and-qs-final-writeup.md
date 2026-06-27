---
title: Mind your Ps and Qs — picoCTF 2021 crypto writeup
created: 2026-06-22
updated: 2026-06-22
type: query
tags: [ctf, picoctf, crypto, writeup]
sources: [https://github.com/vivian-dai/PicoCTF2021-Writeup/blob/main/Cryptography/Mind%20your%20Ps%20and%20Qs/README.md]
confidence: medium
---

# Mind your Ps and Qs — picoCTF 2021 crypto writeup

> **RSA의 n을 인수분해할 수 있느냐**가 핵심입니다. 작은 비트수로 생성된 모듈러스라서 factorization 후 복호화하는 흐름입니다.

## 참고 URL
- [GitHub writeup](https://github.com/vivian-dai/PicoCTF2021-Writeup/blob/main/Cryptography/Mind%20your%20Ps%20and%20Qs/README.md)

## 1. 핵심 요약
- 암호문, n, e를 확보한 뒤 n을 factorization 합니다.
- φ(n)을 계산하고 d를 복원한 뒤 RSA 복호화를 수행합니다.
- 결과 문자열이 거꾸로 보이므로 뒤집어 플래그를 복원합니다.

## 2. 같이 보면 좋은 페이지
- [[picoctf-2021-crypto-survey]]
- [[picoctf-2021-crypto-family-hub]]
- [[crypto-writeup-family-hub]]
