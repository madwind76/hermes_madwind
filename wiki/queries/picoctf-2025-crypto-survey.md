---
title: picoCTF 2025 crypto survey
created: 2026-06-20
updated: 2026-06-22
type: query
tags: [ctf, picoctf, crypto, rsa, md5, hash-collision, reverse-engineering, survey]
sources: [https://github.com/snwau/picoCTF-2025-Writeup, https://raw.githubusercontent.com/snwau/picoCTF-2025-Writeup/main/README.md]
confidence: medium
---

# picoCTF 2025 crypto survey

> 결론부터 말씀드리면, **picoCTF 2025에는 Crypto 문제가 있었습니다.**
> 공개 writeup 기준으로 README에 **Cryptography 섹션 6문제**가 보이며, 그중 일부는 solved, 일부는 unsolved 상태입니다.

## 참고 URL
- [snwau/picoCTF-2025-Writeup](https://github.com/snwau/picoCTF-2025-Writeup)
- [picoCTF 2025 README raw](https://raw.githubusercontent.com/snwau/picoCTF-2025-Writeup/main/README.md)

## 1. 확인 결과
| Challenge | 상태 | 점수 | 비고 |
| --- | --- | ---:| --- |
| hashcrack | Solved | 100 | writeup pending |
| EVEN RSA CAN BE BROKEN??? | Solved | 200 | RSA 계열 |
| Guess My Cheese (Part 1) | Solved | 200 | writeup pending |
| Guess My Cheese (Part 2) | Unsolved | 300 | writeup pending |
| ChaCha Slide | Unsolved | 400 | writeup pending |
| Ricochet | Unsolved | 500 | writeup pending |

## 2. 핵심 포인트
1. **RSA 계열 문제**가 최소 1개 확인됩니다.
2. **해시/무결성 계열** 문제명이 보입니다.
3. **대칭키/스트림 계열**로 보이는 `ChaCha Slide`가 포함되어 있습니다.
4. writeup 저장소가 아직 work in progress라서, 문제 목록은 확인되지만 세부 해법은 일부만 공개되어 있습니다.

## 3. 해석
이건 단순히 "Crypto 섹션이 있다" 수준이 아니라, **picoCTF 2025에 여러 개의 Crypto 문제군이 실제로 배치되었다**는 뜻입니다.

현재 공개 자료만으로 보면:
- `EVEN RSA CAN BE BROKEN???` → RSA 패턴 분석용
- `hashcrack` / `Guess My Cheese` → 해시 또는 인증/검증 계열 가능성
- `ChaCha Slide` → ChaCha 기반 암호 계열 가능성
- `Ricochet` → 아직 공개 writeup이 없어 추가 확인 필요

## 4. 다음 확인 포인트
- 각 문제의 공식 설명문
- solved writeup 유무
- 제가 위키에 개별 writeup으로 파일링할 가치가 있는지 여부

## 5. 공개 writeup 수집

| Challenge | 공개 writeup / 참고 | 메모 |
| --- | --- | --- |
| hashcrack | [InfoSec Write-ups](https://infosecwriteups.com/picoctf-challenges-hashcrack-09fddae4bb9b), [Medium](https://medium.com/@at.kishor.k/picoctf-2025-hashcrack-web-forensics-intro-8e829f9f5f35) | 해시 기반 인증/무결성 계열로 보이는 대표 writeup |
| EVEN RSA CAN BE BROKEN??? | [System Weakness](https://systemweakness.com/even-rsa-can-be-broken-picoctf-2025-9c294c77ca44), [Medium](https://medium.com/@at.kishor.k/picoctf-2025-writeup-even-rsa-can-be-broken-7cedd5d639df) | RSA 파라미터/난수 취약점 해설 |
| Guess My Cheese (Part 1) | [System Weakness](https://systemweakness.com/guess-my-cheese-part-1-picoctf-2025-affine-cipher-72df5b3a5f1e), [Medium](https://medium.com/@171k/picoctf-guess-my-cheese-part-1-de731da4389a) | Affine cipher 계열 writeup |
| Guess My Cheese (Part 2) | [System Weakness tag](https://systemweakness.com/tagged/guess-my-cheese), [YouTube](https://www.youtube.com/watch?v=PY8s2sOKgdg) | 공개 자료에서 Part 2 존재 확인 |
| ChaCha Slide | [Malosdaf Blog](https://blog.malosdaf.me/posts/chacha20-poly1305-and-nonce-reuse-attack/), [Yuma note](https://blog.yuma4869.com/ctf/writeup-for-picoctf-2025/) | ChaCha20-Poly1305 / nonce reuse 계열 |
| Ricochet | [System Weakness](https://systemweakness.com/ricochet-picoctf-2025-mitm-replay-attack-bb47375fb7db), [Yuma note](https://blog.yuma4869.com/ctf/writeup-for-picoctf-2025/) | MITM / replay / DH 계열 해설 |

## 6. 다시 묶은 페이지
- [[picoctf-2025-crypto-family-hub]]
- [[picoctf-2025-crypto-number-theory-writeup]]
- [[picoctf-2025-crypto-cheese-writeup]]
- [[picoctf-2025-crypto-protocol-writeup]]

## 7. 관련 페이지
- [[picoctf-2025-topic-map]]
- [[crypto-writeup-family-hub]]
- [[md5-collision-upload-integrity-bypass-ctf-patterns]]
- [[reverse-engineering-ctf-patterns]]
- [[cia]]
