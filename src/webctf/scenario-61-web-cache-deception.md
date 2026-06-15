---
title: Web Cache Deception (WCD) — Web CTF Scenario
created: 2026-06-14
updated: 2026-06-14
type: ctf-scenario
tags: [ctf, web, cache-deception, wcd, caching, reverse-proxy, proxy-misconfiguration]
confidence: high
---

# Web Cache Deception (WCD) — Web CTF Scenario

## 1. 개요 및 스토리
- **문제명**: Cloud Portal Dashboard (클라우드 포털 대시보드)
- **난이도**: Medium-High
- **핵심 컨셉**: 웹 애플리케이션 프레임워크의 경로 파싱 방식과 리버스 프록시 캐싱 엔진 설정 간의 해석 차이를 파고드는 **웹 캐시 디셉션 (Web Cache Deception, WCD)** 취약점 문제입니다. 대상 애플리케이션은 사용자의 로그인 세션과 민감한 개인 프로필 데이터를 반환하는 `/api/user/settings` API를 제공합니다. 또한, 성능 가속화를 위해 Nginx 등의 캐시 프록시를 전면에 두고 있습니다. 프록시는 파일 확장자가 `.jpg`, `.css`, `.js` 등으로 끝나는 요청을 정적 자원으로 간주해 캐시 스토리지에 자동 적재하도록 구성되었습니다. 공격자는 피해자에게 끝자리에 가짜 이미지 확장자가 부여된 프로필 API 링크(`/api/user/settings/avatar.jpg`)를 클릭하게 만들어, 피해자의 개인정보 응답 내용이 프록시 캐시에 공용 정적 파일로 오인 저장되게 한 후 이를 탈취합니다.

---

## 2. 문제 설계 및 구조 (Architecture)

### 2.1 구성 요소
- **Frontend / Reverse Proxy (Nginx)**:
  - 파일 확장자가 정적 파일 양식(예: `\.(css|js|jpg|jpeg|png)$`)을 띠는 경우 백엔드 응답을 프록시 메모리에 60초간 강제 캐시 설정.
- **Backend API (Spring Boot or Node.js Express)**:
  - `/api/user/settings`에서 로그인 사용자의 민감한 메타 데이터 및 플래그 노출.
  - 경로 파싱 시, `/api/user/settings/avatar.jpg` 와 같이 뒤에 임의의 서브 경로 문자열이 붙어도 이를 무시하거나 파라미터로 취급하여 정상적인 `/api/user/settings` 응답(세션 쿠키에 기반한 정보)을 리턴하는 구조적 특징 보유.

### 2.2 취약점 지점
1. **Discrepancy in Path Resolution (경로 해석의 비대칭성)**:
   - **백엔드**: `/api/user/settings/avatar.jpg` 요청이 유입되었을 때, `avatar.jpg` 부분은 경로 변수로 매핑되지 않으면 와일드카드 처리 등으로 인해 `/api/user/settings` 컨트롤러가 가동되어 개인화된 응답을 출력합니다.
   - **프록시**: 요청 URL의 맨 뒤가 `.jpg`로 끝나므로 이를 정적 이미지 파일로 오판하여 모든 사용자에게 서빙할 수 있도록 캐시 데이터베이스에 `/api/v1/user/settings/avatar.jpg` 주소를 키값으로 설정해 응답 내용을 등록합니다.

---

## 3. 공격 면 (Attack Surface)

| 엔드포인트 | 메소드 | 인증 | 요청 헤더/경로 조작 | 결과 영향 |
|------------|--------|------|---------------------|-----------|
| `/api/user/settings` | GET | 세션 필요 | `/api/user/settings/test.css` | 타겟 사용자의 API 응답이 프록시 정적 영역에 캐시 등록 |

---

## 4. 상세 풀이 흐름 (Exploitation Flow)

### Step 1. 프록시 캐시 규칙 파악
1. 공격자는 일반 파일 요청 시 헤더를 분석합니다.
   `GET /static/logo.png`
   - **응답 헤더**:
     `X-Cache: HIT` 또는 `Cache-Control: public, max-age=60`
2. 특정 정적 확장자에 대해 리버스 프록시 단에서 적극 캐싱을 수행하고 있음을 확인합니다.

### Step 2. 백엔드 와일드카드 경로 파싱 테스트
1. 로그인 세션을 지닌 채 개인화 API 엔드포인트 뒤에 가짜 확장자를 붙여 접속해 봅니다.
   `GET /api/user/settings/styles.css`
2. 서버가 오류(404 Not Found)를 리턴하는 대신, 뒤의 `styles.css`를 무시하고 정상적인 세션 설정 응답(200 OK)과 JSON 개인정보를 출력함을 관찰합니다.
   - **반환된 응답**:
     `{"username":"test_user","api_key":"12345", ...}`

### Step 3. 피해자 유도 및 캐시 유인 (Deception Attack)
1. 공격자는 다음과 같이 가짜 CSS 확장자를 가미한 링크를 합성합니다:
   `http://portal.challenge.local/api/user/settings/avatar.jpg`
2. 관리자 봇(Admin Bot)이 이 링크를 방문하도록 유도합니다.
3. 관리자 봇의 브라우저는 관리자 세션 쿠키를 동반하여 해당 URL에 접근합니다.
4. 백엔드 서버는 관리자 세션을 판별하고 관리자의 중요 설정 데이터(Flag가 내포된 JSON)를 정상 리턴합니다.
5. 중간 리버스 프록시는 응답 전송 과정에서 URL의 `.jpg` 확장자를 감지하여 해당 응답을 캐시 키 `KEY: /api/user/settings/avatar.jpg`로 프록시 캐시 저장소에 등록(Cache Write)합니다.

### Step 4. flag 획득
1. 봇이 방문한 직후(캐시가 만료되기 전 60초 이내), 공격자는 세션 쿠키가 없는 완전 무인증 상태로 동일한 가짜 이미지 주소에 접근합니다:
   `GET http://portal.challenge.local/api/user/settings/avatar.jpg`
2. 리버스 프록시는 해당 URL에 캐시 데이터가 존재하므로, 백엔드로 요청을 보내지 않고 캐시된 관리자의 프로필 응답을 그대로 공격자에게 즉시 반환(Cache HIT)합니다.
3. 공격자는 반환된 응답 데이터 본문에서 관리자의 개인 데이터 및 플래그(`FLAG{web_cache_deception_path_discrepancy_leak}`)를 획득합니다.

---

## 5. 취약점 유발 백엔드 및 프록시 설정 스니펫

### Nginx (취약한 캐시 오설정)
```nginx
# nginx.conf
server {
    listen 80;
    server_name portal.challenge.local;

    location / {
        proxy_pass http://backend_server:8080;
    }

    # 취약점 지점 1: 정적 폴더(/static) 경로 한정이 아닌, 
    # URI 전체 영역에서 확장자만 매칭되면 무조건 캐싱하도록 설정함
    location ~* \.(css|js|jpg|jpeg|png)$ {
        proxy_pass http://backend_server:8080;
        proxy_cache my_zone;
        proxy_cache_valid 200 60s;
        add_header X-Cache $upstream_cache_status;
    }
}
```

### Node.js Express (취약한 라우터 파싱)
```javascript
// server.js (Spring Boot의 @PathVariable 및 Express의 와일드카드 매핑 취약 예시)
const express = require('express');
const cookieParser = require('cookie-parser');
const app = express();

app.use(cookieParser());

// 취약점 지점 2: /api/user/settings 뒤의 모든 서브 와일드카드 경로(예: /avatar.jpg)를 
// 허용하여 동일한 컨트롤러가 응답하도록 매핑
app.get('/api/user/settings*', (req, res) => {
    const session = req.cookies.session;
    if (session !== "valid_admin_session_key") {
        return res.status(401).json({ error: "Unauthorized" });
    }

    // 관리자 개인 기밀 설정 반환
    return res.json({
        role: "admin",
        email: "admin@challenge.local",
        secret_flag: "FLAG{web_cache_deception_path_discrepancy_leak}"
    });
});

app.listen(8080);
```

---

## 6. 방어 및 완화 기법 (Mitigation)

1. **캐시 유효 헤더 제어 (`Cache-Control: private`)**:
   - 세션 상태 및 개인 기밀 정보를 반환하는 모든 중요 API 엔드포인트 응답 헤더에 `Cache-Control: private, no-store, no-cache, must-revalidate` 설정을 철저히 명시하여 프록시 서버 및 브라우저 캐시에 절대 등록되지 않도록 통제합니다.
2. **프록시 캐싱 경로 명확화 (Strict Cache Locations)**:
   - 프록시 캐시 적용 대상을 정적 자원 디렉터리(예: `location /static/` 혹은 `/assets/`) 하위 경로로 확실하게 제한하고, 범용 와일드카드 확장자 패턴 매칭 캐싱을 배제합니다.
3. **경로 파싱 규칙 일치 강화**:
   - 백엔드 웹 컨트롤러 정의 시 와일드카드 경로(`*`) 매핑을 최소화하고, 정확히 `/api/user/settings` 단일 경로와만 1대1 매칭되게 선언하여 서브 경로가 동반된 요청 시 404 에러를 리턴하도록 처리합니다.
