---
title: DNS Rebinding & SSRF — Web CTF Scenario
created: 2026-06-14
updated: 2026-06-14
type: ctf-scenario
tags: [ctf, web, dns-rebinding, ssrf, toctou, security-bypass]
confidence: high
---

# DNS Rebinding & SSRF — Web CTF Scenario

## 1. 개요 및 스토리
- **문제명**: Web Watchdog (웹 왓치독 서비스)
- **난이도**: High
- **핵심 컨셉**: 웹 서버 측의 **사설 IP 대역 필터링**을 우회하는 **DNS 리바인딩(DNS Rebinding)** 공격을 결합한 SSRF(Server-Side Request Forgery) 문제입니다. 대상 웹 서버는 사용자가 제공한 도메인의 상태를 주기적으로 체크하여 알려주는 Uptime 모니터링 툴입니다. 보안 필터는 도메인을 분석해 IP 주소로 해석(Resolve)한 뒤 사설망(`127.0.0.1`, `10.0.0.0/8` 등)에 속하는지 1차로 확인합니다. 하지만 확인 시점과 실제 데이터 요청 시점의 차이(TOCTOU)와 브라우저/서버의 DNS 캐싱 동작 미흡으로 인해 보안 로직을 통과한 뒤 내부 서비스의 플래그 정보를 받아올 수 있습니다.

---

## 2. 문제 설계 및 구조 (Architecture)

### 2.1 구성 요소
- **Frontend / Uptime Console**: 서버 주소(도메인명)를 입력하면 해당 웹사이트의 HTTP 응답 상태 코드(예: 200 OK)와 헤더 정보를 요약하여 출력해 줍니다.
- **Backend Service (Python/FastAPI)**:
  - 도메인을 분석하고 연결하기 위한 DNS Resolver 모듈 포함.
  - 사설 대역 필터링 및 실제 웹 요청 전송부.
- **가상 내부 서비스 (Internal Admin Service)**: 
  - `http://127.0.0.1:9000/admin/secrets` (서버 로컬에서만 접근 가능한 관리 포트, 외부에선 차단됨)
- **Flag 위치**: 
  - 로컬 관리 서비스(`/admin/secrets`)의 JSON 응답 데이터.

### 2.2 취약점 지점
1. **TOCTOU (Time-of-Check to Time-of-Use) & DNS Rebinding**:
   - 백엔드는 도메인을 IP로 받아와 안전한 대역인지 체크하는 단계(Check)와 실제 해당 주소로 HTTP 요청을 전송하는 단계(Use)에서 **두 번 연속으로 DNS Query**를 발생시킬 수 있습니다.
   - 공격자는 짧은 TTL(예: 0초 또는 1초)을 적용한 악의적인 네임서버(DNS Server)를 구성하여 다음을 구현합니다.
     - 1차 Query: 정상적인 공인 IP (예: `8.8.8.8`)를 반환해 검증 통과.
     - 2차 Query: 로컬 사설 IP (`127.0.0.1`)를 반환해 내부 서버 통신 성립.

---

## 3. 공격 면 (Attack Surface)

| 엔드포인트 | 메소드 | 인증 | 입력 값 | 반환 값 | 비고 |
|------------|--------|------|---------|---------|------|
| `/uptime` | GET | 없음 | 없음 | 모니터링 대시보드 | |
| `/api/check`| POST | 없음 | `{"target": "attacker.dns-rebinding.com"}` | 대상 서버의 HTTP 응답 헤더 및 바디 일부 | SSRF 및 DNS 리바인딩 타겟 엔드포인트 |

---

## 4. 상세 풀이 흐름 (Exploitation Flow)

### Step 1. 타겟 분석 및 보호 필터 확인
공격자는 웹 폼에 `localhost`, `127.0.0.1` 등을 입력해 모니터링을 요청해 봅니다.
- *결과*: "Error: Private IP ranges are not allowed!" 응답 확인.
- *동작 분석*: 도메인을 입력하더라도 자체 DNS Lookup을 수행하여 최종 도달 IP가 사설 주소인 경우 요청을 사전에 차단함을 확인합니다.

### Step 2. DNS 리바인딩 공격 서버 설정
공격자는 DNS 리바인딩 서비스를 이용하거나 자체 DNS 서버를 구축합니다. (예: public DNS rebinding tool인 `singularity` 또는 `rbndr.us` 사용)
- **도메인 설정 규칙**:
  - 첫 번째 요청 응답 IP: `93.184.216.34` (example.com - 안전한 공인 IP)
  - 두 번째 요청 응답 IP: `127.0.0.1` (로컬 사설 IP)
  - TTL (Time to Live): `0`초로 설정하여 서버가 DNS 기록을 절대 캐싱하지 않고 매번 조회하게 만듭니다.

### Step 3. 리바인딩 페이로드 전송
공격자는 API 엔드포인트에 구성한 도메인으로 헬스체크를 보냅니다.
- *요청*:
  ```http
  POST /api/check HTTP/1.1
  Host: watchdog.challenge.local
  Content-Type: application/json

  {"target": "a.93.184.216.34.127.0.0.1.rbndr.us"}
  ```

### Step 4. 백엔드 시퀀스 동작 및 플래그 획득
1. **IP 검증 단계 (Check)**: 
   서버가 도메인을 조회하여 `93.184.216.34`를 확인하고, 공인 IP이므로 검증 필터를 통과시킵니다.
2. **HTTP 요청 단계 (Use)**:
   서버는 실제 웹 요청을 보내기 위해 도메인으로 다시 한번 연결을 수립합니다. 이때 TTL이 0이므로 강제로 다시 DNS Query를 발생시키고, 이번에는 `127.0.0.1` 주소를 받게 됩니다.
3. **내부망 요청 발생**:
   서버는 안전하다고 판단했던 도메인 호스트로 HTTP 요청을 보내지만, 실제로는 `http://127.0.0.1:9000/admin/secrets`로 연결이 흘러갑니다.
4. **플래그 노출**:
   반환된 로컬 관리자 페이지의 응답 바디가 공격자 브라우저로 렌더링되며 플래그가 탈취됩니다.

---

## 5. 취약점 유발 백엔드 코드 스니펫 (Python FastAPI)

```python
# main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import socket
import requests

app = FastAPI()

class CheckRequest(BaseModel):
    target: str

def is_private_ip(ip: str) -> bool:
    # 사설망 IP 대역 검증 함수
    parts = list(map(int, ip.split('.')))
    if parts[0] == 127: return True
    if parts[0] == 10: return True
    if parts[0] == 172 and (16 <= parts[1] <= 31): return True
    if parts[0] == 192 and parts[1] == 168: return True
    return False

@app.post("/api/check")
async def check_target(req: CheckRequest):
    domain = req.target
    
    try:
        # 취약점 1차 지점: 호스트명을 IP 주소로 검증 (Check)
        resolved_ip = socket.gethostbyname(domain)
        if is_private_ip(resolved_ip):
            raise HTTPException(status_code=400, detail="Private IP is blocked!")
            
        # 취약점 2차 지점 (TOCTOU): 
        # requests.get 내에서 도메인을 사용하여 실제 웹 요청을 보낼 때, 
        # 내부적으로 DNS Query를 한 번 더 발생시킴 (Use)
        # 이때 DNS 리바인딩에 의해 127.0.0.1로 바뀜!
        url = f"http://{domain}:9000/admin/secrets"
        response = requests.get(url, timeout=3)
        return {"status": "success", "data": response.text}
        
    except socket.gaierror:
        raise HTTPException(status_code=400, detail="Could not resolve domain")
    except Exception as e:
        return {"status": "failed", "reason": str(e)}
```

---

## 6. 방어 및 완화 기법 (Mitigation)

1. **IP 고정 및 1회성 Lookup (Resolve-Once Policy)**:
   - 도메인 검증 단계에서 획득한 IP 주소를 사용하여 실제 웹 요청을 전송하도록 코드를 수정합니다. 도메인명 대신 추출된 IP를 목적지로 하고, HTTP `Host` 헤더에 원래 도메인명을 기입해 요청해야 합니다.
   - **수정 예시**:
     ```python
     resolved_ip = socket.gethostbyname(domain)
     if is_private_ip(resolved_ip): raise Exception(...)
     # 도메인 주소가 아닌 사전에 검증 완료된 IP 주소로만 직접 요청 발생시킴
     response = requests.get(f"http://{resolved_ip}:9000/admin/secrets", headers={"Host": domain})
     ```
2. **독립된 DNS 캐싱 및 프록시 구성**:
   - 내부 DNS 해석기를 설정하여 TTL이 지나치게 짧은 레코드에 대해 최소 캐시 유지 기간을 강제하도록 설정합니다.
3. **내부망 인프라 격리**:
   - 애플리케이션 서버와 내부 관리 및 민감 서비스 서버 간에 네트워크 방화벽(ACL) 설정을 적용하여 원천적으로 다이렉트 통신을 제어합니다.
