---
title: VPN (Virtual Private Network) — 가상 사설망
created: 2026-06-12
updated: 2026-06-16
type: concept
tags: [security, glossary, vpn, encryption, tunneling, network-security, remote-access, wireguard, ipsec]
sources: [https://ko.wikipedia.org/wiki/가상_사설망, https://ko.wikipedia.org/wiki/IPsec, https://ko.wikipedia.org/wiki/OpenVPN, https://ko.wikipedia.org/wiki/WireGuard, https://ko.wikipedia.org/wiki/암호화, https://ko.wikipedia.org/wiki/터널링_프로토콜, https://ko.wikipedia.org/wiki/제로_트러스트_보안]
confidence: high
---

# VPN (Virtual Private Network) — 가상 사설망

## Step 1: 단어 직역 및 쉬운 비유

### 1. 약자 풀이
**VPN** = **V**irtual **P**rivate **N**etwork

| 약자 | 영어 단어 | 직역 | 의미 |
|------|-----------|------|------|
| **V** | **Virtual** | 가상의, 실제 같지만 실제는 아닌 | 물리적 회선 없이 소프트웨어로 만든 연결 |
| **P** | **Private** | 사적인, 개인 전용의 | 타인이 볼 수 없고 나만 사용하는 공간 |
| **N** | **Network** | 네트워크, 통신망 | 컴퓨터와 컴퓨터를 연결하는 통로 |

### 2. 의미 조합
> **공용 인터넷(도로) 위에 소프트웨어로 암호화된 전용 터널을 만들어, 마치 같은 사무실에 있는 것처럼 안전하게 데이터를 주고받는 가상의 사설 네트워크**

### 3. 강력한 비유: "해적 바다 위의 보이지 않는 비밀 터널"

| 비유 요소 | 대응 개념 | 설명 |
|-----------|-----------|------|
| **본사 건물** | 내부 네트워크 (회사 LAN) | 안전한 출발지 |
| **지사 건물** | 원격 네트워크 (지사 LAN) | 안전한 도착지 |
| **해적 득실대는 바다** | 공용 인터넷 | 누구나 엿볼 수 있고, 스니핑/MITM 위험 존재 |
| **지하 비밀 터널** | **VPN 터널 (암호화 채널)** | 인터넷 위를 가로지르지만 아무도 내용 못 봄 |
| **택배 상자** | **데이터 패킷** | 보내는 실제 정보 |
| **터널 입구의 암호 잠금장치** | **암호화 (Encryption)** | 터널 안으로 들어갈 때 자물쇠로 잠금 |
| **터널 출구의 열쇠** | **복호화 (Decryption)** | 나올 때만 열쇠로 풀어서 원래 내용 확인 |
| **가면 쓴 택배 기사** | **IP 주소 위장 / 익명성** | 택배 기사가 가면 쓰고 다녀서 해적이 누가 보냈는지 모름 |
| **해적이 터널 입구 보는 것** | **메타데이터 노출** | 내용(데이터)은 못 보지만 누가 터널 썼는지는 볼 수 있음 |

**동작 순서**:
1. 본사에서 택배 준비 → 데이터 패킷 생성
2. 터널 입구에서 자물쇠 잠금 → VPN 클라이언트가 데이터 **암호화**
3. 해적 바다(인터넷) 위로 터널 통과 → 암호화된 패킷이 인터넷을 통해 전송
4. 터널 출구에서 자물쇠 해제 → VPN 서버가 데이터 **복호화**
5. 지사에 안전하게 택배 도착 → 원래 데이터 형태로 전달

**핵심 포인트**: VPN을 쓰면 **해적이 바다 한가운데서 패킷을 낚아채도** 자물쇠(암호화) 때문에 내용을 절대 볼 수 없습니다. 또한 **택배 기사가 가면(가상 IP)을 쓰고 있어서** 해적이 "누가 보냈는지" 알 수 없어 추적도 어렵습니다.

---

## Step 2: 개념 시각화

![VPN 비유 시각화: 본사 네트워크(안전), 지사 네트워크(안전), 인터넷(위험한 바다/해적), VPN 터널(암호화된 비밀 통로), 데이터(택배 상자), 외부인(해커) 차단, 익명성(가면 쓴 택배 기사) - 한글 레이블 포함](https://v3b.fal.media/files/b/0a9e19a5/g0FiZWCmh6yD5MdhRmOZ__wzK8Xv0c.png)

**이미지 설명**:
- **본사 네트워크(안전)** — 사내 LAN, 출발지
- **지사 네트워크(안전)** — 사내 LAN, 도착지
- **인터넷(위험한 바다/해적)** — 패킷 스니핑, MITM, IP 추적 등 위협이 존재하는 공용망
- **VPN 터널(암호화된 비밀 통로)** — IPsec/WireGuard/OpenVPN 등이 만드는 암호화 터널
- **데이터(택배 상자)** — 암호화된 IP 패킷
- **외부인(해커) 차단** — 인증 + 암호화로 무단 접근 방지
- **익명성(가면 쓴 택배 기사)** — 실제 IP가 아닌 VPN 서버 IP로 출발지 위장

> ⚠️ **참고**: 이미지 생성 도구가 PNG 형식으로 반환했습니다. 스킬 요구사항(.jpg/.jpeg)은 현재 도구 제약상 PNG로 대체됩니다.

---

## Step 3: 전문 용어 설명 (Wikipedia 기반)

### 가상 사설 네트워크 (Virtual Private Network, VPN)

**정의**: 공용 통신망(인터넷) 위에 **암호화·인증·터널링 기술을 결합**하여 물리적으로 떨어진 네트워크 간 또는 사용자-네트워크 간 **안전한 전용 통로(터널)를 가상으로 구축**하는 기술이다.

---

### 작동 원리 (VPN Tunneling Protocol Stack)

```
┌─────────────────────────────────────────┐
│          원본 IP 패킷 (내부 데이터)         │
├─────────────────────────────────────────┤
│     VPN 캡슐화 헤더 (터널 제어 정보)        │
├─────────────────────────────────────────┤
│     암호화 (Encryption) + 인증 (Auth)      │
├─────────────────────────────────────────┤
│     외부 IP 헤더 (VPN 서버 IP 주소)         │
├─────────────────────────────────────────┤
│          인터넷 전송 (공용망)               │
└─────────────────────────────────────────┘
```

1. **캡슐화 (Encapsulation)**: 원본 IP 패킷 전체를 새로운 IP 패킷의 페이로드로 감싼다.
2. **암호화 (Encryption)**: 페이로드(원본 패킷)를 암호화 키로 암호화하여 중간에서 가로채도 내용 식별 불가.
3. **인증 (Authentication)**: HMAC/디지털 서명으로 패킷 변조(malleability) 및 재전송(replay) 방지.
4. **전송 (Transmission)**: 암호화된 패킷이 공용 인터넷을 통해 VPN 서버로 전달됨.
5. **복호화/역캡슐화 (Decapsulation)**: VPN 서버가 패킷을 복호화하고 원본 IP 패킷을 추출하여 목적지 네트워크로 전달.

---

### VPN 프로토콜 비교

| 프로토콜 | 암호화 | 속도 | 보안 수준 | 설정 복잡도 | 특징 |
|----------|--------|------|-----------|-------------|------|
| **IPsec (IKEv2)** | AES-256-GCM, AES-256-CBC | ★★★☆ | ★★★★★ | ★★★★ | ESP/AH, IKEv2 MOBIKE(이동성), Site-to-Site 표준 |
| **WireGuard** | ChaCha20-Poly1305 | ★★★★★ | ★★★★★ | ★☆☆☆ | 최신 프로토콜, 리눅스 커널 내장, 4000줄 코드 |
| **OpenVPN** | AES-256-GCM, ChaCha20-Poly1305 | ★★★☆ | ★★★★★ | ★★★☆ | 가장 검증됨, TLS 기반, 방화벽 우회 우수 |
| **L2TP/IPsec** | AES-256-CBC (IPsec 위) | ★★☆☆ | ★★★★ | ★★★★ | IPsec으로 암호화, L2TP로 터널링, 구형 |
| **PPTP** | MPPE (RC4) | ★★★★ | ★☆☆☆ | ★☆☆☆ | **사용 금지** — 2012년 MS 공식 폐기, 128비트 RC4 취약 |
| **SSTP** | AES-256-CBC | ★★★☆ | ★★★★ | ★★☆☆ | MS 독점, HTTPS 443 포트, 방화벽 우회 우수 |
| **SoftEther** | AES-256-GCM | ★★★★ | ★★★★★ | ★★★☆ | 오픈소스, 멀티 프로토콜 지원, 패킷 로스 복원 |

> ⚠️ **PPTP는 절대 사용하지 말 것**: MS-CHAPv2 인증은 2012년 brute-force로 23분 만에 크랙 가능. 현재 표준은 **WireGuard > OpenVPN > IKEv2/IPsec** 순.

---

### VPN 구축 유형 (Use Cases)

| 유형 | 설명 | 대표 기술 | 활용 사례 |
|------|------|-----------|-----------|
| **Remote Access VPN** | 개별 사용자가 원격에서 회사 내부망 접속 | OpenVPN, WireGuard, AnyConnect, GlobalProtect | 재택근무, 출장 직원, 모바일 오피스 |
| **Site-to-Site VPN** | 지사-본사 또는 클라우드-VPC 간 연결 | IPsec IKEv2, AWS VPN, Azure VPN Gateway | 하이브리드 클라우드, MPLS 대체, 데이터센터 연결 |
| **Client-to-Site VPN** | VPN 클라이언트 SW 설치하여 접속 | OpenVPN Connect, Tunnelblick, Tailscale | 개인 노트북 → 회사망, BYOD 환경 |
| **Split Tunnel VPN** | 내부망 트래픽만 VPN, 외부는 직접 라우팅 | 모든 프로토콜 지원 | 대역폭 절약, 지연 시간 최소화, Netflix 우회 |
| **Full Tunnel VPN** | 모든 트래픽을 VPN 경유 | 모든 프로토콜 지원 | 최대 보안, 검열 우회, IP 위치 위장 |
| **Cloud VPN** | 클라우드 VPC와 온프레미스 간 암호화 연결 | AWS Site-to-Site VPN, GCP Cloud VPN, Azure VPN Gateway | 하이브리드 클라우드 아키텍처 |
| **Mesh VPN** | P2P 연결, 중앙 서버 없이 노드 간 직접 터널 | WireGuard 기반 (Tailscale, Netmaker, ZeroTier) | DevOps, IoT, 분산 팀, Kubernetes 클러스터 |

---

### VPN 보안 고려사항 및 한계

| 고려사항 | 설명 |
|----------|------|
| **제로 트러스트와의 관계** | VPN은 "한 번 인증되면 전부 신뢰" → 제로 트러스트에서는 **VPN 대체**로 ZTNA(SDP) 권장 |
| **로그 정책 / No-Log VPN** | 상용 VPN 제공업체의 로그 보관 정책 확인 필수 (일부 국가는 법적 로그 의무) |
| **IPv6/DNS 누출 (Leak)** | VPN 비활성화 시 원래 IP 노출 가능 → **Kill Switch + DNS Leak Protection** 필수 |
| **메타데이터 노출** | VPN이 내용(데이터)은 숨기지만 연결 자체(타이밍, 볼륨, 빈도)는 ISP/기관이 관찰 가능 |
| **법적·규제 이슈** | 특정 국가(중국, 러시아, 이란, UAE)에서 VPN 사용 제한/금지, 라이선스 필요 |
| **성능 저하** | 암호화 오버헤드, 터널링 라우팅으로 일반 연결 대비 5-30% 대역폭 감소 (WireGuard는 최소화) |

---

### 주요 표준 및 참조 문서

| 표준/문서 | 설명 |
|-----------|------|
| **RFC 4301** | IPsec Security Architecture for the Internet Protocol |
| **RFC 7296** | Internet Key Exchange Protocol Version 2 (IKEv2) |
| **RFC 8446** | TLS 1.3 (OpenVPN 제어 채널에 사용) |
| **WireGuard Whitepaper** | Jason A. Donenfeld (2017) — 20 pages, 커널 보안 감사 완료 |
| **NIST SP 800-77 Rev.1** | Guide to IPsec VPNs |
| **NIST SP 800-113** | Guide to SSL VPNs |

---

### 출처
- 한국어 위키백과: ["가상 사설망"](https://ko.wikipedia.org/wiki/가상_사설망) — VPN 정의, 종류, 프로토콜
- 한국어 위키백과: ["IPsec"](https://ko.wikipedia.org/wiki/IPsec) — IKE, ESP, AH 상세
- 한국어 위키백과: ["OpenVPN"](https://ko.wikipedia.org/wiki/OpenVPN) — 오픈소스 VPN 표준
- 한국어 위키백과: ["WireGuard"](https://ko.wikipedia.org/wiki/WireGuard) — 차세대 경량 VPN 프로토콜
- 한국어 위키백과: ["암호화"](https://ko.wikipedia.org/wiki/암호화) — 대칭키/비대칭키 암호화
- 한국어 위키백과: ["터널링 프로토콜"](https://ko.wikipedia.org/wiki/터널링_프로토콜) — VPN의 네트워크 계층
- 한국어 위키백과: ["제로 트러스트 보안"](https://ko.wikipedia.org/wiki/제로_트러스트_보안) — VPN의 대안 및 진화 방향

---

## 관련 위키 링크
- [[arp]] — ARP (Address Resolution Protocol) — VPN과 함께 네트워크 계층 프로토콜
- [[tcp]] — TCP (Transmission Control Protocol) — VPN 터널 위에서 자주 사용되는 전송 계층 프로토콜
- [[cia]] — CIA Triad (기밀성) — VPN이 제공하는 기밀성·무결성·인증과 직접 연계
- [[reconnaissance]] — Reconnaissance (정찰) — VPN이 방어하는 네트워크 스니핑 위협
- [[rce]] — RCE (원격 코드 실행) — VPN 우회 후 내부망에서 발생 가능한 치명적 취약점
- [[sql-injection]] — SQL Injection — VPN 내부망 DB 접근 시 발생 가능한 공격