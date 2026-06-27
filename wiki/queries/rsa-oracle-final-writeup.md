---
title: rsa_oracle — picoCTF 2024 crypto writeup
created: 2026-06-22
updated: 2026-06-22
type: query
tags: [ctf, picoctf, crypto, rsa, oracle, writeup]
sources: [https://picoctfsolutions.com/picoctf-2024-rsa_oracle, https://github.com/noamgariani11/picoCTF-2024-Writeup/blob/main/Cryptography/rsa_oracle.md]
confidence: medium
---

# rsa_oracle — picoCTF 2024 crypto writeup

> `rsa_oracle`는 **RSA의 곱셈적 성질과 oracle을 이용한 chosen-plaintext 공격**을 활용하는 문제입니다.

## 참고 URL
- [picoCTF Solutions](https://picoctfsolutions.com/picoctf-2024-rsa_oracle)
- [README source](https://github.com/noamgariani11/picoCTF-2024-Writeup/blob/main/Cryptography/rsa_oracle.md)

## 1. 핵심 요약
- 공격자는 `password.enc`와 `secret.enc`를 확보합니다.
- oracle은 `password`만 제외하고 암호문을 복호화할 수 있습니다.
- RSA의 `E(m1) * E(m2) = E(m1*m2)` 성질을 이용하면 우회가 가능합니다.

## 2. 공격 흐름
1. `password.enc`를 정수로 읽습니다.
2. oracle을 이용해 작은 값 `2`의 암호문을 얻습니다.
3. 암호문을 곱해 복호화 가능한 형태로 바꿉니다.
4. 복호화 결과에서 password를 얻고, `secret.enc`를 풉니다.

## 3. 같이 보면 좋은 페이지
- [[picoctf-2024-crypto-family-hub]]
- [[picoctf-2024-crypto-survey]]
- [[crypto-primitive-writeup-survey]]
