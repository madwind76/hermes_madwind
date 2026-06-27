---
title: picoCTF 2025 crypto protocol writeup
created: 2026-06-22
updated: 2026-06-22
type: query
tags: [ctf, picoctf, crypto, writeup, reverse-engineering]
sources: [https://blog.malosdaf.me/posts/chacha20-poly1305-and-nonce-reuse-attack/, https://blog.yuma4869.com/ctf/writeup-for-picoctf-2025/, https://systemweakness.com/ricochet-picoctf-2025-mitm-replay-attack-bb47375fb7db]
confidence: medium
---

# picoCTF 2025 crypto protocol writeup

> 이 페이지는 `ChaCha Slide`와 `Ricochet`를 **프로토콜/상태 재사용 관점**으로 다시 묶은 노트입니다.

## 참고 URL
- [ChaCha Slide — Malosdaf Blog](https://blog.malosdaf.me/posts/chacha20-poly1305-and-nonce-reuse-attack/)
- [ChaCha Slide / Ricochet — Yuma note](https://blog.yuma4869.com/ctf/writeup-for-picoctf-2025/)
- [Ricochet — System Weakness](https://systemweakness.com/ricochet-picoctf-2025-mitm-replay-attack-bb47375fb7db)

## 1. 묶음 요약
| 문제 | 핵심 축 | 한 줄 메모 |
| --- | --- | --- |
| ChaCha Slide | nonce reuse / AEAD misuse | 같은 nonce 재사용은 스트림 보호를 무너뜨립니다. |
| Ricochet | MITM / replay / key exchange | 프로토콜 레벨 재사용과 위조 가능성을 봐야 합니다. |

## 2. 왜 같이 묶는가
1. 두 문제 모두 **암호 알고리즘 이름보다 프로토콜 사용 방식**이 핵심입니다.
2. `ChaCha Slide`는 nonce reuse, `Ricochet`는 replay/MITM 축으로 읽힙니다.
3. 같은 페이지에서 보면 **상태 재사용과 메시지 위조**라는 공통 패턴이 보입니다.

## 3. 개별 페이지
- [[picoctf-2025-chacha-slide-crypto-writeup]]
- [[picoctf-2025-ricochet-crypto-writeup]]

## 4. 연결 페이지
- [[picoctf-2025-crypto-family-hub]]
- [[picoctf-2025-crypto-survey]]
- [[crypto-writeup-family-hub]]
