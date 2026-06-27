---
title: babygame02 — picoCTF 2023 pwn writeup
created: 2026-06-15
updated: 2026-06-15
type: query
tags: [ctf, pwn, oob, partial-overwrite, game-state, picoctf, picoctf2023]
sources: [snwau/picoCTF-2023-Writeup, DanArmor/picoCTF-2023-writeup, picoCTF participant profiles]
---

# babygame02 — picoCTF 2023 pwn writeup

> `babygame02`은 **게임 상태를 더 깊게 건드리는 후속 문제**입니다. 핵심은 **out-of-bounds movement + partial overwrite**입니다.

## 참고 URL
- [snwau/picoCTF-2023-Writeup](snwau/picoCTF-2023-Writeup)
- [DanArmor/picoCTF-2023-writeup](DanArmor/picoCTF-2023-writeup)
- [picoCTF participant profiles](picoCTF participant profiles)


## 요약
- 분류: pwn
- 핵심 primitive: game-state corruption / partial overwrite
- 난이도 감각: 중급
- 연결 개념: [[oob-movement-game-state-corruption-ctf-patterns]]

## 취약점 원인
1편과 비슷하게 맵 바깥 이동이 가능하지만, 2편은 보통 더 많은 상태 값이 존재해 **작은 덮기만으로도 흐름을 바꿀 수 있는 구조**를 가집니다. 즉, 큰 메모리 쓰기보다 **정확한 위치를 찌르는 작은 오염**이 중요합니다.

## 공격 흐름
1. 이동 명령과 게임 오브젝트 배치를 파악합니다.
2. 맵 바깥으로 나가서 덮을 수 있는 필드를 찾습니다.
3. 플래그 조건, 함수 포인터, 상태 플래그 중 하나를 조작합니다.
4. 적절한 종료 조건을 만족시켜 win path로 진입합니다.

## 실전 포인트
- `babygame01`보다 상태 오염 포인트가 더 섬세한 편입니다.
- partial overwrite는 완전한 주소 덮기보다 안정적일 수 있습니다.
- 출력 메시지가 상태 변화를 암시하는 경우가 많아 로그를 잘 봐야 합니다.

## 방어 관점
- 이동 가능 좌표와 상태 저장 메모리를 강하게 분리합니다.
- 상태값은 enum 또는 상수로 제한합니다.
- OOB가 발생해도 인접 상태를 덮을 수 없도록 레이아웃을 설계합니다.

## 재현 절차
1. 이동 가능한 범위와 오염 가능한 상태 필드를 확인합니다.
2. OOB 이동으로 어떤 값이 바뀌는지 관찰합니다.
3. partial overwrite가 성공하는 입력을 찾아 목표 상태를 만듭니다.

```bash
# 게임 상태 변화를 눈으로 확인하기 위해 바이너리를 직접 실행합니다.
./babygame02

# 디버그 모드에서 상태 오염 위치를 확인합니다.
gdb -q ./babygame02
```

## 참고
- [snwau writeup](https://github.com/snwau/picoCTF-2023-Writeup/blob/main/Binary%20Exploitation/babygame02/babygame02.md)
