---
title: Handoff — picoCTF 2025 pwn writeup
created: 2026-06-23
updated: 2026-06-23
type: query
tags: [ctf, picoctf, pwn, binary-exploitation, buffer-overflow, heap]
sources: [https://github.com/asatpathy314/picoctf-2025/tree/main/pwn/handoff]
confidence: medium
---

# Handoff — picoCTF 2025 pwn writeup

> 메뉴 기반 바이너리로, recipient name(8 bytes)과 message(64 bytes)를 저장하는 구조체 배열을 조작해 feedback 버퍼 오버플로우를 트리거하는 문제입니다. `feedback[8]` 버퍼가 `entries[10]` 배열과 인접해 있어 entries 조작으로 return address까지 덮어쓸 수 있습니다.

## 참고 URL
- [asatpathy314/picoctf-2025 — handoff](https://github.com/asatpathy314/picoctf-2025/tree/main/pwn/handoff)

## 1. 문제 구조

| 항목 | 내용 |
|------|------|
| 플랫폼 | picoCTF 2025 |
| 분류 | pwn / binary exploitation |
| 핵심 요소 | Stack/heap buffer overflow, struct array manipulation |
| 난이도 | Medium (300pts) |

### Source (handoff.c)
```c
typedef struct entry {
    char name[8];    // 8 bytes
    char msg[64];    // 64 bytes
} entry_t;

int vuln() {
    char feedback[8];      // ← 8 bytes
    entry_t entries[10];   // ← struct array
    int total_entries = 0;

    while (true) {
        // Option 1: Add recipient → entries[total_entries].name (NAME_LEN=32 bytes read)
        // Option 2: Send message → entries[choice].msg (MSG_LEN=64 bytes read)
        // Option 3: Exit → feedback (NAME_LEN=32 bytes read) ← overflow!
    }
}
```

### 취약점
1. **entries[].name**은 8 bytes지만 `fgets(..., NAME_LEN(32), ...)`로 **32 bytes를 읽음**
2. **feedback[8]**은 스택에서 entries 배열과 인접
3. Option 3에서 `fgets(feedback, NAME_LEN(32), stdin)` → feedback(8)을 넘어 return address까지 overwrite 가능

## 2. 공격 흐름

### Step 1: Name overflow로 msg 영역 침범
Option 1에서 name에 8 bytes 이상 입력하면 name 버퍼를 넘어 msg 영역을 침범합니다.

```text
What's the new recipient's name: AAAAAAAAAAAAAAAABBBBBBBB
→ name(8) + msg overflow
```

### Step 2: Msg overflow → stack 변수 침범
Option 2에서 entries[choice].msg에 입력 시 인접 stack 변수 overwrite

### Step 3: Feedback overflow → return address 조작
Option 3에서 `fgets(feedback, 32, stdin)`로 feedback[8]을 넘어 32 bytes를 쓰면 return address까지 도달합니다.

```text
feedback[8] + padding + return_address → win() or print_flag()
```

## Flag
`picoCTF{...}` (인스턴스별 상이)

## 3. 핵심 패턴
1. **구조체 배열 + 스택 버퍼** 조합에서 발생하는 overflow
2. `name`과 `feedback`의 **버퍼 크기보다 큰 read 크기**가 취약점의 근본 원인
3. Option 3가 feedback을 읽을 때까지 entries 조작으로 경로 확보

## 4. 연결 개념
- [[buffer-overflow-ctf-patterns]]
- [[heap-overflow-adjacent-chunk-overwrite-ctf-patterns]]
- [[exploitation]]