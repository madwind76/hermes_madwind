---
title: DOM XSS writeup survey
created: 2026-06-19
updated: 2026-06-21
type: query
tags: [ctf, web, xss, client-side, browser, survey, writeup]
sources: [https://github.com/xpinked/ctf-writeups/blob/master/noxCTF18/Web/HiddenDOM/Solution.md, https://github.com/aszx87410/ctf-writeups/issues/39, https://github.com/aszx87410/ctf-writeups/issues/49, https://github.com/Crypto-Cat/CTF/blob/main/web/WebSecurityAcademy/xss/dom_xss_jquery_hashchange/writeup.md]
confidence: high
---

# DOM XSS writeup survey

> 공개 writeup 4개를 비교해서, **클라이언트 사이드 입력 → source/sink → DOM 실행**으로 이어지는 공통 메커니즘을 정리한 수집 노트입니다.
> 이 페이지의 목적은 단순히 문제를 나열하는 것이 아니라, 반복되는 DOM XSS 패턴을 `concept` 페이지와 연결하는 것입니다.

## 참고 URL
- [Original writeup](https://github.com/xpinked/ctf-writeups/blob/master/noxCTF18/Web/HiddenDOM/Solution.md)
- [aszx87410/ctf-writeups](https://github.com/aszx87410/ctf-writeups/issues/39)
- [aszx87410/ctf-writeups](https://github.com/aszx87410/ctf-writeups/issues/49)
- [Original writeup](https://github.com/Crypto-Cat/CTF/blob/main/web/WebSecurityAcademy/xss/dom_xss_jquery_hashchange/writeup.md)


## 1. 수집 범위
이번 수집은 GitHub 공개 writeup 중에서 다음 키워드가 겹치는 항목을 중심으로 골랐습니다.

- `DOM XSS`
- `HiddenDOM`
- `hashchange`
- `postMessage`
- `DOM clobbering`
- `CSP bypass`

## 2. 비교 표

| Writeup | 핵심 source | 핵심 sink / 실행 지점 | 대표 트릭 | 재사용 포인트 |
|---|---|---|---|---|
| HiddenDOM (noxCTF18) | `target`, `expression` GET 파라미터 | JS가 읽은 원격 컨텐츠를 regex로 필터링 후 출력 | 소스 코드 정독, obfuscated JS 해독, regex 교체 | `source-inspection-minification-ctf-patterns`, `web-inspector-ctf-patterns` |
| Intigriti 0721 XSS | `postMessage`, DOM 상태, iframe 구조 | `innerHTML`, `eval`, `srcdoc` 조합 | DOM clobbering + postMessage + CSP 우회 | `xss`, `csp-bypass-ctf-patterns` |
| Intigriti 0222 XSS | URL query + fragment | `innerHTML` sink | 24자 제한, `var` 전역 재사용, URL parsing quirk | `xss`, `browser-history-manipulation-ctf-patterns` |
| DOM XSS in jQuery selector sink using hashchange | `location.hash` | jQuery selector sink (`$()`), `scrollIntoView()` | `hashchange` 이벤트 트리거, iframe onload chain | `xss`, `web-inspector-ctf-patterns` |

## 3. 개별 writeup에서 반복되는 primitive

### 3.1 클라이언트 사이드 소스 분석
- `HiddenDOM`은 아예 **JavaScript를 읽어야만** 입력점(`target`, `expression`)이 보입니다.
- 이 계열은 보기 좋은 UI보다 **페이지 소스, 디버거, 콘솔 값**이 먼저입니다.

### 3.2 DOM clobbering / postMessage 체인
- `Intigriti 0721`은 단일 payload보다 **iframe 구조와 window 간 메시지 흐름**이 중요합니다.
- 브라우저가 신뢰하는 전역 객체와 DOM 노드를 덮는 방식이 핵심입니다.

### 3.3 길이 제한과 URL parsing 우회
- `Intigriti 0222`는 짧은 payload 제약 아래서 **URL 디코딩 결과**와 `var` 전역 성질을 재활용합니다.
- 문자 수 제한이 있으면 문자열 길이를 줄이는 것보다 **이미 존재하는 전역 값**을 찾는 편이 효율적입니다.

### 3.4 fragment 기반 DOM XSS
- `hashchange` 기반 writeup은 서버가 아니라 **클라이언트 라우팅**이 문제입니다.
- `location.hash`는 `query`보다 덜 눈에 띄지만, 실제 sink로 들어가면 바로 위험해집니다.

## 4. 위키 연결 우선순위
이 survey는 아래 개념 페이지와 바로 연결하는 것이 적절합니다.

- [[xss]] — DOM XSS의 상위 개념
- [[csp-bypass-ctf-patterns]] — Intigriti 0721 같은 CSP 경로 우회
- [[web-inspector-ctf-patterns]] — 소스/디버거/DOM 추적
- [[source-inspection-minification-ctf-patterns]] — HiddenDOM처럼 코드가 먼저 단서가 되는 경우
- [[browser-history-manipulation-ctf-patterns]] — `hashchange` / URL fragment 계열

## 5. 자동 수집 메모
- 같은 `DOM XSS`라 해도 **source가 query냐 hash냐, sink가 innerHTML이냐 selector냐**에 따라 분류가 달라집니다.
- 이번 묶음은 모두 client-side지만, HiddenDOM처럼 사실상 **source inspection**에 가까운 문제도 섞여 있습니다.
- 따라서 다음 단계에서는 이 survey를 단일 XSS 개념 페이지보다 **클라이언트 사이드 공격면 지도**의 하위 노드로 쓰는 편이 좋습니다.

## 6. 참고 링크
- [HiddenDOM (noxCTF18)](https://github.com/xpinked/ctf-writeups/blob/master/noxCTF18/Web/HiddenDOM/Solution.md)
- [Intigriti 0721 XSS challenge writeup](https://github.com/aszx87410/ctf-writeups/issues/39)
- [Intigriti 0222 XSS challenge author writeup](https://github.com/aszx87410/ctf-writeups/issues/49)
- [DOM XSS in jQuery selector sink using a hashchange event](https://github.com/Crypto-Cat/CTF/blob/main/web/WebSecurityAcademy/xss/dom_xss_jquery_hashchange/writeup.md)
