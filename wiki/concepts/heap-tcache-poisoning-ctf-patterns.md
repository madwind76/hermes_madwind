---
title: Heap tcache poisoning — CTF patterns
created: 2026-06-15
updated: 2026-06-21
type: concept
sources: [queries/horsetrack-final-writeup.md]
confidence: medium
tags: [ctf, pwn, heap, tcache-poisoning, uaf]
---

# Heap tcache poisoning — CTF patterns

> 해제된 chunk가 다시 할당되는 흐름을 이용해 tcache freelist를 오염시키는 패턴입니다.

## 참고 URL
- [Reference](queries/horsetrack-final-writeup.md)

## 핵심 아이디어
- freed chunk의 next 포인터를 덮습니다.
- 다음 malloc이 공격자가 원하는 주소를 반환하도록 만듭니다.
- UAF, double-free, heap leak과 자주 결합됩니다.

## 자주 보이는 형태
- 동일 크기 chunk 반복 할당/해제
- freed chunk 내부 포인터 오염
- 함수 포인터, GOT, hook, vtable 쪽으로 유도
- libc base leak 후 후속 overwrite

## picoCTF 예시
- [[horsetrack-final-writeup]]

## 방어
- UAF와 double-free를 제거합니다.
- 해제 후 포인터를 즉시 무효화합니다.
- 최신 glibc 보호와 safe-linking을 유지합니다.
