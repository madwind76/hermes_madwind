---
title: XPath injection — CTF patterns
created: 2026-06-15
updated: 2026-06-15
type: concept
tags: [ctf, web, xpath, injection, xml, login-bypass]
sources: [https://picoctf2021.haydenhousen.com/web-exploitation/x-marks-the-spot, https://ctftime.org/writeup/27158, https://ctftime.org/writeup/27171]
confidence: high
---

# XPath injection — CTF patterns

## 1. 정의
**XPath injection**은 XML 문서를 질의하는 XPath 식에 사용자 입력이 그대로 결합될 때 발생하는 취약점입니다. SQL injection과 비슷하게 보이지만, 공격 대상은 데이터베이스가 아니라 XML 구조를 탐색하는 식입니다.

## 2. 왜 중요한가
- 로그인/검색/필터 로직이 XML 기반일 때 자주 등장합니다.
- `starts-with()`, `contains()`, `substring()` 같은 함수를 이용한 blind 추측이 가능합니다.
- SQLi처럼 보이는 payload가 먹히지 않아도, XPath 문법으로는 우회될 수 있습니다.

## 3. 공격 흐름
1. 입력값이 XPath 식에 들어가는지 찾습니다.
2. 참/거짓 응답 차이를 관찰합니다.
3. `or` 조건이나 함수 호출을 이용해 oracle을 만듭니다.
4. 문자 단위로 사용자명/비밀번호/flag를 추측합니다.

## 4. picoCTF 2021 `X marks the spot`에서의 적용
이 문제는 blind XPath injection 형태의 로그인 우회 문제입니다. 응답 차이를 이용해 문자열을 한 글자씩 복원하고, 자동화 스크립트로 flag를 찾습니다.

## 5. 같이 보면 좋은 페이지
- [[x-marks-the-spot-final-writeup]]
- [[web-ctf-writeup-parser-template]]
- [[xxe]]

## 6. 방어 관점
- XPath 식을 문자열 결합으로 만들지 않습니다.
- XML 파싱과 쿼리 생성을 분리합니다.
- 인증 로직은 XPath가 아니라 서버 세션/토큰 기반으로 구성합니다.
