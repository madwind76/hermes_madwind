---
title: Ph4nt0m 1ntrud3r — picoCTF 2025 forensics writeup
created: 2026-06-22
updated: 2026-06-22
type: query
tags: [ctf, picoctf, survey, writeup]
sources: [https://github.com/noamgariani11/picoCTF-2025-Writeup/blob/main/Forensics/Ph4nt0m-1ntrud3r.md]
confidence: medium
---

# Ph4nt0m 1ntrud3r — picoCTF 2025 forensics writeup

## 참고 URL
- [GitHub writeup](https://github.com/noamgariani11/picoCTF-2025-Writeup/blob/main/Forensics/Ph4nt0m-1ntrud3r.md)

## 1. 핵심 요약
PCAP 파일을 시간순으로 정렬해 **분산된 base64 세그먼트**를 재조립하는 문제입니다.

## 2. 풀이 포인트
- `strings`로 base64 형태의 조각이 존재하는지 먼저 확인합니다.
- Wireshark에서 패킷을 시간순으로 정렬하면 플래그 조각이 순서대로 보입니다.
- `TCP Out-of-Order`처럼 흐름이 깨진 패킷도 함께 확인해야 합니다.

## 3. 같이 보면 좋은 페이지
- [[picoctf-2025-forensics-survey]]
- [[picoctf-2025-forensics-family-hub]]
- [[forensics-network-hub]]
