---
title: two-sum — picoCTF 2023 pwn writeup
created: 2026-06-15
updated: 2026-06-15
type: query
tags: [ctf, pwn, integer-overflow, logic-bug, picoctf, picoctf2023]
sources: [snwau/picoCTF-2023-Writeup, picoCTF participant profiles]
---

# two-sum — picoCTF 2023 pwn writeup

> `two-sum`은 **두 수의 합 비교 조건을 정수 오버플로우로 깨는 문제**입니다. 핵심은 **integer overflow + logic bug**입니다.

## 요약
- 분류: pwn
- 핵심 primitive: integer overflow / logic bug
- 난이도 감각: 초급~중급
- 연결 개념: [[integer-overflow-logic-bug-ctf-patterns]]

## 취약점 원인
두 값의 합을 검사하는 과정에서 타입 범위를 고려하지 않으면, 실제 합은 크게 벗어나도 연산 결과가 작은 값으로 바뀌어 조건문을 통과할 수 있습니다. 이 문제는 메모리 corruption보다 **검증 로직의 허점**이 핵심입니다.

## 공격 흐름
1. 입력 형식과 합 계산이 어떤 타입으로 이루어지는지 확인합니다.
2. 오버플로우가 발생하는 경계값을 계산합니다.
3. 조건 분기에서 잘못된 참/거짓 판정을 유도합니다.
4. 검증 우회를 통해 flag 경로로 진입합니다.

## 실전 포인트
- signed/unsigned 혼용 여부를 확인해야 합니다.
- 32-bit 정수인지 64-bit 정수인지에 따라 오버플로우 임계값이 달라집니다.
- 합이 아니라 개별 입력의 범위를 따로 검사하는지 여부도 중요합니다.

## 방어 관점
- 산술 연산 전 범위 검사를 수행합니다.
- 자료형을 명시적으로 고정하고, 부호 처리를 일관되게 유지합니다.
- 결과값만 검증하지 말고 입력값 자체를 먼저 검증합니다.

## 재현 절차
1. 합 계산에 사용되는 자료형과 비교 조건을 확인합니다.
2. 오버플로우가 발생하는 경계값을 계산합니다.
3. 조건 분기 우회가 되는 입력을 넣어 flag 경로를 재현합니다.

```bash
# 파이썬으로 32-bit/64-bit 오버플로우 경계값을 빠르게 계산합니다.
python3 - <<'PY'
# 예시: 정수 범위 확인용 스니펫입니다.
for bits in (32, 64):
    limit = 2 ** (bits - 1) - 1
    print(f'{bits}-bit signed max = {limit}')
PY

# 로컬 바이너리가 있으면 입력값을 직접 넣어 동작을 확인합니다.
./two-sum
```

## 참고
- [snwau writeup](https://github.com/snwau/picoCTF-2023-Writeup/blob/main/Binary%20Exploitation/two-sum/two-sum.md)
