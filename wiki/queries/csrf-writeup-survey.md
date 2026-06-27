---
title: CSRF writeup survey
created: 2026-06-19
updated: 2026-06-21
type: query
tags: [ctf, web, survey, writeup, csrf, request-forgery, browser]
sources: [https://raw.githubusercontent.com/Yahyahcini/hacker101-ctf-writeups/main/Ticketastic%3A%20Live%20Instance/README.md, https://github.com/noamgariani11/picoCTF-2024-Writeup]
confidence: high
---

# CSRF writeup survey

## 참고 URL
- [raw source](https://raw.githubusercontent.com/Yahyahcini/hacker101-ctf-writeups/main/Ticketastic%3A%20Live%20Instance/README.md)
- [noamgariani11/picoCTF-2024-Writeup](https://github.com/noamgariani11/picoCTF-2024-Writeup)


## 1. 목적
CSRF가 단독으로 등장하는 경우와 다른 취약점과 결합되는 경우를 비교합니다.

## 2. 비교 대상
| 문제 | 주된 primitive | 보조 primitive | 한 줄 요약 |
|---|---|---|---|
| Ticketastic: Live Instance | stored HTML → CSRF | SQLi | 티켓 본문에 HTML을 넣어 관리자 CSRF를 유도합니다. |
| Secure Email Service | XSS + CSRF | broken auth | HTML email로 CSRF 체인을 구성하고 브라우저 sink를 악용합니다. |

## 3. 공통 관찰
1. CSRF는 토큰 없이 중요한 액션(GET)이 실행되는 지점이 핵심입니다.
2. CSRF는 단독보다 XSS나 stored HTML과 결합될 때 실제 위협이 됩니다.
3. 요청 변조와 CSRF를 구분하는 기준은 인증된 사용자의 의도치 않은 액션 유도 여부입니다.

## 4. 관련 개념
- [[csrf]]
- [[web-ctf-writeup-client-side]]
- [[web-ctf-writeup-auth-session]]
- [[web-ctf-writeup-family-hub]]
- [[ticketastic-live-instance-final-writeup]]
- [[secure-email-service-final-writeup]]

## 5. 다음 읽을 거리
- [[ticketastic-live-instance-final-writeup]]
- [[secure-email-service-final-writeup]]
