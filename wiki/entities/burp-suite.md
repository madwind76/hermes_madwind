---
title: Burp Suite
created: 2026-06-13
updated: 2026-06-21
type: entity
tags: [tool, burp, proxy, web]
sources: [https://portswigger.net/burp, https://github.com/noamgariani11/picoCTF-2024-Writeup/blob/main/Web%20Exploitation/IntroToBurp.md, https://medium.com/@Bl4cky/picoctf-2024-web-exploitation-introtoburp-ecbcfc60272e]
confidence: high
---

# Burp Suite

## 참고 URL
- [PortSwigger](https://portswigger.net/burp)
- [Original source](https://github.com/noamgariani11/picoCTF-2024-Writeup/blob/main/Web%20Exploitation/IntroToBurp.md)
- [Medium article](https://medium.com/@Bl4cky/picoctf-2024-web-exploitation-introtoburp-ecbcfc60272e)

## 정의
웹 요청을 가로채고 수정하는 데 사용하는 HTTP 프록시 기반 테스트 도구입니다.

## 주요 기능
- Proxy: 브라우저 요청 가로채기
- Repeater: 요청 재전송 및 변조
- Intruder: 반복 대입 공격
- Decoder: 인코딩/디코딩

## Web CTF에서의 역할
- 요청 구조를 바꾸어 parameter tampering을 검증합니다.
- 숨겨진 API 호출과 인증 흐름을 확인합니다.
- 302 redirect 이후의 요청을 분석합니다.

## 연결된 예시
- [[intro-to-burp]]
- [[parameter-tampering-ctf-patterns]]
- [[burp-request-mutation]]

## 관련 도구
- [[web-ctf-master-checklist]]
