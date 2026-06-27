---
title: PIE/ASLR function offset — CTF patterns
created: 2026-06-15
updated: 2026-06-21
type: concept
tags: [ctf, pwn, binary-exploitation, pie, aslr, info-leak, function-pointer]
sources: [https://medium.com/@routbiswajit70681/picoctf-write-up-pie-time-37ffcdc29b71, https://systemweakness.com/pie-time-picoctf-2025-dbec42ba0857, https://github.com/snwau/picoCTF-2025-Writeup/blob/main/Binary%20Exploitation/PIE%20TIME/PIE%20TIME.md]
confidence: high
---

# PIE/ASLR function offset — CTF patterns

## 참고 URL
- [medium.com](https://medium.com/@routbiswajit70681/picoctf-write-up-pie-time-37ffcdc29b71)
- [systemweakness.com](https://systemweakness.com/pie-time-picoctf-2025-dbec42ba0857)
- [Original source](https://github.com/snwau/picoCTF-2025-Writeup/blob/main/Binary%20Exploitation/PIE%20TIME/PIE%20TIME.md)

## Step 1. 단어 풀이
- **PIE (Position Independent Executable)**: 실행될 때마다 코드 영역의 기준 주소가 달라지도록 만든 실행 파일 형식입니다.
- **ASLR (Address Space Layout Randomization)**: 프로세스의 주소 공간 배치를 무작위화하는 운영체제 보호 기법입니다.
- **Function offset**: 서로 다른 함수 사이의 고정된 거리입니다. 베이스가 바뀌어도 상대적 차이는 그대로 유지됩니다.

## 한 문장 정의
이 패턴은 **실행 중 누출된 함수 주소와 컴파일 시점의 고정 오프셋을 결합해, PIE/ASLR로 바뀐 목적지 함수 주소를 역산하는 문제 유형**입니다.

## 핵심 흐름
```text
info leak (main) -> fixed symbol offset recovery -> runtime target address calculation -> function pointer / return hijack -> win()
```

## 전문 설명
PIE가 활성화되면 `main`, `win`, `puts@plt` 같은 코드 주소는 매 실행마다 바뀝니다. 그러나 같은 바이너리 내부의 함수들 사이 간격은 동일하므로, 한 함수의 실행 주소를 알면 다른 함수의 주소를 계산할 수 있습니다.

이 유형은 보통 다음 조건 중 하나를 가집니다.

1. `printf("%p", &main)`처럼 **주소 누출**이 제공됩니다.
2. `readelf -s`나 `gdb disassemble`로 **심볼 오프셋**을 찾을 수 있습니다.
3. 입력이 함수 포인터, 리턴 주소, vtable, GOT/PLT, jump table로 연결됩니다.
4. 목표는 `win()` 호출, shellcode 실행, 또는 특정 승인 분기 진입입니다.

## 공격자 관점
- 먼저 프로그램이 어떤 주소를 새는지 확인합니다.
- 로컬과 원격 실행의 차이는 **base address만 다르다**는 점을 기억합니다.
- `win - main`, `target - leak`, `offset = leak - symbol` 관계를 표로 정리합니다.
- PIE가 있어도 **정보 누출이 있으면 우회 가능**한 경우가 많습니다.

## 방어자 관점
- 디버그용 주소 출력 제거
- 함수 포인터 입력 검증
- `printf("%p")` 같은 민감한 포맷 사용 최소화
- 정보 누출과 제어 흐름 변조가 결합되지 않도록 설계

## 관련 writeup
- [[pie-time-final-writeup]]
- [[pachinko-revisited-final-writeup]]

## 같이 보면 좋은 개념
- [[exploitation]]
- [[rce]]
- [[custom-cpu-reverse-engineering-ctf-patterns]]
