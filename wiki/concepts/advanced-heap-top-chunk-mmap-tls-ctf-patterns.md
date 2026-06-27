---
title: Advanced heap exploitation / top chunk / TLS hijack — CTF patterns
created: 2026-06-15
updated: 2026-06-21
type: concept
tags: [ctf, pwn, heap, top-chunk, mmap, tls, tcache, setcontext]
sources: [https://eth007.me/blog/posts/high-frequency-troubles/, https://hackmd.io/@Zzzzek/r14x13FRp]
confidence: medium
---

# Advanced heap exploitation / top chunk / TLS hijack — CTF patterns

> 이 패턴은 단순 heap overflow를 넘어, **allocator 메타데이터와 TLS/tcache 구조를 연쇄적으로 조작**해 libc leak과 셸 실행까지 이어지는 고급 heap 체인입니다.

## 참고 URL
- [eth007.me](https://eth007.me/blog/posts/high-frequency-troubles/)
- [hackmd.io](https://hackmd.io/@Zzzzek/r14x13FRp)

## 패턴
- top chunk 크기 훼손으로 비정상적인 allocator 동작을 유도합니다.
- unsorted bin 또는 mmap 재배치로 leak을 만듭니다.
- `tcache_perthread_struct` 같은 TLS 기반 포인터를 노립니다.
- 마지막에는 `setcontext` 계열이나 FSOP로 실행 흐름을 바꿉니다.

## 공격 흐름
1. heap leak을 먼저 만듭니다.
2. libc base를 계산합니다.
3. TLS/tcache 관련 포인터를 조작합니다.
4. `setcontext` 또는 유사 메커니즘으로 `system("/bin/sh")`를 실행합니다.

## 방어 포인트
- allocator 메타데이터 오염을 막기 위해 입력 길이와 chunk 수명을 엄격히 관리합니다.
- 중요한 포인터를 TLS/heap 근처에 두지 않습니다.
- 최신 libc 동작을 가정하지 말고, 취약성 제거를 우선합니다.

## 예시
- `high frequency troubles`
