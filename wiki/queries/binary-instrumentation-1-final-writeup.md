---
title: Binary Instrumentation 1 — picoCTF 2025 reverse engineering writeup
created: 2026-06-16
updated: 2026-06-16
type: query
tags: [ctf, reverse-engineering, windows, automation, rev, picoctf]
sources: [https://raw.githubusercontent.com/snwau/picoCTF-2025-Writeup/main/Reverse%20Engineering/Binary%20Instrumentation%201/Binary%20Instrumentation%201.md, https://github.com/snwau/picoCTF-2025-Writeup]
confidence: high
---

# Binary Instrumentation 1 — picoCTF 2025 reverse engineering writeup

> 이 문제는 Windows API 호출을 Frida로 가로채서 `Sleep`이 어디서 호출되는지 확인하는 reverse engineering 문제입니다.

## 1. 핵심 요약
- 바이너리는 실행 직후 긴 `Sleep`으로 사용자를 기다리게 만듭니다.
- `frida-trace`로 `Sleep`을 후킹하면 실제 분기 지점을 찾을 수 있습니다.
- 계측 후에는 지연을 우회하고 flag 출력 루틴을 따라갑니다.

연결 개념: [[windows-api-instrumentation-ctf-patterns]], [[reverse-engineering-ctf-patterns]], [[picoctf-2025-rec-survey]]

## 2. 문제 구조
| 항목 | 내용 |
|---|---|
| 플랫폼 | picoCTF 2025 |
| 분류 | reverse engineering / Windows |
| 핵심 요소 | WinAPI, Sleep, Frida |
| 목표 | 잠자고 있는 프로그램을 깨워 flag 루틴을 실행 |

## 3. 공격 흐름
1. 실행했을 때 `Sleep`만 반복되는지 확인합니다.
2. `frida-trace`로 `Sleep` API를 후킹합니다.
3. 후킹 스크립트에서 인자와 호출 위치를 살핍니다.
4. 지연 루틴을 넘긴 뒤 실제 flag 출력 분기를 찾습니다.

## 4. 재현 절차
1. Windows 환경에서 `frida-tools`를 설치합니다.
2. `bininst1.exe`를 실행해 지연 동작을 확인합니다.
3. `frida-trace`로 `Sleep` API를 계측합니다.

```bash
# Frida 도구를 설치합니다.
pip install frida-tools

# Sleep 호출을 추적합니다.
frida-trace -i Sleep -f bininst1\bininst1.exe
```

## 5. 같이 보면 좋은 페이지
- [[windows-api-instrumentation-ctf-patterns]]
- [[reverse-engineering-ctf-patterns]]
- [[binary-instrumentation-2-final-writeup]]

## 6. 참고 소스
- [Binary Instrumentation 1 — snwau/picoCTF-2025-Writeup](https://github.com/snwau/picoCTF-2025-Writeup/blob/main/Reverse%20Engineering/Binary%20Instrumentation%201/Binary%20Instrumentation%201.md)
