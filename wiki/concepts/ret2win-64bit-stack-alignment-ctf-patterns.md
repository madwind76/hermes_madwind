---
title: 64-bit ret2win / stack alignment — CTF patterns
created: 2026-06-15
updated: 2026-06-21
type: concept
tags: [ctf, pwn, ret2win, x64, stack-alignment, function-prologue, buffer-overflow]
sources: [https://ctftime.org/writeup/32813, https://cryptocat.me/blog/ctf/2022/pico/pwn/x_sixty_what/, https://github.com/HHousen/PicoCTF-2022/blob/master/Binary%20Exploitation/x-sixty-what/README.md]
confidence: high
---

# 64-bit ret2win / stack alignment — CTF patterns

## 참고 URL
- [CTFtime writeup](https://ctftime.org/writeup/32813)
- [cryptocat.me](https://cryptocat.me/blog/ctf/2022/pico/pwn/x_sixty_what/)
- [Original source](https://github.com/HHousen/PicoCTF-2022/blob/master/Binary%20Exploitation/x-sixty-what/README.md)

## Step 1. 단어 풀이
- **ret2win**: 리턴 주소를 덮어서 숨겨진 `win()`/`flag()` 함수로 보내는 기법입니다.
- **stack alignment**: 64-bit 호출 규약에서 스택 정렬이 맞아야 함수 호출이 안정적으로 동작하는 성질입니다.
- **function prologue**: 함수 시작 부분의 `push rbp`, `mov rbp, rsp` 같은 준비 코드입니다.

## 한 문장 정의
이 패턴은 **64-bit 바이너리에서 단순히 주소만 덮는 것으로는 부족할 때, 스택 정렬과 함수 prologue를 고려해 올바른 instruction 지점으로 점프하는 문제 유형**입니다.

## 핵심 흐름
```text
overflow -> RIP overwrite -> align/skip prologue -> win()/flag() -> flag
```

## 전문 설명
64-bit에서는 다음이 자주 문제를 일으킵니다.

1. 리턴 주소가 8바이트입니다.
2. 함수 시작 주소에 바로 점프하면 prologue에서 예기치 않은 동작이 나올 수 있습니다.
3. 스택 정렬이 맞지 않으면 함수 내부의 `call`/`movaps` 등에서 크래시가 날 수 있습니다.
4. 따라서 `ret` 한 번을 끼우거나, 함수의 **두 번째 instruction**으로 점프하는 방식이 안정적입니다.

## 공격자 관점
- `checksec`로 PIE/canary/NX 상태를 확인합니다.
- 오프셋을 정확히 계산합니다.
- `win`/`flag` 함수의 실제 엔트리와 내부 instruction 위치를 비교합니다.
- 필요하면 `ret` 가젯이나 prologue-skipping 주소를 사용합니다.

## 방어자 관점
- PIE와 canary를 함께 적용합니다.
- 위험 함수(`gets`, `strcpy`, `scanf %s`)를 사용하지 않습니다.
- 함수 진입점 주변의 가젯만으로 끝나지 않도록 CFI/IBT를 고려합니다.

## 관련 writeup
- [[x-sixty-what-final-writeup]]

## 같이 보면 좋은 개념
- [[stack-leak-ret2win-ctf-patterns]]
- [[rop-chain-execve-ctf-patterns]]
- [[ret2reg-executable-stack-ctf-patterns]]
