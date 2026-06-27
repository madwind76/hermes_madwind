---
title: C3 — picoCTF 2024 crypto writeup
created: 2026-06-22
updated: 2026-06-22
type: query
tags: [ctf, picoctf, crypto, substitution, writeup]
sources: [https://picoctfsolutions.com/picoctf-2024-c3, https://github.com/noamgariani11/picoCTF-2024-Writeup/blob/main/Cryptography/C3.md]
confidence: medium
---

# C3 — picoCTF 2024 crypto writeup

> `C3`는 **lookup table 기반 cyclical cipher**를 역변환하는 문제입니다.
> 핵심은 문자 자체가 아니라 **직전 문자에 따라 누적되는 인덱스 변화**입니다.

## 참고 URL
- [picoCTF Solutions](https://picoctfsolutions.com/picoctf-2024-c3)
- [README source](https://github.com/noamgariani11/picoCTF-2024-Writeup/blob/main/Cryptography/C3.md)

## 1. 핵심 요약
- `lookup1`과 `lookup2` 두 개의 문자 테이블이 있습니다.
- 암호화는 `prev` 상태를 누적하면서 문자를 다른 테이블로 바꿉니다.
- 복호화는 테이블 역할을 뒤집고 덧셈 방향으로 되돌리면 됩니다.

## 2. 공격 흐름
1. 제공된 `convert.py`를 읽습니다.
2. `lookup1`, `lookup2`, `prev`의 관계를 확인합니다.
3. 암호화의 `(cur - prev) % 40`를 복호화에서 `(cur + prev) % 40`로 뒤집습니다.
4. 결과를 다시 원래 문자 테이블에 매핑합니다.

## 3. 같이 보면 좋은 페이지
- [[picoctf-2024-crypto-family-hub]]
- [[picoctf-2024-crypto-survey]]
- [[reverse-engineering-ctf-patterns]]
