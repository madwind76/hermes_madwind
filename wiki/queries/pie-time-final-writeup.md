---
title: PIE TIME — picoCTF 2025 pwn writeup
created: 2026-06-15
updated: 2026-06-21
type: query
tags: [ctf, pwn, binary-exploitation, pie, aslr, function-pointer, picoctf]
sources: [https://medium.com/@routbiswajit70681/picoctf-write-up-pie-time-37ffcdc29b71, https://systemweakness.com/pie-time-picoctf-2025-dbec42ba0857, https://github.com/snwau/picoCTF-2025-Writeup/blob/main/Binary%20Exploitation/PIE%20TIME/PIE%20TIME.md]
confidence: high
---

# PIE TIME — picoCTF 2025 pwn writeup

> `PIE TIME`은 **PIE(Position Independent Executable)로 인해 바뀌는 함수 주소를, `main()` 주소 누출과 고정 오프셋 계산으로 역산해서 `win()`으로 점프하는 picoCTF 2025 Binary Exploitation 문제**입니다. 핵심은 버퍼 오버플로가 아니라 **함수 포인터 점프와 ASLR/PIE 대응**입니다.

## 참고 URL
- [medium.com](https://medium.com/@routbiswajit70681/picoctf-write-up-pie-time-37ffcdc29b71)
- [systemweakness.com](https://systemweakness.com/pie-time-picoctf-2025-dbec42ba0857)
- [Original writeup](https://github.com/snwau/picoCTF-2025-Writeup/blob/main/Binary%20Exploitation/PIE%20TIME/PIE%20TIME.md)


## 1. 핵심 요약

- 프로그램이 `Address of main: %p`처럼 **실행 중인 `main()` 주소를 출력**합니다.
- 사용자가 입력한 16진수 값을 함수 포인터로 캐스팅해 바로 호출합니다.
- PIE 때문에 `win()`의 절대 주소는 매 실행마다 바뀌지만, **`main()`과 `win()`의 상대 오프셋은 고정**됩니다.
- 따라서 `win = leaked_main - 0x96` 형태로 계산해 입력하면 됩니다.

## 2. 문제 구조

| 항목 | 내용 |
|------|------|
| 플랫폼 | picoCTF 2025 |
| 분류 | pwn / binary exploitation |
| 핵심 요소 | PIE, ASLR, function pointer hijack, info leak |
| 입력 | 16진수 주소 |
| 목표 | `win()`으로 제어 흐름 이동 |

## 3. 공격 흐름

1. 원격 실행 시 출력되는 `main()` 주소를 확인합니다.
2. 로컬 `readelf` 또는 `gdb`로 `main`과 `win`의 심볼 오프셋을 확인합니다.
3. 두 함수의 차이값이 `0x96`임을 계산합니다.
4. `leaked_main - 0x96` 값을 입력해 `win()`으로 점프합니다.
5. `You won!`와 flag를 확인합니다.

## 4. 실전 계산 예시

예를 들어 프로그램이 다음처럼 출력했다고 가정합니다.

```text
Address of main: 0x5660322e333d
Enter the address to jump to, ex => 0x12345:
```

오프셋이 `0x96`이므로:

```text
0x5660322e333d - 0x96 = 0x5660322e32a7
```

이 값을 입력하면 `win()`으로 분기합니다.

## 5. 로컬에서 확인하는 방법

```bash
# readelf로 main/win 심볼 오프셋을 확인합니다.
readelf -s ./vuln | egrep "main|win"  # 예상 출력: win=0x12a7, main=0x133d
```

```python
# main과 win의 상대 오프셋을 계산합니다.
main = int('0x133d', 16)
win = int('0x12a7', 16)
print(hex(main - win))  # 예상 출력: 0x96
```

## 6. 방어 관점 메모

- PIE/ASLR 자체는 **절대 주소 의존 공격**을 어렵게 만듭니다.
- 하지만 프로그램이 **정보 누출(info leak)** 을 제공하면, 고정 오프셋 계산으로 우회될 수 있습니다.
- 따라서 실제 서비스에서는 불필요한 주소 출력 금지, 디버그 로그 제거, 함수 포인터 입력 검증이 중요합니다.

## 7. 비교 포인트

- `PIE TIME`은 **주소 계산형 pwn**입니다.
- `Pachinko Revisited`처럼 실행 모델 자체를 역추적하는 문제와는 다릅니다.
- `win()` 호출 주소를 찾는 데는 취약점 체인보다 **컴파일/링크 레이아웃 이해**가 더 중요합니다.

## 재현 절차
1. `main()` 주소 출력과 함수 포인터 입력 흐름을 확인합니다.
2. 로컬 심볼 오프셋으로 `main()`과 `win()` 차이를 계산합니다.
3. 누출된 주소에서 오프셋을 빼서 `win()`으로 점프합니다.

```bash
# 바이너리를 실행해 main 주소 출력과 입력 프롬프트를 확인합니다.
./pie-time

# 정적 분석으로 main/win 심볼과 오프셋을 봅니다.
readelf -s ./pie-time | grep -E ' main$| win$'
```

## 8. 참고 자료

- [Biswajit Rout — PicoCTF Write-up: PIE TIME](https://medium.com/@routbiswajit70681/picoctf-write-up-pie-time-37ffcdc29b71)
- [System Weakness — PIE TIME — picoCTF 2025](https://systemweakness.com/pie-time-picoctf-2025-dbec42ba0857)
- [snwau/picoCTF-2025-Writeup — PIE TIME](https://github.com/snwau/picoCTF-2025-Writeup/blob/main/Binary%20Exploitation/PIE%20TIME/PIE%20TIME.md)
- [[pie-aslr-function-offset-ctf-patterns]]
- [[exploitation]]
