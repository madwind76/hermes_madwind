---
title: heap 2 — picoCTF 2024 pwn writeup
created: 2026-06-15
updated: 2026-06-21
type: query
tags: [ctf, pwn, heap-overflow, function-pointer, endianness, picoctf]
sources: [https://github.com/snwau/picoCTF-2024-Writeup/blob/main/Binary%20Explotation/heap-2.md, https://qiita.com/colza_/items/8ce95eb48a45f28be3e1, https://yun.ng/c/ctf/picoctf/pwn/heap-2]
confidence: high
---

# heap 2 — picoCTF 2024 pwn writeup

> `heap 2`는 **heap overflow로 함수 포인터를 덮어서 `win()`을 호출하는 문제**입니다.

## 참고 URL
- [Original writeup](https://github.com/snwau/picoCTF-2024-Writeup/blob/main/Binary%20Explotation/heap-2.md)
- [qiita.com](https://qiita.com/colza_/items/8ce95eb48a45f28be3e1)
- [yun.ng](https://yun.ng/c/ctf/picoctf/pwn/heap-2)


## 핵심 요약
- `safe_var`가 함수 포인터처럼 사용됩니다.
- `win()` 주소를 little-endian으로 써야 합니다.
- `p64()`를 쓰면 안전합니다.

## 공격 흐름
1. GDB 등으로 `win()` 주소를 확인합니다.
2. 32바이트의 더미 데이터를 채웁니다.
3. `p64(win)`을 뒤에 붙여 함수 포인터를 덮습니다.
4. 프로그램이 `win()`을 호출하면서 flag를 얻습니다.

## 학습 포인트
- 함수 포인터 overwrite는 제어 흐름 탈취의 기본 패턴입니다.
- endian/packing 실수가 자주 발생합니다.

## 방어 관점
- 중요한 포인터를 사용자 버퍼 근처에 두지 않습니다.
- heap metadata와 function pointer를 함께 관리할 때는 보호가 필요합니다.

## 재현 절차
1. 어떤 함수 포인터 또는 제어 데이터가 힙 위에 있는지 확인합니다.
2. 오염 가능한 chunk를 찾습니다.
3. 목표 포인터가 바뀌는지 검증합니다.

```bash
# 함수 포인터 재배치 여부를 확인하기 위해 바이너리를 실행합니다.
./heap-2

# 힙 오염이 발생하는 시점을 디버깅합니다.
gdb -q ./heap-2
```

## 관련 개념
- [[function-pointer-overwrite-ctf-patterns]]
- [[heap-overflow-adjacent-chunk-overwrite-ctf-patterns]]
