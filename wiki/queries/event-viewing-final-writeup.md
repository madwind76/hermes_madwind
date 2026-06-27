---
title: Event-Viewing — picoCTF 2025 forensics writeup
created: 2026-06-22
updated: 2026-06-22
type: query
tags: [ctf, picoctf, survey, writeup]
sources: [https://github.com/noamgariani11/picoCTF-2025-Writeup/blob/main/Forensics/Event-Viewing.md]
confidence: medium
---

# Event-Viewing — picoCTF 2025 forensics writeup

## 참고 URL
- [GitHub writeup](https://github.com/noamgariani11/picoCTF-2025-Writeup/blob/main/Forensics/Event-Viewing.md)

## 1. 핵심 요약
Windows EVTX 로그를 분석해 **세 개의 사건 단서와 base64 조각**을 이어 붙이는 문제입니다.

## 2. 풀이 포인트
- EVTX를 XML로 변환해 읽기 쉽게 만듭니다.
- 이벤트 ID `1033`, `4657`, `1074`를 중심으로 추적합니다.
- 각 이벤트의 설명과 데이터에 분산된 base64를 모읍니다.

## 3. 같이 보면 좋은 페이지
- [[picoctf-2025-forensics-survey]]
- [[picoctf-2025-forensics-family-hub]]
- [[forensics-windows-hub]]
