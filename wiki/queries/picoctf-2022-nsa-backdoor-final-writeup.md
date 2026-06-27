---
title: NSA Backdoor — picoCTF 2022 crypto writeup
created: 2026-06-24
updated: 2026-06-24
type: query
tags: [ctf, picoctf, picoctf2022, crypto, backdoor]
sources: [https://picoctf2022.haydenhousen.com/cryptography/nsa-backdoor.md, https://eprint.iacr.org/2016/644.pdf, https://github.com/mimoo/Diffie-Hellman_Backdoor]
confidence: medium
---

# NSA Backdoor — picoCTF 2022 crypto writeup

## 참고 URL
- [HaydenHousen markdown](https://picoctf2022.haydenhousen.com/cryptography/nsa-backdoor.md)
- [How to Backdoor Diffie-Hellman](https://eprint.iacr.org/2016/644.pdf)
- [mimoo/Diffie-Hellman_Backdoor](https://github.com/mimoo/Diffie-Hellman_Backdoor)

## 핵심 요약
이 문제는 `Very Smooth`와 유사한 구조를 가지지만, 암호화 방식이 RSA가 아니라 **Diffie-Hellman 계열**로 바뀌어 있습니다.
공개 해설은 smooth한 합성 모듈러를 **Pollard p-1**로 분해한 뒤, David Wong의 backdoor 논문과 예제 코드를 따라 비밀을 복원합니다.

## 풀이 메모
1. `gen.py`의 수식이 RSA가 아니라 Diffie-Hellman 형태라는 점을 먼저 확인합니다.
2. smooth 소수 구조를 이용해 `n`을 인수분해합니다.
3. 논문과 공개 코드의 backdoor 절차를 따라 평문을 복원합니다.

## 같이 보면 좋은 페이지
- [[picoctf-2022-crypto-survey]]
- [[picoctf-2022-crypto-family-hub]]
- [[picoctf-2022-topic-map]]
