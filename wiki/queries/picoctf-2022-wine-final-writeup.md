---
title: wine — picoCTF 2022 pwn writeup
created: 2026-06-24
updated: 2026-06-24
type: query
tags: [ctf, picoctf, picoctf2022, pwn, buffer-overflow, windows, x86]
sources: [https://raw.githubusercontent.com/CavemanJay/PicoCTF/master/2022/binary_exploitation/wine/README.md, https://github.com/CavemanJay/PicoCTF/blob/master/2022/binary_exploitation/wine/README.md]
confidence: medium
---

# wine — picoCTF 2022 pwn writeup

## 참고 URL
- [CavemanJay README](https://raw.githubusercontent.com/CavemanJay/PicoCTF/master/2022/binary_exploitation/wine/README.md)
- [GitHub blob](https://github.com/CavemanJay/PicoCTF/blob/master/2022/binary_exploitation/wine/README.md)

## 핵심 요약
Windows용 실행 파일을 `wine`으로 돌리면서 EIP를 제어하는 버퍼 오버플로우 문제입니다.
공개 풀이에서는 `win()` 주소를 먼저 알아내고, `cyclic` 패턴으로 오프셋을 찾은 뒤 그 주소를 리턴 주소에 넣어 플래그를 얻습니다.

## 풀이 메모
1. 수정된 소스에서 `win()` 함수 주소를 출력하게 만들어 위치를 확인합니다.
2. `wine`에서 크래시를 유도하고 `cyclic`으로 EIP 오프셋을 찾습니다.
3. 오프셋 뒤에 `win()` 주소를 붙여 원격에 전송합니다.

## 같이 보면 좋은 페이지
- [[picoctf-2022-pwn-survey]]
- [[picoctf-2022-pwn-family-hub]]
- [[picoctf-2022-topic-map]]
