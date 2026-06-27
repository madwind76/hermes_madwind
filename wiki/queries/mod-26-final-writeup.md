---
title: Mod 26 — picoCTF 2021 crypto writeup
created: 2026-06-22
updated: 2026-06-22
type: query
tags: [ctf, picoctf, crypto, writeup]
sources: [https://github.com/vivian-dai/PicoCTF2021-Writeup/blob/main/Cryptography/Mod%2026/README.md]
confidence: medium
---

# Mod 26 — picoCTF 2021 crypto writeup

> **핵심은 ROT13**입니다. 26글자 알파벳에서 13칸 이동하면 원문이 드러나는 가장 기본적인 고전 암호 문제입니다.

## 참고 URL
- [GitHub writeup](https://github.com/vivian-dai/PicoCTF2021-Writeup/blob/main/Cryptography/Mod%2026/README.md)

## 1. 핵심 요약
- 암호문 `cvpbPGS{arkg_gvzr_V'yy_gel_2_ebhaqf_bs_ebg13_MAZyqFQj}`를 ROT13으로 풀어봅니다.
- 결과는 `picoCTF{next_time_I'll_try_2_rounds_of_rot13_ZNMldSDw}`입니다.
- 별도 트릭보다는 **알파벳 26자에 대한 회전**을 이해하면 바로 풀이됩니다.

## 2. 같이 보면 좋은 페이지
- [[picoctf-2021-crypto-survey]]
- [[picoctf-2021-crypto-family-hub]]
- [[crypto-writeup-family-hub]]
