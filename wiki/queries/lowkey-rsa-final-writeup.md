---
title: Lowkey RSA — L3akCTF 2025 writeup
created: 2026-06-20
updated: 2026-06-21
type: query
tags: [ctf, crypto, rsa, brute-force, reverse-engineering, cia]
sources: [https://ctftime.org/writeup/40345]
confidence: medium
---

# Lowkey RSA — L3akCTF 2025 writeup

> `Lowkey RSA`는 **비정상적인 RSA 파라미터 구성과 작은 비밀값** 때문에, 평범한 RSA 복호화가 아니라 수론 기반 근사와 분수 전개를 써서 깨는 문제입니다.

## 참고 URL
- [CTFtime writeup](https://ctftime.org/writeup/40345)


## 1. 한 줄 요약
- `phi = (p**4-1)*(q**4-1)` 같은 비표준 totient가 등장합니다.
- 비밀값 `d`가 작아서 continued fraction 계열 접근이 가능합니다.
- `phi ≈ (N**2 - 1)**2` 근사를 바탕으로 `p`, `q`를 다시 복원합니다.

## 2. 문제 흐름
| 단계 | 관찰 | 의미 |
|------|------|------|
| 1 | 비표준 totient 확인 | 일반 RSA 공식이 아님 |
| 2 | `e * d ≡ -1 (mod phi)` 형태 확인 | 작은 `d`가 핵심 |
| 3 | `phi`를 `N` 기반으로 근사 | 수학적 공격 가능 |
| 4 | continued fraction으로 `(k, d)` 후보 탐색 | 작은 분수 해석 |
| 5 | `p^4`, `q^4`를 복원 | 인수분해 단계로 이어짐 |
| 6 | 표준 RSA 복호화 | flag 복원 |

## 3. 핵심 분석
이 문제는 RSA 자체보다 **파라미터 설계 실수**가 취약점입니다. 공개키 수식이 비정상적이면, 공격자는 암호문을 푸는 대신 **비밀 관계식**을 먼저 역추적해야 합니다.

### 3.1 공격 포인트
- 작은 `d`는 continued fraction 기반 복원에 취약합니다.
- `phi`를 정확히 몰라도, 근사가 충분히 좋으면 후보를 걸러낼 수 있습니다.
- 결국 목표는 `N`의 구조를 복원해 평범한 RSA로 되돌리는 것입니다.

### 3.2 실전 메모
```python
# 비표준 RSA 식이 보이면, 일반적인 d 복호화보다
# 파라미터 관계식을 먼저 정리합니다.
# 예상 결과: phi 근사와 분수 전개 후보가 나옵니다.
```

## 4. 공격자 관점
1. RSA 소스에서 `phi`와 `e` 계산식을 찾습니다.
2. 작은 비밀값 조건을 확인합니다.
3. 근사식으로 후보를 좁히고 분수 전개를 시도합니다.
4. 유효한 `(k, d)`를 찾으면 `phi_candidate`를 계산합니다.
5. 인수분해를 되살려 표준 RSA 복호화로 마무리합니다.

## 5. 방어자 관점
- RSA 파라미터는 표준 수식을 따르는 것이 안전합니다.
- 작은 비밀값을 사용하지 않습니다.
- 복호화 가능성을 낮추려면 공개 설계에 예측 가능한 관계식을 두지 않아야 합니다.

## 6. 같이 보면 좋은 페이지
- [[crypto-writeup-family-hub]]
- [[reverse-engineering-ctf-patterns]]
- [[cia]]

## 7. 참고 소스
- [CTFtime — Lowkey RSA writeup](https://ctftime.org/writeup/40345)
