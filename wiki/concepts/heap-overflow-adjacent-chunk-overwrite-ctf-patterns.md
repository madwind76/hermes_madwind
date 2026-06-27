---
title: Heap overflow / adjacent chunk overwrite — CTF patterns
created: 2026-06-15
updated: 2026-06-21
type: concept
tags: [ctf, pwn, heap-overflow, adjacent-chunk, buffer-overflow, safe_var, heap-layout]
sources: [https://github.com/snwau/picoCTF-2024-Writeup/blob/main/Binary%20Exploitation/heap%200/heap%200.md, https://medium.com/@kenjikun/picoctf-binary-exploitation-2024-f5125b8874be, https://hackmd.io/@Zzzzek/r14x13FRp]
confidence: high
---

# Heap overflow / adjacent chunk overwrite — CTF patterns

> **힙 오버플로우**는 힙에 할당된 버퍼를 넘어 인접한 chunk의 데이터나 제어 변수를 덮어쓰는 공격 패턴입니다. 스택 오버플로우와 동일하게, **길이 검사가 없는 입력**이 핵심 원인입니다.

## 참고 URL
- [Original source](https://github.com/snwau/picoCTF-2024-Writeup/blob/main/Binary%20Exploitation/heap%200/heap%200.md)
- [medium.com](https://medium.com/@kenjikun/picoctf-binary-exploitation-2024-f5125b8874be)
- [hackmd.io](https://hackmd.io/@Zzzzek/r14x13FRp)

## 1. 이 패턴이 자주 나오는 곳

- 메뉴 기반 바이너리에서 `write to buffer` 기능이 있을 때
- `scanf("%s")`, `gets()`, `strcpy()`, `memcpy()`처럼 길이 제한이 없거나 부적절한 입력 처리
- 중요한 체크 변수가 heap 상에 같이 배치되어 있을 때

## 2. 공격 흐름

1. heap 레이아웃을 출력하거나 디버깅으로 확인합니다.
2. 버퍼와 대상 변수 사이의 **오프셋**을 구합니다.
3. 오프셋만큼 데이터를 넣어 인접한 chunk를 덮습니다.
4. 상태 변수(`safe_var`) 또는 포인터 값을 바꿔 조건을 만족시킵니다.

## 3. 대표 예시

| 문제 | 핵심 |
|------|------|
| `heap 0` | `input_data`에서 `safe_var`까지 32바이트를 덮어써 flag 조건을 만족 |
| `heap 1` | `safe_var`를 특정 문자열(`pico`)로 정확히 맞춤 |
| `heap 2/3` | heap 위의 function pointer / use-after-free로 확장 |

## 4. 방어 포인트

- 입력 길이 검사를 강제합니다.
- 중요한 검증 값은 heap의 인접한 위치에 두지 않습니다.
- ASan/Valgrind로 인접 메모리 overwrite를 검출합니다.

## 5. 참고 연결

- [[buffer-overflow-ctf-patterns]]
- [[heap-0-final-writeup]]
- [[heap-1-final-writeup]]
- [[heap-2-final-writeup]]
- [[heap-3-final-writeup]]
