---
title: CORS Misconfiguration — 핵심
created: 2026-06-12
updated: 2026-06-13
type: concept
tags: [security, glossary, web, cors, misconfiguration, same-origin-policy, cross-origin, owasp, api-security]
sources: [https://ko.wikipedia.org/wiki/교차_출처_리소스_공유, https://ko.wikipedia.org/wiki/동일_출처_정책, https://ko.wikipedia.org/wiki/OWASP]
confidence: high
---

# CORS Misconfiguration (CORS 설정 오류) — 보안 용어 해설

## Step 1: 단어 직역 및 쉬운 비유

### 1. 용어 풀이

**CORS** = **C**ross-**O**rigin **R**esource **S**haring

**Misconfiguration** = **Mis** (잘못된) + **Configuration** (설정)

| 용어 | 직역 | 의미 |
|------|------|------|
| **Cross-Origin** | 교차 출처 | 다른 도메인/프로토콜/포트 간 |
| **Resource Sharing** | 리소스 공유 | 리소스(데이터, API) 주고받기 |
| **Misconfiguration** | 설정 오류 | 잘못된/취약한 설정 |

### 2. 의미 조합

> **"브라우저의 동일 출처 정책(SOP)을 우회하여, 악의적인 사이트가 피해자 브라우저에서 인증된 사용자로 타겟 사이트의 API/리소스에 접근하게 만드는 CORS 헤더 설정 오류"**

### 3. 강력한 비유: "출입증 검사관(브라우저)이 '이 사람 누구든 들여보내줘(Access-Control-Allow-Origin: *)'라고 적힌 메모만 보고 아무나 들여보내는 경비 시스템"

```
┌────────────────────────────────────────────────────────────┐
│  상황: 은행(API 서버)에서 고객(브라우저) 거래 처리           │
│  경비원(브라우저 SOP): "본인 계좌만 조회 가능"              │
│  하지만 은행 직원이 "누구든 다 들여보내줘"라는              │
│  메모(CORS 헤더)를 경비원에게 줌 → 누구든 고객 계좌 접근 가능 │
└────────────────────────────────────────────────────────────┘

🌐  **잘못된 출입증 시나리오 (CORS Misconfiguration 공격 흐름)**

  ① **정상 상황 (SOP 정상 작동)**:
     - 피해자: `bank.com` 로그인 → 세션 쿠키 보유
     - 공격자 사이트: `evil.com`에서 `fetch('https://bank.com/api/account')`
     - 브라우저: **SOP 차단** → `evil.com`이 `bank.com` 응답 읽기 불가 ✓

  ② **CORS 설정 오류 (취약)**:
     - `bank.com` 응답 헤더: `Access-Control-Allow-Origin: *`
     - 또는: `Access-Control-Allow-Origin: https://evil.com`
     - `Access-Control-Allow-Credentials: true` (쿠키 포함 허용)
     - 브라우저: "어? 허용한다고 했네?" → **응답 읽기 허용!**

  ③ **공격자 악용**:
     - 피해자: `evil.com` 방문 (피싱, 광고, XSS 등으로 유도)
     - `evil.com` 스크립트: 
       ```javascript
       fetch('https://bank.com/api/transfer', {
         method: 'POST',
         credentials: 'include',  // 쿠키 자동 포함
         body: JSON.stringify({ to: 'attacker', amount: 10000 })
       })
       ```
     - 브라우저: **쿠키 포함 요청 전송 → 응답 읽기 허용** → 이체 성공!

  ④ **더 위험한 설정들**:
     - `Access-Control-Allow-Origin: *` + `Allow-Credentials: true` → **최악** (모든 출처에서 인증된 요청 가능)
     - `Allow-Origin: null` 허용 → `file://`, `data://`, 샌드박스 iframe에서 접근 가능
     - `Allow-Methods: *` → `DELETE`, `PUT`, `PATCH` 등 위험 메서드 허용
     - `Allow-Headers: *` → 인증 헤더, 커스텀 헤더 노출

💡 **핵심 포인트**: 
- **SOP(동일 출처 정책)** = 브라우저의 핵심 보안 경계
- **CORS** = SOP의 **예외**를 허용하는 메커니즘
- **설정 오류** = 예외를 **너무 넓게/잘못** 허용 → SOP 무력화
- **Credentials 포함 + Origin 검증 부재** = **최악의 조합** (인증된 사용자 세션 탈취)
```

---

## Step 2: 개념 시각화

![CORS Misconfiguration 비유 시각화: 출입증 검사관으로 설명하는 CORS 설정 오류 — 브라우저(경비원), 동일 출처 정책(출입 규칙), CORS 헤더(출입증 메모), 악의적 사이트(가짜 손님), 피해자 브라우저(고객), API 서버(은행) - 한글 레이블 포함](https://v3b.fal.media/files/b/0a9dfef4/KqR2mKxL5vN8tYpHgJkB4_L9wEmVnA.png)

**이미지 설명**:
- **브라우저(경비원)** — 동일 출처 정책(SOP)을 시행하는 주체
- **동일 출처 정책(출입 규칙)** — 같은 출처(도메인/프로토콜/포트)만 리소스 접근 허용
- **CORS 헤더(출입증 메모)** — `Access-Control-Allow-Origin`, `Allow-Credentials` 등 예외 허용 정책
- **악의적 사이트(가짜 손님)** — 피해자 브라우저에서 피해자 권한으로 타겟 API 호출 시도
- **피해자 브라우저(고객)** — 인증된 세션(쿠키)을 가진 상태에서 공격자 사이트 방문
- **API 서버(은행)** — CORS 헤더를 잘못 설정하여 출입 규칙을 무력화

> ⚠️ **참고**: 이미지 생성 도구가 PNG 형식으로 반환했습니다. 스킬 요구사항(.jpg/.jpeg)은 현재 도구 제약상 PNG로 대체됩니다.

---

## Step 3: 전문 용어 설명 (위키백과/OWASP/PortSwigger 기반)
### CORS Misconfiguration (CORS 설정 오류)

**정의**: **CORS Misconfiguration(CORS 설정 오류)**는 웹 애플리케이션이 **Cross-Origin Resource Sharing(CORS) 관련 HTTP 응답 헤더를 잘못 구성하여**, 브라우저의 **동일 출처 정책(Same-Origin Policy, SOP)을 의도하지 않게 우회 허용**함으로써, **악의적인 출처(Origin)에서 인증된 사용자의 브라우저를 통해 민감한 API/리소스에 접근하거나 동작을 수행할 수 있게 만드는 설정 오류**이다.

### CORS 동작 원리 및 핵심 헤더

| 헤더 | 설명 | 보안 영향 |
|------|------|-----------|
| **Access-Control-Allow-Origin** | 어떤 출처(Origin)에서 접근 허용할지 지정 | `*` (모든 출처), 특정 출처(`https://example.com`), `null` |
| **Access-Control-Allow-Credentials** | 쿠키/인증 헤더/클라이언트 인증서 포함 허용 여부 | `true` 시 쿠키 자동 포함 → **CSRF/세션 하이재킹 위험** |
| **Access-Control-Allow-Methods** | 허용할 HTTP 메서드 | `GET, POST, PUT, DELETE, PATCH, OPTIONS` |
| **Access-Control-Allow-Headers** | 요청 시 허용할 커스텀 헤더 | `Authorization`, `Content-Type`, `X-CSRF-Token` 등 |
| **Access-Control-Expose-Headers** | 클라이언트(JS)가 읽을 수 있는 응답 헤더 | `X-Total-Count`, `Link` 등 |
| **Access-Control-Max-Age** | Preflight 결과 캐시 시간 (초) | 너무 길면 설정 변경 반영 지연 |

### Preflight Request (예비 요청) 흐름

```
1. 브라우저: 복잡한 요청(PUT, 커스텀 헤더 포함 등) 감지
         ↓
2. 브라우저 → 서버: OPTIONS /api/resource
   Origin: https://evil.com
   Access-Control-Request-Method: PUT
   Access-Control-Request-Headers: Authorization
         ↓
3. 서버 → 브라우저: 응답 헤더
   Access-Control-Allow-Origin: https://evil.com
   Access-Control-Allow-Methods: GET, POST, PUT, DELETE
   Access-Control-Allow-Headers: Authorization
   Access-Control-Allow-Credentials: true
   Access-Control-Max-Age: 86400
         ↓
4. 브라우저: 헤더 검증 후 실제 요청(PUT) 전송
   Cookie/Authorization 헤더 포함 여부 결정
```

### 주요 CORS 설정 오류 유형

| 오류 유형 | 설명 | 위험도 | 예시 |
|----------|------|--------|------|
| **와일드카드 + Credentials** | `Allow-Origin: *` + `Allow-Credentials: true` | **치명적** | 모든 출처에서 인증된 요청 가능 (브라우저가 차단하지만 잘못 구현 시 우회 가능) |
| **신뢰할 수 없는 Origin 반사** | 요청의 `Origin` 헤더를 검증 없이 그대로 `Allow-Origin`에 반영 | **치명적** | `Origin: https://evil.com` → `Allow-Origin: https://evil.com` |
| **Null Origin 허용** | `Allow-Origin: null` 허용 | **높음** | `file://`, `data://`, 샌드박스 iframe(`sandbox` 속성)에서 접근 가능 |
| **과도한 메서드 허용** | `Allow-Methods: *` 또는 `GET, POST, PUT, DELETE, PATCH, TRACE` 모두 허용 | **높음** | `DELETE /api/users/123`, `TRACE /api/debug` 등 위험 메서드 허용 |
| **과도한 헤더 허용** | `Allow-Headers: *` | **중간** | `Authorization`, `X-CSRF-Token`, 내부 헤더 노출 |
| **Subdomain 와일드카드** | `Allow-Origin: *.example.com` | **중간** | `evil.example.com`, `sub.evil.example.com` 등 서브도메인 탈취 시 악용 |
| **Preflight 캐시 과다** | `Max-Age` 과도하게 길게 설정 (예: 1년) | **낮음** | 설정 변경 시 클라이언트 반영 지연 |
| **HTTPS 사이트에서 HTTP Origin 허용** | `https://bank.com`이 `http://evil.com` 허용 | **높음** | 혼합 콘텐츠, 중간자 공격 경로 |

### CORS Misconfiguration 공격 시나리오

| 시나리오 | 공격 흐름 | 피해 |
|----------|-----------|------|
| **인증된 API 탈취** | 1. 피해자 `bank.com` 로그인<br>2. `evil.com` 방문<br>3. `evil.com`에서 `fetch('https://bank.com/api/account', {credentials: 'include'})`<br>4. CORS 헤더 허용 → 응답 읽기 성공 | 계좌 잔액, 거래 내역, 개인정보 유출 |
| **CSRF 강화** | 1. `Allow-Credentials: true` + `Allow-Origin: *` 또는 신뢰할 수 없는 Origin 허용<br>2. 피해자 `evil.com` 방문<br>3. 자동으로 `POST /api/transfer` 전송 (쿠키 포함) | 무단 이체, 설정 변경, 계정 탈취 |
| **민감 헤더 유출** | 1. `Allow-Headers: *` 또는 `Authorization` 노출<br>2. `evil.com`에서 `fetch`로 응답 헤더 읽기 | JWT 토큰, API 키, CSRF 토큰, 세션 ID 유출 |
| **Subdomain 탈취 연계** | 1. `*.example.com` 허용<br>2. 공격자 `evil.example.com` 장악 (서브도메인 탈취, DNS 하이재킹)<br>3. 메인 도메인 API 접근 | 전체 도메인 API 완전 장악 |
| **Null Origin 악용** | 1. `Allow-Origin: null` 허용<br>2. `file://` 로컬 HTML, `data:` URI, 샌드박스 iframe에서 API 호출 | 로컬 파일/샌드박스에서 인증된 API 접근 |

### CORS 설정 검증 체크리스트

| 검증 항목 | 올바른 설정 | 잘못된 설정 |
|----------|-------------|-------------|
| **Allow-Origin** | 구체적 출처 명시 (`https://app.example.com`) | `*`, 요청 Origin 그대로 반영, `null` 허용 |
| **Allow-Credentials** | `true`일 때 **Origin 반드시 구체적으로 지정** | `Allow-Origin: *` 와 함께 사용 |
| **Allow-Methods** | 실제로 필요한 메서드만 (`GET, POST`) | `*`, `PUT, DELETE, TRACE, CONNECT` 포함 |
| **Allow-Headers** | 필요한 헤더만 (`Authorization, Content-Type`) | `*`, 불필요한 헤더 노출 |
| **Origin 검증** | 화이트리스트 기반 정확한 매칭 | 문자열 포함(`includes`), 접두사 매칭(`startsWith`), 정규식 오류 |
| **HTTPS 강제** | HTTPS Origin만 허용 | HTTP Origin 허용 |
| **Preflight 캐시** | 적절한 `Max-Age` (예: 600~3600초) | 너무 짧음(매번 preflight) 또는 너무 김(변경 반영 지연) |


## 관련 위키 링크
- [[cors-misconfig]] — 인덱스 페이지
- [[cors-misconfig-defense]] — 분할 페이지
- [[rce]]
