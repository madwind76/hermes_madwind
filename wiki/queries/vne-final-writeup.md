---
title: VNE — picoCTF 2023 pwn writeup
created: 2026-06-15
updated: 2026-06-15
type: query
tags: [ctf, pwn, environment-abuse, shell, command-abuse, picoctf, picoctf2023]
sources: [snwau/picoCTF-2023-Writeup, DanArmor/picoCTF-2023-writeup]
---

# VNE — picoCTF 2023 pwn writeup

> `VNE`는 **실행 환경과 셸/명령 호출을 악용하는 문제**입니다. 핵심은 **environment abuse + command execution**입니다.

## 참고 URL
- [snwau/picoCTF-2023-Writeup](snwau/picoCTF-2023-Writeup)
- [DanArmor/picoCTF-2023-writeup](DanArmor/picoCTF-2023-writeup)


## 요약
- 분류: pwn
- 핵심 primitive: environment / command abuse
- 난이도 감각: 초급~중급
- 연결 개념: [[environment-command-abuse-ctf-patterns]]

## 취약점 원인
프로그램이 `system()`, `popen()`, 혹은 셸을 거치는 명령 실행을 사용할 때, `PATH`나 환경 변수의 영향을 그대로 받으면 공격자가 실행 대상을 바꿀 수 있습니다. 겉으로는 단순한 실행이지만 실제로는 **명령 검색 경로가 공격면**이 됩니다.

## 공격 흐름
1. 프로그램이 외부 명령을 어떻게 실행하는지 확인합니다.
2. 환경 변수와 PATH가 어떤 영향을 주는지 확인합니다.
3. 우선순위가 높은 경로에 악성 실행 파일을 배치합니다.
4. 명령이 가로채지면 원하는 코드가 실행됩니다.

## 실전 포인트
- `system()`은 셸을 호출하므로 셸 확장과 PATH 영향을 받습니다.
- 절대경로 사용 여부가 우회 가능성을 크게 좌우합니다.
- setuid 바이너리라면 환경 변수 필터링 여부를 특히 봐야 합니다.

## 방어 관점
- 셸 호출 대신 직접 실행 또는 절대경로를 사용합니다.
- 불필요한 환경 변수를 상속하지 않습니다.
- setuid 프로그램에서 PATH 신뢰를 제거합니다.

## 재현 절차
1. 프로그램이 어떤 명령을 실행하는지 확인합니다.
2. PATH 우선순위를 이용해 가짜 명령을 앞세웁니다.
3. 실행 흐름이 가로채졌는지 검증합니다.

```bash
# 가짜 명령을 앞에 두는 디렉터리를 만들고 PATH를 조작합니다.
mkdir -p ./fakebin
printf '%s\n' '#!/bin/sh' 'echo hijacked' > ./fakebin/md5sum
chmod +x ./fakebin/md5sum

# PATH를 조작한 뒤 바이너리를 실행합니다.
PATH="$PWD/fakebin:$PATH" ./vne
```

## 참고
- [snwau writeup](https://github.com/snwau/picoCTF-2023-Writeup/blob/main/Binary%20Exploitation/VNE/VNE.md)
