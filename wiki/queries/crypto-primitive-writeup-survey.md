---
title: Crypto primitive writeup survey
created: 2026-06-20
updated: 2026-06-20
type: query
tags: [ctf, crypto, rsa, xor, md5, hash-collision, brute-force, reverse-engineering, survey, writeup]
sources: [https://ctftime.org/writeup/40345, https://ctftime.org/writeup/24962, https://ctftime.org/writeup/25360, https://github.com/utisss/foreverctf-writeups/blob/master/reversing-xor.md, https://github.com/valecor95/Crypto_CTF_writeups/blob/master/AffinityCTF2020/Collisions_Course/collisions_course.md, https://github.com/TalaatHarb/ctf-writeups/tree/main/asisctf2020/babymd5]
confidence: high
---

# Crypto primitive writeup survey

> 목적: **RSA, MD5 collision, XOR decoding처럼 문제의 핵심이 암호/해시/변조에 걸쳐 있는 writeup**을 비교합니다.
> 핵심 질문: “암호 알고리즘 자체보다, 약한 파라미터·충돌 가능성·고정 키가 더 중요했는가?”

## 참고 URL
- [Lowkey RSA — CTFtime writeup](https://ctftime.org/writeup/40345)
- [Collision Course — CTFtime writeup](https://ctftime.org/writeup/24962)
- [Collision Course — original writeup](https://github.com/valecor95/Crypto_CTF_writeups/blob/master/AffinityCTF2020/Collisions_Course/collisions_course.md)
- [Baby MD5 — CTFtime writeup](https://ctftime.org/writeup/25360)
- [Baby MD5 — original writeup](https://github.com/TalaatHarb/ctf-writeups/tree/main/asisctf2020/babymd5)
- [reversing-xor — original writeup](https://github.com/utisss/foreverctf-writeups/blob/master/reversing-xor.md)

## 비교 대상

| Source | Primitive | What changed | Takeaway |
| --- | --- | --- | --- |
| `Lowkey RSA` | non-standard RSA + small secret parameter | continued fraction / approximation attack | RSA는 수식이 조금만 비정상적이어도 수론 공격으로 무너집니다. |
| `Collision Course` | MD5 collision + upload integrity bypass | two different files with same hash | 해시 하나만 믿는 업로드 검증은 충돌에 취약합니다. |
| `Baby MD5` | partial hash collision + repeated hashing | brute-force of short hash targets | 부분 충돌과 반복 해시는 상태 재사용 공격을 허용할 수 있습니다. |
| `It is my Birthday` | MD5 collision + integrity bypass | same-hash file upload | 해시 검증이 곧 무결성은 아닙니다. |
| `reversing-xor` | fixed XOR key decoding | whole-file XOR with static key | 고정 키 XOR는 복호화가 아니라 단순한 가림막에 가깝습니다. |

## 공통 패턴

1. **문제의 핵심은 암호 알고리즘이 아니라 설계 실수**인 경우가 많습니다.
2. RSA는 비정상 파라미터, 해시는 충돌, XOR는 고정 키에서 무너집니다.
3. 공격자는 보통 전체를 깨기보다 **약한 부분 하나**를 찾아서 우회합니다.
4. 자동화는 brute force보다 **후보 수를 줄이는 모델링**에 더 중요합니다.

## writeup별 메모

### 1) Lowkey RSA
- 비표준 totient와 작은 비밀값이 핵심입니다.
- continued fraction과 근사로 `p`, `q`를 복원합니다.
- 연습 포인트: 파라미터 관계식 정리, 근사식 선택, 후보 검증

### 2) Collision Course
- MD5 collision을 업로드 검증 우회에 사용합니다.
- 연습 포인트: 블록 단위 구성, 요구 문자열 삽입, collision generator 사용

### 3) Baby MD5
- 부분 충돌과 반복 해시 조건이 섞여 있습니다.
- 연습 포인트: PoW brute force, prefix 조건, 반복 상태 재사용

### 4) It is my Birthday
- 파일 업로드 무결성을 MD5 collision으로 깨는 고전적 문제입니다.
- 연습 포인트: 동일 해시가 동일 파일을 뜻하지 않는다는 점 확인

### 5) reversing-xor
- 고정 XOR 키를 찾아 바이너리를 되돌립니다.
- 연습 포인트: 고정 상수 탐지, 전체 바이트열 일괄 복호화, strings 확인

## 관련 개념

- [[crypto-writeup-family-hub]]
- [[md5-collision-upload-integrity-bypass-ctf-patterns]]
- [[reverse-engineering-ctf-patterns]]
- [[cia]]
- [[it-is-my-birthday-final-writeup]]

## 다음 읽을 거리

- [[lowkey-rsa-final-writeup]]
- [[collision-course-final-writeup]]
- [[baby-md5-final-writeup]]
- [[reversing-xor-final-writeup]]
- [[it-is-my-birthday-final-writeup]]
