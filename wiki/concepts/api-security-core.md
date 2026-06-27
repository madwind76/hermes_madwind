---
title: API Security (API 보안) — 핵심 메커니즘
created: 2026-06-13
updated: 2026-06-21
type: concept
tags: [security, api, api-security, authentication, authorization, rate-limiting]
sources: [https://owasp.org/www-project-api-security/, https://owasp.org/API-Security/editions/2023/en/0x11-t10/]
confidence: high
---

# API Security (API 보안) — 핵심 메커니즘

> [[api-security]]의 핵심 개념과 방어 아키텍처를 다루는 분할 페이지입니다.

## 참고 URL
- [owasp.org](https://owasp.org/www-project-api-security/)
- [owasp.org](https://owasp.org/API-Security/editions/2023/en/0x11-t10/)

## Step 3: 전문 용어 설명 (OWASP/PortSwigger/업계 표준 기반)
### API Security (API 보안)

**정의**: **API Security(API 보안)**은 **API(Application Programming Interface)의 설계, 개발, 배포, 운영 전 생애주기에서 발생할 수 있는 보안 위협을 식별하고 완화하여, API를 통해 노출되는 데이터의 기밀성/무결성/가용성(CIA)과 API 제공자의 인프라를 보호하는 종합적인 보안 체계**이다.

### OWASP API Security Top 10 (2023 버전)

| 순위 | ID | 위협 | 설명 |
|------|----|------|------|
| **1** | **API1:2023** | **Broken Object Level Authorization (BOLA)** | 객체 ID 직접 참조로 타인 데이터 접근 (IDOR) |
| **2** | **API2:2023** | **Broken Authentication** | 인증 메커니즘 결함 (토큰 탈취, 약한 비밀번호, 세션 관리 결함) |
| **3** | **API3:2023** | **Broken Object Property Level Authorization** | 민감 속성 과다 노출/수정 (Mass Assignment, Overposting) |
| **4** | **API4:2023** | **Unrestricted Resource Consumption** | 레이트 리미트 없음, 페이지네이션 없음, 대용량 파일 업로드 등 DoS |
| **5** | **API5:2023** | **Broken Function Level Authorization** | 관리자/특권 기능에 인가 검사 없음 (수직 권한 상승) |
| **6** | **API6:2023** | **Unrestricted Access to Sensitive Business Flows** | 비즈니스 로직 우회 (쿠폰 중복 사용, 주문 우회 등) |
| **7** | **API7:2023** | **Server Side Request Forgery (SSRF)** | 사용자 입력 URL로 내부망/메타데이터 접근 |
| **8** | **API8:2023** | **Security Misconfiguration** | 기본 설정, 불필요한 기능 활성화, 상세 에러 메시지, CORS 오류 |
| **9** | **API9:2023** | **Improper Inventory Management** | 구버전/미사용/문서화되지 않은 API 엔드포인트 방치 |
| **10** | **API10:2023** | **Unsafe Consumption of APIs** | 서드파티 API 응답 검증 없이 신뢰, 공급망 공격 |

> **참고**: 2019 버전 대비 **BOLA(1위)**, **인증/인가 분리**, **비즈니스 로직**, **SSRF**, **공급망** 등 현대 API 위협 반영

### API 보안 핵심 영역별 상세

| 영역 | 핵심 위협 | 핵심 방어 |
|------|-----------|-----------|
| **인증 (Authentication)** | 토큰 탈취, 약한 비밀번호, 세션 고정, 자격증명 스터핑 | 강력한 비밀번호 정책, MFA, 토큰 만료/갱신, JWT 서명 검증, JWKS 로테이션 |
| **인가 (Authorization)** | BOLA(IDOR), 기능 레벨 권한 상승, 과도한 권한 | RBAC/ABAC, 객체 레벨 권한 검사, 최소 권한 원칙 |
| **입력 검증/데이터 무결성** | 인젝션(SQLi, Command, LDAP), XSS, 역직렬화, Mass Assignment | 스키마 검증(JSON Schema, Protobuf), 허용 목록, 새니타이징 |
| **레이트 리미팅/DoS** | 무제한 요청, 대용량 페이로드, 무한 페이지네이션 | 토큰 버킷, 고정/슬라이딩 윈도우, 적응형 제한, 페이지네이션 강제 |
| **데이터 보호** | 과다 노출(Overposting), 민감 정보 누출, PII 유출 | 필드 레벨 권한, 응답 필터링, 민감 데이터 마스킹/암호화 |
| **전송 보안** | MITM, 인증서 검증 누락, 다운그레이드 공격 | **TLS 1.2+ 강제**, HSTS, 인증서 핀닝, mTLS |
| **CORS/출처 제어** | 과도한 허용(`*`), 자격증명 포함 오류, 프리플라이트 우회 | 정확한 오리진 화이트리스트, `credentials: include` 주의 |
| **공급망/서드파티** | 서드파티 API 응답 신뢰, 공급망 공격 | 응답 검증, 스키마 검증, 서킷 브레이커, 타임아웃 |
| **모니터링/감사** | 이상 탐지 불가, 포렌식 불가 | 구조화된 로그, 실시간 알림, SIEM 연계, 분산 추적 |
| **수명주기/거버넌스** | 좀비 API, 문서 미비, 버전 관리 부재 | API 게이트웨이, 카탈로그, 버전 관리, 폐기 정책 |

### OWASP API Security Top 10 (2023) 상세 대응

| # | 위협 | 핵심 대응 |
|---|------|-----------|
| **API1: BOLA** | 객체 ID 직접 참조로 타인 데이터 접근 | **모든 객체 접근 시 소유권/권한 검증** (`user.can('read', resource)`) |
| **API2: 인증** | 토큰 탈취, 세션 하이재킹, 약한 비밀번호 | **강력한 비밀번호 정책, MFA, JWT 짧은 만료/리프레시 로테이션, JWKS 로테이션** |
| **API3: 속성 레벨 권한** | 민감 필드 과다 노출/수정 (Overposting/Mass Assignment) | **필드 레벨 권한**, DTO/시리얼라이저로 화이트리스트 필드만 허용 |
| **API4: 자원 소모** | 레이트 리미트 없음, 대용량 업로드, 무한 페이지네이션 | **레이트 리미팅(토큰 버킷)**, 페이지네이션 강제, 업로드 크기/타입 제한 |
| **API5: 기능 레벨 권한** | 관리자 API 일반 사용자 접근 | **RBAC/ABAC**, 엔드포인트별 역할/권한 검사 미들웨어 |
| **API6: 비즈니스 플로우** | 쿠폰 중복, 주문 우회, 결제 우회 | **비즈니스 로직 검증**, 멱등성 키, 상태 머신 기반 검증 |
| **API7: SSRF** | 사용자 입력 URL로 내부망 접근 | **URL 화이트리스트**, 내부 IP 차단, `allow_url_include=Off` |
| **API8: 설정 오류** | 기본값, 상세 에러, CORS `*`, 불필요한 HTTP 메소드 | **보안 헤더**, 에러 메시지 최소화, 정확한 CORS 오리진 |
| **API9: 인벤토리** | 좀비 API, 문서 없는 API, 구버전 방치 | **API 게이트웨이/카탈로그**, 버전 관리, 자동 문서화(Swagger), 폐기 정책 |
| **API10: 서드파티 소비** | 외부 API 응답 맹목적 신뢰 | **응답 스키마 검증**, 서킷 브레이커, 타임아웃, 서명 검증 |

### API 보안 아키텍처: 계층별 방어 (Defense in Depth)

| 계층 | 구성 요소 | 핵심 역할 |
|------|-----------|-----------|
| **네트워크/인프라** | WAF, API 게이트웨이, 방화벽, DDoS 보호, mTLS | 1차 차단, 트래픽 정제, 인증서 검증 |
| **게이트웨이/프록시** | API 게이트웨이(Kong, Kong, Apigee, AWS API GW, Kong, Envoy) | 인증/인가 중앙화, 레이트 리밋, 라우팅, 변환 |
| **애플리케이션** | 프레임워크 미들웨어, 미들웨어 체인 | 인증/인가 미들웨어, 입력 검증, 레이트 리밋, 로깅 |
| **비즈니스 로직** | 서비스 레이어, 도메인 모델 | 비즈니스 규칙 검증, 상태 머신, 멱등성 |
| **데이터/스토리지** | ORM, 리포지토리, 암호화 | 필드 레벨 암호화, 컬럼 레벨 권한, 감시 |
| **관측성/운영** | 로깅, 메트릭, 추적, 알림, SIEM | 실시간 탐지, 포렌식, 컴플라이언스 |

### API 인증/인가 구현 패턴

| 방식 | 특징 | 적용 시나리오 | 보안 고려사항 |
|------|------|---------------|----------------|
| **API Key** | 단순, 헤더/쿼리로 전달 | 서드파티 공개 API, 서버간 통신 | **전송 중 암호화 필수(TLS)**, 로테이션, 스코프 제한 |
| **JWT (Bearer Token)** | Stateless, 클레임 포함 | SPA/모바일, 마이크로서비스 간 | **서명 검증(RS256/ES256)**, 짧은 만료(15-30분), 리프레시 토큰 로테이션 |
| **OAuth 2.0 / OIDC** | 표준 위임 인가, 스코프/동의 | 서드파티 접근, SSO, 모바일/웹 | **PKCE 필수**, 리다이렉트 URI 검증, State 파라미터 |
| **mTLS (Mutual TLS)** | 양방향 인증서 검증 | 마이크로서비스 간, 제로 트러스트 | 인증서 관리/로테이션 자동화 (SPIFFE/SPIRE, cert-manager) |
| **API Gateway JWT Validation** | 게이트웨이에서 중앙 검증 | API 게이트웨이 패턴 | **JWKS 캐싱**, 클레임 기반 라우팅/권한 |
| **API Key + HMAC** | 요청 서명으로 무결성 보장 | 서버간 중요 트랜잭션 | 타임스탬프/논스 포함, 리플레이 방지 |

### 레이트 리미팅 (Rate Limiting) 알고리즘 비교

| 알고리즘 | 동작 방식 | 장점 | 단점 | 적용 예시 |
|----------|-----------|------|------|-----------|
| **고정 윈도우 (Fixed Window)** | 시간 윈도우 내 요청 수 카운트 | 구현 단순, 메모리 적음 | 경계에서 버스트 허용 (2배 버스트) | 간단한 API, 내부 도구 |
| **슬라이딩 윈도우 (Sliding Window)** | 시간 윈도우를 슬라이드하며 카운트 | 경계 버스트 완화 | 메모리/연산 더 필요 | 일반 API |
| **토큰 버킷 (Token Bucket)** | 버킷에 토큰 채워지고 요청 시 소모 | **버스트 허용 + 평균 레이트 제어**, 부드러움 | 구현 복잡 | **가장 권장**, 외부 API |
| **누수 버킷 (Leaky Bucket)** | 일정 속도로 요청 처리, 큐에 쌓임 | 일정한 처리율 보장 | 버스트 처리 못함 | 스트리밍, 큐잉 시스템 |
| **슬라이딩 윈도우 로그** | 각 요청 타임스탬프 기록, 윈도우 내 개수 카운트 | **가장 정확** | 메모리/성능 비용 높음 | 엄격한 제한 필요 시 |

> **모범 사례**: **토큰 버킷 + 적응형 레이트 리미팅** (사용자/엔드포인트/권한별 차등) + **429 응답에 `Retry-After` 헤더** + **`X-RateLimit-Limit/Remaining/Reset` 헤더**

### CORS (Cross-Origin Resource Sharing) 보안 설정

| 설정 | 안전한 값 | 위험한 값 | 설명 |
|------|-----------|-----------|------|
| `Access-Control-Allow-Origin` | **구체적 오리진** (`https://app.example.com`) | `*` (와일드카드) | 자격증명 포함 시 `*` 불가 |
| `Access-Control-Allow-Credentials` | `true` (필요 시) | `false` (기본) | 쿠키/인증 헤더 포함 시 |
| `Access-Control-Allow-Methods` | 필요한 메소드만 (`GET, POST, PUT, DELETE`) | `*` 또는 불필요한 메소드 | 사전 요청(Preflight) 최적화 |
| `Access-Control-Allow-Headers` | 필요한 헤더만 (`Content-Type, Authorization, X-Request-ID`) | `*` | 불필요한 헤더 노출 방지 |
| `Access-Control-Expose-Headers` | 클라이언트 노출 필요 헤더만 | 모든 헤더 | 클라이언트 접근 제어 |
| `Access-Control-Max-Age` | `86400` (24시간) 등 | 너무 짧음/길음 | 프리플라이트 캐싱 최적화 |

> **핵심**: **`Access-Control-Allow-Origin: *` + `Access-Control-Allow-Credentials: true` = 조합 불가 (브라우저 차단)** — 구체적 오리진 필수

### API 보안 테스트 체크리스트

| 테스트 영역 | 체크 항목 |
|------------|-----------|
| **인증/인가** | BOLA 테스트(타인 객체 ID), 인가 우회(역할 변경), 토큰 탈취/재사용, JWT 서명/만료 검증 |
| **입력 검증** | SQLi/NoSQLi, Command Injection, XSS, XXE, 파일 업로드, 역직렬화, Mass Assignment |
| **레이트 리미팅** | 버스트 테스트, 429 응답 확인, `Retry-After` 헤더, 분산 공격 시뮬레이션 |
| **데이터 보호** | 과다 노출 필드(Overposting), 민감 정보 마스킹, PII 암호화, 응답 필터링 |
| **CORS/전송** | CORS 정책, TLS 1.2+, HSTS, 인증서 핀닝, CSP |
| **비즈니스 로직** | 멱등성, 상태 머신, 동시성 제어, 쿠폰/결제 우회 |
| **서드파티/공급망** | 외부 API 응답 검증, 서킷 브레이커, 타임아웃, 서명 검증 |
| **관측성** | 구조화 로그(JSON), 분산 추적(OpenTelemetry), 메트릭(RED: Rate, Errors, Duration), 알림 |
| **문서/거버넌스** | OpenAPI 3.0 스펙, 버전 관리, 폐기 정책, 변경 관리, 보안 연락처 |



## 관련 위키 링크
- [[api-security]] — API Security 메인 페이지
- [[api-security-defense]] — API 보안 실전 대응 페이지
- [[cors-misconfig]] — CORS 설정 오류
- [[broken-auth]] — 인증 체계 결함
