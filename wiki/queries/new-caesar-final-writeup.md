---
title: New Caesar — picoCTF 2021 crypto writeup
created: 2026-06-22
updated: 2026-06-22
type: query
tags: [ctf, picoctf, crypto, writeup]
sources: [https://github.com/vivian-dai/PicoCTF2021-Writeup/blob/main/Cryptography/New%20Caesar/README.md]
confidence: medium
---

# New Caesar — picoCTF 2021 crypto writeup

> **알파벳이 26자가 아니라 16자라는 점**이 포인트입니다. 전통적인 Caesar를 커스텀 알파벳으로 옮겨놓은 형태입니다.

## 참고 URL
- [GitHub writeup](https://github.com/vivian-dai/PicoCTF2021-Writeup/blob/main/Cryptography/New%20Caesar/README.md)

## 1. 핵심 요약
- 코드에서 알파벳이 `a`부터 `p`까지만 쓰이는 구조를 확인합니다.
- 각 문자의 이동 규칙을 16자 순환으로 해석하면 평문이 드러납니다.
- `New Vignere`로 이어지는 전처리/알파벳 구조를 이해하는 데도 도움이 됩니다.

## 2. 같이 보면 좋은 페이지
- [[picoctf-2021-crypto-survey]]
- [[picoctf-2021-crypto-family-hub]]
- [[crypto-writeup-family-hub]]
