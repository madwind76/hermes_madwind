---
title: buffer overflow 1 — picoCTF 2022 pwn writeup
created: 2026-06-24
updated: 2026-06-24
type: query
tags: [ctf, picoctf, picoctf2022, pwn, buffer-overflow, ret2win]
sources: [https://picoctf2022.haydenhousen.com/binary-exploitation/buffer-overflow-1.md, https://github.com/HHousen/PicoCTF-2022/blob/master/Binary%20Exploitation/buffer%20overflow%201/script.py]
confidence: medium
---

# buffer overflow 1 — picoCTF 2022 pwn writeup

## 참고 URL
- [HaydenHousen markdown](https://picoctf2022.haydenhousen.com/binary-exploitation/buffer-overflow-1.md)
- [script.py](https://github.com/HHousen/PicoCTF-2022/blob/master/Binary%20Exploitation/buffer%20overflow%201/script.py)

## 핵심 요약
`vuln()`의 반환 주소를 덮어 `win()`으로 점프하는 가장 기본적인 ret2win 문제입니다.
버퍼 오프셋만 정확히 찾으면, 추가적인 ROP 체인 없이도 플래그 함수를 직접 호출할 수 있습니다.

## 풀이 메모
1. 입력이 리턴 주소까지 도달하는 오프셋을 확인합니다.
2. `vuln`의 저장된 리턴 주소를 `win` 함수 주소로 교체합니다.
3. 공개 `script.py`를 기준으로 페이로드를 자동화하면 재현이 쉽습니다.

## 같이 보면 좋은 페이지
- [[picoctf-2022-pwn-survey]]
- [[picoctf-2022-pwn-family-hub]]
- [[picoctf-2022-topic-map]]
