---
title: x-sixty-what — picoCTF 2022 pwn writeup
created: 2026-06-24
updated: 2026-06-24
type: query
tags: [ctf, picoctf, picoctf2022, pwn, buffer-overflow, x64, ret2win]
sources: [https://picoctf2022.haydenhousen.com/binary-exploitation/x-sixty-what.md, https://github.com/Dvd848/CTFs/blob/master/2019_picoCTF/NewOverFlow-1.md]
confidence: medium
---

# x-sixty-what — picoCTF 2022 pwn writeup

## 참고 URL
- [HaydenHousen markdown](https://picoctf2022.haydenhousen.com/binary-exploitation/x-sixty-what.md)
- [picoCTF 2019 NewOverFlow-1](https://github.com/Dvd848/CTFs/blob/master/2019_picoCTF/NewOverFlow-1.md)

## 핵심 요약
64-bit 환경에서 버퍼를 덮어 **리턴 주소를 flag 함수로 바꾸는** 문제입니다.
다만 바로 flag로 가지 않고 `main`을 한 번 거쳐 돌아가야 하는 점이 핵심이며, 이 동작은 64-bit 호출 규약과 스택 상태 차이에서 비롯됩니다.

## 풀이 메모
1. 64-bit 오프셋을 맞춘 뒤 saved RIP를 제어합니다.
2. 먼저 `main`으로 돌아가도록 페이로드를 구성한 뒤, 다시 `flag`로 이동합니다.
3. 공개 해설처럼 두 단계 반환을 사용하면 안정적으로 플래그를 얻을 수 있습니다.

## 같이 보면 좋은 페이지
- [[picoctf-2022-pwn-survey]]
- [[picoctf-2022-pwn-family-hub]]
- [[picoctf-2022-topic-map]]
