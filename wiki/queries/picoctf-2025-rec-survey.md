---
title: picoCTF 2025 reverse engineering survey
created: 2026-06-16
updated: 2026-06-16
type: query
tags: [ctf, reverse-engineering, survey, picoctf, picoctf2025, windows, prng, wasm]
sources: [https://github.com/snwau/picoCTF-2025-Writeup, https://github.com/noamgariani11/picoCTF-2025-Writeup, concepts/reverse-engineering-ctf-patterns.md]
confidence: high
---

# picoCTF 2025 reverse engineering survey

> picoCTF 2025의 Reverse Engineering 문제를 한 번에 훑는 상위 허브입니다. 공개 writeup 기준으로 문제 목록, 사용한 기법, 재사용 가능한 패턴을 한 페이지에서 연결합니다.

## 1. 범위
- **포함**: picoCTF 2025 Reverse Engineering 공개 writeup
- **경계 사례**: `Pachinko Revisited`는 pwn/rev 성격이 강해서 별도 노트로 유지합니다. [[pachinko-revisited-final-writeup]]

## 2. 문제 목록
| 문제 | 점수 | 핵심 기법 | 문서 |
|---|---:|---|---|
| Flag Hunters | 75 | source-code control flow, semicolon injection | [[flag-hunters-final-writeup]] |
| Binary Instrumentation 1 | 200 | Windows API instrumentation, Frida | [[binary-instrumentation-1-final-writeup]] |
| Tap into Hash | 200 | decode, XOR, encrypted payload reconstruction | [[tap-into-hash-final-writeup]] |
| Chronohack | 200 | time-seeded PRNG, token brute force | [[chronohack-final-writeup]] |
| Quantum Scrambler | 200 | nested list scramble reversal | [[quantum-scrambler-final-writeup]] |
| Binary Instrumentation 2 | 300 | file API instrumentation, Frida | [[binary-instrumentation-2-final-writeup]] |
| perplexed | 400 | static analysis, brute force | [[perplexed-final-writeup]] |

## 3. 관찰한 패턴
- `Flag Hunters`는 **스크립트 기반 상태 머신**을 읽고 입력을 조작하는 문제입니다.
- `Binary Instrumentation 1/2`는 **Windows API 호출 계측**이 핵심입니다.
- `Chronohack`는 **시간 seed PRNG**를 밀리초 단위로 맞추는 문제가 핵심입니다.
- `Quantum Scrambler`와 `Tap into Hash`는 **변환 루틴을 역으로 적용해 평문을 복원**하는 유형입니다.
- `perplexed`는 Ghidra로 조건을 읽고 제한된 입력 공간을 brute force하는 유형입니다.

## 4. 관련 개념 허브
- [[reverse-engineering-ctf-patterns]]
- [[windows-api-instrumentation-ctf-patterns]]
- [[prng-seed-bruteforce-ctf-patterns]]
- [[wasm-reverse-engineering-ctf-patterns]]
- [[custom-cpu-reverse-engineering-ctf-patterns]]

## 5. 같이 보면 좋은 페이지
- [[picoctf-pwn-survey]] — pwn / binary exploitation과의 경계 확인
- [[picoctf-2025-web-exploitation-survey]] — `Pachinko` 계열의 Web 경계 확인
- [[picoctf-2025-rec-survey]]의 하위 개별 writeup들
