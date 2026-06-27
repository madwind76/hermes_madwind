---
title: Dachshund Attacks — picoCTF 2021 RSA Wiener concept
created: 2026-06-22
updated: 2026-06-22
type: concept
tags: [ctf, picoctf, crypto, survey, writeup]
sources: [https://github.com/vivian-dai/PicoCTF2021-Writeup/blob/main/Cryptography/Dachshund%20Attacks/README.md]
confidence: medium
---

# Dachshund Attacks — picoCTF 2021 RSA Wiener concept

## 참고 URL
- [GitHub writeup](https://github.com/vivian-dai/PicoCTF2021-Writeup/blob/main/Cryptography/Dachshund%20Attacks/README.md)

## 1. 핵심
`Dachshund Attacks`는 **작은 개인지수 `d`** 를 노리는 Wiener attack 유형입니다.

## 2. 풀이 포인트
- `e`, `n`, `d` 관계를 본 뒤 연분수 기반 공격 가능성을 확인합니다.
- 인수분해가 아니라 **키 파라미터 취약성**이 핵심입니다.
- `Mind your Ps and Qs`와 함께 보면 RSA 약점의 유형 차이가 분명합니다.

## 3. 같이 보면 좋은 페이지
- [[picoctf-2021-crypto-survey]]
- [[picoctf-2021-crypto-rsa-bundle]]
- [[dachshund-attacks-final-writeup]]
