---
title: Broken Access Control — 방어
created: 2026-06-12
updated: 2026-06-21
type: concept
tags: [security, glossary, web, broken-access-control, access-control, authorization, idor, privilege-escalation, owasp]
sources: [https://ko.wikipedia.org/wiki/접근_제어, https://ko.wikipedia.org/wiki/OWASP]
confidence: high
---
> [[broken-access-control]]의 후반부입니다.

## 참고 URL
- [ko.wikipedia.org](https://ko.wikipedia.org/wiki/접근_제어)
- [ko.wikipedia.org](https://ko.wikipedia.org/wiki/OWASP)

## Step 3: 전문 용어 설명 (위키백과/OWASP/PortSwigger 기반)
### Broken Access Control 방어 기법 (심층 방어)

| 방어 계층 | 기법 | 구현 예시 | 효과/비고 |
|----------|------|-----------|-----------|
| **설계/아키텍처 (최우선)** | **기본 거부 (Deny by Default)** | 모든 엔드포인트 기본 차단, 명시적 허용만 | **가장 확실** — 기본 철학 |
| | **중앙화된 접근 제어** | 모든 권한 검사 단일 모듈/미들웨어로 집중 | 일관성/유지보수성 |
| | **RBAC/ABAC 모델링** | 역할/속성 기반 정책 정의 (`can(user, action, resource)`) | 복잡한 권한 모델 대응 |
| **코드/구현 (필수)** | **모든 엔드포인트 인가 검사** | `@require_permission('read:order')`, `if user.can('view', order):` | **필수** — 미들웨어/데코레이터로 일관 적용 |
| | **소유권/관계 검증** | `if resource.owner_id != user.id && !user.is_admin: abort(403)` | IDOR 원천 차단 |
| | **서버 사이드 권한 검증** | 클라이언트 측 체크만 하지 말고 **서버에서 재검증** | 클라이언트 우회 방지 |
| **세션/토큰** | **JWT 클레임 검증** | `role:admin` 클레임 검증, `scope` 기반 권한 | 무상태 API 보호 |
| | **세션 무효화/갱신** | 권한 변경 시 즉시 세션 갱신/강제 로그아웃 | 권한 변경 즉시 반영 |
| **API/엔드포인트** | **기본 경로 보호** | `/admin/*`, `/api/admin/*`, `/internal/*` 기본 차단 | 관리자 경로 원천 보호 |
| | **HTTP 메소드별 권한** | `GET` 허용, `POST/PUT/DELETE` 별도 권한 | 메소드별 세분화 |
| | **API 버전별 일관성** | v1, v2 등 모든 버전에서 동일 권한 적용 | 버전 간 우회 차단 |
| **프론트엔드 (보조)** | **UI 요소 조건부 렌더링** | 관리자 메뉴 숨김, 버튼 비활성화 | UX + 1차 방어 (우회 가능) |
| | **네비게이션 가드** | 라우터 가드로 권한 없는 라우트 차단 | SPA 보호 |
| **모니터링/탐지** | **비정상 접근 패턴 탐지** | 403/404 다발, 비정상 경로 접근, 권한 상승 시도 | SIEM/UEBA 연계 |
| | **접근 로그/감사** | 누가/언제/어떤 자원에 접근/시도했는지 완전 기록 | 사후 추적/컴플라이언스 |
| **테스트/검증** | **자동화된 접근 제어 테스트** | OWASP ZAP, Burp Suite, 커스텀 테스트 스위트 | CI/CD 파이프라인 통합 |
| | **권한 매트릭스 검증** | 역할×리소스×액션 매트릭스 전체 테스트 | 누락 방지 |

### 언어/프레임워크별 접근 제어 구현 패턴

| 프레임워크 | 핵심 구현 패턴 |
|-----------|----------------|
| **Django** | `@permission_required`, `@user_passes_test`, `UserPassesTestMixin`, Django Guardian |
| **Spring Security** | `@PreAuthorize`, `@Secured`, `@RolesAllowed`, `SecurityFilterChain` |
| **Node.js (Express)** | `helmet()`, 커스텀 미들웨어 `requirePermission()`, `casl` 라이브러리 |
| **ASP.NET Core** | `[Authorize(Roles="Admin")]`, `IAuthorizationService`, Policy-based auth |
| **Go** | `casbin` RBAC/ABAC, 미들웨어 `authz.RequirePermission()` |
| **FastAPI** | `Depends(get_current_user)`, `Security(scopes=["admin"])` |
| **GraphQL** | `@auth` directive, `shield`, `graphql-shield` |
| **Laravel** | `Gate`, `Policy`, `@can`, `authorize()` |

### 주요 Broken Access Control 사고 사례

| 사고 | 연도 | 공격 벡터 | 피해 |
|------|------|-----------|------|
| **First American Financial** | 2019 | 문서 ID 순회 (`/api/documents/123` → 순회) | 8.85억 건 모기지 문서 유출 |
| **Facebook** | 2018 | `user_id` 파라미터 조작으로 타인 사진 접근 | 5,000만 계정 사진 유출 가능성 |
| **Instagram** | 2018 | `media_id` 조작으로 비공개 콘텐츠 접근 | 버그바운티 $10,000+ |
| **T-Mobile** | 2021 | API 인가 검증 누락으로 고객 데이터 접근 | 4,700만 고객 데이터 유출 |
| **LinkedIn** | 2021 | GraphQL 권한 검증 누락 | 7억 사용자 데이터 스크래핑 |
| **Twitter** | 2022 | API 권한 검증 누락으로 비공개 트윗/리스트 접근 | 540만 사용자 데이터 유출 |
| **Optus (호주 통신사)** | 2022 | 인증 없는 API 엔드포인트 | 1,000만 고객 개인정보 유출 |

### 관련 표준 및 참고

| 표준/문서 | 내용 |
|----------|------|
| **OWASP Top 10 2021 A01** | Broken Access Control |
| **OWASP Authorization Cheat Sheet** | 인가 구현 종합 가이드 |
| **OWASP Access Control Testing Guide** | 접근 제어 테스트 방법론 |
| **CWE-284** | Improper Access Control |
| **CWE-285** | Improper Authorization |
| **CWE-639** | Authorization Bypass Through User-Controlled Key |
| **NIST SP 800-53 AC-3** | Access Enforcement |

---


## 관련 위키 링크

- [[idor]] — IDOR (Broken Access Control의 대표적 하위 유형)
- [[broken-auth]] — Broken Authentication (인증/인가 결함 상위 개념)
- [[path-traversal]] — Path Traversal (파일 시스템 접근 제어 결함)
- [[privilege-escalation]] — Privilege Escalation (권한 상승의 결과)
- [[real-world-breach-cases]] — 실제 침해 사례 (First American, Facebook, LinkedIn 등)
- [[exploitation]] — 익스플로잇 (접근 제어 우회 후 포스트 익스플로잇)

---

## 참고 문헌

- 한국어 위키백과: [접근 제어](https://ko.wikipedia.org/wiki/접근_제어)
- OWASP Top 10 2021: [A01 Broken Access Control](https://owasp.org/Top10/A01_2021-Broken_Access_Control)
- OWASP Authorization Cheat Sheet: [Authorization Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html)
- PortSwigger: [Access control vulnerabilities](https://portswigger.net/web-security/access-control)
- NIST SP 800-53 AC-3: [Access Enforcement](https://csrc.nist.gov/projects/risk-management/sp-800-53-controls)
## 관련 위키 링크
- [[broken-access-control]] — 인덱스 페이지
- [[broken-access-control-core]] — 분할 페이지
- [[rce]]
