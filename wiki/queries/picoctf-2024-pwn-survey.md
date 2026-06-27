---
title: picoCTF 2024 pwn survey
created: 2026-06-24
updated: 2026-06-24
type: query
tags: [ctf, picoctf, pwn, binary-exploitation, survey, writeup]
sources: [https://github.com/noamgariani11/picoCTF-2024-Writeup/blob/main/README.md, https://github.com/noamgariani11/picoCTF-2024-Writeup/tree/main/Binary%20Explotation]
confidence: medium
---

# picoCTF 2024 pwn survey

## 참고 URL
- [picoCTF 2024 README](https://github.com/noamgariani11/picoCTF-2024-Writeup/blob/main/README.md)
- [Binary Explotation directory](https://github.com/noamgariani11/picoCTF-2024-Writeup/tree/main/Binary%20Explotation)

## 핵심 요약
picoCTF 2024 Binary Exploitation(pwn)은 공개 writeup 기준 10문제로 구성됩니다.
`format-string-*`, `heap-*`, `babygame03`, `high-frequency-troubles`를 묶어 보면 패턴이 잘 보입니다.

## 문제 목록
| # | Challenge | 핵심 패턴 | 페이지 |
|---|---|---|---|
| 1 | babygame03 | 게임 상태 조작 / 로그 출력 | [[babygame03-final-writeup]] |
| 2 | format-string-0 | format string | [[format-string-0-final-writeup]] |
| 3 | format-string-1 | format string | [[format-string-1-final-writeup]] |
| 4 | format-string-2 | format string | [[format-string-2-final-writeup]] |
| 5 | format-string-3 | format string | [[format-string-3-final-writeup]] |
| 6 | heap-0 | heap overflow / layout | [[heap-0-final-writeup]] |
| 7 | heap-1 | heap exploit / layout | [[heap-1-final-writeup]] |
| 8 | heap-2 | heap exploit / layout | [[heap-2-final-writeup]] |
| 9 | heap-3 | heap exploit / layout | [[heap-3-final-writeup]] |
| 10 | high-frequency-troubles | address leak + control flow | [[high-frequency-troubles-final-writeup]] |

## 같이 보면 좋은 페이지
- [[picoctf-2024-pwn-family-hub]]
- [[picoctf-2024-topic-map]]
- [[buffer-overflow-ctf-patterns]]
