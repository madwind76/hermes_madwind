---
title: ChaCha Slide — picoCTF 2025 crypto writeup
created: 2026-06-22
updated: 2026-06-22
type: query
tags: [ctf, picoctf, crypto, writeup, encryption]
sources: [https://blog.malosdaf.me/posts/chacha20-poly1305-and-nonce-reuse-attack/, https://blog.yuma4869.com/ctf/writeup-for-picoctf-2025/, https://github.com/snwau/picoCTF-2025-Writeup]
confidence: medium
---

# ChaCha Slide — picoCTF 2025 crypto writeup

> 공개 writeup 제목과 참가자 프로필 기준으로 `ChaCha Slide`의 공개 해설을 모은 페이지입니다.

## 참고 URL
- [Malosdaf Blog](https://blog.malosdaf.me/posts/chacha20-poly1305-and-nonce-reuse-attack/)
- [Yuma note](https://blog.yuma4869.com/ctf/writeup-for-picoctf-2025/)
- [snwau/picoCTF-2025-Writeup](https://github.com/snwau/picoCTF-2025-Writeup)

## 1. 확인된 사실
- picoCTF 2025 Cryptography 섹션의 ChaCha 계열 문제입니다.
- 공개 글 제목에서 ChaCha20-Poly1305와 nonce reuse가 언급됩니다.
- 따라서 스트림/AEAD의 재사용 취약성을 보는 문제로 정리할 수 있습니다.

## 2. 공개 writeup 메모
- Malosdaf Blog는 nonce reuse 공격 관점을 다룹니다.
- Yuma note에도 같은 문제에 대한 언급이 있습니다.
- 이 페이지는 문제 이름과 공격 키워드를 함께 모아두는 역할입니다.

## 3. 관련 페이지
- [[picoctf-2025-crypto-family-hub]]
- [[picoctf-2025-crypto-survey]]
- [[crypto-primitive-writeup-survey]]
