---
title: DoS — 보안 용어 해설
created: 2026-06-13
updated: 2026-06-13
type: concept
tags: [security, glossary, dos, denial-of-service, syn-flood, slowloris, ping-of-death]
sources: [https://ko.wikipedia.org/wiki/서비스_거부_공격, https://ko.wikipedia.org/wiki/분산_서비스_거부_공격, https://ko.wikipedia.org/wiki/SYN_플러드, https://ko.wikipedia.org/wiki/침입_차단_시스템]
confidence: high
---

# DoS (Denial of Service) — 서비스 거부 공격

## Step 1: 단어 직역 및 쉬운 비유

### 1. 약자 풀이
**DoS** = **D**enial **o**f **S**ervice

| 약자 | 영어 단어 | 직역 | 의미 |
|------|-----------|------|------|
| **D** | **Denial** | 거부, 부인 | 못하게 막음 |
| **o** | **of** | ~의 | 연결/소유 |
| **S** | **Service** | 서비스 | 제공되는 기능 |

### 2. 의미 조합
> **단일 출처(한 대의 시스템/IP)에서 대상 시스템에 과도한 트래픽 또는 요청을 보내 정상 사용자의 서비스 이용을 방해(거부)하는 공격**

### 3. 강력한 비유: "한 대의 트럭이 레스토랑 정문 앞을 막는 상황"

| 비유 요소 | 대응 개념 |
|-----------|-----------|
| **레스토랑** | **웹 서버 / 애플리케이션** |
| **손님들** | **정상 사용자 트래픽** |
| **트럭 한 대가 정문 앞을 막음** | **DoS 공격 — 단일 IP/소스** |
| **트럭이 쉴 새 없이 경적을 울림** | **요청 폭주 → CPU/메모리/대역폭 고갈** |
| **트럭 하나가 경비원 10명 붙잡음** | **SYN Flood — 연결 테이블 고갈** |
| **트럭이 경비원에게 천천히 말을 검** | **Slowloris — HTTP 연결 풀 고갈** |
| **경비원이 트럭 번호판 확인하고 차단** | **DoS 방어 — 단일 IP 차단, Rate Limiting** |

**핵심 포인트**: DoS는 **트럭 한 대**라서 **경비원(방화벽)이 번호판(IP)만 확인하고 차단하면 끝**입니다. 이게 **DDoS(수백 대 트럭)** 와의 결정적 차이입니다.

---

## Step 2: 개념 시각화

![DoS 비유 시각화: 단일 공격자(트럭 1대), 대상 서버(레스토랑), 정상 사용자 차단, 리소스 고갈, SYN Flood, Slowloris, Ping of Death - 한글 레이블 포함](https://v3b.fal.media/files/b/0a9e1c6c/S2vzcGYoulpx9tpEhYLAQ_GHbVKmTu.png)

> ⚠️ **참고**: 이미지 생성 도구가 PNG 형식으로 반환했습니다. 스킬 요구사항(.jpg/.jpeg)은 현재 도구 제약상 PNG로 대체됩니다.

---

## Step 3: 전문 용어 설명 (Wikipedia 기반)

### 서비스 거부 공격 (Denial of Service, DoS)

**정의**: 단일 시스템/IP에서 대상 서버·네트워크·서비스에 비정상적으로 과도한 트래픽이나 요청을 전송하여 정상적인 서비스 제공을 불가능하게 만드는 공격이다. 방화벽에서 공격 IP를 차단하는 것으로 대부분 방어 가능하며, 이 점이 수많은 분산 IP에서 발생하는 DDoS와의 핵심 차이이다.

### 주요 DoS 공격 유형

| 공격 유형 | 설명 | 방어 방법 |
|-----------|------|-----------|
| **SYN Flood** | TCP SYN 패킷만 대량 전송 → 연결 테이블(backlog) 고갈 | SYN Cookie, SYN Proxy, 타임아웃 단축 |
| **Ping of Death** | >65535 bytes ICMP 패킷 → 버퍼 오버플로우, 충돌 | 최신 OS 패치됨(1996), ping 차단 |
| **Slowloris** | HTTP 헤더를 수 초 간격 전송 → 연결 풀 고갈 | Keep-Alive 타임아웃, 리버스 프록시 |
| **UDP Flood** | 랜덤 포트로 대량 UDP → ICMP 응답 리소스 소모 | UDP Rate Limiting, 불필요 서비스 비활성화 |
| **ICMP Flood** | 대량 Ping → CPU 응답 생성 과부하 | ICMP Rate Limiting, 방화벽 차단 |
| **HTTP Flood** | 대량 HTTP GET/POST → CPU/메모리 고갈 | Rate Limiting, WAF, CAPTCHA |

### DoS vs DDoS 비교

| 항목 | DoS | DDoS |
|------|-----|------|
| **공격 출처** | 단일 IP | 수만~수십만 개 분산 IP |
| **방어 용이성** | 쉬움 — IP 차단 → 끝 | 어려움 — IP 차단만으로 불가 |
| **공격 규모** | 수백 Mbps ~ 수 Gbps | 수백 Gbps ~ 수 Tbps |
| **필요 자원** | PC 1대로 가능 | 봇넷 필요 |
| **현대적 의미** | 실효성 낮음 (자동 방어) | 실질적 위협 |

> **참고**: 2020년대 들어 단순 DoS는 대부분의 클라우드/CDN에서 자동 차단됩니다. 현대 사이버 공격에서 실질적 위협은 DDoS입니다.

### DoS 방어 기본 전략

| 방법 | 설명 |
|------|------|
| **방화벽 ACL** | 공격 IP 차단 — 단일 IP DoS에 100% 효과 |
| **Rate Limiting** | IP당 초당 요청 수 제한 |
| **SYN Cookie** | TCP 연결 테이블 보호 (리눅스 기본 활성화) |
| **IDS/IPS** | 시그니처 기반 탐지 + 차단 |
| **WAF** | L7 HTTP Flood 차단 |

---

### 출처
- 한국어 위키백과: ["서비스 거부 공격"](https://ko.wikipedia.org/wiki/서비스_거부_공격) — DoS 정의 및 유형
- 한국어 위키백과: ["분산 서비스 거부 공격"](https://ko.wikipedia.org/wiki/분산_서비스_거부_공격) — DoS와 대비되는 DDoS 상세
- 한국어 위키백과: ["SYN 플러드"](https://ko.wikipedia.org/wiki/SYN_플러드) — 대표적 DoS 기법
- 한국어 위키백과: ["침입 차단 시스템"](https://ko.wikipedia.org/wiki/침입_차단_시스템) — DoS 방어 장비

---

## 관련 위키 링크
- [[ddos]] — DDoS (분산 서비스 거부 공격) — DoS의 고도화된 형태, 수십만 IP 동시 공격
- [[ips]] — IPS (침입 방지 시스템) — DoS 트래픽 인라인 차단
- [[ids]] — IDS (침입 탐지 시스템) — DoS 패턴 시그니처 탐지
- [[cia]] — CIA Triad (가용성) — DoS가 직접적으로 파괴하는 보안 목표