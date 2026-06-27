---
title: Integer overflow / logic bug — CTF patterns
created: 2026-06-15
updated: 2026-06-21
type: concept
sources: [queries/two-sum-final-writeup.md]
confidence: medium
tags: [ctf, pwn, integer-overflow, logic-bug]
---

# Integer overflow / logic bug — CTF patterns

> 산술 결과가 오버플로우되어 조건문이 잘못 평가되는 패턴입니다.

## 참고 URL
- [Reference](queries/two-sum-final-writeup.md)

## 핵심 아이디어
- 계산은 맞지만, 타입 범위를 넘으면 결과가 깨집니다.
- 그 결과 검증 조건이 의도와 다르게 참/거짓으로 바뀔 수 있습니다.

## 자주 보이는 형태
- 두 수의 합 비교
- 곱셈 결과로 길이/점수 산출
- 음수와 양수를 섞는 부호 혼동
- 32-bit vs 64-bit 차이 이용

## picoCTF 예시
- [[two-sum-final-writeup]]

## 방어
- signed/unsigned를 혼용하지 않습니다.
- 계산 전에 범위 검사를 수행합니다.
- 검증 로직을 자료형 변환보다 먼저 수행합니다.
