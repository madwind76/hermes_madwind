---
title: PHP array input + null hash comparison — picoCTF 패턴
created: 2026-06-14
updated: 2026-06-14
type: concept
tags: [ctf, web, php, authentication, parameter-tampering, type-juggling]
sources: [https://medium.com/@mihasha/apriti-sesamo-picoctf-2025-write-up-7f3d4bfd6085, https://medium.com/@ahmednarmer1/ctf-day-23-595078e28d0f, https://hackmd.io/@fearnot/picoCTF_Web]
confidence: high
---

# PHP array input + null hash comparison — picoCTF 패턴

## Step 1. 한 줄 정의
이 패턴은 **PHP에서 스칼라 문자열을 기대하는 코드에 배열을 넣어 함수 반환값을 `null`로 만들고, 그 결과를 느슨하게 또는 동일성 비교로 우회하는 문제 유형**입니다.

## Step 2. 비유
- **비유**: 검사대에 여권 대신 “여권 묶음”을 내밀면, 검사기가 제대로 읽지 못하고 빈 종이처럼 처리되는 상황입니다.
- **이미지**: 백업 파일로 로직을 훔쳐본 뒤, 배열 입력으로 함수가 실패하도록 만들어 비교문을 깨뜨립니다.
- **전문 설명**: `sha1(array)`처럼 타입이 맞지 않으면 PHP가 경고를 내고 `null`을 반환할 수 있으며, `null === null` 또는 잘못된 분기 처리로 인증이 무너집니다.

## 핵심 흐름
```text
backup/source disclosure -> login logic 확인 -> scalar 입력 가정 찾기 -> array input 전송 -> sha1()/hash 함수 실패 -> null 비교 우회 -> flag / privileged action
```

## 공격자 관점
1. 백업 파일(`~`, `.bak`, `.old`)이나 소스 노출을 먼저 찾습니다.
2. 해시나 비교 로직에서 입력 타입을 확인합니다.
3. `username[]`, `password[]`처럼 배열이 되도록 전송합니다.
4. 함수 반환값이 경고와 함께 `null`이 되는지 봅니다.
5. 비교 조건이 `null` 기반으로 무너지는지 확인합니다.

## 방어자 관점
- 입력 타입을 먼저 검증합니다: `is_string()` / `ctype_*()` / 정규식.
- 해시 비교 전에 `null` 가능성을 배제합니다.
- 백업 파일과 소스 주석을 외부에 노출하지 않습니다.
- 인증 로직은 타입 강제 후 비교하도록 작성합니다.

## 같이 보면 좋은 페이지
- [[apriti-sesamo-final-writeup]]
- [[parameter-tampering-ctf-patterns]]
- [[web-ctf-writeup-auth-session]]
- [[lfi-rfi-core]] — 백업 파일/소스 노출 관점에서 연결

## 참고 소스
- [Apriti sesamo PicoCTF 2025 Write-up](https://medium.com/@mihasha/apriti-sesamo-picoctf-2025-write-up-7f3d4bfd6085)
- [CTF Day(23). picoCTF Web Exploitation: Apriti sesamo](https://medium.com/@ahmednarmer1/ctf-day-23-595078e28d0f)
- [picoCTF Web writeup - HackMD](https://hackmd.io/@fearnot/picoCTF_Web)
