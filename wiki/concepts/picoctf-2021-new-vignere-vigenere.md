---
title: New Vignere — picoCTF 2021 Vigenere concept
created: 2026-06-22
updated: 2026-06-22
type: concept
tags: [ctf, picoctf, crypto, survey, writeup]
sources: [https://github.com/vivian-dai/PicoCTF2021-Writeup/blob/main/Cryptography/New%20Vignere/README.md]
confidence: medium
---

# New Vignere — picoCTF 2021 Vigenere concept

## 참고 URL
- [GitHub writeup](https://github.com/vivian-dai/PicoCTF2021-Writeup/blob/main/Cryptography/New%20Vignere/README.md)

## 1. 핵심
`New Vignere`는 **Vigenere cryptanalysis**를 요구하는 고전 암호 분석 문제입니다.

## 2. 풀이 포인트
- 키 길이 추정과 주기 분석이 먼저입니다.
- 단순 치환이 아니라 **반복 키 패턴**을 찾아야 합니다.
- `Play Nice`와 함께 보면 classical family 안에서도 복호화 기법이 크게 다릅니다.

## 3. 같이 보면 좋은 페이지
- [[picoctf-2021-crypto-survey]]
- [[picoctf-2021-crypto-classical-bundle]]
- [[new-vignere-final-writeup]]
