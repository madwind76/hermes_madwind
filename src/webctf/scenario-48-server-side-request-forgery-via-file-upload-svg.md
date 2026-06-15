---
title: SSRF / XXE via SVG File Upload and Rendering — Web CTF Scenario
created: 2026-06-14
updated: 2026-06-14
type: ctf-scenario
tags: [ctf, web, ssrf, xxe, svg, file-upload, image-rendering]
confidence: high
---

# SSRF / XXE via SVG File Upload and Rendering — Web CTF Scenario

## 1. 개요 및 스토리
- **문제명**: Avatar Processor Pro (아바타 이미지 프로세서)
- **난이도**: Medium-High
- **핵심 컨셉**: 사용자가 업로드할 수 있는 아바타 파일 규격 중 **SVG(Scalable Vector Graphics)** 파일의 구조적 특성을 악용하여 내부망 서버 데이터를 취득하는 **SSRF / XXE 결합형** 취약점 문제입니다. 대상 애플리케이션은 사용자가 프로필 이미지로 업로드한 SVG 파일을 서버의 그래픽 라이브러리 엔진(ImageMagick, Librsvg 등)을 거쳐 PNG 규격으로 강제 렌더링 및 변환해 줍니다. 공격자는 XML 문서 형식인 SVG 파일 내부의 엔티티 참조 지시어(XXE)나 외부 객체 로드용 하이퍼링크 태그(`<image href="...">`)를 정교하게 엮어 서버 내부의 특정 클라우드 메타데이터(IMDS) 혹은 내부 관리용 서비스 API 주소에 조회를 시도하고, 반환된 데이터를 렌더링 이미지 결과값으로 변환해 시각적으로 가로챕니다.

---

## 

## 2. 문제 설계 및 구조 (Architecture)

### 2.1 구성 요소
- **Avatar Uploader API (`/api/upload`)**:
  - 사용자가 업로드한 SVG 이미지를 검증 및 수신한 뒤, 서버 내 렌더러를 가동하여 변환된 이미지 경로 혹은 리사이징된 이미지를 응답으로 출력.
- **Internal API Service (Only Internal Access)**:
  - 포트 8080 혹은 169.254.169.254 등 서버 내부 로컬 인터페이스에서만 조회되는 중요 인프라 정보 또는 관리 대시보드 API.
- **Flag 위치**:
  - 내부 API 서버 응답값(`/internal/secret`)에 플래그가 보관되어 있으며, SSRF를 통해 데이터 내용을 읽어오거나 이미지로 나타나게 유도해야 합니다.

### 2.2 취약점 지점
1. **Unrestricted SVG Uploading & Processing**:
   - 개발자는 아바타 이미지로 SVG 포맷을 허용하며, SVG는 픽셀 데이터가 아니라 XML을 표현하는 코드의 형태라는 위험성을 인지하지 못했습니다.
2. **Vulnerable Image Rendering Engine**:
   - 백엔드의 SVG 리더가 XML 외부 엔티티 파싱(XXE)을 억제하지 않아 로컬 시스템 파일 읽기가 가능하거나, 혹은 `<image>` / `<iframe` / `<audio>` 등의 미디어 태그 속 외부 주소 질의(SSRF)를 무방비하게 가동하여 변환 후 이미지 출력창에 해당 자원 내용을 시각적으로 오버레이해 줍니다.

---

## 3. 공격 면 (Attack Surface)

| 엔드포인트 | 메소드 | 인증 | 파라미터 | 데이터 포맷 | 역할 |
|------------|--------|------|----------|-------------|------|
| `/api/upload` | POST | 세션 필요 | `file` | Multipart Form Data | SVG 파일 업로드 및 변환 요청 지점 |
| `/uploads/*.png` | GET | 불필요 | - | Image/PNG | 변환 처리가 끝난 렌더링 이미지 조회 경로 |

---

## 4. 상세 풀이 흐름 (Exploitation Flow)

### Step 1. SVG 업로드 허용 여부 파악
1. 프로필 이미지 설정 메뉴에서 업로드할 수 있는 파일 형식을 분석합니다.
2. `.svg` 파일의 확장자 지정을 시도하고 서버에서 무리 없이 정상 수락하고 변환용 PNG 파일 주소를 돌려주는 것을 확인합니다.

### Step 2. SSRF용 SVG 페이로드 설계
SVG는 벡터 렌더링 시 외부 리소스를 참조할 수 있는 속성을 제공합니다.
- **XML/SVG SSRF 페이로드**:
  ```xml
  <?xml version="1.0" encoding="UTF-8" standalone="no"?>
  <svg width="600" height="400" xmlns="http://www.w3.org/2000/svg">
    <!-- 서버가 이 SVG를 PNG로 그릴 때 내부 API 서비스에 GET 쿼리를 전송하게 유도 -->
    <image href="http://127.0.0.1:8080/internal/secret" width="600" height="400" />
  </svg>
  ```
  *(만약 이미지 렌더러가 외부 HTML 데이터를 텍스트로 그리게 유도하려면 `<text>` 태그 안에 XXE 외부 엔티티를 삽입해 시스템 파일을 유출시킬 수도 있습니다)*
  - **XXE Local File Read 예시**:
    ```xml
    <?xml version="1.0" standalone="yes"?>
    <!DOCTYPE test [
      <!ENTITY xxe SYSTEM "file:///etc/passwd" >
    ]>
    <svg width="500px" height="100px" xmlns="http://www.w3.org/2000/svg">
      <text x="10" y="50" font-size="20">&xxe;</text>
    </svg>
    ```

### Step 3. SVG 페이로드 업로드 요청
1. 설계한 악성 SVG 파일을 업로드 폼을 통해 전송합니다.
2. 서버는 이 파일의 내부 코드를 확인하지 않고 받아들인 뒤, 시스템 로컬 렌더링 도구를 호출해 SVG 코드를 기반으로 PNG 이미지를 새로 컴파일합니다.
3. 이 컴파일 과정에서 서버의 렌더러는 내부 네트워크 `http://127.0.0.1:8080/internal/secret`로 HTTP GET 리퀘스트를 보내 해당 기밀 텍스트를 응답받아 이미지 영역 내에 삽입 묘사합니다.

### Step 4. 변환된 결과물 뷰잉 및 flag 획득
1. 업로드 결과로 제공받은 PNG 아바타 파일 경로(`/uploads/avatar_random123.png`)를 브라우저로 요청해 열어봅니다.
2. 그림 파일 형태로 변환되어 화면에 그려진 그림 내부 문자열(혹은 데이터 덤프 형상)에서 숨겨진 내부 응답 내용인 플래그(`FLAG{svg_image_rendering_engine_ssrf_xxe_leakage}`)를 판독하여 획득합니다.

---

## 5. 취약점 유발 백엔드 코드 스니펫 (Python Flask + ImageMagick/librsvg)

```python
# app.py (취약한 Flask 아바타 업로드 가공 서버 예시)
import os
import subprocess
import uuid
from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__)
UPLOAD_FOLDER = '/tmp/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/api/upload', methods=['POST'])
def upload_avatar():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # 업로드된 파일이 SVG인지 판정
    if file and file.filename.endswith('.svg'):
        filename = str(uuid.uuid4()) + ".svg"
        out_filename = filename.replace(".svg", ".png")
        
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        out_filepath = os.path.join(app.config['UPLOAD_FOLDER'], out_filename)
        
        file.save(filepath)

        # 취약점 지점: SVG 내부의 리스크 요소를 확인(Sanitize)하지 않고 
        # 시스템의 이미지 렌더러(convert/ImageMagick 등)로 이미지 강제 변환
        # 이 시점에 SVG에 정의된 외부 image href 주소에 대해 SSRF 연결이 발생함
        try:
            # ImageMagick을 이용한 SVG to PNG 렌더링 호출
            subprocess.run(["convert", filepath, out_filepath], check=True)
            return jsonify({
                "status": "success",
                "converted_url": f"/uploads/{out_filename}"
            })
        except Exception as e:
            return jsonify({"error": f"Rendering failed: {str(e)}"}), 500
            
    return jsonify({"error": "Only SVG allowed"}), 400

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
```

---

## 6. 방어 및 완화 기법 (Mitigation)

1. **SVG 보안 소독 (SVG Sanitization)**:
   - 사용자가 전송한 SVG 파일의 내용을 파싱하여 사전에 허가되지 않은 위험한 태그(`<image>`, `<feImage>`, `<script>`, `<iframe`, `<object>`, `<embed>`) 및 XML DTD 지시어(`<!DOCTYPE ...>`)를 전부 제거 및 소독(Sanitize)한 뒤 컴파일러에 전달합니다.
2. **이미지 렌더러 네트워크 및 XXE 차단 설정**:
   - ImageMagick 등의 도구 설정 파일(`policy.xml`)을 수정하여 SVG 변환 기능을 비활성화하거나, 혹은 외부 프로토콜/네트워크 통신 기능을 원천 거절하도록 차단 정책을 적용합니다.
   - XML Parser 설정 시 `disallow-doctype-decl`을 활성화하고 외부 엔티티 파싱(`External General Entities`, `External Parameter Entities`)을 전부 비활성화 처리합니다.
3. **네트워크 격리 및 아웃바운드 통제**:
   - 백엔드 변환 프로세스를 실행하는 컨테이너 환경의 아웃바운드 트래픽을 폐쇄망 수준으로 통제하여, 로컬 IP 주소나 내부 중요 네트워크 서비스로의 비인가 요청 생성을 물리적 네트워크 단에서 기각합니다.
