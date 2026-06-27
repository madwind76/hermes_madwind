---
title: Ticketastic: Live Instance — Hacker101 CTF writeup
created: 2026-06-19
updated: 2026-06-19
type: query
tags: [ctf, web, writeup, csrf, sqli, injection, tampering]
sources: [https://raw.githubusercontent.com/Yahyahcini/hacker101-ctf-writeups/main/Ticketastic%3A%20Live%20Instance/README.md]
confidence: high
---

# Ticketastic: Live Instance — Hacker101 CTF writeup

> HTML이 그대로 렌더링되는 티켓 본문과, SQL injection 가능한 ticket ID 조회가 함께 있는 복합 Web writeup입니다.

## 참고 URL
- [raw source](https://raw.githubusercontent.com/Yahyahcini/hacker101-ctf-writeups/main/Ticketastic%3A%20Live%20Instance/README.md)


## 1. 한 줄 요약
- 관리자에게 보이는 티켓 본문에 HTML 링크를 넣어 CSRF를 유도합니다.
- `/newUser`가 GET 기반이라 토큰 없이 계정이 생성됩니다.
- 이후 `/ticket?id=`에서 SQL injection으로 사용자 테이블을 덤프합니다.

## 2. 문제 구조
| 항목 | 내용 |
|---|---|
| 플랫폼 | Hacker101 CTF |
| 난이도 | Moderate |
| 핵심 아이디어 | CSRF, stored HTML injection, SQL injection |
| 관련 개념 | [[csrf]], [[sql-injection]], [[parameter-tampering-ctf-patterns]] |
| 관련 survey | [[hacker101-web-writeup-survey]] |

## 3. 공격면 정리
1. 인증 없이 티켓을 제출할 수 있는지 확인합니다.
2. 티켓 본문이 HTML로 렌더링되는지 봅니다.
3. `newUser` 요청이 CSRF 토큰 없이 동작하는지 점검합니다.
4. 새로 만든 계정으로 로그인한 뒤, `ticket?id=` 파라미터를 테스트합니다.

## 4. 풀이 흐름
```html
<!-- 1) 관리자에게 노출될 티켓 본문에 CSRF 링크를 삽입합니다. -->
<a href="http://localhost/newUser?username=hcini&password=ooooooo&password2=ooooooo">click</a>
<!-- 예상 결과: 관리자가 티켓을 열면 서버 측 요청이 발생합니다. -->
```

```bash
# 2) SQLi가 있는 티켓 조회 요청을 반복 분석합니다.
# 예상 결과: DB 이름과 테이블, 사용자 계정이 열거됩니다.
ghauri -r req2.txt --dbs
```

## 5. 왜 취약한가
- HTML 렌더링을 그대로 허용합니다.
- 상태 변경 요청이 GET으로 열려 있습니다.
- ID 기반 조회가 문자열 결합으로 구성됩니다.

## 6. 방어 관점
- 상태 변경은 POST + CSRF token으로 제한합니다.
- 사용자 입력은 HTML로 렌더링하기 전에 escape합니다.
- SQL query는 prepared statement로 바꿉니다.

## 7. 다음 연결
- [[hacker101-web-writeup-survey]]
- [[csrf]]
- [[sql-injection]]
- [[web-ctf-writeup-auth-session]]
