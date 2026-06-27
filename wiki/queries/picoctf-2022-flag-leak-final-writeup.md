---
title: flag leak — picoCTF 2022 pwn writeup
created: 2026-06-24
updated: 2026-06-24
type: query
tags: [ctf, picoctf, picoctf2022, pwn, format-string, stack-leak]
sources: [https://picoctf2022.haydenhousen.com/binary-exploitation/flag-leak.md, https://github.com/Dvd848/CTFs/blob/master/2019_picoCTF/stringzz.md]
confidence: medium
---

# flag leak — picoCTF 2022 pwn writeup

## 참고 URL
- [HaydenHousen markdown](https://picoctf2022.haydenhousen.com/binary-exploitation/flag-leak.md)
- [picoCTF 2019 stringzz](https://github.com/Dvd848/CTFs/blob/master/2019_picoCTF/stringzz.md)

## 핵심 요약
이 문제는 **format string** 계열로, 플래그 문자열 자체는 힙에 있지만 그 위치를 가리키는 포인터가 스택에 있습니다.
문자열 포인터를 찾아 `%s`로 출력하면 플래그를 읽을 수 있고, 첫 부분이 잘려 보일 때는 `CTF{` 기준으로 복원합니다.

## 풀이 메모
1. 출력 중 플래그 포인터가 스택의 몇 번째 인자인지 찾습니다.
2. `printf`의 직접 접근 문법으로 해당 위치를 `%n$s` 형태로 읽습니다.
3. 결과가 `picoCTF{...}`의 앞부분만 보이면 `pico`를 앞에 붙여 완성합니다.

## 같이 보면 좋은 페이지
- [[picoctf-2022-pwn-survey]]
- [[picoctf-2022-pwn-family-hub]]
- [[picoctf-2022-topic-map]]
