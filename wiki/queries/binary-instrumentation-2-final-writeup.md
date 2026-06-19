---
title: Binary Instrumentation 2 — picoCTF 2025 reverse engineering writeup
created: 2026-06-16
updated: 2026-06-16
type: query
tags: [ctf, reverse-engineering, windows, automation, rev, picoctf]
sources: [https://raw.githubusercontent.com/snwau/picoCTF-2025-Writeup/main/Reverse%20Engineering/Binary%20Instrumentation%202/Binary%20Instrumentation%202.md, https://github.com/snwau/picoCTF-2025-Writeup]
confidence: high
---

# Binary Instrumentation 2 — picoCTF 2025 reverse engineering writeup

> 이 문제는 파일 생성/쓰기 API를 계측해서, 프로그램이 실제로 어떤 경로와 내용을 쓰는지 복원하는 Windows reverse engineering 문제입니다.

## 1. 핵심 요약
- 설명상으로는 파일에 flag를 직접 저장해야 하는 프로그램입니다.
- 실제로는 `CreateFileA` 같은 WinAPI 호출이 핵심 관찰 지점입니다.
- `CreateFileA`와 `WriteFile`의 인자/반환값을 보면 잘못된 파일 경로나 쓰기 내용을 잡을 수 있습니다.

연결 개념: [[windows-api-instrumentation-ctf-patterns]], [[reverse-engineering-ctf-patterns]], [[picoctf-2025-rec-survey]]

## 2. 문제 구조
| 항목 | 내용 |
|---|---|
| 플랫폼 | picoCTF 2025 |
| 분류 | reverse engineering / Windows |
| 핵심 요소 | WinAPI, file I/O, Frida |
| 목표 | 실제 파일 쓰기 경로와 내용을 복원 |

## 3. 공격 흐름
1. 파일 관련 WinAPI를 모두 추적합니다.
2. `CreateFileA()`의 파일 경로를 찍어봅니다.
3. `WriteFile()` 또는 관련 API의 버퍼를 확인합니다.
4. flag가 빠지는 지점을 찾아 결과를 복원합니다.

## 4. 재현 절차
1. `frida-trace`로 파일 API를 후킹합니다.
2. `CreateFileA`가 어떤 파일을 여는지 로그로 확인합니다.
3. `WriteFile` 쪽 인자에서 실제 출력 내용을 확인합니다.

```bash
# 파일 관련 API를 추적합니다.
frida-trace -i *File* -f bininst2.exe -X KERNEL32

# 추적 후 생성된 handler에서 lpFileName와 buffer를 확인합니다.
```

## 5. 같이 보면 좋은 페이지
- [[windows-api-instrumentation-ctf-patterns]]
- [[reverse-engineering-ctf-patterns]]
- [[binary-instrumentation-1-final-writeup]]

## 6. 참고 소스
- [Binary Instrumentation 2 — snwau/picoCTF-2025-Writeup](https://github.com/snwau/picoCTF-2025-Writeup/blob/main/Reverse%20Engineering/Binary%20Instrumentation%202/Binary%20Instrumentation%202.md)
