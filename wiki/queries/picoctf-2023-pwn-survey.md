---
title: picoCTF 2023 pwn survey
created: 2026-06-24
updated: 2026-06-24
type: query
tags: [ctf, picoctf, picoctf2023, binary-exploitation, pwn, survey, writeup]
sources: [https://github.com/noamgariani11/picoCTF-2023-Writeup/blob/main/README.md, https://github.com/noamgariani11/picoCTF-2023-Writeup/tree/main/Binary%20Explotation]
confidence: medium
---

# picoCTF 2023 pwn survey

## 참고 URL
- [picoCTF 2023 README](https://github.com/noamgariani11/picoCTF-2023-Writeup/blob/main/README.md)
- [Binary Explotation directory](https://github.com/noamgariani11/picoCTF-2023-Writeup/tree/main/Binary%20Explotation)

## 핵심 요약
picoCTF 2023 Binary Exploitation(pwn)은 공개 writeup 기준 3문제로 구성됩니다.
게임 상태 변조, 모듈 하이재킹, 산술/로직 결함으로 나눠 보면 기억하기 쉽습니다.

## 문제 목록
| # | Challenge | 핵심 패턴 | 페이지 |
|---|---|---|---|
| 1 | babygame01 | game-state / out-of-bounds | [[babygame01-final-writeup]] |
| 2 | hijacking | module hijack / environment abuse | [[hijacking-final-writeup]] |
| 3 | two-sum | arithmetic / logic bug | [[two-sum-final-writeup]] |

## 같이 보면 좋은 페이지
- [[picoctf-2023-pwn-family-hub]]
- [[picoctf-2023-topic-map]]
- [[picoctf-2023-quick-summary]]
