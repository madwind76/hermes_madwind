---
title: JWT Key ID (kid) Path Traversal Signature Bypass — Web CTF Scenario
created: 2026-06-14
updated: 2026-06-14
type: ctf-scenario
tags: [ctf, web, jwt, kid, path-traversal, signature-bypass, cryptography]
confidence: high
---

# JWT Key ID (kid) Path Traversal Signature Bypass — Web CTF Scenario

## 1. 개요 및 스토리
- **문제명**: Token File Lock (토큰 파일 보관소)
- **난이도**: Medium-High
- **핵심 컨셉**: JWT(JSON Web Token) 구조의 헤더 내부에 존재하는 **`kid` (Key ID)** 파라미터를 처리할 때 발생하는 **디렉터리 트래버셜(Directory Traversal)** 및 서명 검증 우회 취약점 문제입니다. 대상 애플리케이션은 사용자 세션을 JWT(HS256) 형식으로 클라이언트에 발급하고 복호화 및 검증을 위해 키 파일 보관 폴더 내부에서 `kid` 명칭을 읽어 매칭되는 키 파일을 동적으로 로드합니다. 그러나 공격자가 `kid` 필드를 파일 시스템의 특수 파일인 **`/dev/null`**로 탐색 우회(`../../../../dev/null`)하도록 조작하면, 서버는 빈 파일 내용을 읽어 대칭키 값을 빈 문자열(`""`)로 설정하게 됩니다. 결과적으로 공격자는 빈 문자열(`""`) 키를 사용하여 유효하게 서명된 가짜 Admin JWT 토큰을 만들어 세션을 탈취합니다.

---

## 2. 문제 설계 및 구조 (Architecture)

### 2.1 구성 요소
- **JWT Authentication Layer**:
  - JWT 토큰을 해석할 때, 헤더 속 `kid` 값을 검증 없이 파일 조회 함수(`fs.readFileSync`)에 전달:
    `const key = fs.readFileSync('/var/keys/' + header.kid);`
- **Flag 위치**:
  - 어드민 토큰으로 인증을 우회하고 `/api/admin/flag`에 접근할 때 플래그 획득 가능.

### 2.2 취약점 지점
1. **Unsanitized Path Concatenation in Key Loading**:
   - `kid` 파라미터는 파일 이름만 들어오는 것으로 개발자는 착각하지만, 실제로는 상위 경로로 이동할 수 있는 `../` 문자열 필터링이 없어 경로 변조가 가능합니다.
2. **Deterministic Empty Key Match**:
   - `/dev/null` 파일은 리눅스에서 항상 비어 있는 가상의 널 디바이스 파일입니다. 이를 동적 키 파일로 로드하게 만들면 읽어들인 키의 내용물이 항상 0바이트(공백 문자열 `""`)로 반환됩니다.
   - 공격자는 로컬에서 키 값을 빈 값(`""`)으로 적용해 JWT(HS256) 토큰을 서명 생성하면 서버 측이 `/dev/null`을 대칭키로 바라보고 서명을 검증할 때 정상 서명으로 통과됩니다.

---

## 3. 공격 면 (Attack Surface)

| 엔드포인트 | 메소드 | 인증 | 쿠키 | 비고 |
|------------|--------|------|------|------|
| `/api/flag` | GET | 토큰 필요 | `Authorization: Bearer [JWT]` | 어드민 JWT 서명 통과 검증 및 플래그 획득 지점 |

---

## 4. 상세 풀이 흐름 (Exploitation Flow)

### Step 1. JWT 토큰 분석 및 kid 헤더 발견
1. 포털에 일반 사용자 계정으로 로그인 후 API 요청 헤더의 `Authorization: Bearer <JWT>` 형태를 캡처합니다.
2. JWT 헤더(Base64)를 해독합니다:
   ```json
   {
     "alg": "HS256",
     "typ": "JWT",
     "kid": "key1.key"
   }
   ```
3. 헤더에 `kid` 속성을 통해 대칭키 파일을 로딩하는 로직이 백엔드에 존재함을 추정합니다.

### Step 2. kid Path Traversal 테스트
1. 공격자는 `kid` 값을 조작하여 일반적인 경로 변조 시도를 감행합니다.
2. `kid`를 `../../../../etc/passwd` 등으로 지정했을 때, 서버 내부에서 `etc/passwd`를 대칭키로 삼아 검증을 시도하는 과정에서 에러가 발생하거나 실패하는 것을 확인합니다.
3. 이를 통해 로컬 파일 시스템의 모든 파일을 키 소스로 조작할 수 있음을 알아냅니다.

### Step 3. /dev/null 매핑 및 빈 키 서명 토큰 위조
1. 서버 OS 환경이 리눅스이므로 항상 존재하고 항상 비어 있는 가상 파일 `/dev/null`로 경로를 지정합니다.
   `"kid": "../../../../../../../dev/null"`
2. 빈 문자열(`""` 혹은 `null`)을 비밀키(Secret)로 설정하고 로컬에서 어드민 페이로드를 서명하여 토큰을 만듭니다.
   - **조작된 JWT 페이로드**: `{"username": "admin", "role": "admin"}`
   - **서명 비밀키**: `""` (빈 문자열)
3. 완성된 JWT 토큰은 다음과 같은 형식을 띱니다.
   - Header: `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ii4uLy4uLy4uLy4uLy4uLy4uLy4uL2Rldi9udWxsIn0`
   - Payload: `eyJ1c2VybmFtZSI6ImFkbWluIiwicm9sZSI6ImFkbWluIn0`
   - Signature: 빈 키 `""`로 HS256 서명된 값

### Step 4. flag 획득
1. 위조된 JWT 토큰을 `Authorization: Bearer [TOKEN]` 헤더로 삽입해 `/api/flag`로 요청을 보냅니다.
2. 서버는 헤더 속 `kid` 경로인 `/var/keys/../../../../../../../dev/null`을 읽어 빈 값 `""`으로 비밀키를 세팅하고 서명을 비교합니다.
3. 공격자가 빈 키로 생성한 서명과 정확히 매칭되므로 검증이 성공하고 어드민으로 판명되어 플래그(`FLAG{jwt_kid_path_traversal_signature_nullification}`)를 얻습니다.

---

## 5. 취약점 유발 백엔드 코드 스니펫 (Node.js)

```javascript
// auth.js (취약한 JWT 검증 미들웨어 예시)
const express = require('express');
const jwt = require('jsonwebtoken');
const fs = require('fs');
const path = require('path');
const app = express();

const KEY_DIR = "/var/keys/";

app.get('/api/flag', (req, res) => {
    const authHeader = req.headers.authorization;
    if (!authHeader || !authHeader.startsWith('Bearer ')) {
        return res.status(401).json({ error: "Unauthorized" });
    }

    const token = authHeader.split(' ')[1];
    
    try {
        const decodedHeader = JSON.parse(Buffer.from(token.split('.')[0], 'base64').toString());
        const kid = decodedHeader.kid;

        // 취약점 지점 1: kid 경로 값에 대해 화이트리스트 검증이나 트래버셜 필터가 존재하지 않음
        // 공격자는 '../../../../dev/null'로 /dev/null의 빈 파일 컨텐츠를 로딩 가능
        const keyPath = path.join(KEY_DIR, kid);
        const secretKey = fs.readFileSync(keyPath); // /dev/null을 읽으면 secretKey는 빈 Buffer/String이 됨

        // 취약점 지점 2: 로드된 빈 비밀키를 바탕으로 JWT 서명 검증 수행
        const payload = jwt.verify(token, secretKey, { algorithms: ['HS256'] });

        if (payload.role === 'admin') {
            return res.json({ flag: "FLAG{jwt_kid_path_traversal_signature_nullification}" });
        }
        return res.json({ message: "Welcome User" });

    } catch (err) {
        return res.status(403).json({ error: "Forbidden", details: err.message });
    }
});

app.listen(8080);
```

---

## 6. 방어 및 완화 기법 (Mitigation)

1. **경로 탐색 공격 차단 (Prevent Path Traversal)**:
   - `kid` 파라미터 값에서 `../` 나 `..\\`와 같은 디렉터리 경로 제어 문자를 절대 허용하지 않고 제거합니다.
   - 키 파일 조회 시 `path.basename()` 함수를 강제 적용하여 파일명 부분만 엄격하게 추출합니다.
2. **키 화이트리스트 맵 매핑 (Use Key Map Whitelists)**:
   - 파일 시스템을 직접 조회하지 않고, 정의된 키 식별자 맵(Key Map Object)을 인메모리에 두고 매핑되는 키만 가져오도록 통제합니다.
     ```javascript
     const keyMap = {
         "key1": "secret_abc...",
         "key2": "secret_xyz..."
     };
     const secretKey = keyMap[kid];
     if (!secretKey) throw new Error("Invalid Key ID");
     ```
3. **빈 대칭키 차단 (Disallow Empty Secret)**:
   - 키 파일 로딩 결과가 비어 있거나 일정 길이 미만인 경우 검증 자체를 에러로 처리하여 안전성을 도모합니다.
