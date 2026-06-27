---
title: basic-mod1 — picoCTF 2022 crypto writeup
created: 2026-06-22
updated: 2026-06-22
type: query
tags: [ctf, picoctf, crypto, writeup]
sources: [https://github.com/noamgariani11/picoCTF-2022-Writeup/blob/main/Cryptography/basic-mod1/basic-mod1.md]
confidence: medium
---

# basic-mod1 — picoCTF 2022 crypto writeup

> mod 37에 따라 숫자를 매핑하는 기본 모듈러 디코딩 문제입니다.

## 참고 URL
- [GitHub writeup](https://github.com/noamgariani11/picoCTF-2022-Writeup/blob/main/Cryptography/basic-mod1/basic-mod1.md)

## 1. 핵심 요약
- 숫자를 37로 나눈 뒤 미리 정해진 문자 집합에 대응시킵니다.
- 0-25는 대문자, 26-35는 숫자, 36은 밑줄입니다.
- 복호화된 문자열을 `picoCTF{...}` 형식으로 감싸 제출합니다.

## 2. 같이 보면 좋은 페이지
- [[picoctf-2022-crypto-survey]]
- [[picoctf-2022-crypto-family-hub]]
- [[crypto-writeup-family-hub]]
