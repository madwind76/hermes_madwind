---
title: Wireshark doo dooo do doo... — picoCTF 2021 forensics writeup
created: 2026-06-22
updated: 2026-06-22
type: query
tags: [ctf, picoctf, forensics, survey, writeup, picoctf2021]
sources: [https://raw.githubusercontent.com/Cajac/picoCTF-writeups/main/picoCTF_2021/Forensics/Wireshark_doo_dooo_do_doo.md]
confidence: medium
---

# Wireshark doo dooo do doo... — picoCTF 2021 forensics writeup

## 참고 URL
- [GitHub writeup](https://raw.githubusercontent.com/Cajac/picoCTF-writeups/main/picoCTF_2021/Forensics/Wireshark_doo_dooo_do_doo.md)

## 1. 핵심 요약
Can you find the flag? shark1.pcapng.

## 2. 풀이 포인트
- Wireshark로 패킷 흐름을 확인하고, 필요한 경우 TCP stream이나 프로토콜 계층을 따라 숨은 데이터를 찾습니다.
- 문제 제목과 설명에서 드러나는 아티팩트 유형부터 먼저 확인한 뒤, 필요한 경우 문자열 검색과 파일 포맷 검사를 병행합니다.

## 3. 같이 보면 좋은 페이지
- [[picoctf-2021-forensics-survey]]
- [[picoctf-2021-forensics-family-hub]]
- [[forensics-writeup-family-hub]]
