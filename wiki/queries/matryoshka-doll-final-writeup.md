---
title: Matryoshka doll — picoCTF 2021 forensics writeup
created: 2026-06-22
updated: 2026-06-22
type: query
tags: [ctf, picoctf, forensics, survey, writeup, picoctf2021]
sources: [https://raw.githubusercontent.com/Cajac/picoCTF-writeups/main/picoCTF_2021/Forensics/Matryoshka_doll.md]
confidence: medium
---

# Matryoshka doll — picoCTF 2021 forensics writeup

## 참고 URL
- [GitHub writeup](https://raw.githubusercontent.com/Cajac/picoCTF-writeups/main/picoCTF_2021/Forensics/Matryoshka_doll.md)

## 1. 핵심 요약
Matryoshka dolls are a set of wooden dolls of decreasing size placed one inside another. What's the final one?

## 2. 풀이 포인트
- strings, grep, OCR, 간단한 인코딩/디코딩으로 숨은 문자열이나 메타데이터를 추적합니다.
- 문제 제목과 설명에서 드러나는 아티팩트 유형부터 먼저 확인한 뒤, 필요한 경우 문자열 검색과 파일 포맷 검사를 병행합니다.

## 3. 같이 보면 좋은 페이지
- [[picoctf-2021-forensics-survey]]
- [[picoctf-2021-forensics-family-hub]]
- [[forensics-writeup-family-hub]]
