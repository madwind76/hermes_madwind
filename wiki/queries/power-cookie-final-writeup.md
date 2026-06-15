---
title: Power Cookie — picoCTF 2022 web writeup
created: 2026-06-15
updated: 2026-06-15
type: query
tags: [ctf, web, cookies, session, auth, burp, tampering]
sources: [https://medium.com/@ahmednarmer1/ctf-day-27-1e6bb61eb835, https://ctftime.org/writeup/32830, https://github.com/arvindshima/PicoCTF-2022/blob/main/Web%20Exploitation/power-cookie.md, https://github.com/wasi-master/picoCTF-2022/blob/main/web_exploitation/power_cookie.md]
confidence: high
---

# Power Cookie — picoCTF 2022 web writeup

> `Power Cookie`는 브라우저 쿠키에 들어 있는 **권한 플래그를 직접 바꾸면 통과되는** 전형적인 클라이언트 신뢰 오류 문제입니다.

## 1. 한 줄 요약
- 핵심은 **`isAdmin=0` → `isAdmin=1`** 입니다.
- 서버가 쿠키 값을 권한 판단에 직접 사용합니다.
- 쿠키는 세션 유지용이지, 신뢰 가능한 관리자 증명이 아닙니다.

## 2. 문제 흐름
| 단계 | 관찰 | 의미 |
|------|------|------|
| 1 | `Continue as guest` 버튼이 보임 | 일반 사용자 흐름처럼 보임 |
| 2 | `/check.php`로 이동 | 별도 검증 엔드포인트가 존재 |
| 3 | `We apologize, but we have no guest services at the moment.` | 게스트 권한이 차단됨 |
| 4 | 쿠키를 확인 | 권한 판별 값이 쿠키에 있을 가능성 |
| 5 | `isAdmin=0` 발견 | 클라이언트가 통제 가능한 값 |
| 6 | `isAdmin=1`로 변경 | 권한 상승 시도 |
| 7 | flag 확인 | 문제 해결 |

## 3. 핵심 분석
이 문제는 **인증(authentication)** 이 아니라 **권한(authorization)** 검증을 클라이언트 쿠키에 맡긴 경우입니다.

- 브라우저 쿠키는 사용자가 마음대로 바꿀 수 있습니다.
- 서버가 `isAdmin` 값을 그대로 믿으면, 단 한 글자 변경으로 접근이 바뀝니다.
- `isAdmin` 같은 값을 쿠키에 두더라도, 반드시 서버에서 서명/세션 검증을 해야 합니다.

### 대표 조작 예시
```javascript
// 브라우저 콘솔에서 쿠키 값을 바꿔 권한 체크를 우회합니다.
// 예상 결과: /check.php 재요청 시 관리자 흐름 또는 flag 페이지로 이동할 수 있습니다.
document.cookie = 'isAdmin=1; path=/';
```

## 4. 공격자 관점
1. 버튼 클릭 후 어떤 요청이 나가는지 봅니다.
2. 쿠키를 확인합니다.
3. `isAdmin=0` 같은 권한 플래그를 찾습니다.
4. 값을 `1`로 바꾸고 다시 요청합니다.
5. 서버가 클라이언트 값을 신뢰하는지 확인합니다.

## 5. 방어자 관점
- 권한은 쿠키의 숫자값 하나로 판단하지 않습니다.
- 세션은 서버에서 관리하고, 권한은 서버 저장소 기준으로 검증합니다.
- 관리 권한은 서명된 토큰이나 서버 세션으로만 판별합니다.
- 클라이언트 쿠키는 언제든 변조될 수 있다고 가정합니다.

## 6. 같이 보면 좋은 페이지
- [[cookie-client-storage-ctf-patterns]]
- [[web-ctf-writeup-auth-session]]
- [[broken-auth]]
- [[idor]]
- [[cookie-monster-secret-recipe-final-writeup]]

## 7. 참고 소스
- [Ahmed Narmer — Power Cookie](https://medium.com/@ahmednarmer1/ctf-day-27-1e6bb61eb835)
- [CTFtime — Power Cookie writeup](https://ctftime.org/writeup/32830)
- [Arvind Shima — power-cookie.md](https://github.com/arvindshima/PicoCTF-2022/blob/main/Web%20Exploitation/power-cookie.md)
- [wasi-master — power_cookie.md](https://github.com/wasi-master/picoCTF-2022/blob/main/web_exploitation/power_cookie.md)
