---
title: Broken Authentication — 인증 체계 결함
created: 2026-06-12
updated: 2026-06-12
type: concept
tags: [security, glossary, web, broken-auth, authentication, session, owasp, credential-stuffing, brute-force, mfa-bypass]
sources: [https://ko.wikipedia.org/wiki/인증, https://ko.wikipedia.org/wiki/OWASP]
confidence: high
---

# Broken Authentication (인증 체계 결함) — 보안 용어 해설

## Step 1: 단어 직역 및 쉬운 비유

### 1. 용어 풀이

**Broken Authentication** = **Broken** (망가진, 고장난) + **Authentication** (인증, 본인 확인)

| 영어 단어 | 직역 | 의미 |
|-----------|------|------|
| **Broken** | 망가진, 작동 안 함 | 제 기능을 못 함, 결함이 있음 |
| **Authentication** | 인증, 본인 확인 | "당신이 누구인지 증명해봐" 과정 |

### 2. 의미 조합

> **"로그인/세션/비밀번호 재설정 등 인증 관련 기능에 결함이 있어, 공격자가 정상 사용자인 척 가장하거나 인증 절차를 우회하여 계정을 탈취할 수 있는 취약점"**

### 3. 강력한 비유: "열쇠 구멍이 망가져서 아무 열쇠나 다 들어가는 집"

```
┌────────────────────────────────────────────────────────────┐
│  상황: 당신 집(계정)의 현관문(인증 시스템)이 고장남        │
│  정상적인 열쇠(비밀번호) 없어도 문이 열림                   │
└────────────────────────────────────────────────────────────┘

🔓  **망가진 자물쇠 시나리오 (Broken Authentication 공격 흐름)**

  ① **자물쇠가 헐거움 (약한 비밀번호 정책)**: 
     - "123456", "password", "qwerty" 같은 비밀번호 허용
     - 공격자: 흔한 비밀번호 리스트로 무차별 대입 → 로그인 성공

  ② **마스터 키 존재 (세션/토큰 관리 결함)**: 
     - 로그아웃해도 세션 쿠키 만료 안 함 / 토큰 재사용 가능
     - 공격자: 유출된 세션 ID/토큰으로 바로 로그인된 상태 진입

  ③ **여분 열쇠 숨김 (비밀번호 재설정/복구 결함)**: 
     - "비밀번호 찾기"에서 이메일/전화 인증 없이 진행 가능
     - 공격자: 피해자 계정으로 재설정 링크 요청 → 새 비밀번호 설정 → 계정 탈취

  ④ **이중 잠금 안 함 (2FA/MFA 부재 또는 우회)**: 
     - 2단계 인증 없음 / SMS 인증 코드 가로채기(SIM 스와핑) / 백업 코드 유출
     - 공격자: 비밀번호 알아도 2FA 못 뚫음 → 우회 기법으로 뚫음

  ⑤ **열쇠 복사본 무제한 (브루트포스/자격증명 대입 방어 없음)**: 
     - 로그인 시도 횟수 제한 없음 / 계정 잠금 없음 / CAPTCHA 없음
     - 공격자: 자동화 도구로 초당 수천 회 시도 → 결국 맞춤

💡 **핵심 포인트**: 
- 인증은 **"당신이 누구인지 증명"**하는 과정
- 이 과정이 **"망가졌다(Broken)"** = 증명 없이도 통과 가능, 또는 증명을 우회 가능
- OWASP Top 10에서 **2017년 2위, 2021년 7위 (Identification and Authentication Failures)** 로 꾸준히 상위권
```

---

## Step 2: 개념 시각화

![Broken Authentication 비유 시각화: 망가진 자물쇠로 설명하는 인증 결함 — 집(계정), 망가진 자물쇠(인증 시스템), 약한 비밀번호(헐거운 자물쇠), 마스터 키(세션 토큰 탈취), 여분 열쇠(비밀번호 재설정 우회), 이중 잠금 없는 문(2FA 부재), 열쇠 복사 무제한(브루트포스 방어 없음) - 한글 레이블 포함](https://v3b.fal.media/files/b/0a9dfef4/KqR2mKxL5vN8tYpHgJkB4_L9wEmVnA.png)

**이미지 설명**:
- **집(계정)** — 보호 대상 자산 (사용자 계정, 권한, 데이터)
- **망가진 자물쇠(인증 시스템)** — 제 기능을 못 하는 로그인/세션/비밀번호 재설정 메커니즘
- **약한 비밀번호(헐거운 자물쇠)** — 정책 미흡으로 쉽게 열리는 1차 관문
- **마스터 키(세션 토큰 탈취)** — 세션 고정/하이재킹으로 우회하는 만능 열쇠
- **여분 열쇠(비밀번호 재설정 우회)** — 복구 프로세스 허점으로 만드는 새로운 열쇠
- **이중 잠금 없는 문(2FA 부재)** — 2단계 인증 없어 단일 인증만으로 뚫림
- **열쇠 복사 무제한(브루트포스 방어 없음)** — 시도 제한 없어 무한 복사 시도 가능

> ⚠️ **참고**: 이미지 생성 도구가 PNG 형식으로 반환했습니다. 스킬 요구사항(.jpg/.jpeg)은 현재 도구 제약상 PNG로 대체됩니다.

---

## Step 3: 전문 용어 설명 (위키백과/OWASP/PortSwigger 기반)

### Broken Authentication (인증 체계 결함)

**정의**: **Broken Authentication(인증 체계 결함)**은 애플리케이션의 **인증(Authentication)과 세션 관리(Session Management) 기능이 제대로 구현되지 않아, 공격자가 정상 사용자의 신원을 도용하거나 인증 절차를 우회하여 시스템에 무단 접근할 수 있게 하는 취약점 클래스**이다. OWASP Top 10에서 **2017년 A2 (2위), 2021년 A07 (Identification and Authentication Failures, 7위)** 로 선정될 만큼 빈도와 영향이 크다.

### 주요 결함 유형 및 공격 기법

| 결함 분류 | 구체적 결함 |攻击 기법 | 영향 |
|----------|------------|----------|------|
| **약한 자격증명 정책** | 짧은/단순 비밀번호 허용, 흔한 비밀번호 차단 안 함 | 크리덴셜 스터핑(Credential Stuffing), 패스워드 스프레이(Password Spraying), 브루트포스 | 대량 계정 탈취, 수평 이동 |
| | 비밀번호 복잡도/히스토리/만료 정책 없음 | 사전 공격(Dictionary Attack), 레인보우 테이블 | 단일 계정 탈취 |
| **세션 관리 결함** | 세션 ID 예측 가능/짧음/엔트로피 낮음 | 세션 예측(Session Prediction), 세션 고정(Session Fixation) | 세션 하이재킹 |
| | 로그아웃/타임아웃 후 세션 무효화 안 함 | 세션 재사용, 공용 PC에서 세션 탈취 | 계정 지속적 접근 |
| | 세션 ID URL 노출 / HttpOnly/Secure 플래그 없음 | XSS로 세션 쿠키 탈취, 중간자 공격(HTTPS 미사용) | 세션 쿠키 탈취 → 계정 탈취 |
| | 동시 세션 제한 없음 / 기기별 세션 관리 안 함 | 다중 기기 동시 로그인 감지 안 함 | 다중 위치 동시 접근 |
| **인증 우회/논리 결함** | 비밀번호 재설정 토큰 예측 가능/재사용 가능 | 토큰 예측, 토큰 재사용, 이메일/전화 인증 우회 | 계정 탈취 (비밀번호 재설정) |
| | 2FA/MFA 부재 또는 우회 가능 | SIM 스와핑, 푸시 피로 공격(MFA Fatigue), 백업 코드 유출, TOTP 시드 유출 | 2FA 우회 → 계정 탈취 |
| | 인증 후 권한 검사 누락 (IDOR과 결합) | 인증된 사용자가 타인 리소스 접근 | 수평/수직 권한 상승 |
| **브루트포스/자동화 방어 부재** | 로그인 시도 횟수 제한 없음 / 계정 잠금 없음 | 무차별 대입(Brute Force), 크리덴셜 스터핑(대량 자격증명 대입) | 대량 계정 탈취 |
| | CAPTCHA/WAF/속도 제한 없음 | 자동화 도구(SELENIUM, Puppeteer, Hydra, Burp Intruder) 무력화 | 대규모 자동화 공격 |
| | IP/디바이스/지문 기반 차단 없음 | 분산 공격(프록시/봇넷), 회전 프록시 | 방어 회피 |
| **취약한 구현/구성** | 기본/관리자 계정 비활성화 안 함, 기본 비밀번호 변경 안 함 | `admin/admin`, `root/root`, `admin/123456` 등 기본값 시도 | 관리자 권한 탈취 |
| | JWT/토큰 서명 검증 안 함, 알고리즘 혼란(Algorithm Confusion) | `none` 알고리즘, 약한 시크릿, 키 혼동 | 토큰 위조 → 인증 우회 |
| | OAuth/SAML/OIDC 구현 결함 | Redirect URI 검증 안 함, State 파라미터 없음, PKCE 미사용 | 토큰 탈취, 계정 연결 탈취 |

### 공격 시나리오별 실전 예시

| 시나리오 | 공격 절차 | 피해 |
|----------|-----------|------|
| **크리덴셜 스터핑** | 1. 타 사이트 유출 DB(이메일:비번) 확보<br>2. 타겟 사이트 로그인 폼에 자동 대입<br>3. 성공 시 계정 탈취 | 대량 계정 탈취, 동일 비밀번호 재사용 피해자 다수 |
| **패스워드 스프레이** | 1. 사용자명 리스트 확보<br>2. 공통 비번 몇 개(`Password1`, `Welcome123`)로 전체 시도<br>3. 계정 잠금 회피 (한 계정당 1회 시도) | 계정 잠금 회피, 탐지 회피, 다수 계정 탈취 |
| **세션 고정(Session Fixation)** | 1. 공격자가 세션 ID 발급받음<br>2. 피해자에게 해당 세션 ID 링크 전송<br>3. 피해자 로그인 → 같은 세션 ID로 인증됨<br>4. 공격자 같은 세션 ID로 접근 | 피해자 모르게 계정 공유/탈취 |
| **비밀번호 재설정 토큰 예측** | 1. `reset?token=123456` 형태 예측 가능<br>2. 순차/시간 기반 토큰 브루트포스<br>3. 피해자 계정 비밀번호 재설정 | 계정 탈취, 이메일 접근 불필요 |
| **MFA 우회 (푸시 피로/MFA Fatigue)** | 1. 피해자 자격증명 확보<br>2. MFA 푸시 알림 연속 전송 (수십 회)<br>3. 피해자 짜증/실수로 '승인' 누름 | 2FA 우회, 계정 탈취 (Uber, Microsoft 등 실제 사례) |
| **JWT 알고리즘 혼란** | 1. 서버가 `alg: none` 또는 `HS256` 공개키 검증<br>2. 공격자 `{"alg":"none"}` 또는 공개키로 서명<br>3. 임의 클레임(payload) 토큰 생성 | 임의 사용자/관리자 권한 토큰 위조 |

### Broken Authentication 방어 기법

| 방어 영역 | 기법 | 구현 예시 | 효과/비고 |
|----------|------|-----------|-----------|
| **자격증명 정책** | **강력한 비밀번호 정책** | 최소 12자, 대소문자/숫자/특수문자, 흔한 비번 차단(HaveIBeenPwned API 연동), 히스토리 5개 이상 기억 | NIST 800-63B 권장 사항 준수 |
| | **비밀번호 해시** | Argon2id (메모리 하드), bcrypt (cost≥12), scrypt, PBKDF2 (반복≥310,000) | **절대 평문/MD5/SHA1 저장 금지** |
| | **비밀번호 노출 확인** | HaveIBeenPwned API / 내부 DB로 유출 비번 차단 | 크리덴셜 스터핑 선제 차단 |
| **다단계 인증 (MFA/2FA)** | **필수 MFA 적용** | TOTP (Google Authenticator, Authy), FIDO2/WebAuthn (YubiKey, Passkey), 푸시 알림 (Duo, Microsoft Authenticator) | **가장 강력한 단일 방어** — SMS/이메일 OTP는 SIM 스와핑/피싱 취약 |
| | **적응형/위험 기반 MFA** | 새 기기/위치/시간/행위 분석 시 MFA 요구 | UX와 보안 균형 |
| **세션 관리** | **안전한 세션 쿠키** | `Secure; HttpOnly; SameSite=Strict; Path=/` | XSS/CSRF/중간자 공격 차단 |
| | **세션 생성/갱신/무효화** | 로그인 시 새 세션 ID 발급(고정 방지), 유휴/절대 타임아웃(예: 15분/4시간), 로그아웃 시 서버/클라이언트 동시 무효화 | 세션 하이재킹/고정 방지 |
| | **동시 세션 제어** | 사용자당 최대 세션 수 제한, 기기별 세션 목록 제공/원격 로그아웃 | 계정 공유/탈취 탐지 |
| **브루트포스/자동화 방어** | **속도 제한 (Rate Limiting)** | IP/사용자/디바이스별 분당/시간당 시도 제한 (예: 5회/분), 계정 잠금 (5회 실패 시 15분) | 브루트포스/스프레이 차단 |
| | **CAPTCHA/봇 탐지** | reCAPTCHA v3, hCaptcha, Turnstile, 행동 기반 봇 탐지 | 자동화 도구 차단 |
| | **계정 잠금/알림** | 실패 임계값 초과 시 계정 잠금 + 소유자 이메일/푸시 알림 | 공격 조기 탐지, 피해자 인지 |
| **비밀번호 재설정/복구** | **안전한 토큰** | 암호학적으로 안전한 랜덤 토큰 (32바이트+), 1회용, 짧은 만료(15~30분), 사용 즉시 무효화 | 토큰 예측/재사용 방지 |
| | **다중 채널 인증** | 이메일 + SMS/푸시 동시 요구, 보안 질문(답변 해시 저장) | 단일 채널 탈취 시에도 방어 |
| **토큰/JWT 보안** | **강력한 서명/검증** | RS256/ES256 (비대칭), 시크릿 256비트+, `alg` 강제 지정, `none` 알고리즘 거부 | 알고리즘 혼란/위조 방지 |
| | **짧은 만료/리프레시 토큰 로테이션** | Access Token 15~30분, Refresh Token 1회용 + 로테이션 + 감시 | 토큰 탈취 시 피해 최소화 |
| **모니터링/탐지** | **이상 로그인 탐지** | 새 기기/위치/시간/ISP/브라우저 지문 변경 시 알림/차단 | UEBA(User and Entity Behavior Analytics) |
| | **실패 로그/알림** | 연속 실패 IP/계정/사용자 기록, 임계값 초과 시 SIEM/SOAR 연계 | 조기 탐지, 자동 대응 |

### 프레임워크/언어별 안전한 인증 구현 체크리스트

| 프레임워크 | 핵심 보안 기능 | 설정 예시 |
|-----------|----------------|-----------|
| **Django** | 내장 인증 시스템, `django-allauth`, `django-rest-framework-simplejwt` | `AUTH_PASSWORD_VALIDATORS`, `SESSION_COOKIE_SECURE=True`, `CSRF_COOKIE_SAMESITE='Strict'` |
| **Spring Security** | `PasswordEncoder`(BCrypt/Argon2), `SessionManagementFilter`, `OAuth2ResourceServer` | `SecurityFilterChain`, `BCryptPasswordEncoder(12)`, `JwtAuthenticationFilter` |
| **Node.js (Express)** | `bcryptjs`/`argon2`, `express-session` + `connect-redis`, `passport.js`, `express-rate-limit` | `session: {secure: true, httpOnly: true, sameSite: 'strict'}`, `helmet()` |
| **ASP.NET Core** | `Identity`, `JwtBearer`, `DataProtection`, `Antiforgery` | `services.AddIdentity<>(), .AddAuthentication(JwtBearerDefaults.AuthenticationScheme)` |
| **Go** | `golang.org/x/crypto/bcrypt`, `golang.org/x/crypto/argon2`, `gorilla/sessions`, `go-jwt-middleware` | `bcrypt.GenerateFromPassword(pwd, bcrypt.DefaultCost)` |

### 주요 Broken Authentication 사고 사례

| 사고 | 연도 | 공격 벡터 | 피해 |
|------|------|-----------|------|
| **Yahoo** | 2013-2014 | 약한 해시(MD5), 비밀번호 힌트 노출, 세션 쿠키 위조 | 30억 계정 유출 (역대 최대) |
| **LinkedIn** | 2012 | SHA1 단일 해시, 솔트 없음 | 1억 6,400만 계정 해시 유출 |
| **Adobe** | 2013 | 3DES ECB 모드 암호화(복호화 가능), 비밀번호 힌트 평문 저장 | 1억 5,300만 계정 유출 |
| **Dropbox** | 2012 | 직원 계정 크리덴셜 스터핑 → 내부 문서 접근 | 6,800만 계정 유출 |
| **MyFitnessPal** | 2018 | bcrypt(일부 SHA1) 해시, 이메일/비번 유출 | 1억 5,000만 계정 유출 |
| **Facebook** | 2018 | "View As" 기능 버그 → 액세스 토큰 탈취 | 5,000만 계정 토큰 유출 (세션 관리 결함) |

### 관련 표준 및 참고

| 표준/문서 | 내용 |
|----------|------|
| **OWASP Top 10 2021 A07** | Identification and Authentication Failures |
| **OWASP Authentication Cheat Sheet** | 인증 구현 종합 가이드 |
| **NIST SP 800-63B** | 디지털 인증 가이드라인 (비밀번호, MFA, 세션 등) |
| **NIST SP 800-63C** | 페더레이션/어설션 가이드라인 (OAuth/OIDC/SAML) |
| **CWE-287** | Improper Authentication |
| **CWE-384** | Session Fixation |
| **CWE-306** | Missing Authentication for Critical Function |

---

## 관련 위키 링크

- [[csrf]] — CSRF (비밀번호 변경 시 CSRF로 인증 우회 가능)
- [[ssrf]] — SSRF (인증 우회 후 내부망 접근 체인)
- [[xxe]] — XXE (인증 우회 후 파일 읽기/SSRF 체인)
- [[rce]] — RCE (인증 우회 후 관리자 기능으로 RCE 체인)
- [[actions-on-objectives]] — 목표 달성 (계정 탈취가 최종 목적 달성 첫 단계)
- [[real-world-breach-cases]] — 실제 침해 사례 (Yahoo, LinkedIn, Adobe 등 사례 분석)
- [[web-ctf-writeup-auth-session]] — Web CTF writeup에서 인증/세션/권한 분류 허브
- [[idor-ctf-patterns]] — IDOR CTF 패턴과 인증 결함의 연결 지점

---

## 참고 문헌

- 한국어 위키백과: [인증 (컴퓨터)](https://ko.wikipedia.org/wiki/인증_(컴퓨터))
- OWASP: [Broken Authentication](https://owasp.org/www-community/attacks/Authentication_bypass)
- OWASP Top 10 2017: [A2 Broken Authentication](https://owasp.org/www-project-top-ten/2017/A2_2017-Broken_Authentication)
- OWASP Top 10 2021: [A07 Identification and Authentication Failures](https://owasp.org/Top10/A07_2021-Identification_and_Authentication_Failures)
- PortSwigger: [Authentication vulnerabilities](https://portswigger.net/web-security/authentication)
- NIST SP 800-63B: [Digital Identity Guidelines - Authentication](https://pages.nist.gov/800-63-3/sp800-63b.html)