---
title: FANTASY CTF — picoCTF 2025 general skills writeup
created: 2026-06-24
updated: 2026-06-24
type: query
tags: [ctf, picoctf, picoctf2025, general-skills, terminal, workflow, writeup]
sources: [https://raw.githubusercontent.com/noamgariani11/picoCTF-2025-Writeup/main/General%20Skills/FANTASY-CTF.md]
confidence: high
---

# FANTASY CTF — picoCTF 2025 general skills writeup

## 참고 URL
- [GitHub writeup](https://raw.githubusercontent.com/noamgariani11/picoCTF-2025-Writeup/main/General%20Skills/FANTASY-CTF.md)

## 핵심 요약
- 이 문제는 짧은 터미널 상호작용 게임입니다.
- 안내에 따라 Enter를 여러 번 누르고, 중간 선택지에서 `A`를 고르면 플래그가 출력됩니다.
- 일반적인 취약점 익스플로잇보다 **프롬프트 순서**를 정확히 따르는 것이 핵심입니다.

## 풀이 메모
1. Enter를 5번 누릅니다.
2. `A`를 선택합니다.
3. Enter를 6번 누릅니다.
4. 다시 `A`를 선택합니다.
5. Enter를 계속 눌러 게임을 진행합니다.
6. 마지막 플래그가 출력됩니다.

## 같이 보면 좋은 페이지
- [[picoctf-2025-general-skills-survey]]
- [[picoctf-2025-general-skills-family-hub]]
