---
title: Insecure Direct Object Reference (IDOR) — Web CTF Scenario
created: 2026-06-15
updated: 2026-06-15
type: ctf-scenario
tags: [ctf, web, idor, broken-access-control, easy]
confidence: high
---

# Insecure Direct Object Reference (IDOR) — Web CTF Scenario

## 1. 개요 및 스토리
- **문제명**: User Profile Manager (간이 유저 프로필 관리기)
- **난이도**: Easy (초급)
- **핵심 컨셉**: 권한 검증 미흡으로 타인의 비공개 객체 데이터에 직접 접근하는 **안전하지 않은 직접 객체 참조 (IDOR)** 취약점 문제입니다. 해당 애플리케이션은 가입 회원이 마이페이지에서 자신의 개인 정보(이메일, 연락처, 주소 등)를 확인할 수 있도록 `/profile.php?user_id=105` 형태의 동적 URL을 제공합니다. 여기서 사용되는 `user_id` 파라미터는 데이터베이스 테이블의 순차적인 정수 기본키(Primary Key)입니다. 개발자는 데이터베이스에서 프로필 정보를 쿼리하여 출력할 때, 현재 세션에 저장된 로그인 유저의 ID값과 파라미터로 입력된 `user_id`값이 일치하는지 검증하지 않았습니다. 공격자는 단순히 `user_id` 값을 증감 및 대입해 보며 회원 가입된 다른 사용자 또는 서비스 관리자(Admin)의 민감 정보와 플래그를 취득할 수 있습니다.

---

## 2. 문제 설계 및 구조 (Architecture)

### 2.1 구성 요소
- **Profile Page (`/profile.php`)**:
  - `?user_id=...` 파라미터를 입력받고 해당하는 사용자의 이메일, 가입일, 비공개 메모 항목을 조회하여 화면에 출력.
- **Session Manager**:
  - 로그인 성공 시 사용자 번호를 세션 변수(`$_SESSION['logged_in_user']`)에 기록하지만, 프로필 조회 로직 내부에서는 이 세션 변수를 통한 조회 권한 검사를 수행하지 않음.
- **Flag 위치**:
  - 데이터베이스 내부의 최고 관리자 계정(`user_id=1` 또는 `user_id=1000` 등 특정 시드 번호)의 프로필 '비공개 메모' 항목.

### 2.2 취약점 지점
1. **Missing Access Control Authorization Check**:
  - 요청 주소에 동봉된 식별자 `user_id` 파라미터를 신뢰하여 곧바로 데이터베이스 조회 쿼리를 실행합니다:
    `SELECT * FROM users WHERE id = $_GET['user_id']`
  - 요청을 보낸 실제 주체가 해당 데이터 행(Row)의 소유주인지 판별하는 조건 절차(`if (session_id != target_id)`)가 완전히 생략되어 있어 타인의 데이터를 임의로 유출합니다.

---

## 3. 공격 면 (Attack Surface)

| 엔드포인트 | 메소드 | 인증 | 파라미터 | 데이터 타입 | 취약 함수 및 태그 |
|------------|--------|------|----------|-------------|-------------------|
| `/profile.php` | GET | 필요 (일반 계정) | `user_id` | Integer | SQL Select 쿼리 및 소유권 비교 누락부 |

---

## 4. 상세 풀이 흐름 (Exploitation Flow)

### Step 1. 본인 회원가입 및 프로필 메뉴 진입
1. 임의의 테스트 계정(`user_test` / `password123`)으로 회원가입을 완료하고 로그인합니다.
2. 마이페이지 메뉴를 누르고 브라우저 주소창의 URL 경로를 식별합니다.
   `/profile.php?user_id=125`
3. 정상적인 본인의 이메일 정보와 회원 등급이 출력되는 것을 확인합니다.

### Step 2. 파라미터 식별자 변경 시도
1. 주소창의 `user_id` 값을 125에서 임의의 다른 숫자(예: 124, 126)로 변경하여 요청을 재발송합니다.
   `/profile.php?user_id=124`
2. 자신이 아닌 제3의 타인의 이메일 주소 정보가 에러 없이 평문 렌더링되어 표시되는 현상을 발견합니다. 이를 통해 취약한 IDOR 상태임을 확인합니다.

### Step 3. 대상 관리자 계정 추적 및 무차별 대입
1. 일반적으로 시스템이 구축된 시점의 최초 데이터 인덱스 번호는 `1`인 경우가 지배적이므로 관리자의 아이디를 특정하기 위해 `user_id=1`을 대입합니다.
   `/profile.php?user_id=1`
2. 데이터베이스 쿼리가 수행되어 관리자의 세부 프로필 정보 영역이 화면에 성공적으로 나타납니다.

### Step 4. flag 획득
1. 관리자 프로필 화면 하단에 위치한 '비공개 관리자 비고란 (Private Admin Notes)' 항목을 분석합니다.
2. 메모란 내용에 기록되어 있는 최종 플래그 값(`FLAG{idor_insecure_direct_object_reference_easy_leak}`)을 취득합니다.

---

## 5. 취약점 유발 백엔드 코드 스니펫 (PHP)

```php
<!-- profile.php (취약한 IDOR PHP 예시) -->
<?php
session_start();

// 로그인 검사 (단순히 세션이 있는지만 검증하고, 소유권 정합성은 미흡)
if (!isset($_SESSION['user_id'])) {
    die("Please login first.");
}

// 사용자로부터 프로필 식별 대상을 파라미터로 받음
if (isset($_GET['user_id'])) {
    $target_user_id = intval($_GET['user_id']);

    // 데이터베이스 연결부 (예시)
    $conn = new mysqli("localhost", "dbuser", "dbpass", "ctf_db");
    
    // 취약점 지점: 조회 요청 대상 ID가 현재 세션 로그인 유저의 ID와 동일한지 
    // 검증하는 권한 로직(if ($target_user_id !== $_SESSION['user_id']))이 아예 없음
    $stmt = $conn->prepare("SELECT email, role, private_note FROM users WHERE id = ?");
    $stmt->bind_param("i", $target_user_id);
    $stmt->execute();
    $result = $stmt->get_result();
    
    if ($row = $result->fetch_assoc()) {
        echo "<h1>프로필 조회 결과</h1>";
        echo "<p>이메일: " . htmlspecialchars($row['email']) . "</p>";
        echo "<p>역할: " . htmlspecialchars($row['role']) . "</p>";
        echo "<p>메모: " . htmlspecialchars($row['private_note']) . "</p>";
    } else {
        echo "User not found.";
    }
} else {
    echo "User parameter is missing.";
}
?>
```

---

## 6. 방어 및 완화 기법 (Mitigation)

1. **상대 세션 기반 객체 참조 (Session-Based Lookup)**:
   - 클라이언트 파라미터로부터 수정 및 조회가 가능한 객체의 주 키(Primary Key)를 입력받지 않고, 검증된 사용자 세션 데이터 내의 유저 토큰정보를 역추적하여 본인의 데이터 레코드만 쿼리하도록 강제 설계합니다.
     ```php
     // 파라미터를 사용하지 않는 안전한 마이페이지 구현 예
     $stmt = $conn->prepare("SELECT email, role, private_note FROM users WHERE id = ?");
     $stmt->bind_param("i", $_SESSION['user_id']); // 세션 값을 바인딩
     ```
2. **간접 참조 및 불투명 토큰(UUID / Hash) 도입**:
   - 순차적으로 증가하는 단순 정수 키를 클라이언트 인터페이스 주소에 드러내지 않으며, 암호학적으로 강력한 무작위 값인 UUIDv4를 식별자로 채택하여 타 사용자의 값을 추측 불가능하게 난독화합니다.
3. **명시적 권한 검사 기법 도입**:
   - 파라미터를 기반으로 직접 리소스에 접근해야 하는 비즈니스 환경이라면, SQL 조회를 완료한 후 혹은 시작 시점에 반드시 "요청한 유저가 해당 데이터를 소유/접근할 수 있는가?"에 관한 권한 통제 체크 목록(ACL)을 강제 가동하여 권한 탈취를 방지합니다.
