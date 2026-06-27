---
title: Elements — picoCTF 2024 web writeup
created: 2026-06-15
updated: 2026-06-21
type: query
tags: [ctf, web, xss, csp, client-side, picoctf]
sources: [https://www.justinsteven.com/posts/2024/04/02/picoctf-2024-elements-csp-bypass/, https://blog.jettchen.me/posts/elements/, https://blog.qz.sg/picoctf-2024-web-exploitation-writeups/, https://infosecwriteups.com/picoctf-2024-write-up-web-992348f48b99]
confidence: high
---

# Elements — picoCTF 2024 web writeup

> `Elements`는 **XSS + CSP bypass + server-side bot interaction**이 결합된 picoCTF 2024 Web 문제입니다. 단순히 스크립트를 실행하는 것보다, 브라우저 정책과 봇의 동작을 함께 이해해야 합니다.

## 참고 URL
- [www.justinsteven.com](https://www.justinsteven.com/posts/2024/04/02/picoctf-2024-elements-csp-bypass/)
- [blog.jettchen.me](https://blog.jettchen.me/posts/elements/)
- [blog.qz.sg](https://blog.qz.sg/picoctf-2024-web-exploitation-writeups/)
- [infosecwriteups.com](https://infosecwriteups.com/picoctf-2024-write-up-web-992348f48b99)


## 1. 한 줄 요약
- 게임 상태는 URL fragment에서 복원됩니다.
- 특정 조합으로 `XSS` 요소를 만들면 `state.xss`가 실행됩니다.
- 서버 측 Chromium bot이 공격자가 구성한 상태를 방문합니다.
- CSP가 매우 빡빡해서 일반적인 외부 exfiltration이 막힙니다.
- 공개 writeup에서는 `PendingBeacon/fetchLater` 계열 우회 또는 **timing side-channel** 기반 풀이가 소개됩니다.

## 2. 문제 흐름
| 단계 | 관찰 | 의미 |
|------|------|------|
| 1 | 드래그앤드롭형 element 조합 게임 | 브라우저 상태 조작 가능 |
| 2 | URL fragment가 base64 JSON으로 파싱됨 | 상태 주입 가능 |
| 3 | `XSS`를 만들면 `eval(state.xss)`가 호출됨 | 공격자 JS 실행 가능 |
| 4 | server-side Chrome bot이 같은 상태를 방문 | bot 대상 공격 가능 |
| 5 | CSP와 브라우저 정책이 강함 | 직접 exfiltration 곤란 |
| 6 | 대안 채널 또는 timing side-channel 필요 | 우회 풀이 핵심 |

## 3. 핵심 분석
### 3.1 XSS 트리거
`Elements`의 중요한 점은 단순한 DOM XSS가 아니라, **특정 제작 순서에서만 `XSS`가 생성되고 그때만 `state.xss`가 실행**된다는 점입니다. 즉, 입력 한 번으로 끝나는 문제가 아니라 **제작 순서와 상태 복원**을 같이 봐야 합니다.

### 3.2 CSP 우회
공개 writeup에서는 두 가지 축이 보입니다.
- **Experimental beacon 계열**: `PendingBeacon`/`fetchLater`처럼 CSP 제한을 덜 받는 전송 메커니즘 활용
- **Timing side-channel**: 직접 플래그를 밖으로 보내기 어렵다면, 서버 부하나 응답 시간 차이를 이용해 정보를 복원

### 3.3 봇 환경
서버 측 Chromium bot은 네트워크, URL 이동, 일부 웹 API가 제한됩니다. 따라서 일반적인 `fetch()` 기반 exfiltration보다 **브라우저 정책을 읽고 우회 채널을 찾는 것**이 더 중요합니다.

## 4. 공격자 관점
1. 상태 복원 로직을 분석합니다.
2. `XSS`가 생성되는 조합을 찾습니다.
3. `state.xss`가 실행되는 순간을 이용합니다.
4. CSP가 막는 채널과 허용되는 채널을 구분합니다.
5. 직접 exfil이 안 되면 timing side-channel 같은 간접 채널을 찾습니다.

## 5. 방어자 관점
- CSP는 강하지만, 실질적으로는 **브라우저 정책 + 봇 실행 모델 + 상태 주입 구조**를 함께 봐야 합니다.
- `eval()`은 가능한 피해야 합니다.
- fragment/JSON 상태를 직접 신뢰하면 안 됩니다.
- 봇이 사용자 입력을 렌더링하는 경우, 네트워크 제어와 격리를 더 강화해야 합니다.

## 6. 같이 보면 좋은 페이지
- [[web-ctf-writeup-client-side]]
- [[xss]]
- [[csp-bypass-ctf-patterns]]
- [[web-inspector-ctf-patterns]]
- [[web-ctf-writeup-topic-map]]

## 7. 참고 소스
- [Justin Steven — picoCTF 2024 Elements (Web, CSP Bypass)](https://www.justinsteven.com/posts/2024/04/02/picoctf-2024-elements-csp-bypass/)
- [Jett’s blog — PicoCTF 2024 Elements Writeup](https://blog.jettchen.me/posts/elements/)
- [PicoCTF 2024 Web Exploitation Writeups](https://blog.qz.sg/picoctf-2024-web-exploitation-writeups/)
- [InfoSec Write-ups — picoCTF 2024 Web write-up](https://infosecwriteups.com/picoctf-2024-write-up-web-992348f48b99)
