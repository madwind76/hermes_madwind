---
title: PRNG writeup survey
created: 2026-06-20
updated: 2026-06-21
type: query
tags: [ctf, crypto, prng, brute-force, timing, token-forgery, reverse-engineering, automation, survey, writeup]
sources: [https://raw.githubusercontent.com/snwau/picoCTF-2025-Writeup/main/Reverse%20Engineering/Chronohack/Chronohack.md, https://github.com/snwau/picoCTF-2025-Writeup, https://ctftime.org/writeup/33269, https://cryptocat.me/blog/ctf/2022/pico/pwn/rps/, https://hhyleung.github.io/writeups/picoctf-2022-binary/]
confidence: high
---

# PRNG writeup survey

> 목적: **예측 가능한 난수 생성기와 그 주변 로직**을 비교합니다.
> 핵심 질문: “seed, 출력 규칙, 자동화 범위를 알면 토큰이나 승리 조건을 재현할 수 있는가?”

## 참고 URL
- [raw source](https://raw.githubusercontent.com/snwau/picoCTF-2025-Writeup/main/Reverse%20Engineering/Chronohack/Chronohack.md)
- [snwau/picoCTF-2025-Writeup](https://github.com/snwau/picoCTF-2025-Writeup)
- [CTFtime writeup](https://ctftime.org/writeup/33269)
- [cryptocat.me](https://cryptocat.me/blog/ctf/2022/pico/pwn/rps/)
- [hhyleung.github.io](https://hhyleung.github.io/writeups/picoctf-2022-binary/)


## 비교 대상

| Source | Primitive | What changed | Takeaway |
| --- | --- | --- | --- |
| `Chronohack` | time-seeded PRNG token forging | millisecond-level seed window brute force | 로컬과 원격의 시간 오차를 맞추면 토큰을 재현할 수 있습니다. |
| `RPS` | rand()-driven logic bug | substring-based win condition | 난수 자체보다 **판정 로직**이 취약할 수 있습니다. |

## 공통 관찰

1. PRNG는 보안용 난수가 아니라면 출력이 예측 가능할 수 있습니다.
2. seed가 시간 기반이면 오차 범위를 좁히는 자동화가 핵심입니다.
3. 난수 출력이 들어가는 판정 로직은 문자열 비교/부분 문자열 검사 같은 **부가 로직**에서 더 쉽게 깨집니다.

## writeup별 메모

### 1) Chronohack
- 현재 시각으로 PRNG를 초기화하고, 토큰 생성 결과를 맞추는 문제입니다.
- 핵심은 `time.time() * 1000`류의 seed 오차를 빠르게 스윕하는 자동화입니다.
- 연습 포인트:
  - seed 범위를 밀리초 단위로 좁히기
  - 원격/로컬 시각 차이 보정
  - 제한 횟수 내 자동 시도

### 2) RPS
- `rand()`로 고른 수를 `strstr()` 기반 부분 문자열 검사로 판정합니다.
- 핵심은 PRNG 예측 자체보다, **승리 판정이 느슨하게 구현된 로직 버그**입니다.
- 연습 포인트:
  - `rand()`의 예측 가능성 확인
  - 입력 문자열이 여러 후보를 포함하도록 구성
  - 난수와 판정 함수의 상호작용 점검

## 관련 개념

- [[prng-seed-bruteforce-ctf-patterns]]
- [[reverse-engineering-ctf-patterns]]
- [[substring-logic-bug-ctf-patterns]]
- [[crypto-writeup-family-hub]]
- [[chronohack-final-writeup]]
- [[rps-final-writeup]]

## 다음 읽을 거리

- [[chronohack-final-writeup]]
- [[rps-final-writeup]]
