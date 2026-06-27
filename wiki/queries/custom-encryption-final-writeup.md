---
title: Custom encryption — picoCTF 2024 crypto writeup
created: 2026-06-22
updated: 2026-06-22
type: query
tags: [ctf, picoctf, crypto, reverse-engineering, xor, writeup]
sources: [https://picoctfsolutions.com/picoctf-2024-custom-encryption, https://github.com/noamgariani11/picoCTF-2024-Writeup/blob/main/Cryptography/Custom-encryption.md]
confidence: medium
---

# Custom encryption — picoCTF 2024 crypto writeup

> `Custom encryption`는 **Diffie-Hellman 스타일 키 생성 + 숫자 곱셈 + dynamic XOR**가 섞인 커스텀 암호를 역으로 풀어야 하는 문제입니다.

## 참고 URL
- [picoCTF Solutions](https://picoctfsolutions.com/picoctf-2024-custom-encryption)
- [README source](https://github.com/noamgariani11/picoCTF-2024-Writeup/blob/main/Cryptography/Custom-encryption.md)

## 1. 핵심 요약
- 제공된 Python 코드에 `generator`, `encrypt`, `dynamic_xor_encrypt`가 있습니다.
- 복호화는 **역순**으로 진행합니다.
- 먼저 DH 계열 키를 구하고, 곱셈을 나눗셈으로 되돌린 뒤 XOR를 뒤집습니다.
- 결국 보안성은 “복잡해 보이는 조합”보다 **소스 코드 공개와 연산 가역성**에 의해 무너집니다.

## 2. 공격 흐름
1. `custom_encryption.py`를 읽습니다.
2. 키 생성과 상수(`311`)를 확인합니다.
3. 곱셈 단계는 정수 나눗셈으로 되돌립니다.
4. XOR를 뒤집는 함수를 작성합니다.
5. 최종 평문에서 flag를 추출합니다.

## 3. 같이 보면 좋은 페이지
- [[picoctf-2024-crypto-family-hub]]
- [[picoctf-2024-crypto-survey]]
- [[reverse-engineering-ctf-patterns]]
- [[prng-seed-bruteforce-ctf-patterns]]
