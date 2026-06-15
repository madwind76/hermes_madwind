---
title: Flask signed session cookie forgery — CTF patterns
created: 2026-06-15
updated: 2026-06-15
type: concept
tags: [ctf, web, flask, cookies, session, signing, authentication]
sources: [https://palletsprojects.com/p/flask/, https://itsdangerous.palletsprojects.com/, https://picoctf2021.haydenhousen.com/web-exploitation/most-cookies]
confidence: high
---

# Flask signed session cookie forgery — CTF patterns

## 1. 정의
**Flask signed session cookie forgery**는 Flask가 `secret_key`로 서명하는 세션 쿠키를 CTF 공격면으로 보는 패턴입니다. 쿠키 값이 암호화되지 않았더라도, 서명 키가 약하면 공격자가 세션을 다시 만들어 관리자 권한이나 다른 사용자 상태를 위조할 수 있습니다.

## 2. 쉬운 비유
이 패턴은 **도장 찍힌 종이 봉투**와 비슷합니다. 내용물이 봉투 안에 그대로 보여도, 봉투에 찍힌 도장이 진짜인지 확인하는 방식이면 됩니다. 그런데 도장에 쓰는 잉크 색이나 도장 모양을 쉽게 맞출 수 있으면, 공격자가 똑같은 봉투를 다시 만들어 제출할 수 있습니다.

## 3. 관찰 포인트
1. `session` 쿠키가 Flask 스타일로 보이는지 확인합니다.
2. `flask-unsign`, `itsdangerous`, `cookie` 같은 단서가 코드나 힌트에 있는지 봅니다.
3. 소스 코드에 `secret_key` 후보 목록이 짧게 들어 있지 않은지 확인합니다.
4. 쿠키 값이 변조 불가능한지, 또는 키를 알면 재서명 가능한지 테스트합니다.

## 4. 기본 풀이 루프
```text
# 1) 세션 쿠키를 복사합니다.
# 예상 결과: Flask session 문자열이 확보됩니다.

# 2) 언서명/검증 도구로 secret key 후보를 시험합니다.
# 예상 결과: 짧은 후보 목록 중 하나가 맞습니다.

# 3) 관리자 payload를 만든 뒤 다시 서명합니다.
# 예상 결과: 관리자 권한이나 숨은 기능이 열립니다.
```

## 5. CTF에서 자주 보이는 변형
- secret key가 짧은 사전 단어 목록에서 선택됨
- 소스 코드에서 키 후보가 그대로 노출됨
- 쿠키 payload가 JSON/딕셔너리 구조라 일부 필드만 수정하면 됨
- `admin`, `isAdmin`, `role` 같은 플래그성 필드가 세션에 직접 들어감

## 6. 방어 관점
- Flask `secret_key`는 충분히 길고 무작위여야 합니다.
- 세션에 민감한 권한을 과하게 넣지 않습니다.
- 서버는 클라이언트 쿠키를 “권한의 원천”으로 취급하지 않습니다.

## 7. 같이 보면 좋은 페이지
- [[most-cookies-final-writeup]]
- [[cookie-client-storage-ctf-patterns]]
- [[web-ctf-writeup-auth-session]]
- [[power-cookie-final-writeup]]
- [[cbc-bit-flipping-ctf-patterns]]
