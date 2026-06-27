---
title: Play Nice — picoCTF 2021 crypto writeup
created: 2026-06-22
updated: 2026-06-22
type: query
tags: [ctf, picoctf, crypto, writeup]
sources: [https://github.com/vivian-dai/PicoCTF2021-Writeup/blob/main/Cryptography/Play%20Nice/README.md]
confidence: medium
---

# Play Nice — picoCTF 2021 crypto writeup

> **Playfair cipher**를 푸는 문제입니다. 고전적인 5x5 키드 매트릭스를 이해하면 됩니다.

## 참고 URL
- [GitHub writeup](https://github.com/vivian-dai/PicoCTF2021-Writeup/blob/main/Cryptography/Play%20Nice/README.md)

## 1. 핵심 요약
- 제공된 key와 암호문을 이용해 Playfair 암호표를 구성합니다.
- 문자 쌍 단위로 규칙을 적용해 복호화합니다.
- 결과는 표준 `picoCTF{...}` 형식이 아닐 수 있으므로, 문제 조건을 그대로 따릅니다.

## 2. 같이 보면 좋은 페이지
- [[picoctf-2021-crypto-survey]]
- [[picoctf-2021-crypto-family-hub]]
- [[crypto-writeup-family-hub]]
