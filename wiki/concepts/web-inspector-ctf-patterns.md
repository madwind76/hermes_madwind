---
title: Web Inspector
created: 2026-06-13
updated: 2026-06-16
type: concept
tags: [ctf, web, inspector, source-analysis]
sources: [https://github.com/noamgariani11/picoCTF-2024-Writeup/blob/main/Web%20Exploitation/WebDecode.md, https://medium.com/@Kamal_S/picoctf-web-exploitation-webdecode-2fb5f668eae6, https://infosecwriteups.com/picoctf-2024-webdecode-3801d825f803]
confidence: medium
---

# Web Inspector

## 정의
브라우저 개발자 도구에서 HTML, CSS, JS, 네트워크 응답을 확인해 숨겨진 정보와 동작을 분석하는 기법입니다.

## 왜 중요한가
Web CTF는 화면에 보이는 내용보다 **소스 코드와 응답 본문**에 답이 숨는 경우가 많습니다.

## 관찰 포인트
- HTML attribute
- 주석
- 포함된 JS/CSS 파일
- hidden input / meta tag
- 응답 본문의 안내 문구

## 공격 패턴
1. 페이지의 모든 링크를 탐색합니다.
2. Inspector로 HTML 소스를 확인합니다.
3. 수상한 attribute나 주석을 찾습니다.
4. 값을 복사해 인코딩 여부를 판별합니다.

## 방어 포인트
- 민감한 정보는 클라이언트에 노출하지 않습니다.
- 소스에 넣은 값은 이미 공격자에게 공개된 것으로 봐야 합니다.
- 중요한 로직은 서버 측에서만 처리합니다.

## 관련 예시
- [[webdecode]]
- [[unminify]]
- [[source-inspection-minification-ctf-patterns]]
- [[intro-to-burp]]

## 관련 도구
- [[cyberchef]]
- [[web-ctf-master-checklist]]
