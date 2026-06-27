---
title: Mod 26 — picoCTF 2021 crypto substitution concept
created: 2026-06-22
updated: 2026-06-22
type: concept
tags: [ctf, picoctf, crypto, survey, writeup]
sources: [https://github.com/vivian-dai/PicoCTF2021-Writeup/blob/main/Cryptography/Mod%2026/README.md]
confidence: medium
---

# Mod 26 — picoCTF 2021 crypto substitution concept

## 참고 URL
- [GitHub writeup](https://github.com/vivian-dai/PicoCTF2021-Writeup/blob/main/Cryptography/Mod%2026/README.md)

## 1. 핵심
`Mod 26`은 **26자 알파벳 순환**을 읽으면 풀리는 가장 기본적인 치환 문제입니다.

## 2. 풀이 포인트
- ROT13처럼 문자 위치를 이동시키는 구조입니다.
- 숫자나 기호보다 **알파벳 매핑**을 먼저 봅니다.
- `New Caesar`와 함께 보면 커스텀 치환의 변형 폭을 비교하기 좋습니다.

## 3. 같이 보면 좋은 페이지
- [[picoctf-2021-crypto-survey]]
- [[picoctf-2021-crypto-substitution-bundle]]
- [[mod-26-final-writeup]]
- [[caesar-cipher-ctf-patterns]]
