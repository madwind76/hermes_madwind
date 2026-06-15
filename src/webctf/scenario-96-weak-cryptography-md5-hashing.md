---
title: Weak Cryptography — Web CTF Scenario
created: 2026-06-15
updated: 2026-06-15
type: ctf-scenario
tags: [ctf, web, cryptography, weak-hash, md5, hash-cracking, easy]
confidence: high
---

# Weak Cryptography (취약한 암호화 알고리즘 단독 사용) — Web CTF Scenario

## 1. 개요 및 스토리
- **문제명**: Hash Vault Reader (해시 금고 분석기)
- **난이도**: Easy (초급)
- **핵심 컨셉**: 민감한 사용자 비밀번호 정보를 안전하지 않은 오래된 해시 함수(MD5)와 추가 암호학적 솔트(Salt) 없이 단독 처리해 기밀성을 보장받지 못하는 **취약한 암호화 알고리즘 단독 사용 및 패스워드 크래킹 (Weak Cryptography)** 취약점 문제입니다.
- 대상 웹 서비스는 로컬 DB 백업 SQL 파일이나 데이터 베이스 데이터 일부를 덤프해 제공하는 관리 부주의 현상이 있는 상태입니다. 덤프된 정보 안에는 관리자 `admin` 계정의 패스워드 해시 문자열이 평문 대신 해시 처리되어 보관되어 있습니다. 하지만 개발자는 현대적인 강력한 비밀번호 해시 방식(Bcrypt, PBKDF2, Argon2 등)을 사용하지 않고, 연산 속도가 너무 빠르고 충돌 결함이 있는 MD5 알고리즘을 단독 사용해 비밀번호를 보관했습니다. 공격자는 해시의 빠른 대량 대입 연산 가능성을 이용한 레인보우 테이블(Rainbow Table) 조회나 사전식 무차별 크래킹을 가동해 관리자의 원래 평문 패스워드를 알아내 로그인하고 플래그를 취득할 수 있습니다.

---

## 2. 문제 설계 및 구조 (Architecture)

### 2.1 구성 요소
- **Database Dump File (`/db_backup.sql`)**:
  - 설정 실수로 웹 경로에 공개된 SQL 데이터 파일.
  - `admin` 계정의 패스워드 해시값(`admin_hash = "5f4dcc3b5aa765d61d8327deb882cf99"`)이 수록되어 있음.
- **Login Endpoint (`/login.php`)**:
  - 획득한 패스워드 평문 데이터를 사용해 로그인을 수행하는 페이지.
- **Flag 위치**:
  - 해시 해독 후 평문 암호로 로그인을 통과했을 때 보여지는 관리자 프로필 정보 본문.

### 2.2 취약점 지점
1. **Use of a Broken Cryptographic Algorithm (MD5)**:
  - 비밀번호 저장 로직 설계 시 솔트 없는 단순 MD5 해시 함수를 구동합니다:
    `$stored_password = md5($password);`
  - 암호학적 Salt가 적용되지 않은 MD5 결과값은 정해진 원문 입력에 대해 항상 100% 동일한 결과 해시 문자열을 가집니다.
  - 전 세계에 널리 사용되는 비밀번호 해시 데이터베이스(레인보우 테이블)가 이미 온라인상에 상용 구축되어 있으므로, 복잡한 연산 장비 없이도 단순 조회만으로 해시의 원래 평문 데이터가 고스란히 역디코딩되는 보안 무력화 상태를 낳습니다.

---

## 3. 공격 면 (Attack Surface)

| 엔드포인트 | 메소드 | 인증 | 파라미터 | 데이터 타입 | 취약 함수 및 태그 |
|------------|--------|------|----------|-------------|-------------------|
| `/db_backup.sql` | GET | 불필요 | 없음 | 파일 | MD5 암호 데이터 노출 구역 |

---

## 4. 상세 풀이 흐름 (Exploitation Flow)

### Step 1. 기밀 데이터베이스 덤프 획득
1. 서비스에 노출된 디렉터리 리스팅이나 웹 경로 스캔을 통해 `/db_backup.sql` 파일을 획득합니다.
2. 다운로드된 파일의 SQL 스키마 내용 중 `users` 테이블 생성 구문과 가입 레코드를 관찰합니다:
   ```sql
   INSERT INTO users (id, username, password) VALUES (1, 'admin', '5f4dcc3b5aa765d61d8327deb882cf99');
   ```

### Step 2. 해시 유형 판독
1. 식별된 패스워드 문자열(`5f4dcc3b5aa765d61d8327deb882cf99`)의 특징을 식별합니다.
   - 글자 수: 32글자 (16진수 문자 구성)
   - 이 길이는 대표적인 128비트 해시 함수인 **MD5** 포맷의 전형적인 시그니처입니다.

### Step 3. 레인보우 테이블 / 해시 크래킹 검색
1. 획득한 해시 문자열을 크래킹하기 위해 공용 해시 데이터베이스 리스트 조회 사이트(예: CrackStation 등)에 `5f4dcc3b5aa765d61d8327deb882cf99` 해시를 대입 검색합니다.
2. 매치 완료 결과로 평문 원본 텍스트 데이터인 `password` 문자열을 신속히 복원해 냅니다.

### Step 4. 로그인 수행 및 flag 획득
1. 알아낸 관리자 평문 패스워드를 들고 로그인 창(`/login.php`)으로 진입합니다.
   - ID: `admin`
   - PW: `password`
2. 인증 통과 후 관리자 메뉴로 진입해 플래그(`FLAG{weak_md5_hash_without_salt_cracked}`)를 획득합니다.

---

## 5. 취약점 유발 백엔드 코드 스니펫 (PHP)

```php
<!-- /login.php (취약한 해시 로그인 PHP 예시) -->
<?php
session_start();

if (isset($_POST['username']) && isset($_POST['password'])) {
    $username = $_POST['username'];
    $password = $_POST['password'];

    $conn = new mysqli("localhost", "dbuser", "dbpass", "ctf_db");

    // 취약점 지점: 사용자의 입력 패스워드를 비교할 때, 
    // 솔트(Salt)의 가미 없이 오직 MD5 단방향 함수만을 구동하여 원시값 비교 대조를 수행함.
    $hashed_input = md5($password);
    
    $stmt = $conn->prepare("SELECT * FROM users WHERE username = ? AND password = ?");
    $stmt->bind_param("ss", $username, $hashed_input);
    $stmt->execute();
    $result = $stmt->get_result();

    if ($row = $result->fetch_assoc()) {
        $_SESSION['user_role'] = $row['role'];
        echo "로그인 성공! 환영합니다. ";
        if ($row['role'] === 'admin') {
            echo "플래그: FLAG{weak_md5_hash_without_salt_cracked}";
        }
    } else {
        echo "로그인 실패: 아이디 또는 비밀번호 오류.";
    }
}
?>
```

---

## 6. 방어 및 완화 기법 (Mitigation)

1. **단방향 비밀번호 해싱 전용 최신 알고리즘 채택 (Bcrypt / Argon2id)**:
   - MD5나 SHA1, SHA256과 같이 순수 수학 연산 가속에 치우친 범용 해시 함수는 비밀번호 보관에 사용하면 안 됩니다.
   - GPU 병렬 연산을 방해하는 메모리 하드웨어 집약적 연산 지연 구조를 지닌 최신 비밀번호 암호화 표준 함수(예: Bcrypt, Argon2id)를 적용하여 해독 연산 난이도를 무제한 격상시킵니다.
     ```php
     // 안전한 해싱 적용 예 (PHP 내장 bcrypt 표준 엔진 구동)
     $secure_hash = password_hash($password, PASSWORD_BCRYPT);
     ```
2. **솔팅(Salting) 및 키 스트레칭 기법 의무화**:
   - 해시 생성 시마다 임의의 긴 보안 일회용 난수(Salt)를 고유 부착하여 해싱을 처리함으로써, 설령 동일한 비밀번호 평문이라 하더라도 유출된 해시 문자열이 각기 전혀 다르게 보이도록 난독화하며, 레인보우 테이블 조회 공격 시도를 전면 무력화합니다.
3. **데이터베이스 파일 보안 통제**:
   - DB 백업본 등 물리적 자산이 보관된 디렉터리는 외부 웹 서버의 퍼블릭 폴더에서 철저히 영구 배제하며, 기밀 자산 유출 가능성을 원천 예방합니다.
