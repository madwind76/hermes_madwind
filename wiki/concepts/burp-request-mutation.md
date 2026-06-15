---
title: Burp Request Mutation
created: 2026-06-13
updated: 2026-06-16
type: concept
tags: [ctf, web, burp, request-manipulation]
sources: [https://github.com/noamgariani11/picoCTF-2024-Writeup/blob/main/Web%20Exploitation/IntroToBurp.md, https://medium.com/@Bl4cky/picoctf-2024-web-exploitation-introtoburp-ecbcfc60272e, https://infosecwriteups.com/picoctf-2024-write-up-web-992348f48b99]
confidence: medium
---

# Burp Request Mutation

## 정의
Burp Suite의 Repeater/Intercept를 이용해 HTTP 요청을 변형하면서 서버의 취약한 전제조건을 찾는 절차입니다.

## 핵심 도구
- Intercept: 요청을 중간에서 멈춤
- Repeater: 동일 요청을 반복 변조
- Intruder: 동일 패턴을 대량 테스트

## 실전 관찰 포인트
- 특정 파라미터를 삭제했을 때만 성공하는가
- 값 변경보다 구조 변경이 더 효과적인가
- POST 바디, 쿼리스트링, 헤더 중 어디가 핵심인가
- 302 이후 흐름에서 검증이 생략되는가

## CTF에서 자주 보이는 형태
- OTP/2FA 파라미터 제거
- CSRF 토큰 삭제 또는 재사용
- hidden field 변조
- admin flag 파라미터 주입

## 방어 포인트
- 모든 상태 변경은 서버측에서 재검증
- 중요 파라미터 누락 처리
- 요청 구조 화이트리스트
- 토큰 재사용 방지

## 관련 예시
- [[intro-to-burp]]
- [[parameter-tampering-ctf-patterns]]

## 관련 도구
- [[burp-suite]]
- [[web-ctf-master-checklist]]
