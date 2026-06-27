---
title: buffer overflow 2 — picoCTF 2022 pwn writeup
created: 2026-06-24
updated: 2026-06-24
type: query
tags: [ctf, picoctf, picoctf2022, pwn, buffer-overflow, rop]
sources: [https://picoctf2022.haydenhousen.com/binary-exploitation/buffer-overflow-2.md, https://github.com/HHousen/PicoCTF-2019/tree/master/Binary%20Exploitation/OverFlow%202]
confidence: medium
---

# buffer overflow 2 — picoCTF 2022 pwn writeup

## 참고 URL
- [HaydenHousen markdown](https://picoctf2022.haydenhousen.com/binary-exploitation/buffer-overflow-2.md)
- [PicoCTF 2019 OverFlow 2](https://github.com/HHousen/PicoCTF-2019/tree/master/Binary%20Exploitation/OverFlow%202)

## 핵심 요약
리턴 주소뿐 아니라 **인자까지 제어**해야 하는 버퍼 오버플로우 문제입니다.
공개 해설은 ROP를 사용해 원하는 함수와 인자를 배치하고, `pwntools`로 페이로드를 자동화합니다.

## 풀이 메모
1. 오프셋을 구한 뒤 저장된 리턴 주소를 원하는 함수로 바꿉니다.
2. 함수 인자가 필요한 경우 ROP 체인을 이어 붙여 인자 레지스터/스택 값을 맞춥니다.
3. 공개 해설처럼 `pwntools`를 쓰면 페이로드 구성과 원격 전송을 쉽게 재현할 수 있습니다.

## 같이 보면 좋은 페이지
- [[picoctf-2022-pwn-survey]]
- [[picoctf-2022-pwn-family-hub]]
- [[picoctf-2022-topic-map]]
