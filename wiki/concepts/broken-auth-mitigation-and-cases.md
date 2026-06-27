---
title: Broken Authentication — mitigation, tooling, and case notes
created: 2026-06-24
updated: 2026-06-24
type: concept
tags: [security, glossary, web, broken-auth, authentication, session, owasp, credential-stuffing, brute-force, mfa-bypass, jwt, login-bypass, session-riding]
sources: [https://ko.wikipedia.org/wiki/인증, https://ko.wikipedia.org/wiki/OWASP]
confidence: high
---

# Broken Authentication — mitigation, tooling, and case notes

## 주요 결함 유형
| 결함 분류 | 구체적 결함 | 공격 기법 | 영향 |
|----------|------------|----------|------|
| 약한 자격증명 정책 | 짧은/단순 비밀번호, 흔한 비밀번호 차단 없음 | 크리덴셜 스터핑, 패스워드 스프레이, 브루트포스 | 대량 계정 탈취 |
| 세션 관리 결함 | 예측 가능 세션 ID, 로그아웃 후 무효화 누락 | 세션 예측, 세션 고정 | 세션 하이재킹 |
| 인증 우회/논리 결함 | 재설정 토큰 예측 가능/재사용 가능 | 토큰 예측/재사용, 이메일/전화 우회 | 계정 탈취 |
| 브루트포스 방어 부재 | 시도 제한/잠금/CAPTCHA 없음 | 자동화 무차별 대입 | 대량 계정 탈취 |
| 취약한 구현/구성 | JWT 서명 검증 누락, OAuth/OIDC 구현 결함 | 토큰 위조, Redirect URI 우회 | 인증 우회 |

## 공격 시나리오별 예시
| 시나리오 | 공격 절차 | 피해 |
|----------|-----------|------|
| 크리덴셜 스터핑 | 유출 자격증명 자동 대입 | 동일 비밀번호 재사용 피해 |
| 패스워드 스프레이 | 사용자명 리스트에 공통 비번 소량 시도 | 계정 잠금 회피 |
| 세션 고정 | 공격자가 세션 ID를 주입 후 피해자 로그인 유도 | 같은 세션으로 접근 |
| 재설정 토큰 예측 | 토큰 형식을 추측하거나 시간 기반 브루트포스 | 비밀번호 재설정 탈취 |
| MFA 우회 | 푸시 피로, SIM 스와핑, 백업 코드 유출 | 2FA 우회 |
| JWT 알고리즘 혼란 | `alg:none` 또는 공개키 혼용 | 임의 토큰 위조 |

## 방어 기법
| 방어 영역 | 기법 | 구현 예시 | 효과/비고 |
|----------|------|-----------|-----------|
| 자격증명 정책 | 강력한 비밀번호 정책 | 최소 12자, 흔한 비밀번호 차단 | 재사용/추측 방지 |
| 비밀번호 해시 | Argon2id, bcrypt, scrypt, PBKDF2 | 평문/MD5/SHA1 저장 금지 | 유출 시 피해 최소화 |
| 다단계 인증 | TOTP, FIDO2/WebAuthn, passkey | SMS OTP 의존 최소화 | 피싱 저항성 향상 |
| 세션 관리 | Secure/HttpOnly/SameSite, 재발급, 타임아웃 | 로그인 시 새 세션 ID 발급 | 고정/하이재킹 방지 |
| 브루트포스 방어 | Rate limiting, CAPTCHA, 계정 잠금 | IP/사용자별 시도 제한 | 자동화 차단 |
| 재설정/복구 | 1회용 랜덤 토큰, 짧은 만료 | 사용 즉시 무효화 | 재사용 방지 |
| 토큰/JWT 보안 | 강한 서명, `alg` 강제, 짧은 만료 | access/refresh 분리 | 위조/탈취 피해 축소 |
| 모니터링 | 이상 로그인 탐지, 실패 로그/알림 | UEBA, SIEM 연계 | 조기 탐지 |

## 프레임워크별 안전한 구현 체크리스트
| 프레임워크 | 핵심 보안 기능 | 설정 예시 |
|-----------|----------------|-----------|
| Django | 내장 인증, allauth, simplejwt | `AUTH_PASSWORD_VALIDATORS`, `SESSION_COOKIE_SECURE=True` |
| Spring Security | PasswordEncoder, SessionManagement, OAuth2 | BCrypt, JwtAuthenticationFilter |
| Node.js (Express) | bcrypt/argon2, express-session, passport | `secure`, `httpOnly`, `sameSite` |
| ASP.NET Core | Identity, JwtBearer, Antiforgery | `AddIdentity`, `AddAuthentication` |
| Go | bcrypt, argon2, gorilla/sessions | `bcrypt.GenerateFromPassword(...)` |

## 주요 사고 사례
| 사고 | 연도 | 공격 벡터 | 피해 |
|------|------|-----------|------|
| Yahoo | 2013-2014 | 약한 해시, 세션 쿠키 위조 | 30억 계정 유출 |
| LinkedIn | 2012 | SHA1 단일 해시, 솔트 없음 | 1억 6,400만 계정 유출 |
| Adobe | 2013 | 3DES ECB, 평문 힌트 | 1억 5,300만 계정 유출 |
| Dropbox | 2012 | 직원 계정 크리덴셜 스터핑 | 내부 문서 접근 |
| MyFitnessPal | 2018 | 해시 유출 | 1억 5,000만 계정 유출 |
| Facebook | 2018 | View As 버그로 토큰 유출 | 5,000만 토큰 유출 |

## 관련 표준 및 참고
| 표준/문서 | 내용 |
|----------|------|
| OWASP Top 10 2021 A07 | Identification and Authentication Failures |
| OWASP Authentication Cheat Sheet | 인증 구현 종합 가이드 |
| NIST SP 800-63B | 비밀번호, MFA, 세션 가이드라인 |
| NIST SP 800-63C | 페더레이션/어설션 가이드라인 |
| CWE-287 | Improper Authentication |
| CWE-384 | Session Fixation |
| CWE-306 | Missing Authentication for Critical Function |

## 관련 위키 링크
- [[broken-auth]] — 상위 개념
- [[csrf]] — 인증 우회 체인
- [[ssrf]] — 내부망 접근 체인
- [[xxe]] — 파일 읽기/SSRF 체인
- [[rce]] — 관리자 기능 악용 체인
- [[actions-on-objectives]] — 계정 탈취 이후의 최종 피해 단계
- [[real-world-breach-cases]] — 실제 침해 사례
- [[web-ctf-writeup-auth-session]] — Web CTF 인증/세션/권한 허브
- [[idor-ctf-patterns]] — 인증 결함과 결합되는 패턴
