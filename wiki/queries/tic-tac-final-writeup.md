---
title: tic-tac — picoCTF 2023 pwn writeup
created: 2026-06-15
updated: 2026-06-15
type: query
tags: [ctf, pwn, buffer-overflow, return-address, picoctf, picoctf2023]
sources: [snwau/picoCTF-2023-Writeup, DanArmor/picoCTF-2023-writeup]
---

# tic-tac — picoCTF 2023 pwn writeup

> `tic-tac`은 **전형적인 버퍼 오버플로우로 제어 흐름을 바꾸는 문제**입니다. 핵심은 **saved return address control**입니다.

## 요약
- 분류: pwn
- 핵심 primitive: buffer overflow / saved return address control
- 난이도 감각: 초급
- 연결 개념: [[saved-return-address-control-ctf-patterns]]

## 취약점 원인
사용자의 입력이 스택 버퍼에 그대로 복사되고 길이 검사가 없으면, 함수의 지역 변수와 saved return address까지 덮을 수 있습니다. 이 문제는 실전에서 가장 기본적인 **ret2win형 overrun**입니다.

## 공격 흐름
1. 입력 버퍼와 saved RIP 사이의 오프셋을 찾습니다.
2. `win()` 함수나 목표 함수 주소를 확인합니다.
3. 오프셋만큼 패딩을 넣고 리턴 주소를 덮습니다.
4. 제어 흐름을 목표 함수로 이동시킵니다.

## 실전 포인트
- 64-bit에서는 stack alignment 이슈를 같이 봐야 합니다.
- 함수 앞에 `push rbp` / `sub rsp, ...`가 있으면 오프셋 계산이 달라질 수 있습니다.
- PIE가 꺼져 있으면 주소가 고정인 경우가 많아 ret2win이 더 단순합니다.

## 방어 관점
- `fgets`, `snprintf` 같은 길이 제한 함수를 사용합니다.
- stack canary, NX, PIE를 함께 적용합니다.
- 입력 길이를 명확히 제한하고 실패 시 종료합니다.

## 재현 절차
1. 입력 버퍼와 saved return address 사이의 거리를 확인합니다.
2. `win()` 주소를 찾고 패딩 길이를 맞춥니다.
3. 리턴 주소를 덮어 제어 흐름이 이동하는지 검증합니다.

```bash
# 오프셋을 찾기 위해 cyclic 패턴을 넣고 크래시 위치를 관찰합니다.
python3 - <<'PY'
# 예시: 입력 길이 검증용 더미 패턴 생성
print('A' * 64)
PY

# 바이너리를 실행해 오프셋을 조정합니다.
./tic-tac
```

## 참고
- [Brandon T. Elliott writeup](https://brandon-t-elliott.github.io/tic-tac)
