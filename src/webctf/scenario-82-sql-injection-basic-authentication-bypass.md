---
title: Basic SQL Injection Authentication Bypass — Web CTF Scenario
created: 2026-06-15
updated: 2026-06-15
type: ctf-scenario
tags: [ctf, web, sqli, sql-injection, authentication-bypass, easy]
confidence: high
---

# Basic SQL Injection Authentication Bypass — Web CTF Scenario

## 1. 개요 및 스토리
- **문제명**: Admin Gatekeeper (관리자 인증 게이트)
- **난이도**: Easy (초급)
- **핵심 컨셉**: 웹 백엔드와 데이터베이스 간의 통신 시 발생하는 가장 대표적인 고전 보안 취약점인 **SQL 인젝션 기반 인증 우회 (SQL Injection Authentication Bypass)** 문제입니다. 대상 애플리케이션은 포털 로그인을 처리하기 위해 사용자가 입력한 아이디와 비밀번호 값을 문자열 포맷팅으로 직접 결합하여 데이터베이스 SQL 질의문을 수행합니다. 공격자는 입력값 검증이 미흡한 로그인 아이디 입력 필드에 SQL 문법적 논리 기호인 싱글 쿼터(`'`)와 오어(`OR`) 연산자를 삽입해, 비밀번호를 알지 못하더라도 전체 SQL 쿼리의 WHERE 조건문 판단 결과를 항상 '참(True)'으로 조작해 인증 절차를 우회하고 최고 관리자 권한을 획득합니다.

---

## 2. 문제 설계 및 구조 (Architecture)

### 2.1 구성 요소
- **Login Endpoint (`/login.php`)**:
  - `POST` 메소드로 사용자가 전달한 `username` 및 `password` 데이터를 수신.
  - 백엔드 데이터베이스 조회 SQL 실행:
    `SELECT * FROM users WHERE username = '$user' AND password = '$password'`
- **Flag 위치**:
  - `admin` 계정 로그인 우회 통과에 성공하여 관리자 인덱스 대시보드 `/admin_panel.php` 화면에 접속했을 때 노출되는 기밀 텍스트.

### 2.2 취약점 지점
1. **Dynamic Query Assembly via String Interpolation**:
   - 사용자 입력값을 SQL 컴파일 단계 전에 안전하게 이스케이프(Escape)하거나 바인딩하지 않고, 문자열 사이에 그대로 하드코딩해 결합함으로써 쿼리 문법 구조 자체의 제어권을 상실합니다.
2. **Boolean Logic Alteration (불리언 논리 조작)**:
   - 쿼리 WHERE 절에 `OR 1=1`과 같은 항상 참이 되는 명제를 주입해 SQL 파서가 앞쪽의 비밀번호 일치 조건 유무에 상관없이 결과를 무조건 참으로 평가하게 유도합니다.

---

## 3. 공격 면 (Attack Surface)

| 엔드포인트 | 메소드 | 인증 필요성 | 파라미터 | 데이터 타입 | 핵심 공격 목표 |
|------------|--------|-------------|----------|-------------|----------------|
| `/login.php` | POST | 불필요 | `username`, `password` | String | WHERE 절 문법 구조 변조 및 인증 우회 |

---

## 4. 상세 풀이 흐름 (Exploitation Flow)

### Step 1. SQL 문법 에러 유발 테스트
1. 로그인 페이지의 아이디 입력창에 싱글 쿼터 `'` 기호를 입력하고 임의의 비밀번호를 넣고 제출해 봅니다.
   - 아이디: `test'`
   - 패스워드: `password`
2. 데이터베이스 문법 오류(SQL Syntax Error)가 화면에 반환되는지 확인하여, 입력한 특수문자가 쿼리 파서에 그대로 직접 인계되는 취약점이 있음을 확인합니다.

### Step 2. 로그인 우회 SQL 페이로드 설계
백엔드의 조회 쿼리가 다음과 같이 구성되어 있다고 판단합니다.
`SELECT * FROM users WHERE username = '[USER]' AND password = '[PASS]'`
- **아이디 입력값 설계**:
  `admin' --` 또는 `admin' OR '1'='1`
- **조립된 완성형 SQL 쿼리**:
  `SELECT * FROM users WHERE username = 'admin' --' AND password = '...'`
  *(더블 대시 `--` 혹은 샵 `#` 기호가 PostgreSQL/MySQL/SQLite 등에서 SQL 한 줄 주석 기호로 동작하므로, 뒤쪽의 패스워드 검증 로직인 `' AND password = ...` 구문 전체가 무시 및 삭제 처리됨)*

### Step 3. 우회 페이로드 제출
1. 로그인 입력 폼의 Username 칸에 준비한 우회 공격 구문을 기입합니다.
   - Username: `admin' --`
   - Password: `any_password` (임의 기입)
2. 로그인 요청을 전송합니다.

### Step 4. flag 획득
1. 백엔드는 주석으로 인해 패스워드를 비교하지 않고 `SELECT * FROM users WHERE username = 'admin'` 결과 레코드 세트만 성공적으로 조회하여 가져옵니다.
2. 시스템은 데이터베이스 조회가 성공했고 행(Row) 결과가 존재하므로 인증이 적법하게 통과된 것으로 오판하여 세션을 발급해 줍니다.
3. 리다이렉트 처리된 관리자 전용 대시보드 화면(`/admin_panel.php`)에서 플래그(`FLAG{sql_injection_basic_auth_bypass_success}`)를 확인합니다.

---

## 5. 취약점 유발 백엔드 코드 스니펫 (PHP + SQLite)

```php
<?php
// login.php (취약한 SQL Injection 로그인 구현 예시)
session_start();

if (isset($_POST['username']) && isset($_POST['password'])) {
    $user = $_POST['username'];
    $pass = $_POST['password'];

    // 데이터베이스 연결 (SQLite 예시)
    $db = new SQLite3('users.db');

    // 취약점 지점 1: 사용자 입력을 파라미터화하지 않고 문자열 포맷 결합을 통해 SQL 쿼리를 구성함
    // 이로 인해 $user에 "admin' --" 가 들어오면 패스워드 검증 절차가 완전히 주석 처리로 날아감
    $query = "SELECT * FROM users WHERE username = '" . $user . "' AND password = '" . $pass . "'";

    $result = $db->query($query);

    if ($row = $result->fetchArray()) {
        // 결과 행이 한 개라도 존재하면 정상 로그인 처리
        $_SESSION['user'] = $row['username'];
        $_SESSION['role'] = $row['role'];
        
        header("Location: admin_panel.php");
        exit();
    } else {
        echo "<h4>아이디 또는 비밀번호가 올바르지 않습니다.</h4>";
    }
}
?>
```

---

## 6. 방어 및 완화 기법 (Mitigation)

1. **파라미터화된 쿼리 의무 사용 (Prepared Statements)**:
   - SQLi 취약점을 방지하는 가장 완벽한 해법은 동적 문자열 조립을 버리고 **준비된 구성 쿼리 (Prepared Statements / Parameterized Queries)** 기술을 사용하는 것입니다.
   - 사용자 입력 변수를 쿼리와 완전 분리하여 데이터 영역의 인자(Parameter)로만 처리되도록 DBMS 컴파일러 단에서 규정합니다.
     ```php
     // 안전한 Prepared Statement 적용법
     $stmt = $db->prepare('SELECT * FROM users WHERE username = :username AND password = :password');
     $stmt->bindValue(':username', $user, SQLITE3_TEXT);
     $stmt->bindValue(':password', $pass, SQLITE3_TEXT);
     $result = $stmt->execute();
     ```
2. **ORM 프레임워크 활용**:
   - Raw SQL 쿼리 작성을 자제하고, 파라미터 바인딩이 기본 내장 제공되는 신뢰도 높은 ORM(Hibernate, Sequelize, Django ORM 등)을 연동하여 개발 품질을 높입니다.
3. **상세한 DB 에러 노출 방지**:
   - 쿼리 실패 시 반환되는 상세 시스템 디버그 메시지를 외부 방문자에 직접 출력하지 않고, 범용 에러 코드만 반환하여 정보 유출 위협을 줄입니다.
