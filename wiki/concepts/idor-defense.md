---
title: IDOR — 방어
created: 2026-06-12
updated: 2026-06-13
type: concept
tags: [security, glossary, web, idor, broken-access-control, authorization, owasp, horizontal-privilege-escalation, vertical-privilege-escalation]
sources: [https://ko.wikipedia.org/wiki/OWASP, https://ko.wikipedia.org/wiki/접근_제어]
confidence: high
---
> [[idor]]의 후반부입니다.

## Step 3: 전문 용어 설명 (위키백과/OWASP/PortSwigger 기반)
### IDOR 방어 기법

| 방어 계층 | 기법 | 구현 예시 | 효과/비고 |
|----------|------|-----------|-----------|
| **인가 검사 (핵심)** | **모든 객체 접근 시 권한 검증** | `if resource.owner_id != current_user.id: abort(403)` | **가장 필수** — 모든 객체 접근 지점에서 필수 |
| | **역할 기반 접근 제어 (RBAC)** | `@require_role('admin')`, `current_user.can('delete', resource)` | 권한 세분화 |
| | **소유권/관계 기반 검증** | `if document.project.team_id not in current_user.team_ids: abort(403)` | 복잡한 권한 모델 대응 |
| **간접 참조 (Indirect Reference)** | **직접 ID 대신 매핑 토큰 사용** | `GET /api/documents/abc123` → 내부적으로 `doc_id=555` 매핑 | **가장 확실** — 실제 ID 노출 원천 차단 |
| | **세션/컨텍스트 기반 조회** | `GET /api/my/orders` → 세션의 `user_id`로 자동 필터링 | 사용자 입력 ID 완전 배제 |
| **객체 식별자 보호** | **예측 불가능한 식별자** | UUID v4, 암호학적 난수, 해시 기반 ID (`hashids`) | 순차 ID 열거 방지 |
| | **민감 ID 노출 최소화** | API 응답에 내부 ID 노출 안 함, 프론트엔드용 별도 키 사용 | 정보 노출 최소화 |
| **입력 검증** | **화이트리스트/권한 기반 필터링** | 사용자 권한 내 객체만 조회 가능하도록 쿼리 제한 (`WHERE user_id = ?`) | SQL 레벨 보호 |
| | **파라미터 타입/형식 검증** | UUID 형식 검증, 숫자 범위 검증 | 형식 위반 요청 차단 |
| **모니터링/탐지** | **비정상 접근 패턴 탐지** | 단시간 다수 ID 순회, 403/404 다발, 비정상 시간대 접근 | SIEM/UEBA 연계 |
| | **접근 로깅/감사** | 누가/언제/어떤 객체에 접근했는지 완전 기록 | 사후 추적/컴플라이언스 |
| **API 설계** | **RESTful하지 않은 안전한 엔드포인트** | `GET /api/orders` (내 주문만) vs `GET /api/orders/{id}` (타인 가능) | 설게 단계에서 예방 |
| | **GraphQL 권한 지시자** | `@directive @auth on FIELD_DEFINITION` | GraphQL 레벨 권한 제어 |

### IDOR 테스트 체크리스트

| 테스트 항목 | 확인 사항 |
|------------|-----------|
| **수평 권한 상승** | 내 객체 ID → 타인 객체 ID 변경 시 403/404 반환되는가? |
| **수직 권한 상승** | 일반 사용자 → 관리자/타인 권한 엔드포인트 접근 시 차단되는가? |
| **ID 열거** | 순차 ID(`1,2,3...`), UUID 열거 시 정보 유출되는가? |
| **다중 파라미터** | `user_id`, `account_id`, `document_id` 등 모든 객체 파라미터 테스트 |
| **메소드별 테스트** | GET(읽기), POST(생성), PUT/PATCH(수정), DELETE(삭제) 모두 테스트 |
| **GraphQL** | 쿼리/뮤테이션 변수 조작, 중첩 객체 접근 권한 |
| **파일/문서** | 다운로드/업로드/삭제 시 소유권 검증 |
| **API 버전** | v1, v2 등 버전별 권한 검증 일관성 |

### 주요 IDOR 사고 사례

| 사고 | 연도 | 공격 벡터 | 피해 |
|------|------|-----------|------|
| **Facebook** | 2018 | `user_id` 파라미터 조작으로 타인 사진/게시물 접근 | 5,000만 계정 사진 유출 가능성 |
| **Instagram** | 2018 | `media_id` 조작으로 비공개 사진/스토리 접근 | 버그바운티 $10,000+ |
| **Tinder** | 2019 | `user_id` 조작으로 매칭 상대 위치/개인정보 접근 | 위치 정보 유출 |
| **GitLab** | 2020 | `project_id` 조작으로 비공개 프로젝트/이슈 접근 | CVE-2020-10977 |
| **Shopify** | 2019 | `order_id` 조작으로 타인 주문/결제 정보 접근 | 버그바운티 $20,000+ |
| **Uber** | 2016 | `trip_id` 조작으로 타인 운행 기록/영수증 접근 | 버그바운티 $10,000+ |

### 관련 표준 및 참고

| 표준/문서 | 내용 |
|----------|------|
| **OWASP Top 10 2021 A01** | Broken Access Control (IDOR 포함) |
| **OWASP Authorization Cheat Sheet** | 인가 구현 가이드 |
| **CWE-639** | Authorization Bypass Through User-Controlled Key |
| **CAPEC-194** | Cloud Service Provider API Abuse (IDOR 유사) |

---


## 관련 위키 링크

- [[broken-auth]] — Broken Authentication (인가 결함의 상위 개념)
- [[path-traversal]] — Path Traversal (파일 경로 조작으로 IDOR 확장)
- [[broken-access-control]] — Broken Access Control (IDOR의 상위 카테고리)
- [[rce]] — RCE (IDOR로 관리자 기능 접근 후 RCE 체인)
- [[real-world-breach-cases]] — 실제 침해 사례 (Facebook, Instagram, GitLab 등 사례)
- [[exploitation]] — 익스플로잇 (IDOR → 데이터 유출/변조 → 포스트 익스플로잇)

---

## 참고 문헌

- 한국어 위키백과: [안전하지 않은 직접 객체 참조](https://ko.wikipedia.org/wiki/안전하지_않은_직접_객체_참조)
- OWASP: [Insecure Direct Object References](https://owasp.org/www-community/attacks/Insecure_Direct_Object_References)
- PortSwigger: [Insecure Direct Object References (IDOR)](https://portswigger.net/web-security/access-control/idor)
- OWASP Cheat Sheet: [Authorization](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html)
## 관련 위키 링크
- [[idor]] — 인덱스 페이지
- [[idor-core]] — 분할 페이지
- [[rce]]
