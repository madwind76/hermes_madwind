---
title: heap 3 — picoCTF 2024 pwn writeup
created: 2026-06-15
updated: 2026-06-15
type: query
tags: [ctf, pwn, use-after-free, tcache, heap, memory-corruption, picoctf]
sources: [https://github.com/snwau/picoCTF-2024-Writeup/blob/main/Binary%20Exploitation/heap%203/heap%203.md, https://qiita.com/colza_/items/cacc3999c02b6519ae91, https://yun.ng/c/ctf/picoctf/pwn/heap-3]
confidence: high
---

# heap 3 — picoCTF 2024 pwn writeup

> `heap 3`는 **use-after-free 기반 heap exploitation**으로 정리할 수 있습니다. freed chunk를 다시 할당받아, 남아 있는 데이터를 덮어 목적 문자열을 바꾸는 형태입니다.

## 핵심 요약
- 객체를 `free()`한 뒤에도 동일 chunk를 다시 얻을 수 있습니다.
- 같은 주소를 재사용하면 옛 데이터를 덮을 수 있습니다.
- 목표 문자열을 `pico`로 바꾸면 flag 분기로 이어집니다.

## 공격 흐름
1. 대상 객체를 해제합니다.
2. 동일 크기의 `malloc()`으로 같은 chunk를 재할당합니다.
3. 재할당된 메모리에 새 값을 써서 기존 문자열을 바꿉니다.
4. 검증 함수가 성공하면 flag를 출력합니다.

## 학습 포인트
- UAF는 할당/해제 순서를 잘못 관리할 때 생깁니다.
- tcache 재사용은 UAF를 쉽게 악용하게 만듭니다.

## 방어 관점
- free 후 포인터를 NULL로 만듭니다.
- 객체 수명과 권한 검증을 분리합니다.

## 재현 절차
1. 해제된 chunk 재사용 흐름과 tcache 상태를 확인합니다.
2. leak이 필요한지, 덮기만으로 되는지 구분합니다.
3. 재할당 주소가 원하는 값으로 바뀌는지 검증합니다.

```bash
# 힙 상태를 보기 위해 바이너리를 실행합니다.
./heap-3

# tcache 흐름을 확인하기 위해 gdb를 붙입니다.
gdb -q ./heap-3
```

## 관련 개념
- [[heap-overflow-adjacent-chunk-overwrite-ctf-patterns]]
