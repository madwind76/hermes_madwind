---
title: format string 0 — picoCTF 2024 pwn writeup
created: 2026-06-15
updated: 2026-06-21
type: query
tags: [ctf, pwn, format-string, buffer-overflow, crash, signal-handler, picoctf]
sources: [https://github.com/snwau/picoCTF-2024-Writeup/blob/main/Binary%20Exploitation/format%20string%200/format%20string%200.md, https://www.youtube.com/watch?v=bkCV44NdNh0, https://hackmd.io/@Zzzzek/r14x13FRp]
confidence: high
---

# format string 0 — picoCTF 2024 pwn writeup

> `format string 0`는 공개 풀이마다 표현이 조금 다르지만, 핵심은 **버거 메뉴의 선택 문자열/입력이 잘못 처리되어 flag 경로가 열리는 문제**입니다. 공개 writeup에서는 **format specifier가 포함된 선택지**와 **충분한 길이의 입력으로 크래시를 유도하는 방식**이 함께 강조됩니다.

## 참고 URL
- [Original writeup](https://github.com/snwau/picoCTF-2024-Writeup/blob/main/Binary%20Exploitation/format%20string%200/format%20string%200.md)
- [www.youtube.com](https://www.youtube.com/watch?v=bkCV44NdNh0)
- [hackmd.io](https://hackmd.io/@Zzzzek/r14x13FRp)


## 핵심 요약
- 메뉴형 바이너리입니다.
- `Cla%sic_Che%s%steak` 같은 선택지는 format string 취약점을 드러냅니다.
- 일부 풀이에서는 버퍼 크기 초과로 크래시를 유도해 `sigsegv` handler가 flag를 출력합니다.

## 공격 흐름
1. 제공된 선택지 중 format specifier(`%s`, `%d`)가 들어간 값을 찾습니다.
2. 프로그램의 입력/출력 흐름을 관찰해 flag가 출력되는 분기를 찾습니다.
3. 문제의 의도에 맞는 선택지를 고르거나, 입력 크기를 초과시켜 크래시를 유도합니다.

## 학습 포인트
- format specifier가 문자열에 그대로 남아 있으면 위험합니다.
- crash handler가 민감 정보를 출력하면, **크래시 자체가 공격 목표**가 될 수 있습니다.

## 방어 관점
- 사용자 입력을 `printf(user_input)`로 출력하지 않습니다.
- 메뉴 문자열에 `%` 문자를 허용할 때는 이스케이프가 필요합니다.

## 재현 절차
1. 메뉴 선택과 입력 문자열이 어떻게 처리되는지 확인합니다.
2. format specifier가 노출되는 지점을 찾습니다.
3. 크래시 유도 또는 flag 분기 진입이 되는 입력을 재현합니다.

```bash
# 문제 바이너리를 실행해 메뉴와 입력 형식을 먼저 확인합니다.
./format-string-0

# 디버깅용으로 gdb를 붙여 입력 처리 흐름을 관찰합니다.
gdb -q ./format-string-0
```

## 관련 개념
- [[format-string-ctf-patterns]]
