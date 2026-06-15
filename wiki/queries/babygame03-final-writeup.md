---
title: babygame03 — picoCTF 2024 pwn writeup
created: 2026-06-15
updated: 2026-06-15
type: query
tags: [ctf, pwn, out-of-bounds, underflow, game-state, memory-corruption, picoctf]
sources: [https://yun.ng/c/ctf/picoctf/pwn/babygame03, https://hackmd.io/@Zzzzek/r14x13FRp, https://github.com/snwau/picoCTF-2024-Writeup/blob/main/Binary%20Exploitation/babygame03/babygame03.md]
confidence: high
---

# babygame03 — picoCTF 2024 pwn writeup

> `babygame03`는 **그리드 밖으로 이동하는 out-of-bounds/underflow를 이용해 게임 상태를 바꾸는 문제**입니다.

## 핵심 요약
- 플레이어 정보가 맵 근처에 배치됩니다.
- 맵의 시작점에서 뒤로 이동하면 underflow가 가능합니다.
- 무한 생명 상태를 만든 뒤 자동 해결 명령을 사용합니다.

## 공격 흐름
1. 경계 밖으로 이동해 주변 메모리를 덮습니다.
2. 생명 수를 비정상적으로 크게 만듭니다.
3. `p` 같은 자동 솔버 명령을 사용합니다.
4. level 4 체크를 우회하고 최종 win 주소로 분기합니다.

## 학습 포인트
- 게임 바이너리도 결국 메모리 문제입니다.
- out-of-bounds는 데이터와 제어 흐름 둘 다 망가뜨릴 수 있습니다.

## 방어 관점
- 배열 경계 검사와 상태 검증을 강제합니다.
- 게임 상태를 인접 메모리에 두지 않습니다.

## 재현 절차
1. 게임 좌표와 맵 경계 조건을 확인합니다.
2. OOB 이동으로 덮이는 필드를 찾아봅니다.
3. 상태 변조가 발생하는 경로를 재현합니다.

```bash
# 게임 바이너리를 실행해 이동 명령을 직접 입력합니다.
./babygame03

# 상태 변화를 추적할 때 gdb를 사용합니다.
gdb -q ./babygame03
```

## 관련 개념
- [[oob-movement-game-state-corruption-ctf-patterns]]
