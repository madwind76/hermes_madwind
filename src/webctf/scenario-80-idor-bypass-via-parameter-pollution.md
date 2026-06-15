---
title: IDOR Bypass via HTTP Parameter Pollution (HPP) — Web CTF Scenario
created: 2026-06-14
updated: 2026-06-14
type: ctf-scenario
tags: [ctf, web, idor, hpp, parameter-pollution, authorization-bypass, gateway-bypass]
confidence: high
---

# IDOR Bypass via HTTP Parameter Pollution (HPP) — Web CTF Scenario

## 1. 개요 및 스토리
- **문제명**: Gatekeeper Document Hub (게이트키퍼 문서 보관소)
- **난이도**: Medium-High
- **핵심 컨셉**: HTTP 파라미터 오염(HPP)의 프록시 검증부와 백엔드 해석기 간의 비대칭성을 활용해 비인가 자원에 접근하는 **IDOR 우회 결합형** 취약점 문제입니다. 대상 서비스 인프라는 외부 요청 유입 시 권한 제어 프록시(API Gateway)를 거쳐 백엔드로 전달됩니다. API 게이트웨이는 쿼리 파라미터 내의 `doc_id` 값을 파싱해, 해당 세션 사용자가 접근 가능한 파일 ID가 맞는지 엄격히 인가 검증(Authorization)을 처리합니다. 그러나 공격자가 동일 파라미터명을 중복 기입(`doc_id=123&doc_id=1`)하여 전송하면, 게이트웨이는 최초 앞쪽의 일반 권한 번호(`123`)만 검증해 안전하다고 판단하고 통과시키는 반면, 실제 백엔드 애플리케이션은 마지막 뒤쪽의 어드민 기밀 번호(`1`)를 읽어와 데이터를 처리함으로써 게이트웨이 보안 통제를 우회하며 IDOR을 달성합니다.

---

## 2. 문제 설계 및 구조 (Architecture)

### 2.1 구성 요소
- **API Gateway (Authentication Proxy)**:
  - 클라이언트의 GET `/api/document?doc_id=[ID]` 요청 수신 시, 사용자 세션 권한을 체크해 해당 `[ID]`에 접근할 권리가 있는지 인가 정책을 조회하고 필터링.
  - 파라미터 파싱 규칙: 동일 파라미터 중복 유입 시 **첫 번째** 값만 파싱 및 검증 수행.
- **Backend Document Service**:
  - 실제 데이터베이스에서 문서 정보를 조회하여 반환하는 실 서비스.
  - 파라미터 파싱 규칙: 동일 파라미터 중복 유입 시 **마지막(Last)** 값을 신뢰해 조회 수행.
- **Flag 위치**:
  - `doc_id=1` (어드민 전용 시스템 기밀 설정 문서)의 본문 데이터 내용 중 플래그가 존재합니다.

### 2.2 취약점 지점
1. **Parameter Parsing Mismatch between Gateway and Backend (HPP 비대칭)**:
   - 클라이언트의 `doc_id=123&doc_id=1` 요청에 대해:
     - **API Gateway**: 첫 번째 값인 `123`만 검사. 일반 사용자가 자신의 소유인 `123`번 문서에 접근하려는 것으로 판단해 인가 처리 완료 후 백엔드로 패킷 인계.
     - **Backend Service**: 최종 조회 변수로 마지막 값인 `1`을 선택해 DB에서 어드민 기밀 문서를 로드해 반환.
2. **IDOR via Authorization Bypass**:
   - 백엔드는 게이트웨이가 이미 완벽히 인가 처리를 완료했다고 맹신하여 자체적인 권한 체크를 이중으로 수행하지 않는 설계 맹점이 존재합니다.

---

## 3. 공격 면 (Attack Surface)

| 엔드포인트 | 메소드 | 인증 | 파라미터 조작 포맷 | 게이트웨이 파싱 | 백엔드 파싱 | 목표 |
|------------|--------|------|--------------------|-----------------|-------------|------|
| `/api/document` | GET | 일반 사용자 세션 필요 | `doc_id=123&doc_id=1` | 첫 번째 값 (`123`) 검사 통과 | 마지막 값 (`1`) 조회 | `doc_id=1` (어드민 문서) IDOR 유출 |

---

## 4. 상세 풀이 흐름 (Exploitation Flow)

### Step 1. 일반 IDOR 및 권한 장벽 식별
1. 사용자는 로그인 후 자신의 문서인 `123`번 문서 조회를 시도합니다.
   `GET /api/document?doc_id=123` -> 정상 200 OK
2. 타겟이 되는 다른 자산 번호인 `1`번 문서 조회를 시도합니다.
   `GET /api/document?doc_id=1` -> 게이트웨이 단에서 `"Access Denied: You do not own this document"` 403 에러 응답을 회신합니다.
3. 이를 통해 권한 제어 필터가 프록시 또는 게이트웨이 단에서 작동하고 있음을 파악합니다.

### Step 2. HPP 파라미터 비대칭성 테스트
게이트웨이와 백엔드 간에 파라미터를 복수 기입했을 때 파싱 동작의 순서 격차가 존재하는지 분석합니다.
- **테스트 케이스**:
  `/api/document?doc_id=123&doc_id=999`
  - 만약 403 에러가 나지 않고 통과하되, 화면에 "999번 문서를 찾을 수 없습니다" 라는 백엔드 에러가 출력된다면:
    1. 게이트웨이는 앞의 `123` (성공 계정 권한)을 보고 통과시켰습니다.
    2. 백엔드는 뒤의 `999`를 기반으로 비즈니스 쿼리를 날렸습니다.
    즉, HPP 우회 각도가 정확히 성립함을 의미합니다.

### Step 3. 우회 쿼리 발송
1. 공격자는 자신의 소유인 유효 ID `123`을 앞에 기입하고, 탈취하고자 하는 어드민 ID `1`을 뒤에 앰퍼샌드로 이어 붙여 요청을 보냅니다.
   - **공격 요청**:
     ```http
     GET /api/document?doc_id=123&doc_id=1 HTTP/1.1
     Host: document-hub.challenge.local
     Cookie: session=my_user_session
     Connection: close
     ```

### Step 4. flag 획득
1. API 게이트웨이는 앞의 `doc_id=123`을 파싱하여 세션 유저의 권한 일치 여부를 파악하고, 검증에 통과했으므로 백엔드로 요청 패킷을 인계합니다.
2. 백엔드는 중복 파라미터 중 뒤의 값인 `doc_id=1`을 추출하여 데이터베이스 조회를 가동해 관리자 중요 문서를 반환합니다.
3. 리턴된 HTML 또는 JSON 데이터 내의 문서 내용 영역에서 플래그(`FLAG{idor_bypass_via_http_parameter_pollution_discrepancy}`)를 획득합니다.

---

## 5. 취약점 유발 백엔드 및 게이트웨이 코드 스니펫

### API Gateway (취약한 Node.js Proxy 예시)
```javascript
// gateway.js (API 게이트웨이 권한 통제 필터 모킹)
const express = require('express');
const axios = require('axios');
const url = require('url');
const app = express();

app.use((req, res, next) => {
    // 취약점 지점 1: URL 파싱 시 중복 파라미터 중 첫 번째 값만 읽어내 검사
    // 예: doc_id=123&doc_id=1 인 경우, docId는 '123' 만 할당됨
    const urlParts = url.parse(req.url, true);
    let docId = urlParts.query.doc_id;

    if (Array.isArray(docId)) {
        docId = docId[0]; // 중복 배열 중 첫 번째 요소만 인가 필터에 사용
    }

    const session = req.headers.session; // 세션 데이터 취득 가정

    // 인가 검증 로직 실행 (사용자가 docId 문서의 소유자가 맞는지 확인)
    if (docId === '1' && session !== "admin_session") {
        return res.status(403).json({ error: "Access Denied: Admin permission required" });
    }
    
    // 검증 통과 시 백엔드 서비스로 요청 포워딩
    next();
});

// 백엔드로 포워딩
app.get('/*', (req, res) => {
    // 원본 URL 그대로 백엔드 서버에 전달
    axios.get(`http://backend_service:8080${req.url}`, { headers: req.headers })
        .then(response => res.status(response.status).send(response.data))
        .catch(err => res.status(500).send(err.message));
});

app.listen(80);
```

### Backend Document Service (Python Flask)
```python
# backend.py (취약한 백엔드 문서 조회 서비스 예시)
from flask import Flask, request, jsonify

app = Flask(__name__)

# 가상 DB
documents = {
    "1": "Secret Admin System configurations: FLAG{idor_bypass_via_http_parameter_pollution_discrepancy}",
    "123": "User Alice personal profile data..."
}

@app.route('/api/document', methods=['GET'])
def get_document():
    # 취약점 지점 2: Flask의 request.args.get() 함수는 동일한 키가 여러 개 중복해서 들어올 때 
    # 기본적으로 맨 마지막(Last) 값을 선택하여 리턴하는 구조적 사양이 적용되어 있음
    # 예: doc_id=123&doc_id=1 -> doc_id는 '1'이 매핑됨
    doc_id = request.args.get('doc_id')

    if not doc_id:
        return jsonify({"error": "doc_id is missing"}), 400

    # 게이트웨이를 통과했으므로 이 단계에서는 별도 권한 체크 없이 문서를 DB에서 가져와 즉각 반환
    doc_content = documents.get(doc_id)
    if doc_content:
        return jsonify({"doc_id": doc_id, "content": doc_content})
    return jsonify({"error": "Document not found"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
```

---

## 6. 방어 및 완화 기법 (Mitigation)

1. **파라미터 파싱 라이브러리 일관성 확보**:
   - 외부 API 게이트웨이 단과 백엔드 서비스 단의 파라미터 처리 모듈이 중복 파라미터 유입 시 채택하는 정책(First, Last, Array, 혹은 400 Bad Request 에러 반려)을 확실하게 1대1로 일치시킵니다.
2. **중복 파라미터 입력 기각 (Disallow HPP)**:
   - 게이트웨이 또는 WAF 레이어에서 단일 요청 내에 동일한 명칭의 쿼리/바디 매개변수 키가 2회 이상 감지되는 경우 파라미터 오염 시도로 규정하여 HTTP `400 Bad Request` 에러로 통신을 사전에 차단합니다.
3. **백엔드 이중 권한 검증 (Defense in Depth)**:
   - 게이트웨이의 선제 검증 통과 여부와 무관하게, 중요 기밀 정보를 데이터베이스에서 최종 로드해 출력하는 백엔드 비즈니스 로직 단에서도 반드시 현재 세션 계정 소유권이 해당 데이터 ID와 매칭되는지 이중 검증(`Secondary Auth Check`)을 구현합니다.
    ```python
    # 백엔드 안전 예시
    if not has_permission(current_user, doc_id):
        return jsonify({"error": "Forbidden"}), 403
    ```
