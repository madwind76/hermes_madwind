---
title: Web CTF Writeup — 인증/세션/권한
created: 2026-06-14
updated: 2026-06-21
type: query
tags: [ctf, web, research, writeup, auth, session]
sources: [https://blog.hokyun.dev/posts/csaw-ctf-2024-quals-writeup/, https://github.com/ernw/ctf-writeups/blob/master/csaw2016/mfw/README.md, raw/articles/20260613_web-ctf-writeup-curated.md]
confidence: high
---

# Web CTF Writeup — 인증/세션/권한

> 로그인, 세션 위조, 객체 소유권 검증, 권한 분기 실수를 모아둔 분류입니다.

## 참고 URL
- [blog.hokyun.dev](https://blog.hokyun.dev/posts/csaw-ctf-2024-quals-writeup/)
- [Original writeup](https://github.com/ernw/ctf-writeups/blob/master/csaw2016/mfw/README.md)
- [raw/articles/20260613_web-ctf-writeup-curated.md](raw/articles/20260613_web-ctf-writeup-curated.md)


## 1. 핵심 요약
- 이 분류는 **토큰이 맞는지**보다 **토큰이 누구를 의미하는지**가 중요한 문제를 모읍니다.
- 서버가 세션 값, 쿠키, 사용자 ID를 신뢰하는 방식이 핵심 관찰 포인트입니다.
- `broken-auth`, `parameter-tampering`, `idor`와 자주 연결됩니다.

연결 개념: [[broken-auth]], [[idor]], [[parameter-tampering-ctf-patterns]], [[cookie-client-storage-ctf-patterns]], [[websocket-message-tampering-ctf-patterns]], [[broken-access-control]], [[flask-signed-session-cookie-ctf-patterns]], [[php-object-injection-ctf-patterns]]

## 2. 대표 writeup

| 문제 | 출처 | 핵심 아이디어 |
|------|------|---------------|
| `log me in` | CSAW CTF 2024 Quals | XOR 토큰 복원 후 `uid: 0` 세션 위조 |
| `mfw` | CSAW CTF 2016 | `assert()` 기반 RCE로 비밀 파일 접근 |
| `Power Cookie` | picoCTF 2022 | `isAdmin=0` → `isAdmin=1` 쿠키 변조 |
| `Cookies` | picoCTF 2021 | `name` 쿠키 값을 열거해 분기 우회 |
| `More Cookies` | picoCTF 2021 | CBC bit flipping으로 암호화 쿠키 변조 |
| `Most Cookies` | picoCTF 2021 | Flask signed session cookie 브루트포스 및 재서명 |
| `Super Serial` | picoCTF 2021 | PHP unserialize cookie로 object injection |
| [[no-sql-injection-final-writeup]] | picoCTF 2024 | MongoDB NoSQL injection으로 login bypass |
| [[cookie-monster-secret-recipe-final-writeup]] | picoCTF 2025 | `secret_recipe` cookie를 URL/Base64 디코딩 |

## 3. 자주 보이는 패턴
1. 토큰이 대칭 XOR/커스텀 인코딩으로 보호됨
2. 세션 cookie가 JSON과 1:1로 대응됨
3. `uid`, `role`, `admin` 같은 필드만 바꾸면 되는 구조
4. 권한 체크가 화면과 API에서 다르게 구현됨
5. ID 변경만으로 타 사용자 데이터가 노출됨

## 4. 읽을 때 확인할 것
- 세션 생성과 검증이 같은 함수인지
- 사용자 식별자와 권한 정보가 분리되어 있는지
- 서버가 클라이언트에서 온 식별자를 그대로 믿는지
- 관리자 기능이 별도 엔드포인트로 열려 있는지

## 5. 방어 관점
- 서명 없는 커스텀 토큰을 쓰지 않습니다.
- 권한 정보는 클라이언트에 넣지 않습니다.
- 객체 소유권은 모든 민감 API에서 재검증합니다.
- `role=admin` 같은 문자열 비교에 의존하지 않습니다.

## 6. 추천 다음 읽기
- [[web-ctf-master-checklist]]
- [[broken-auth]]
- [[idor]]
- [[broken-access-control]]
- [[idor-ctf-patterns]]
