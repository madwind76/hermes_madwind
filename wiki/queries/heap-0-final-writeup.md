---
title: heap 0 — picoCTF 2024 pwn writeup
created: 2026-06-15
updated: 2026-06-15
type: query
tags: [ctf, pwn, heap-overflow, adjacency, safe_var, buffer-overflow, picoctf]
sources: [https://github.com/snwau/picoCTF-2024-Writeup/blob/main/Binary%20Exploitation/heap%200/heap%200.md, https://medium.com/@kenjikun/picoctf-binary-exploitation-2024-f5125b8874be, https://hackmd.io/@Zzzzek/r14x13FRp]
confidence: high
---

# heap 0 — picoCTF 2024 pwn writeup

> `heap 0`는 **힙에 인접하게 할당된 버퍼를 오버플로우해서 `safe_var`를 덮는 picoCTF 2024 pwn 문제**입니다. 핵심은 **heap overflow + adjacent heap chunk overwrite**입니다.

## 1. 핵심 요약

- 프로그램은 `input_data`와 `safe_var`를 힙에 각각 할당합니다.
- 두 영역은 매우 가깝게 배치되어 있어, `input_data`를 길게 쓰면 `safe_var`까지 덮을 수 있습니다.
- `safe_var`를 조건에 맞게 바꾸면 플래그가 출력됩니다.

## 2. 문제 구조

| 항목 | 내용 |
|------|------|
| 플랫폼 | picoCTF 2024 |
| 분류 | pwn / heap overflow |
| 핵심 요소 | heap allocation, adjacent overwrite, `safe_var` |
| 목표 | `safe_var`를 원하는 값으로 변경해 flag 출력 |
| 난이도 | 초급 |

## 3. 취약점 위치

```c
// 개념상 요약
char *input_data;
char *safe_var;

// input_data에 대한 입력이 길이 제한 없이 들어감
scanf("%s", input_data);
```

## 4. 공격 흐름

1. 메뉴에서 heap 상태를 확인해 두 할당의 주소 간격을 봅니다.
2. `input_data`에서 `safe_var`까지의 거리가 **32 bytes**임을 확인합니다.
3. 입력을 32바이트 이상 보내서 `safe_var`를 덮습니다.
4. 조건이 만족되면 `Print Flag` 메뉴를 선택해 flag를 얻습니다.

## 5. 실습 예시

```bash
# 32바이트를 채워 인접한 safe_var까지 도달합니다.
python3 - <<'PY'
print('2')          # Write to buffer
print('A' * 32)     # 32 bytes = boundary to safe_var
print('4')          # Print Flag
PY
```

## 6. 왜 가능한가

힙도 스택처럼 **인접한 메모리 영역이 서로 영향을 줍니다**. 길이 검사가 없는 입력 함수(`scanf("%s", ...)`)는 힙 버퍼를 넘어 다음 chunk의 데이터를 덮을 수 있습니다.

## 7. 방어 관점 메모

- `scanf("%s", ...)`처럼 길이 제한이 없는 입력을 피합니다.
- 힙에 중요한 검증 변수(`safe_var`)를 두지 않습니다.
- 입력 길이 검사를 항상 수행합니다.

## 8. 참고 자료

- [picoCTF-2024-Writeup/heap 0](https://github.com/snwau/picoCTF-2024-Writeup/blob/main/Binary%20Exploitation/heap%200/heap%200.md)
- [PICOCTF||Binary Exploitation|| 2024 - Medium](https://medium.com/@kenjikun/picoctf-binary-exploitation-2024-f5125b8874be)
- [picoCTF 2024 - Binary Exploitation Challenges - HackMD](https://hackmd.io/@Zzzzek/r14x13FRp)
- [[heap-overflow-adjacent-chunk-overwrite-ctf-patterns]]
