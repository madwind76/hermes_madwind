---
title: flags are stepic — picoCTF 2025 forensics writeup
created: 2026-06-22
updated: 2026-06-22
type: query
tags: [ctf, picoctf, survey, writeup]
sources: [https://github.com/noamgariani11/picoCTF-2025-Writeup/blob/main/Forensics/flags-are-stepic.md]
confidence: medium
---

# flags are stepic — picoCTF 2025 forensics writeup

## 참고 URL
- [GitHub writeup](https://github.com/noamgariani11/picoCTF-2025-Writeup/blob/main/Forensics/flags-are-stepic.md)

## 1. 핵심 요약
이미지 안에 숨겨진 데이터를 `stepic`으로 꺼내는 **스테가노그래피** 문제입니다.

## 2. 풀이 포인트
- 웹 페이지의 이미지 목록 중 `upz.png`를 찾아 내려받습니다.
- `stepic -i upz.png -d`로 숨겨진 내용을 확인합니다.
- 결과는 base64 계열 문자열로 이어집니다.

## 3. 같이 보면 좋은 페이지
- [[picoctf-2025-forensics-survey]]
- [[picoctf-2025-forensics-family-hub]]
- [[forensics-stego-hub]]
