---
title: Function pointer overwrite — CTF patterns
created: 2026-06-15
updated: 2026-06-15
type: concept
tags: [ctf, pwn, function-pointer, arbitrary-write, out-of-bounds, control-flow-hijack]
sources: [https://picoctf2022.haydenhousen.com/binary-exploitation/function-overwrite, https://cryptocat.me/blog/ctf/2022/pico/pwn/function_overwrite/]
confidence: high
---

# Function pointer overwrite — CTF patterns

## Step 1. 단어 풀이
- **Function pointer**: 함수를 가리키는 포인터입니다.
- **Overwrite**: 기존 값을 덮어 다른 값으로 바꾸는 행위입니다.
- **Out-of-bounds write**: 배열 범위를 벗어난 위치에 쓰는 취약점입니다.

## 한 문장 정의
이 패턴은 **배열 인덱스 오류나 임의 쓰기 원시를 이용해 함수 포인터를 다른 함수로 바꿔 제어 흐름을 탈취하는 문제 유형**입니다.

## 핵심 흐름
```text
user input -> index mistake -> out-of-bounds write -> function pointer corruption -> hidden win/easy checker call
```

## 전문 설명
이 유형은 보통 다음 형태로 나타납니다.

1. 배열 근처에 함수 포인터가 배치됩니다.
2. 인덱스 검사가 상한만 있거나, 음수 인덱스를 허용합니다.
3. 포인터 값 자체를 덮거나, 포인터가 가리키는 주소를 우회적으로 수정합니다.
4. 결과적으로 `win()`, `easy_checker()`, `admin()` 같은 함수로 분기합니다.

## 공격자 관점
- 메모리 레이아웃을 먼저 파악합니다.
- 음수 인덱스, 큰 인덱스, 덧셈/감산형 write primitive를 시험합니다.
- 대상 함수 간 오프셋을 계산해 덮을 값을 정합니다.
- 간단한 델타 조작으로 우회가 되는지 확인합니다.

## 방어자 관점
- 배열 접근은 하한과 상한 모두 검증합니다.
- 함수 포인터는 가능하면 직접 노출하지 않습니다.
- 구조체 배치 시 민감한 포인터를 사용자 데이터 근처에 두지 않습니다.
- 정적 분석과 sanitizers로 OOB write를 조기에 잡습니다.

## 관련 writeup
- [[function-overwrite-final-writeup]]

## 같이 보면 좋은 개념
- [[exploitation]]
- [[ret2reg-executable-stack-ctf-patterns]]
- [[pie-aslr-function-offset-ctf-patterns]]
