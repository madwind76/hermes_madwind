---
title: Web CTF Writeup Topic Map
created: 2026-06-14
updated: 2026-06-14
type: concept
tags: [web, ctf, research, reference]
sources: [raw/articles/20260613_web-ctf-writeup-curated.md, /home/kisec/wiki/index.md]
confidence: high
---

# Web CTF Writeup Topic Map

> 현재 wiki에 축적된 Web CTF writeup 정보를 **주제별로 재배열한 상위 지도**입니다.
> 목적은 개별 writeup을 찾는 것이 아니라, 어떤 문제를 어떤 분류로 읽어야 하는지 빠르게 잡는 것입니다.

## 1. 현재 wiki의 구조 요약

현재 Web CTF 자료는 크게 세 층으로 정리되어 있습니다.

1. **리소스/가이드 층**
   - [[web-ctf-writeup-resources]]: 외부 writeup 소스와 학습 로드맵
   - [[web-ctf-writeup-curation]]: 공개 writeup을 다시 묶은 큐레이션 허브

2. **유형별 분류 층**
   - [[web-ctf-writeup-auth-session]]: 인증 / 세션 / 권한
   - [[web-ctf-writeup-client-side]]: 클라이언트 사이드 / XSS / CSP
- [[source-inspection-minification-ctf-patterns]]: source inspection / minification
   - [[web-ctf-writeup-parser-template]]: 파서 / 템플릿 / 검증기 우회
   - [[web-ctf-writeup-storage-upload]]: 파일 업로드 / 스토리지 / 클라우드
   - [[web-ctf-writeup-internal-service]]: 내부 서비스 / 프로토콜 악용

3. **문제별 실전 노트 층**
   - `urlapp`, `bbs`, `gcalc`, `sourceless`, `under-construction` 같은 개별 writeup 페이지
   - 체크리스트: [[web-ctf-master-checklist]]

## 2. 재정리 기준

현재 분류는 다음 기준으로 나누는 편이 가장 유지보수성이 좋습니다.

- **문제의 진입점**이 어디인지
- **실패 원인**이 검증 실패인지, 파서 차이인지, 권한 누락인지
- **브라우저 상태**를 다루는지, **서버 내부 요청**을 다루는지
- **후처리 파이프라인**(업로드, 변환, 백업)이 있는지

이 기준으로 보면 Web CTF writeup은 단순 취약점 목록이 아니라, **공격면이 어디서 시작되고 어디서 이어지는지**를 보여주는 네트워크처럼 읽는 것이 좋습니다.

## 3. 분류별 읽기 경로

### A. 인증/세션/권한
가장 먼저 읽으면 좋은 분류입니다. 토큰 구조, uid 변조, IDOR, 접근 제어 누락이 여기에 들어갑니다.

- [[web-ctf-writeup-auth-session]]
- [[no-sql-injection-final-writeup]]
- [[java-code-analysis-final-writeup]]
- [[jauth-final-writeup]]
- 관련 개념: [[broken-auth]], [[idor]], [[broken-access-control]], [[cookie-client-storage-ctf-patterns]], [[nosql-injection-ctf-patterns]], [[jwt-secret-exposure-ctf-patterns]]

### B. 클라이언트 사이드 체인
브라우저 상태, nonce, CSP, window.name, JSONP가 얽히는 문제입니다.

- [[elements-final-writeup]]
- [[websockfish-final-writeup]]
- [[web-ctf-writeup-client-side]]
- 관련 개념: [[xss]], [[csrf]], [[web-inspector-ctf-patterns]], [[cors-misconfig]], [[csp-bypass-ctf-patterns]]

### C. 파서/템플릿/검증기 우회
같은 입력이 다른 계층에서 다르게 해석되는 문제입니다. 문자열 조합, `assert`, multipart, 템플릿 렌더링이 자주 나옵니다.

- [[web-ctf-writeup-parser-template]]
- 관련 개념: [[ssti]], [[command-injection]], [[path-traversal]], [[xpath-injection-ctf-patterns]]

### D. 파일 업로드/스토리지/클라우드
업로드 자체보다 저장, 버전, 변환, 백업, 다운로드 경로가 더 중요합니다.

- [[web-ctf-writeup-storage-upload]]
- 관련 개념: [[file-upload]], [[ssrf]], [[idor]]

### E. 헤더/브라우저 식별 스푸핑
브라우저 정체성, 지역, 언어, 추적 헤더를 바꿔서 접근 제어를 통과하는 문제입니다.

- [[browser-identity-header-spoofing-ctf-patterns]]
- 관련 개념: [[http]], [[burp-suite]], [[web-ctf-writeup-auth-session]]

### F. 암호화 쿠키/토큰 변조
암호화된 클라이언트 상태를 비트 플리핑이나 서명 우회로 건드리는 문제입니다.

- [[cbc-bit-flipping-ctf-patterns]]
- 관련 개념: [[cookie-client-storage-ctf-patterns]], [[base64-decoding-ctf-patterns]]

### G. 내부 서비스 및 프로토콜 악용
서버가 내부로 대신 요청을 보내는 구조입니다. SSRF, admin bot, Redis, TURN, gopher, signed email rendering sink, Git webhook routing이 여기에 들어갑니다.

- [[web-ctf-writeup-internal-service]]
- [[bithug-final-writeup]]
- 관련 개념: [[ssrf]], [[redis-ssrf-command-injection-ctf-patterns]], [[webrtc-turn-proxying-ctf-patterns]], [[signed-html-email-ctf-patterns]]

### H. SQLi / 필터 우회
SQLite 같은 DBMS 차이와 블랙리스트 필터 우회를 함께 읽는 분류입니다.

- [[web-gauntlet-2-3-sqlite-survey]]
- [[web-gauntlet-2-final-writeup]]
- [[web-gauntlet-3-final-writeup]]
- [[startup-compagny-final-writeup]]
- [[more-sqli-final-writeup]]
- 관련 개념: [[sql-injection]], [[sqlite-sqli-filter-bypass-ctf-patterns]], [[sqlite-union-based-sqli-ctf-patterns]], [[parameter-tampering-ctf-patterns]]

## 4. 현재 wiki에서 보이는 강점

1. **개념 페이지와 실전 노트의 연결이 좋습니다.**
   - `[[xss]]`, `[[ssrf]]`, `[[ssti]]` 같은 개념 페이지가 이미 있어 writeup을 읽은 뒤 개념 복습이 쉽습니다.

2. **새로 만든 query 페이지가 분류별로 자연스럽습니다.**
   - writeup 큐레이션이 이제 한 장에 뭉치지 않고, 분류별로 바로 들어갈 수 있습니다.

3. **체크리스트가 존재해서 재사용성이 높습니다.**
   - [[web-ctf-master-checklist]]를 기준으로 각 writeup을 같은 프레임으로 읽을 수 있습니다.

## 5. 보완하면 더 좋은 부분

1. **개별 writeup 페이지를 유형별 허브와 더 강하게 연결하기**
   - 예: `urlapp-final-writeup` → [[web-ctf-writeup-internal-service]]
   - 예: `intro-to-burp-final-writeup` → [[web-ctf-writeup-auth-session]] 또는 [[web-ctf-writeup-parser-template]]

2. **대회별 묶음 페이지와 유형별 묶음 페이지를 분리하기**
   - 대회별: CSAW, Google CTF, SECCON
   - 유형별: 인증, 클라이언트 사이드, 파서 우회, 업로드, 내부 서비스

3. **고난도 페이지는 하위 page로 더 쪼개기**
   - 예: `client-side` 아래에 `csp`, `xs-leak`, `window-name`, `csp-bypass` 같은 세부 페이지를 둘 수 있습니다.

## 6. 추천 탐색 순서

1. [[web-ctf-writeup-resources]]
2. [[web-ctf-writeup-curation]]
3. [[web-ctf-writeup-auth-session]]
4. [[web-ctf-writeup-client-side]]
5. [[web-ctf-writeup-parser-template]]
6. [[web-ctf-writeup-storage-upload]]
7. [[web-ctf-writeup-internal-service]]
8. [[web-ctf-master-checklist]]

## 7. 개별 실전 노트로 내려가는 경로

유형 허브에서 실제 풀이 노트로 내려갈 때는 아래 페이지를 함께 보면 좋습니다.

- 인증/세션/권한: [[intro-to-burp-final-writeup]], [[urlapp-final-writeup]], [[bbs-final-writeup]], [[cookies-final-writeup]], [[most-cookies-final-writeup]], [[super-serial-final-writeup]]
- 클라이언트 사이드: [[bookmarklet-final-writeup]], [[bookmarklet-execution-ctf-patterns]], [[webdecode-final-writeup]], [[csaw-2020-webrtc-final-writeup]], [[some-assembly-required-1-final-writeup]], [[some-assembly-required-2-final-writeup]], [[some-assembly-required-3-final-writeup]], [[some-assembly-required-4-final-writeup]], [[ancient-history-final-writeup]]
- 파서/템플릿/검증기 우회: [[under-construction-final-writeup]], [[gcalc-final-writeup]], [[soap-final-writeup]], [[x-marks-the-spot-final-writeup]]
- 파일 업로드/스토리지: [[boomshop-final-writeup]], [[one-line-php-challenge-final-writeup]], [[it-is-my-birthday-final-writeup]]
- 내부 서비스/프로토콜: [[csaw-2020-webrtc-final-writeup]], [[sourceless-final-writeup]], [[secure-email-service-final-writeup]]
- 정찰/숨은 파일: [[web-recon-hidden-file-discovery-ctf-hub]], [[where-are-the-robots-final-writeup]], [[roboto-sans-final-writeup]], [[scavenger-hunt-final-writeup]], [[secrets-final-writeup]]

## 8. 결론

현재 wiki는 이미 **리소스 → 큐레이션 → 유형별 분류 → 개별 writeup**의 흐름을 갖추고 있습니다.
다음 단계는 개별 writeup 페이지를 해당 유형 허브에 더 촘촘히 연결해서, "문제 하나를 읽으면 관련 개념과 다른 writeup이 자동으로 따라오는 구조"로 만드는 것입니다.

## 9. 기존 개별 노트 묶음

아래 페이지들은 현재 wiki에 이미 존재하는 개별 writeup/템플릿 노트들입니다. topic map에서 한 번 더 묶어 두면 탐색이 편해집니다.

- [[ssti-ctf-patterns]]
- [[log4j]]
- [[vulpixelize-final-writeup]]
- [[command-injection-ctf-template]]
- [[n0s4n1ty-1-final-writeup]]
- [[idor-ctf-template]]
- [[under-construction]]
- [[gcalc]]
- [[ssrf-ctf-template]]
- [[bookmarklet-final-writeup]]
- [[one-line-php-challenge]]
- [[bbs]]
- [[path-traversal-ctf-patterns]]
- [[path-traversal-ctf-template]]
- [[boomshop-example]]
- [[game-arcade-final-writeup]]
- [[file-upload-ctf-template]]
- [[postviewer-v5-final-writeup]]
- [[log4j-final-writeup]]


- [[search-source-final-writeup]] — Search Source — picoCTF 2022 web writeup
- [[includes-final-writeup]] — Includes — picoCTF 2022 web writeup
- [[get-ahead-final-writeup]] — GET aHEAD — picoCTF web writeup
- [[web-gauntlet-final-writeup]] — Web Gauntlet — picoCTF 2020 web writeup
- [[web-gauntlet-2-final-writeup]] — Web Gauntlet 2 — picoCTF 2021 web writeup

## 10. picoCTF 2025 묶음

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

- [[trickster-final-writeup]] — Trickster — picoCTF 2024 web writeup

- [[unminify-final-writeup]] — Unminify — picoCTF 2024 web writeup
- [[where-are-the-robots-final-writeup]] — Where Are the Robots? — picoCTF web writeup
- [[roboto-sans-final-writeup]] — Roboto Sans — picoCTF web writeup
- [[scavenger-hunt-final-writeup]] — Scavenger Hunt — picoCTF web writeup
