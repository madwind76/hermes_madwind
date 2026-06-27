---
title: It is my Birthday 2 — picoCTF 2021 SHA-1 collision concept
created: 2026-06-22
updated: 2026-06-22
type: concept
tags: [ctf, picoctf, crypto, survey, writeup]
sources: [https://github.com/vivian-dai/PicoCTF2021-Writeup/blob/main/Cryptography/It%20is%20my%20Birthday%202/README.md]
confidence: medium
---

# It is my Birthday 2 — picoCTF 2021 SHA-1 collision concept

## 참고 URL
- [GitHub writeup](https://github.com/vivian-dai/PicoCTF2021-Writeup/blob/main/Cryptography/It%20is%20my%20Birthday%202/README.md)

## 1. 핵심
이 문제는 **SHA-1 collision**을 이용해 서로 다른 입력이 같은 해시를 갖게 만드는 구조입니다.

## 2. 풀이 포인트
- 동일한 해시를 만드는 두 입력의 차이를 관리합니다.
- 파일 끝부분이나 검증 조건을 유지해야 합니다.
- `Pixelated`와 함께 보면 결과가 겉모습/형식에 의해 결정되는 계열로 볼 수 있습니다.

## 3. 같이 보면 좋은 페이지
- [[picoctf-2021-crypto-survey]]
- [[picoctf-2021-crypto-visual-collision-bundle]]
- [[it-is-my-birthday-2-final-writeup]]
