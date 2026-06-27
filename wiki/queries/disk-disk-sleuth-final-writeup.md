---
title: Disk, disk, sleuth! — picoCTF 2021 forensics writeup
created: 2026-06-22
updated: 2026-06-22
type: query
tags: [ctf, picoctf, forensics, survey, writeup, picoctf2021]
sources: [https://raw.githubusercontent.com/Cajac/picoCTF-writeups/main/picoCTF_2021/Forensics/Disk_disk_sleuth.md]
confidence: medium
---

# Disk, disk, sleuth! — picoCTF 2021 forensics writeup

## 참고 URL
- [GitHub writeup](https://raw.githubusercontent.com/Cajac/picoCTF-writeups/main/picoCTF_2021/Forensics/Disk_disk_sleuth.md)

## 1. 핵심 요약
Use `srch_strings` from the sleuthkit and some terminal-fu to find a flag in this disk image: dds1-alpine.flag.img.gz

## 2. 풀이 포인트
- file, strings, binwalk, sleuthkit 같은 도구로 디스크 이미지나 파일 구조를 먼저 확인합니다.
- 문제 제목과 설명에서 드러나는 아티팩트 유형부터 먼저 확인한 뒤, 필요한 경우 문자열 검색과 파일 포맷 검사를 병행합니다.

## 3. 같이 보면 좋은 페이지
- [[picoctf-2021-forensics-survey]]
- [[picoctf-2021-forensics-family-hub]]
- [[forensics-writeup-family-hub]]
