---
title: picoCTF forensics writeup family hub
created: 2026-06-22
updated: 2026-06-22
type: concept
tags: [ctf, picoctf, forensics, survey, writeup]
sources: [https://github.com/Cajac/picoCTF-writeups/blob/main/picoCTF_2021/Forensics/README.md, https://github.com/Cajac/picoCTF-writeups/blob/main/picoCTF_2022/Forensics/README.md, https://github.com/Cajac/picoCTF-writeups/blob/main/picoCTF_2023/Forensics/README.md, https://github.com/Cajac/picoCTF-writeups/blob/main/picoCTF_2024/Forensics/README.md, https://github.com/Cajac/picoCTF-writeups/blob/main/picoCTF_2025/Forensics/README.md]
confidence: medium
---

# picoCTF forensics writeup family hub

## 참고 URL
- [picoCTF 2021 Forensics README](https://github.com/Cajac/picoCTF-writeups/blob/main/picoCTF_2021/Forensics/README.md)
- [picoCTF 2022 Forensics README](https://github.com/Cajac/picoCTF-writeups/blob/main/picoCTF_2022/Forensics/README.md)
- [picoCTF 2023 Forensics README](https://github.com/Cajac/picoCTF-writeups/blob/main/picoCTF_2023/Forensics/README.md)
- [picoCTF 2024 Forensics README](https://github.com/Cajac/picoCTF-writeups/blob/main/picoCTF_2024/Forensics/README.md)
- [picoCTF 2025 Forensics README](https://github.com/Cajac/picoCTF-writeups/blob/main/picoCTF_2025/Forensics/README.md)

## 1. 목적
이 허브는 picoCTF forensics writeup을 **연도별로 탐색**하고, 공통 아티팩트 유형별로 다시 비교하기 위한 상위 진입점입니다.
각 연도 허브는 필요하면 `network / stego / disk / memory / windows` 세부 허브로 내려갑니다.

## 2. 연도별 묶음
- [[picoctf-2021-forensics-family-hub]]
- [[picoctf-2022-forensics-family-hub]]
- [[picoctf-2023-forensics-family-hub]]
- [[picoctf-2024-forensics-family-hub]]
- [[picoctf-2025-forensics-family-hub]]

## 3. 공통 패턴
1. **네트워크 / PCAP**: Wireshark, stream follow, protocol hierarchy가 핵심입니다.
2. **디스크 / 파일시스템**: file, strings, sleuthkit, binwalk로 구조를 먼저 확인합니다.
3. **이미지 / 스테고**: 메타데이터, 숨은 레이어, OCR, zsteg/steghide류를 봅니다.
4. **텍스트 / 숨은 문자열**: grep, strings, 인코딩/디코딩, 대용량 문자열 검색이 유효합니다.

## 4. 관련 페이지
- [[picoctf-2021-forensics-survey]]
- [[picoctf-2022-forensics-survey]]
- [[picoctf-2023-forensics-survey]]
- [[picoctf-2024-forensics-survey]]
- [[picoctf-2025-forensics-survey]]
- [[forensics-beginner-intermediate-scenarios]]
- [[forensics-scenario-production-plan]]
- [[forensics-scenario-deployment-readme]]
