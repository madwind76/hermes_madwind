---
title: ret2reg / executable stack — CTF patterns
created: 2026-06-15
updated: 2026-06-15
type: concept
tags: [ctf, pwn, ret2reg, shellcode, executable-stack, stack-overflow, register-control]
sources: [https://www.ztz0.com/writeups/2025/picoctf/pwn/handoff/, https://recaptcha.team/picoCTF-2025/pwn/Handoff/, https://medium.com/@z.ishan_Ansari/handoff-f6ec74face4d]
confidence: high
---

# ret2reg / executable stack — CTF patterns

## Step 1. 단어 풀이
- **ret2reg**: return 주소를 덮어 특정 **레지스터를 대상으로 하는 점프 가젯**으로 제어를 넘기는 기법입니다.
- **Executable stack**: 스택 메모리에서 실행 권한이 켜져 있어, 그 위에 올린 shellcode를 바로 실행할 수 있는 상태입니다.
- **Shellcode**: 시스템 콜을 직접 호출해 쉘 획득 같은 목적을 달성하는 짧은 기계어 코드입니다.

## 한 문장 정의
이 패턴은 **오버플로로 제어 흐름을 가젯(`jmp rax`, `jmp rsp` 등)으로 돌린 뒤, 실행 가능한 스택/버퍼에 올려둔 shellcode를 실행하는 문제 유형**입니다.

## 핵심 흐름
```text
buffer overflow -> control RIP -> jmp <register> gadget -> register points to attacker-controlled buffer -> shellcode execution
```

## 전문 설명
이 유형은 다음 조건이 겹칠 때 자주 나타납니다.

1. `RAX`, `RSP`, `RDI` 같은 레지스터가 공격자 입력 주소를 가리킵니다.
2. 바이너리에서 `jmp reg`, `call reg`, `push reg; ret` 같은 가젯을 찾을 수 있습니다.
3. NX가 꺼져 있거나 스택이 RWX로 설정되어 있습니다.
4. PIE가 없거나, 주소를 쉽게 계산할 수 있습니다.

## 공격자 관점
- 먼저 `checksec`로 NX/PIE/canary 상태를 확인합니다.
- `gdb`로 크래시 시 어떤 레지스터가 입력을 가리키는지 봅니다.
- `ROPgadget`, `ropper`, `objdump`로 `jmp rax`나 `jmp rsp`를 찾습니다.
- shellcode는 짧고 안정적인 것을 쓰고, 필요하면 NOP sled를 붙입니다.
- 입력 도중 널 바이트가 끼는지 확인합니다.

## 방어자 관점
- NX 활성화가 가장 중요합니다.
- 스택 실행 권한을 제거하고, PIE와 canary를 함께 켭니다.
- 입력 제한과 인덱스 검증을 철저히 해야 합니다.
- 레지스터에 사용자 입력 주소가 오래 남지 않도록 설계합니다.

## 관련 writeup
- [[handoff-final-writeup]]

## 같이 보면 좋은 개념
- [[exploitation]]
- [[rce]]
- [[pie-aslr-function-offset-ctf-patterns]]
