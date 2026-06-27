---
title: IDOR (Insecure Direct Object Reference, 안전하지 않은 직접 객체 참조) — 보안 용어 해설
created: 2026-06-12
updated: 2026-06-21
type: concept
tags: [security, glossary, web, idor, broken-access-control, authorization, owasp, horizontal-privilege-escalation, vertical-privilege-escalation]
sources: [https://ko.wikipedia.org/wiki/OWASP, https://ko.wikipedia.org/wiki/접근_제어]
confidence: high
---

# IDOR (Insecure Direct Object Reference, 안전하지 않은 직접 객체 참조) — 보안 용어 해설

## 참고 URL
- [ko.wikipedia.org](https://ko.wikipedia.org/wiki/OWASP)
- [ko.wikipedia.org](https://ko.wikipedia.org/wiki/접근_제어)

## Step 1: 단어 직역 및 쉬운 비유

### 1. 용어 풀이

**IDOR** = **I**nsecure **D**irect **O**bject **R**eference

| 약자 | 원래 단어 | 직역 | 의미 |
|------|-----------|------|------|
| **I** | **Insecure** | 안전하지 않은, 불안전한 | 보안 검증이 없는 |
| **D** | **Direct** | 직접적인, 직통의 | 중개 없이 바로 |
| **O** | **Object** | 객체, 대상 | 데이터 레코드, 파일, 리소스 |
| **R** | **Reference** | 참조, 가리키기 | 식별자를 통해 접근 |

### 2. 의미 조합

> **"인가 검사 없이 객체 식별자(ID, 키, 경로 등)를 직접 사용하여, 권한 없는 사용자가 타인의 데이터에 접근/수정/삭제할 수 있게 하는 접근 제어 취약점"**

### 3. 강력한 비유: "열쇠 번호만 알면 아무 방이나 들어갈 수 있는 호텔"

```
┌────────────────────────────────────────────────────────────┐
│  상황: 호텔(애플리케이션)에서 투숙객(사용자)에게            │
│  301호 열쇠(객체 ID)만 줬는데, 마스터 키(인가 검사) 없이    │
│  302호, 303호, 스위트룸(타인 데이터)도 열쇠 번호만 바꿔서  │
│  마음대로 들어갈 수 있음                                    │
└────────────────────────────────────────────────────────────┘

🔑  **열쇠 번호 조작 시나리오 (IDOR 공격 흐름)**

  ① **정상 사용**: 로그인한 사용자가 본인 프로필 조회
     - 요청: `GET /api/users/12345/profile`
     - 서버: 세션 확인 → 본인 ID(12345) 확인 → 프로필 반환

  ② **공격자 악용**: ID 파라미터만 조작
     - 요청: `GET /api/users/12346/profile` (타인 ID)
     - 서버: **인가 검사 없음** → 12346번 프로필 그대로 반환!

  ③ **더 심각한 악용**:
     - `GET /api/orders/99999` → 타인 주문 내역/주소/결제정보 유출
     - `DELETE /api/documents/555` → 타인 중요 문서 삭제
     - `PUT /api/admin/users/999/role` → 권한 상승 (수직 권한 상승)
     - `POST /api/bank/transfer` with `from_account=12346` → 타인 계좌에서 이체

  ④ **대규모 자동화 (IDOR Enumeration)**:
     - Burp Intruder 등으로 ID 순회 (`12345` → `12346` → `12347`...)
     - 수천/수만 건 개인정보/주문/문서 자동 수집

💡 **핵심 포인트**: 
- **인증(Authentication) ≠ 인가(Authorization)** — 로그인했어도 **권한 검사**는 별도
- **객체 참조(ID, UUID, 경로 등)가 노출**되고 **서버 측 권한 검증**이 없으면 IDOR
- **수평 권한 상승(Horizontal)** — 동일 권한 타인 데이터 접근
- **수직 권한 상승(Vertical)** — 관리자/상위 권한 기능 접근
- **API 시대 더 치명적** — REST/GraphQL API에서 객체 ID 직접 노출 빈번
```

---

## Step 2: 개념 시각화

![IDOR 비유 시각화: 호텔 열쇠로 설명하는 IDOR — 프런트(서버), 301호 열쇠(정상 객체 ID), 302호/303호/스위트룸(타인 객체), 마스터 키 부재(인가 검사 없음), 고객(공격자) - 한글 레이블 포함](https://v3b.fal.media/files/b/0a9dfef4/KqR2mKxL5vN8tYpHgJkB4_L9wEmVnA.png)

**이미지 설명**:
- **프런트(서버)** — 객체 접근 요청을 처리하는 애플리케이션
- **301호 열쇠(정상 객체 ID)** — 사용자에게 정식으로 부여된 자신의 객체 식별자
- **302호/303호/스위트룸(타인 객체)** — 다른 사용자의 데이터 (프로필, 주문, 문서, 설정 등)
- **마스터 키 부재(인가 검사 없음)** — 객체 ID만 알면 접근 가능한 인가 로직 부재
- **고객(공격자)** — 자신의 객체 ID를 타인 것으로 조작하여 무단 접근하는 악의적 사용자

> ⚠️ **참고**: 이미지 생성 도구가 PNG 형식으로 반환했습니다. 스킬 요구사항(.jpg/.jpeg)은 현재 도구 제약상 PNG로 대체됩니다.

---

## Step 3: 전문 용어 설명 (위키백과/OWASP/PortSwigger 기반)
### IDOR (Insecure Direct Object Reference, 안전하지 않은 직접 객체 참조)

**정의**: **IDOR(Insecure Direct Object Reference)**는 애플리케이션이 **사용자 입력(객체 식별자: ID, UUID, 파일명, 경로 등)을 직접 사용하여 객체에 접근할 때, 해당 사용자가 해당 객체에 접근할 권한이 있는지 서버 측에서 검증하지 않아** 발생하는 **인가(Authorization) 결함**이다. OWASP Top 10 **2021년 A01 (Broken Access Control, 1위)**의 대표적인 유형이다.

### 공격 원리: 인가 검사 누락

| 단계 | 설명 |
|------|------|
| **1. 객체 식별자 노출** | URL 파라미터, 헤더, 쿠키, 바디, GraphQL 변수 등에서 객체 ID 직접 노출 |
| **2. 사용자 제어 가능** | 공격자가 객체 식별자(ID, UUID, 슬러그, 파일명 등) 임의 조작 가능 |
| **3. 서버 측 인가 검사 누락** | 서버가 "이 사용자가 이 객체에 접근 권한이 있는가?" 검증 안 함 |
| **4. 무단 접근/조작** | 공격자가 타인 객체 읽기/쓰기/삭제/실행 가능 |

### IDOR 공격 벡터 및 위치

| 위치 | 예시 | 설명 |
|------|------|------|
| **URL 경로 파라미터** | `/api/users/12345/profile`, `/orders/99999/detail` | REST API 경로 변수 |
| **쿼리 파라미터** | `?user_id=12345`, `?document_id=555` | GET/POST 쿼리 스트링 |
| **요청 바디** | `{"user_id": 12345, "action": "view"}`, `{"file_id": "doc_555"}` | JSON/XML 바디 |
| **헤더/쿠키** | `X-User-ID: 12345`, `document_id=doc_555` | 커스텀 헤더, 쿠키 값 |
| **GraphQL 변수** | `query { user(id: "12345") { ... } }` | GraphQL 쿼리 변수 |
| **파일 경로/이름** | `/download?file=../../../etc/passwd`, `filename=../../config.php` | Path Traversal과 결합 |
| **UUID/해시** | `/api/users/550e8400-e29b-41d4-a716-446655440000` | 예측 어려운 UUID도 열거/유출 시 위험 |

### IDOR 공격 유형

| 유형 | 설명 | 예시 | 권한 상승 구분 |
|------|------|------|----------------|
| **수평 권한 상승 (Horizontal)** | 동일 권한 수준의 타인 데이터 접근 | 내 주문(`order_id=100`) → 타인 주문(`order_id=101`) 조회 | 수평 |
| **수직 권한 상승 (Vertical)** | 상위 권한 필요 기능/데이터 접근 | 일반 사용자 → 관리자 패널(`/admin/users`), 타인 계정 삭제 | 수직 |
| **데이터 유출 (Data Exposure)** | 민감 정보 읽기 | 타인 프로필, 주문 내역, 의료 기록, 금융 정보 | 수평/수직 |
| **데이터 변조/삭제 (Data Manipulation)** | 타인 데이터 수정/삭제 | 타인 주문 취소, 문서 삭제, 프로필 수정 | 수평/수직 |
| **비즈니스 로직 우회** | 결제/승인 프로세스 우회 | `from_account` 파라미터 조작으로 타인 계좌에서 이체 | 수직 |

### IDOR 취약 코드 패턴

```python
# ❌ 취약: 인가 검사 없이 직접 객체 조회
@app.route('/api/users/<int:user_id>/profile')
def get_profile(user_id):
    user = User.query.get(user_id)  # 인가 검사 없음!
    return jsonify(user.to_dict())

# ❌ 취약: 파일 다운로드 시 경로 검증 없음
@app.route('/download')
def download_file():
    filename = request.args.get('file')
    return send_file(f'/var/www/uploads/{filename}')  # Path Traversal + IDOR

# ✅ 안전: 인가 검사 후 객체 조회
@app.route('/api/users/<int:user_id>/profile')
@login_required
def get_profile(user_id):
    if current_user.id != user_id and not current_user.is_admin:
        abort(403)  # 인가 검사!
    user = User.query.get_or_404(user_id)
    return jsonify(user.to_dict())

# ✅ 안전: 객체 소유권 확인
@app.route('/api/orders/<int:order_id>')
@login_required
def get_order(order_id):
    order = Order.query.get_or_404(order_id)
    if order.user_id != current_user.id and not current_user.is_admin:
        abort(403)  # 소유자만 접근 가능
    return jsonify(order.to_dict())
```


## 관련 위키 링크
- [[idor]] — 인덱스 페이지
- [[idor-defense]] — 분할 페이지
- [[rce]]
