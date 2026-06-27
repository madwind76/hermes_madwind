---
title: Dachshund Attacks — picoCTF 2021 crypto writeup
created: 2026-06-22
updated: 2026-06-22
type: query
tags: [ctf, picoctf, crypto, writeup]
sources: [https://github.com/vivian-dai/PicoCTF2021-Writeup/blob/main/Cryptography/Dachshund%20Attacks/README.md]
confidence: medium
---

# Dachshund Attacks — picoCTF 2021 crypto writeup

> **Wiener's attack**를 적용하는 RSA 문제입니다. `d`가 너무 작은 경우를 노립니다.

## 참고 URL
- [GitHub writeup](https://github.com/vivian-dai/PicoCTF2021-Writeup/blob/main/Cryptography/Dachshund%20Attacks/README.md)

## 1. 핵심 요약
- 서비스에서 e, n, c를 수집합니다.
- `d`가 작다는 힌트를 보고 Wiener's attack을 사용합니다.
- 복호화 후 플래그를 얻습니다.

## 2. 같이 보면 좋은 페이지
- [[picoctf-2021-crypto-survey]]
- [[picoctf-2021-crypto-family-hub]]
- [[crypto-writeup-family-hub]]
