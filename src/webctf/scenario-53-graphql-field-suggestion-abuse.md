---
title: GraphQL Field Suggestion Abuse (Schema Reconstruction) — Web CTF Scenario
created: 2026-06-14
updated: 2026-06-14
type: ctf-scenario
tags: [ctf, web, graphql, suggestion-abuse, schema-leak, information-disclosure, query-bruteforcing]
confidence: high
---

# GraphQL Field Suggestion Abuse (Schema Reconstruction) — Web CTF Scenario

## 1. 개요 및 스토리
- **문제명**: Dark Portal API (어둠의 API)
- **난이도**: Medium-High
- **핵심 컨셉**: GraphQL 인프라의 오류 탐지 도우미 설정을 역이용하여 비공개 API 스펙을 원격 복원하는 **GraphQL Field Suggestion Abuse** 취약점 문제입니다. 대상 애플리케이션은 보안 강화를 위해 인트로스펙션(Introspection) 질의를 명시적으로 비활성화해 외부에서 쿼리 스키마를 사전 분석할 수 없게 설계되었습니다. 하지만 GraphQL 엔진의 기본 에러 가이드라인인 **"Did you mean ...?" (필드 오타 추천)** 기능이 잔존해 있습니다. 공격자는 사전 공격 도구를 사용하여 임의의 필드명을 계속 대입해 본 뒤, 엔진이 "이 필드가 아니라 `[비공개_필드명]`을 의미하셨나요?"라고 반환하는 디버그 추천 힌트를 자동 추적 및 조립함으로써 은폐된 어드민 전용 필드 스키마와 데이터 모델을 전체 복원하여 핵심 데이터 탈취에 성공합니다.

---

## 2. 문제 설계 및 구조 (Architecture)

### 2.1 구성 요소
- **GraphQL Endpoint (`/graphql`)**:
  - 인트로스펙션 요청(`__schema`, `__type`) 차단 필터가 활성화된 엔드포인트.
- **Flag 위치**:
  - 은폐된 비공개 필드(예: `adminSecretFlag` 혹은 `systemSecretConfig`)에 접근하여 질의가 정상 성립되었을 때 추출되는 데이터 내 플래그.

### 2.2 취약점 지점
1. **Unrestricted Field Suggestions Enabled**:
   - GraphQL 개발 환경 및 프로덕션 빌드 단계에서 스키마 에러에 따른 제안 기능(`field suggestion`)이 꺼져 있지 않습니다.
   - 쿼리 질의문에 존재하지 않는 필드를 넘기면, GraphQL 파서는 내부 컴파일 스키마 맵과 레벤슈타인 거리(Levenshtein Distance) 알고리즘을 이용해 근접한 스키마 필드명을 오류 메시지에 노출합니다.
   - 예: `query { user { secret } }` -> `"Cannot query field \"secret\" on type \"User\". Did you mean \"secretFlagAdmin\"?"`

---

## 3. 공격 면 (Attack Surface)

| 엔드포인트 | 메소드 | 인증 | 파라미터 | HTTP 응답 특징 |
|------------|--------|------|----------|----------------|
| `/graphql` | POST | 불필요 | GraphQL Query | 에러 메시지 내부 `"Did you mean ...?"` 구문 탑재 |

---

## 4. 상세 풀이 흐름 (Exploitation Flow)

### Step 1. Introspection 상태 진단
1. 공격자는 스키마 전체를 가져오기 위해 일반적인 인트로스펙션 쿼리를 보냅니다.
   ```graphql
   query { __schema { queryType { name } } }
   ```
2. 서버는 인트로스펙션 기능이 제한되었다는 오류 응답을 리턴합니다:
   `"GraphQL Introspection is disabled for security reasons."`

### Step 2. Suggestion Abuse 취약점 진단
1. 공격자는 스키마 내에 존재할 것 같지 않은 의도적 오타 필드를 기입하여 에러 형식을 분석합니다.
   - **질의**: `query { user { flg } }`
   - **반환**:
     ```json
     {
       "errors": [
         {
           "message": "Cannot query field \"flg\" on type \"User\". Did you mean \"flag\"?"
         }
       ]
     }
     ```
2. 엔진이 입력한 오타를 기준으로 유효한 필드인 `"flag"`를 추천해 줌을 식별하고, 단어 오타 브루트포싱을 가동하면 비공개된 스키마 전체를 발굴할 수 있음을 알아냅니다.

### Step 3. 스키마 복원 자동화 스크립트 가동
1. 공격자는 API 침투 도구(예: `clairvoyance` 또는 custom python script)를 사용하여 문자열 자소 대입 및 사전(Wordlist) 대입 질의를 수행합니다.
2. `adm`, `sec`, `flg`, `sys`, `pass` 등의 단어 시드로 오타 쿼리를 자동 발송합니다:
   - `query { adm }` -> `"Did you mean adminQuery?"`
   - `query { adminQuery { sec } }` -> `"Did you mean secretSystemInfo?"`
3. 스크립트는 반환된 오류의 제안(Suggestions) 영역 속 추천 단어들을 추출하여 계층형 GraphQL 쿼리 맵을 트리 형태로 복원해 냅니다.
4. 분석 결과, 숨겨진 관리자 쿼리 경로인 `adminSystem` 및 그 하위 필드 `flagValueRaw`가 실존함을 식별해 냅니다.

### Step 4. flag 획득
1. 복원 완료한 비공개 쿼리 주소로 정상적인 GraphQL 질의를 발송합니다:
   ```graphql
   query {
     adminSystem {
       flagValueRaw
     }
   }
   ```
2. 백엔드는 스키마 규칙이 맞으므로 정상 데이터를 리턴하고, 공격자는 플래그(`FLAG{graphql_field_suggestion_leak_reconstruction}`)를 취득합니다.

---

## 5. 취약점 유발 백엔드 코드 스니펫 (Python Apollo/Graphene 등 개념)

```javascript
// server.js (Apollo Server v3/v4 개념 기반의 취약 설정 예시)
const { ApolloServer, gql } = require('apollo-server-express');
const express = require('express');
const app = express();

const typeDefs = gql`
  type AdminSystem {
    id: ID!
    # 이 필드는 외부에 전혀 공개하지 않으려고 하며, 인트로스펙션도 꺼두었음
    flagValueRaw: String!
  }

  type Query {
    normalAPI: String!
    adminSystem: AdminSystem
  }
`;

const resolvers = {
    Query: {
        normalAPI: () => "This is public API",
        adminSystem: () => {
            return { flagValueRaw: "FLAG{graphql_field_suggestion_leak_reconstruction}" };
        }
    }
};

const server = new ApolloServer({
    typeDefs,
    resolvers,
    // 취약점 지점 1: 인트로스펙션은 거짓으로 막았으나, 
    // 기본 에러 양식 필터에서 Suggestion 기능을 해제하지 않음
    introspection: false, 
    
    // Apollo Server는 기본적으로 잘못 입력된 필드에 대해 Levenshtein 추천을 에러 메세지에 내포함
    formatError: (error) => {
        // 취약점 지점 2: Did you mean 문구가 제거되지 않고 클라이언트에 그대로 송출됨
        return error;
    }
});

async function start() {
    await server.start();
    server.applyMiddleware({ app });
    app.listen(8080);
}
start();
```

---

## 6. 방어 및 완화 기법 (Mitigation)

1. **에러 메시지 제안 기능 차단 (Disable Field Suggestions)**:
   - 프로덕션(Production) 모드 웹 API에서는 오류 발생 시 필드 추천 로직을 소스코드 단에서 완전히 비활성화시킵니다.
   - Apollo Server의 경우, 플러그인 또는 `formatError` 인터페이스 상에서 에러 내용 속 `"Did you mean ...?"` 문구나 내부 스키마 힌트 문자열을 찾아 삭제하거나 에러 객체를 제약된 일반 텍스트로 단순화 변환해 출력합니다.
     ```javascript
     formatError(error) {
         if (error.message.includes("Did you mean")) {
             // 에러 메세지를 변조하여 필드 명 힌트 유출 원천 차단
             return new Error("Invalid GraphQL Query Execution");
         }
         return error;
     }
     ```
2. **에러 디버깅 세부 모드 완전 오프**:
   - 빌드 단계를 상시 배포용 프로덕션 환경 변수(`NODE_ENV=production`)로 가동하여 개발 단계 디버그 도우미가 동작하지 못하게 억제합니다.
3. **가드 프록시 및 API 게이트웨이 도입**:
   - 허가된 정확한 구조의 질의 쿼리 해시 목록(Persisted Queries) 화이트리스트만 백엔드로 인계하고, 임의 작성 쿼리는 실행 단계 진입 전에 WAF/Gateway 레이어에서 기각합니다.
