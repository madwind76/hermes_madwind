---
title: Browser identity / header spoofing — Web CTF patterns
created: 2026-06-15
updated: 2026-06-21
type: concept
tags: [ctf, web, http, headers, user-agent, referer, dnt, x-forwarded-for, accept-language]
sources: [https://medium.com/@ahmednarmer1/ctf-day-41-fe36ae3311b0, https://picoctf2021.haydenhousen.com/web-exploitation/who-are-you, https://github.com/ZeroDayTea/PicoCTF-2021-Killer-Queen-Writeups/blob/main/WebExploitation/WhoAreYou.md]
confidence: high
---

# Browser identity / header spoofing — Web CTF patterns

## 참고 URL
- [medium.com](https://medium.com/@ahmednarmer1/ctf-day-41-fe36ae3311b0)
- [picoctf2021.haydenhousen.com](https://picoctf2021.haydenhousen.com/web-exploitation/who-are-you)
- [Original source](https://github.com/ZeroDayTea/PicoCTF-2021-Killer-Queen-Writeups/blob/main/WebExploitation/WhoAreYou.md)

## 1. 정의
**Browser identity / header spoofing**은 서버가 `User-Agent`, `Referer`, `Date`, `DNT`, `X-Forwarded-For`, `Accept-Language` 같은 HTTP 헤더를 신뢰하는 지점을 노리는 Web CTF 유형입니다. 브라우저의 정체성·출처·시간·지역·추적 설정을 직접 바꿔 서버의 분기 조건을 만족시키는 문제가 여기에 들어갑니다.

## 2. 쉬운 비유
서버가 “어디서 왔는지, 어떤 브라우저인지, 어느 나라 사람인지”를 묻는 상황에서, 공격자는 **신분증과 출입증을 모두 인쇄해서 다시 내는 사람**과 비슷합니다. 질문에 답하는 문구를 헤더 값으로 맞춰 넣으면, 서버가 진짜 사용자로 오해할 수 있습니다.

## 3. 자주 보이는 헤더
| 헤더 | 의미 | CTF에서 자주 쓰는 용도 |
|------|------|------------------------|
| `User-Agent` | 브라우저/디바이스 식별 | 특정 브라우저로 위장 |
| `Referer` | 이전 페이지 출처 | 외부 유입 차단 우회 |
| `Date` | 요청 시간 | 특정 연도/시점 체크 우회 |
| `DNT` | 추적 거부 여부 | 프라이버시 체크 우회 |
| `X-Forwarded-For` | 원 IP 추정 | 지역/IP 기반 차단 우회 |
| `Accept-Language` | 언어/로캘 | 국가/언어 조건 우회 |

## 4. 기본 풀이 루프
```text
거부 메시지 읽기 -> 어떤 헤더를 보는지 추측 -> Burp/curl로 한 줄씩 수정 -> 응답 메시지 확인 -> 다음 헤더로 진행
```

## 5. 공격자 관점
1. 거부 문구를 순서대로 읽어 힌트를 찾습니다.
2. 헤더를 한 번에 많이 바꾸지 않고 하나씩 바꿉니다.
3. `User-Agent`부터 시작해 `Referer`, `Date`, `DNT`, `X-Forwarded-For`, `Accept-Language` 순으로 점검합니다.
4. `curl -H` 또는 Burp Repeater로 반복 테스트합니다.
5. 마지막 조건이 만족되면 flag가 나옵니다.

## 6. 방어자 관점
- 브라우저 식별 정보는 보조 신호로만 사용합니다.
- IP 기반 판정은 프록시 신뢰 경계 밖에서 하면 안 됩니다.
- `Referer`나 `User-Agent`만으로 접근 제어를 하지 않습니다.
- 지역/언어 체크는 UX 용도로만 쓰고, 보안 경계로 쓰지 않습니다.

## 7. 같이 보면 좋은 페이지
- [[who-are-you-final-writeup]]
- [[http-method-manipulation-ctf-patterns]]
- [[web-ctf-writeup-auth-session]]
- [[web-ctf-writeup-client-side]]
- [[http]]

## 8. 관련 메모
- picoCTF `Who are you?`는 이 패턴의 대표 예시입니다.
- 실제로는 `PicoBrowser` 위장과 스웨덴 관련 헤더/지역 값이 필요했습니다.
