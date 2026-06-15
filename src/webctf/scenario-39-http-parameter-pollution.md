---
title: HTTP Parameter Pollution (HPP) to Bypass WAF — Web CTF Scenario
created: 2026-06-14
updated: 2026-06-14
type: ctf-scenario
tags: [ctf, web, http-parameter-pollution, hpp, waf-bypass, parameter-parsing, proxy-mismatch]
confidence: high
---

# HTTP Parameter Pollution (HPP) to Bypass WAF — Web CTF Scenario

## 1. 개요 및 스토리
- **문제명**: Protected Admin Gate (보호된 관리자 관문)
- **난이도**: Medium
- **핵심 컨셉**: 다중 서버 환경에서 요청 매개변수를 처리하는 방식의 차이를 악용하는 **HTTP 매개변수 오염(HPP - HTTP Parameter Pollution)** 우회 문제입니다. 웹 서비스의 프론트엔드 방화벽(WAF) 또는 인증 대리 필터는 유입되는 쿼리스트링 중 특정 변수(예: `admin=true`)를 탐지하여 일반 사용자 접근을 차단합니다. 그러나 프론트엔드 필터와 백엔드 애플리케이션 프레임워크가 동일한 이름의 파라미터가 다수 존재할 때 해석하는 우선순위(첫 번째 매개변수 우선 채택 vs 마지막 매개변수 우선 채택)가 불일치하는 결함이 있습니다. 공격자는 중복 파라미터(`?admin=false&admin=true`)를 던져 방화벽 검증을 통과하고 백엔드에는 어드민 권한 상태로 도달합니다.

---

## 2. 문제 설계 및 구조 (Architecture)

### 2.1 구성 요소
- **Frontend Reverse Proxy (WAF / Authentication Filter in Python or Node.js)**:
  - 사용자의 요청을 수집하여 위험한 파라미터 키와 값이 포함되어 있는지 선제 검사.
  - 검사 규칙: `admin` 매개변수 값이 `true` 이면 403 Forbidden 반환.
  - 파라미터 파싱 로직: 중복 키가 유입되면 **첫 번째 값만** 추출하여 비교 검증을 거침.
- **Backend Application Server (PHP or ASP.NET)**:
  - 프록시 통과 후 실 비즈니스 로직 연산을 수행하는 서버.
  - 파라미터 파싱 로직: 중복 키가 유입되면 **마지막 값**을 읽어 적용하거나, 여러 값을 배열/문자열로 결합하여 사용함.
- **Flag 위치**:
  - `admin=true` 파라미터가 백엔드에 성공적으로 도달해 어드민 모드로 렌더링된 메인 화면.

### 2.2 취약점 지점
1. **HTTP Parameter Parsing Mismatch**:
   - HTTP 표준 스펙에는 동일한 파라미터가 다수 유입될 때의 처리 규칙이 명시되어 있지 않아 프레임워크별로 각각 다른 파싱 로직을 동작시킵니다.
     - Node.js (querystring): 배열로 반환 (`['false', 'true']`)
     - PHP / ASP.NET: 마지막 값만 덮어써서 사용 (`true`)
     - Python (Flask / Werkzeug): 첫 번째 값만 사용 (`false`)
   - 앞 단의 Nginx/WAF 필터(첫 번째 값으로 검사)와 뒷 단의 PHP 백엔드(마지막 값으로 적용) 간의 해석 괴리로 인해 보안 차단망이 무력화됩니다.

---

## 3. 공격 면 (Attack Surface)

| 엔드포인트 / 파라미터 | 메소드 | 인증 | 입력 값 | 반환 값 | 비고 |
|---------------------|--------|------|---------|---------|------|
| `/api/view?admin=false`| GET | 없음 | `admin` 권한 제어 변수 | 일반 유저 화면 또는 어드민 비밀 데이터 | WAF 바이패스 공격 경로 |

---

## 4. 상세 풀이 흐름 (Exploitation Flow)

### Step 1. 인가 필터 동작 진단
일반적인 어드민 파라미터 입력을 시도하여 보안 게이트웨이의 차단 동작을 진단합니다.
- *단순 어드민 시도*: `/api/view?admin=true`  
  -> *결과*: `403 Forbidden (Blocked by WAF)` 반환.

### Step 2. HPP 취약점 테스트 (중복 파라미터 주입)
방화벽 필터(Flask 기반)와 백엔드 서비스(PHP 기반)의 파라미터 처리 차이를 노려 두 개의 동일한 키 값을 덧붙입니다.
- **공격용 쿼리스트링 조합**: `?admin=false&admin=true`
- **시퀀스 해석 분석**:
  1. **WAF 필터 단계 (Python Flask 기반)**:
     `request.args.get('admin')`을 수행하면 첫 번째 매칭 값인 `'false'`를 반환받습니다. WAF 필터는 `admin`이 `true`가 아닌 `false`이므로 안전한 요청으로 판별하고 백엔드로 프록시 패스를 보냅니다.
  2. **백엔드 애플리케이션 단계 (PHP 기반)**:
     `$_GET['admin']` 값을 획득합니다. PHP의 엔진 기본 특성에 의해 뒤쪽에 기재되어 최종적으로 덮어쓴 값인 `'true'`를 얻게 됩니다.

### Step 3. 우회 요청 전송
- *공격 요청*:
  ```http
  GET /api/view?admin=false&admin=true HTTP/1.1
  Host: gate.challenge.local
  ```

### Step 4. flag 획득
서버는 WAF 차단을 완벽히 빗겨 가며 백엔드 단에서 `admin` 모드로 인가 판단을 통과시킵니다. 
결과 화면으로 어드민 전용 시스템 리포트 정보가 출력되며, 그 메타데이터에 포함되어 있던 최종 플래그(`FLAG{http_parameter_pollution_waf_mismatch_bypass}`)를 획득합니다.

---

## 5. 취약점 유발 프론트엔드 및 백엔드 코드 스니펫

### 5.1 WAF 프록시 코드 (Python Flask - 첫 번째 값 판별)
```python
# proxy_waf.py (Front-end WAF)
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

BACKEND_URL = "http://backend.internal/api/view"

@app.route("/api/view")
def waf_filter():
    # 취약점 지점: request.args.get() 은 중복 키 입력 시 첫 번째 값만 반환함
    # '?admin=false&admin=true' 가 유입되면 admin_val은 'false'가 됨
    admin_val = request.args.get("admin", "false")
    
    if admin_val == "true":
        return "Blocked by WAF! Admin access forbidden.", 403
        
    # 통과 시 백엔드로 전체 쿼리 전달
    backend_query = request.query_string.decode()
    resp = requests.get(f"{BACKEND_URL}?{backend_query}")
    return resp.text, resp.status_code

if __name__ == "__main__":
    app.run(port=8000)
```

### 5.2 백엔드 코드 (PHP - 마지막 값 판별)
```php
// backend/index.php (Back-end PHP)
<?php
// 취약점 지점: PHP는 동일 파라미터 수신 시 뒤쪽 값을 덮어써서 최종 채택함
// '?admin=false&admin=true' 가 유입되면 $_GET['admin']은 'true'가 됨
$admin_status = isset($_GET['admin']) ? $_GET['admin'] : 'false';

if ($admin_status === 'true') {
    echo json_encode([
        "status" => "success",
        "role" => "administrator",
        "flag" => "FLAG{http_parameter_pollution_waf_mismatch_bypass}"
    ]);
} else {
    echo json_encode([
        "status" => "success",
        "role" => "guest",
        "message" => "Welcome guest user."
    ]);
}
?>
```

---

## 6. 방어 및 완화 기법 (Mitigation)

1. **파라미터 파싱 로직의 일치화 (Homogeneous Architecture)**:
   - 프론트엔드 WAF 필터 계층과 백엔드 애플리케이션 프레임워크 계층의 파라미터 파서 구조를 동일하게 통일하거나, 모든 계층에서 안전한 글로벌 라이브러리를 사용해 해석하도록 셋업합니다.
2. **중복 파라미터 키 차단**:
   - 요청 수집 시 단일 쿼리 파라미터 명칭이 중복(배열 형태로 유입)되어 들어오는 경우, 이를 변조 공격 시도로 판단하여 게이트웨이 레벨에서 즉각 400 Bad Request 에러로 전체 요청을 무력화시킵니다.
3. **URL 재구성 전달**:
   - 프록시 통과 시 프론트엔드가 자체 정규화한 변수 값들을 명시적인 새 쿼리스트링 구조로 안전하게 재조립하여 백엔드로 안전 전달(파라미터 클렌징)되도록 조치합니다.
