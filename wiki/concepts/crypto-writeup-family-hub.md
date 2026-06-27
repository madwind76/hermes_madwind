---
title: Crypto writeup family hub
created: 2026-06-20
updated: 2026-06-21
type: concept
tags: [ctf, crypto, cookies, cbc, prng, brute-force, reverse-engineering, session-forgery, token-forgery, survey, writeup]
sources: [https://github.com/HHousen/PicoCTF-2021/blob/master/Web%20Exploitation/More%20Cookies/README.md, https://github.com/apoirrier/CTFs-writeups/blob/master/PicoCTF/Web/MostCookies.md, https://raw.githubusercontent.com/snwau/picoCTF-2025-Writeup/main/Reverse%20Engineering/Chronohack/Chronohack.md, https://ctftime.org/writeup/33269]
confidence: medium
---

# Crypto writeup family hub

## 참고 URL
- [Original source](https://github.com/HHousen/PicoCTF-2021/blob/master/Web%20Exploitation/More%20Cookies/README.md)
- [Original source](https://github.com/apoirrier/CTFs-writeups/blob/master/PicoCTF/Web/MostCookies.md)
- [Raw source](https://raw.githubusercontent.com/snwau/picoCTF-2025-Writeup/main/Reverse%20Engineering/Chronohack/Chronohack.md)
- [CTFtime writeup](https://ctftime.org/writeup/33269)

## 1. 목적
이 페이지는 **쿠키/세션 조작, CBC bit flipping, 시간 기반 PRNG 토큰 재현**처럼 CTF에서 자주 반복되는 Crypto 계열 패턴을 묶는 상위 진입점입니다.

## 2. 이번 묶음
- [[cookie-tampering-writeup-survey]] → [[cookie-client-storage-ctf-patterns]], [[cbc-bit-flipping-ctf-patterns]], [[flask-signed-session-cookie-ctf-patterns]]
- [[prng-writeup-survey]] → [[prng-seed-bruteforce-ctf-patterns]], [[reverse-engineering-ctf-patterns]], [[substring-logic-bug-ctf-patterns]]
- [[crypto-primitive-writeup-survey]] → [[md5-collision-upload-integrity-bypass-ctf-patterns]], [[reverse-engineering-ctf-patterns]], [[cia]]
- [[picoctf-2021-crypto-family-hub]] → [[picoctf-2021-crypto-survey]], [[picoctf-2021-crypto-substitution-bundle]], [[picoctf-2021-crypto-rsa-bundle]], [[picoctf-2021-crypto-classical-bundle]], [[picoctf-2021-crypto-visual-collision-bundle]], [[picoctf-2021-mod-26-substitution]], [[picoctf-2021-new-caesar-substitution]], [[picoctf-2021-mind-your-ps-and-qs-rsa-factorization]], [[picoctf-2021-dachshund-attacks-rsa-wiener]], [[picoctf-2021-play-nice-playfair]], [[picoctf-2021-new-vignere-vigenere]], [[picoctf-2021-pixelated-visual-crypto]], [[picoctf-2021-it-is-my-birthday-2-sha1-collision]]
- [[picoctf-2022-crypto-family-hub]] → [[picoctf-2022-crypto-survey]], [[basic-mod1-final-writeup]], [[basic-mod2-final-writeup]], [[credstuff-final-writeup]], [[morse-code-final-writeup]], [[rail-fence-final-writeup]], [[substitution0-final-writeup]], [[substitution1-final-writeup]], [[substitution2-final-writeup]], [[transposition-trial-final-writeup]], [[vigenere-final-writeup]], [[very-smooth-final-writeup]], [[sequences-final-writeup]], [[sum-o-primes-final-writeup]], [[nsa-backdoor-final-writeup]]
- [[picoctf-2023-crypto-family-hub]] → [[picoctf-2023-crypto-survey]], [[hide-to-see-final-writeup]], [[read-my-cert-final-writeup]], [[rotation-final-writeup]]

- [[picoctf-2025-crypto-family-hub]] → [[picoctf-2025-crypto-survey]], [[picoctf-2025-crypto-number-theory-writeup]], [[picoctf-2025-crypto-cheese-writeup]], [[picoctf-2025-crypto-protocol-writeup]]

## 3. 왜 이 허브가 필요한가
- cookie 값은 상태와 권한을 담는 경우가 많아 **변조**와 **서명 위조**로 이어집니다.
- time-seeded PRNG는 **예측 가능한 출력** 때문에 brute force의 전형적인 대상입니다.
- Crypto 계열 문제는 단순 암호 해독이 아니라, **클라이언트 신뢰**, **무결성 부재**, **난수 예측 가능성**으로 자주 귀결됩니다.

## 4. 연결 개념
- [[cbc-bit-flipping-ctf-patterns]]
- [[cookie-client-storage-ctf-patterns]]
- [[flask-signed-session-cookie-ctf-patterns]]
- [[prng-seed-bruteforce-ctf-patterns]]
- [[reverse-engineering-ctf-patterns]]
- [[caesar-cipher-ctf-patterns]]
- [[md5-collision-upload-integrity-bypass-ctf-patterns]]
- [[picoctf-2025-crypto-family-hub]]

## 5. 다음 작업
- cookie / session / PRNG 계열 writeup이 더 모이면 survey를 세분화합니다.
- 새로운 leaf가 생기면 이 허브와 관련 survey에 함께 연결합니다.
- crypto 문제를 수집할 때는 암호 알고리즘보다 **출력 재현 가능성**과 **상태 위조 가능성**을 먼저 봅니다.
