---
title: WinAntiDbg0x300 — picoCTF 2024 reverse engineering writeup
created: 2026-06-24
updated: 2026-06-24
type: query
tags: [ctf, picoctf, picoctf2024, reverse-engineering, windows, debugger, outputdebugstring]
sources: [https://github.com/noamgariani11/picoCTF-2024-Writeup/blob/main/Reverse%20Engineering/WinAntiDbg0x300.md, https://picoctfsolutions.com/picoctf-2024-winantidbg0x300]
confidence: medium
---

# WinAntiDbg0x300 — picoCTF 2024 reverse engineering writeup

## 참고 URL
- [GitHub writeup](https://github.com/noamgariani11/picoCTF-2024-Writeup/blob/main/Reverse%20Engineering/WinAntiDbg0x300.md)
- [picoCTF Solutions](https://picoctfsolutions.com/picoctf-2024-winantidbg0x300)

## 핵심 요약
이 문제는 디버거를 적극적으로 방해하는 Windows 바이너리를 패치해서, 최종적으로 `OutputDebugString` 기반 flag 출력 경로에 도달하는 문제입니다.
공개 해설에서는 UPX 언팩, PDB 활용, Ghidra 패치, DebugView 관찰 흐름이 핵심입니다.

## 풀이 메모
1. `WinAntiDbg0x300.exe`를 `upx -d`로 먼저 언팩하고, Ghidra에 PDB를 함께 넣어 심볼 이름을 복원합니다.
2. `WinMain`과 `challenge_create_thread` 흐름을 확인한 뒤, 무한 루프를 유지하는 `JMP`를 찾습니다.
3. 해당 무조건 분기를 `NOP`으로 패치하면 flag 경로로 fall-through 할 수 있습니다.
4. 실제 flag는 일반 콘솔이 아니라 `DebugView`의 출력 창에서 확인합니다.
5. 실행 시 5초 정도의 지연이 있으므로, 패치 후 바로 출력되지 않더라도 잠시 기다립니다.

## 방어 관점 메모
- 디버거를 직접 붙이면 child process가 종료시키는 구조라서, 패치/관찰 도구를 분리하는 접근이 필요합니다.
- `OutputDebugString`은 표준 출력이 아니므로, 관찰 도구를 잘못 고르면 flag가 안 보입니다.

## 같이 보면 좋은 페이지
- [[picoctf-2024-reverse-engineering-survey]]
- [[picoctf-2024-reverse-engineering-family-hub]]
- [[picoctf-2024-topic-map]]
