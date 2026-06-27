---
title: picoCTF 2021 crypto survey
created: 2026-06-22
updated: 2026-06-22
type: query
tags: [ctf, picoctf, crypto, survey, writeup]
sources: [https://github.com/vivian-dai/PicoCTF2021-Writeup/blob/main/README.md, https://github.com/vivian-dai/PicoCTF2021-Writeup/tree/main/Cryptography]
confidence: medium
---

# picoCTF 2021 crypto survey

> 결론부터 말씀드리면, **picoCTF 2021에는 Crypto 문제가 8개 확인됩니다.**
> 이번 재분류에서는 8문제를 **8개 challenge-level 개념 페이지**로 더 잘게 나눕니다.

## 참고 URL
- [PicoCTF2021-Writeup README](https://github.com/vivian-dai/PicoCTF2021-Writeup/blob/main/README.md)
- [PicoCTF2021-Writeup Cryptography directory](https://github.com/vivian-dai/PicoCTF2021-Writeup/tree/main/Cryptography)

## 1. 확인 결과
| Challenge | Points | 분류 | 개념 페이지 |
| --- | ---: | --- | --- |
| Mod 26 | 10 | classical substitution | [[picoctf-2021-mod-26-substitution]] |
| Mind your Ps and Qs | 20 | RSA factorization | [[picoctf-2021-mind-your-ps-and-qs-rsa-factorization]] |
| New Caesar | 60 | custom Caesar | [[picoctf-2021-new-caesar-substitution]] |
| Dachshund Attacks | 80 | low-d RSA / Wiener attack | [[picoctf-2021-dachshund-attacks-rsa-wiener]] |
| Pixelated | 200 | visual cryptography | [[picoctf-2021-pixelated-visual-crypto]] |
| Play Nice | 110 | Playfair cipher | [[picoctf-2021-play-nice-playfair]] |
| It is my Birthday 2 | 170 | SHA-1 collision | [[picoctf-2021-it-is-my-birthday-2-sha1-collision]] |
| New Vignere | 300 | Vigenere cryptanalysis | [[picoctf-2021-new-vignere-vigenere]] |

## 2. 재분류 기준
1. `Mod 26`과 `New Caesar`는 **알파벳 순환/치환** 계열입니다.
2. `Mind your Ps and Qs`와 `Dachshund Attacks`는 **RSA 파라미터 취약점** 계열입니다.
3. `Play Nice`와 `New Vignere`는 **고전 암호 + 암호 분석** 계열입니다.
4. `Pixelated`와 `It is my Birthday 2`는 **출력 형식 또는 파일 합성**을 활용합니다.

## 3. 세부 페이지
- [[picoctf-2021-crypto-family-hub]]
- [[picoctf-2021-crypto-substitution-bundle]]
- [[picoctf-2021-crypto-rsa-bundle]]
- [[picoctf-2021-crypto-classical-bundle]]
- [[picoctf-2021-crypto-visual-collision-bundle]]

## 4. 관련 페이지
- [[crypto-writeup-family-hub]]
- [[caesar-cipher-ctf-patterns]]
