---
title: IDOR writeup survey
created: 2026-06-19
updated: 2026-06-21
type: query
tags: [ctf, web, survey, writeup, idor, broken-access-control, authorization, tampering]
sources: [https://raw.githubusercontent.com/Yahyahcini/hacker101-ctf-writeups/main/petshop-pro/README.md, https://github.com/atomicmemory/llm-wiki/blob/main/examples/boomshop-final-writeup.md]
confidence: high
---

# IDOR writeup survey

## 참고 URL
- [raw source](https://raw.githubusercontent.com/Yahyahcini/hacker101-ctf-writeups/main/petshop-pro/README.md)
- [Original writeup](https://github.com/atomicmemory/llm-wiki/blob/main/examples/boomshop-final-writeup.md)


## 1. 목적
객체 식별자를 직접 바꾸는 IDOR와, 그것이 parameter tampering / broken access control과 어떻게 연결되는지 비교합니다.

## 2. 비교 대상
| 문제 | 주된 primitive | 보조 primitive | 한 줄 요약 |
|---|---|---|---|
| Petshop Pro | IDOR + hidden field tampering | stored XSS | `/edit?id=`와 hidden `price`를 함께 조작합니다. |
| BoomShop | IDOR + SSRF | broken access control | profile ID 변경으로 권한이 새는 구조를 확인합니다. |

## 3. 공통 관찰
1. ID 값이 URL이나 JSON에 그대로 드러나면 객체 소유권 검사가 핵심입니다.
2. hidden field 조작은 종종 IDOR와 같은 뿌리에서 나옵니다.
3. IDOR는 단독 취약점처럼 보여도 다른 공격면(SSRF, XSS, export 기능)으로 이어집니다.

## 4. 관련 개념
- [[idor-ctf-patterns]]
- [[broken-access-control-defense]]
- [[parameter-tampering-ctf-patterns]]
- [[web-ctf-writeup-family-hub]]
- [[petshop-pro-final-writeup]]
- [[boomshop-final-writeup]]

## 5. 다음 읽을 거리
- [[petshop-pro-final-writeup]]
- [[boomshop-final-writeup]]
