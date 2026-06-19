---
title: Time-seeded PRNG brute force — CTF patterns
created: 2026-06-16
updated: 2026-06-16
type: concept
tags: [ctf, reverse-engineering, prng, brute-force, timing, token-forgery, automation]
sources: [https://github.com/snwau/picoCTF-2025-Writeup, https://github.com/noamgariani11/picoCTF-2025-Writeup]
confidence: high
---

# Time-seeded PRNG brute force — CTF patterns

## 1. 정의
**Time-seeded PRNG brute force**는 현재 시각으로 seed를 잡는 난수 생성기를 대상으로, seed 오차를 좁혀 동일한 출력 시퀀스를 재현하는 CTF 패턴입니다.

## 2. 핵심 아이디어
- `time.time()` 또는 유사한 시간 기반 seed는 재현 가능성이 높습니다.
- 로컬과 원격의 시각 차이, 네트워크 지연을 함께 고려해야 합니다.
- 작은 허용 횟수 안에서 seed window를 자동 탐색하는 스크립트가 핵심입니다.

## 3. 전형적 분석 흐름
1. seed가 생성되는 위치를 찾습니다.
2. seed 범위를 밀리초 단위로 좁힙니다.
3. 로컬 구현을 원본 로직과 최대한 동일하게 맞춥니다.
4. 자동 제출 스크립트로 허용 횟수 내 brute force를 수행합니다.

## 4. 같이 보면 좋은 페이지
- [[reverse-engineering-ctf-patterns]]
- [[chronohack-final-writeup]]
- [[picoctf-2025-rec-survey]]

## 5. 방어 관점
- 시간 seed만으로 토큰을 만들지 않습니다.
- 예측 가능한 PRNG를 인증에 사용하지 않습니다.
- 반복 시도에 rate limit와 재생 방지 장치를 둡니다.
