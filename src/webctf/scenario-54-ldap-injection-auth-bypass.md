---
title: LDAP Injection for Authentication Bypass and Data Extraction — Web CTF Scenario
created: 2026-06-14
updated: 2026-06-14
type: ctf-scenario
tags: [ctf, web, ldap, ldap-injection, authentication-bypass, data-exfiltration, active-directory]
confidence: high
---

# LDAP Injection for Authentication Bypass and Data Extraction — Web CTF Scenario

## 1. 개요 및 스토리
- **문제명**: Intranet Directory Finder (사내 임직원 조회기)
- **난이도**: Medium-High
- **핵심 컨셉**: 기업형 디렉터리 통합 관리 서비스인 **LDAP (Lightweight Directory Access Protocol)** 환경에서 검색 질의 처리 시 발생하는 **LDAP 인젝션** 취약점 문제입니다. 대상 애플리케이션은 사내 인트라넷 환경으로, 로그인 인증 및 직원 주소록 검색 기능을 내부 LDAP 서버와 연동하여 수행합니다. 이때 개발자가 사용자 입력값을 검증 없이 LDAP 필터 쿼리 스트링 문자열과 직접 조립하는 실수를 범했습니다. 공격자는 LDAP 필터 문법의 특수 메타 문자들(예: `*`, `(`, `)`, `&`, `|`)을 정교하게 주입해 검색 범위를 변조함으로써 비공개 어드민 계정의 속성 데이터를 탈취하거나 로그인 패스워드 검증 로직 자체를 무력화하여 시스템 관리자 권한을 강탈합니다.

---

## 2. 문제 설계 및 구조 (Architecture)

### 2.1 구성 요소
- **LDAP Directory Service**:
  - `ou=users,dc=challenge,dc=local` 트리 하에 사용자 정보를 보유. 어드민 계정 정보(`cn=admin`) 포함.
- **Portal Search / Login API**:
  - 사번이나 부서, 혹은 사용자 ID를 입력받아 내부 LDAP 쿼리를 구성 및 조회:
    `(&(objectClass=user)(uid=[USER_INPUT]))`
- **Flag 위치**:
  - `cn=admin` 사용자 개체 정보의 특정 속성 필드(예: `description` 혹은 `employeeNumber`) 내에 플래그가 기입되어 있습니다.

### 2.2 취약점 지점
1. **Unescaped LDAP Filter Construction**:
   - 주입 값이 필터 괄호 구조를 깨고 새로운 논리 연산자(`&`, `|`, `!`)를 삽입할 수 있어, LDAP 쿼리 평가 트리가 공격자의 의도대로 작동합니다.
   - 예: `uid` 변수에 `*`를 넣으면 모든 사용자 정보가 리턴되며, `admin)(description=*` 형태를 기입하면 속성 유무 검증 구조로 변조할 수 있습니다.

---

## 3. 공격 면 (Attack Surface)

| 엔드포인트 | 메소드 | 인증 | 파라미터 | 데이터 포맷 | 역할 |
|------------|--------|------|----------|-------------|------|
| `/api/search` | GET | 불필요 | `username` | Query Parameter | 직원 조회 필터 (공격 주입 벡터) |
| `/api/login` | POST | 불필요 | `user`, `pass` | JSON / Form | LDAP 연동 포털 로그인 지점 |

---

## 4. 상세 풀이 흐름 (Exploitation Flow)

### Step 1. LDAP 쿼리 동작 여부 식별
1. 검색 창에 일반 문자를 넣어 조회 결과를 봅니다.
2. 와일드카드 기호인 `*`를 입력 파라미터로 대입했을 때, 시스템의 모든 유저 목록이 출력되는 것을 확인합니다.
3. 괄호 기호 `)`를 기입했을 때 LDAP 파서 에러(LDAP Syntax Error / Bad Search Filter)가 웹 화면 혹은 서버 로그에 나타나는 것을 확인하여 LDAP 쿼리 빌드 과정에 인젝션이 통함을 직단합니다.

### Step 2. 인증 우회 공격 (Login Bypass)
백엔드가 패스워드까지 LDAP에서 한 번에 검사하기 위해 아래의 쿼리를 돌린다고 가정합니다:
`(&(uid=[USER_INPUT])(userPassword=[PASSWORD_INPUT]))`
공격자는 `user` 인자 칸에 다음과 같이 주입합니다:
- **주입 문자열**: `admin)(objectClass=*`
- **완성 쿼리**:
  `(&(uid=admin)(objectClass=*)(userPassword=[PASSWORD_INPUT]))`
  여기서 `&` 연산자는 `(uid=admin)`과 `(objectClass=*)` 두 조건이 참이면 성립하고 뒤의 패스워드 검증 괄호는 무시될 수 있습니다. 
  *(LDAP 구현과 라이브러리에 따라 뒤의 여분 괄호를 무시하기 위해 널 바이트 `%00`를 끝에 붙여 쿼리를 인위 종결하기도 함: `admin)(%00`)*
- 이를 통해 비밀번호를 기입하지 않고도 `admin` 계정으로의 세션 로그인이 체결됨을 확인합니다.

### Step 3. Blind LDAP Injection을 이용한 데이터 추출
만약 조회 결과가 직접 노출되지 않고 성공 여부(True/False)만 판단할 수 있는 구조라면, Blind SQLi와 유사하게 문자 비교를 수행하여 관리자의 속성값을 파헤칩니다.
- **구조**: `admin)(description=[CHAR]*`
- **테스트 시나리오**:
  - `username=admin)(description=F*` -> 참(결과 존재)
  - `username=admin)(description=FL*` -> 참(결과 존재)
  - `username=admin)(description=FLA*` -> 참(결과 존재)
  - `username=admin)(description=FLAZ*` -> 거짓(결과 없음)
- 위와 같이 한 글자씩 문자를 대입해 참/거짓 판단을 수행하는 익스플로잇 스크립트를 작동시킵니다.

### Step 4. flag 획득
1. Blind LDAP Injection 자동화 스크립트를 통해 `cn=admin` 계정의 `description` 정보를 순차 덤프합니다.
2. 최종 추출된 속성 데이터에서 플래그 값(`FLAG{ldap_injection_filter_bypass_data_leak}`)을 취득합니다.

---

## 5. 취약점 유발 백엔드 코드 스니펫 (Python django-auth-ldap / ldap3 라이브러리 예시)

```python
# app.py (취약한 LDAP 조회 Flask 서버 예시)
import ldap3
from flask import Flask, request, jsonify

app = Flask(__name__)

LDAP_SERVER = "ldap://localhost:389"
BASE_DN = "ou=users,dc=challenge,dc=local"

@app.route('/api/search', methods=['GET'])
def search_user():
    username_input = request.args.get('username', '')

    if not username_input:
        return jsonify({"error": "Missing username"}), 400

    # 취약점 지점: 사용자의 입력을 LDAP 필터 문자열과 그대로 결합(Concatenate)
    # 입력값에 괄호나 특수문자가 필터링되지 않아 LDAP 쿼리 구조가 변조됨
    search_filter = f"(&(objectClass=user)(uid={username_input}))"
    
    try:
        server = ldap3.Server(LDAP_SERVER, get_info=ldap3.ALL)
        conn = ldap3.Connection(server, auto_bind=True)
        
        # LDAP 검색 수행
        conn.search(
            search_base=BASE_DN,
            search_filter=search_filter,
            attributes=['uid', 'cn', 'description']
        )
        
        results = []
        for entry in conn.entries:
            results.append({
                "uid": entry.uid.value,
                "cn": entry.cn.value,
                # Admin의 description에 FLAG{ldap_injection_filter_bypass_data_leak} 존재
                "description": entry.description.value if entry.uid.value != 'admin' else "Hidden"
            })
            
        return jsonify({"status": "success", "users": results})
    except Exception as e:
        return jsonify({"status": "error", "message": f"LDAP Query Failed: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
```

---

## 6. 방어 및 완화 기법 (Mitigation)

1. **사용자 입력 특수 문자 이스케이프 (LDAP Sanitization & Escaping)**:
   - LDAP 필터 구문에서 특별한 의미를 지니는 메타 문자들인 `\`, `*`, `(`, `)`, `\x00` (NUL) 기호들을 사용자 입력값 수신 시 반드시 백슬래시 이스케이프 코드로 치환 처리합니다.
   - 예: `(` -> `\28`, `)` -> `\29`, `*` -> `\2a`, `\` -> `\5c` 등 RFC 4514/4515 명세에 맞춘 인코딩 함수를 사용합니다.
2. **화이트리스트 기반 정규식 필터링**:
   - 입력값에 대해 오직 알파벳과 숫자(`^[a-zA-Z0-9]+$`)만 들어오도록 강제하는 입력 검증 미들웨어를 도입하여 특수 문자가 주입될 틈새를 사전에 원천 차단합니다.
3. **LDAP Parameterized Queries / SDK Safe APIs**:
   - Raw String 조립을 지양하고, 사용 중인 LDAP SDK 라이브러리에서 인자 주입 공격 방어가 기본 내장된 안전한 매칭 API 객체를 연동하여 개발할 것을 권장합니다.
