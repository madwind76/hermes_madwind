---
title: Very Smooth — picoCTF 2022 crypto writeup
created: 2026-06-24
updated: 2026-06-24
type: query
tags: [ctf, picoctf, picoctf2022, crypto, rsa]
sources: [https://picoctf2022.haydenhousen.com/cryptography/very-smooth.md, https://github.com/HHousen/PicoCTF-2022/blob/master/Cryptography/Very%20Smooth/script.py]
confidence: medium
---

# Very Smooth — picoCTF 2022 crypto writeup

## 참고 URL
- [HaydenHousen markdown](https://picoctf2022.haydenhousen.com/cryptography/very-smooth.md)
- [script.py](https://github.com/HHousen/PicoCTF-2022/blob/master/Cryptography/Very%20Smooth/script.py)

## 핵심 요약
`gen.py`와 `output.txt`로부터 RSA 계열 암호문을 복원하는 문제입니다.
핵심은 **Pollard p-1**으로 매우 부드러운(smooth) 소수 구조를 분해하고, 그 결과로 얻은 인수들을 이용해 복호화하는 것입니다.

## 풀이 메모
1. 온라인 검색으로 Pollard p-1 알고리즘을 확인합니다.
2. `RsaCtfTool` 또는 공개 `script.py`를 변형해 충분히 많은 소수를 시도합니다.
3. `n`을 인수분해한 뒤 평문을 복호화해 플래그를 얻습니다.

## 같이 보면 좋은 페이지
- [[picoctf-2022-crypto-survey]]
- [[picoctf-2022-crypto-family-hub]]
- [[picoctf-2022-topic-map]]
