---
title: Chronohack — picoCTF 2025 reverse engineering writeup
created: 2026-06-16
updated: 2026-06-21
type: query
tags: [ctf, reverse-engineering, prng, brute-force, timing, token-forgery, automation, picoctf]
sources: [https://raw.githubusercontent.com/snwau/picoCTF-2025-Writeup/main/Reverse%20Engineering/Chronohack/Chronohack.md, https://github.com/snwau/picoCTF-2025-Writeup]
confidence: high
---

# Chronohack — picoCTF 2025 reverse engineering writeup

> 이 문제는 시간 기반 seed로 생성되는 토큰을 맞추는 reverse engineering / brute force 문제입니다.

## 참고 URL
- [raw source](https://raw.githubusercontent.com/snwau/picoCTF-2025-Writeup/main/Reverse%20Engineering/Chronohack/Chronohack.md)
- [snwau/picoCTF-2025-Writeup](https://github.com/snwau/picoCTF-2025-Writeup)


## 1. 핵심 요약
- 서버는 현재 시각을 seed로 PRNG를 초기화합니다.
- 로컬과 원격의 시간 차이를 밀리초 단위로 보정해야 합니다.
- 50회 제한 안에서 seed window를 자동으로 훑는 스크립트가 핵심입니다.

연결 개념: [[prng-seed-bruteforce-ctf-patterns]], [[reverse-engineering-ctf-patterns]], [[picoctf-2025-rec-survey]]

## 2. 문제 구조
| 항목 | 내용 |
|---|---|
| 플랫폼 | picoCTF 2025 |
| 분류 | reverse engineering / brute force |
| 핵심 요소 | time seed, PRNG, token guessing |
| 목표 | 같은 PRNG output을 재현해 token을 맞춤 |

## 3. 공격 흐름
1. `token_generator.py`에서 seed 생성 방식을 확인합니다.
2. `time.time() * 1000`처럼 시간 기반인 부분을 찾습니다.
3. 로컬 토큰 생성기를 동일 로직으로 재구현합니다.
4. seed 오차를 조정하면서 자동 제출합니다.

## 4. 재현 절차
1. 소스코드에서 PRNG seed 계산식을 찾습니다.
2. 로컬에서 동일한 토큰 생성기를 준비합니다.
3. 초 단위가 아니라 밀리초 단위로 seed 범위를 돌립니다.

```bash
# seed 오차를 자동으로 스윕하는 스크립트를 실행합니다.
python3 brute_force_token.py

# 예상 결과: 50회 제한 안에서 올바른 token이 찾아집니다.
```

## 5. 같이 보면 좋은 페이지
- [[prng-seed-bruteforce-ctf-patterns]]
- [[reverse-engineering-ctf-patterns]]
- [[flag-hunters-final-writeup]]

## 6. 참고 소스
- [Chronohack — snwau/picoCTF-2025-Writeup](https://github.com/snwau/picoCTF-2025-Writeup/blob/main/Reverse%20Engineering/Chronohack/Chronohack.md)
