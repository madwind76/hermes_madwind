---
title: morse-code — picoCTF 2022 crypto writeup
created: 2026-06-22
updated: 2026-06-22
type: query
tags: [ctf, picoctf, crypto, writeup]
sources: [https://github.com/noamgariani11/PicoCTF-2022-Writeup/blob/main/Cryptography/morse-code/morse-code.md]
confidence: medium
---

# morse-code — picoCTF 2022 crypto writeup

> 오디오에 담긴 Morse 신호를 해독하는 문제입니다.

## 참고 URL
- [GitHub writeup](https://github.com/noamgariani11/PicoCTF-2022-Writeup/blob/main/Cryptography/morse-code/morse-code.md)

## 1. 핵심 요약
- 제공된 WAV 파일에서 Morse 신호를 추출합니다.
- 점과 선, 간격을 문자로 변환합니다.
- 소문자와 underscore 규칙에 맞춰 `picoCTF{...}`로 제출합니다.

## 2. 같이 보면 좋은 페이지
- [[picoctf-2022-crypto-survey]]
- [[picoctf-2022-crypto-family-hub]]
- [[crypto-writeup-family-hub]]
