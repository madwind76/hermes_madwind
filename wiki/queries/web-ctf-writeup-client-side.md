---
title: Web CTF Writeup — 클라이언트 사이드/XSS/CSP
created: 2026-06-14
updated: 2026-06-14
type: query
tags: [ctf, web, research, writeup, xss, csp, client-side]
sources: [https://blog.hokyun.dev/posts/google-ctf-2024-quals-writeup/, https://blog.drstra.in/posts/assn-wu/, https://blog.s1r1us.ninja/CTF/IuseBing, https://blog.arkark.dev/2023/12/28/seccon-finals, raw/articles/20260613_web-ctf-writeup-curated.md]
confidence: high
---

# Web CTF Writeup — 클라이언트 사이드/XSS/CSP

> 브라우저 상태, CSP, nonce, window.name, JSONP, XS-Leak를 다루는 분류입니다.

## 1. 핵심 요약
- 이 분류는 **브라우저가 실제로 실행하는 것**과 **개발자가 안전하다고 믿은 것**의 차이를 다룹니다.
- `XSS` 자체보다 `CSP 우회`, `nonce leak`, `window.name`, `prototype pollution` 체인이 핵심인 경우가 많습니다.
- `web-inspector`, `csrf`, `cors-misconfig`, `xss`와 함께 읽으면 좋습니다.

연결 개념: [[xss]], [[csrf]], [[web-inspector-ctf-patterns]], [[websocket-message-tampering-ctf-patterns]], [[cors-misconfig]], [[ssrf-defense]], [[csp-bypass-ctf-patterns]]

## 2. 대표 writeup

|| 문제 | 출처 | 핵심 아이디어 |
||------|------|---------------|
| `Ancient History` | picoCTF 2021 | browser history back으로 이전 상태에서 flag 회수 |
| `Bookmarklet` | picoCTF 2024 | bookmarklet 실행, browser JavaScript execution |
| `WebDecode` | picoCTF 2024 | minified/hidden source에서 encoded flag 추출 |
| `Some Assembly Required 3` | picoCTF 2021 | WebAssembly 디컴파일과 XOR key 복원 |
| `Some Assembly Required 4` | picoCTF 2021 | WASM 변환 루틴 재현과 brute force |
|| [[elements-final-writeup]] | picoCTF 2024 | XSS + CSP bypass + server-side bot, timing side-channel |
|| [[websockfish-final-writeup]] | picoCTF 2025 | WebSocket `eval` 메시지 변조로 fish 항복 유도 |
|| `sappy` | Google CTF 2024 Quals | host 검증 우회 후 메시지 기반 렌더링 조작 |
|| `Another secure store note` | LINE CTF 2023 | CSRF + nonce leak + CSP bypass |
|| `ALL THE LITTLE THINGS` | Google CTF 2020 | prototype pollution + `window.name` + JSONP |
|| `babywaf` | SECCON 2023 Finals | WAF와 JSON 파싱 차이로 우회 |
|| `cgi-2023` | SECCON 2023 Finals | XS-Leak와 SRI를 이용한 오라클 구성 |

## 3. 자주 보이는 패턴
1. `postMessage` 또는 `window.name`에 상태를 저장함
2. `document.domain`, `iframe`, `nonce`가 공격면이 됨
3. CSP가 엄격하지만 nonce/리포트 채널이 존재함
4. 브라우저와 서버의 파서 차이로 `JSON.parse` 오라클이 생김
5. 이미지, 스타일, 리소스 로드가 정보 누출 통로가 됨
6. WebSocket 메시지의 상태값·점수·명령이 서버 로직에 영향을 줌

## 4. 읽을 때 확인할 것
- CSP가 어떤 소스를 허용하는지
- nonce가 어디서 생성되고 언제 고정되는지
- 프레임/팝업/리다이렉트가 같은 origin으로 유지되는지
- `window.name`, `localStorage`, 쿠키가 어떤 시점에 읽히는지

## 5. 방어 관점
- CSP는 `base-uri`, `object-src`, `frame-ancestors`까지 함께 봐야 합니다.
- origin 검증은 문자열 비교보다 URL 파서 결과를 기준으로 해야 합니다.
- 클라이언트 상태를 신뢰 경계로 쓰지 않습니다.
- `postMessage` 수신자는 origin 체크를 엄격히 해야 합니다.

## 6. 추천 다음 읽기
- [[xss]]
- [[csrf]]
- [[web-inspector-ctf-patterns]]
- [[source-inspection-minification-ctf-patterns]]
- [[websocket-message-tampering-ctf-patterns]]
- [[web-ctf-master-checklist]]
