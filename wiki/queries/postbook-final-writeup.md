---
title: Postbook — Hacker101 CTF writeup
created: 2026-06-19
updated: 2026-06-21
type: query
tags: [ctf, web, writeup, auth, session, cookie, tampering]
sources: [https://github.com/Yahyahcini/hacker101-ctf-writeups/blob/main/postbook/README.md, https://github.com/Yahyahcini/hacker101-ctf-writeups/blob/main/README.md]
confidence: medium
---

# Postbook — Hacker101 CTF writeup

> 쿠키와 숨은 필드를 함께 조작해 서버가 신뢰하는 사용자 식별값을 바꾸는 cookie tampering 계열 writeup입니다.

## 참고 URL
- [Original writeup](https://github.com/Yahyahcini/hacker101-ctf-writeups/blob/main/postbook/README.md)
- [Original writeup](https://github.com/Yahyahcini/hacker101-ctf-writeups/blob/main/README.md)


## 1. 한 줄 요약
- `id` 쿠키가 사용자의 식별자와 연결되어 있고, 이 값이 서버 인증/권한 판정에 직접 쓰입니다.
- hidden field와 cookie를 함께 바꾸면 관리자 또는 다른 사용자 관점으로 동작이 바뀔 수 있습니다.

## 2. 문제 구조
| 항목 | 내용 |
|---|---|
| 플랫폼 | Hacker101 CTF |
| 카테고리 | Web / Auth |
| 핵심 아이디어 | cookie tampering, hidden field manipulation, IDOR 감별 |
| 관련 개념 | [[cookie-client-storage-ctf-patterns]], [[parameter-tampering-ctf-patterns]], [[broken-auth]] |
| 관련 survey | [[cookie-tampering-writeup-survey]] |

## 3. 관찰 포인트
1. 로그인 후 페이지가 사용자별로 달라지는지 봅니다.
2. `user_id`, `id`, `role` 같은 값이 쿠키 또는 hidden field에 노출되는지 확인합니다.
3. 쿠키 값을 다른 사용자로 바꿨을 때 응답 차이가 있는지 봅니다.
4. hidden field와 cookie를 동시에 바꿔야만 통과하는지 테스트합니다.

## 4. 풀이 흐름
1. 브라우저 개발자 도구에서 쿠키를 확인합니다.
2. hidden field를 Burp Repeater로 재전송합니다.
3. `id` 값과 서버 반응의 관계를 비교합니다.
4. 서버가 클라이언트 입력을 신뢰한다면 권한 상승 또는 사용자 위장이 가능합니다.

## 5. 방어 관점
- 사용자 식별과 권한은 클라이언트 쿠키가 아니라 서버 세션에서 관리합니다.
- hidden field는 편의용 메타데이터로만 쓰고, 권한 판정에 사용하지 않습니다.
- 민감한 값은 서명 또는 서버 조회로 검증합니다.

## 6. 다음 연결
- [[cookie-tampering-writeup-survey]]
- [[cookie-client-storage-ctf-patterns]]
- [[web-ctf-writeup-auth-session]]
