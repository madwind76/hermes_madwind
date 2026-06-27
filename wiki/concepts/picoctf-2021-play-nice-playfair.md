---
title: Play Nice — picoCTF 2021 Playfair concept
created: 2026-06-22
updated: 2026-06-22
type: concept
tags: [ctf, picoctf, crypto, survey, writeup]
sources: [https://github.com/vivian-dai/PicoCTF2021-Writeup/blob/main/Cryptography/Play%20Nice/README.md]
confidence: medium
---

# Play Nice — picoCTF 2021 Playfair concept

## 참고 URL
- [GitHub writeup](https://github.com/vivian-dai/PicoCTF2021-Writeup/blob/main/Cryptography/Play%20Nice/README.md)

## 1. 핵심
`Play Nice`는 **Playfair cipher**의 전형적인 적용 문제입니다.

## 2. 풀이 포인트
- 5x5 키 مربع를 구성한 뒤 digraph 단위로 해독합니다.
- 반복 문자 처리와 filler 규칙을 먼저 확인합니다.
- `New Vignere`와 비교하면 고전 암호라도 분석 방식이 다르다는 점이 보입니다.

## 3. 같이 보면 좋은 페이지
- [[picoctf-2021-crypto-survey]]
- [[picoctf-2021-crypto-classical-bundle]]
- [[play-nice-final-writeup]]
