---
title: Broken Access Control — 핵심
created: 2026-06-12
updated: 2026-06-13
type: concept
tags: [security, glossary, web, broken-access-control, access-control, authorization, idor, privilege-escalation, owasp]
sources: [https://ko.wikipedia.org/wiki/접근_제어, https://ko.wikipedia.org/wiki/OWASP]
confidence: high
---

# Broken Access Control (접근 제어 결함) — 보안 용어 해설

## Step 1: 단어 직역 및 쉬운 비유

### 1. 용어 풀이

**Broken Access Control** = **Broken** (망가진) + **Access** (접근) + **Control** (제어)

| 영어 단어 | 직역 | 의미 |
|-----------|------|------|
| **Broken** | 망가진, 고장난 | 제 기능을 못 함 |
| **Access** | 접근, 이용 | 자원에 도달/사용함 |
| **Control** | 제어, 통제 | 권한을 관리/제한함 |

### 2. 의미 조합

> **"사용자가 자신의 권한을 넘어선 자원/기능에 접근할 수 있도록, 접근 제어 메커니즘이 제대로 작동하지 않는 상태"**

### 3. 강력한 비유: "열쇠는 301호만 여는데, 마스터 키로 모든 방 문 따는 경비원"

```
┌────────────────────────────────────────────────────────────┐
│  상황: 호텔(앱)에서 투숙객(사용자)에게                      │
│  301호 열쇠(권한)만 줬는데,                                │
│  경비원(접근 제어)이 302호, 스위트룸, 관리자 사무실도       │
│  "어? 손님이네? 들어가세요~" 하고 다 열어줌               │
└────────────────────────────────────────────────────────────┘

🚪  **문 열림 시나리오 (Broken Access Control 공격 흐름)**

  ① **정상**: 301호 투숙객이 301호 문 열기
     - 요청: "내 방(301호) 들어갈게요"
     - 경비원: "네, 301호 키 있으시네. 들어가세요." ✓

  ② **공격 (수평 권한 상승)**: 301호 투숙객이 302호 문 열기
     - 요청: "302호도 잠깐 볼게요"
     - 경비원: "어? 손님이네? 들어가세요~" 🚨 **수평 권한 상승**

  ③ **공격 (수직 권한 상승)**: 301호 투숙객이 관리자 사무실 문 열기
     - 요청: "관리자 사무실 좀 볼게요"
     - 경비원: "어? 손님이네? 들어가세요~" 🚨 **수직 권한 상승**

  ④ **공격 (기능 레벨)**: 일반 사용자가 관리자 API 호출
     - 요청: `DELETE /api/admin/users/123`
     - 서버: "어? 로그인했네? 실행해드릴게요~" 🚨 **기능 레벨 접근 제어 누락**

💡 **핵심 포인트**: 
- **인증(Authentication) ≠ 인가(Authorization)** — "누구냐" ≠ "뭐 할 수 있냐"
- **OWASP Top 10 2021 1위 (A01)** — 가장 빈번하고 치명적인 웹 취약점
- **IDOR, 기능 레벨 접근 제어 누락, 디렉토리 순회** 모두 Broken Access Control의 하위 유형
```

---

## Step 2: 개념 시각화

![Broken Access Control 비유 시각화: 호텔 경비원으로 설명하는 접근 제어 결함 — 프런트(서버), 301호 열쇠(정상 권한), 302호/스위트룸/관리자실(무단 접근 영역), 경비원(접근 제어 시스템), 고객(공격자) - 한글 레이블 포함](https://v3b.fal.media/files/b/0a9dfef4/KqR2mKxL5vN8tYpHgJkB4_L9wEmVnA.png)

**이미지 설명**:
- **프런트(서버)** — 접근 요청을 처리하는 애플리케이션
- **301호 열쇠(정상 권한)** — 사용자에게 정식으로 부여된 접근 권한
- **302호/스위트룸/관리자실(무단 접근 영역)** — 타인 데이터, 관리자 기능, 민감 자원
- **경비원(접근 제어 시스템)** — "이 사용자가 이 자원에 접근 권한이 있는가?" 검증해야 할 시스템
- **고객(공격자)** — 자신의 권한을 넘어 타인 자원/관리자 기능에 접근하려는 악의적 사용자

> ⚠️ **참고**: 이미지 생성 도구가 PNG 형식으로 반환했습니다. 스킬 요구사항(.jpg/.jpeg)은 현재 도구 제약상 PNG로 대체됩니다.

---

## Step 3: 전문 용어 설명 (위키백과/OWASP/PortSwigger 기반)
### Broken Access Control (접근 제어 결함)

**정의**: **Broken Access Control(접근 제어 결함)**은 애플리케이션이 **인증된 사용자가 자신의 권한 범위를 넘어선 자원(데이터, 기능, 관리자 패널 등)에 접근할 수 있도록, 접근 제어(Authorization/Access Control) 메커니즘이 누락되거나 잘못 구현되어 있는 상태**를 말한다. OWASP Top 10 **2021년 1위 (A01: Broken Access Control)** 로 선정될 만큼 가장 빈번하고 영향력이 큰 웹 애플리케이션 취약점이다.

### 접근 제어의 두 축: 인증 vs 인가

| 구분 | **인증 (Authentication)** | **인가 (Authorization/Access Control)** |
|------|---------------------------|----------------------------------------|
| **질문** | "당신은 누구인가?" | "당신은 무엇을 할 수 있는가?" |
| **대상** | 신원 확인 (아이디/비번, 토큰, 생체) | 권한 확인 (역할, 소유권, 정책) |
| **시점** | 로그인 시 (세션 시작) | **매 요청마다** (모든 엔드포인트) |
| **실패 시** | 401 Unauthorized | **403 Forbidden** |
| **Broken Access Control** | 인증 우회, 세션 하이재킹 | **권한 우회, IDOR, 기능 레벨 접근 제어 누락** |

> **핵심**: **"로그인했으면 다 된다"는 착각** — 인증된 사용자도 **자신의 권한 범위 내**에서만 접근해야 함.

### 주요 Broken Access Control 유형 (OWASP 분류)

| 유형 | 설명 | 공격 예시 | CWE |
|------|------|-----------|-----|
| **IDOR (Insecure Direct Object Reference)** | 객체 ID 직접 참조로 타인 데이터 접근 | `/api/users/123/profile` → `124` 변경 | CWE-639 |
| **기능 레벨 접근 제어 누락 (Missing Function Level Access Control)** | 관리자/특권 기능에 인가 검사 없음 | `GET /api/admin/users` 일반 사용자 접근 | CWE-285 |
| **강제 브라우징 (Forced Browsing)** | 비공개 URL 직접 접근 | `/admin`, `/api/internal/debug`, `/backup.zip` | CWE-425 |
| **디렉토리 순회/파일 접근** | Path Traversal으로 파일 시스템 접근 | `../../../etc/passwd`, `/admin/backup.sql` | CWE-22 |
| **수평/수직 권한 상승** | 동일/상위 권한 데이터/기능 접근 | 타인 주문 조회, 관리자 패널 접근 | CWE-284 |
| **CORS/CSRF를 통한 우회** | 출처 검증 누락으로 타인 세션에서 요청 위조 | 악성 사이트에서 관리자 API 호출 | CWE-942 |
| **JWT/토큰 권한 검증 누락** | 클레임(role, scope) 검증 안 함 | `role:user` 토큰으로 `admin` 기능 호출 | CWE-345 |
| **메타데이터/매개변수 조작** | 숨겨진 파라미터/헤더 조작으로 권한 우회 | `role=admin`, `is_admin=true` 헤더 추가 | CWE-23 |

### 주요 공격 시나리오 및 페이로드

| 시나리오 | 요청 예시 | 결과 |
|----------|-----------|------|
| **IDOR (수평)** | `GET /api/orders/1001` → `1002` | 타인 주문 내역/주소/결제정보 유출 |
| **IDOR (수직)** | `GET /api/users/123` → `GET /api/admin/users` | 관리자 사용자 목록/관리 기능 접근 |
| **기능 레벨** | `DELETE /api/users/999` (일반 유저) | 타인 계정 삭제 |
| **강제 브라우징** | `GET /admin`, `/api/internal/debug`, `/backup/db.sql` | 관리자 패널, 디버그 엔드포인트, 백업 파일 접근 |
| **파라미터 조작** | `POST /api/transfer {from:123, to:456}` → `from:999` | 타인 계좌에서 출금 |
| **헤더/쿠키 조작** | `X-User-Role: admin`, `X-User-ID: 999` | 권한 상승 |
| **GraphQL** | `query { adminUsers { email } }` | 관리자만 조회 가능 필드 유출 |
| **파일 업로드/다운로드** | `GET /download?file=../../config.php` | 소스코드/설정파일 유출 |


## 관련 위키 링크
- [[broken-access-control]] — 인덱스 페이지
- [[broken-access-control-defense]] — 분할 페이지
- [[rce]]
