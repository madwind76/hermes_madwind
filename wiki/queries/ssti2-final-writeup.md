---
title: SSTI2 — picoCTF 2025 web writeup
created: 2026-06-14
updated: 2026-06-14
type: query
tags: [ctf, web, writeup, ssti, template-injection, bypass, sandbox-escape, rce]
sources: [https://medium.com/@mihasha/ssti2-write-up-picoctf-2025-5fc53e2320ba, https://www.ehchris.com/blog/picoctf-ssti2-writeup, https://hackmd.io/@mv2XixOkQZyIZHzn48T8Tg/r1XtmrToge, https://medium.com/@kheyraldhs12/picoctf-2025-ssti2-a047c0c5887a, https://0day.work/jinja2-template-injection-filter-bypasses/, https://jinja.palletsprojects.com/en/stable/sandbox/, https://portswigger.net/web-security/server-side-template-injection, https://owasp.org/www-project-web-security-testing-guide/v41/4-Web_Application_Security_Testing/07-Input_Validation_Testing/18-Testing_for_Server_Side_Template_Injection]
confidence: high
---

# SSTI2 — picoCTF 2025 web writeup

> SSTI1보다 한 단계 더 나아가, 입력 필터가 붙은 Jinja2 SSTI를 `attr()`·hex escape·`__getitem__` 조합으로 우회해 서버에서 명령을 실행하는 picoCTF 2025 문제입니다.

## 1. 한 줄 요약

`SSTI2`는 Jinja2 SSTI가 확인된 뒤, `.` `__` `[]` `os` `popen` 같은 문자열이 차단된 상황에서 **필터 우회**로 내부 객체 경로를 복원해야 하는 문제입니다. 공개 writeup들은 `attr()` 필터, `_` hex escape, `__getitem__()` 재구성을 이용해 `os` 모듈에 도달한 뒤 flag를 읽는 흐름을 공유합니다.

## 2. 문제 메타데이터

| 항목 | 내용 |
|------|------|
| 플랫폼 | picoCTF 2025 |
| 카테고리 | Web Exploitation |
| 문제명 | SSTI2 |
| 핵심 취약점 | [[ssti|Server-Side Template Injection]] |
| 보조 기법 | [[jinja2-filter-bypass|Jinja2 Filter Bypass]] |
| 난이도 | Medium / 200 points로 공개 writeup들에서 언급 |
| 재사용 패턴 | SSTI 확인 → 필터 규칙 조사 → 우회 표현 조립 → 내부 객체 접근 → RCE → flag 읽기 |

## 3. 공격면

| 요소 | 관찰 |
|------|------|
| 입력 지점 | 공지 문구를 입력하는 단일 form field |
| 출력 지점 | 입력값이 서버 응답 페이지에 표시됨 |
| 추가 방어 | 점, 밑줄, 대괄호, 일부 키워드가 필터링됨 |
| 실제 핵심 | 템플릿 문법이 서버에서 평가되는 [[ssti]] |
| 우회 목표 | 필터를 피하면서도 Jinja2 내부 객체 그래프에 도달 |

## 4. 풀이 흐름

### 4.1 SSTI 여부 확인

공개 writeup들은 먼저 다음과 같은 산술식을 시험합니다.

```jinja2
{{7*7}}
```

또는:

```jinja2
{{7*'7'}}
```

이 값이 `49` 또는 `7777777` 식으로 평가되면, 입력이 서버에서 템플릿으로 해석되고 있음을 뜻합니다.

### 4.2 필터 규칙 파악

출처별로 차단된 문자열은 조금씩 다르지만, 공통적으로 아래 패턴이 등장합니다.

- `.`
- `_`
- `[]`
- `os`
- `popen`
- `class`
- `globals`
- `subclasses`

EhChris writeup은 이러한 블랙리스트와 출력 필터링까지 확인했다고 정리합니다. Mihasha writeup과 Kheyraldhs writeup은 `attr()`와 hex escape를 조합해 이를 우회합니다.

### 4.3 우회 경로 구성

가장 핵심적인 발상은 다음과 같습니다.

- 점 접근 대신 `attr()` 사용
- `_` 문자는 `_`로 위장
- 대괄호 접근 대신 `__getitem__()` 사용
- `request.application` 또는 `config`에서 출발해 `__globals__`로 이동

예시로 공개 writeup에서 반복되는 형태는 다음과 같습니다.

```jinja2
{{request|attr('application')|attr('__globals__')|attr('__getitem__')('__builtins__')|attr('__getitem__')('__import__')('os')|attr('popen')('ls')|attr('read')()}}
```

이 구조는 문법적으로는 여러 단계로 보이지만, 실제 의미는 다음과 같습니다.

1. Flask/Jinja2 컨텍스트의 `request`에 접근
2. `application`을 가져옴
3. `__globals__`에 접근
4. `__builtins__`를 꺼냄
5. `__import__`로 `os` 모듈을 로드
6. `popen()`으로 명령 실행
7. `read()`로 출력 회수

### 4.4 결과 획득

명령 실행이 가능해지면 `ls`로 파일을 확인하거나, `cat flag`로 flag 파일을 읽는 흐름으로 마무리합니다. 0day.work의 Jinja2 filter bypass 글은 이런 블랙리스트 우회가 SSTI/RCE 체인에서 얼마나 일반적인지 잘 보여 줍니다.

## 5. 핵심 개념 분리

이 문제에서 재사용 가능한 개념은 다음과 같습니다.

- [[jinja2-filter-bypass]] — 블랙리스트와 `attr()` 우회 패턴
- [[jinja2-template-engine]] — 이번 문제의 기반 엔진
- [[ssti]] — 서버 측 템플릿 주입
- [[rce]] — 최종 영향
- sandbox-escape — 내부 객체 체인으로 sandbox를 벗어나는 흐름

## 6. 방어 관점

1. 문자열 blacklist는 우회되기 쉽습니다.
2. 사용자 입력은 템플릿 원문과 분리해서 전달해야 합니다.
3. Jinja2의 `SandboxedEnvironment`와 allowlist를 적용합니다.
4. `request`/`config` 같은 강한 객체를 템플릿 컨텍스트에 과도하게 넣지 않습니다.
5. 서버 프로세스 권한을 최소화하고, 민감 파일은 웹 계정이 읽을 수 없게 분리합니다.

## 7. 동일 계열 문제 체크리스트

- [ ] 기본 산술 SSTI가 성립하는가?
- [ ] 필터가 차단하는 문자/키워드는 무엇인가?
- [ ] `attr()`로 대체 가능한가?
- [ ] `_` 같은 escape로 우회 가능한가?
- [ ] `__getitem__()`으로 `[]`를 대체 가능한가?
- [ ] 내부 객체에서 `__builtins__`까지 도달 가능한가?
- [ ] 최종적으로 RCE 또는 file read가 가능한가?

## 8. 출처별 교차 확인

| 출처 | 확인한 내용 |
|------|-------------|
| mihasha Medium | `attr()` + hex escape + `__getitem__` 조합, 필터 우회 흐름 |
| EhChris | 차단 문자/키워드 조사, 출력 필터링 관찰, Jinja2 escape 체인 |
| HackMD | `request.application.__globals__` 기반 체인과 `id`/flag 읽기 흐름 |
| Kheyraldhs Medium | Jinja2/Twig 식별, `_` 우회, `popen('ls')` 체인 |
| 0day.work | Jinja2 filter bypass의 일반 원리와 blacklist 한계 |
| PortSwigger / OWASP WSTG | SSTI 탐지·식별·익스플로잇 방법론과 방어 원칙 |

## 9. 관련 페이지

- [[web-ctf-writeup-parser-template]]
- [[web-ctf-writeup-curation]]
- [[ssti-ctf-patterns]]
- [[jinja2-filter-bypass]]
- [[ssti-defense]]
