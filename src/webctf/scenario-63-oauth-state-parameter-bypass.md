---
title: OAuth state Parameter Missing (Account Linkage CSRF) — Web CTF Scenario
created: 2026-06-14
updated: 2026-06-14
type: ctf-scenario
tags: [ctf, web, oauth, state-parameter, csrf, account-linkage, business-logic]
confidence: high
---

# OAuth state Parameter Missing (Account Linkage CSRF) — Web CTF Scenario

## 1. 개요 및 스토리
- **문제명**: Social Integration Portal (소셜 로그인 연동 센터)
- **난이도**: Medium-High
- **핵심 컨셉**: OAuth 2.0 인증 프로토콜 연동 시 필수 보안 매개변수인 **`state` 파라미터**의 부재로 인해 발생하는 **계정 연동 CSRF (OAuth Account Hijacking)** 취약점 문제입니다. 대상 애플리케이션은 사용자가 자신의 기존 포털 계정에 소셜 로그인(GitHub 등)을 연동할 수 있는 기능을 제공합니다. 그러나 OAuth 연동을 요청하고 인증 서버로부터 Callback 승인 토큰을 수신하는 과정에서 세션 일치성을 판별하기 위한 `state` 검증 처리를 생략했습니다. 공격자는 자신의 소셜 계정이 연동될 대기 상태의 OAuth Callback 동기화 링크를 취득한 뒤, 이를 피해자에게 CSRF 형태로 실행시켜 피해자의 로그인 세션 내부 계정에 공격자의 소셜 ID가 영구 바인딩되게 만들고 이를 통해 로그인을 우회하여 피해자 계정을 하이재킹합니다.

---

## 2. 문제 설계 및 구조 (Architecture)

### 2.1 구성 요소
- **OAuth Linkage Initiator (`/oauth/connect`)**:
  - 사용자가 소셜 연동 버튼을 누르면 연동 처리를 위해 외부 OAuth 제공자 로그인 주소로 리다이렉트.
- **OAuth Callback Handler (`/oauth/callback`)**:
  - 인증 서버가 로그인 성공 후 `code` 파라미터를 실어 되돌려보내는 콜백 엔드포인트.
  - 리퀘스트 세션 검증이 누락되어 다른 사람의 브라우저 컨텍스트에서도 실행 수락됩니다.
- **Flag 위치**:
  - 관리자 봇(Admin Bot)의 포털 계정을 하이재킹하여 로그인한 뒤, 관리자 권한 전용 프로필 데이터에서 플래그 취득.

### 2.2 취약점 지점
1. **Missing state Parameter in Authorization Request**:
   - `/oauth/connect` 기동 시, CSRF 방지용 임의의 난수 토큰(`state`)을 만들어 세션에 담고 주소창에 `&state=RANDOM` 형태로 붙여야 하지만, `state` 변수 자체가 누락되었습니다.
2. **Unvalidated Callback Process**:
   - `/oauth/callback?code=[AUTH_CODE]` 수신 시, 백엔드는 이 요청이 실제로 해당 브라우저에서 최초 발의한 로그인 흐름인지 확인하지 않고, 현재 세션 사용자 계정에 소셜 정보를 그대로 연동해 버립니다.

---

## 3. 공격 면 (Attack Surface)

| 엔드포인트 | 메소드 | 인증 상태 | 파라미터 | 취약점 핵심 원인 |
|------------|--------|-----------|----------|------------------|
| `/oauth/callback` | GET | 피해자 세션 활성 상태 | `code` | `state` 토큰 유무 및 정합성 검사 누락 |

---

## 4. 상세 풀이 흐름 (Exploitation Flow)

### Step 1. OAuth 연동 프로토콜 분석
1. 일반 계정으로 로그인한 뒤 소셜 계정 연동 버튼을 누르고 잡힌 패킷을 봅니다.
   - **리다이렉트 주소**:
     `https://github.com/login/oauth/authorize?client_id=123&redirect_uri=http://target.local/oauth/callback&scope=user`
2. 주소창 및 파라미터 내부에 세션 보안용 임의 문자열인 `state` 파라미터가 보이지 않음을 식별하고 CSRF 연동 기회가 열려있음을 인지합니다.

### Step 2. 공격자의 OAuth 승인 코드(Code) 캡처
1. 공격자는 자신의 계정으로 소셜 연동을 진행합니다.
2. GitHub 로그인 창을 통과한 후, 브라우저가 타겟 포털의 콜백 주소 `/oauth/callback?code=ATTACKER_CODE`로 리다이렉트되는 찰나의 요청 패킷을 강제 일시 정지(Intercept)하고, 이 콜백 요청이 완료되지 않도록 차단하여 코드값 `ATTACKER_CODE`를 미사용 유효 상태로 확보합니다.

### Step 3. Account Linkage CSRF 시나리오 가동
1. 공격자는 이 차단된 콜백 주소를 피해자가 자신의 세션 컨텍스트 하에서 대신 실행하도록 유인하는 익스플로잇 HTML 페이지를 만듭니다.
   - **공격 HTML**:
     ```html
     <html>
     <body>
         <!-- 피해자 세션 상태에서 공격자의 OAuth 승인 코드를 실행시킴 -->
         <img src="http://target.local/oauth/callback?code=ATTACKER_CODE" style="display:none;" />
     </body>
     </html>
     ```
2. 이 페이지 링크를 관리자 봇(Admin Bot)에게 보냅니다.

### Step 4. flag 획득
1. 관리자 봇이 악성 페이지를 오픈하면, 봇의 세션(관리자 세션) 하에서 `target.local/oauth/callback?code=ATTACKER_CODE` 호출이 강제 실행됩니다.
2. 서버는 `state` 검증이 없으므로, 현재 접속자(관리자)의 계정에 `ATTACKER_CODE`가 지시하는 소셜 계정(공격자 소셜 ID)을 정상 매핑 및 바인딩 완료합니다.
3. 이제 공격자는 포털의 일반 로그인 메뉴로 이동하여 "소셜 계정(GitHub)으로 로그인" 버튼을 눌러 자신의 소셜 ID로 진입합니다.
4. 서버는 공격자의 소셜 ID가 관리자 계정과 연동되어 있으므로, 공격자를 관리자(Admin) 권한으로 로그인 처리해 줍니다.
5. 포털 관리 대시보드에서 플래그(`FLAG{oauth_state_parameter_missing_account_linkage_csrf}`)를 획득합니다.

---

## 5. 취약점 유발 백엔드 코드 스니펫 (Node.js Express)

```javascript
// oauth.js (취약한 OAuth 연동 콜백 예시)
const express = require('express');
const axios = require('axios');
const app = express();

const CLIENT_ID = "12345";
const CLIENT_SECRET = "secret_key";
const REDIRECT_URI = "http://target.local/oauth/callback";

// 1. 소셜 연동 요청 초기화
app.get('/oauth/connect', (req, res) => {
    // 취약점 지점 1: CSRF 방지용 임의 state 난수를 생성하여 세션에 보관하는 로직 누락
    // res.redirect(`https://github.com/...&state=${randomState}`) 가 권장 사항
    res.redirect(`https://github.com/login/oauth/authorize?client_id=${CLIENT_ID}&redirect_uri=${REDIRECT_URI}`);
});

// 2. OAuth Callback 처리 핸들러
app.get('/oauth/callback', async (req, res) => {
    const { code } = req.query;
    
    // 취약점 지점 2: 쿼리로 들어온 state 값과 세션에 저장해두었던 state 값이 일치하는지 검증하는 구문 결여
    if (!code) return res.status(400).send("No Auth Code Provided");

    try {
        // 인가 코드를 이용해 소셜의 access_token 취득
        const tokenRes = await axios.post("https://github.com/login/oauth/access_token", {
            client_id: CLIENT_ID,
            client_secret: CLIENT_SECRET,
            code: code,
            redirect_uri: REDIRECT_URI
        }, { headers: { accept: 'application/json' } });

        const accessToken = tokenRes.data.access_token;
        
        // 소셜 사용자 정보 호출
        const userRes = await axios.get("https://api.github.com/user", {
            headers: { Authorization: `token ${accessToken}` }
        });
        const githubUserId = userRes.data.id;

        // 현재 로그인된 사용자의 DB 엔트리에 해당 GitHub ID를 연동 처리
        // 만약 관리자가 이 콜백을 실행했다면 관리자 레코드에 공격자의 githubUserId가 바인딩됨
        const currentUser = req.session.userId; 
        if (currentUser) {
            await db.linkSocialAccount(currentUser, 'github', githubUserId);
            return res.send("GitHub 계정이 정상적으로 연동되었습니다.");
        } else {
            // 소셜 아이디 기반 로그인 처리
            const user = await db.findUserBySocialId('github', githubUserId);
            req.session.userId = user.id;
            return res.redirect('/dashboard');
        }

    } catch (err) {
        return res.status(500).send("OAuth 동기화 중 오류 발생: " + err.message);
    }
});

app.listen(8080);
```

---

## 6. 방어 및 완화 기법 (Mitigation)

1. **`state` 파라미터 필수 적용 및 검증 (Enforce Cryptographic state)**:
   - OAuth 인증 흐름을 개시하는 단계에서, 예측 불가능한 암호학적 일회성 난수 토큰(`state`)을 생성하여 사용자의 세션에 바인딩합니다.
   - 인증 서버로 리다이렉트 시 이 `state` 값을 주소창에 파라미터로 함께 실어 발송합니다.
2. **콜백 단 1대1 무조건 대조**:
   - 인증 콜백 수신 핸들러(`/oauth/callback`)에서 쿼리 파라미터의 `state` 값과 세션 속 저장된 `state` 값을 비교하여, 불일치하거나 세션에 토큰이 부재할 시 비정상적인 외부 CSRF 요청으로 간주하고 처리를 즉각 거절합니다.
     ```javascript
     if (!req.query.state || req.query.state !== req.session.oauthState) {
         return res.status(403).send("CSRF Detected: State Mismatch");
     }
     ```
3. **사용자 재인증 가동**:
   - 계정 연동 등 보안 민감 논리 실행 직전, 현재 사용자의 비밀번호를 다시 한번 재확인(Re-authentication)하는 단계를 두어 비동기 백그라운드 공격 위협을 방지합니다.
