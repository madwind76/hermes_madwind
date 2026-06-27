---
title: Pixelated — picoCTF 2021 visual cryptography concept
created: 2026-06-22
updated: 2026-06-22
type: concept
tags: [ctf, picoctf, crypto, survey, writeup]
sources: [https://github.com/vivian-dai/PicoCTF2021-Writeup/blob/main/Cryptography/Pixelated/README.md]
confidence: medium
---

# Pixelated — picoCTF 2021 visual cryptography concept

## 참고 URL
- [GitHub writeup](https://github.com/vivian-dai/PicoCTF2021-Writeup/blob/main/Cryptography/Pixelated/README.md)

## 1. 핵심
`Pixelated`는 **이미지를 겹쳐서 메시지를 복원**하는 visual cryptography 문제입니다.

## 2. 풀이 포인트
- 텍스트가 아니라 **픽셀 배열**을 봐야 합니다.
- 두 이미지를 합쳤을 때 드러나는 패턴이 핵심입니다.
- `It is my Birthday 2`와 함께 보면 출력 형식/형상 기반 문제로 묶을 수 있습니다.

## 3. 같이 보면 좋은 페이지
- [[picoctf-2021-crypto-survey]]
- [[picoctf-2021-crypto-visual-collision-bundle]]
- [[pixelated-final-writeup]]
