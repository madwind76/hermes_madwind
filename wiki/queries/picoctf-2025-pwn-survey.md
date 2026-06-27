---
title: picoCTF 2025 pwn survey
created: 2026-06-23
updated: 2026-06-26
type: query
tags: [ctf, picoctf, pwn, binary-exploitation, survey]
sources: [https://github.com/asatpathy314/picoctf-2025, https://github.com/PS-003R32/picoCTF, https://github.com/Cajac/picoCTF-writeups]
confidence: high
---

# picoCTF 2025 pwn survey

> picoCTF 2025 Binary Exploitation(pwn) **7문제**의 전체 현황과 공개 writeup 출처를 정리한 조사 노트입니다.
> 연결 허브: [[picoctf-2025-pwn-family-hub]] · [[buffer-overflow-ctf-patterns]]

## 참고 URL
- [asatpathy314/picoctf-2025](https://github.com/asatpathy314/picoctf-2025)
- [PS-003R32/picoCTF](https://github.com/PS-003R32/picoCTF)
- [Cajac/picoCTF-writeups](https://github.com/Cajac/picoCTF-writeups)

## 1. 문제 목록

| # | Challenge | 난이도 | 점수 | 핵심 취약점 | Wiki |
|---|-----------|--------|-----:|-------------|:----:|
| 1 | [[pie-time-final-writeup|PIE TIME]] | Easy | 100 | PIE bypass (main→win offset 계산) | ✅ |
| 2 | [[pie-time-2-final-writeup|PIE TIME 2]] | Easy | 200 | Format string leak + PIE bypass | ✅ |
| 3 | [[echo-valley-final-writeup|Echo Valley]] | Medium | 300 | Format string (PIE+stack leak) → return address overwrite | ✅ |
| 4 | [[handoff-final-writeup|Handoff]] | Medium | 300 | Heap buffer overflow (struct entry + feedback overflow) | ✅ |
| 5 | [[hash-only-1-final-writeup|hash-only-1]] | Easy | 100 | PATH manipulation / alias md5sum → cat | ✅ |
| 6 | [[hash-only-2-final-writeup|hash-only-2]] | Easy | 100 | Symbolic link + PATH export hijack | ✅ |
| 7 | [[pachinko-revisited-final-writeup|Pachinko Revisited]] | Medium | 300 | Pwn/Rev 경계 — Pachinko 후속, game state 변조 | ✅ |

## 2. 카테고리 내 분류

### Memory Corruption (Classic pwn)
| 문제 | 유형 |
|------|------|
| [[pie-time-final-writeup|PIE TIME]] | Address leak → win() jump (PIE 기본) |
| [[pie-time-2-final-writeup|PIE TIME 2]] | Format string leak → win() jump (PIE 고급) |
| [[echo-valley-final-writeup|Echo Valley]] | Format string (PIE + stack leak) → return address overwrite |
| [[handoff-final-writeup|Handoff]] | Stack/heap buffer overflow (entry struct + feedback) |
| [[pachinko-revisited-final-writeup|Pachinko Revisited]] | Pachinko 후속 — 게임 상태 변조로 win 도달 (pwn/rev 경계) |

### Environment Manipulation (Unix pwn)
| 문제 | 유형 |
|------|------|
| [[hash-only-1-final-writeup|hash-only-1]] | alias hijack, PATH 내 명령어 치환 |
| [[hash-only-2-final-writeup|hash-only-2]] | symlink + PATH export hijack |

## 3. 반복되는 풀이 패턴

1. **PIE 우회는 offset 계산이 기본**
   - main과 win 사이의 고정 offset = `objdump -d` 또는 `gdb`로 계산
   - PIE TIME: 바로 jump address 입력
   - PIE TIME 2: format string으로 main 주소 leak 후 offset 적용

2. **Format string은 leak + overwrite 두 가지 용도**
   - echo-valley: `%p`로 PIE 주소 + stack 주소 leak
   - 이후 return address를 `print_flag()`로 overwrite

3. **Unix 권한/환경 조작은 pwn의 특수 분류**
   - hash-only-1/2: 메모리 취약점이 아니라 실행 환경 조작
   - `alias`, `ln -s`, `PATH` 조작으로 flaghasher가 실행하는 md5sum을 cat으로 치환

## 4. 연결 개념
- [[pie-aslr-function-offset-ctf-patterns]]
- [[format-string-ctf-patterns]]
- [[saved-return-address-control-ctf-patterns]]
- [[path-hijacking-system-abuse-ctf-patterns]]
- [[buffer-overflow-ctf-patterns]]

## 5. 관련 페이지
- [[picoctf-2025-topic-map]]
- [[picoctf-2025-pwn-family-hub]]
- [[buffer-overflow-ctf-patterns]]
- [[picoctf-2023-pwn-survey]]
- [[picoctf-2022-pwn-survey]]