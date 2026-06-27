---
title: credstuff — picoCTF 2022 crypto writeup
created: 2026-06-22
updated: 2026-06-22
type: query
tags: [ctf, picoctf, crypto, writeup]
sources: [https://github.com/noamgariani11/PicoCTF-2022-Writeup/blob/main/Cryptography/credstuff/credstuff.md]
confidence: medium
---

# credstuff — picoCTF 2022 crypto writeup

> 유출된 credential 목록에서 특정 사용자와 비밀번호를 매칭하는 문제입니다.

## 참고 URL
- [GitHub writeup](https://github.com/noamgariani11/PicoCTF-2022-Writeup/blob/main/Cryptography/credstuff/credstuff.md)

## 1. 핵심 요약
- usernames.txt와 passwords.txt의 순서를 1:1로 대응시킵니다.
- 대상 사용자 `cultiris`의 비밀번호를 찾습니다.
- 해당 비밀번호로 암호문을 복호화합니다.

## 2. 같이 보면 좋은 페이지
- [[picoctf-2022-crypto-survey]]
- [[picoctf-2022-crypto-family-hub]]
- [[crypto-writeup-family-hub]]
