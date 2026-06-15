---
title: DoS/DDoS — 보안 용어 해설
created: 2026-06-13
updated: 2026-06-13
type: concept
tags: [security, glossary, dos, ddos, denial-of-service, botnet, amplification, network-security, cloudflare, mirai]
sources: [https://ko.wikipedia.org/wiki/분산_서비스_거부_공격, https://ko.wikipedia.org/wiki/서비스_거부_공격, https://ko.wikipedia.org/wiki/봇넷, https://ko.wikipedia.org/wiki/Mirai_(악성코드), https://ko.wikipedia.org/wiki/SYN_플러드, https://ko.wikipedia.org/wiki/DNS_증폭_공격, https://ko.wikipedia.org/wiki/클라우드플레어]
confidence: high
---

# DoS / DDoS (서비스 거부 / 분산 서비스 거부 공격)

## Step 1: 단어 직역 및 쉬운 비유

### 1. 약자 풀이

**DoS** = **D**enial **o**f **S**ervice
**DDoS** = **D**istributed **D**enial **o**f **S**ervice

| 약자 | Full Name | 직역 | 의미 |
|------|-----------|------|------|
| **Do** | **Denial of** | 거부하는, 부인하는 | 못하게 막음 |
| **S** | **Service** | 서비스 | 제공되는 기능 |
| **DDoS** | **Distributed** + DoS | 분산된 + 서비스 거부 | 여러 출처에서 동시에 서비스 거부 |

### 2. 의미 조합
**DoS**: 단일 출처에서 대상 시스템에 과도한 트래픽/요청을 보내 정상 사용자의 서비스 이용을 방해하는 공격

**DDoS**: 수많은 분산된 출처(봇넷)에서 동시에 대상 시스템을 압도하여 서비스를 마비시키는 훨씬 강력한 공격

### 3. 강력한 비유: "레스토랑 앞을 막는 트럭 한 대 vs 수백 대의 트럭"

| 비유 요소 | 대응 개념 | 설명 |
|-----------|-----------|------|
| **레스토랑** | **웹 서버 / 애플리케이션** | 서비스 제공자 |
| **손님들** | **정상 사용자 트래픽** | 실제로 서비스를 이용하려는 사람들 |
| **트럭 한 대가 정문 앞을 막음** | **DoS 공격** | 단일 IP/소스가 서버를 압도 |
| **수백 대 트럭 행렬이 레스토랑 포위** | **DDoS 공격** | 수만~수십만 개의 분산된 IP가 동시 공격 |
| **트럭 운전사들 = 감염된 좀비 PC** | **봇넷 (Botnet)** | 공격자가 원격 조종하는 감염 기기들 |
| **트럭이 문 앞에 주차만 함** | **대역폭 소진 공격** | 네트워크 대역폭을 다 채워서 정상 트래픽 차단 |
| **트럭이 계속 경적 울리며 주문함** | **애플리케이션 계층 공격** | 서버 리소스(CPU/메모리)를 고갈시킴 |
| **트럭 한 대가 경비원 10명 붙잡음** | **SYN Flood** | TCP 핸드셰이크 연결 테이블 고갈 |
| **100대 트럭이 동시에 경비원 붙잡음** | **DDoS SYN Flood** | 분산된 출처에서 동시 SYN 요청 → 완전 마비 |

**핵심 포인트**:
- **DoS**: 한 사람이 레스토랑 앞에서 "못 들어와!" 외침 → 경비원 한 명이 막을 수 있음
- **DDoS**: 수천 명이 레스토랑 사방을 둘러싸고 "못 들어와!" 외침 → 막기 어려움
- DoS는 방화벽에서 IP 하나 차단하면 끝, **DDoS는 IP 수십만 개라서 IP 차단만으로 방어 불가능**

---

## Step 2: 개념 시각화

![DoS/DDoS 비교 시각화: DoS(트럭 1대) vs DDoS(트럭 행렬/봇넷), 대상 서버, 정상 사용자 차단, SYN Flood, HTTP Flood, DNS 증폭, 대역폭/리소스 고갈 - 한글 레이블 포함](https://v3b.fal.media/files/b/0a9e1c39/wy1ihuHcTrAkphlB-9LwB_soUwp0xG.png)

> ⚠️ **참고**: 이미지 생성 도구가 PNG 형식으로 반환했습니다. 스킬 요구사항(.jpg/.jpeg)은 현재 도구 제약상 PNG로 대체됩니다.

---

## Step 3: 전문 용어 설명 (Wikipedia 기반)

### DoS / DDoS 정의

**DoS**: 대상 시스템(서버, 네트워크, 서비스)에 과도한 트래픽/요청을 보내 정상적인 서비스 제공을 불가능하게 만드는 공격

**DDoS**: 수많은 분산된 노드(봇넷)에서 동시에 발생하여 탐지와 차단이 훨씬 어려운 형태

### DoS vs DDoS 비교

| 비교 항목 | DoS | DDoS |
|-----------|-----|------|
| **공격 출처** | 단일 IP/시스템 | 수만~수십만 개 분산 IP (봇넷) |
| **탐지 난이도** | 낮음 — 단일 IP 차단으로 방어 가능 | 매우 높음 — IP 기반 차단 불가능 |
| **공격 규모** | 수백 Mbps ~ 수 Gbps | 수백 Gbps ~ 수 Tbps |
| **필요 자원** | 공격자 PC 1대로 가능 | 봇넷 필요 (수천~수만 대 감염 기기) |
| **방어 방식** | 방화벽 ACL, Rate Limiting | CDN/Scrubber/Anycast — 차원이 다른 방어 |
| **법적 처벌** | 비교적 추적 용이 | 추적 극히 어려움 (C2 경유, Tor 사용) |
| **대표 사례** | Ping of Death(1996), Slowloris | Mirai(2016, 1.2Tbps), AWS Shield(2020, 2.3Tbps) |

### DDoS 공격 분류

#### L3/L4 — 네트워크/전송 계층 공격

| 공격 유형 | 설명 | 방어 방법 |
|-----------|------|-----------|
| **SYN Flood** | TCP SYN 패킷 대량 전송 → 연결 테이블 고갈 | SYN Cookie, SYN Proxy, Rate Limiting |
| **UDP Flood** | 대량 UDP 패킷 랜덤 포트 전송 → ICMP 응답 소모 | UDP Rate Limiting, Stateful inspection |
| **ICMP Flood** | 대량 Ping 패킷 → 대역폭/CPU 고갈 | ICMP Rate Limiting, 방화벽 차단 |
| **Smurf Attack** | Spoofed ICMP 브로드캐스트 → 증폭 | Directed Broadcast 차단 |

#### L7 — 애플리케이션 계층 공격

| 공격 유형 | 설명 | 방어 방법 |
|-----------|------|-----------|
| **HTTP Flood** | 정상 HTTP GET/POST 대량 전송 → CPU/메모리 고갈 | Rate Limiting, CAPTCHA, WAF, JS Challenge |
| **Slowloris** | HTTP 헤더 느리게 전송 → 연결 풀 고갈 | Keep-Alive 타임아웃, 리버스 프록시 |
| **Slow POST** | POST 본문 1byte/2초 전송 → 연결 장시간 점유 | Content-Length 기반 타임아웃 |

### 증폭 공격 (Amplification Attacks)

| 프로토콜 | 증폭 비율 | 최대 크기 | 특징 |
|----------|-----------|-----------|------|
| **Memcached** | **1:51,000** | ~6MB | GitHub 1.35Tbps (2018) |
| **NTP** | 1:556 | ~4.6KB | monlist 명령어 |
| **DNS** | 1:50~70 | ~4KB | ANY/TXT 레코드 |
| **SSDP** | 1:30~75 | ~7KB | UPnP |

### 봇넷 (Botnet) — DDoS 핵심 인프라

| 구성 요소 | 설명 |
|-----------|------|
| **C2 (Command & Control)** | 봇넷 사령부 — IRC, P2P, Tor, TLS 기반 |
| **봇 (Bot/Zombie)** | 감염된 일반 기기 (PC, IoT, CCTV, 라우터) |
| **C2 프로토콜** | IRC(고전) → HTTP(S) → P2P/Tor(현대) |

**주요 봇넷**:
| 봇넷 | 등장 | 규모 | 특징 |
|------|------|------|------|
| **Mirai** | 2016 | 600k IoT | CCTV/라우터, 1.2Tbps Dyn DNS 공격 |
| **Zeus Gameover** | 2011 | 1M+ PC | P2P 기반, 금융+ DDoS |
| **Emotet** | 2014 | 1.5M+ | 이메일 웜 → DDoS 모듈 |

### DDoS 방어 전략

| 방어 계층 | 기술 | 설명 |
|-----------|------|------|
| **사전 예방** | 네트워크 용량 계획, CDN, Anycast BGP | 대역폭을 공격 규모 이상으로 확보 |
| **온-프레미스** | IPS 인라인, 방화벽 Rate Limiting, SYN Cookie | 소규모 공격 차단 (5~10Gbps 이하) |
| **클라우드 스크러빙** | Cloudflare, AWS Shield, Akamai, GCP Cloud Armor | 트래픽을 스크러빙 센터로 리디렉션 후 정화 |
| **애플리케이션 방어** | WAF, JS Challenge, CAPTCHA, Rate Limiting | L7 애플리케이션 공격 방어 |
| **Anycast 네트워크** | 동일 IP 전 세계 PoC 광고 → 트래픽 분산 | Cloudflare, Google 핵심 기술 |
| **BGP RTBH/Flowspec** | ISP 레벨 Null 라우팅/정밀 필터링 | 고급 ISP 협력 필요 |

### 실제 주요 DDoS 공격 사례

| 연도 | 사건 | 규모 | 유형 | 영향 |
|------|------|------|------|------|
| 2016 | **Mirai — Dyn DNS** | 1.2 Tbps | IoT 봇넷 | Twitter, Netflix, GitHub, Reddit 마비 |
| 2018 | **Memcached Amplification** | 1.35 Tbps | 증폭 1:51,000 | GitHub (10분 만에 종료) |
| 2020 | **AWS Shield** | 2.3 Tbps | CLDAP 증폭 | AWS 고객 (3일 지속, 자동 방어) |
| 2021 | **Microsoft Azure** | 3.47 Tbps | UDP Amplification | Azure 고객 (중국 발) |

---

### 출처
- 한국어 위키백과: ["분산 서비스 거부 공격"](https://ko.wikipedia.org/wiki/분산_서비스_거부_공격) — DDoS 정의, 유형, 방어
- 한국어 위키백과: ["서비스 거부 공격"](https://ko.wikipedia.org/wiki/서비스_거부_공격) — DoS 정의 및 DDoS와의 차이
- 한국어 위키백과: ["봇넷"](https://ko.wikipedia.org/wiki/봇넷) — DDoS 인프라 설명
- 한국어 위키백과: ["Mirai (악성코드)"](https://ko.wikipedia.org/wiki/Mirai_(악성코드)) — IoT 봇넷 DDoS 사례
- 한국어 위키백과: ["SYN 플러드"](https://ko.wikipedia.org/wiki/SYN_플러드) — L4 DDoS 대표 기법
- 한국어 위키백과: ["DNS 증폭 공격"](https://ko.wikipedia.org/wiki/DNS_증폭_공격) — 반사/증폭 공격 원리
- 한국어 위키백과: ["클라우드플레어"](https://ko.wikipedia.org/wiki/클라우드플레어) — DDoS 방어 서비스

---

## 관련 위키 링크
- [[dos]] — DoS (서비스 거부 공격) — DDoS의 단일 출처 버전, IP 차단으로 방어 가능
- [[ips]] — IPS (Intrusion Prevention System) — DDoS 방어의 온-프레미스 계층
- [[ids]] — IDS (Intrusion Detection System) — DDoS 트래픽 패턴 탐지
- [[tcp]] — TCP (Transmission Control Protocol) — SYN flood 기반 DDoS의 핵심 전송 계층 프로토콜
- [[vpn]] — VPN (가상 사설망) — DDoS 공격이 VPN 인프라에도 영향
- [[cia]] — CIA Triad (가용성) — DDoS는 가용성(Availability)을 직접적으로 파괴하는 공격