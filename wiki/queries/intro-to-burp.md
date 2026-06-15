---
title: IntroToBurp
created: 2026-06-13
updated: 2026-06-16
type: query
tags: [ctf, web, burp, parameter-tampering]
sources: [https://github.com/noamgariani11/picoCTF-2024-Writeup/blob/main/Web%20Exploitation/IntroToBurp.md, https://medium.com/@Bl4cky/picoctf-2024-web-exploitation-introtoburp-ecbcfc60272e, https://infosecwriteups.com/picoctf-2024-write-up-web-992348f48b99]
confidence: medium
---

# IntroToBurp

> 이 페이지는 **picoCTF 2024 공개 writeup**을 바탕으로 정리한 학습용 진행 노트입니다.

## 1. 요약
- 플랫폼: picoCTF 2024
- 난이도: Easy
- 문제 유형: Web Exploitation
- 핵심 개념: [[burp-suite]], [[parameter-tampering-ctf-patterns]], [[web-ctf-master-checklist]]
- 현재 상태: 공개 writeup 기반으로 풀이 흐름 정리 완료

## 2. 공격면
| Route | Method | Auth | Input | Output | Notes |
|------|------|------|------|------|------|
| / | GET / POST | No | registration form | redirect / OTP flow | 초기 등록 입력값은 크게 중요하지 않음 |
| /dashboard | GET / POST | No | otp | flag / invalid otp | OTP 파라미터 조작이 핵심 |

## 3. 가설
- 가설 1: 서버는 OTP 존재 여부를 제대로 검증하지 않습니다.
- 가설 2: OTP 값의 형식보다 파라미터 구조 자체가 중요합니다.
- 가설 3: `otp` 파라미터를 제거하면 우회가 성립할 수 있습니다.

## 4. 실험 기록
### 시도 1
- payload: 임의 등록 값 입력
- 관찰: 다음 단계로 OTP 페이지가 열림
- 해석: 초기 등록 자체는 검증 포인트가 아닙니다.
- 다음 가설: OTP 요청을 Burp로 잡아 조작

### 시도 2
- payload: `otp=123456` 또는 임의 문자열
- 관찰: Invalid OTP
- 해석: 단순 값 변경은 실패합니다.
- 다음 가설: 파라미터 존재 여부를 시험

### 시도 3
- payload: `otp` 파라미터 제거
- 관찰: flag 응답
- 해석: 필수 파라미터 누락에 대한 서버측 검증이 약합니다.

## 5. 연결된 개념
- [[parameter-tampering-ctf-patterns]]
- [[burp-request-mutation]]
- [[burp-suite]]
- [[web-ctf-master-checklist]]

## 6. 회고
- 막힌 지점: OTP 값을 바꿔도 실패해서, 처음에는 값 자체가 핵심이라고 착각하기 쉽습니다.
- 우회 포인트: **값 조작보다 파라미터 제거**가 핵심입니다.
- 다음에 먼저 볼 것: 필수 필드 존재 여부, 서버측 입력 검증, 프런트엔드 의존 여부
- 재사용 체크리스트:
  - [ ] 필수 파라미터가 서버에서 검증되는가
  - [ ] 값 범위보다 파라미터 존재가 더 중요한가
  - [ ] Burp Repeater로 요청 구조를 쉽게 바꿀 수 있는가
  - [ ] OTP / CSRF / 토큰 검증이 누락되었는가
