---
title: format string 3 — picoCTF 2024 pwn writeup
created: 2026-06-15
updated: 2026-06-21
type: query
tags: [ctf, pwn, format-string, got-overwrite, libc-leak, picoctf]
sources: [https://blog.thecyberthesis.com/blog/writeups/picoCTF/pwn/format-string-3, https://hackmd.io/@Zzzzek/r14x13FRp, https://yun.ng/c/ctf/picoctf/pwn/format-string-3]
confidence: high
---

# format string 3 — picoCTF 2024 pwn writeup

> `format string 3`는 **libc leak 후 GOT overwrite로 `puts`를 `system`으로 바꾸는 문제**입니다.

## 참고 URL
- [blog.thecyberthesis.com](https://blog.thecyberthesis.com/blog/writeups/picoCTF/pwn/format-string-3)
- [hackmd.io](https://hackmd.io/@Zzzzek/r14x13FRp)
- [yun.ng](https://yun.ng/c/ctf/picoctf/pwn/format-string-3)


## 핵심 요약
- `hello()`가 `setvbuf` 주소를 출력해줍니다.
- 이를 통해 libc base를 계산합니다.
- format string으로 GOT의 `puts` 항목을 `system`으로 바꿉니다.

## 공격 흐름
1. 노출된 `setvbuf` 주소를 읽습니다.
2. libc base를 계산합니다.
3. `fmtstr_payload()` 등으로 `puts@GOT`를 `system`으로 덮습니다.
4. `puts("/bin/sh")`가 `system("/bin/sh")`로 바뀌어 셸이 열립니다.

## 학습 포인트
- GOT overwrite는 Partial RELRO에서 특히 유효합니다.
- libc leak과 format string write를 결합하는 전형적인 체인입니다.

## 방어 관점
- RELRO를 강화합니다.
- 포맷 문자열 취약점을 제거합니다.

## 재현 절차
1. GOT 또는 함수 포인터가 덮이는 위치를 확인합니다.
2. `puts` 같은 호출을 `system` 또는 목표 함수로 바꾸는 흐름을 재현합니다.
3. 필요한 주소 누출 후 덮기 성공 여부를 검증합니다.

```bash
# GOT overwrite 가능성을 확인하기 위해 바이너리를 실행합니다.
./format-string-3

# 심볼/주소를 확인할 때는 readelf/objdump를 활용합니다.
readelf -s ./format-string-3
```

## 관련 개념
- [[format-string-ctf-patterns]]
- [[pie-aslr-function-offset-ctf-patterns]]
