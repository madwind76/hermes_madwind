---
title: ARP — Address Resolution Protocol
created: 2026-06-12
updated: 2026-06-12
type: concept
tags: [security, glossary, arp, network, protocol, layer2, spoofing, mitm]
sources: [https://ko.wikipedia.org/wiki/ARP, https://ko.wikipedia.org/wiki/주소_분석_프로토콜]
confidence: high
---

# ARP (Address Resolution Protocol) — 보안 용어 해설

## Step 1: 단어 직역 및 쉬운 비유

### 1. 약자 풀이

**ARP** = **A**ddress **R**esolution **P**rotocol

| 약자 | 원래 단어 | 직역 | 의미 |
|------|-----------|------|------|
| **A** | **Address** | 주소 | 네트워크 상의 위치 식별자 |
| **R** | **Resolution** | 해결, 변환 | 한 형태의 주소를 다른 형태로 변환 |
| **P** | **Protocol** | 프로토콜, 규약 | 통신을 위한 약속된 규칙 |

### 2. 의미 조합

> **"IP 주소(논리 주소)를 MAC 주소(물리 주소)로 변환해 주는 네트워크 프로토콜"**

### 3. 강력한 비유: "아파트 택배 배송 시스템"

```
┌────────────────────────────────────────────────────────────┐
│  상황: 택배 기사(데이터 패킷)가 103동 204호(IP 주소)로    │
│  배송해야 하는데, 실제 현관문 비밀번호(MAC 주소)를 모름   │
└────────────────────────────────────────────────────────────┘

1️⃣  **택배 기사(송신자)**: "103동 204호 사시는 분~ 현관문 비번 좀 알려주세요!"
    → 브로드캐스트: "누구 IP 192.168.1.50이에요? 본인 MAC 주소 좀 알려줘!" (ARP Request)

2️⃣  **경비실(스위치/허브)**: 전체 세대(같은 네트워크 대역)에 방송
    → "103동 204호 찾습니다~ 본인 나오세요!"

3️⃣  **103동 204호 거주자(수신자)**: "내 맞아요! 제 현관문 비번은 **1234(MAC: aa:bb:cc:dd:ee:ff)** 예요."
    → 유니캐스트 응답: "내 IP 192.168.1.50이고, MAC은 aa:bb:cc:dd:ee:ff입니다!" (ARP Reply)

4️⃣  **택배 기사**: 비번( MAC 주소) 알았으니 바로 배송 완료!
    → ARP 캐시에 저장: "192.168.1.50 = aa:bb:cc:dd:ee:ff" (다음엔 바로 찾아감)

💡 **핵심 포인트**: IP는 **"몇 동 몇 호"** (논리적 주소), MAC은 **"현관문 비밀번호/열쇠"** (물리적 주소). ARP는 둘 사이를 **자동으로 중개**해 주는 **경비실 안내 방송**입니다.
```

---

## Step 2: 개념 시각화

![ARP 비유 시각화: 아파트 택배 배송 시스템으로 설명하는 ARP 동작 원리 — 택배 기사(송신자), 아파트 건물(네트워크), 103동 204호(목표 IP), 경비실(스위치/브로드캐스트), 거주자(수신자), ARP 캐시 테이블 - 한글 레이블 포함](https://v3b.fal.media/files/b/0a9dfb8f/CiJ9ruRqp0N8j9Frx4IVu_x94sgbin.png)

**이미지 설명**:
- **택배 기사(송신자)** — 데이터 패킷을 전달하려는 호스트
- **아파트 건물(네트워크)** — 같은 브로드캐스트 도메인 (예: 192.168.1.0/24)
- **103동 204호(목표 IP)** — 목적지 IP 주소 (192.168.1.50)
- **경비실(스위치/브로드캐스트)** — ARP Request를 모든 포트로 플러딩하는 L2 스위치
- **거주자(수신자)** — 대상 IP를 가진 호스트, 자신의 MAC으로 ARP Reply 전송
- **ARP 캐시 테이블** — IP-MAC 매핑을 저장해 둔 캐시 (TTL 기반 만료)

> ⚠️ **참고**: 이미지 생성 도구가 PNG 형식으로 반환했습니다. 스킬 요구사항(.jpg/.jpeg)은 현재 도구 제약상 PNG로 대체됩니다.

---

## Step 3: 전문 용어 설명 (위키백과 기반)

### ARP (Address Resolution Protocol, 주소 결정 프로토콜)

**정의**: **ARP(Address Resolution Protocol)**는 **IP 네트워크에서 논리 주소(IP 주소)를 물리 주소(MAC 주소)로 변환**하기 위해 사용되는 통신 프로토콜이다. IPv4 환경에서 필수적이며, OSI 7계층 중 **데이터 링크 계층(Layer 2)**과 **네트워크 계층(Layer 3)** 사이에서 동작한다.

### 동작 원리

| 단계 | 동작 | 설명 |
|------|------|------|
| **1. ARP Request** | 브로드캐스트 송신 | 송신자가 대상 IP의 MAC을 모를 때, 같은 네트워크 대역 모든 호스트에게 `Who has IP X? Tell IP Y` 요청 전송 |
| **2. ARP Reply** | 유니캐스트 응답 | 대상 IP를 가진 호스트만 자신의 MAC 주소를 `IP X is at MAC aa:bb:cc:dd:ee:ff` 형태로 회신 |
| **3. 캐시 저장** | ARP 테이블 갱신 | 송신자는 응답받은 IP-MAC 매핑을 **ARP 캐시(ARP 테이블)**에 저장 (일정 시간 TTL 후 만료) |
| **4. 후속 통신** | 캐시 활용 | 동일 대상 재통신 시 브로드캐스트 없이 캐시된 MAC 주소로 바로 프레임 구성하여 전송 |

### ARP 패킷 구조 (Ethernet + IPv4)

```
┌────────────────────────────────────────────────────────────┐
│ Ethernet Header                                            │
├─────────────┬─────────────┬─────────────┬──────────────────┤
│ Dst MAC     │ Src MAC     │ EtherType   │ ARP Payload      │
│ (ff:ff:ff:  │ (송신자     │ 0x0806      │ (28 bytes)       │
│  ff:ff:ff)  │  MAC)       │ (ARP)       │                  │
├─────────────┴─────────────┴─────────────┴──────────────────┤
│ ARP Payload Fields:                                        │
│ Hardware Type (HTYPE) = 1 (Ethernet)                       │
│ Protocol Type (PTYPE) = 0x0800 (IPv4)                      │
│ Hardware Size (HLEN) = 6 (MAC 주소 길이)                   │
│ Protocol Size (PLEN) = 4 (IPv4 주소 길이)                  │
│ Operation (OPER) = 1(Request) / 2(Reply)                   │
│ Sender Hardware Address (SHA) = 송신자 MAC                 │
│ Sender Protocol Address (SPA) = 송신자 IP                  │
│ Target Hardware Address (THA) = 00:00... (Request 시)      │
│ Target Protocol Address (TPA) = 대상 IP                    │
└────────────────────────────────────────────────────────────┘
```

### 주요 특징

| 특징 | 설명 |
|------|------|
| **비연결성** | 연결 설정 과정 없음 (Request-Reply 단순 교환) |
| **스테이트리스** | 프로토콜 자체에 상태 없음, 캐시는 호스트가 별도 관리 |
| **로컬 네트워크 한정** | 라우터를 넘지 않음 (같은 브로드캐스트 도메인 내) |
| **캐시 타임아웃** | 일반적으로 30초~수 분 (OS별 상이, Linux 기본 ~60초) |
| **Gratuitous ARP** | 요청 없이 자기 IP-MAC 알림 (IP 중복 검사, 페일오버 시 갱신) |

### 보안 이슈: **ARP Spoofing (ARP Poisoning)**

- ARP는 **인증 메커니즘이 없음** → 공격자가 위조된 ARP Reply로 **MAC 주소 가로채기** 가능
- **공격 시나리오**: 공격자 → 피해자("게이트웨이 IP 내 MAC이야"), 게이트웨이("피해자 IP 내 MAC이야") → **MITM(Man-in-the-Middle)** 성립
- **방어**: Dynamic ARP Inspection (DAI), Static ARP 엔트리, Port Security, ARPwatch 모니터링

### IPv6에서의 대체: **NDP (Neighbor Discovery Protocol)**

- IPv6에서는 **ARP 폐지**, ICMPv6 기반 **NDP** 사용
- 멀티캐스트 기반 Neighbor Solicitation/Advertisement로 동작
- 보안 강화: **SEND(SEcure Neighbor Discovery)** 지원

### 관련 도구 및 명령어

| 도구/명령어 | 용도 |
|-------------|------|
| `arp -a` / `ip neigh` | ARP 캐시 조회 |
| `arping` | ARP Request 수동 송신 |
| `arpwatch` | ARP 변동 모니터링 (스푸핑 탐지) |
| `ettercap`, `bettercap` | ARP 스푸핑 공격/테스트 |
| Wireshark 필터 `arp` | ARP 패킷 분석 |

---

## 관련 위키 링크

- [[rce]] — 원격 코드 실행 (네트워크 계층 공격 후 상위 계층 익스플로잇)
- [[reconnaissance]] — 정찰 (ARP 스캔을 통한 네트워크 토폴로지 파악)
- [[sql-injection]] — SQL 인젝션 (애플리케이션 계층 공격과 대비)

---

## 참고 문헌

- 한국어 위키백과: [주소 결정 프로토콜](https://ko.wikipedia.org/wiki/주소_결정_프로토콜)
- 한국어 위키백과: [ARP 스푸핑](https://ko.wikipedia.org/wiki/ARP_스푸핑)
- 한국어 위키백과: [네이버 디스커버리 프로토콜](https://ko.wikipedia.org/wiki/네이버_디스커버리_프로토콜)