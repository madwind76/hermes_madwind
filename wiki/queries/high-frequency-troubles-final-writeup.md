---
title: high frequency troubles — picoCTF 2024 pwn writeup
created: 2026-06-15
updated: 2026-06-15
type: query
tags: [ctf, pwn, heap, top-chunk, mmap, tls, tcache, setcontext, picoctf]
sources: [https://eth007.me/blog/posts/high-frequency-troubles/, https://hackmd.io/@Zzzzek/r14x13FRp, https://github.com/snwau/picoCTF-2024-Writeup]
confidence: medium
---

# high frequency troubles — picoCTF 2024 pwn writeup

> `high frequency troubles`는 picoCTF 2024에서 가장 어려운 축에 속하는 **고급 heap exploitation** 문제입니다. 공개 writeup 기준으로는 **top chunk corruption → leak → TLS/tcache hijack → setcontext32** 체인이 핵심입니다.

## 핵심 요약
- 정상적인 `free()` 경로가 없거나 제한적입니다.
- top chunk 크기를 망가뜨려 unsorted bin/leak 상황을 만듭니다.
- mmap/TLS 쪽을 건드려 `tcache_perthread_struct` 포인터를 탈취합니다.
- 마지막에는 `setcontext32`를 이용해 `system("/bin/sh")`로 이어집니다.

## 공격 흐름
1. top chunk 관련 메타데이터를 훼손해 heap leak을 얻습니다.
2. mmap chunk 오버플로우로 TLS/스레드 로컬 구조를 노립니다.
3. libc leak을 만든 뒤 tcache 관련 포인터를 조작합니다.
4. ROP 없이 `setcontext32`를 활용해 셸을 획득합니다.

## 학습 포인트
- 고급 heap 문제는 단일 primitive가 아니라 **연쇄 primitive**로 풀립니다.
- heap leak, libc leak, 구조체 포인터 조작이 결합됩니다.

## 방어 관점
- 최신 allocator 보호를 우회하는 패턴이므로, 입력 길이와 chunk 수명 관리가 중요합니다.
- 힙 메타데이터와 중요한 포인터를 가까이 두지 않습니다.

## 재현 절차
1. heap leak과 libc leak이 각각 어디서 나오는지 확인합니다.
2. top chunk / mmap / TLS 관련 구조를 추적합니다.
3. 후반부 제어 흐름을 `setcontext` 계열로 재현합니다.

```bash
# 고급 heap 흐름을 보기 위해 바이너리를 실행합니다.
./high-frequency-troubles

# 메모리 구조를 추적할 때 디버깅 세션을 사용합니다.
gdb -q ./high-frequency-troubles
```

## 관련 개념
- [[advanced-heap-top-chunk-mmap-tls-ctf-patterns]]
