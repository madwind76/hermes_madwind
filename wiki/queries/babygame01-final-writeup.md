---
title: babygame01 — picoCTF 2023 pwn writeup
created: 2026-06-15
updated: 2026-06-15
type: query
tags: [ctf, pwn, oob, game-state, picoctf, picoctf2023]
sources: [snwau/picoCTF-2023-Writeup, DanArmor/picoCTF-2023-writeup, picoCTF participant profiles]
---

# babygame01 — picoCTF 2023 pwn writeup

> `babygame01`은 **게임 맵 경계 밖으로 이동해 게임 상태를 망가뜨리는 pwn 문제**입니다. 핵심은 **out-of-bounds movement + game-state corruption**입니다.

## 요약
- 분류: pwn
- 핵심 primitive: out-of-bounds movement
- 난이도 감각: 초중급
- 연결 개념: [[oob-movement-game-state-corruption-ctf-patterns]]

## 취약점 원인
이동 함수가 좌표 범위를 충분히 검증하지 않으면, 플레이어 위치가 맵 바깥으로 벗어납니다. 이 상태에서 인접한 메모리 슬롯이 맵 데이터와 겹치면, 실제로는 단순 이동처럼 보이는 입력이 **상태 값 덮기(write primitive)** 로 바뀝니다.

## 공격 흐름
1. 맵의 좌표 체계와 이동 명령의 동작을 파악합니다.
2. 경계 체크가 어디에서 빠지는지 찾습니다.
3. 맵 바깥 좌표로 이동해 상태 배열/플래그를 덮습니다.
4. `win()` 또는 flag 조건이 만족되도록 게임 상태를 조작합니다.

## 실전 포인트
- 좌표를 한 번만 검사하는지, 혹은 각 이동 단계마다 검사하는지 구분해야 합니다.
- 음수 좌표와 overflow가 함께 쓰이면 더 쉽게 우회가 됩니다.
- 게임 로직상 `x`, `y`, `score`, `level` 등이 인접하게 배치되는지 확인하면 좋습니다.

## 방어 관점
- 좌표 경계 검증을 반드시 수행해야 합니다.
- 배열 인덱스와 플레이어 위치를 분리해야 합니다.
- 상태 구조체를 직접 수정하지 못하도록 캡슐화해야 합니다.

## 재현 절차
1. 바이너리를 실행해 이동 입력과 맵 크기를 확인합니다.
2. 경계 체크가 빠지는 좌표 조합을 찾습니다.
3. 상태 값이 덮이는 지점을 찾은 뒤 win 조건을 재현합니다.

```bash
# 문제 바이너리를 실행해 입력 형식을 먼저 확인합니다.
./babygame01

# 디버깅용으로 gdb를 붙여 좌표 변경 시 메모리 상태를 관찰합니다.
gdb -q ./babygame01
```

## 참고
- [snwau writeup](https://github.com/snwau/picoCTF-2023-Writeup/blob/main/Binary%20Exploitation/babygame01/babygame01.md)
