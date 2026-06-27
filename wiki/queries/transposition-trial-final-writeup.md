---
title: transposition-trial — picoCTF 2022 crypto writeup
created: 2026-06-22
updated: 2026-06-22
type: query
tags: [ctf, picoctf, crypto, writeup]
sources: [https://github.com/noamgariani11/PicoCTF-2022-Writeup/blob/main/Cryptography/transposition-trial/transposition-trial.md]
confidence: medium
---

# transposition-trial — picoCTF 2022 crypto writeup

> 3글자 단위 블록이 뒤섞인 transposition 문제입니다.

## 참고 URL
- [GitHub writeup](https://github.com/noamgariani11/PicoCTF-2022-Writeup/blob/main/Cryptography/transposition-trial/transposition-trial.md)

## 1. 핵심 요약
- 모든 블록이 3글자 단위로 재배열되었다는 점을 확인합니다.
- 첫 단어의 길이 정보를 이용해 재조합합니다.
- 원문을 복구한 뒤 플래그 형식으로 제출합니다.

## 2. 같이 보면 좋은 페이지
- [[picoctf-2022-crypto-survey]]
- [[picoctf-2022-crypto-family-hub]]
- [[crypto-writeup-family-hub]]
