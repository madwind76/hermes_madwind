---
title: ropfu — picoCTF 2022 pwn writeup
created: 2026-06-24
updated: 2026-06-24
type: query
tags: [ctf, picoctf, picoctf2022, pwn, rop]
sources: [https://picoctf2022.haydenhousen.com/binary-exploitation/ropfu.md, https://github.com/Dvd848/CTFs/blob/master/2019_picoCTF/rop32.md]
confidence: medium
---

# ropfu — picoCTF 2022 pwn writeup

## 참고 URL
- [HaydenHousen markdown](https://picoctf2022.haydenhousen.com/binary-exploitation/ropfu.md)
- [picoCTF 2019 rop32](https://github.com/Dvd848/CTFs/blob/master/2019_picoCTF/rop32.md)

## 핵심 요약
이 문제는 이름 그대로 **ROP 체인**을 구성하는 연습 문제입니다.
공개 해설은 `ROPgadget`으로 가젯을 찾고, 바이트 제한을 고려해 체인을 구성한 뒤 플래그 함수를 호출합니다.

## 풀이 메모
1. `ROPgadget --binary ./vuln --rop --badbytes "0a"`로 사용 가능한 가젯을 확인합니다.
2. 필요 체인을 조립해 원하는 함수로 제어 흐름을 넘깁니다.
3. 공개 해설과 동일하게 자동화하면 원격 환경에서도 재현이 쉽습니다.

## 같이 보면 좋은 페이지
- [[picoctf-2022-pwn-survey]]
- [[picoctf-2022-pwn-family-hub]]
- [[picoctf-2022-topic-map]]
