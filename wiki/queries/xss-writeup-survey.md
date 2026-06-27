---
title: XSS writeup survey
created: 2026-06-19
updated: 2026-06-21
type: query
tags: [ctf, web, survey, writeup, xss, client-side, browser, csp]
sources: [https://github.com/xpinked/ctf-writeups/blob/master/noxCTF18/Web/HiddenDOM/Solution.md, https://github.com/Yahyahcini/hacker101-ctf-writeups/tree/main/BBS, https://github.com/noamgariani11/picoCTF-2024-Writeup/blob/main/Web%20Exploitation/SecureEmailService.md]
confidence: high
---

# XSS writeup survey

## 참고 URL
- [Original writeup](https://github.com/xpinked/ctf-writeups/blob/master/noxCTF18/Web/HiddenDOM/Solution.md)
- [Original writeup](https://github.com/Yahyahcini/hacker101-ctf-writeups/tree/main/BBS)
- [Original writeup](https://github.com/noamgariani11/picoCTF-2024-Writeup/blob/main/Web%20Exploitation/SecureEmailService.md)


## 1. 목적
DOM XSS, stored XSS, and 브라우저 sink 기반 writeup을 비교해, 클라이언트 측 실행이 어떻게 정보 탈취와 권한 우회로 이어지는지 정리합니다.

## 2. 비교 대상
| 문제 | 주된 primitive | 보조 primitive | 한 줄 요약 |
|---|---|---|---|
| HiddenDOM | DOM XSS | source inspection | 숨겨진 DOM sink를 찾아 script를 주입합니다. |
| BBS | avatar / report 기반 XSS | parameter tampering | avatar와 report 흐름을 악용해 admin 경로를 노립니다. |
| Secure Email Service | XSS + CSRF | broken auth | HTML email과 브라우저 sink가 함께 문제를 만듭니다. |

## 3. 공통 관찰
1. XSS는 단순 alert가 아니라 브라우저 내 권한을 훔치는 수단입니다.
2. DOM sink와 저장형 렌더링 sink는 공격 지점이 다르지만 결과는 비슷합니다.
3. CSP나 encoding만으로는 충분하지 않고, sink 자체를 제거하는 것이 핵심입니다.

## 4. 관련 개념
- [[xss]]
- [[csp-bypass-ctf-patterns]]
- [[web-ctf-writeup-client-side]]
- [[web-ctf-writeup-family-hub]]
- [[dom-xss-writeup-survey]]
- [[secure-email-service-final-writeup]]
- [[bbs-final-writeup]]

## 5. 다음 읽을 거리
- [[dom-xss-writeup-survey]]
- [[secure-email-service-final-writeup]]
- [[bbs-final-writeup]]
