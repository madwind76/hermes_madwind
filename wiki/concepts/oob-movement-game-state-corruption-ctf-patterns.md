---
title: Out-of-bounds movement / game-state corruption — CTF patterns
created: 2026-06-15
updated: 2026-06-15
type: concept
tags: [ctf, pwn, out-of-bounds, underflow, game-state, array-bounds, movement]
sources: [https://yun.ng/c/ctf/picoctf/pwn/babygame03, https://hackmd.io/@Zzzzek/r14x13FRp]
confidence: high
---

# Out-of-bounds movement / game-state corruption — CTF patterns

> 그리드형 게임이나 맵 기반 바이너리에서 **경계 밖 이동**이 허용되면, 플레이어 상태가 인접 메모리와 겹치면서 게임 규칙 자체를 무너뜨릴 수 있습니다.

## 패턴
- 맵 배열의 앞/뒤로 이동해 underflow 또는 overflow를 일으킵니다.
- 플레이어 좌표, 생명 수, 체크 플래그가 옆 메모리에 있으면 같이 덮입니다.
- 자동 해결 명령이나 숨겨진 함수 호출을 이용해 최종 상태로 점프합니다.

## 공격 흐름
1. 경계 검사 부족을 확인합니다.
2. 배열의 시작/끝을 넘어 이동해 주변 상태를 바꿉니다.
3. 무한 생명, 레벨 스킵, 승리 조건 우회 등을 달성합니다.
4. 마지막 체크를 통과해 flag를 얻습니다.

## 방어 포인트
- 배열 인덱스 검사를 강제합니다.
- 상태 변수와 사용자 입력을 인접하게 두지 않습니다.
- 게임 로직과 메모리 레이아웃을 분리합니다.

## 예시
- `babygame03`
