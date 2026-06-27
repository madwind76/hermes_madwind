---
title: New Caesar — picoCTF 2021 crypto substitution concept
created: 2026-06-22
updated: 2026-06-22
type: concept
tags: [ctf, picoctf, crypto, survey, writeup]
sources: [https://github.com/vivian-dai/PicoCTF2021-Writeup/blob/main/Cryptography/New%20Caesar/README.md]
confidence: medium
---

# New Caesar — picoCTF 2021 crypto substitution concept

## 참고 URL
- [GitHub writeup](https://github.com/vivian-dai/PicoCTF2021-Writeup/blob/main/Cryptography/New%20Caesar/README.md)

## 1. 핵심
`New Caesar`는 **표준 Caesar가 아니라 커스텀 알파벳 집합**을 쓰는 변형 문제입니다.

## 2. 풀이 포인트
- 먼저 사용된 문자 집합이 26자인지 확인합니다.
- 고정 시프트인지, 별도 매핑표인지 확인합니다.
- `Mod 26`과 함께 보면 단순 순환형과 커스텀형을 구분할 수 있습니다.

## 3. 같이 보면 좋은 페이지
- [[picoctf-2021-crypto-survey]]
- [[picoctf-2021-crypto-substitution-bundle]]
- [[new-caesar-final-writeup]]
- [[caesar-cipher-ctf-patterns]]
