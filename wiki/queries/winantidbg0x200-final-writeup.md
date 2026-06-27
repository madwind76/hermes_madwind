---
title: WinAntiDbg0x200 — picoCTF 2024 reverse engineering writeup
created: 2026-06-24
updated: 2026-06-24
type: query
tags: [ctf, picoctf, picoctf2024, reverse-engineering, windows, debugger, outputdebugstring]
sources: [https://github.com/noamgariani11/picoCTF-2024-Writeup/blob/main/Reverse%20Engineering/WinAntiDbg0x200.md, https://picoctfsolutions.com/picoctf-2024-winantidbg0x200]
confidence: medium
---

# WinAntiDbg0x200 — picoCTF 2024 reverse engineering writeup

## 참고 URL
- [GitHub writeup](https://github.com/noamgariani11/picoCTF-2024-Writeup/blob/main/Reverse%20Engineering/WinAntiDbg0x200.md)
- [picoCTF Solutions](https://picoctfsolutions.com/picoctf-2024-winantidbg0x200)

## 핵심 요약
이 문제는 Windows 실행 파일의 여러 anti-debug check를 순서대로 우회한 뒤, 최종 flag 경로로 흐르게 만드는 리버싱 문제입니다.
공개 해설 기준으로는 Ghidra에서 체크 지점을 먼저 찾고, x32dbg에서 각 분기 조건을 맞춰 주는 방식이 핵심입니다.

## 풀이 메모
1. `WinAntiDbg0x200.zip`을 풀고, Ghidra에서 실행 흐름과 anti-debug 분기 지점을 먼저 확인합니다.
2. 공개 해설 기준으로 핵심 체크는 3개이며, 각 체크는 서로 다른 조건과 분기 방향을 가집니다.
3. 32-bit x32dbg에서 각 분기 지점의 마지막 4자리 주소를 기준으로 브레이크포인트를 맞춥니다.
4. 첫 번째/두 번째 체크는 레지스터 값을 맞춰 `JNZ` 분기를 통과시키고, 세 번째 체크는 `IsDebuggerPresent` 흐름에서 `EAX=0`이 되도록 조정합니다.
5. 최종 flag는 `OutputDebugString`으로 로그 창에 출력되므로, x32dbg의 *Log* 탭을 확인합니다.

## 방어 관점 메모
- 여러 anti-debug check를 한 번에 매핑하지 않으면, 우회한 뒤 다른 체크에 걸려 다시 실패하기 쉽습니다.
- `OutputDebugString` 기반 출력은 콘솔이 아니라 디버거 로그에 찍히는 경우가 많습니다.

## 같이 보면 좋은 페이지
- [[picoctf-2024-reverse-engineering-survey]]
- [[picoctf-2024-reverse-engineering-family-hub]]
- [[picoctf-2024-topic-map]]
