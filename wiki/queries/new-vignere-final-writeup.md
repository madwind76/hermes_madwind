---
title: New Vignere — picoCTF 2021 crypto writeup
created: 2026-06-22
updated: 2026-06-22
type: query
tags: [ctf, picoctf, crypto, writeup]
sources: [https://github.com/vivian-dai/PicoCTF2021-Writeup/blob/main/Cryptography/New%20Vignere/README.md]
confidence: medium
---

# New Vignere — picoCTF 2021 crypto writeup

> **New Caesar와 같은 코드 기반에 Vigenere cryptanalysis를 얹은 문제**입니다. 대문자/알파벳 제약을 읽는 것이 중요합니다.

## 참고 URL
- [GitHub writeup](https://github.com/vivian-dai/PicoCTF2021-Writeup/blob/main/Cryptography/New%20Vignere/README.md)

## 1. 핵심 요약
- New Caesar와 동일한 전처리 구조를 먼저 이해합니다.
- Vigenere cipher의 주기와 암호 분석을 적용합니다.
- 최종적으로 hex-like flag 문자열을 복원합니다.

## 2. 같이 보면 좋은 페이지
- [[picoctf-2021-crypto-survey]]
- [[picoctf-2021-crypto-family-hub]]
- [[crypto-writeup-family-hub]]
