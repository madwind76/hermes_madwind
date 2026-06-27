---
title: YaraRules0x100 — picoCTF 2025 general skills writeup
created: 2026-06-24
updated: 2026-06-24
type: query
tags: [ctf, picoctf, picoctf2025, general-skills, yara, malware-analysis, reverse-engineering, writeup]
sources: [https://raw.githubusercontent.com/noamgariani11/picoCTF-2025-Writeup/main/General%20Skills/YaraRules0x100.md]
confidence: high
---

# YaraRules0x100 — picoCTF 2025 general skills writeup

## 참고 URL
- [GitHub writeup](https://raw.githubusercontent.com/noamgariani11/picoCTF-2025-Writeup/main/General%20Skills/YaraRules0x100.md)

## 핵심 요약
- 의심스러운 Windows 실행 파일을 분석하고 YARA 룰을 작성하는 문제입니다.
- UPX 패킹 여부를 확인한 뒤 압축을 풀고 문자열을 추가로 확인합니다.
- 악성코드를 식별할 고유 문자열과 파일 시그니처를 조합해 룰을 만듭니다.

## 풀이 메모
1. `strings suspicious.exe`로 초기 문자열을 확인합니다.
2. `upx -d suspicious.exe`로 패킹을 해제합니다.
3. 재차 `strings`를 실행해 특이 문자열을 찾습니다.
4. `MZ`, `YaraRules0x100`, `UPX`, `NtQuery`, `debugger process`를 이용해 YARA 룰을 작성합니다.
5. 작성한 룰을 제출해 검증받습니다.

## 같이 보면 좋은 페이지
- [[picoctf-2025-general-skills-survey]]
- [[picoctf-2025-general-skills-family-hub]]
