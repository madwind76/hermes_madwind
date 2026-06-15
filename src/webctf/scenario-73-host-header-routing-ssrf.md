---
title: HTTP Host Header Proxy Routing SSRF — Web CTF Scenario
created: 2026-06-14
updated: 2026-06-14
type: ctf-scenario
tags: [ctf, web, ssrf, host-header, proxy-routing, infrastructure, routing-ssrf]
confidence: high
---

# HTTP Host Header Proxy Routing SSRF — Web CTF Scenario

## 1. 개요 및 스토리
- **문제명**: Intelligent Routing Edge (지능형 라우팅 에지 프록시)
- **난이도**: High
- **핵심 컨셉**: 프록시/게이트웨이 레이어의 동적 목적지 분석 설계 결함을 역이용하는 **Host 헤더 기반 라우팅 SSRF** 취약점 문제입니다. 대상 서비스 인프라는 외부의 단일 통로인 프록시 에지를 통해 유입되며, 프록시 장비는 내부 마이크로서비스들의 결합 복잡도를 낮추기 위해 클라이언트 HTTP 요청 내의 **`Host` 헤더** 값을 신뢰하여 백엔드 내부 포워딩 IP 및 포트를 동적으로 분석 및 포인팅하도록 구현되었습니다. 공격자는 요청 패킷 내의 `Host` 헤더 필드를 내부 루프백 인터페이스 관리 포트(예: `127.0.0.1:9000`)로 변조하여 전송함으로써, 프록시가 요청을 내부 비공개 관리자 모듈로 직접 인계(Routing)하도록 강제하여 인프라 기밀 정보를 유출시킵니다.

---

## 2. 문제 설계 및 구조 (Architecture)

### 2.1 구성 요소
- **Frontend Reverse Proxy (Node.js Dynamic Proxy / http-proxy)**:
  - 수신된 HTTP 요청을 해석하여 백엔드 마이크로서비스로 라우팅하는 단일 엔트리 포인트.
  - 라우팅 목적지 설정 로직:
    `const targetHost = req.headers.host;`
    `proxy.web(req, res, { target: 'http://' + targetHost });`
- **Internal Admin Console (Port 9000)**:
  - 외부망과 완벽 차단되어 사설망 로컬 호스트(`127.0.0.1:9000`)에서만 접근할 수 있는 서버 관리 제어 패널.
- **Flag 위치**:
  - `http://127.0.0.1:9000/admin/system-diagnostics` 페이지에서 노출되는 진단 데이터 내 플래그.

### 2.2 취약점 지점
1. **Unvalidated Host Header Routing**:
   - 프록시는 외부 도메인 필터링(White-list Host Domain)을 거쳐 들어온 요청에 대해서만 라우팅 처리를 해야 하지만, 인바운드 방화벽을 통과한 HTTP 패킷 내부의 `Host` 헤더를 그대로 목적지 주소로 빌드하여 포워딩합니다.
   - 공격자는 DNS는 정상 공용 도메인을 지정해 인바운드 방화벽/DNS 확인 단계를 뚫고 들어온 뒤, 전송하는 실제 HTTP 패킷 내부 텍스트의 `Host` 헤더만 로컬 호스트(`127.0.0.1:9000`)로 교체하여 프록시가 내부망의 비공개 관리 포트로 접속하게 만듭니다.

---

## 3. 공격 면 (Attack Surface)

| 진입 채널 | 프록시 라우팅 로직 | 인증 필요성 | 변조 대상 헤더 | 최종 타겟 주소 |
|-----------|--------------------|-------------|----------------|----------------|
| 외부 공용 웹 포트 (80/443) | `req.headers.host` 동적 파싱 포워딩 | 불필요 | `Host` | `http://127.0.0.1:9000/` (내부망 전용 관리 콘솔) |

---

## 4. 상세 풀이 흐름 (Exploitation Flow)

### Step 1. 프록시 헤더 신뢰 특성 진단
1. 사용자는 일반 도메인을 지정해 웹 서비스를 이용합니다.
2. HTTP 요청 패킷 내의 `Host` 헤더를 외부의 공격자 수신 웹 서버 주소(`attacker.local`)로 살짝 교체하여 전송해 봅니다.
   - **요청**:
     ```http
     GET / HTTP/1.1
     Host: attacker.local
     Connection: close
     ```
3. 공격자 서버로 프록시 서버의 내부 사설 IP가 찍힌 HTTP 포워딩 연결 요청이 들어옴을 탐지하여, 프록시가 `Host` 헤더 주소를 기반으로 아웃바운드 라우팅을 수행하는 취약점이 존재함을 식별합니다.

### Step 2. 로컬 관리자 콘솔 포트 스캔
1. 내부망에 숨겨져 있을 대표적인 관리자 포트(예: 8080, 9000, 10000, 2375 등)들을 타겟으로 Host 헤더를 변경하여 요청을 순차 전송해 봅니다.
   - **스캐닝 요청 예시**:
     ```http
     GET /admin/system-diagnostics HTTP/1.1
     Host: 127.0.0.1:9000
     Connection: close
     ```
2. 포트 9000번에 진입했을 때, 일반적인 404/502/504 에러 대신 관리자 대시보드 구조의 200 OK HTML 응답 혹은 인증 필터 예외 에러가 리턴되는 포트를 확정합니다.

### Step 3. Routing SSRF 실행
1. 확정한 포트 9000번의 어드민 진단 페이지 경로인 `/admin/system-diagnostics`를 URI 경로로 기재하고, `Host` 헤더를 `127.0.0.1:9000`으로 조작한 HTTP 패킷을 완성해 에지 프록시 서버로 다이렉트 전송합니다.
   - **최종 공격 패킷**:
     ```http
     GET /admin/system-diagnostics HTTP/1.1
     Host: 127.0.0.1:9000
     User-Agent: Mozilla/5.0
     Connection: close
     ```

### Step 4. flag 획득
1. 프록시 서버는 들어온 HTTP 요청의 `Host` 헤더 정보를 파싱하여 `127.0.0.1:9000` 주소를 획득합니다.
2. 프록시는 이 주소로 연결을 빌드하여 `http://127.0.0.1:9000/admin/system-diagnostics` 로 요청을 인계합니다.
3. 내부 관리자 서버는 로컬 호스트(`127.0.0.1`)에서 온 정상 요청으로 판단하여 기밀 시스템 로그를 프록시에 전달하고, 프록시는 이를 그대로 클라이언트에 응답으로 반환합니다.
4. 반환받은 화면 본문 로그에서 최종 플래그(`FLAG{proxy_host_header_routing_ssrf_breach}`)를 취득합니다.

---

## 5. 취약점 유발 백엔드 코드 스니펫 (Node.js Express + http-proxy)

```javascript
// proxy.js (취약한 동적 에지 프록시 서버 예시)
const express = require('express');
const httpProxy = require('http-proxy');
const app = express();
const proxy = httpProxy.createProxyServer({});

// 취약점 지점: 들어온 요청의 headers.host 값을 
// 아무런 화이트리스트 검사나 포트 바인딩 제한 없이 타겟 목적지 주소로 빌드하여 포워딩
app.all('/*', (req, res) => {
    const targetHost = req.headers.host; 
    
    console.log(`[ROUTING] Forwarding request to: http://${targetHost}`);
    
    // 공격자가 Host 헤더를 127.0.0.1:9000 으로 보내면 
    // http://127.0.0.1:9000 내부 관리 서버로 포워딩이 강제 성립됨
    proxy.web(req, res, { 
        target: 'http://' + targetHost,
        changeOrigin: true
    }, (err) => {
        res.status(502).send("Bad Gateway: " + err.message);
    });
});

app.listen(80);
```

---

## 6. 방어 및 완화 기법 (Mitigation)

1. **라우팅 대상 도메인 화이트리스트 엄격 적용 (Strict Host Whitelisting)**:
   - 프록시 장비가 라우팅 목적지를 동적으로 잡을 때, `req.headers.host`가 사전에 승인된 도메인 리스트(예: `portal.challenge.local` 등)에 명확히 속하는지 1대1 매칭 및 엄격한 검사를 거친 후 포워딩 처리를 승인하도록 통제합니다.
2. **사설 대역 및 루프백 호스트 전달 금지**:
   - `Host` 헤더 내부에 루프백 IP(`127.0.0.1`, `localhost`) 또는 사설 IP 대역이 포진해 있는 요청은 게이트웨이 파싱 단계에서 즉각 무효화시키고 `400 Bad Request` 에러를 회신합니다.
3. **정적 라우팅 맵 정의 (Static Route Mapping)**:
   - 클라이언트 헤더 주소를 목적지 IP와 일치시키는 동적 설정을 차단하고, 프록시 설정 파일에 각 도메인 경로별 포워딩 목적지를 정적으로 완전히 고정 정의하여 운영합니다.
     ```nginx
     # Nginx 안전 예시
     location / {
         proxy_pass http://internal_backend_upstream; # 정적 고정
     }
     ```
