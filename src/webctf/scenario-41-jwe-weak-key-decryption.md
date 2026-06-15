---
title: JWE Weak Key Decryption — Web CTF Scenario
created: 2026-06-14
updated: 2026-06-14
type: ctf-scenario
tags: [ctf, web, cryptography, jwe, jwt, weak-key, pbkdf2, session-hijacking]
confidence: high
---

# JWE Weak Key Decryption — Web CTF Scenario

## 1. 개요 및 스토리
- **문제명**: Encrypted Portal (암호화된 포털)
- **난이도**: Medium-High
- **핵심 컨셉**: 암호학적 기밀성을 보장하기 위해 도입된 **JWE (JSON Web Encryption)**의 키 유도 사양 및 암호키 관리 허점을 공략하는 취약점 문제입니다. 대상 애플리케이션은 사용자 세션의 중요 정보를 담은 쿠키 데이터를 JWE(PBES2-HS256+A128KW / A128GCM) 토큰 형식으로 클라이언트 측에 발급하고 복호화해 사용합니다. 그러나 키 유도 알고리즘인 PBKDF2의 비밀 키(Password)가 추측 가능하게 취약하거나, 반복 횟수(`p2c`) 매개변수가 매우 낮게 설정되어 오프라인 무차별 대입 공격(Offline Brute-Force Attack)에 노출됩니다. 공격자는 본인의 JWE 세션을 가로채 분석한 뒤, 로컬 브루트포싱을 수행해 마스터 비밀번호(Password)를 추출하고 이를 통해 관리자(Admin) 권한으로 변조된 신규 JWE 세션을 위조하여 포털에 침투합니다.

---

## 2. 문제 설계 및 구조 (Architecture)

### 2.1 구성 요소
- **Frontend / API Service**:
  - 포털 로그인 시 사용자 정보를 담아 JWE 형태의 `session` 쿠키를 발급.
  - 매 요청마다 `session` 쿠키 내 JWE 토큰을 받아 서버에서 복호화 및 인증 수행.
- **Flag 위치**:
  - `admin` 권한을 획득하고 내부 대시보드 API `/api/flag`에 접근 시 플래그 획득 가능.

### 2.2 취약점 지점
1. **Weak PBKDF2 Password**:
   - JWE PBES2(Password-Based Encryption Scheme 2) 키 합의에 사용된 공용 마스터 비밀번호가 단순 단어로 설정되어 사전 공격에 취약함.
2. **Low PBKDF2 Iteration Count (`p2c`)**:
   - 서버의 키 유도 연산 성능 부담을 줄이기 위해 PBKDF2 반복 횟수(`p2c`)가 권장 사양(최소 수만 회 이상) 대신 극도로 낮은 값(예: `100` 또는 `1000`)으로 하드코딩되어 빠른 속도로 로컬 오프라인 크래킹이 가능.

---

## 3. 공격 면 (Attack Surface)

| 엔드포인트 | 메소드 | 인증 | 쿠키 | 비고 |
|------------|--------|------|------|------|
| `/api/login` | POST | 불필요 | - | 로그인 후 취약한 JWE 발급 |
| `/api/flag` | GET | 세션 필요 | `session=[JWE_TOKEN]` | 어드민 사용자 권한 검증 및 플래그 획득 지점 |

---

## 4. 상세 풀이 흐름 (Exploitation Flow)

### Step 1. JWE 토큰 확인 및 구조 분석
1. 포털에 일반 사용자 계정(`test` / `test`)으로 로그인하고 발급된 `session` 쿠키 값을 수집합니다.
2. 수집된 JWE는 점(`.`)으로 구분된 5개의 부분(Header, Encrypted Key, Initialization Vector, Ciphertext, Authentication Tag)으로 이루어져 있습니다.
3. JWE 헤더(첫 번째 base64 부분)를 디코딩합니다.
   - **디코딩된 헤더 예시**:
     ```json
     {
       "alg": "PBES2-HS256+A128KW",
       "enc": "A128GCM",
       "p2s": "c2FsdF9leGFtcGxlMTIz",
       "p2c": 100
     }
     ```
   - PBKDF2 솔트(`p2s`)값과 반복 횟수(`p2c`: 100)를 획득합니다. 반복 횟수가 100으로 매우 낮아 오프라인에서 키를 찾아내기 쉽다는 것을 인지합니다.

### Step 2. 오프라인 사전 공격 (Brute-Force)
JWE PBES2-HS256+A128KW 스펙의 키 도출 방식에 따라, 비밀번호(Password)와 솔트(`p2s`), 반복 횟수(`p2c`)를 결합해 복호화 키를 얻고, 이 키로 암호화된 대칭키(Encrypted Key)를 푸는 방식으로 마스터 비밀번호를 크래킹하는 도구(예: custom python script 또는 hashcat)를 실행합니다.
- **크래킹 로직 예시 (Python)**:
  ```python
  import base64
  from cryptography.hazmat.primitives.ciphers.aead import AESGCM
  # (생략) 헤더의 p2s, p2c와 Encrypted Key 및 Ciphertext를 이용하여 일반적인 암호 사전 리스트(Rockyou.txt 등) 대입
  ```
- 공격자는 사전 공격을 통해 비밀번호인 `"spring2026"`를 알아내는 데 성공합니다.

### Step 3. 토큰 변조 및 관리자 JWE 생성
1. 알아낸 마스터 비밀번호 `"spring2026"`를 이용해 새로운 암호화 세션 토큰을 직접 빌드합니다.
2. 세션 데이터 내부의 사용자 역할을 `"user"`에서 `"admin"`으로 수정합니다.
   - **원본 데이터(Plaintext Payload)**: `{"username": "test", "role": "user"}`
   - **변조된 데이터(Plaintext Payload)**: `{"username": "admin", "role": "admin"}`
3. 동일한 솔트(`p2s`)와 `p2c` 파라미터를 사용하여 관리자 데이터가 들어간 정상적인 JWE 토큰을 서명 및 암호화하여 생성합니다.

### Step 4. flag 획득
1. 브라우저의 `session` 쿠키에 변조 생성한 관리자 JWE 토큰을 삽입합니다.
2. `/api/flag` 엔드포인트로 GET 요청을 전송합니다.
3. 서버는 전달받은 토큰을 성공적으로 복호화하여 역할을 `"admin"`으로 판별하고 플래그(`FLAG{jwe_pbkdf2_low_iteration_cracking_success}`)를 반환합니다.

---

## 5. 취약점 유발 백엔드 코드 스니펫 (Node.js)

```javascript
// auth.js - JWE 발행 및 파싱 코드 (Node-jose 라이브러리 사용 예시)
const jose = require('node-jose');

// 취약점 지점 1: 유추 가능한 고정 패스워드와 극도로 낮은 iteration 설정
const PASSWORD = "spring2026"; 
const ITERATIONS = 100; // 지나치게 낮은 반복 횟수
const SALT = Buffer.from("salt_example123");

async function createSession(userData) {
    const payload = JSON.stringify(userData);
    
    // PBES2 사양을 활용한 암호화 헤더 정의
    const fields = {
        alg: 'PBES2-HS256+A128KW',
        enc: 'A128GCM',
        p2s: jose.util.base64url.encode(SALT),
        p2c: ITERATIONS
    };

    // PBKDF2 키 도출 과정을 거쳐 대칭키 생성 및 JWE 암호화 수행
    // node-jose 내부에서 패스워드를 기반으로 key 생성
    const keystore = jose.JWK.createKeyStore();
    const key = await keystore.perform('generate', 'oct', 256, {
        k: jose.util.base64url.encode(PASSWORD)
    });

    const encrypted = await jose.JWE.createEncrypt({ format: 'compact', fields }, key)
        .update(payload)
        .final();
        
    return encrypted;
}

async function verifySession(token) {
    try {
        const keystore = jose.JWK.createKeyStore();
        const key = await keystore.perform('generate', 'oct', 256, {
            k: jose.util.base64url.encode(PASSWORD)
        });

        const result = await jose.JWE.createDecrypt(key)
            .decrypt(token);
            
        return JSON.parse(result.payload.toString());
    } catch (err) {
        return null;
    }
}
```

---

## 6. 방어 및 완화 기법 (Mitigation)

1. **안전한 비밀번호 복잡도 설정**:
   - JWE 키 유도에 쓰이는 마스터 비밀키는 최소 32바이트 이상의 엔트로피를 가지는 난수 형태의 보안 비밀키를 사용해야 합니다.
2. **충분한 PBKDF2 반복 횟수 설정 (Increase Iteration Count)**:
   - 키 유도 알고리즘(PBKDF2) 적용 시 권장 표준(최소 10,000 ~ 100,000회 이상)에 맞추어 반복 횟수(`p2c`)를 대폭 상향 설정하여, 오프라인 공격 시 연산 비용을 기하급수적으로 증가시킵니다.
3. **대칭형 세션 관리의 지양**:
   - 마스터 키 노출 시 전체 클라이언트의 세션이 전방위적으로 변조되는 것을 막기 위해, 비대칭 키(RSA/ECDSA) 구조를 적용하거나 세션 저장소를 백엔드(Redis 등)에 위치시키고 난수 토큰 식별자만 발행하는 방식으로 전환합니다.
