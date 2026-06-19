---
title: picoCTF 2022 pwn survey
created: 2026-06-16
updated: 2026-06-16
type: query
tags: [ctf, pwn, survey, picoctf, picoctf2022]
sources: [picoCTF 2022 public writeups, participant profiles]
---

# picoCTF 2022 pwn survey

> picoCTF 2022 Binary Exploitation 문제를 한 번에 보는 요약 페이지입니다.
> 현재 위키에는 **10/10 문제**가 모두 정리되어 있습니다.
> 상위 허브: [[picoctf-pwn-survey]]

| # | 문제 | 상태 | 핵심 primitive | 연결 문서 |
|---|---|---|---|---|
| 1 | buffer overflow 0 | solved | intentional crash / signal handler | [[buffer-overflow-0-final-writeup]] |
| 2 | buffer overflow 1 | solved | saved return address control | [[buffer-overflow-1-final-writeup]] |
| 3 | buffer overflow 2 | solved | ret2win / function argument control | [[buffer-overflow-2-final-writeup]] |
| 4 | buffer overflow 3 | solved | stack canary brute force | [[buffer-overflow-3-final-writeup]] |
| 5 | x-sixty-what | solved | 64-bit ret2win / stack alignment | [[x-sixty-what-final-writeup]] |
| 6 | stack cache | solved | stack leak / ret2win | [[stack-cache-final-writeup]] |
| 7 | RPS | solved | substring logic bug | [[rps-final-writeup]] |
| 8 | ropfu | solved | classic ROP / execve | [[ropfu-final-writeup]] |
| 9 | function overwrite | solved | function pointer overwrite | [[function-overwrite-final-writeup]] |
| 10 | flag leak | solved | format string | [[flag-leak-final-writeup]] |

## 문제 묶음별 해석

### 1) 기본 스택 오버플로우 계열
- `buffer overflow 0`
- `buffer overflow 1`
- `buffer overflow 2`
- `buffer overflow 3`
- `x-sixty-what`
- `stack cache`

이 묶음은 저장된 리턴 주소, 함수 인자, canary, 64-bit stack alignment, stack leak 같은 pwn의 기본기를 확인하는 구간입니다.

### 2) 논리 결함 계열
- `RPS`

메모리 오염이 아니라 문자열 비교/검증 로직의 허점을 이용하는 문제입니다.

### 3) 제어 흐름 변조 계열
- `ropfu`
- `function overwrite`

ROP chain 구성, execve 호출, 함수 포인터 덮어쓰기 같은 primitive를 확인하는 구간입니다.

### 4) 정보 유출 계열
- `flag leak`

`printf` 계열 형식 문자열을 이용한 정보 유출/메모리 읽기 패턴입니다.

## 짧은 결론
- 2022 pwn은 **stack overflow / canary / ret2win / ROP / format string / logic bug**가 고르게 배치되어 있습니다.
- 위키에는 현재 **10/10 문제**가 모두 정리되어 있습니다.

## 참고
- [[picoctf-pwn-survey]]
- [[buffer-overflow-0-final-writeup]]
- [[buffer-overflow-1-final-writeup]]
- [[buffer-overflow-2-final-writeup]]
- [[buffer-overflow-3-final-writeup]]
- [[x-sixty-what-final-writeup]]
- [[stack-cache-final-writeup]]
- [[rps-final-writeup]]
- [[ropfu-final-writeup]]
- [[function-overwrite-final-writeup]]
- [[flag-leak-final-writeup]]
