---
title: Broken Authentication (인증 체계 결함) — 보안 용어 해설
created: 2026-06-12
updated: 2026-06-24
type: concept
tags: [security, glossary, web, broken-auth, authentication, session, owasp, credential-stuffing, brute-force, mfa-bypass]
sources: [https://ko.wikipedia.org/wiki/인증, https://ko.wikipedia.org/wiki/OWASP]
confidence: high
---

# Broken Authentication (인증 체계 결함) — 보안 용어 해설

## 참고 URL
- [ko.wikipedia.org](https://ko.wikipedia.org/wiki/인증)
- [ko.wikipedia.org](https://ko.wikipedia.org/wiki/OWASP)

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

## 심화 자료
- [[broken-auth-mitigation-and-cases]] — 결함 유형, 방어 기법, 사례, 표준 정리

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
