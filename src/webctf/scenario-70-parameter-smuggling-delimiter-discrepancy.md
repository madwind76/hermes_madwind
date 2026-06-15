---
title: Parameter Smuggling via Delimiter Discrepancy (WAF Bypass) — Web CTF Scenario
created: 2026-06-14
updated: 2026-06-14
type: ctf-scenario
tags: [ctf, web, parameter-smuggling, delimiter-discrepancy, waf-bypass, tomcat, logic-bypass]
confidence: high
---

# Parameter Smuggling via Delimiter Discrepancy (WAF Bypass) — Web CTF Scenario

## 1. 개요 및 스토리
- **문제명**: WAF Guarded Data Searcher (WAF가 감시하는 데이터 검색기)
- **난이도**: Medium-High
- **핵심 컨셉**: 웹 애플리케이션 방화벽(WAF)과 실제 백엔드 웹 애플리케이션 서버 간의 **쿼리 파라미터 구분자(Delimiter) 해석 비대칭성**을 악용하여 보안 감시망을 무력화하는 **Parameter Smuggling** 취약점 문제입니다. 대상 웹 서비스는 외부 유해 요청을 사전에 걸러내기 위해 정방 프록시 WAF 방화벽 장비를 거쳐 들어옵니다. 이 WAF는 파라미터를 구분하는 표준 문자로 오직 앰퍼샌드(`&`)만 인식하고 내부 위협 키워드 필터링을 검사합니다. 그러나 백엔드 WAS(예: Apache Tomcat 등)는 레거시 규격 호환을 이유로 세미콜론(**`;`**) 또한 유효한 파라미터 구분자로 분리 처리합니다. 공격자는 세미콜론 뒤에 악성 페이로드(SQL Injection 등)를 엮어 전송함으로써, WAF는 이를 무해한 하나의 단일 매개변수 값으로 오인하게 하고 백엔드는 이를 완전히 독립된 파라미터 조건문으로 분리 분석하게 만들어 필터를 우회합니다.

---

## 2. 문제 설계 및 구조 (Architecture)

### 2.1 구성 요소
- **Frontend Web Application Firewall (WAF)**:
  - 인입되는 HTTP GET/POST 요청을 전면 감사.
  - 파라미터 분할 문자: 오직 `&` 만 매핑 처리.
  - 필터 룰: `UNION`, `SELECT`, `OR`, `AND` 등 SQL 주입 키워드가 파라미터 키 또는 값에 존재하는지 검사하여 발견 시 차단.
- **Backend Application Server (Apache Tomcat / Java Servlet)**:
  - 쿼리 파라미터 파싱 시 `&` 및 `;` 둘 다 구분 기호로 인정해 키-값을 쪼갭니다:
    `param1=val1;param2=val2` -> `param1: val1, param2: val2`
- **Flag 위치**:
  - WAF의 검사 필터를 회피해 백엔드 SQL Injection 취약 엔드포인트에 쿼리를 통과시킨 후, 데이터베이스 내부의 `flags` 테이블에서 플래그 텍스트 덤프.

### 2.2 취약점 지점
1. **Discrepancy in Parameter Parsing (파라미터 파서 간 비대칭)**:
   - WAF와 백엔드 간에 HTTP 명세의 쿼리스트링 구분자 세부 해석 기준이 어긋나 있습니다.
   - 공격자가 전송한 `id=1;id=UNION SELECT...` 요청이 들어오면:
     - **WAF**: `id` 라는 단일 파라미터 키의 값이 `"1;id=UNION SELECT..."` 인 것으로 판독합니다. 이때 쿼리스트링 전체 검사가 아닌 개별 파라미터 단위 안전성 검사가 적용될 시, 특정 WAF는 값 내부에 세미콜론이 포함된 일반 문자열로 오해하거나, 혹은 앰퍼샌드가 없기 때문에 뒤의 쿼리 조각이 단순 서브 값에 지나지 않는다고 무시하게 됩니다.
     - **백엔드**: 세미콜론 기호 `;`를 매개로 파라미터를 분할하여 `id=1`과 `id=UNION SELECT...` 라는 두 개의 동일 키 다중 입력으로 분해합니다. 다중 파라미터 처리 원칙에 따라 백엔드는 뒤에 정의된 악성 SQL 쿼리를 데이터베이스 질의 스트림으로 흘려보내 작동시킵니다.

---

## 3. 공격 면 (Attack Surface)

| 엔드포인트 | 수신 프록시 | 백엔드 WAS | 주입 구분자 | 우회 타겟 |
|------------|-------------|------------|-------------|-----------|
| `/api/search` | WAF (Only `&` Delimiter) | Tomcat / Java (Supports `;` Delimiter) | `;` (Semicolon) | WAF의 SQLi 필터 룰 우회 및 SQL 인젝션 가동 |

---

## 4. 상세 풀이 흐름 (Exploitation Flow)

### Step 1. WAF의 차단 메커니즘 확인
1. 공격자는 일반적인 SQL Injection 구문을 쿼리로 던져 봅니다.
   `/api/search?id=1' UNION SELECT flag FROM flags --`
2. 프론트 WAF 장비가 이를 감지하여 차단 응답을 회신합니다:
   `HTTP/1.1 403 Forbidden` (WAF SQL Injection Rule Blocked)

### Step 2. WAS 파라미터 구분자 특성 파악
1. 백엔드가 세미콜론을 파라미터 구분자로 인정하는 구조(Java Servlet, Tomcat, Spring 등)인지 간접 확인하기 위해 세미콜론이 가미된 쿼리를 기입해 봅니다.
   `/api/search?id=1;query=test`
2. WAF는 SQL 키워드가 없으므로 통과시키고, 백엔드 서버가 `id=1`의 결과와 `query=test` 조건을 병렬 파싱해 에러 없이 정상 페이지를 출력함을 검증합니다.

### Step 3. Parameter Smuggling WAF 우회 페이로드 조립
세미콜론을 중간에 끼워, WAF 단에서는 단순 문자열 값으로 해석되지만 백엔드로 인계되는 시점에는 유해 쿼리로 분해되는 인젝션을 기획합니다.
- **공격 페이로드**:
  `/api/search?id=1;id='+UNION+SELECT+flag,null+FROM+flags--`
- **구조 분석**:
  - **WAF 관점**: 
    파라미터: `id` (값: `1;id='+UNION+SELECT+flag,null+FROM+flags--`)
    특정 WAF가 파라미터 단일 값 단위로 시그니처 매칭 검사 시, 세미콜론으로 엮인 값 덩어리 전반을 공격으로 인지하지 못하고 일반 조회 값으로 간주해 스킵합니다. (혹은 WAF는 `id`가 하나인 줄 알고 검사했으나 뒤의 주입 부분을 단순 하위 텍스트로 흘려보냄)
  - **Tomcat 백엔드 관점**:
    수신한 쿼리를 `;` 기준으로 분리하여 2개의 파라미터를 생성합니다.
    1. `id` = `1`
    2. `id` = `'+UNION+SELECT+flag,null+FROM+flags--`
    Tomcat은 동일한 이름의 파라미터가 중복 수신될 경우 이들을 쉼표로 연결하거나 배열로 받아 SQL 쿼리를 구성하므로, 취약한 동적 SQL 조합에 의해 공격 구문이 최종 실행됩니다.

### Step 4. flag 획득
1. 조작한 세미콜론 우회 URL을 전송합니다.
2. WAF 필터링을 우회하여 백엔드로 전달된 SQL Injection 쿼리가 정상 실행되어 DB의 `flags` 테이블을 조회합니다.
3. 쿼리 결과로 출력된 화면 텍스트 혹은 응답 데이터 본문에서 플래그(`FLAG{parameter_smuggling_waf_bypass_delimiter_discrepancy}`)를 획득합니다.

---

## 5. 취약점 유발 백엔드 코드 스니펫 (Java Servlet 기반)

```java
// SearchServlet.java (Tomcat 환경에서 구동 중인 취약한 자바 서블릿 예시)
package com.challenge;

import java.io.IOException;
import java.io.PrintWriter;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.Statement;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@WebServlet("/api/search")
public class SearchServlet extends HttpServlet {

    protected void doGet(HttpServletRequest request, HttpServletResponse response) 
            throws ServletException, IOException {
        
        response.setContentType("application/json;charset=UTF-8");
        PrintWriter out = response.getWriter();

        // 취약점 지점 1: Tomcat 컨테이너는 기본적으로 query string 파싱 시 
        // 앰퍼샌드(&)뿐 아니라 세미콜론(;)도 구분자로 취급하여getParameterValues()에 배열로 담아줍니다.
        // 예: ?id=1;id=2 -> id 파라미터 배열에 ["1", "2"]가 탑재됨
        String[] ids = request.getParameterValues("id");

        if (ids == null || ids.length == 0) {
            out.print("{\"error\":\"Missing id\"}");
            return;
        }

        // 전달받은 파라미터들을 하나로 합침
        StringBuilder idBuilder = new StringBuilder();
        for (String id : ids) {
            idBuilder.append(id); 
        }
        String mergedId = idBuilder.toString(); // "1'+UNION+SELECT..." 형태로 복원됨

        try {
            Class.forName("org.postgresql.Driver");
            Connection conn = DriverManager.getConnection("jdbc:postgresql://localhost:5432/webctf", "dbuser", "dbpass");
            Statement stmt = conn.createStatement();
            
            // 취약점 지점 2: 병합된 파라미터 문자열을 바인딩 없이 SQL 쿼리에 직접 결합
            String sql = "SELECT item_name, description FROM items WHERE item_id = '" + mergedId + "'";
            System.out.println("[SQL-EXECUTE]: " + sql);
            
            ResultSet rs = stmt.executeQuery(sql);
            
            // 결과 JSON 출력 처리...
            if (rs.next()) {
                out.print("{\"item_name\":\"" + rs.getString("item_name") + "\", \"desc\":\"" + rs.getString("description") + "\"}");
            }
            conn.close();
        } catch (Exception e) {
            out.print("{\"error\":\"Database Error: " + e.getMessage() + "\"}");
        }
    }
}
```

---

## 6. 방어 및 완화 기법 (Mitigation)

1. **파라미터 구분 기호 비대칭성 조율 (Align Parameter Delimiters)**:
   - 프론트 WAF 장비와 백엔드 애플리케이션의 파라미터 구분자 파싱 기준을 반드시 단일하게 정제하여 통일시킵니다.
   - 백엔드(Nginx/Tomcat/Spring 등) 설정을 조정하여, 앰퍼샌드(`&`) 이외의 구분자(예: 세미콜론 `;`)를 파라미터 나누기 기호로 취급하는 레거시 동작 설정을 완전히 비활성화시킵니다.
     - 예: Tomcat의 `org.apache.tomcat.util.http.Parameters.MAX_COUNT` 설정 및 쿼리 파라미터 내 세미콜론 수용 정책을 엄격히 제한합니다.
2. **엄격한 SQL 파라미터 바인딩 및 ORM 사용**:
   - 파라미터를 여러 개로 쪼개서 우회 주입하더라도 SQL 인젝션 공격으로 변환되지 못하도록, SQL 질의 시 PreparedStatement를 사용하는 매개변수 바인딩(Parameterized Queries) 기법을 기본 사양으로 의무 적용합니다.
3. **WAF 시그니처 룰 및 원시 쿼리스트링 검사 강화**:
   - WAF 정책 설정 시, 개별 파라미터 파싱 후의 값에만 필터를 매칭하지 말고, HTTP 요청 주소 전체 원문(Raw Query String) 영역에서 금지 위협 키워드(`UNION`, `SELECT` 등)가 검출되는 경우 파라미터 키 구조와 무관하게 차단하도록 정책 강도를 강화합니다.
