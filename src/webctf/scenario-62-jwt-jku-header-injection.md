---
title: JWS Header Injection (jku parameter validation bypass) — Web CTF Scenario
created: 2026-06-14
updated: 2026-06-14
type: ctf-scenario
tags: [ctf, web, jwt, jws, jku-injection, jwk, signature-bypass, cryptography]
confidence: high
---

# JWS Header Injection (jku parameter validation bypass) — Web CTF Scenario

## 1. 개요 및 스토리
- **문제명**: Global Key Verifier (글로벌 인증 포털)
- **난이도**: High
- **핵심 컨셉**: JWT(JSON Web Token) 및 JWS(JSON Web Signature) 규격의 확장 사양 헤더인 **`jku` (JWK Set URL)**를 활용한 서명 무력화 및 권한 상승 취약점 문제입니다. 대상 애플리케이션은 타사 로그인 연동 및 다중 서비스 동기화를 위해 비대칭키(RS256) 기반 서명을 채택하고, 토큰 검증 시 헤더 내의 `jku` 파라미터가 지시하는 원격 경로에서 검증용 공개키 셋(JWKS)을 받아와 서명을 대조합니다. 그러나 백엔드 검증 모듈이 `jku`가 가리키는 도메인이 신뢰 그룹에 속하는지 판별하는 과정에서 정규표현식이나 문자열 필터링 검증 단계를 부실하게 처리했습니다. 공격자는 `jku` 파라미터를 자신이 개설한 외부 공격용 키 서버 주소로 우회 변조한 토큰을 제출하여 임의의 관리자 세션을 위조하는 데 성공합니다.

---

## 2. 문제 설계 및 구조 (Architecture)

### 2.1 구성 요소
- **JWT Verifier Engine**:
  - 전달받은 토큰 헤더의 `jku` 주소를 동적으로 쿼리하여 공개키 획득:
    `fetch(decodedHeader.jku).then(res => res.json())`
  - 요청 주소 필터에 도메인 검증이 미흡하여 외부 악성 도메인 접속이 허용됩니다.
- **Flag 위치**:
  - `role: admin` 페이로드가 탑재되고 공격자의 JWK 공개키 셋으로 정상 서명되어 검증을 통과한 토큰을 소지한 상태로 어드민 전용 기능 `/api/admin/system`을 호출해 취득.

### 2.2 취약점 지점
1. **Insecure jku Domain Verification**:
   - 개발자는 `jku` 도메인이 자신의 호스트인 `auth.challenge.local`로 시작하는지만 검사하여 통과시키고자 `startsWith("http://auth.challenge.local")` 코드를 적용했습니다.
   - **우회 수단**: 공격자는 오픈 리다이렉트 취약점을 내포한 경로(예: `http://auth.challenge.local/oauth/redirect?url=http://attacker.local`)를 `jku` 값으로 주입하거나, 정규식의 경계 누락 구멍을 노려 `http://auth.challenge.local.attacker.local/jwks.json` 형태로 도메인을 매핑하여 우회 필터링 통과를 달성합니다.

---

## 3. 공격 면 (Attack Surface)

| 엔드포인트 | 메소드 | 인증 | 쿠키/헤더 | 공격 타겟 속성 |
|------------|--------|------|-----------|----------------|
| `/api/verify` | POST | 불필요 | `Authorization: Bearer [JWT]` | JWT 헤더 내 `jku` 주소값 변조 주입 |

---

## 4. 상세 풀이 흐름 (Exploitation Flow)

### Step 1. JWT 헤더 명세 분석
1. 사용자는 일반 로그인 후 발급된 JWT 헤더를 복사하여 디코딩합니다.
   ```json
   {
     "alg": "RS256",
     "typ": "JWT",
     "jku": "http://auth.challenge.local/keys/jwks.json"
   }
   ```
2. 검증용 공개키 주소(`jku`)를 백엔드가 매 요청마다 조회하여 검증에 쓴다는 매커니즘을 식별합니다.

### Step 2. 공격용 키 쌍(JWK Set) 생성
1. 공격자는 로컬 환경에서 테스트용 RSA Public/Private Key Pair를 새로 생성합니다.
2. 생성한 공개키에 대응되는 JSON Web Key(JWK) 객체 데이터를 빌드합니다.
   - **공개키 셋 (`jwks.json`) 예시**:
     ```json
     {
       "keys": [
         {
           "kty": "RSA",
           "use": "sig",
           "alg": "RS256",
           "kid": "attacker-key-1",
           "n": "공개키 모듈러스 n값...",
           "e": "AQAB"
         }
       ]
     }
     ```
3. 이 `jwks.json` 파일을 공격자의 외부 웹 서버(`http://attacker.local/jwks.json`)에 업로드해 둡니다.

### Step 3. jku 도메인 검증 우회 및 위조 토큰 발송
1. 공격자는 생성한 개인키(Private Key)를 활용해 관리자 데이터셋이 담긴 가짜 토큰을 서명합니다.
   - **가짜 토큰 헤더**:
     ```json
     {
       "alg": "RS256",
       "typ": "JWT",
       "kid": "attacker-key-1",
       "jku": "http://auth.challenge.local.attacker.local/jwks.json"
     }
     ```
     *(서버 도메인 검증이 `http://auth.challenge.local` 시작 조건이므로, `auth.challenge.local.attacker.local` 서브도메인을 연결하여 우회 만족시킴)*
   - **가짜 토큰 페이로드**: `{"username": "admin", "role": "admin"}`
2. 위조된 JWT 토큰을 머리에 얹어 `/api/verify` 에 요청을 보냅니다.

### Step 4. flag 획득
1. 백엔드는 우회 주소인 `http://auth.challenge.local.attacker.local/jwks.json`이 신뢰 문자열 패턴을 통과하므로, 외부 공격자 서버에 접속하여 `jwks.json` (공격자 공개키)을 로드해 서명 검증을 돌립니다.
2. 공격자가 자신의 개인키로 서명한 가짜 토큰이므로, 다운로드한 공개키와 정확히 서명이 맞아 떨어져 검증 통과가 성립됩니다.
3. 최종 반환되는 관리자 등급 정보 창에서 플래그(`FLAG{jwt_jku_header_injection_signature_spoofing}`)를 확인합니다.

---

## 5. 취약점 유발 백엔드 코드 스니펫 (Node.js)

```javascript
// verify.js (취약한 jku 파라미터 로딩 및 검증 예시)
const express = require('express');
const jwt = require('jsonwebtoken');
const jwksClient = require('jwks-rsa');
const app = express();

app.use(express.json());

// 취약점 지점 1: jku 도메인 검증이 startsWith로만 체크되어 서브도메인 우회에 취약
function isValidJku(jkuUrl) {
    if (!jkuUrl) return false;
    // auth.challenge.local.attacker.local 과 같은 도메인 통과 허점
    return jkuUrl.startsWith("http://auth.challenge.local");
}

app.post('/api/verify', async (req, res) => {
    const token = req.headers.authorization?.split(' ')[1];
    if (!token) return res.status(401).json({ error: "No token provided" });

    try {
        const decoded = jwt.decode(token, { complete: true });
        const { kid, jku } = decoded.header;

        if (!isValidJku(jku)) {
            return res.status(400).json({ error: "Untrusted JWKS URL" });
        }

        // 취약점 지점 2: 안전하지 않은 jku 원격 경로 주소로 직접 HTTP 요청을 보내 jwks를 취득
        const client = jwksClient({ jwksUri: jku });
        const key = await client.getSigningKey(kid);
        const signingKey = key.getPublicKey();

        // 인증서 서명 검증 가동
        const verified = jwt.verify(token, signingKey, { algorithms: ['RS256'] });

        if (verified.role === 'admin') {
            return res.json({ secret: "FLAG{jwt_jku_header_injection_signature_spoofing}" });
        }
        return res.json({ message: "Hello User" });

    } catch (err) {
        return res.status(403).json({ error: "Signature verification failed", details: err.message });
    }
});

app.listen(8080);
```

---

## 6. 방어 및 완화 기법 (Mitigation)

1. **엄격한 도메인 파싱 및 1대1 비교 (Strict Domain Matching)**:
   - 문자열 단순 접두사 검사(`startsWith`)나 느슨한 정규식을 배제하고, `URL` 파서 객체로 호스트명(Hostname)을 완전 추출한 뒤 정확히 타겟 도메인(`auth.challenge.local`)과 1대1 일치하는지 비교합니다.
2. **동적 jku 로딩 비활성화 및 로컬 JWKS 연동**:
   - 헤더의 `jku` 원격 주소를 매번 조회하는 아웃바운드 연결 패턴을 차단하고, 로컬 디렉터리에 키 셋을 정적 보관하며 토큰 검증 키를 내부 파일 시스템에서 불러오도록 정교화합니다.
3. **타사 오픈 리다이렉트 지점 단속**:
   - 설령 도메인 검증이 맞다 하더라도 신뢰 도메인 내부에 오픈 리다이렉터(Open Redirector) 취약점이 상존하면, 프록시 요청이 우회해 나갈 수 있으므로 타사 서비스 연동 시 리다이렉트 주소를 고정 관리합니다.
