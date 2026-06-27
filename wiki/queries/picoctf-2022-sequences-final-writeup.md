---
title: Sequences — picoCTF 2022 crypto writeup
created: 2026-06-24
updated: 2026-06-24
type: query
tags: [ctf, picoctf, picoctf2022, crypto]
sources: [https://picoctf2022.haydenhousen.com/cryptography/sequences.md, https://www.wolframalpha.com/input?i=a%280%29%3D1%2Ca%281%29%3D2%2Ca%282%29%3D3%2Ca%283%29%3D4%2Ca_n%3D55692a_%7Bn-4%7D+-+9549a_%7Bn-3%7D+%2B+301a_%7Bn-2%7D+%2B+21a_%7Bn-1%7D]
confidence: medium
---

# Sequences — picoCTF 2022 crypto writeup

## 참고 URL
- [HaydenHousen markdown](https://picoctf2022.haydenhousen.com/cryptography/sequences.md)
- [WolframAlpha 식](https://www.wolframalpha.com/input?i=a%280%29%3D1%2Ca%281%29%3D2%2Ca%282%29%3D3%2Ca%283%29%3D4%2Ca_n%3D55692a_%7Bn-4%7D+-+9549a_%7Bn-3%7D+%2B+301a_%7Bn-2%7D+%2B+21a_%7Bn-1%7D)

## 핵심 요약
선형 점화식의 일반항을 구해 큰 n에 대해 빠르게 계산하는 문제입니다.
핵심은 점화식을 닫힌 형태로 바꾸고, `a(2*10^7)`의 결과를 모듈러 연산으로 처리한 뒤 복호화 단계로 이어 가는 것입니다.

## 풀이 메모
1. 점화식을 일반항으로 바꾸거나 빠른 계산식을 도출합니다.
2. `a(2*10^7) mod 10^10000` 형태로 결과를 구합니다.
3. 계산된 수를 이용해 `decrypt_flag` 과정을 완료합니다.

## 같이 보면 좋은 페이지
- [[picoctf-2022-crypto-survey]]
- [[picoctf-2022-crypto-family-hub]]
- [[picoctf-2022-topic-map]]
