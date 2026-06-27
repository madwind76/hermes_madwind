---
title: Bitlocker-1 — picoCTF 2025 forensics writeup
created: 2026-06-22
updated: 2026-06-22
type: query
tags: [ctf, picoctf, survey, writeup]
sources: [https://github.com/noamgariani11/picoCTF-2025-Writeup/blob/main/Forensics/Bitlocker-1.md]
confidence: medium
---

# Bitlocker-1 — picoCTF 2025 forensics writeup

## 참고 URL
- [GitHub writeup](https://github.com/noamgariani11/picoCTF-2025-Writeup/blob/main/Forensics/Bitlocker-1.md)

## 1. 핵심 요약
BitLocker 디스크 이미지를 대상으로 **비밀번호 추출 → 복호화 → 마운트** 흐름을 타는 문제입니다.

## 2. 풀이 포인트
- `bitlocker2john`으로 해시를 추출합니다.
- `hashcat`으로 약한 비밀번호를 크래킹합니다.
- 마운트 시 `ntfs-3g`가 필요할 수 있습니다.

## 3. 같이 보면 좋은 페이지
- [[picoctf-2025-forensics-survey]]
- [[picoctf-2025-forensics-family-hub]]
- [[forensics-disk-hub]]
