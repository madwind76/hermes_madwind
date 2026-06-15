---
title: parameter tampering — web ctf patterns
created: 2026-06-13
updated: 2026-06-14
type: concept
tags: [ctf, web, burp, parameter-tampering]
sources: [https://github.com/noamgariani11/picoCTF-2024-Writeup/blob/main/Web%20Exploitation/IntroToBurp.md, https://medium.com/@Bl4cky/picoctf-2024-web-exploitation-introtoburp-ecbcfc60272e, https://infosecwriteups.com/picoctf-2024-write-up-web-992348f48b99]
confidence: medium
---

# Parameter Tampering

## 정의
클라이언트가 보내는 파라미터를 값 변경, 삭제, 재배열하여 서버의 검증 허점을 찾는 기법입니다.

## 왜 중요한가
서버가 프런트엔드 입력만 믿으면, 공격자는 Burp Suite나 curl로 요청을 쉽게 바꿀 수 있습니다.

## 관찰 포인트
- 필수 필드 누락 시 동작
- 값 형식 오류 시 동작
- 세션/토큰과 파라미터의 결합 여부
- 302 redirect 이후 숨은 검증 단계

## 공격 패턴
1. 정상 요청을 캡처합니다.
2. 단일 필드를 바꿔봅니다.
3. 값이 아니라 파라미터 삭제를 시험합니다.
4. 순서 변경, 중복 파라미터, 빈 값도 확인합니다.

## 방어 포인트
- 서버측 필수 필드 검증
- 세션 바인딩
- 상태 전이 검증
- 실패 응답의 일관성 확보

## 관련 CTF 예시
- [[intro-to-burp]]
- [[n0s4n1ty-1]]
- [[websockfish-final-writeup]]

## 관련 개념
- [[tampering]]
- [[http]]
- [[burp-request-mutation]]
- [[websocket-message-tampering-ctf-patterns]]
- [[burp-suite]]
- [[web-ctf-master-checklist]]
- [[intro-to-burp]] — 실제 파라미터 조작 예시
