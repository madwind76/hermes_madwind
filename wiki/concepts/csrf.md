---
title: CSRF (Cross-Site Request Forgery, 사이트 간 요청 위조) — 보안 용어 해설
created: 2026-06-12
updated: 2026-06-21
type: concept
tags: [security, glossary, web, csrf, csrf-token, sameorigin, owasp, session-riding]
sources: [https://ko.wikipedia.org/wiki/사이트_간_요청_위조, https://ko.wikipedia.org/wiki/OWASP]
confidence: high
---

# CSRF (Cross-Site Request Forgery, 사이트 간 요청 위조) — 보안 용어 해설

## 참고 URL
- [ko.wikipedia.org](https://ko.wikipedia.org/wiki/사이트_간_요청_위조)
- [ko.wikipedia.org](https://ko.wikipedia.org/wiki/OWASP)

## Step 1: 단어 직역 및 쉬운 비유

### 1. 약자 풀이

**CSRF** = **C**ross-**S**ite **R**equest **F**orgery

| 약자 | 원래 단어 | 직역 | 의미 |
|------|-----------|------|------|
| **C** | **Cross** | 교차, 가로지르다 | 서로 다른 사이트 간 |
| **S** | **Site** | 사이트 | 웹사이트, 출처(Origin) |
| **R** | **Request** | 요청 | HTTP 요청 |
| **F** | **Forgery** | 위조, 변조 | 가짜로 만듦 |

### 2. 의미 조합

> **"피해자의 브라우저가 의도하지 않은 요청을 공격자가 만든 악성 페이지에서 대상 사이트로 보내게 하여, 피해자 권한으로 원치 않는 작업(비밀번호 변경, 송금, 게시글 작성 등)을 수행하게 하는 공격"**

### 3. 강력한 비유: "당신 명의로 위장된 위임장"

```
┌────────────────────────────────────────────────────────────┐
│  상황: 은행(대상 사이트)에서 당신이 로그인한 상태           │
│  해커(공격자)가 당신 모르게 당신의 도장(쿠키/세션)을        │
│  찍은 위임장(위조 요청)을 은행에 제출하게 만듦             │
└────────────────────────────────────────────────────────────┘

🏦  **은행 강도 시나리오 (CSRF 공격 흐름)**

  ① **정상 로그인**: 당신이 bank.com에 로그인 → 세션 쿠키 발급
     (브라우저: "나는 user123이야" 증명서 보관)

  ② **악성 페이지 방문**: 해커가 만든 evil.com 페이지 접속
     (이메일 링크, 광고, 해킹된 정상 사이트 등 경유)

  ③ **위조 요청 자동 실행**: evil.com에 숨겨진 코드 실행
     ```html
     <!-- 눈에 안 보이는 iframe 또는 자동 submit form -->
     <form action="https://bank.com/transfer" method="POST">
       <input name="to" value="hacker_account">
       <input name="amount" value="1000000">
     </form>
     <script>document.forms[0].submit()</script>
     ```

  ④ **브라우저의 순진한 행동**: 
     "어? bank.com으로 POST 요청이네? 
     내 쿠키(user123 세션) 자동 첨부해서 보내줘야지!"

  ⑤ **은행 서버 처리**: 
     "쿠키 검증 OK → user123 인증됨 → 송금 처리 완료"

  ⑥ **결과**: 당신의 돈 100만 원이 해커 계좌로 이체됨
     당신은 아무 클릭도 안 했는데!

💡 **핵심 포인트**: 
- **브라우저는 "같은 사이트 요청이면 쿠키 자동 첨부"라는 규칙을 따름**
- 해커는 **쿠키를 몰라도** 브라우저가 알아서 붙여줌을 악용
- 피해자는 **악성 페이지만 방문**하면 되고, 별도 클릭 불필요
- **"Session Riding(세션 타고 가기)"** 라고도 부름
```

---

## Step 2: 개념 시각화

![CSRF 비유 시각화: 위임장 위조로 설명하는 CSRF — 사용자(피해자), 은행(대상 사이트), 세션 쿠키(도장/위임장), 악성 페이지(위조 위임장), 자동 제출 폼(숨겨진 요청), 해커 계좌(이체 대상) - 한글 레이블 포함](https://v3b.fal.media/files/b/0a9dfe8c/ZqR2mKxL5vN8tYpHgJkB4_L9wEmVnA.png)

**이미지 설명**:
- **사용자(피해자)** — 정상적으로 대상 사이트에 로그인한 상태 (세션 쿠키 보유)
- **은행(대상 사이트)** — 인증 후 상태 변경 요청을 처리하는 서버
- **세션 쿠키(도장/위임장)** — 사용자 인증 증명서, 브라우저가 자동 첨부
- **악성 페이지(위조 위임장)** — 공격자가 만든 페이지, 위조된 요청 포함
- **자동 제출 폼(숨겨진 요청)** — 사용자 인지 없이 자동 전송되는 POST 요청
- **해커 계좌(이체 대상)** — 공격자가 이득을 보는 대상 (송금, 비밀번호 변경 등)

> ⚠️ **참고**: 이미지 생성 도구가 PNG 형식으로 반환했습니다. 스킬 요구사항(.jpg/.jpeg)은 현재 도구 제약상 PNG로 대체됩니다.

---

## Step 3: 전문 용어 설명 (위키백과/OWASP 기반)

### CSRF (Cross-Site Request Forgery, 사이트 간 요청 위조)

**정의**: **CSRF(사이트 간 요청 위조)**는 웹 애플리케이션 취약점의 일종으로, **인증된 사용자가 의도하지 않은 요청을 공격자가 조작한 페이지를 통해 대상 웹사이트로 전송하게 하여, 사용자 권한으로 원치 않는 상태 변경 작업(자금 이체, 비밀번호 변경, 권한 부여 등)을 수행하게 하는 공격**이다. OWASP Top 10에서 지속적으로 상위권에 랭크되는 고전적이면서도 강력한 공격 기법이다.

### 공격 원리: Same-Origin Policy와 쿠키 자동 전송의 틈

| 요소 | 설명 |
|------|------|
| **Same-Origin Policy (SOP)** | 브라우저 보안 정책: 다른 출처(Origin: 프로토콜+도메인+포트)의 리소스 접근 제한 |
| **SOP의 예외** | `<form>`, `<img>`, `<script>`, `<iframe>` 등 **크로스 오리진 요청 전송은 허용** (응답 읽기만 차단) |
| **쿠키 자동 전송** | 브라우저는 **요청 대상 도메인과 쿠키 도메인이 일치하면 자동으로 쿠키 포함** 전송 |
| **공격 가능 조건** | 1) 피해자 로그인 상태(세션 유효) 2) 상태 변경 요청 예측 가능 3) CSRF 토큰 등 검증 부재 |

### CSRF 공격 분류

| 유형 | 설명 | 예시 |
|------|------|------|
| **GET 기반** | URL만으로 상태 변경 수행 (REST 위반) | `<img src="https://bank.com/transfer?to=hacker&amt=100">` |
| **POST 기반** | Form 자동 제출로 상태 변경 | `<form action="..." method="POST">...</form><script>submit()</script>` |
| **JSON/Content-Type 우회** | `text/plain` 등으로 Content-Type 우회 | `fetch(url, {method:'POST', body:json, headers:{'Content-Type':'text/plain'}})` |
| **로그인 CSRF** | 공격자 계정으로 피해자 로그인 유도 | 피해자가 공격자 계정으로 활동 → 개인정보/검색기록 유출 |
| **저장형 CSRF (Stored CSRF)** | 악성 코드가 대상 사이트에 저장 (XSS와 결합) | 게시글/댓글에 CSRF 페이로드 저장 → 관리자 열람 시 실행 |

### 실제 공격 시나리오

| 시나리오 | 공격 내용 | 영향 |
|----------|-----------|------|
| **비밀번호 변경** | `/change-password?new=hacker123` | 계정 탈취 (2FA 우회 시 완전 장악) |
| **이메일 변경** | `/change-email?email=hacker@evil.com` | 계정 복구 링크 가로채기 → 계정 탈취 |
| **자금 이체** | `/transfer?to=attacker&amount=10000` | 직접적 금전 피해 |
| **권한 부여/역할 변경** | `/admin/grant-role?user=victim&role=admin` | 권한 상승, 관리자 권한 획득 |
| **게시물/댓글 작성** | `/post/create?content=spam_or_malware` | 평판 훼손, 악성 링크 유포 |
| **API 키/토큰 생성** | `/api/keys/create` | 이후 무인 접근 권한 획득 |
| **2FA 비활성화** | `/security/2fa/disable` | 2차 인증 우회 → 계정 완전 장악 |

### CSRF 방어 기법

| 방어 기법 | 설명 | 구현 예시 | 효과/한계 |
|----------|------|-----------|-----------|
| **CSRF 토큰 (Synchronizer Token Pattern)** | 세션별 랜덤 토큰 생성 → 폼/헤더에 포함 → 서버 검증 | `<input name="csrf_token" value="{{session.csrf_token}}">` | **가장 강력/표준** — 상태 변경 모든 요청에 필수 |
| **SameSite 쿠키 속성** | `SameSite=Strict` (크로스 사이트 요청 시 쿠키 미전송), `Lax` (일부 GET 허용) | `Set-Cookie: session=abc; SameSite=Strict; Secure` | **모던 브라우저 기본 방어** — 토큰과 병행 권장 |
| **Custom Header 검증** | `X-Requested-With: XMLHttpRequest` 등 커스텀 헤더 요구 (브라우저가 크로스 오리진 시 자동 추가 불가) | `if (req.headers['x-requested-with'] !== 'XMLHttpRequest') reject` | AJAX/SPA 환경 적합 — 서버사이드 렌더링 폼은 별도 처리 필요 |
| **Referer/Origin 헤더 검증** | 요청 출처(Referer, Origin)가 신뢰 도메인인지 확인 | `if (req.headers.origin !== 'https://bank.com') reject` | 프록시/방화벽에서 헤더 제거 시 오탐 가능 — 보조 수단 |
| **이중 제출 쿠키 (Double Submit Cookie)** | 쿠키에 랜덤 값 저장 + 요청 파라미터/헤더에 동일 값 요구 → 서버에서 비교 | `Cookie: csrf=abc123` + `Header: X-CSRF-Token: abc123` | 상태 비저장(Stateless) 가능 — 서브도메인 이슈 주의 |
| **사용자 재인증 (Re-authentication)** | 민감 작업 시 비밀번호/OTP/생체인증 재요청 | 비밀번호 재입력, SMS OTP, FIDO2 | **가장 확실** — UX 저하, 중요 작업만 적용 |
| **CAPTCHA / 봇 탐지** | 자동화된 요청 차단 | reCAPTCHA, hCaptcha, Turnstile | 사람 대상 공격엔 무력 — 보조 수단 |

### 프레임워크별 CSRF 방어

| 프레임워크 | 기본 제공/미들웨어 | 설정 예시 |
|------------|-------------------|-----------|
| **Django** | `CsrfViewMiddleware` (기본 활성화) | `{% csrf_token %}` 템플릿 태그, `@csrf_exempt` 장식자 |
| **Spring Security** | `CsrfFilter` (기본 활성화) | `<csrf/>`, `CsrfTokenRepository`, `with(csrf().ignoringRequestMatchers(...))` |
| **Express (csurf)** | `csurf` 미들웨어 (deprecated) → `csrf-sync` 권장 | `app.use(csrf({cookie: true}))`, `req.csrfToken()` |
| **FastAPI / Starlette** | `Starlette-CSRFMiddleware` | `app.add_middleware(CSRFMiddleware, secret=...)` |
| **ASP.NET Core** | `AddAntiforgery()` | `@Html.AntiForgeryToken()`, `[ValidateAntiForgeryToken]` |
| **Laravel** | `VerifyCsrfToken` 미들웨어 (기본) | `@csrf` 블레이드 디렉티브, 세션에 `_token` 자동 저장 |
| **React / Vue / SPA** | CSRF 쿠키 + 헤더 패턴 (`X-CSRFToken`, `X-XSRF-TOKEN`) | `axios.defaults.xsrfCookieName = 'csrftoken'` |
| **GraphQL** | 상태 변경(Mutation)에만 토큰/헤더 요구 | `Apollo Link` 커스텀 헤더 주입 |

### CSRF 탐지 및 테스트

| 방법 | 도구/기법 |
|------|-----------|
| **자동 스캔** | OWASP ZAP, Burp Suite CSRF Scanner, Nikto |
| **수동 테스트** | Burp Suite "Generate CSRF PoC" 기능, 커스텀 HTML PoC 작성 |
| **코드 리뷰** | 상태 변경 엔드포인트(POST/PUT/DELETE/PATCH) 토큰 검증 여부 확인 |
| **자동화 테스트** | Cypress/Playwright로 토큰 누락 엔드포인트 탐지 |

### 관련 표준 및 참고

| 표준/문서 | 내용 |
|----------|------|
| **OWASP CSRF Prevention Cheat Sheet** | 방어 기법 종합 가이드 |
| **RFC 6265 (Cookie SameSite)** | SameSite 속성 표준화 |
| **OWASP ASVS 4.0 V4.5** | CSRF 보호 검증 요구사항 |
| **CWE-352** | Cross-Site Request Forgery 약점 열거 |

---

## 관련 위키 링크

- [[xss]] — XSS (CSRF와 결합 시 저장형 CSRF 가능, 동일 출처 정책 우회)
- [[sql-injection]] — SQL Injection (입력 검증 미흡이라는 공통 원인)
- [[ssrf]] — SSRF (서버 측 요청 위조, CSRF와 대조: 클라이언트 vs 서버)
- **Broken Authentication** — 깨진 인증 (CSRF로 비밀번호 변경 시 인증 우회) → [[broken-auth]]
- [[actions-on-objectives]] — 목표 달성 (CSRF로 계정 탈취/권한 상승 등 최종 목적 달성)

---

## 참고 문헌

- 한국어 위키백과: [사이트 간 요청 위조](https://ko.wikipedia.org/wiki/사이트_간_요청_위조)
- 한국어 위키백과: [세션 하이재킹](https://ko.wikipedia.org/wiki/세션_하이재킹)
- OWASP: [Cross-Site Request Forgery (CSRF)](https://owasp.org/www-community/attacks/csrf)
- OWASP Cheat Sheet: [CSRF Prevention](https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html)
- MDN Web Docs: [SameSite cookies](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Set-Cookie/SameSite)
