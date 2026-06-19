---
title: picoCTF 2023 pwn survey
created: 2026-06-15
updated: 2026-06-16
type: query
tags: [ctf, pwn, survey, picoctf, picoctf2023]
sources: [snwau/picoCTF-2023-Writeup, DanArmor/picoCTF-2023-writeup, participant profiles]
---

# picoCTF 2023 pwn survey

> picoCTF 2023 Binary Exploitation의 전체 문제를 한 번에 보는 요약 페이지입니다.
> 현재 위키에는 **7/7 문제**가 모두 정리되어 있습니다.
> 상위 허브: [[picoctf-pwn-survey]]

| # | 문제 | 상태 | 핵심 primitive | 연결 문서 |
|---|---|---|---|---|
| 1 | babygame01 | solved | out-of-bounds / game-state corruption | [[babygame01-final-writeup]] |
| 2 | two-sum | solved | integer overflow / logic bug | [[two-sum-final-writeup]] |
| 3 | babygame02 | solved | out-of-bounds / partial overwrite | [[babygame02-final-writeup]] |
| 4 | hijacking | solved | module hijack / environment abuse | [[hijacking-final-writeup]] |
| 5 | tic-tac | solved | buffer overflow / saved return address | [[tic-tac-final-writeup]] |
| 6 | VNE | solved | environment / command abuse | [[vne-final-writeup]] |
| 7 | Horsetrack | solved | heap / tcache poisoning | [[horsetrack-final-writeup]] |

## 문제 묶음별 해석
### 1) 게임 상태 변조 계열
- `babygame01`
- `babygame02`

맵 경계 밖 이동으로 상태를 바꾸는 문제들입니다. 단순 이동 로직처럼 보이지만 실제로는 상태 배열이 공격면이 됩니다.

### 2) 로직 결함 계열
- `two-sum`

계산값 검증이 허술하면, 메모리 오염이 없어도 조건 우회를 만들 수 있습니다.

### 3) 환경/경로 조작 계열
- `hijacking`
- `VNE`

import search path나 `PATH`/셸 실행 순서를 공격합니다. 바이너리보다는 실행 환경이 핵심입니다.

### 4) 고전적인 ret2win 계열
- `tic-tac`

버퍼 오버플로우로 리턴 주소를 바꾸는 기본형입니다.

### 5) Heap 계열
- `Horsetrack`

tcache poisoning과 같은 힙 오염 패턴을 사용합니다.

## 짧은 결론
- `babygame01`/`babygame02`는 게임 상태 변조 계열입니다.
- `two-sum`은 산술 오버플로우 기반 로직 결함입니다.
- `hijacking`과 `VNE`는 환경/경로 조작 계열입니다.
- `Horsetrack`은 heap/tcache 계열의 마지막 문제입니다.

## 참고
- [snwau/picoCTF-2023-Writeup](https://github.com/snwau/picoCTF-2023-Writeup)
- [DanArmor/picoCTF-2023-writeup](https://github.com/DanArmor/picoCTF-2023-writeup)
