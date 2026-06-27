---
title: Buffer overflow — CTF patterns
created: 2026-06-23
updated: 2026-06-23
type: concept
tags: [ctf, pwn, buffer-overflow, stack-overflow, heap-overflow, saved-return-address]
sources: [https://medium.com/@muranyi.levente/picoctf-2022-buffer-overflow-0-f26e5fc9b31e, https://colej.net/picoctf-2022-buffer-overflow-1, https://github.com/snwau/picoCTF-2024-Writeup/blob/main/Binary%20Exploitation/heap%200/heap%200.md]
confidence: high
---

# Buffer overflow — CTF patterns

## 참고 URL
- [medium.com](https://medium.com/@muranyi.levente/picoctf-2022-buffer-overflow-0-f26e5fc9b31e)
- [colej.net](https://colej.net/picoctf-2022-buffer-overflow-1)
- [GitHub writeup](https://github.com/snwau/picoCTF-2024-Writeup/blob/main/Binary%20Exploitation/heap%200/heap%200.md)

## Step 1. 단어 풀이
- **Buffer overflow**: 버퍼에 허용된 크기보다 더 많은 데이터를 써서 인접 메모리를 덮는 취약점입니다.
- **Stack overflow**: 스택에 있는 지역 버퍼를 넘쳐 saved return address나 canary를 건드리는 경우입니다.
- **Heap overflow**: 힙에 있는 버퍼를 넘어 인접 chunk나 제어 변수를 덮는 경우입니다.

## 한 문장 정의
이 패턴은 **길이 검사가 없는 입력을 통해 스택 또는 힙의 인접 메모리를 덮고, 함수 흐름이나 검증 변수를 바꿔 flag를 얻는 문제 유형**입니다.

## 핵심 흐름
```text
unchecked input -> buffer overwrite -> control data / checker corruption -> win() / flag / arbitrary action
```

## 전문 설명
버퍼 오버플로우는 pwn의 가장 넓은 출발점입니다. 스택에서는 saved return address를 덮어 `ret2win`으로 이어지고, 힙에서는 인접 chunk나 상태 변수를 바꿔 flag 조건을 만족시킵니다.

보호 기법이 있어도 문제 구조에 따라 우회 경로가 달라집니다.

1. **NX**가 있어도 return address overwrite는 여전히 가능합니다.
2. **Canary**가 있으면 leak이 필요하거나 canary를 건드리지 않는 경로를 찾아야 합니다.
3. **PIE**가 있으면 주소 leak과 offset 계산이 추가됩니다.
4. **Heap** 문제는 레이아웃과 chunk 간 거리 계산이 핵심입니다.

## 공격자 관점
- 먼저 입력 길이와 버퍼 크기를 비교합니다.
- 오프셋을 찾아 어떤 제어 값을 덮을 수 있는지 확인합니다.
- `win()` 호출, saved return address overwrite, 상태 변수 변조 중 가능한 경로를 고릅니다.

## 방어자 관점
- `gets`, `strcpy`, 길이 없는 `%s` 입력을 제거합니다.
- canary, PIE, NX, RELRO를 조합합니다.
- 힙/스택의 중요한 상태 변수 옆에 가변 길이 입력을 두지 않습니다.

## 관련 개념
- [[picoctf-2025-pwn-family-hub]]
- [[saved-return-address-control-ctf-patterns]]
- [[heap-overflow-adjacent-chunk-overwrite-ctf-patterns]]
- [[ret2win-with-arguments-ctf-patterns]]
