---
title: stack cache — picoCTF 2022 pwn writeup
created: 2026-06-24
updated: 2026-06-24
type: query
tags: [ctf, picoctf, picoctf2022, pwn, buffer-overflow, memory-corruption]
sources: [https://picoctf2022.haydenhousen.com/binary-exploitation/stack-cache.md, https://github.com/HHousen/PicoCTF-2022/blob/master/Binary%20Exploitation/stack%20cache/script.py]
confidence: medium
---

# stack cache — picoCTF 2022 pwn writeup

## 참고 URL
- [HaydenHousen markdown](https://picoctf2022.haydenhousen.com/binary-exploitation/stack-cache.md)
- [script.py](https://github.com/HHousen/PicoCTF-2022/blob/master/Binary%20Exploitation/stack%20cache/script.py)

## 핵심 요약
이 문제는 **undefined behavior**와 버퍼 오버플로우를 함께 다루는 문제입니다.
공개 해설은 별도 `script.py`를 통해 취약 동작을 안정적으로 재현하고 플래그를 획득합니다.

## 풀이 메모
1. 소스와 입력 흐름을 살펴 취약한 상태 전이를 찾습니다.
2. 공개 `script.py`를 기준으로 취약 동작을 트리거합니다.
3. 실행 결과로 출력되는 플래그를 확인합니다.

## 같이 보면 좋은 페이지
- [[picoctf-2022-pwn-survey]]
- [[picoctf-2022-pwn-family-hub]]
- [[picoctf-2022-topic-map]]
