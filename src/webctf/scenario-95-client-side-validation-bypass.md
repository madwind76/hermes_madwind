---
title: Client-Side Validation Bypass — Web CTF Scenario
created: 2026-06-15
updated: 2026-06-15
type: ctf-scenario
tags: [ctf, web, client-side-validation, bypass, proxy, easy]
confidence: high
---

# Client-Side Validation Bypass (클라이언트단 검증 우회) — Web CTF Scenario

## 1. 개요 및 스토리
- **문제명**: Age & Role Register (간이 회원 등급 등록기)
- **난이도**: Easy (초급)
- **핵심 컨셉**: 보안 유효성 검증(Validation)을 서버가 아닌 사용자가 직접 변경할 수 있는 브라우저 클라이언트 영역에만 단독 위임해 통제선이 무너지는 **클라이언트단 검증 단독 의존 및 프록시 우회 (Client-Side Validation Bypass)** 취약점 문제입니다.
- 대상 웹 서비스는 가입 시 사용자가 나이와 역할(Role)을 지정해 회원 가입을 수행하는 페이지입니다. HTML 입력 필드는 일반 사용자 등급인 `user`만 드롭다운 메뉴로 선택할 수 있고 나이 입력 필드는 자바스크립트로 제한 조건(0세 이상 120세 이하)이 엄격히 제약되어 있습니다. 개발자는 클라이언트 웹페이지에서 철저히 값을 가로막기 때문에 안전할 것이라 맹신하고, 서버 측 백엔드 처리 코드에는 유효성 검사 루틴을 구현하지 않았습니다. 공격자는 브라우저의 제약 조건을 우회하고 프록시 도구를 이용해 요청 데이터 패킷을 가로채 값을 임의의 위험한 데이터(`role=admin`)로 수정해 전송하여 권한을 강탈할 수 있습니다.

---

## 2. 문제 설계 및 구조 (Architecture)

### 2.1 구성 요소
- **Registration Page (`/register.html`)**:
  - 사용자 등록 입력을 받는 HTML 화면.
  - 역할 선택 박스는 정해진 옵션만 선택하도록 구현되어 있고, 제출 시 정밀 자바스크립트 함수(`validateForm()`)가 실행되어 부적격 데이터를 사전에 필터링함.
- **Process Endpoint (`/register_process.php`)**:
  - 수신된 가입 POST 데이터를 데이터베이스에 반영.
- **Flag 위치**:
  - `role` 속성이 `admin`으로 조작 및 승인되어 권한이 탈취된 계정으로 로그인했을 때 반환받는 내부 대시보드 페이지.

### 2.2 취약점 지점
1. **Missing Server-side Input Validation**:
  - 백엔드 PHP 스크립트에서 입력받은 인자의 안전성을 대조하는 단계가 생략되어 있습니다:
    `$role = $_POST['role']; // 검증 없이 DB insert`
  - 공격자가 브라우저가 아닌 파이썬 코드나 버프스위트(Burp Suite) 프록시 장치를 기용해 서버 포트에 요청을 바로 밀어 넣으면 프론트엔드의 검증 코드 전체가 무력화되어 임의의 데이터 주입을 허용합니다.

---

## 3. 공격 면 (Attack Surface)

| 엔드포인트 | 메소드 | 인증 | 파라미터 | 데이터 타입 | 취약 함수 및 태그 |
|------------|--------|------|----------|-------------|-------------------|
| `/register_process.php` | POST | 불필요 | `username`, `role`, `age` | Form Data | 백엔드 입력 유효성 대조 누락부 |

---

## 4. 상세 풀이 흐름 (Exploitation Flow)

### Step 1. 회원가입 가동 조건 파악
1. 회원가입 화면인 `/register.html` 로 진입합니다.
2. 입력 폼의 등급(Role) 선택 도구(Select Box)에서 일반 회원 권한인 `User` 등급 이외에 관리자 권한을 선택하는 항목이 물리적으로 보이지 않음을 식별합니다.
3. 소스코드의 가입 자바스크립트 코드(`validateForm`)를 읽고 나이가 숫자가 아닐 시 에러 알림창을 표시하여 가입 프로세스를 인터셉트하는 로직을 포착합니다.

### Step 2. 요청 패킷 프록시 캡처 및 조작
1. 프록시 도구(Burp Suite)를 실행하고 인터셉트(Intercept) 기능을 활성화합니다.
2. 회원가입 버튼을 클릭하여 서버로 날아가는 원시 POST HTTP 패킷을 캡처합니다:
   ```http
   POST /register_process.php HTTP/1.1
   Host: target.local
   Content-Type: application/x-www-form-urlencoded
   
   username=hacker&role=user&age=25
   ```

### Step 3. 파라미터 변조 데이터 송신
1. 캡처되어 홀딩되어 있는 POST 데이터 바디 필드의 `role` 값을 `user`에서 숨겨진 값인 `admin`으로 교체 변조합니다.
   ```http
   username=hacker&role=admin&age=25
   ```
2. 프록시 도구의 'Forward' 버튼을 눌러 위조된 데이터를 서버로 보냅니다.
3. 서버는 프론트 자바스크립트 필터를 이미 통과하여 들어온 올바른 데이터인 양 오류 메시지 없이 가입을 정상 처리 완료하고 200 OK 회신을 돌려줍니다.

### Step 4. flag 획득
1. 조작해 가입시킨 어드민 유저 계정(`hacker` / `password`)으로 포털 로그인을 수행합니다.
2. 가입 시 전달한 `admin` 속성에 상응하여 시스템이 어드민 대시보드 권한을 부여하고, 화면 본문 중심에 플래그(`FLAG{client_side_validation_is_completely_useless}`)를 반환함을 목격하여 획득합니다.

---

## 5. 취약점 유발 백엔드 코드 스니펫 (HTML/PHP)

### 취약한 프론트엔드 구조 (`register.html`)
```html
<!-- register.html -->
<form action="register_process.php" method="POST" onsubmit="return validateForm()">
    <input type="text" name="username" required>
    
    <!-- 사용자는 일반 'user' 속성 이외의 역할을 선택할 방법이 없음 -->
    <select name="role">
        <option value="user">일반 회원</option>
    </select>
    
    <input type="number" id="age_field" name="age">
    <button type="submit">가입하기</button>
</form>

<script>
function validateForm() {
    var age = document.getElementById("age_field").value;
    // 나이가 음수이거나 과도하게 크면 폼 전송을 차단함 (클라이언트단 검증)
    if (age < 0 || age > 120) {
        alert("올바르지 않은 나이입니다.");
        return false;
    }
    return true;
}
</script>
```

### 취약한 백엔드 구조 (`register_process.php`)
```php
<!-- register_process.php -->
<?php
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $username = $_POST['username'];
    
    // 취약점 지점: 사용자가 전달한 role 값과 age 값이 정상적인 허용 범위 내에 존재하는지
    // 서버 단에서 화이트리스트 검사(예: if ($role !== 'user') 등)를 일체 수행하지 않고
    // 요청 값을 전적으로 무조건 신용하여 처리 진행함.
    $role = $_POST['role']; 
    $age = intval($_POST['age']);

    $conn = new mysqli("localhost", "dbuser", "dbpass", "ctf_db");
    
    $stmt = $conn->prepare("INSERT INTO users (username, role, age) VALUES (?, ?, ?)");
    $stmt->bind_param("ssi", $username, $role, $age);
    
    if ($stmt->execute()) {
        echo "가입 완료! 회원 권한: " . htmlspecialchars($role);
    } else {
        echo "Error.";
    }
}
?>
```

---

## 6. 방어 및 완화 기법 (Mitigation)

1. **서버 측 이중 유효성 검사 (Server-side Validation) 필수 구현**:
   - 클라이언트단에서 수행한 모든 유효성 검사 규칙은 단순한 사용자 편의성 제공 및 네트워크 대역폭 낭비 방지 목적으로만 간주해야 합니다.
   - 실제 비즈니스 로직을 처리하기 전에 백엔드 컨트롤러 내부에서 유입된 파라미터가 유효한 값 목록(예: `['user']` 배열과 1:1 일치 여부)에 존재하는지 반드시 서버 메모리 단에서 필터링을 재실행합니다.
     ```php
     // 서버 측의 확실한 화이트리스트 검사 추가
     $allowed_roles = ['user'];
     if (!in_array($role, $allowed_roles)) {
         die("Invalid Role data provided.");
     }
     ```
2. **신뢰 경계 설정 (Zero-Trust on Client Data)**:
   - 사용자의 브라우저를 거쳐 전달되어 유입되는 모든 HTTP 데이터(헤더, 쿠키, 파라미터, 바디 등)는 공격자에 의해 변조 및 조작될 수 있다는 무신뢰(Zero-Trust) 원칙 하에 애플리케이션 코딩 표준을 확립합니다.
3. **스키마 및 속성 자동화 매핑 도구 사용**:
   - ORM 프레임워크나 스키마 검증 유효성 라이브러리(예: Joi, Zod, Pydantic 등)를 서버에 도입하여, 사전에 합의 및 정의된 데이터 구조 포맷과 조금이라도 틀어지는 유입 데이터를 예외 없이 드롭 처리합니다.
