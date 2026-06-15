---
title: Format String — CTF patterns
created: 2026-06-15
updated: 2026-06-15
type: concept
tags: [ctf, pwn, format-string, printf, stack-leak, memory-disclosure]
sources: [https://ctftime.org/writeup/32816, https://picoctf2022.haydenhousen.com/binary-exploitation/flag-leak, https://medium.com/@zeyadsalah686/flag-leak-picoctf-writeup-e7b53f3273e2]
confidence: high
---

# Format String — CTF patterns

## Step 1. 단어 풀이
- **Format string**: 문자열에 들어 있는 `%p`, `%x`, `%s` 같은 서식 지정자입니다.
- **Vulnerability**: 입력이 포맷 문자열로 해석되면서, 프로그램이 의도치 않게 메모리를 읽거나 쓸 수 있는 결함입니다.
- **Stack leak**: 스택에 있는 값이 유출되는 현상입니다.

## 한 문장 정의
이 패턴은 **`printf(user_input)`처럼 사용자 입력이 포맷 문자열로 처리될 때, 스택/힙/전역 메모리를 읽어 flag나 주소를 유출하는 문제 유형**입니다.

## 핵심 흐름
```text
user input -> printf format parsing -> stack traversal -> leak addresses / strings -> reconstruct flag or bypass checks
```

## 전문 설명
이 유형은 보통 다음 특징을 가집니다.

1. `printf`, `fprintf`, `snprintf` 등에서 **고정 포맷 문자열이 없음**.
2. `%p`, `%x`, `%s`, `%n` 등이 공격 표면이 됩니다.
3. positional specifier(`%7$p`, `%36$s`)로 원하는 위치를 지정할 수 있습니다.
4. 민감한 데이터가 스택이나 전역 변수에 있다면 그대로 유출될 수 있습니다.

## 공격자 관점
- 먼저 `%p %p %p`로 취약점을 확인합니다.
- `nil`, `0x41414141`, 리턴 주소 같은 값을 보고 스택 구조를 추정합니다.
- `%s`는 문자열 포인터를 따라가므로 크래시 위험이 있지만, flag를 직접 읽는 데 유용합니다.
- 위치를 알면 brute force 대신 positional specifier를 씁니다.

## 방어자 관점
- `printf(user_input)`를 금지하고 `printf("%s", user_input)`를 사용합니다.
- `-Wformat-security`, `-Werror=format-security`를 활성화합니다.
- 민감 데이터를 스택에 오래 두지 않습니다.
- 프로덕션 로그에 사용자 입력을 포맷 문자열로 흘리지 않습니다.

## 관련 writeup
- [[flag-leak-final-writeup]]
- [[pie-time-final-writeup]]

## 같이 보면 좋은 개념
- [[exploitation]]
- [[rce]]
- [[pie-aslr-function-offset-ctf-patterns]]
