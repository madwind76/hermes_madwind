---
title: picoCTF 2024 quick summary
created: 2026-06-24
updated: 2026-06-24
type: concept
tags: [ctf, picoctf, picoctf2024, survey, hub, writeup]
sources: [https://github.com/noamgariani11/picoCTF-2024-Writeup/blob/main/README.md, https://github.com/noamgariani11/picoCTF-2024-Writeup/tree/main]
confidence: medium
---

# picoCTF 2024 quick summary

## 참고 URL
- [picoCTF 2024 README](https://github.com/noamgariani11/picoCTF-2024-Writeup/blob/main/README.md)
- [picoCTF 2024 repository root](https://github.com/noamgariani11/picoCTF-2024-Writeup/tree/main)
- [[picoctf-2024-topic-map]]

## 한눈에 보기
이 페이지는 picoCTF 2024 전체 구성을 30초 안에 훑기 위한 요약판입니다.
전체 흐름은 **topic map → survey → family hub → leaf writeup** 순서로 보면 가장 빠릅니다.

## 카테고리 요약
| 분류 | 문제 수 | survey | family hub | 한 줄 메모 |
|---|---:|---|---|---|
| Cryptography | 5 | [[picoctf-2024-crypto-survey]] | [[picoctf-2024-crypto-family-hub]] | 기본 암호 프리미티브와 반복 패턴 |
| Forensics | 8 | [[picoctf-2024-forensics-survey]] | [[picoctf-2024-forensics-family-hub]] | 이미지/디스크/스테고/메모리/Windows 아티팩트 |
| Binary Exploitation / pwn | 10 | [[picoctf-2024-pwn-survey]] | [[picoctf-2024-pwn-family-hub]] | format string, heap, leak, control-flow |
| General Skills | 10 | [[picoctf-2024-general-skills-survey]] | [[picoctf-2024-general-skills-family-hub]] | git, shell, SSH, 숫자/바이트 변환 |
| Reverse Engineering | 7 | [[picoctf-2024-reverse-engineering-survey]] | [[picoctf-2024-reverse-engineering-family-hub]] | crackme, anti-debug, packing, bytecode |
| Web Exploitation | 7 | [[picoctf-2024-web-exploitation-survey]] | [[picoctf-2024-web-exploitation-family-hub]] | 브라우저, Burp, injection, client-side |

## 추천 읽는 순서
1. 먼저 [[picoctf-2024-topic-map]]에서 전체 구조를 봅니다.
2. 관심 분류의 survey를 열어 전체 문제 목록을 확인합니다.
3. family hub에서 같은 유형의 문제를 묶어 봅니다.
4. 마지막에 leaf writeup으로 내려가 세부 풀이 메모를 봅니다.

## 빠르게 찾는 기준
- **pwn**: `babygame03`, `format-string-*`, `heap-*`, `high-frequency-troubles`
- **General Skills**: `Binary-Search`, `Blame-Game`, `SansAlpha`, `Super-SSH`, `endianness`
- **Reverse Engineering**: `WinAntiDbg0x100/0x200/0x300`, `packer`, `weirdSnake`
- **Forensics**: `Dear Diary`, `endianness-v2`, `Verify`
- **Web**: `Bookmarklet`, `IntroToBurp`, `No-Sql-Injection`, `Unminify`, `WebDecode`

## 관련 페이지
- [[picoctf-2024-topic-map]]
- [[picoctf-2024-general-skills-family-hub]]
- [[picoctf-2024-pwn-family-hub]]
- [[picoctf-2024-reverse-engineering-family-hub]]
- [[picoctf-2024-forensics-family-hub]]
- [[picoctf-2024-web-exploitation-family-hub]]
