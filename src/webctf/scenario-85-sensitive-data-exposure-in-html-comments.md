---
title: Sensitive Data Exposure in HTML Comments — Web CTF Scenario
created: 2026-06-15
updated: 2026-06-15
type: ctf-scenario
tags: [ctf, web, sensitive-data-exposure, information-disclosure, html-comments, easy]
confidence: high
---

# Sensitive Data Exposure in HTML Comments — Web CTF Scenario

## 1. 개요 및 스토리
- **문제명**: Hidden Developer Notes (개발자의 숨겨진 메모)
- **난이도**: Easy (초급)
- **핵심 컨셉**: 웹 개발 도중 남겨진 민감한 디버깅 주석이 상용 배포 환경에 노출되어 핵심적인 기밀 자산을 유출시키는 **HTML 주석 내 민감 정보 노출 (Sensitive Data Exposure in HTML Comments)** 취약점 문제입니다. 
- 대상 서비스는 간단한 포털 사이트 로그인 웹 페이지입니다. 개발 과정에서 시스템 연동 테스트나 디버깅 편의를 위해 임시로 추가해 둔 관리자 계정 계정정보나, 백업으로 압축해 둔 비밀 경로 데이터 주석(`<!-- TODO: 임시 관리자 아이디: admin / 비밀번호: ... -->`)을 실수로 정제하지 않은 채 배포했습니다. 이 주석 정보는 일반적인 브라우저 화면에는 보이지 않지만, 웹 브라우저의 '페이지 소스 보기' 또는 '개발자 도구(F12)' 기능을 열어 정적 소스코드를 관찰하는 단순 조사 과정을 거쳐 누구나 쉽게 획득할 수 있습니다.

---

## 2. 문제 설계 및 구조 (Architecture)

### 2.1 구성 요소
- **Login Portal Page (`/login.html`)**:
  - 사용자 인증을 위한 단순 로그인 폼 UI.
  - HTML 본문 하단에 디버그용으로 삽입된 정적 주석 블록이 남겨져 있음.
- **Admin Dashboard (`/admin_dashboard.php`)**:
  - 관리자 계정으로 올바르게 로그인했을 때 접근할 수 있는 보호 구역 페이지.

### 2.2 취약점 지점
1. **Unremoved Sensitive Comments in Client-side Code**:
  - 웹 브라우저가 수신하여 파싱하는 HTML/JS 정적 데이터 소스 영역 내에 실제 운영 환경에서 유효한 인증 크레덴셜이 주석 문법(`<!-- ... -->` 또는 `// ...`)으로 방치되어 있습니다.
  - 서버 측 코드가 아닌 클라이언트 측 코드로 다운로드되므로, 어떠한 웹 애플리케이션 방화벽(WAF)의 동적 차단 정책 없이 정적 소스코드 보기로 기밀 획득이 가능합니다.

---

## 3. 공격 면 (Attack Surface)

| 엔드포인트 | 메소드 | 인증 | 파라미터 | 데이터 타입 | 취약 함수 및 태그 |
|------------|--------|------|----------|-------------|-------------------|
| `/login.html` | GET | 불필요 | 없음 | 정적 파일 | HTML 주석 태그 `<!--` ~ `-->` |

---

## 4. 상세 풀이 흐름 (Exploitation Flow)

### Step 1. 웹 로그인 페이지 접속
1. 웹 브라우저를 사용하여 대상 서비스의 로그인 페이지인 `/login.html`에 접속합니다.
2. 입력 폼창 이외에 별도의 추가 안내 정보가 없는 일반적인 UI 구성을 보입니다.

### Step 2. 클라이언트단 소스코드 열람
1. 브라우저 화면에서 마우스 우클릭을 한 뒤 '페이지 소스 보기(View Page Source)'를 클릭하거나 단축키(Ctrl + U)를 입력합니다.
2. 혹은 개발자 도구(F12)의 'Elements' 탭을 활성화하여 전송된 DOM 트리를 조사합니다.

### Step 3. 주석 분석 및 기밀 계정정보 식별
1. 소스코드 전체를 스크롤하며 녹색 또는 다크 그레이로 하이라이트된 주석 영역을 탐색합니다.
2. 아래와 같이 명백하게 방치되어 있는 임시 정보 메모를 획득합니다:
   `<!-- TODO: 배포 시 꼭 지울 것 - 테스트 관리자 계정: admin / admin_debug_9999 -->`
3. 획득한 아이디와 패스워드 조합을 복사해 둡니다.

### Step 4. 로그인 및 flag 획득
1. 획득한 크레덴셜 정보(`admin` / `admin_debug_9999`)를 로그인 화면에 직접 기입하여 인증 과정을 통과합니다.
2. 정상 로그인 후 도달한 관리자 전용 대시보드(`admin_dashboard.php`) 웹 사이트 상단에 걸려 있는 플래그(`FLAG{html_comments_leak_developer_credentials}`)를 취득합니다.

---

## 5. 취약점 유발 백엔드 코드 스니펫 (HTML)

```html
<!-- login.html (취약한 주석 노출 HTML 예시) -->
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <title>Enterprise Portal Login</title>
    <style>
        body { font-family: sans-serif; background: #fafafa; padding: 50px; }
        .login-box { width: 300px; margin: 0 auto; background: white; padding: 20px; border: 1px solid #ccc; }
    </style>
</head>
<body>
    <div class="login-box">
        <h2>로그인 Portal</h2>
        <form method="POST" action="login_process.php">
            <label>ID:</label><br>
            <input type="text" name="username"><br><br>
            <label>Password:</label><br>
            <input type="password" name="password"><br><br>
            <button type="submit">로그인</button>
        </form>
    </div>

    <!-- 
      취약점 지점: 백엔드 단에서 처리되지 않고 사용자에게 그대로 다운로드되는 
      클라이언트 웹 페이지 파일에 민감한 테스트 계정 관리 정보와 개발 일정이 기록된 채 그대로 노출됨.
      
      TODO: 다음 주 정식 배포 전에 이 주석 삭제할 것!
      * 임시 디버깅용 어드민 계정 정보:
        - Username: admin
        - Password: admin_debug_9999
    -->
    
    <script>
        // JS 단 주석도 클라이언트 단에 그대로 노출됩니다.
        console.log("Portal UI Version 1.0.0 Loaded");
    </script>
</body>
</html>
```

---

## 6. 방어 및 완화 기법 (Mitigation)

1. **상용 배포 시 소스코드 압축화 및 정제(Minification & Obfuscation)**:
   - 빌드 및 배포 파이프라인에서 HTML, CSS, JavaScript 소스코드를 빌드할 때 주석을 모두 삭제(Stripping)해 주는 Minifier 도구(예: Webpack, Terser, Esbuild 등)를 파이프라인에 구축하여 인간이 해독 가능한 형태의 모든 주석 줄을 원천 소거합니다.
2. **서버 측 주석 처리 (Server-Side Comments)**:
   - 개발 단계의 메모가 화면상에 부득이하게 필요할 경우, 클라이언트로 내려가지 않는 서버 측 템플릿 엔진 주소 체계(예: PHP의 `<?php /* 주석 */ ?>`, JSP의 `<%-- 주석 --%>`)를 활용하여 최종 웹페이지 HTML 생성 시 주석 데이터가 애초에 포함되지 않게 설계합니다.
3. **엄격한 기밀 관리 정책 (Credential Management Policy)**:
   - 비밀번호, API 키, 데이터베이스 주소 등 보안과 밀접한 자산은 절대로 개발 코드의 주석이나 파일에 평문으로 기록하지 않고, 환경 변수(`.env`) 및 통합 비밀 제어 도구(Secrets Manager)를 통해 격리 운영하는 관리 정책을 준수합니다.
