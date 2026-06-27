---
title: Substring logic bug — CTF patterns
created: 2026-06-15
updated: 2026-06-21
type: concept
tags: [ctf, pwn, logic-bug, strstr, substring, validation, prng]
sources: [https://ctftime.org/writeup/33269, https://cryptocat.me/blog/ctf/2022/pico/pwn/rps/]
confidence: high
---

# Substring logic bug — CTF patterns

## 참고 URL
- [CTFtime writeup](https://ctftime.org/writeup/33269)
- [cryptocat.me](https://cryptocat.me/blog/ctf/2022/pico/pwn/rps/)

## Step 1. 단어 풀이
- **Substring**: 문자열 안에 들어있는 부분 문자열입니다.
- **Logic bug**: 메모리 손상 없이 프로그램의 판단 로직이 틀린 상태입니다.
- **`strstr()`**: 두 문자열 중 한 문자열이 다른 문자열에 포함되는지 찾는 함수입니다.

## 한 문장 정의
이 패턴은 **정확한 비교가 아니라 포함 여부/부분 일치 여부로 승패나 권한을 판단해서, 입력 하나로 조건을 우회하는 문제 유형**입니다.

## 핵심 흐름
```text
user input -> weak string check -> partial match -> wrong win/allow decision -> flag
```

## 전문 설명
이 유형은 다음과 같은 상황에서 자주 보입니다.

1. `strstr`, `contains`, `indexOf`, `includes` 같은 함수로 판정합니다.
2. 정확한 동등 비교가 아니라 부분 문자열 존재만 확인합니다.
3. 사용자는 여러 후보를 한 문자열에 섞어 넣어 승리를 강제할 수 있습니다.
4. 때로는 정규식, prefix 검사, suffix 검사도 같은 문제가 됩니다.

## 공격자 관점
- 판정 코드가 “정확한 값”인지 “포함/부분일치”인지 확인합니다.
- 여러 후보를 하나의 입력에 합쳐 우회 가능한지 봅니다.
- 대소문자, 공백, 구분자 처리도 점검합니다.

## 방어자 관점
- 권한/승리/인증 판단은 정확한 값 비교가 기본입니다.
- 부분 문자열 검색은 표시용으로만 사용하고, 인증 판단에는 쓰지 않습니다.
- 입력 정규화 후 비교합니다.

## 관련 writeup
- [[rps-final-writeup]]

## 같이 보면 좋은 개념
- [[exploitation]]
- [[format-string-ctf-patterns]]
- [[pie-aslr-function-offset-ctf-patterns]]
