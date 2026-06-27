---
title: RPS — picoCTF 2022 pwn writeup
created: 2026-06-24
updated: 2026-06-24
type: query
tags: [ctf, picoctf, picoctf2022, pwn, prng, automation]
sources: [https://raw.githubusercontent.com/Cajac/picoCTF-Writeups/main/picoCTF_2022/Binary_Exploitation/RPS.md, https://github.com/Cajac/picoCTF-Writeups/blob/main/picoCTF_2022/Binary_Exploitation/RPS.md]
confidence: medium
---

# RPS — picoCTF 2022 pwn writeup

## 참고 URL
- [Cajac raw writeup](https://raw.githubusercontent.com/Cajac/picoCTF-Writeups/main/picoCTF_2022/Binary_Exploitation/RPS.md)
- [Cajac blob writeup](https://github.com/Cajac/picoCTF-Writeups/blob/main/picoCTF_2022/Binary_Exploitation/RPS.md)

## 핵심 요약
게임은 `srand(time(0))`로 시드를 초기화하므로, 컴퓨터의 선택이 사실상 예측 가능합니다.
로컬 `libc`와 현재 시간을 맞춰 `rand()`를 미리 계산하고, 이기는 수를 자동으로 보내 5연승을 만들면 플래그가 출력됩니다.

## 풀이 메모
1. `time()`으로 시드가 고정되는 지점을 확인합니다.
2. `ctypes`나 로컬 `libc`로 `srand(int(time()))`와 `rand() % 3`을 동일하게 재현합니다.
3. 매 턴마다 상대의 수에 이기는 값을 자동 입력해 5연승을 만듭니다.

## 같이 보면 좋은 페이지
- [[picoctf-2022-pwn-survey]]
- [[picoctf-2022-pwn-family-hub]]
- [[picoctf-2022-topic-map]]
