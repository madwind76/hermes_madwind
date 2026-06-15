---
title: Unicode Normalization Bypass for Account Takeover — Web CTF Scenario
created: 2026-06-14
updated: 2026-06-14
type: ctf-scenario
tags: [ctf, web, unicode, normalization, account-takeover, homoglyph, business-logic]
confidence: high
---

# Unicode Normalization Bypass for Account Takeover — Web CTF Scenario

## 1. 개요 및 스토리
- **문제명**: Global ID Center (글로벌 계정 중앙 센터)
- **난이도**: Medium-High
- **핵심 컨셉**: 유니코드 문자 처리 표준화 알고리즘의 결함을 공략하는 **유니코드 정규화 우회(Unicode Normalization Bypass)** 계정 탈취 문제입니다. 일반적으로 웹 서비스는 사용자가 동일한 아이디(예: `admin`)로 가입하는 것을 차단합니다. 그러나 가입 시 입력 문자열 검증 단계(Check)와 실제 데이터베이스에 등록되는 단계(Insert) 간에 유니코드 정규화 기법(NFKC/NFD 등)이 적용되는 순서 불일치로 인해, 공격자가 변형된 유니코드 문자(Homoglyph 또는 Accented Character)를 사용해 가입하면 검증 단계를 통과한 후 최종적으로 기존 계정인 `admin` 레코드를 침범하거나 덮어써서 해당 권한을 획득합니다.

---

## 2. 문제 설계 및 구조 (Architecture)

### 2.1 구성 요소
- **Frontend / Registration**: 사용자 ID와 이메일을 등록해 가입하는 회원가입 폼.
- **Backend Service (Python/Flask with SQL Database)**:
  - 회원가입 핸들러 `/api/register` 구동.
  - 가입 검증: 기존 데이터베이스에 가입하려는 `username`이 존재하는지 사전 쿼리.
  - 유니코드 표준화: 백엔드는 가입 전후 혹은 데이터베이스에 입력하기 전 `unicodedata.normalize('NFKC', username)`를 수행하여 텍스트 포맷을 통일하려 함.
- **Flag 위치**: 
  - `admin` 계정으로 패스워드를 재설정하거나 어드민 상태로 `/admin/console`에 접속 시 출력됨.

### 2.2 취약점 지점
1. **Normalization Order Discrepancy**:
   - 데이터베이스 고유 키 검사 시에는 입력값 그대로(예: `admín` - 3번째 글자가 악센트 i) 조회하므로 기존 `admin` 계정이 존재하지 않는 것으로 보고 검증을 통과시킵니다.
   - 검증 통과 후, 가입을 기록하는 시점에 유니코드 NFKC 정규화(`unicodedata.normalize`)가 돌면서 악센트 기호가 분리/소실되거나 표준 `i` 문자(ASCII `0x69`)로 치환되어 최종적으로 데이터베이스에는 `admin`이라는 텍스트로 저장(또는 비밀번호 충돌 업데이트)됩니다.

---

## 3. 공격 면 (Attack Surface)

| 엔드포인트 | 메소드 | 인증 | 입력 값 (Body JSON) | 반환 값 | 비고 |
|------------|--------|------|--------------------|---------|------|
| `/api/register`| POST | 없음 | `{"username": "조작 아이디", "password": "..."}` | 가입 성공 메시지 또는 중복 에러 | 유니코드 취약 가입 지점 |

---

## 4. 상세 풀이 흐름 (Exploitation Flow)

### Step 1. 유니코드 매핑 후보 탐색
공격자는 타겟 아이디인 `admin`과 유니코드 정규화(NFKC) 처리를 통과했을 때 동일한 영문 `i` 또는 `a`로 치환되는 특수 유니코드 문자(Homoglyph)를 물색합니다.
- 영문 소문자 `i` (ASCII `0x69`)로 매핑되는 후보 문자:
  - `í` (Latin Small Letter I with Acute - `U+00ED`)
  - `ı` (Latin Small Letter Dotless I - `U+0131`)
  - `ｉ` (Fullwidth Latin Small Letter I - `U+FF49`)
- **선정 페이로드**: `admın` (Dotless i인 `U+0131` 적용) 또는 `admín`.

### Step 2. 중복 검증 우회 및 회원 가입 요청
1. 공격자는 아이디로 `admın`을 기입하고, 패스워드는 자신이 사용할 임의 값을 지정해 `/api/register`로 POST 요청을 보냅니다.
- *회원가입 요청*:
  ```http
  POST /api/register HTTP/1.1
  Host: auth-center.challenge.local
  Content-Type: application/json

  {"username": "admın", "password": "attacker_pass"}
  ```

### Step 3. 서버 측 정규화 처리 동작 분석
1. **중복 확인 단계**: DB 쿼리 `SELECT * FROM users WHERE username = 'admın'` 실행. 기존 `admin`과는 다른 문자셋이므로 결과가 발견되지 않아 가입 검증을 통과합니다.
2. **정규화 단계**: 저장 전 백엔드 코드가 `unicodedata.normalize('NFKC', 'admın')`을 실행합니다. `ı` (Dotless i)가 영문 일반 소문자 `i`로 정상 치환(Standardization)되면서, 텍스트 데이터가 `"admin"`으로 바뀌게 됩니다.
3. **데이터베이스 기록**: 바뀌어버린 `"admin"` 텍스트와 공격자의 비밀번호 `"attacker_pass"`가 최종 INSERT 처리되거나, 기존 키가 존재한다면 비밀번호 정보가 덮어써(Overwrite/Update)집니다.

### Step 4. 로그인 수행 및 flag 획득
공격자는 일반 로그인창에 ID `admin`과 자신이 설정한 패스워드 `attacker_pass`를 입력해 로그인을 수행합니다. 정상 인증이 성립되어 관리자 콘솔 페이지에 액세스 권한이 주어지고 최종 플래그(`FLAG{unicode_normalization_homoglyph_takeover}`)를 탈취합니다.

---

## 5. 취약점 유발 백엔드 코드 스니펫 (Python Flask with SQLite)

```python
# app.py
from flask import Flask, request, jsonify
import sqlite3
import unicodedata

app = Flask(__name__)

def db_init():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS users (username TEXT UNIQUE, password TEXT)")
    # 실제 어드민 계정 사전 등록
    try:
        cursor.execute("INSERT INTO users VALUES ('admin', 'SuperComplexPassword123!')")
        conn.commit()
    except sqlite3.IntegrityError:
        pass
    conn.close()

@app.route("/api/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username", "")
    password = data.get("password", "")
    
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    
    # 취약점 지점 1: 정규화 전 날것의 입력값 그대로 중복 확인 수행
    # 'admın' (Dotless i)은 'admin'과 대조하여 다르게 판별되므로 조회 실패(통과)
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    if cursor.fetchone():
        conn.close()
        return jsonify({"error": "Username already exists"}), 400
        
    # 취약점 지점 2: 검증이 끝난 후 저장 시점에만 유니코드 NFKC 정규화 적용
    # 이에 따라 'admın'은 'admin'으로 변환됨!
    normalized_username = unicodedata.normalize('NFKC', username)
    
    try:
        # 데이터베이스에 쓰기 (이미 admin이 있으나 SQLite의 INSERT OR REPLACE 설정 또는 덮어쓰기 결함 발생)
        # 만약 고유 키(UNIQUE) 충돌이 나면 덮어쓰거나, 인증 테이블 로직에 따라 비정상 가입 완료됨
        cursor.execute("INSERT OR REPLACE INTO users VALUES (?, ?)", (normalized_username, password))
        conn.commit()
        return jsonify({"status": "success", "message": f"User {normalized_username} registered."})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()

if __name__ == "__main__":
    db_init()
    app.run(host="0.0.0.0", port=5000)
```

---

## 6. 방어 및 완화 기법 (Mitigation)

1. **입력 즉시 정규화 처리 (Early Normalization)**:
   - 사용자로부터 입력 데이터가 인입되는 가장 첫 단계(Input Gateway)에서 곧바로 유니코드 정규화(`normalize`)를 먼저 완벽히 수행한 뒤, 중복 검사 및 DB 쿼리 등 후속 비즈니스 로직을 동작시키도록 순서를 보정합니다.
   - **수정 예시**:
     ```python
     # 요청 인자 파싱 직후 바로 정규화
     raw_username = data.get("username", "")
     username = unicodedata.normalize('NFKC', raw_username)
     
     # 이후 중복 확인과 가입 쿼리 모두 정규화 완료된 'username' 변수만 사용
     cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
     ```
2. **엄격한 캐릭터셋 제한 및 정규식 화이트리스트 필터**:
   - 사용자 계정 생성 ID의 허용 문자 대역을 알파벳 소문자, 숫자, 마이너스 기호 등 표준 ASCII 범위(`^[a-z0-9_\-]+$`)로 제한하여 이외의 유니코드 Homoglyph 문자의 침투 가능성을 원천 배제합니다.
3. **데이터베이스 콜레이션(Collation) 매치 설정**:
   - 데이터베이스 테이블 생성 시 유니코드 변형 문자가 인입되더라도 조회 단계에서 동일하게 인식해 차단하도록 `NOCASE` 또는 정규화 호환 콜레이션을 스키마에 정의합니다.
