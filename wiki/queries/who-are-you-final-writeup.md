---
title: Who are you? — picoCTF 2021 web writeup
created: 2026-06-15
updated: 2026-06-21
type: query
tags: [ctf, web, headers, user-agent, referer, dnt, x-forwarded-for, accept-language, burp]
sources: [https://medium.com/@ahmednarmer1/ctf-day-41-fe36ae3311b0, https://picoctf2021.haydenhousen.com/web-exploitation/who-are-you, https://github.com/ZeroDayTea/PicoCTF-2021-Killer-Queen-Writeups/blob/main/WebExploitation/WhoAreYou.md, https://ctftime.org/writeup/26905]
confidence: high
---

# Who are you? — picoCTF 2021 web writeup

> `Who are you?`는 서버가 신뢰하는 **HTTP 헤더 묶음**을 순서대로 맞춰서, 브라우저 정체성을 위장하는 문제입니다.

## 참고 URL
- [medium.com](https://medium.com/@ahmednarmer1/ctf-day-41-fe36ae3311b0)
- [picoctf2021.haydenhousen.com](https://picoctf2021.haydenhousen.com/web-exploitation/who-are-you)
- [Original writeup](https://github.com/ZeroDayTea/PicoCTF-2021-Killer-Queen-Writeups/blob/main/WebExploitation/WhoAreYou.md)
- [CTFtime writeup](https://ctftime.org/writeup/26905)


## 1. 한 줄 요약
- 핵심은 `PicoBrowser`처럼 보이게 만드는 것입니다.
- `User-Agent`, `Referer`, `Date`, `DNT`, `X-Forwarded-For`, `Accept-Language`를 바꿉니다.
- Burp Suite나 curl로 요청 헤더를 직접 수정하면 됩니다.

## 2. 문제 흐름
| 단계 | 관찰 | 의미 |
|------|------|------|
| 1 | “official PicoBrowser”만 허용 | `User-Agent` 체크 |
| 2 | “I don’t trust users visiting from another site.” | `Referer` 체크 |
| 3 | “This site only worked in 2018.” | `Date` 체크 |
| 4 | “I don’t trust users who can be tracked.” | `DNT` 체크 |
| 5 | “only for people from Sweden” | `X-Forwarded-For` 체크 |
| 6 | “You’re in Sweden but you don’t speak Swedish?” | `Accept-Language` 체크 |
| 7 | flag 확인 | 모든 조건 충족 |

## 3. 핵심 분석
이 문제는 브라우저가 보내는 **클라이언트 메타데이터**를 서버가 너무 많이 믿는 사례입니다.

- `User-Agent`는 브라우저 이름을 속일 수 있습니다.
- `Referer`는 이전 페이지 출처를 가장할 수 있습니다.
- `Date`는 오래된 브라우저 환경을 흉내 낼 수 있습니다.
- `DNT`는 추적 거부 의사처럼 보이는 값입니다.
- `X-Forwarded-For`는 프록시 뒤의 IP를 가짜로 넣는 데 쓰입니다.
- `Accept-Language`는 지역 언어 설정을 속이는 데 쓰입니다.

### 대표 헤더 예시
```http
# 브라우저 정체성을 흉내 내는 최소 예시입니다.
User-Agent: PicoBrowser
Referer: http://mercury.picoctf.net/
Date: Wed, 21 Oct 2018 07:28:00 GMT
DNT: 1
X-Forwarded-For: 31.3.152.55
Accept-Language: sv-SE
```

## 4. 공격자 관점
1. 서버가 어떤 메시지로 거부하는지 순서대로 읽습니다.
2. 한 번에 다 바꾸지 말고, 메시지 하나씩 따라갑니다.
3. 헤더를 하나 바꿀 때마다 서버 응답이 달라지는지 확인합니다.
4. 마지막 조건까지 충족하면 flag가 나옵니다.

## 5. 방어자 관점
- `User-Agent`나 `Referer`만으로 권한을 판단하지 않습니다.
- `X-Forwarded-For`는 신뢰 가능한 프록시 뒤에서만 해석합니다.
- 클라이언트가 보내는 메타데이터를 인증/인가 근거로 사용하지 않습니다.
- 지역/브라우저 기반 차단은 보조 신호로만 씁니다.

## 6. 같이 보면 좋은 페이지
- [[web-ctf-writeup-parser-template]]
- [[http-method-manipulation-ctf-patterns]]
- [[web-ctf-writeup-client-side]]
- [[web-ctf-writeup-auth-session]]
- [[browser-identity-header-spoofing-ctf-patterns]]

## 7. 참고 소스
- [Ahmed Narmer — Who are you?](https://medium.com/@ahmednarmer1/ctf-day-41-fe36ae3311b0)
- [PicoCTF-2021 Writeup — Who are you?](https://picoctf2021.haydenhousen.com/web-exploitation/who-are-you)
- [ZeroDayTea — WhoAreYou.md](https://github.com/ZeroDayTea/PicoCTF-2021-Killer-Queen-Writeups/blob/main/WebExploitation/WhoAreYou.md)
- [CTFtime — Who are you writeup](https://ctftime.org/writeup/26905)
