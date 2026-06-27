---
title: picoCTF 2025 crypto number theory writeup
created: 2026-06-22
updated: 2026-06-22
type: query
tags: [ctf, picoctf, crypto, rsa, hash-collision, writeup]
sources: [https://infosecwriteups.com/picoctf-challenges-hashcrack-09fddae4bb9b, https://medium.com/@at.kishor.k/picoctf-2025-hashcrack-web-forensics-intro-8e829f9f5f35, https://systemweakness.com/even-rsa-can-be-broken-picoctf-2025-9c294c77ca44, https://medium.com/@at.kishor.k/picoctf-2025-writeup-even-rsa-can-be-broken-7cedd5d639df]
confidence: medium
---

# picoCTF 2025 crypto number theory writeup

> 이 페이지는 `hashcrack`과 `EVEN RSA CAN BE BROKEN???`를 **한 묶음**으로 다시 정리한 상위 노트입니다.
> 둘 다 겉모습은 다르지만, 결국 **약한 검증/파라미터/수학적 구조**가 핵심이었습니다.

## 참고 URL
- [hashcrack — InfoSec Write-ups](https://infosecwriteups.com/picoctf-challenges-hashcrack-09fddae4bb9b)
- [hashcrack — Medium](https://medium.com/@at.kishor.k/picoctf-2025-hashcrack-web-forensics-intro-8e829f9f5f35)
- [EVEN RSA CAN BE BROKEN??? — System Weakness](https://systemweakness.com/even-rsa-can-be-broken-picoctf-2025-9c294c77ca44)
- [EVEN RSA CAN BE BROKEN??? — Medium](https://medium.com/@at.kishor.k/picoctf-2025-writeup-even-rsa-can-be-broken-7cedd5d639df)

## 1. 묶음 요약
| 문제 | 핵심 축 | 한 줄 메모 |
| --- | --- | --- |
| hashcrack | 해시 검증 / 무결성 | 해시를 검증 근거로만 믿으면 우회 여지가 생깁니다. |
| EVEN RSA CAN BE BROKEN??? | RSA 파라미터 / 수학적 취약점 | RSA는 구현·파라미터가 흔들리면 빠르게 무너집니다. |

## 2. 왜 같이 묶는가
1. 두 문제 모두 **암호 자체보다 설계 가정**이 더 중요합니다.
2. `hashcrack`은 해시 검증의 허점을, `EVEN RSA CAN BE BROKEN???`은 RSA 설계의 약점을 봅니다.
3. 둘 다 수학적 구조를 읽어야 해서 **number-theory / integrity weakness** 축으로 함께 보는 것이 더 빠릅니다.

## 3. 개별 페이지
- [[picoctf-2025-hashcrack-crypto-writeup]]
- [[picoctf-2025-even-rsa-can-be-broken-crypto-writeup]]

## 4. 연결 페이지
- [[picoctf-2025-crypto-family-hub]]
- [[picoctf-2025-crypto-survey]]
- [[crypto-primitive-writeup-survey]]
