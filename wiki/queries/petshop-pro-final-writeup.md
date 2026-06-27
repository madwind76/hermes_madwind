---
title: Petshop Pro — Hacker101 CTF writeup
created: 2026-06-19
updated: 2026-06-19
type: query
tags: [ctf, web, writeup, idor, parameter-tampering, xss, tampering]
sources: [https://raw.githubusercontent.com/Yahyahcini/hacker101-ctf-writeups/main/petshop-pro/README.md]
confidence: high
---

# Petshop Pro — Hacker101 CTF writeup

> hidden field, IDOR, stored XSS가 각각 다른 지점에서 터지며, 개별 취약점이 아닌 체인으로 점수를 주는 전형적인 Web writeup입니다.

## 참고 URL
- [raw source](https://raw.githubusercontent.com/Yahyahcini/hacker101-ctf-writeups/main/petshop-pro/README.md)


## 1. 한 줄 요약
- 체크아웃 폼의 hidden `price` 값을 바꾸면 결제가 바뀝니다.
- `/edit?id=`는 인증 없이 접근되는 IDOR입니다.
- 상품명에 저장된 XSS가 카트 페이지에서 실행됩니다.

## 2. 문제 구조
| 항목 | 내용 |
|---|---|
| 플랫폼 | Hacker101 CTF |
| 난이도 | Easy |
| 핵심 아이디어 | hidden field tampering, IDOR, stored XSS |
| 관련 개념 | [[parameter-tampering-ctf-patterns]], [[idor-ctf-patterns]], [[xss]] |
| 관련 survey | [[hacker101-web-writeup-survey]] |

## 3. 공격면 정리
1. checkout request에서 hidden `price` 필드를 찾습니다.
2. `/edit?id=0` 또는 `/edit?id=1` 같은 직접 객체 참조를 확인합니다.
3. 상품명 필드가 저장 후 어디에서 렌더링되는지 확인합니다.
4. 카트 페이지에서 저장된 XSS가 실행되는지 검증합니다.

## 4. 풀이 흐름
```text
# 1) hidden field tampering
price=100 → price=1
# 예상 결과: 서버가 클라이언트 값을 그대로 신뢰하는지 확인합니다.

# 2) IDOR 확인
/edit?id=0
# 예상 결과: 인증 없이 편집 페이지가 열립니다.

# 3) stored XSS 관찰
상품명 입력 → /cart에서 실행
# 예상 결과: 저장된 값이 카트 페이지에서 렌더링됩니다.
```

## 5. 왜 취약한가
- 금액을 클라이언트 폼에 두었습니다.
- ID를 순차적으로 노출하면서 권한 검사를 누락했습니다.
- 저장 후 렌더링 시 escape가 부족합니다.

## 6. 방어 관점
- 가격은 서버에서 계산합니다.
- ID 접근은 권한 체크를 붙입니다.
- 저장된 HTML은 렌더링 시 escape합니다.

## 7. 다음 연결
- [[hacker101-web-writeup-survey]]
- [[parameter-tampering-ctf-patterns]]
- [[idor-ctf-patterns]]
- [[xss]]
