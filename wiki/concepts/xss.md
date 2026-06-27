---
title: XSS (Cross-Site Scripting) — 보안 용어 해설
created: 2026-06-12
updated: 2026-06-21
type: concept
tags: [vulnerability, xss, web, injection, owasp]
sources: [raw/articles/xss-glossary-original.md]
confidence: high
---

# XSS (Cross-Site Scripting) — 보안 용어 해설

## 참고 URL
- [Reference](raw/articles/xss-glossary-original.md)

## 약자 풀이

**XSS** = **C**ross-**S**ite **S**cripting

| 약자 | 원래 단어 | 뜻 |
|------|----------|-----|
| **C** | **Cross** | 교차, 가로지르다 |
| **S** | **Site** | 사이트 (웹사이트) |
| **S** | **Scripting** | 스크립트를 실행하는 행위 |

**의미**: "서로 다른 웹사이트를 가로질러 악성 스크립트를 실행하게 하는 공격 기법"

## 쉬운 비유 — "식당 직원으로 위장한 배달 사기꾼"

### Step 1: 악성 주문 입력
해커(=나쁜 손님)가 식당 **메뉴판(=게시판/댓글창)** 에 "주문과 함께 **물 한 잔에 수면제를 타서** 갖다 주세요"라고 적어 놓습니다. (악성 스크립트를 게시물에 심음)

### Step 2: 검증 없는 전달
식당 주인(=웹 서버)은 그 메뉴판 내용을 그대로 다음 손님에게 전달합니다. 주인은 손님이 주문한 내용이 수상한지 **전혀 확인하지 않습니다**. (서버는 입력값을 검증 없이 그대로 출력)

### Step 3: 피해자 실행
피해자(=일반 손님)는 식당에 와서 메뉴판을 보고, 거기 적힌 대로 **물에 수면제를 탄 음료**를 받아 마시게 됩니다. 피해자는 "이 식당이 시키는 거니까 안전하겠지"라고 믿었지만, 사실 그 내용은 **전혀 다른 손님이 심어 놓은 것**입니다.

### 결과
피해자는 정신을 잃고, 해커는 피해자의 **지갑(=쿠키, 세션 토큰)**, **휴대폰(=개인정보)** 등을 마음대로 가져갑니다.

---

## 전문 설명

### 정의

**사이트 간 스크립팅 (Cross-Site Scripting, XSS)** 은 웹 애플리케이션에서 가장 많이 나타나는 취약점 중 하나로, **웹사이트 관리자가 아닌 공격자가 웹 페이지에 악성 스크립트를 삽입할 수 있는 취약점**입니다. 명칭이 XSS인 이유는 웹 기술인 CSS(Cascading Style Sheets)와의 혼동을 피하기 위함입니다.

### CWE 분류
- **CWE-79**: Improper Neutralization of Input During Web Page Generation

### OWASP Top 10
- 2017: 7위 (A7: XSS)
- 2021: 3위 (A03: Injection)

### 공격 유형

#### 1. 반사형 XSS (Reflected XSS)
- 악성 스크립트가 서버에 저장되지 않고, HTTP 요청(URL 파라미터 등)에 포함되어 즉시 응답에 반영
- 피해자가 **악성 URL을 클릭**해야 동작
- 대상: 검색 엔진, 에러 페이지

```http
http://victim.com/search?q=<script>...
```

#### 2. 저장형 XSS (Stored XSS)
- 악성 스크립트가 **서버에 영구 저장** → 다른 사용자가 조회할 때마다 실행
- 가장 치명적인 XSS — 피해자의 별도 조작 불필요
- 대상: 게시판, 댓글, 프로필

#### 3. DOM 기반 XSS (DOM-based XSS)
- 서버 응답에는 악성 코드가 없지만, 클라이언트 JS가 DOM을 동적 처리하는 과정에서 발생
- 감지가 가장 어려운 유형

### 방어 방법

| 기법 | 설명 |
|------|------|
| **HTML 인코딩** | `<` → `&lt;`, `>` → `&gt;` 등 특수문자 변환 |
| **CSP** | `Content-Security-Policy` 헤더로 스크립트 출처 제한 |
| **입력값 검증** | 화이트리스트 방식 |
| **HttpOnly 쿠키** | JS에서 `document.cookie` 접근 차단 |
| **프레임워크 이스케이프** | React JSX, Vue 템플릿 등 자동 이스케이프 |

### MITRE ATT&CK 매핑
| Tactic | Technique | ID |
|--------|-----------|----|
| Initial Access | Drive-by Compromise | T1189 |
| Execution | User Execution | T1204 |
| Credential Access | Web Session Cookie | T1539 |

### 관련 개념
- [[cve-2024-6387-regresshion]] (메모리 취약점과 대비)
- [[ai-ctf-overview]] (CTF에서 XSS 활용)
- [[prompt-injection-ctf]] (인젝션 계열 취약점 비교)
- SQL Injection, CSRF (같은 웹 취약점 계열)

---

**참고**: 한국어 위키백과 — [사이트 간 스크립팅](https://ko.wikipedia.org/wiki/%EC%82%AC%EC%9D%B4%ED%8A%B8_%EA%B0%84_%EC%8A%A4%ED%81%AC%EB%A6%BD%ED%8C%85)
## 관련 보강 링크
- [[eval]] — 문자열 코드 실행이 XSS injection sink가 되는 대표 사례
