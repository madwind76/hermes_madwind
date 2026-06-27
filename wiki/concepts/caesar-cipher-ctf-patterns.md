---
title: Caesar Cipher CTF Patterns
created: 2026-06-22
updated: 2026-06-22
type: concept
tags: [ctf, crypto, caesar, rotation, substitution, writeup]
sources: [https://picoctfsolutions.com/picoctf-2023-rotation, https://github.com/noamgariani11/PicoCTF-2023-Writeup/tree/main/Cryptography/rotation/rotation.md]
confidence: medium
---

# Caesar Cipher CTF Patterns

## 참고 URL
- [picoCTF 2023 rotation](https://picoctfsolutions.com/picoctf-2023-rotation)
- [README source](https://github.com/noamgariani11/PicoCTF-2023-Writeup/tree/main/Cryptography/rotation/rotation.md)

## 1. 정의
Caesar cipher는 알파벳을 일정 칸수만큼 회전시키는 고전적 치환 방식입니다.
CTF에서는 `ROT13`, `ROT18`, 단순 `shift N` 형태로 자주 등장합니다.

## 2. 왜 잘 풀리나
- 가능한 회전 수가 매우 적습니다.
- 출력이 사람 읽을 수 있는 문자열인지로 정답을 쉽게 판별할 수 있습니다.
- 문자열 패턴이 `picoCTF{...}` 같은 플래그 형식과 잘 맞습니다.

## 3. 실전 체크리스트
1. ROT13부터 먼저 시도합니다.
2. 결과가 이상하면 모든 rotation 값을 brute force로 돌립니다.
3. 숫자/기호가 보존되는지 확인하면서 후보를 좁힙니다.
4. 가장 자연스러운 평문을 선택합니다.

## 4. 연결된 페이지
- [[rotation-final-writeup]]
- [[picoctf-2023-crypto-family-hub]]
- [[crypto-writeup-family-hub]]
