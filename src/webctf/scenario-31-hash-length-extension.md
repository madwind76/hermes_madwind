---
title: Hash Length Extension Attack on Signed URLs — Web CTF Scenario
created: 2026-06-14
updated: 2026-06-14
type: ctf-scenario
tags: [ctf, web, hash-length-extension, md5, cryptography, signed-url, bypass-signature]
confidence: high
---

# Hash Length Extension Attack on Signed URLs — Web CTF Scenario

## 1. 개요 및 스토리
- **문제명**: Secure File Downloader (보안 파일 다운로더)
- **난이도**: Medium-High
- **핵심 컨셉**: 암호학적 해시 함수의 구조적 결함(Merkle-Damgård 구조)을 악용하는 **해시 길이 확장 공격(Hash Length Extension Attack)** 취약점 문제입니다. 서버는 다운로드할 파일명을 포함하여 API 요청 검증용 서명 값을 생성할 때 `md5(secret_key + filename)` 구조를 사용합니다. 공격자는 비밀키(`secret_key`)의 값은 모르지만, 그 **길이**만을 추정한 뒤 이미 알려진 임의 파일의 서명값을 시작점으로 삼아, 내부 상태 정보를 조작하고 뒤쪽에 `/../../etc/passwd`와 같은 경로 탐색(Path Traversal) 공격 구문을 주입한 새로운 파일명과 이에 유효한 서명을 변조 생성하여 서명 확인 절차를 우회하고 기밀 파일을 강제로 다운로드합니다.

---

## 2. 문제 설계 및 구조 (Architecture)

### 2.1 구성 요소
- **Frontend**: 팩트 시트, 제품 설명서 등을 링크로 클릭하면 다운로드받을 수 있는 사용자 화면.
- **Backend Service (Python/Flask)**:
  - 다운로드 핸들러 `/api/download?file=filename.txt&sig=md5_hash` 제공.
  - 서명 생성 알고리즘: `hash_val = md5(SECRET_KEY + file)`
  - 수신한 `file`과 `sig`를 검증하고, 서명이 일치하는 경우에만 로컬 파일을 열어 응답함.
- **Flag 위치**: 
  - 서버 시스템 파일 내: `/flag.txt`

### 2.2 취약점 지점
1. **Insecure MAC Construction (Length Extension Vulnerability)**:
   - MD5나 SHA1, SHA256과 같은 Merkle-Damgård 기반 해시 알고리즘은 내부 패딩 구조로 인해, `hash(message)` 값을 알고 있으면 `message` 뒤에 악성 데이터를 추가한 `hash(message + padding + extra_data)` 값을 비밀키 없이도 계산할 수 있는 취약점을 가지고 있습니다.
   - `md5(key + data)`로 서명을 만드는 방식(가짜 MAC)은 이 공격에 노출되므로 안전하지 않습니다.

---

## 3. 공격 면 (Attack Surface)

| 엔드포인트 / 파라미터 | 메소드 | 인증 | 입력 값 | 반환 값 | 비고 |
|---------------------|--------|------|---------|---------|------|
| `/api/download` | GET | 없음 | `file`, `sig` | 다운로드할 파일 바이너리 / 에러 | 서명 우회 및 LFI 타켓 경로 |

---

## 4. 상세 풀이 흐름 (Exploitation Flow)

### Step 1. 정상 요청 및 해시값 수집
사용자는 웹 메인 화면에서 제공되는 기본 파일 다운로드 링크를 캡처하여 정보들을 수집합니다.
- *정상 요청*: `/api/download?file=welcome.txt&sig=8fa6a8d672ef...`
- *알려진 평문*: `welcome.txt`
- *알려진 MD5 해시*: `8fa6a8d672ef...`
- *비밀키 길이 추정*:
  웹 개발 소스 분석 또는 무차별 대입을 통해 비밀키의 길이를 `16`바이트로 가정합니다.

### Step 2. Hash Length Extension 공격 도구 활용
공격자는 `hashpump` 또는 파이썬의 `hashpumpy` 라이브러리를 사용해 조작된 페이로드와 서명을 생성합니다.
- **공격 시나리오**:
  기존 파일명 `welcome.txt`에 패딩을 덧붙인 뒤 LFI 경로 탐색 문자열(`../../../../flag.txt`)을 이어 붙입니다.
- **해시 펌프 실행 (hashpump 이용 예시)**:
  ```bash
  # 키 길이 16, 원본 데이터 welcome.txt, 원본 해시 8fa6a8d672ef..., 추가할 데이터 ../../../../flag.txt
  hashpump -s "8fa6a8d672ef..." -d "welcome.txt" -a "../../../../flag.txt" -k 16
  ```
- *출력 결과*:
  - **새로운 해시(서명)**: `5e89d873...`
  - **새로운 전송 페이로드 (Hex 인코딩 포함)**:
    `welcome.txt\x80\x00...\x00\x00\x80\x00../../../../flag.txt` (URL 인코딩 포맷으로 변환)

### Step 3. 조작된 파라미터 요청 전송
공격자는 인쇄된 페이로드와 위조 서명을 대입해 웹 서버에 파일을 요청합니다.
- *공격 요청 URL*:
  `/api/download?file=welcome.txt%80%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%5c%00%00%00%00%00%00%00..%2f..%2f..%2f..%2fflag.txt&sig=5e89d873...`

### Step 4. flag 획득
서버는 전달받은 위조 `file` 파라미터(패딩이 포함된 긴 문자열)를 가져와 내부적으로 `md5(SECRET_KEY + file)`를 다시 계산합니다. 해시 길이 확장 공격 원리에 의해, 공격자가 생성해 준 해시값(`5e89d873...`)과 백엔드 계산 해시가 완벽히 일치하게 되므로 서명 검증을 통과합니다. 
이후 서버가 `open(file)`을 실행할 때, 패딩 데이터 뒤의 상대 경로 문자열(`/../../../../flag.txt`)이 파일 시스템 해석 단계에서 상위 경로로 성공적으로 이스케이프되어 `/flag.txt` 내용을 읽어 오고, 공격자는 최종 플래그(`FLAG{length_extension_attack_bypasses_simple_mac}`)를 획득합니다.

---

## 5. 취약점 유발 백엔드 코드 스니펫 (Python Flask)

```python
# app.py
from flask import Flask, request, send_file, abort
import hashlib
import os

app = Flask(__name__)

# 보안 기밀 키 (길이 16)
SECRET_KEY = b"supersecretkey12"

@app.route("/api/download")
def download_file():
    filename = request.args.get("file")
    signature = request.args.get("sig")
    
    if not filename or not signature:
        return "Missing parameters", 400
        
    # 취약점 지점: 단순한 md5(secret + data) 형식의 서명 구현
    # 이는 해시 길이 확장 공격에 무기력하게 무력화됩니다.
    expected_sig = hashlib.md5(SECRET_KEY + filename.encode('utf-8')).hexdigest()
    
    if signature != expected_sig:
        return "Invalid signature!", 403
        
    # 서명 통과 후 파일 경로 지정
    # 실제 환경에서 경로 정규화(safe check)가 부실할 시 LFI 발생
    base_dir = "static/files/"
    target_path = os.path.join(base_dir, filename)
    
    # Null byte나 패딩 문자 뒷부분의 경로 탐색 지시어 해석
    # os.path.join("static/files/", "welcome.txt[padding]/../../../../flag.txt") -> /flag.txt로 해석 가능
    try:
        # 경로 정규화로 안전하게 읽기
        real_path = os.path.abspath(target_path)
        return send_file(real_path)
    except Exception as e:
        return str(e), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
```

---

## 6. 방어 및 완화 기법 (Mitigation)

1. **HMAC 규격 표준 사용 (Use HMAC-SHA256)**:
   - 길이 확장 공격을 방어하기 위해 설계된 표준 암호학적 메시지 인증 코드 알고리즘인 **HMAC** 기법을 사용하여 서명을 구현합니다.
   - **올바른 수정 예시**:
     ```python
     import hmac
     import hashlib
     
     # hmac 라이브러리를 이용해 해싱
     expected_sig = hmac.new(SECRET_KEY, filename.encode(), hashlib.sha256).hexdigest()
     ```
2. **입력 파일 경로 정규화 및 상위 디렉터리 접근 차단**:
   - 파일 이름 인자에서 디렉터리 경로 기호(`/`, `\`, `.`)를 전면 거부하고, 파일 명칭 자체(basename)만 추출하여 허용된 하위 폴더 내에서만 조회 가능하도록 고정합니다.
3. **서명 포맷의 순서 역전 또는 대안 알고리즘**:
   - SHA-3 또는 BLAKE2 같은 해시 알고리즘은 Merkle-Damgård 구조가 아니므로 길이 확장 공격에 강건합니다.
   - 임시 조치로 `md5(data + secret)`와 같이 키를 뒤에 두는 방식도 고려할 수 있으나, 가급적 표준 **HMAC** 규격 도입을 의무화합니다.
