---
title: Bitlocker-2 — picoCTF 2025 forensics writeup
created: 2026-06-22
updated: 2026-06-22
type: query
tags: [ctf, picoctf, survey, writeup]
sources: [https://github.com/noamgariani11/picoCTF-2025-Writeup/blob/main/Forensics/Bitlocker-2.md]
confidence: medium
---

# Bitlocker-2 — picoCTF 2025 forensics writeup

## 참고 URL
- [GitHub writeup](https://github.com/noamgariani11/picoCTF-2025-Writeup/blob/main/Forensics/Bitlocker-2.md)

## 1. 핵심 요약
메모리 덤프에서 문자열을 찾거나 volatility를 사용해 **BitLocker 복구 단서**를 찾는 문제입니다.

## 2. 풀이 포인트
- 먼저 `strings`로 `picoCTF` 문자열을 빠르게 찾습니다.
- 의도된 풀이로는 `volatility3`나 Autopsy의 volatility 모듈을 사용할 수 있습니다.
- 메모리에서 확인한 플래그가 디스크 복구로 이어집니다.

## 3. 같이 보면 좋은 페이지
- [[picoctf-2025-forensics-survey]]
- [[picoctf-2025-forensics-family-hub]]
- [[forensics-memory-hub]]
