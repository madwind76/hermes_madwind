---
title: Business Logic Coupon Race Condition — Web CTF Scenario
created: 2026-06-14
updated: 2026-06-14
type: ctf-scenario
tags: [ctf, web, race-condition, business-logic, concurrency, transaction-lock, coupon-reuse]
confidence: high
---

# Business Logic Coupon Race Condition — Web CTF Scenario

## 1. 개요 및 스토리
- **문제명**: Promotion Gift Center (프로모션 기프트 센터)
- **난이도**: Medium-High
- **핵심 컨셉**: 웹 애플리케이션의 비동기 동시 요청 처리 흐름과 데이터베이스 상태 변경 시점의 시간 차(TOCTOU)를 공략하는 **비즈니스 로직 연계 레이스 컨디션(Concurrency Race Condition)** 취약점 문제입니다. 대상 애플리케이션은 사용자가 1회성 프로모션 쿠폰을 등록하면 포인트를 적립해 주는 기능을 제공합니다. 그러나 백엔드의 쿠폰 검증 및 적용 로직 구현 시, 동일한 쿠폰이 여러 요청에서 동시에 인입될 때 데이터의 무결성을 보장하는 **데이터베이스 락(Database Row/Table Lock)** 장치를 적용하지 않았습니다. 공격자는 다중 스레드 도구(예: Turbo Intruder)를 사용해 밀리초 단위로 동일한 쿠폰 코드를 다량 동시 전송하여, 최초 조회 조건 만족 단계와 사용 처리 갱신 단계 사이의 틈새에서 하나의 쿠폰으로 다중 포인트 누적 적립을 성사시킵니다.

---

## 2. 문제 설계 및 구조 (Architecture)

### 2.1 구성 요소
- **Coupon Redemption API (`/api/redemption/coupon`)**:
  - 쿠폰 코드(`coupon_code`)를 입력받아 포인트 적립 처리를 수행하는 API.
- **Flag 위치**:
  - 포인트 상점(`/api/shop/buy`)에서 누적 포인트를 소모하여 비싼 가격의 플래그 상품(예: `Secret Flag`, 가격: 10,000 포인트)을 구입했을 때 반환되는 결과값.
  - 일반 쿠폰 하나당 지급 포인트는 100 포인트이며, 정상적인 사용은 단 1회로 한정되므로 레이스 컨디션 복제 없이는 목표 포인트에 도달할 수 없습니다.

### 2.2 취약점 지점
1. **Lack of Database Concurrency Locking**:
   - 백엔드는 쿠폰 등록 시 다음과 같은 단계로 처리합니다:
     1단계: 쿠폰이 사용되었는지 확인 (`SELECT used FROM coupons WHERE code = ?`)
     2단계: 사용 안 됨 상태면, 사용자 포인트를 증가시킴 (`UPDATE users SET points = points + 100 WHERE id = ?`)
     3단계: 쿠폰을 사용 완료 상태로 업데이트 (`UPDATE coupons SET used = true WHERE code = ?`)
   - **문제점**: 1단계와 3단계 사이에 락이 전혀 결여되어 있어, 동시에 유입된 여러 스레드가 모두 "used = false" 상태를 조회하는 데 성공하고 각 스레드마다 포인트를 중복 적립한 뒤 뒤늦게 used 상태를 true로 갱신하게 됩니다.

---

## 3. 공격 면 (Attack Surface)

| 엔드포인트 | 메소드 | 인증 | 파라미터 | 데이터 포맷 | 핵심 검증 대상 |
|------------|--------|------|----------|-------------|----------------|
| `/api/redemption/coupon` | POST | 세션 필요 | `coupon_code` | JSON | 단일 쿠폰 코드의 동시 다발 처리 허점 |

---

## 4. 상세 풀이 흐름 (Exploitation Flow)

### Step 1. 쿠폰 등록 프로세스 진단
1. 사용자는 회원가입 후 기본 발급되는 1회용 웰컴 쿠폰 번호(`WELCOME-2026`)를 확인합니다.
2. 쿠폰 등록 API `/api/redemption/coupon`에 요청을 전송하여 정상 적용(100 포인트 적립)되고, 다시 전송 시 "이미 사용된 쿠폰입니다" 에러가 반환되는 로직 흐름을 관찰합니다.

### Step 2. 동시성 레이스 컨디션 테스트 설계
1. 서버가 멀티스레드 혹은 비동기 워커 구조(Node.js, Go, Java 등)로 동작함을 인지합니다.
2. 동일 쿠폰 코드를 아주 조밀한 시간 차로 다중 전송하는 자동화 스크립트(Python `threading`/`asyncio` 또는 Burp Suite `Turbo Intruder`)를 작성합니다.
- **Turbo Intruder 공격 스크립트 예시**:
  ```python
  def queueRequests(target, wordlists):
      engine = RequestEngine(endpoint=target.endpoint, concurrentConnections=30)
      # 30개의 연결 세션을 동시에 수립하고 준비 상태로 둠
      req = '''POST /api/redemption/coupon HTTP/1.1
  Host: target.local
  Content-Type: application/json
  Cookie: session=my_session_token_123
  
  {"coupon_code": "WELCOME-2026"}'''
      
      # 게이트 방식을 이용해 30개 요청을 거의 동일 밀리초 내에 해제 발송
      for i in range(30):
          engine.queue(req, gate='race1')
      engine.openGate('race1')
  ```

### Step 3. 레이스 컨디션 공격 감행
1. 동시 다발 요청을 타겟 엔드포인트로 일제히 전송합니다.
2. 각 스레드의 응답 결과를 모니터링합니다.
   - **성공적인 레이스 결과**:
     - 30개의 요청 중 15개 이상의 요청이 동시에 `200 OK (포인트 적립 성공)` 응답을 회신하고, 일부 늦은 요청들만 `400 Bad Request (이미 사용됨)` 응답을 수신하는 양상을 보입니다.
3. 내 정보 창에서 포인트 잔액을 확인하여, 원래 100 포인트만 지급되어야 할 쿠폰으로 1,500 포인트 이상이 비정상 중복 적립되었는지 검증합니다.

### Step 4. 상점 구매 및 flag 획득
1. 이 레이스 컨디션을 몇 회 반복 실행하여(새 쿠폰을 구하거나 세션을 새로 파서 적립) 최종 상품 가격인 10,000 포인트 조건을 돌파합니다.
2. 포인트 상점 API `/api/shop/buy`에 플래그 상품 구매 요청을 보냅니다.
3. 포인트 차감 처리 완료와 함께 반환되는 구매 완료 영수증 내역에서 플래그(`FLAG{concurrency_race_condition_database_transaction_unlock}`)를 획득합니다.

---

## 5. 취약점 유발 백엔드 코드 스니펫 (Python Flask + PostgreSQL 개념)

```python
# app.py (취약한 쿠폰 적립 로직 예시)
from flask import Flask, request, jsonify, session
import psycopg2
from db_pool import get_db_connection # 모킹 풀 커넥션 함수

app = Flask(__name__)
app.secret_key = "super_secret_session_key"

@app.route('/api/redemption/coupon', methods=['POST'])
def redeem_coupon():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401
        
    data = request.json
    code = data.get('coupon_code', '')

    conn = get_db_connection()
    cur = conn.cursor()

    # 취약점 지점 1: SELECT 시점에 행 잠금(FOR UPDATE 등)이 설정되어 있지 않음
    # 여러 스레드가 동시에 이 SELECT 쿼리를 조회하면, 모두 used가 false인 상태를 획득함
    cur.execute("SELECT id, used, amount FROM coupons WHERE code = %s", (code,))
    coupon = cur.fetchone()

    if not coupon:
        cur.close()
        conn.close()
        return jsonify({"error": "Invalid coupon code"}), 400

    coupon_id, used, amount = coupon

    if used:
        cur.close()
        conn.close()
        return jsonify({"error": "This coupon has already been used"}), 400

    # 취약점 지점 2: 사용자의 포인트를 즉각 차감/적립함
    cur.execute("UPDATE users SET points = points + %s WHERE id = %s", (amount, user_id))

    # 취약점 지점 3: 뒤늦게 쿠폰을 사용됨 상태로 갱신함
    # 1단계 SELECT 조회와 이 UPDATE 실행 사이의 지연 시간 동안 레이스 컨디션 성립
    cur.execute("UPDATE coupons SET used = true WHERE id = %s", (coupon_id,))

    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"status": "success", "message": f"{amount} points credited!"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
```

---

## 6. 방어 및 완화 기법 (Mitigation)

1. **데이터베이스 비관적 락 도입 (Pessimistic Locking / SELECT FOR UPDATE)**:
   - 중복 점검 방지를 위한 최초 데이터 조회 단계에서 `SELECT ... FOR UPDATE` 구문을 활용해 해당 쿠폰 레코드 행(Row)을 강력하게 잠금 설정합니다.
   - 트랜잭션이 완료되어 `COMMIT`되기 전까지는 다른 동시 요청 스레드들이 동일 행을 SELECT조차 할 수 없도록 대기 상태로 유도하여 순차 처리를 강제합니다.
     ```sql
     -- 안전한 SQL 조회 락 기법
     SELECT id, used, amount FROM coupons WHERE code = ? FOR UPDATE;
     ```
2. **복합 고유 인덱스 및 단일 SQL 업데이트 활용**:
   - 쿠폰 사용 이력을 사용자 매핑 테이블(예: `user_coupons`)에 저장하고, `(user_id, coupon_id)` 복합 키에 `UNIQUE` 제약 조건을 걸어 동시 삽입 발생 시 DB 수준에서 유니크 제약 조건 위반 예외로 튕겨내도록 설계합니다.
3. **낙관적 락 (Optimistic Locking) 활용**:
   - 데이터 테이블에 버전 번호(`version`) 칼럼을 두어, 데이터를 업데이트할 때 이전에 읽어온 버전 번호와 일치하는 경우에만 업데이트에 성공하도록 통제합니다.
     ```sql
     UPDATE coupons SET used = true, version = version + 1 WHERE id = ? AND version = ?;
     ```
