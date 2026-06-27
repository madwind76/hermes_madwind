---
title: picoCTF 2025 pwn family hub
created: 2026-06-23
updated: 2026-06-23
type: concept
tags: [ctf, picoctf, pwn, binary-exploitation, writeup]
sources: [https://github.com/asatpathy314/picoctf-2025, https://github.com/PS-003R32/picoCTF]
confidence: medium
---

# picoCTF 2025 pwn family hub

## 참고 URL
- [asatpathy314/picoctf-2025](https://github.com/asatpathy314/picoctf-2025)
- [PS-003R32/picoCTF](https://github.com/PS-003R32/picoCTF)

## 1. 목적
이 허브는 **picoCTF 2025 Binary Exploitation 섹션 6문제**를 문제별로 쪼개서 연결하는 상위 진입점입니다.
survey는 전체 목록과 공개 writeup 수집을 담당하고, 아래의 개별 query 페이지는 문제별 메모를 담습니다.

## 2. 문제 목록

| 문제 | 난이도 | 핵심 패턴 | 개별 페이지 |
|------|--------|-----------|:----------:|
| PIE TIME | Easy | PIE bypass (main→win offset) | [[pie-time-final-writeup]] |
| PIE TIME 2 | Easy | Format string leak + PIE bypass | [[pie-time-2-final-writeup]] |
| echo-valley | Medium | Format string → return address overwrite | [[echo-valley-final-writeup]] |
| handoff | Medium | Stack/heap buffer overflow | [[handoff-final-writeup]] |
| hash-only-1 | Easy | PATH / alias hijacking | [[hash-only-1-final-writeup]] |
| hash-only-2 | Easy | Symlink + PATH export hijacking | [[hash-only-2-final-writeup]] |

## 3. 전체 흐름
1. `picoctf-2025-pwn-survey`에서 6문제 전체를 먼저 확인합니다.
2. 세부 leaf는 개별 writeup 페이지로 들어갑니다.
3. 공통 패턴은 [[buffer-overflow-ctf-patterns]], [[format-string-ctf-patterns]], [[pie-aslr-function-offset-ctf-patterns]], [[path-hijacking-system-abuse-ctf-patterns]]로 다시 묶습니다.

## 4. 관련 페이지
- [[picoctf-2025-topic-map]]
- [[picoctf-2025-pwn-survey]]
- [[buffer-overflow-ctf-patterns]]
- [[format-string-ctf-patterns]]
- [[pie-aslr-function-offset-ctf-patterns]]
- [[path-hijacking-system-abuse-ctf-patterns]]
- [[picoctf-2023-pwn-survey]]
- [[picoctf-2022-pwn-survey]]