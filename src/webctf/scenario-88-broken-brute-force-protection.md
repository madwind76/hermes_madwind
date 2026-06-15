---
title: Broken Brute Force Protection — Web CTF Scenario
created: 2026-06-15
updated: 2026-06-15
type: ctf-scenario
tags: [ctf, web, brute-force, broken-authentication, rate-limiting, easy]
confidence: high
---

# Broken Brute Force Protection — Web CTF Scenario

## 1. 개요 및 스토리
- **문제명**: Secure Login Admin (간이 로그인 포털)
- **난이도**: Easy (초급)
- **핵심 컨셉**: 로그인 프로세스에서 연속된 실패 요청을 제한하는 임계치 설정과 보안 보호 기작이 누락되어 계정 권한이 위협받는 **무차별 대입 보호 미흡 (Broken Brute Force Protection)** 취약점 문제입니다.
- 대상 서비스는 관리자 로그인 페이지를 서비스하고 있습니다. 관리자 아이디는 널리 알려진 `admin`으로 설정되어 있으나 패스워드는 유추가 다소 어려운 고빈도 사전 단어로 정의되어 있습니다. 일반적으로 올바른 웹 서비스라면 단시간 내 수백 번 이상 로그인을 틀리거나 시도할 때 클라이언트 IP 차단(Rate Limiting), 일시적 계정 잠금(Account Lockout), 또는 로봇 가동을 걸러내기 위한 CAPTCHA(입력 방지 문자) 인증이 발동해야 합니다. 그러나 이 사이트는 로그인 차단 장치가 전혀 없어 공격자가 자동화 도구를 가동해 패스워드 사전 대입 공격을 가함으로써 관리자 계정을 완전히 강탈할 수 있습니다.

---

## 2. 문제 설계 및 구조 (Architecture)

### 2.1 구성 요소
- **Login Portal (`/login.php`)**:
  - `username` 및 `password` POST 데이터를 가공하여 인증을 시도하는 로그인 핸들러.
  - 로그인 실패 시 데이터베이스에 별도의 시도 횟수를 누적하거나 차단(Lock) 처리하는 절차가 없음.
- **Wordlist File (`/wordlist.txt`)**:
  - CTF 참가자가 무차별 대입 사전 공격에 활용할 수 있도록 웹 경로 상단에 방치되어 있거나 널리 쓰이는 기본 사전 파일(예: Top 100 Common Passwords).
- **Flag 위치**:
  - 어드민 계정 로그인 통과 후 나타나는 내부 대시보드 화면 상단.

### 2.2 취약점 지점
1. **Lack of Rate Limiting and Lockout Mechanism**:
  - 로그인 인증 실패 처리가 발생했을 때 단순히 경고 메시지만 출력하고 별도의 제약 없이 다음 요청을 무제한으로 접수합니다.
  - 1초당 수십~수백 건에 달하는 브라우저 자동화 POST 패킷을 서버가 거부하지 않고 데이터베이스 비밀번호 대조 작업을 기계적으로 반복 처리합니다.

---

## 3. 공격 면 (Attack Surface)

| 엔드포인트 | 메소드 | 인증 | 파라미터 | 데이터 타입 | 취약 함수 및 태그 |
|------------|--------|------|----------|-------------|-------------------|
| `/login.php` | POST | 불필요 | `username`, `password` | Form Data | 로그인 실패 검증 및 요청 속도 제한 누락부 |

---

## 4. 상세 풀이 흐름 (Exploitation Flow)

### Step 1. 로그인 요청 구조 및 응답 반응 관찰
1. 로그인 입력 폼에 `admin` / `wrongpass`를 대입하여 로그인 실패 반응을 봅니다.
2. 응답으로 실패 문구(`Invalid credentials!`)와 함께 200 OK 등의 일정한 웹 페이지 상태가 리턴되는 패턴을 식별합니다.

### Step 2. 자동화 공격 설계
1. 공격 자동화 도구(예: Burp Suite Intruder, Hydra, 또는 간단한 파이썬 스크립트)를 활용하여 `/login.php` 엔드포인트에 대한 브루트포스 공격 양식을 세팅합니다.
2. 타겟을 `username=admin`으로 지정하고, 패스워드 파라미터 영역을 무차별 대입 대상(Payload)으로 선언합니다.

### Step 3. 사전 공격(Dictionary Attack) 가동
1. 널리 알려진 일반적인 비밀번호 리스트 또는 힌트로 획득한 사전 텍스트 파일을 로드하여 로그인 요청 공격을 대량 수행합니다.
   ```http
   POST /login.php HTTP/1.1
   Host: target.local
   Content-Type: application/x-www-form-urlencoded
   
   username=admin&password=§password_payload§
   ```
2. 요청 속도가 지연되거나 IP 차단 응답(예: 429 Too Many Requests)이 오는지 확인합니다. 차단 없이 모든 요청이 즉시 리턴되는 것을 보고 방어 정책 부재를 확인합니다.

### Step 4. flag 획득
1. 응답 데이터의 길이(Length) 또는 특정 성공 반응 키워드(예: `Redirecting` 또는 `Welcome`)가 달라진 패밀리 리퀘스트 번호를 찾습니다.
2. 매칭되는 올바른 로그인 암호(예: `admin12345`)를 식별합니다.
3. 찾은 크레덴셜로 정상 로그인하여 어드민 계정 전용 영역에 감춰져 있던 플래그(`FLAG{broken_brute_force_protection_easy_bypass}`)를 획득합니다.

---

## 5. 취약점 유발 백엔드 코드 스니펫 (PHP)

```php
<!-- login.php (취약한 무차별 대입 방어 누락 PHP 예시) -->
<?php
session_start();

if (isset($_POST['username']) && isset($_POST['password'])) {
    $username = $_POST['username'];
    $password = $_POST['password'];

    // 데이터베이스 연결
    $conn = new mysqli("localhost", "dbuser", "dbpass", "ctf_db");
    
    // 취약점 지점: 로그인 실패가 수백 번 발생하더라도 요청 IP나 ID를 
    // 임시 차단(IP Block)하거나 일정 시간 요청 대기(Delay)를 강제하는 코드가 없음.
    // 또한 CAPTCHA 등을 통한 자동화 차단 정책도 구현되어 있지 않음.
    $stmt = $conn->prepare("SELECT id, password FROM users WHERE username = ?");
    $stmt->bind_param("s", $username);
    $stmt->execute();
    $result = $stmt->get_result();

    if ($row = $result->fetch_assoc()) {
        // 평문 대조 혹은 간단한 검증
        if ($password === $row['password']) {
            $_SESSION['admin_logged'] = true;
            header("Location: dashboard.php");
            exit();
        }
    }
    
    // 실패 시 매번 딜레이나 IP 로깅 없이 에러 메시지만 단순 반환
    echo "<p style='color:red;'>Invalid username or password.</p>";
}
?>
```

---

## 6. 방어 및 완화 기법 (Mitigation)

1. **속도 제한 정책 도입 (Rate Limiting)**:
   - 특정 단일 IP 주소나 동일 세션 키로부터 단시간에 기준치 이상의 로그인 실패 리퀘스트가 들어올 시, HTTP 429(Too Many Requests) 상태 코드와 함께 강제 요청 거부 필터를 기동합니다. (예: Redis 등을 활용한 IP별 실패 횟수 로깅 및 타이머 처리)
2. **계정 임시 잠금 체계 (Account Lockout)**:
   - 로그인 비밀번호 입력 오류가 누적 5회 이상 발생했을 때, 해당 계정의 로그인 처리를 일정 시간(예: 30분) 동안 물리적으로 비활성화(Lock)하여 추가 사전 대입 공격 시도를 무력화합니다.
3. **CAPTCHA(캡차) 및 다요소 인증(MFA) 의무화**:
   - 다수의 로그인 요청 오류가 발생하거나 위험성이 높은 인증 인터페이스 영역에는 구글 reCAPTCHA 등의 시각 챌린지 인증 기작을 적용하여 봇 자동화 툴이 패킷을 조작해 직접 로그인 시도를 반복하는 메커니즘을 물리적으로 방어합니다.
