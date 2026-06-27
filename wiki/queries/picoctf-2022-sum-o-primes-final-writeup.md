---
title: Sum-O-Primes — picoCTF 2022 crypto writeup
created: 2026-06-24
updated: 2026-06-24
type: query
tags: [ctf, picoctf, picoctf2022, crypto, rsa]
sources: [https://picoctf2022.haydenhousen.com/cryptography/sum-o-primes.md, https://doi.org/10.1515/jmc-2016-0046]
confidence: medium
---

# Sum-O-Primes — picoCTF 2022 crypto writeup

## 참고 URL
- [HaydenHousen markdown](https://picoctf2022.haydenhousen.com/cryptography/sum-o-primes.md)
- [논문 DOI](https://doi.org/10.1515/jmc-2016-0046)

## 핵심 요약
RSA에서 보통 숨기는 `p+q`까지 함께 제공하는 문제입니다.
그 합과 공개된 곱 `n`을 이용하면 이차방정식으로 두 소수를 복원할 수 있고, 큰 정수 계산은 `gmpy2`의 높은 precision으로 처리합니다.

## 풀이 메모
1. `p+q`와 `pq=n`을 이용해 판별식 `x^2-4n`을 계산합니다.
2. `p=(x+sqrt(x^2-4n))/2` 형태로 소수를 복원합니다.
3. 복원한 소수로 RSA 비밀지수를 구해 평문을 복호화합니다.

## 같이 보면 좋은 페이지
- [[picoctf-2022-crypto-survey]]
- [[picoctf-2022-crypto-family-hub]]
- [[picoctf-2022-topic-map]]
