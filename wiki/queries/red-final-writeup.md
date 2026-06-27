---
title: RED — picoCTF 2025 forensics writeup
created: 2026-06-22
updated: 2026-06-22
type: query
tags: [ctf, picoctf, survey, writeup]
sources: [https://github.com/noamgariani11/picoCTF-2025-Writeup/blob/main/Forensics/RED.md]
confidence: medium
---

# RED — picoCTF 2025 forensics writeup

## 참고 URL
- [GitHub writeup](https://github.com/noamgariani11/picoCTF-2025-Writeup/blob/main/Forensics/RED.md)

## 1. 핵심 요약
빨간 이미지 `red.png`에서 **stegano 데이터와 base64 문자열**을 추출하는 문제입니다.

## 2. 풀이 포인트
- `zsteg`로 PNG의 은닉 데이터를 확인합니다.
- 추출 결과에 base64가 반복되어 나타납니다.
- base64를 디코딩하면 플래그를 얻을 수 있습니다.

## 3. 같이 보면 좋은 페이지
- [[picoctf-2025-forensics-survey]]
- [[picoctf-2025-forensics-family-hub]]
- [[forensics-stego-hub]]
