---
title: It is my Birthday 2 — picoCTF 2021 crypto writeup
created: 2026-06-22
updated: 2026-06-22
type: query
tags: [ctf, picoctf, crypto, writeup]
sources: [https://github.com/vivian-dai/PicoCTF2021-Writeup/blob/main/Cryptography/It%20is%20my%20Birthday%202/README.md]
confidence: medium
---

# It is my Birthday 2 — picoCTF 2021 crypto writeup

> **SHA-1 collision**을 이용하는 문제입니다. 파일 두 개가 같은 해시를 가지도록 만드는 것이 핵심입니다.

## 참고 URL
- [GitHub writeup](https://github.com/vivian-dai/PicoCTF2021-Writeup/blob/main/Cryptography/It%20is%20my%20Birthday%202/README.md)

## 1. 핵심 요약
- shattered 프로젝트의 충돌 PDF를 이용합니다.
- 서로 다른 두 PDF가 동일한 SHA-1 해시를 갖도록 만듭니다.
- 원본 초대장과 같은 마지막 1000바이트 조건을 맞춰 제출합니다.

## 2. 같이 보면 좋은 페이지
- [[picoctf-2021-crypto-survey]]
- [[picoctf-2021-crypto-family-hub]]
- [[crypto-writeup-family-hub]]
