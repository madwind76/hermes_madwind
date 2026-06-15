---
title: Weak Session ID Prediction — Web CTF Scenario
created: 2026-06-15
updated: 2026-06-15
type: ctf-scenario
tags: [ctf, web, session-management, weak-session-id, session-hijacking, easy]
confidence: high
---

# Weak Session ID Prediction (취약한 세션 ID 예측) — Web CTF Scenario

## 1. 개요 및 스토리
- **문제명**: Session Predictor Portal (세션 ID 검증 포털)
- **난이도**: Easy (초급)
- **핵심 컨셉**: 세션을 식별하는 쿠키 토큰값이 복잡한 난수가 아닌 취약하고 규칙적인 로직으로 생성되어 타인의 권한을 도용당하는 **예측 가능한 세션 ID 구조 및 세션 하이재킹 (Weak Session ID Prediction)** 취약점 문제입니다.
- 대상 서비스는 회원가입 및 로그인을 처리하며, 로그인 성공 시 브라우저 쿠키에 `PHPSESSID` 대신 커스텀 쿠키 명칭인 `my_session`을 발급해 세션을 유지합니다. 하지만 개발자가 세션 식별자를 설계할 때 보안성이 확보된 난수 생성기 대신, 로그인한 유저명의 MD5 해시값(예: `md5(username)`) 또는 회원 가입 시 부여되는 순차적인 유저 고유 일련번호(Integer)를 그대로 세션 쿠키 값으로 사용했습니다. 공격자는 일반 사용자로 로그인하여 본인의 세션 ID 발급 규칙성을 찾아낸 뒤, 최고 권한 관리자인 `admin` 계정의 세션 쿠키 값을 역으로 예측해 쿠키 정보를 조작함으로써 패스워드 없이 관리자 권한을 완전히 획득할 수 있습니다.

---

## 2. 문제 설계 및 구조 (Architecture)

### 2.1 구성 요소
- **Login Handler Page (`/login.php`)**:
  - 사용자 인증 후 세션을 강제 할당하는 페이지.
  - 규칙성 있는 해시 및 정수를 조합해 세션 쿠키 `my_session`을 브라우저로 리턴.
- **Protected Dashboard (`/dashboard.php`)**:
  - 브라우저 쿠키 `my_session`을 체크해 사용자 등급(Role) 및 프로필 정보를 화면에 전시.
- **Flag 위치**:
  - `admin` 계정으로 세션이 변경되어 대시보드에 도달했을 때 보여지는 관리 전용 패널 내부 영역.

### 2.2 취약점 지점
1. **Predictable Session Generation Algorithm**:
  - 세션 쿠키 값을 생성하는 로직이 암호학적으로 복잡하지 않고 단조로운 수식에 기대어 동작합니다:
    `$session_cookie = md5($username);`
  - 공격자가 `admin` 이라는 관리자 계정명이 시스템에 존재함을 알고 있다면, 그의 세션 토큰 값인 `md5("admin")` 값(`21232f297a57a5a743894a0e4a801fc3`)을 컴퓨터 상에서 언제든지 쉽게 연산하여 알아낼 수 있습니다.
  - 서버는 수신한 쿠키가 DB 혹은 해시 맵에 실제로 등록되어 대조되는 유효 세션인지 추가적으로 검증하지 않고, 단순 데이터 매핑 해석을 거쳐 관리자 권한을 인가합니다.

---

## 3. 공격 면 (Attack Surface)

| 엔드포인트 | 메소드 | 인증 | 파라미터 | 데이터 타입 | 취약 함수 및 태그 |
|------------|--------|------|----------|-------------|-------------------|
| `/dashboard.php` | GET | 필요 (쿠키 인증) | `my_session` (Cookie) | MD5 Hash / Text | 세션 검증 및 발급 알고리즘 설계부 |

---

## 4. 상세 풀이 흐름 (Exploitation Flow)

### Step 1. 임의 계정 가입 및 세션 관찰
1. 테스트용 회원 계정 `testuser`를 가입시키고 로그인을 시도합니다.
2. 개발자 도구(F12)의 Application -> Cookies 탭 또는 Network 패킷 조회를 통해 발급된 쿠키 정보를 확인합니다:
   - 쿠키명: `my_session`
   - 쿠키값: `5d9c68c6c50ed3d02a2fcf54f63993b6`

### Step 2. 발급된 세션 ID의 디코딩 및 규칙 파악
1. 획득한 세션 문자열 값을 분석 및 온라인 해시 대조 서비스를 통해 역추적합니다.
2. `5d9c68c6c50ed3d02a2fcf54f63993b6` 해시값의 원문 평문이 가입 아이디인 `testuser`임을 식별합니다.
3. 즉, 세션 ID 규칙이 단순 `md5(username)` 구조임을 파악해 냅니다.

### Step 3. 대상 관리자 계정(admin) 세션 쿠키 유추
1. 공격 대상인 어드민 계정명 `admin` 문자열의 MD5 해시 결과값을 툴이나 해시 제너레이터를 사용해 로컬에서 계산합니다:
   - 대상 아이디: `admin`
   - 변환 해시: `21232f297a57a5a743894a0e4a801fc3`

### Step 4. 쿠키 변조 및 flag 획득
1. 브라우저 개발자 도구의 콘솔 혹은 쿠키 편집기를 열어 기존 쿠키를 조작합니다.
   - 쿠키명: `my_session`
   - 값을 `21232f297a57a5a743894a0e4a801fc3` 으로 업데이트 교체합니다.
2. 변경된 쿠키를 소지한 채로 보호 구역 대시보드 페이지 `/dashboard.php`를 새로고침 요청합니다.
3. 서버가 세션 쿠키를 해석하여 관리자 계정으로 인가 처리하고 보여주는 어드민 특별 패널에서 최종 플래그(`FLAG{predictable_session_id_hijack_easy_md5}`)를 획득합니다.

---

## 5. 취약점 유발 백엔드 코드 스니펫 (PHP)

```php
<!-- login.php (취약한 세션 생성 PHP 예시) -->
<?php
if (isset($_POST['username']) && isset($_POST['password'])) {
    $username = $_POST['username'];
    $password = $_POST['password'];

    // DB 연동 및 인증 절차 진행 (예시 생략)
    $login_success = true; 

    if ($login_success) {
        // 취약점 지점: 암호학적으로 안전한 무작위 난수(Session ID)를 생성하지 않고, 
        // 단순히 입력된 유저 아이디값을 MD5로 변형하여 브라우저에 세션 토큰으로 제공함.
        $session_token = md5($username);

        // my_session 이라는 이름의 쿠키로 세션 식별자를 발행
        setcookie("my_session", $session_token, time() + 3600, "/");
        
        header("Location: dashboard.php");
        exit();
    }
}
?>

<!-- dashboard.php (취약한 세션 인증 검증부 PHP) -->
<?php
if (isset($_COOKIE['my_session'])) {
    $session = $_COOKIE['my_session'];

    // 데이터베이스 또는 맵에서 세션 토큰을 이용해 복원
    // 예제 시뮬레이션: 역연산하여 사용자 판별 혹은 직접 DB 매핑 조회
    $conn = new mysqli("localhost", "dbuser", "dbpass", "ctf_db");
    
    // 쿠키 세션 해시값과 DB 내 해싱된 유저명을 1:1 대조
    $stmt = $conn->prepare("SELECT username, role FROM users WHERE MD5(username) = ?");
    $stmt->bind_param("s", $session);
    $stmt->execute();
    $result = $stmt->get_result();

    if ($row = $result->fetch_assoc()) {
        $user = $row['username'];
        $role = $row['role'];
        
        echo "<h1>환영합니다, " . htmlspecialchars($user) . "님!</h1>";
        if ($role === 'admin') {
            echo "<p><b>Admin Flag:</b> FLAG{predictable_session_id_hijack_easy_md5}</p>";
        }
    } else {
        echo "유효하지 않은 세션입니다.";
    }
} else {
    echo "로그인이 필요합니다.";
}
?>
```

---

## 6. 방어 및 완화 기법 (Mitigation)

1. **내장 웹 애플리케이션 프레임워크 표준 세션 핸들러 사용**:
   - 직접 커스텀 세션 토큰을 개발하는 방식을 배제하고, 언어 및 프레임워크가 공식적으로 지원하고 검증받은 안전한 내장 세션 모듈(예: PHP의 `session_start()`, Node.js의 `express-session` 등)을 기동시킵니다.
2. **CORS/CSPRNG 기반의 암호학적으로 안전한 무작위 값 사용**:
   - 세션 ID 생성 시 엔트로피가 극도로 높아 추측이 완전 불가능한 암호학적 의사난수 생성기(CSPRNG - Cryptographically Secure Pseudo-Random Number Generator)를 활용하고, 최소 128비트 이상의 길이(예: UUIDv4 또는 32바이트 이상의 랜덤 Hex값)로 임의 세션 키를 생성합니다.
3. **세션 유효 기간 설정 및 데이터베이스 매핑 철저화**:
   - 세션 식별자가 단순 정적 값(유저명 변환값 등)으로 고정되지 않고 매 로그인마다 무작위 재구성되도록 폐기 처리를 보장하며, 세션 상태를 서버 세션 테이블에 바인딩하여 만료 기간(Session Timeout) 초과 시 서버에서 즉시 데이터를 휘발시키는 정책을 관리합니다.
