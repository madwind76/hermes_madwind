---
title: Broken Object Level Authorization (BOLA) in Password Reset — Web CTF Scenario
created: 2026-06-15
updated: 2026-06-15
type: ctf-scenario
tags: [ctf, web, bola, idor, broken-authentication, logic-flaw, easy]
confidence: high
---

# Broken Object Level Authorization (BOLA) in Password Reset — Web CTF Scenario

## 1. 개요 및 스토리
- **문제명**: PassReset Validator (간이 비밀번호 변경 API 서비스)
- **난이도**: Easy (초급)
- **핵심 컨셉**: 비즈니스 로직 및 API 설계 시 로그인 세션이 아닌 클라이언트 전송 파라미터를 그대로 신뢰해 타인의 계정을 침해하는 **객체 수준 권한 검증 누락 (Broken Object Level Authorization - BOLA)** 취약점 문제입니다.
- 대상 웹 서비스는 회원 로그인 후 비밀번호를 변경할 수 있는 페이지(`/change-password.php`)를 제공합니다. 사용자가 새 비밀번호를 입력하고 변경 버튼을 누르면 API 호출이 발생합니다. 이때 서버는 요청을 보낸 사용자의 세션 정보에서 안전하게 식별자를 꺼내오는 대신, 요청 본문(JSON 또는 Post body)에 동봉되어 날아오는 `"username": "user1"` 이라는 매개변수를 그대로 받아 패스워드 변경 대상 계정으로 지정합니다. 공격자는 프록시 도구를 통해 이 요청 패킷을 가로채고 `username` 인자를 `admin`으로 변경 전송함으로써 관리자의 패스워드를 자신의 의도대로 임의 조작할 수 있습니다.

---

## 2. 문제 설계 및 구조 (Architecture)

### 2.1 구성 요소
- **Password Change Page (`/change-password.php`)**:
  - 비밀번호 변경을 수행하는 사용자 인터페이스 폼.
  - 로그인된 유저 세션을 검사하는 예비 루틴은 있으나, 실제 저장 가동 프로세스는 요청 본문의 타겟 파라미터에 의존함.
- **Change Password API (`/api/update-password.php`)**:
  - POST 방식으로 `username`과 `new_password`를 수신하여 계정의 패스워드를 갱신.
- **Flag 위치**:
  - 관리자 계정(`admin`)으로 비밀번호를 탈취해 로그인한 후 도달하는 내부 프로필 관리 메뉴.

### 2.2 취약점 지점
1. **Implicit Trust in Request Parameters (BOLA / IDOR)**:
  - 서버 측 패스워드 업데이트 동작 함수에서 로그인 인증 세션 변수인 `$_SESSION['user_id']`를 배제하고, 클라이언트가 변조할 수 있는 인풋 파라미터 `$POST['target_user']`를 기준으로 DB 쿼리를 결정합니다:
    `UPDATE users SET password = '$new_pass' WHERE username = '$target_user'`
  - 이로 인해 일반 회원 세션만 획득하면 누구나 타 계정의 비밀번호를 임의로 초기화시킬 수 있는 권한 상승 조건이 형성됩니다.

---

## 3. 공격 면 (Attack Surface)

| 엔드포인트 | 메소드 | 인증 | 파라미터 | 데이터 타입 | 취약 함수 및 태그 |
|------------|--------|------|----------|-------------|-------------------|
| `/api/update-password.php` | POST | 필요 (일반 세션 필요) | `username`, `new_password` | JSON / Form | SQL Update 구문 내 식별자 바인딩 로직 |

---

## 4. 상세 풀이 흐름 (Exploitation Flow)

### Step 1. 마이페이지 비밀번호 변경 메뉴 접근
1. 임의 가입한 테스트 유저(`testuser` / `password123`)로 로그인합니다.
2. 회원 정보 관리 영역의 '비밀번호 변경' 메뉴로 들어갑니다.

### Step 2. 요청 패킷 프록시 캡처 및 관찰
1. 웹 브라우저 개발자 도구의 Network 탭을 열거나 버프스위트(Burp Suite)와 같은 프록시 분석 도구를 켭니다.
2. 변경할 비밀번호를 입력하고 '비밀번호 변경 완료' 버튼을 클릭합니다.
3. 전송되는 POST HTTP 요청 데이터 패킷의 파라미터를 파악합니다:
   ```http
   POST /api/update-password.php HTTP/1.1
   Host: target.local
   Content-Type: application/x-www-form-urlencoded
   Cookie: PHPSESSID=abcdef123456...
   
   username=testuser&new_password=hacked123
   ```

### Step 3. 대상 계정 식별자(username) 조작 공격
1. 캡처된 패킷 데이터 중에서 `username` 변수의 값을 본인의 계정명이 아닌 타겟 관리자 계정 이름인 `admin`으로 교체합니다.
   ```http
   username=admin&new_password=hacked123
   ```
2. 변조한 HTTP 요청을 웹 서버로 포워딩 전송합니다.
3. 서버로부터 "Password updated successfully" 라는 성공 응답 코드를 확인합니다.

### Step 4. 변경된 비밀번호로 로그인 및 flag 획득
1. 기존의 테스트 계정 세션을 로그아웃 처리합니다.
2. 공격자가 임의로 지정한 패스워드를 사용해 관리자 계정으로 로그인을 시도합니다.
   - ID: `admin`
   - Password: `hacked123`
3. 정상적으로 관리자 콘솔 진입이 완료되며, 대시보드 관리자 프로필 정보에 기록되어 있는 플래그(`FLAG{bola_password_reset_logic_flaw_takeover}`)를 취득합니다.

---

## 5. 취약점 유발 백엔드 코드 스니펫 (PHP)

```php
<!-- /api/update-password.php (취약한 패스워드 변경 API 예시) -->
<?php
session_start();

// 최소한의 로그인 검사는 진행함
if (!isset($_SESSION['username'])) {
    http_response_code(401);
    echo json_encode(["status" => "error", "message" => "Unauthorized session."]);
    exit();
}

// 클라이언트 요청 바디 값 파싱
if (isset($_POST['username']) && isset($_POST['new_password'])) {
    $target_user = $_POST['username'];
    $new_password = $_POST['new_password'];

    // 데이터베이스 연결
    $conn = new mysqli("localhost", "dbuser", "dbpass", "ctf_db");

    // 패스워드 해싱 처리
    $hashed_password = password_hash($new_password, PASSWORD_DEFAULT);

    // 취약점 지점: 현재 로그인한 세션의 주인($_SESSION['username'])이 누구인지 
    // 검증하지 않고, 사용자가 조작하여 전송한 POST['username'] 파라미터를 그대로 신뢰해 
    // 비밀번호 업데이트 대상 계정을 조회하고 업데이트를 실행함.
    $stmt = $conn->prepare("UPDATE users SET password = ? WHERE username = ?");
    $stmt->bind_param("ss", $hashed_password, $target_user);
    
    if ($stmt->execute()) {
        echo json_encode(["status" => "success", "message" => "Password updated successfully for " . htmlspecialchars($target_user)]);
    } else {
        echo json_encode(["status" => "error", "message" => "Database error."]);
    }
} else {
    echo json_encode(["status" => "error", "message" => "Missing parameters."]);
}
?>
```

---

## 6. 방어 및 완화 기법 (Mitigation)

1. **로그인 세션 기반 식별 강제화**:
   - 비밀번호 변경처럼 중요도가 높은 계정 속성 수정 작업은 요청 매개변수의 식별자 인풋을 무시하고, 서버 메모리에 바인딩되어 위변조가 불가능한 세션 계정 키(`$_SESSION['username']`)를 기준으로 SQL 쿼리의 주체를 결정하도록 고정 설계합니다.
     ```php
     // 안전한 쿼리 처리 예시 (세션 소유주의 패스워드만 변경)
     $stmt->bind_param("ss", $hashed_password, $_SESSION['username']);
     ```
2. **현재 비밀번호 검증 확인 절차 (Re-authentication) 의무화**:
   - 개인정보 수정 및 비밀번호 변경 프로세스 진행 시, 새 비밀번호 외에 '현재 사용 중인 기존 비밀번호(Current Password)'를 필히 입력받아 백엔드에서 검증하는 다단계 로직을 추가합니다. 공격자는 타인의 세션은 뺏을 수 있더라도 기존 비밀번호 평문은 알지 못하므로 BOLA 패턴을 완벽히 봉쇄할 수 있습니다.
3. **엄격한 다중 접근 제어 체계 수립**:
   - 특정 유저의 식별자를 쿼리에 매핑해야 하는 특수한 도메인 모델 구조라면, 변경 요청 대상자가 세션 소유자와 명백히 동등한 권한 또는 동일 인물인지 확인하는 유효성 판별 모듈을 API 처리 초입에 공통 미들웨어 형태로 의무 삽입합니다.
