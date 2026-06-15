---
title: Base64 Decoding
created: 2026-06-13
updated: 2026-06-16
type: concept
tags: [ctf, web, base64, encoding]
sources: [https://github.com/noamgariani11/picoCTF-2024-Writeup/blob/main/Web%20Exploitation/WebDecode.md, https://medium.com/@Kamal_S/picoctf-web-exploitation-webdecode-2fb5f668eae6, https://infosecwriteups.com/picoctf-2024-webdecode-3801d825f803]
confidence: medium
---

# Base64 Decoding

## 정의
Base64는 바이너리/텍스트 데이터를 ASCII 문자열로 옮기기 위한 인코딩 방식입니다. 암호화가 아닙니다.

## 왜 중요한가
CTF에서는 HTML 속성, 쿠키, API 응답에 Base64 문자열이 자주 숨겨집니다.

## 판별 포인트
- 길이가 길고 알파벳/숫자/`+`/`/`/`=` 패턴이 보이는지
- 앞뒤가 `picoCTF{` 형태로 복원될 가능성이 있는지
- 디코딩 후 사람이 읽을 수 있는 문자열이 나오는지

## 공격 패턴
1. 수상한 문자열을 복사합니다.
2. Base64 decode를 시도합니다.
3. 결과가 또 다른 인코딩인지 확인합니다.
4. flag 형식이면 종료합니다.

## 방어 포인트
- 인코딩 값을 민감 정보 저장에 사용하지 않습니다.
- 클라이언트에 노출되는 값은 보호 대상이 아닙니다.

## 관련 예시
- [[webdecode]]
- [[cookie-monster-secret-recipe-final-writeup]]
- [[cookie-client-storage-ctf-patterns]]
- [[web-inspector-ctf-patterns]]

## 관련 도구
- [[cyberchef]]
- [[web-ctf-master-checklist]]
