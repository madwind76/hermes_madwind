---
title: hijacking — picoCTF 2023 pwn writeup
created: 2026-06-15
updated: 2026-06-15
type: query
tags: [ctf, pwn, module-hijack, environment-abuse, python, picoctf, picoctf2023]
sources: [snwau/picoCTF-2023-Writeup, DanArmor/picoCTF-2023-writeup]
---

# hijacking — picoCTF 2023 pwn writeup

> `hijacking`은 **Python import/module 검색 경로를 악용하는 문제**로 볼 수 있습니다. 핵심은 **module hijack + environment abuse**입니다.

## 요약
- 분류: pwn
- 핵심 primitive: module hijack
- 난이도 감각: 초급~중급
- 연결 개념: [[python-module-hijack-ctf-patterns]]

## 취약점 원인
프로그램이 현재 디렉터리나 `PYTHONPATH`를 신뢰한 채 모듈을 import하면, 공격자는 같은 이름의 모듈을 먼저 배치해 코드 실행을 가로챌 수 있습니다. 이는 전통적인 버퍼 오버플로우가 아니라 **검색 순서 자체를 공격**하는 패턴입니다.

## 공격 흐름
1. 프로그램이 어떤 모듈을 import하는지 확인합니다.
2. import search path 우선순위를 파악합니다.
3. 같은 이름의 모듈을 준비해 우선 로드되게 합니다.
4. 원하는 코드가 실행되도록 만들어 flag를 획득합니다.

## 실전 포인트
- 작업 디렉터리에 있는 파일이 표준 라이브러리보다 먼저 잡히는지 확인합니다.
- 파일명만 맞추는 것으로 끝나는지, 함수 시그니처도 맞춰야 하는지 확인합니다.
- subprocess 호출과 결합되어 있으면 환경 변수 조작도 함께 봐야 합니다.

## 방어 관점
- 절대경로 import 또는 명시적 패키지 로딩을 사용합니다.
- 실행 경로와 import path를 신뢰하지 않습니다.
- 배포 환경에서 현재 디렉터리 포함 여부를 점검합니다.

## 재현 절차
    1. import 대상 모듈 이름과 검색 경로를 확인합니다.
    2. 우선 로드되는 위치에 동일 이름의 파일을 배치합니다.
    3. 악성 모듈이 먼저 로드되는지 검증합니다.

    ```bash
    # 현재 디렉터리에 같은 이름의 모듈을 두고 import 우선순위를 확인합니다.
    printf 'print("hijacked")
' > os.py

    # 문제 바이너리/스크립트를 실행해 우선 로드 여부를 확인합니다.
    python3 ./hijacking.py
    ```

## 참고
- [snwau writeup](https://github.com/snwau/picoCTF-2023-Writeup/blob/main/Binary%20Exploitation/hijacking/hijacking.md)
