---
title: Windows API instrumentation — CTF patterns
created: 2026-06-16
updated: 2026-06-21
type: concept
tags: [ctf, windows, reverse-engineering, automation, rev]
sources: [https://github.com/snwau/picoCTF-2025-Writeup, https://github.com/noamgariani11/picoCTF-2025-Writeup]
confidence: high
---

# Windows API instrumentation — CTF patterns

## 참고 URL
- [snwau/picoCTF-2025-Writeup](https://github.com/snwau/picoCTF-2025-Writeup)
- [noamgariani11/picoCTF-2025-Writeup](https://github.com/noamgariani11/picoCTF-2025-Writeup)

## 1. 정의
**Windows API instrumentation**은 Frida, debugger, hook script로 `Sleep`, `CreateFileA`, `WriteFile` 같은 Win32 API 호출을 가로채 동작을 관찰하는 CTF 패턴입니다.

## 2. 핵심 아이디어
- 바이너리 내부 로직을 한 번에 이해하기보다 API 경계에서 정보를 뽑습니다.
- `Sleep`은 지연 우회, `CreateFileA`/`WriteFile`은 파일 입출력 경로 추적에 유용합니다.
- 함수 인자와 반환값을 같이 보면 의도와 실제 동작의 차이를 빠르게 찾을 수 있습니다.

## 3. 전형적 분석 흐름
1. 문제 설명에서 Windows API 키워드를 찾습니다.
2. 호출 빈도가 높은 API를 `frida-trace`로 훅합니다.
3. 인자와 반환값을 로그로 남깁니다.
4. 조건 분기를 바꾸는 트리거를 찾아 재실행합니다.

## 4. 같이 보면 좋은 페이지
- [[reverse-engineering-ctf-patterns]]
- [[binary-instrumentation-1-final-writeup]]
- [[binary-instrumentation-2-final-writeup]]
- [[picoctf-2025-rec-survey]]

## 5. 방어 관점
- 실행 경로와 파일 경로를 API 호출만으로 노출하지 않습니다.
- 보안 검증은 GUI/클라이언트가 아니라 서버 또는 독립 검증 루틴에 둡니다.
- 디버그 친화적인 힌트와 개발 로그는 배포판에서 제거합니다.
