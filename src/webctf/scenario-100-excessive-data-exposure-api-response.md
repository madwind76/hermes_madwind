---
title: Excessive Data Exposure — Web CTF Scenario
created: 2026-06-15
updated: 2026-06-15
type: ctf-scenario
tags: [ctf, web, api, excessive-data-exposure, information-disclosure, easy]
confidence: high
---

# Excessive Data Exposure (과도한 데이터 노출) — Web CTF Scenario

## 1. 개요 및 스토리
- **문제명**: Member Card Searcher (간이 회원 카드 조회기)
- **난이도**: Easy (초급)
- **핵심 컨셉**: 웹 화면(UI)단에서는 보이지 않지만, 백엔드 API가 클라이언트로 발송하는 원시 JSON 데이터 내에 과도하게 민감한 정보가 함께 포함되어 전송되는 **과도한 데이터 노출 (Excessive Data Exposure / API3:2019)** 취약점 문제입니다.
- 대상 웹 서비스는 가입된 회원의 닉네임과 가입 연도를 카드 형식으로 조회하여 표시해 주는 사용자 탐색 페이지를 운영 중입니다. 프론트엔드 자바스크립트는 API 서버로부터 특정 회원의 데이터를 수신해 카드 영역에 닉네임 문자열만을 바인딩해 출력합니다. 그러나 개발자는 백엔드 API를 구현할 때 데이터베이스 조회 결과를 필터링하지 않고 `SELECT *` 쿼리로 조회된 계정 레코드 배열 전체를 그대로 JSON 포맷으로 인코딩하여 반환했습니다. 공격자는 브라우저의 개발자 도구 Network 패널을 확인하여 화면 뒤에서 노출되는 원시 JSON 응답을 뜯어봄으로써 비공개 메모란에 담겨 있는 플래그를 취득할 수 있습니다.

---

## 2. 문제 설계 및 구조 (Architecture)

### 2.1 구성 요소
- **Member Search Card Web UI (`/members.html`)**:
  - 회원 닉네임을 보여주는 웹 UI 카드 페이지.
  - 검색 시 자바스크립트를 이용해 `/api/user_info.php?id=12` 에 동적 AJAX 호출을 전달하고 응답을 파싱해 이름만 전시.
- **REST API Endpoint (`/api/user_info.php`)**:
  - `?id=...` 파라미터를 받아 해당하는 유저 정보를 데이터베이스에서 로드해 JSON 객체로 반환.
- **Flag 위치**:
  - 데이터베이스 `users` 테이블 컬럼 중 일반 화면에는 출력되지 않는 비공개 컬럼 `api_secret_flag` 또는 `private_note`.

### 2.2 취약점 지점
1. **Unfiltered REST API Response (JSON Dump)**:
  - API 백엔드 소스에서 데이터베이스 계정 엔티티 필드를 일괄 직렬화(Serialize)하여 반환합니다:
    `echo json_encode($user_record_row);`
  - 클라이언트 개발자 도구의 네트워크 통신 모니터링 기능을 쓰면 가려져 있던 미렌더링 필드 데이터가 평문으로 모두 노출됩니다.
  - 보안 통제의 경계를 클라이언트의 UI단(가려진 CSS, 특정 필드만 렌더링하는 JS)에 둔 채 백엔드 전송 필터를 배제하여 발생합니다.

---

## 3. 공격 면 (Attack Surface)

| 엔드포인트 | 메소드 | 인증 | 파라미터 | 데이터 타입 | 취약 함수 및 태그 |
|------------|--------|------|----------|-------------|-------------------|
| `/api/user_info.php` | GET | 불필요 | `id` | Integer | `json_encode()` 등 API 데이터 일괄 덤프 전송부 |

---

## 4. 상세 풀이 흐름 (Exploitation Flow)

### Step 1. 회원 카드 조회 동작 확인
1. 회원 카드 목록 페이지인 `/members.html`에 접속합니다.
2. 회원 검색창에 임의의 번호를 대입하여 조회 카드를 띄웁니다.
3. 카드 상에는 오로지 해당 회원의 닉네임과 가입한 해 정보만 표시되는 심플한 UI 구성을 보입니다.

### Step 2. 브라우저 개발자 도구(F12) 기동 및 통신 분석
1. 키보드의 F12 키를 입력하여 브라우저 개발자 도구를 켜고 **Network(네트워크)** 탭으로 이동합니다.
2. 회원 카드를 재조회하여 발생하는 AJAX HTTP 통신 리퀘스트 엔드포인트를 찾아냅니다:
   `/api/user_info.php?id=1`
3. 탐지된 해당 호출 명세를 더블클릭하거나 우측의 'Response(응답)' 서브 패널로 전환하여 응답 상태 본문을 조회합니다.

### Step 3. 원시 JSON Response 구조 정밀 판독
1. 수신된 JSON 데이터 패킷을 분석합니다.
   ```json
   {
     "id": 1,
     "username": "superadmin",
     "join_year": "2025",
     "email": "admin@enterprise.local",
     "api_secret_flag": "FLAG{excessive_api_data_exposure_information_leak}",
     "internal_role": "SYSTEM_OWNER"
   }
   ```
2. 웹 페이지 UI 상에는 `username`과 `join_year` 두 가지만 보여서 렌더링되고 있었으나, 백엔드로부터 전송된 JSON 원문에는 비공개 이메일 주소 및 `api_secret_flag` 데이터가 원시적으로 실려 전송되고 있음을 확인합니다.

### Step 4. flag 획득
1. 획득한 JSON 내용의 `api_secret_flag` 컬렉션에 기록된 최종 플래그 값(`FLAG{excessive_api_data_exposure_information_leak}`)을 취득합니다.

---

## 5. 취약점 유발 백엔드 코드 스니펫 (PHP)

```php
<!-- /api/user_info.php (취약한 API 데이터 노출 PHP 예시) -->
<?php
header('Content-Type: application/json');

if (isset($_GET['id'])) {
    $user_id = intval($_GET['id']);

    // 데이터베이스 연결
    $conn = new mysqli("localhost", "dbuser", "dbpass", "ctf_db");

    // 취약점 지점: SQL 질의 수행 시 필요한 컬럼(username, join_year)만 선별 쿼리하지 않고 
    // SELECT *를 기동하여 DB 내의 모든 보안 정보가 포함된 행(Row) 객체를 덤프함.
    $stmt = $conn->prepare("SELECT * FROM users WHERE id = ?");
    $stmt->bind_param("i", $user_id);
    $stmt->execute();
    $result = $stmt->get_result();

    if ($row = $result->fetch_assoc()) {
        // 취약점 지점: 획득한 $row 연관 배열의 전체 키-값을 어떠한 정제나 필터링 없이
        // 그대로 json_encode()를 이용해 클라이언트로 덤프 송신함.
        echo json_encode($row);
    } else {
        echo json_encode(["error" => "User not found"]);
    }
}
?>
```

---

## 6. 방어 및 완화 기법 (Mitigation)

1. **데이터 전송 객체 (DTO - Data Transfer Object) 패턴 기용**:
   - 데이터베이스 엔티티 구조를 API 응답으로 다이렉트 덤프해서는 절대 안 됩니다.
   - 외부 전송용을 위해 보안이 필터링된 DTO 클래스 모델을 선언하고, 필요한 값들만 1:1 매핑 후 클라이언트로 변환 송출하도록 설계합니다.
     ```php
     // 안전한 매핑 DTO 구성
     $safe_response = [
         "username" => $row['username'],
         "join_year" => $row['join_year']
     ];
     echo json_encode($safe_response);
     ```
2. **SQL 쿼리 내 명시적 조회 속성 기입**:
   - 습관적인 `SELECT *` 구문의 남용을 전면 지양하며, 데이터베이스 질의 단계에서부터 화면 전시에 필수적인 한정 필드들(`SELECT username, join_year FROM ...`)만 추출하도록 질의 쿼리를 설계하여 데이터베이스 메모리 차원에서의 누출 발생 가능성을 격리합니다.
3. **정기적인 API 명세 관리 및 통신 감사**:
   - Swagger나 OpenAPI Spec 등으로 배포 전 REST API 응답 명세서가 노출하는 스키마 범위를 보안 부서에서 정기 검수하여 비공개 정보가 클라이언트로 무단 흘러가는 흐름을 사전 차단합니다.
