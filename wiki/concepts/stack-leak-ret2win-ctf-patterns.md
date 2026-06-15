---
title: Stack leak / ret2win — CTF patterns
created: 2026-06-15
updated: 2026-06-15
type: concept
tags: [ctf, pwn, stack-leak, ret2win, buffer-overflow, rop, aslr]
sources: [https://picoctf2022.haydenhousen.com/binary-exploitation/stack-cache, https://github.com/HHousen/PicoCTF-2022/blob/master/Binary%20Exploitation/stack%20cache/script.py]
confidence: high
---

# Stack leak / ret2win — CTF patterns

## Step 1. 단어 풀이
- **Stack leak**: 스택 주소를 외부로 노출하는 취약점입니다.
- **ret2win**: 리턴 주소를 덮어서 숨겨진 `win()` 함수로 보내는 기법입니다.
- **ROP padding**: 스택 정렬이나 오프셋 오차를 보완하기 위해 가젯을 여러 번 배치하는 방법입니다.

## 한 문장 정의
이 패턴은 **취약점으로 먼저 스택 위치를 알아낸 뒤, 그 정보를 바탕으로 리턴 주소를 조작해 `win()`이나 원하는 함수로 보내는 문제 유형**입니다.

## 핵심 흐름
```text
overflow -> stack leak -> address calculation -> ret2win / small ROP -> flag
```

## 전문 설명
이 유형은 다음과 같은 상황에서 나옵니다.

1. 출력 포맷에 스택 주소가 섞여 나옵니다.
2. 첫 번째 입력으로는 주소를 누출하고, 두 번째 입력으로 제어 흐름을 바꿉니다.
3. 주소를 알게 되면 ASLR의 보호가 약해집니다.
4. `ret` 가젯을 여러 개 두어 스택 정렬과 체인 안정성을 확보합니다.

## 공격자 관점
- cyclic pattern으로 오프셋을 찾습니다.
- 출력 문자열에서 주소 필드를 정확히 파싱합니다.
- 누출된 주소에서 고정 오프셋을 빼거나 더해 필요한 값을 계산합니다.
- `win`, `printf`, `system` 같은 함수로 ret2win/ret2libc를 구성합니다.

## 방어자 관점
- 주소를 직접 출력하지 않습니다.
- 포맷 문자열과 디버그용 출력은 분리합니다.
- 스택 보호(NX, canary, PIE, ASLR)를 함께 적용합니다.
- 취약 함수와 진단용 함수의 역할을 분리합니다.

## 관련 writeup
- [[stack-cache-final-writeup]]

## 같이 보면 좋은 개념
- [[exploitation]]
- [[pie-aslr-function-offset-ctf-patterns]]
- [[rop-chain-execve-ctf-patterns]]
