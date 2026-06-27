---
title: picoCTF 2024 pwn family hub
created: 2026-06-24
updated: 2026-06-24
type: concept
tags: [ctf, picoctf, pwn, binary-exploitation, writeup]
sources: [https://github.com/noamgariani11/picoCTF-2024-Writeup/blob/main/README.md, https://github.com/noamgariani11/picoCTF-2024-Writeup/tree/main/Binary%20Explotation]
confidence: medium
---

# picoCTF 2024 pwn family hub

## 참고 URL
- [picoCTF 2024 README](https://github.com/noamgariani11/picoCTF-2024-Writeup/blob/main/README.md)
- [Binary Explotation directory](https://github.com/noamgariani11/picoCTF-2024-Writeup/tree/main/Binary%20Explotation)

## 한눈에 보기
이 허브는 picoCTF 2024 Binary Exploitation을 한 번 더 묶어 보는 진입점입니다.
format string, heap, PIE, 환경 조작 같은 반복 패턴을 빠르게 찾을 수 있게 정리했습니다.

## 구성
| 분류 | 페이지 | 메모 |
|---|---|---|
| 전체 목록 | [[picoctf-2024-pwn-survey]] | 10문제 전체 |
| classic pwn | [[babygame03-final-writeup]] | 게임 상태/행동 제어 |
| format string | [[format-string-0-final-writeup]] · [[format-string-1-final-writeup]] · [[format-string-2-final-writeup]] · [[format-string-3-final-writeup]] | format string |
| heap | [[heap-0-final-writeup]] · [[heap-1-final-writeup]] · [[heap-2-final-writeup]] · [[heap-3-final-writeup]] | heap |
| mixed pattern | [[high-frequency-troubles-final-writeup]] | leak + control flow |

## 관련 페이지
- [[picoctf-2024-pwn-survey]]
- [[picoctf-2024-topic-map]]
- [[buffer-overflow-ctf-patterns]]
- [[format-string-ctf-patterns]]
- [[pie-aslr-function-offset-ctf-patterns]]
- [[path-hijacking-system-abuse-ctf-patterns]]
