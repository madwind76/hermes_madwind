---
title: Web CTF Writeup 큐레이션
created: 2026-06-14
updated: 2026-06-14
type: query
tags: [ctf, web, research, writeup]
sources: [https://blog.hokyun.dev/posts/csaw-ctf-2024-quals-writeup/, https://blog.hokyun.dev/posts/google-ctf-2024-quals-writeup/, https://blog.arkark.dev/2023/12/28/seccon-finals, https://blog.drstra.in/posts/assn-wu/, https://blog.s1r1us.ninja/CTF/IuseBing, https://github.com/ernw/ctf-writeups/blob/master/csaw2016/mfw/README.md, raw/articles/20260613_web-ctf-writeup-curated.md]
confidence: high
---

# Web CTF Writeup 큐레이션

> 공개 writeup을 바탕으로 재구성한 Web CTF 학습용 요약 페이지입니다.
> 상위 지도: [[web-ctf-writeup-topic-map]]

## 1. 빠른 결론

- Web CTF writeup은 단일 취약점보다 **체인 구조**를 읽는 연습에 좋습니다.
- 최근 writeup은 `XSS` 하나로 끝나기보다 `CSP`, `parser differential`, `client-side state`, `internal service chain`을 엮는 경우가 많습니다.
- 입문은 `PortSwigger Web Security Academy`와 기존 개념 페이지를 먼저 보고, 그다음 공개 writeup으로 넘어가면 효율이 좋습니다.

연결 개념:
[[web-ctf-writeup-resources]], [[web-ctf-master-checklist]], [[xss]], [[ssrf]], [[ssti]], [[csrf]], [[broken-auth]], [[file-upload]], [[path-traversal]], [[command-injection]], [[cookie-client-storage-ctf-patterns]], [[browser-identity-header-spoofing-ctf-patterns]], [[sqlite-sqli-filter-bypass-ctf-patterns]]

## 2. 취약점 유형별 세부 분류

- [[web-ctf-writeup-auth-session]] — 인증/세션/권한
- [[web-ctf-writeup-client-side]] — 클라이언트 사이드/XSS/CSP
- [[web-ctf-writeup-parser-template]] — 파서/템플릿/검증기 우회
- [[web-ctf-writeup-storage-upload]] — 파일 업로드/스토리지/클라우드
- [[web-ctf-writeup-internal-service]] — 내부 서비스/프로토콜 악용
- [[browser-identity-header-spoofing-ctf-patterns]] — 헤더/브라우저 식별 스푸핑
- [[cbc-bit-flipping-ctf-patterns]] — 암호화 쿠키/토큰 변조

## 3. 추천 읽기 순서

1. **mfw** — 소스 노출 + `assert()` 기반 RCE
2. **log me in** — 토큰 XOR 복원 + 세션 위조
3. **sappy / grand prix heaven** — host validation 우회, 템플릿 주입
4. **babywaf / cgi-2023** — WAF 우회, XS-Leak, SRI
5. **X marks the spot** — blind XPath injection, login bypass
6. **Super Serial** — PHP unserialize object injection
7. **Another secure store note** — CSRF + CSP + nonce leak
8. **ALL THE LITTLE THINGS** — prototype pollution + `window.name` + CSP bypass

## 4. 큐레이션 표

| 출처 | 대표 챌린지 | 핵심 패턴 | 왜 읽을 가치가 있는가 |
|------|-------------|-----------|------------------------|
| [CSAW CTF 2024 Quals Writeup](https://blog.hokyun.dev/posts/csaw-ctf-2024-quals-writeup/) | `log me in`, `bucketwars`, `charlies angels` | 인증 토큰 위조, S3 버전 노출, multipart 업로드 체인 | 최근 Web 문제의 전형적인 체인형 사고를 잘 보여줍니다. |
| [Google CTF 2024 Quals Writeup](https://blog.hokyun.dev/posts/google-ctf-2024-quals-writeup/) | `onlyecho`, `sappy`, `grand prix heaven` | bash parser bypass, host validation 우회, template injection | 파서/검증기 차이를 이용하는 고난도 문제를 한 번에 볼 수 있습니다. |
| [CTF Day(27) — Power Cookie](https://medium.com/@ahmednarmer1/ctf-day-27-1e6bb61eb835) | `Power Cookie` | cookie tampering, `isAdmin` 변조 | 쿠키가 권한 판단에 직접 연결될 때의 위험을 빠르게 보여줍니다. |
| [CTFtime — Super Serial](https://ctftime.org/writeup/27159) | `Super Serial` | PHP unserialize, object injection | 역직렬화 취약점과 gadget chain의 기본 흐름을 보기 좋습니다. |
| [CTFtime — X marks the spot](https://ctftime.org/writeup/27158) | `X marks the spot` | blind XPath injection, login bypass | XML/XPath 기반 인증 로직의 우회를 볼 수 있습니다. |
| [CTF Day(41) — Who are you?](https://medium.com/@ahmednarmer1/ctf-day-41-fe36ae3311b0) | `Who are you?` | header spoofing, browser identity checks | 서버가 헤더를 신뢰할 때 어떤 우회가 가능한지 한 번에 볼 수 있습니다. |
| [More Cookies — picoCTF 2021](https://github.com/HHousen/PicoCTF-2021/blob/master/Web%20Exploitation/More%20Cookies/README.md) | `More Cookies` | CBC bit flipping, encrypted cookie tampering | 암호화된 쿠키도 무결성 없으면 변조될 수 있음을 보여줍니다. |
| [Web Gauntlet — picoCTF 2020](https://github.com/onealmond/hacking-lab/blob/master/picoctf-2020/web-gauntlet/writeup.md) | `Web Gauntlet` | SQLite SQLi, filter bypass | Web Gauntlet 2/3의 원형이라 함께 읽기 좋습니다. |
| [Web Gauntlet 2 — picoCTF 2021](https://github.com/Dvd848/CTFs/blob/master/2021_picoCTF/Web_Gauntlet_2.md) | `Web Gauntlet 2` | SQLite SQLi, keyword filter bypass | SQLite 전용 연산자와 짧은 payload의 조합을 읽기 좋습니다. |
| [No SQL Injection — picoCTF 2024](https://github.com/noamgariani11/picoCTF-2024-Writeup/blob/main/Web%20Exploitation/No-Sql-Injection.md) | `No SQL Injection` | MongoDB NoSQL injection, login bypass | JSON 객체 주입으로 인증이 깨지는 전형적인 NoSQL 문제입니다. |
| [Elements — picoCTF 2024](https://www.justinsteven.com/posts/2024/04/02/picoctf-2024-elements-csp-bypass/) | `Elements` | XSS, CSP bypass, timing side-channel | 브라우저 정책과 봇 환경을 함께 읽는 고난도 문제입니다. |
| [LINE CTF 2023 — Another secure store note](https://blog.drstra.in/posts/assn-wu/) | `Another secure store note` | CSRF, CSP, nonce leak, XSS 체인 | 브라우저 상태와 CSP를 엮는 실전형 클라이언트 사이드 문제입니다. |
| [Google CTF 2020 — ALL THE LITTLE THINGS](https://blog.s1r1us.ninja/CTF/IuseBing) | `ALL THE LITTLE THINGS` | prototype pollution, `window.name`, JSONP, CSP bypass | 클라이언트 사이드 취약점이 어떻게 체인으로 이어지는지 잘 드러납니다. |
| [ERNW ctf-writeups — mfw](https://github.com/ernw/ctf-writeups/blob/master/csaw2016/mfw/README.md) | `mfw` | source exposure, `assert()` injection, RCE | 오래된 문제지만 소스 분석과 코드 인젝션의 교과서적 예시입니다. |

## 5. 패턴별로 묶어 읽기

### A. 인증/세션 변조
- `log me in`
- `mfw`
- `Power Cookie`
- `Cookies`
- `More Cookies`
- `Most Cookies`
- `Java Code Analysis!?!`
- `JAuth`
- 관련 개념: [[broken-auth]], [[parameter-tampering-ctf-patterns]], [[cookie-client-storage-ctf-patterns]], [[cbc-bit-flipping-ctf-patterns]], [[jwt-secret-exposure-ctf-patterns]], [[flask-signed-session-cookie-ctf-patterns]]

### B. 클라이언트 사이드 체인
- `Ancient History`
- `Bookmarklet`
- `WebDecode`
- `Some Assembly Required 1`
- `Some Assembly Required 2`
- `Some Assembly Required 3`
- `Some Assembly Required 4`
- `Another secure store note`
- `ALL THE LITTLE THINGS`
- 관련 개념: [[xss]], [[csrf]], [[web-inspector-ctf-patterns]], [[websocket-message-tampering-ctf-patterns]], [[cors-misconfig]], [[ssrf-defense]], [[csp-bypass-ctf-patterns]], [[browser-history-manipulation-ctf-patterns]]

### C. 내부 서비스 및 프로토콜 악용
- `charlies angels`
- `bucketwars`
- 관련 개념: [[ssrf]], [[file-upload]], [[redis-ssrf-command-injection-ctf-patterns]]

### D. 헤더/브라우저 식별 스푸핑
- `Who are you?`
- 관련 개념: [[browser-identity-header-spoofing-ctf-patterns]], [[http]], [[burp-suite]]

### E. 방어 기법 우회
- `babywaf`
- `DOMLeakify`
- 관련 개념: [[xss]], [[ssrf]], [[ssrf-defense]], [[ssti-defense]]

### F. SQLi / 필터 우회
- `Web Gauntlet`
- `Web Gauntlet 2`
- `Web Gauntlet 3`
- `Startup Compagny`
- `Web Gauntlet 2/3 survey`
- `More SQLi`
- 관련 개념: [[sql-injection]], [[sqlite-sqli-filter-bypass-ctf-patterns]], [[sqlite-union-based-sqli-ctf-patterns]], [[parameter-tampering-ctf-patterns]]

## 6. 학습 포인트

- **검증 로직과 실제 처리 로직이 같은지** 먼저 봅니다.
- **브라우저/서버/프록시가 각각 무엇을 믿는지** 분리해서 봅니다.
- **정상 경로와 예외 경로가 다른 파서를 타는지** 확인합니다.
- **클라이언트 상태(localStorage, window.name, nonce, 쿠키)** 가 공격면이 되는지 봅니다.
- **내부 서비스가 외부 입력으로 간접 제어되는지** 확인합니다.

## 7. 같이 보면 좋은 위키

- [[web-ctf-writeup-resources]] — 공개 writeup 리소스 가이드
- [[web-ctf-master-checklist]] — Web CTF 범용 체크리스트
- [[prompt-injection-ctf]] — 다른 유형의 CTF 분류 참고
- [[agent-security-ctf]] — 웹 외 챌린지 분류 참고

## 8. 개별 실전 노트

유형별 허브에서 바로 내려가 읽기 좋은 노트들입니다.

### picoCTF 2025 묶음
- [[picoctf-2025-web-exploitation-survey]]
- [[3v-l-final-writeup]]
- [[apriti-sesamo-final-writeup]]
- [[pachinko-final-writeup]]
- [[secure-email-service-final-writeup]]
- [[cookie-monster-secret-recipe-final-writeup]]
- [[head-dump-final-writeup]]
- [[n0s4n1ty-1-final-writeup]]
- [[ssti1-final-writeup]]
- [[ssti2-final-writeup]]
- [[websockfish-final-writeup]]

### 인증/세션/권한
- [[cookie-monster-secret-recipe-final-writeup]]
- [[intro-to-burp-final-writeup]]
- [[urlapp-final-writeup]]
- [[bbs-final-writeup]]
- [[web-ctf-starter]]

### 클라이언트 사이드
- [[get-ahead-final-writeup]]
- [[websockfish-final-writeup]]
- [[bookmarklet-final-writeup]]
- [[includes-final-writeup]]
- [[webdecode-final-writeup]]
- [[local-authority-final-writeup]]
- [[secrets-final-writeup]]
- [[csaw-2020-webrtc-final-writeup]]

### 파서/템플릿/검증기 우회
- [[ssti1-final-writeup]]
- [[ssti2-final-writeup]]
- [[under-construction-final-writeup]]
- [[gcalc-final-writeup]]
- [[soap-final-writeup]]

### 파일 업로드/스토리지
- [[boomshop-final-writeup]]
- [[one-line-php-challenge-final-writeup]]
- [[trickster-final-writeup]]

### 내부 서비스/프로토콜
- [[bithug-final-writeup]]
- [[head-dump-final-writeup]]
- [[csaw-2020-webrtc-final-writeup]]
- [[sourceless-final-writeup]]

### 정찰/숨은 파일
- [[web-recon-hidden-file-discovery-ctf-hub]]
- [[search-source-final-writeup]]
- [[where-are-the-robots-final-writeup]]
- [[roboto-sans-final-writeup]]
- [[scavenger-hunt-final-writeup]]
