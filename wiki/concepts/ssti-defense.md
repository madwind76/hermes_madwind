---
title: SSTI — 방어
created: 2026-06-12
updated: 2026-06-13
type: concept
tags: [security, glossary, web, ssti, template-injection, rce, owasp, template-engine, sandbox-escape]
sources: [https://ko.wikipedia.org/wiki/템플릿_인젝션, https://ko.wikipedia.org/wiki/OWASP]
confidence: high
---
> [[ssti]]의 후반부입니다.

## Step 3: 전문 용어 설명 (위키백과/OWASP/PortSwigger 기반)
### 주요 템플릿 엔진별 안전한 설정

| 엔진 | 안전한 설정 예시 |
|------|------------------|
| **Jinja2** | `env = SandboxedEnvironment(autoescape=True)` / `Environment(autoescape=select_autoescape(['html','xml']))` |
| **Twig** | `$twig->addExtension(new Twig\Extension\SandboxExtension()); $twig->getExtension(SandboxExtension::class)->setSecurityPolicy($policy);` |
| **Thymeleaf** | 기본적으로 안전한 컨텍스트 인식 이스케이프 제공 (`th:text="${...}"` 자동 이스케이프) |
| **FreeMarker** | `cfg.setNewBuiltinClassResolver(TemplateClassResolver.SAFER_RESOLVER)` |
| **Handlebars** | 기본적으로 로직리스(Logic-less) — 코드 실행 불가, 헬퍼 함수만 등록 가능 |
| **ERB (Rails)** | `<%= ... %>` 자동 HTML 이스케이프, `<%== ... %>`만 raw 출력 (주의) |

### SSTI 탐지 및 테스트 도구

| 도구/방법 | 용도 |
|----------|------|
| **PortSwigger Web Security Academy** | SSTI 실습 랩 (Jinja2, Twig, FreeMarker, Velocity 등) |
| **Burp Suite** | SSTI 스캐너, 템플릿 엔진 식별, 페이로드 생성 |
| **Nuclei** | `-t cves/ -t vulnerabilities/ssti/` 템플릿으로 자동 스캔 |
| **tplmap** | 자동 SSTI 탐지/익스플로잇 도구 (Jinja2, Twig, Smarty 등 지원) |
| **SSTImap** | 자동 SSTI 탐지/익스플로잇 (Python) |
| **JAWS** | Jinja2 전용 SSTI 스캐너/익스플로잇 |
| **Semgrep/CodeQL** | 정적 분석으로 SSTI 취약 코드 패턴 탐지 |

### 주요 SSTI 사고 사례

| 사고 | 연도 | 템플릿 엔진 | 공격 벡터 | 피해 |
|------|------|------------|-----------|------|
| **Shopify** | 2016 | Liquid | 관리자 페이지 템플릿 주입 | 버그바운티 $10,000+ |
| **Uber** | 2016 | Jinja2 | 고객 지원 티켓 템플릿 주입 | 버그바운티 $10,000 |
| **Twitter** | 2014 | Ruby ERB | 프로필 페이지 템플릿 주입 | 버그바운티 $10,080 |
| **Atlassian Confluence** | 2019 | Velocity (CVE-2019-3396) | Widget Connector 매크로 SSTI → RCE | RCE 체인 |
| **Apache Struts2** | 2017-2022 | OGNL (표현식 언어) | 다수 CVE (SSTI 유사) | 다수 RCE 사고 |

### SSTI vs XSS vs Command Injection 비교

| 구분 | **SSTI** | **XSS** | **Command Injection** |
|------|----------|---------|----------------------|
| **실행 위치** | **서버 사이드** (템플릿 엔진) | **클라이언트 사이드** (브라우저) | **서버 사이드** (OS 쉘) |
| **실행 권한** | 템플릿 엔진 권한 (웹앱 사용자) | 피해자 브라우저 권한 (사용자 컨텍스트) | 웹앱 사용자 (종종 www-data) |
| **주입 대상** | 템플릿 문법 (`{{...}}`, `{%...%}`) | HTML/JS 문법 (`<script>`, `onerror`) | 쉘 메타문자 (`;`, `&`, `|`, `$`) |
| **최대 영향** | **RCE** (서버 완전 장악) | 세션 하이재킹, 디페이스, 키로거 | **RCE** (서버 완전 장악) |
| **샌드박스** | 템플릿 엔진 샌드박스 (우회 가능) | 브라우저 샌드박스 (CSP, SameSite) | OS 권한/컨테이너 격리 |
| **탐지 난이도** | 높음 (서버 사이드, 응답 기반) | 중간 (브라우저 실행, CSP 우회) | 중간 (명령어 실행, 프로세스 트리) |

### 관련 표준 및 참고

| 표준/문서 | 내용 |
|----------|------|
| **OWASP SSTI** | 서버 사이드 템플릿 주입 공격/방어 가이드 |
| **PortSwigger SSTI** | 실습 랩, 엔진별 페이로드, 샌드박스 우회 |
| **CWE-1336** | Improper Neutralization of Special Elements used in a Template Engine |
| **CWE-94** | Improper Control of Generation of Code ('Code Injection') |

---


## 관련 위키 링크
- [[headroom]] — Headroom (LLM Context Compression Layer) — SSTI와 함께 템플릿 및 LLM 컨텍스트 압축 기술

- [[command-injection]] — Command Injection (템플릿 엔진에서 명령 실행 가능)
- [[rce]] — RCE (SSTI는 RCE의 주요 경로 중 하나)
- [[file-upload]] — File Upload (템플릿 파일 업로드 → SSTI)
- [[ssti]] — SSTI (자기 참조)
- [[real-world-breach-cases]] — 실제 침해 사례 (Confluence, Shopify, Uber 등 사례)
- [[exploitation]] — 익스플로잇 (SSTI → RCE → 포스트 익스플로잇)

---

## 참고 문헌

- 한국어 위키백과: [서버 사이드 템플릿 주입](https://ko.wikipedia.org/wiki/서버_사이드_템플릿_주입)
- OWASP: [Server-Side Template Injection](https://owasp.org/www-community/attacks/Server_Side_Template_Injection)
- PortSwigger: [Server-side template injection](https://portswigger.net/web-security/server-side-template-injection)
- OWASP Cheat Sheet: [SSTI Prevention](https://cheatsheetseries.owasp.org/cheatsheets/Server-Side_Template_Injection_Cheat_Sheet.html)
- "SSTI in Modern Web Applications" — BlackHat/DEF CON 발표 자료 모음
## 관련 위키 링크
- [[ssti]] — 인덱스 페이지
- [[ssti-core]] — 분할 페이지
- [[ssti2-final-writeup]] — picoCTF 2025 SSTI2 필터 우회 writeup
- [[rce]]
