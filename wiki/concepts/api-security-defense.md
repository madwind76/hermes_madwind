---
title: API Security — 보안 용어 해설 (실전 대응)
created: 2026-06-13
updated: 2026-06-14
type: concept
tags: [security, api, api-security, waf, scanner]
sources: [https://owasp.org/www-project-api-security/, https://owasp.org/API-Security/editions/2023/en/0x11-t10/]
confidence: high
---

# API Security (API 보안) — 실전 대응

> [[api-security]]의 검증/도구/사고사례를 다루는 분할 페이지입니다.

## Step 3: 전문 용어 설명 (OWASP/PortSwigger/업계 표준 기반)
### API 보안 도구/프레임워크

| 카테고리 | 도구/프레임워크 |
|----------|----------------|
| **API 게이트웨이** | Kong, Apigee, AWS API Gateway, Azure API Management, Envoy, Traefik, KrakenD |
| **인증/인가 라이브러리** | Ory Kratos/Hydra, Keycloak, Auth0, Firebase Auth, Firebase Auth, Passport.js, Spring Security, .NET Identity |
| **레이트 리미팅** | Redis + Token Bucket, `express-rate-limit`, `slowapi`, `golang.org/x/time/rate`, Bucket4j |
| **입력 검증/스키마** | JSON Schema, Pydantic, Zod, Joi, validator.js, Cerberus, Go-playground/validator |
| **API 문서/테스트** | Swagger/OpenAPI 3.0, Postman, Insomnia, Hoppscotch, Schemathesis (자동 테스트) |
| **보안 스캐닝/테스트** | OWASP ZAP API Scan, Postman Test, Schemathesis, 42Crunch, APISpec Converter |
| **모니터링/관측성** | Prometheus/Grafana, Datadog, New Relic, Elastic APM, Jaeger/Zipkin (분산 추적) |
| **API 카탈로그/거버넌스** | Backstage, Stoplight, Apicurio, Gravitee, WSO2 |

### 주요 API 보안 사고 사례

| 사고 | 연도 | 벡터 | 피해 |
|------|------|------|------|
| **Facebook (Cambridge Analytica)** | 2018 | Graph API 과다 권한(`user_friends` 등) + 앱 검증 부재 | 8,700만 사용자 데이터 유출 |
| **T-Mobile** | 2021 | 인증 없는 API 엔드포인트 (`/api/v1/...`) | 4,700만 고객 데이터 유출 |
| **LinkedIn** | 2021 | GraphQL 권한 검증 누락 + 페이지네이션 없음 | 7억 사용자 데이터 스크래핑 |
| **Twitter** | 2022 | API 권한 검증 누락 + 엔드포인트 노출 | 540만 사용자 데이터 유출 |
| **Optus** | 2022 | 인증 없는 API 엔드포인트 | 1,000만 고객 개인정보 유출 |
| **Peloton** | 2021 | 인증 없는 사용자 프로필 API (`/api/user/{id}`) | 전 사용자 프로필 데이터 유출 |
| **John Deere** | 2022 | 인증 없는 트랙터 텔레메트리 API | 장비 위치/상태 데이터 노출 |

### 관련 표준 및 참고

| 표준/문서 | 내용 |
|----------|------|
| **OWASP API Security Top 10 (2023)** | API 보안 위협/대응 종합 가이드 |
| **OWASP API Security Project** | API 보안 종합 프로젝트 (가이드, 체크리스트, 툴) |
| **OWASP REST Security Cheat Sheet** | REST API 보안 구현 체크리스트 |
| **OWASP GraphQL Security Cheat Sheet** | GraphQL 보안 가이드 |
| **REST API Security Best Practices (Microsoft/Google/AWS)** | 클라우드 벤더별 모범 사례 |
| **NIST SP 800-207** | Zero Trust Architecture (API 게이트웨이/마이크로서비스 적용) |
| **RFC 6749/6750/7519/7523/7636/8414/8628/8705/8707** | OAuth 2.0, Bearer Token, JWT, JWK, PKCE, JARM, DPoP, OAuth 2.1 |
| **RFC 6454 / Fetch Standard** | Same-Origin Policy, CORS 상세 |

---



## 관련 위키 링크
- [[api-security]] — API Security 메인 페이지
- [[api-security-core]] — API 보안 핵심 메커니즘 페이지
- [[heap-dump-ctf-patterns]] — 진단 엔드포인트와 heap snapshot 노출 위험
- [[head-dump-final-writeup]] — picoCTF 2025 API 문서/heapdump 문제
- [[cors-misconfig]] — CORS 설정 오류
- WAF(Web Application Firewall) — 웹 방화벽
