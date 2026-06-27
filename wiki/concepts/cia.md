---
title: CIA Triad (CIA 트라이어드) — 정보보안의 3대 핵심 원칙
created: 2026-06-12
updated: 2026-06-21
type: concept
tags: [security, glossary, cia, confidentiality, integrity, availability, triad, iso27001, nist, parkerian-hexad]
sources: [https://ko.wikipedia.org/wiki/CIA_트라이어드, https://ko.wikipedia.org/wiki/정보보안, https://ko.wikipedia.org/wiki/ISO/IEC_27001, https://ko.wikipedia.org/wiki/미국_국립표준기술연구소, https://ko.wikipedia.org/wiki/암호학, https://ko.wikipedia.org/wiki/고가용성, https://ko.wikipedia.org/wiki/파커리안_헥사드]
confidence: high
---

# CIA Triad (CIA 트라이어드) — 정보보안의 3대 핵심 원칙

## 참고 URL
- [ko.wikipedia.org](https://ko.wikipedia.org/wiki/CIA_트라이어드)
- [ko.wikipedia.org](https://ko.wikipedia.org/wiki/정보보안)
- [ko.wikipedia.org](https://ko.wikipedia.org/wiki/ISO/IEC_27001)
- [ko.wikipedia.org](https://ko.wikipedia.org/wiki/미국_국립표준기술연구소)
- [ko.wikipedia.org](https://ko.wikipedia.org/wiki/암호학)
- [ko.wikipedia.org](https://ko.wikipedia.org/wiki/고가용성)
- [ko.wikipedia.org](https://ko.wikipedia.org/wiki/파커리안_헥사드)

## Step 1: 단어 직역 및 쉬운 비유

### 1. 약자 풀이
**CIA** = **C**onfidentiality, **I**ntegrity, **A**vailability
→ 정보보안의 **3대 핵심 원칙(트라이어드, Triad)**

| 약자 | 영어 단어 | 직역 | 보안적 의미 |
|------|-----------|------|-------------|
| **C** | **Confidentiality** | 기밀성, 비밀 유지 | **권한 있는 자만** 정보에 접근 가능 |
| **I** | **Integrity** | 무결성, 온전함, 완전성 | 정보가 **임의로 변경/삭제되지 않음** |
| **A** | **Availability** | 가용성, 이용 가능성 | **필요할 때** 정보/시스템 사용 가능 |

### 2. 의미 조합
> **정보 자산을 보호하기 위해 반드시 지켜야 할 3대 목표: 승인된 사용자만 볼 수 있게 하고(기밀성), 데이터가 변조되지 않게 하며(무결성), 필요할 때 언제든 쓸 수 있게 한다(가용성) — 이 세 가지가 균형을 이뤄야 진정한 보안이 성립한다.**

### 3. 강력한 비유: "왕실 금고를 지키는 세 명의 수호 기사"

| 수호 기사 | 역할 | 비유 설명 |
|-----------|------|-----------|
| **기밀성 기사 (C)** | **"열쇠 관리인"** | 금고 열쇠는 **왕과 재무장관만** 가짐. 도둑이 성에 들어와도 금고는 못 엶. → 접근 제어(ACL), 암호화, 인증 |
| **무결성 기사 (I)** | **"봉인 검사관"** | 금고 문에 **특수 왁스 봉인** + **내용물 목록 장부**. 누가 살짝 열어서 금화 하나 빼가도 바로 들킴. → 해시/디지털 서명, 버전 관리, WORM |
| **가용성 기사 (A)** | **"비상 발전기/예비 열쇠 담당"** | 정전돼도 **발전기 돌아감**, 열쇠 잃어버려도 **마스터 키 보관**. 전쟁 중에도 금고 열 수 있음. → 이중화(HA), 백업, DR, DDoS 방어 |

**핵심 포인트**:
- 기밀성만 강조 → 금고 너무 단단히 잠가서 **왕도 못 열게 됨(서비스 중단)**
- 무결성만 강조 → 모든 변경에 **결재 10단계 거쳐야 함(업무 마비)**
- 가용성만 강조 → 금고 **활짝 열어둠(누구나 훔쳐감)**

**진정한 보안 = 세 기사가 서로 타협하며 균형 맞추기** ⚖️
- 예: 암호화(기밀성 ↑) → 복호화 시간 ↑ → 가용성 ↓ → **적절한 알고리즘/키 길이 선택으로 균형**
- 예: 엄격한 변경 관리(무결성 ↑) → 배포 지연 → 가용성 ↓ → **CI/CD 파이프라인에 무결성 검사 자동화로 균형**

---

## Step 2: 개념 시각화

![CIA 트라이어드 비유 시각화: 기밀성(열쇠 관리인), 무결성(봉인 검사관), 가용성(비상 발전기/예비 열쇠) - 한글 레이블 포함, 삼각형 균형 구조](https://v3b.fal.media/files/b/0a9dfac2/-ejKyvks958f789iJkqFk_qxpui9LY.png)

**이미지 설명**:
- **기밀성(Confidentiality) — 열쇠 관리인** — 권한 있는 자만 접근, 암호화, 인증, ACL
- **무결성(Integrity) — 봉인 검사관** — 데이터 변조 탐지/방지, 해시, 디지털 서명, 버전 관리
- **가용성(Availability) — 비상 발전기/예비 열쇠** — 서비스 지속성, 이중화, 백업, DR, DDoS 방어
- **중앙 삼각형** — 세 요소 간 **트레이드오프(trade-off)와 균형** 시각화

> ⚠️ **참고**: 이미지 생성 도구가 PNG 형식으로 반환했습니다. 스킬 요구사항(.jpg/.jpeg)은 현재 도구 제약상 PNG로 대체됩니다.

---

## Step 3: 전문 용어 설명 (Wikipedia 기반)

### CIA 트라이어드 (Confidentiality, Integrity, Availability)

**정의**: 정보보안(Information Security) 분야에서 정보 자산 보호의 **3대 핵심 목표**를 나타내는 모델이다. 1970년대 미 군사 표준(DoD 5200.28-STD)에서 유래했으며, 현재 ISO/IEC 27001, NIST SP 800-53 등 국제 표준의 기초가 된다.

---

### 1. 기밀성 (Confidentiality)

**정의**: 정보가 **승인되지 않은 개인·엔티티·프로세스에게 공개되지 않는 성질**

| 구현 기법 | 설명 |
|-----------|------|
| **암호화 (Encryption)** | 대칭키(AES, ChaCha20), 비대칭키(RSA, ECC), TLS/SSL, IPsec, 디스크 암호화(LUKS, BitLocker) |
| **접근 제어 (Access Control)** | RBAC(역할 기반), ABAC(속성 기반), MAC(강제), DAC(임의), 최소 권한 원칙 |
| **인증 (Authentication)** | MFA(다중 인증), SSO, 생체인증, FIDO2/WebAuthn, Kerberos, OAuth2/OIDC |
| **데이터 마스킹/난독화** | 프로덕션 데이터를 개발/테스트 환경에서 가명화, 토큰화 |
| **네트워크 분리** | VLAN, DMZ, 제로 트러스트 아키텍처, 마이크로 세그멘테이션 |

**위협 사례**: 데이터 유출(데이터 브리치), 스니핑, 어깨 넘어 보기(Shoulder Surfing), 소셜 엔지니어링, 내부자 위협

---

### 2. 무결성 (Integrity)

**정의**: 정보가 **인가되지 않은 방식으로 생성·수정·삭제되지 않고 정확하고 완전하게 유지되는 성질**

| 구현 기법 | 설명 |
|-----------|------|
| **해시 함수 (Hash Functions)** | SHA-256/384/512, SHA-3, BLAKE3 — 파일/메시지 무결성 검증 |
| **디지털 서명 (Digital Signatures)** | RSA-PSS, ECDSA, EdDSA — 출처 인증 + 변조 탐지 + 부인 방지 |
| **메시지 인증 코드 (MAC/HMAC)** | HMAC-SHA256, AES-GCM, ChaCha20-Poly1305 — 무결성 + 인증 동시 제공 |
| **버전 관리/감사 로그** | Git, WORM 스토리지, 불변 로그(Append-only), 블록체인/머클 트리 |
| **체크섬/패리티** | CRC, ECC 메모리, RAID 패리티 — 저장/전송 중 비트 오류 탐지 |
| **코드 서명/SBOM** | 소프트웨어 공급망 무결성(SLSA, in-toto, Sigstore/Cosign) |

**위협 사례**: 데이터 변조(웹 디페이스먼트, DB 레코드 변경), 랜섬웨어(파일 암호화 = 무결성 파괴), 중간자 공격(MITM), 공급망 공격(의존성 패키지 변조), 로그 삭제/위조

---

### 3. 가용성 (Availability)

**정의**: **인가된 사용자가 필요할 때 정보·시스템·서비스에 접근하여 사용할 수 있는 성질**

| 구현 기법 | 설명 |
|-----------|------|
| **고가용성 아키텍처 (HA)** | Active-Active/Active-Passive 클러스터링, 로드 밸런싱, 페일오버, 멀티 AZ/리전 |
| **백업/복구 (Backup & Recovery)** | 3-2-1 규칙(사본 3개, 매체 2종류, 오프사이트 1개), RPO/RTO 정의, 스냅샷, PITR |
| **재해복구 (DR/BCP)** | 핫/웜/콜드 사이트, DR 플랜 테스트, 런북 자동화, 클라우드 DR(AWS Elastic Disaster Recovery 등) |
| **DDoS 방어** | WAF, CDN(Cloudflare, Akamai), Rate Limiting, Anycast, 스크러빙 센터 |
| **모니터링/자동 복구** | 헬스체크, 오토스케일링, 자기 치유(Self-healing), 카오스 엔지니어링(Chaos Mesh, Gremlin) |
| **용량 계획/성능 관리** | 병목 지점 사전 탐지, 리소스 쿼터, 서킷 브레이커, 벌크헤드 패턴 |

**위협 사례**: DDoS 공격, 랜섬웨어(시스템 마비), 하드웨어 장애, 전력/냉각 장애, 자연재해, 소프트웨어 버그/패치 오류, 인적 실수(잘못된 배포)

---

### CIA 트레이드오프 (Trade-offs) 와 균형 설계

| 상황 | 기밀성 ↔ 가용성 | 무결성 ↔ 가용성 | 기밀성 ↔ 무결성 |
|------|----------------|----------------|----------------|
| **강화 시** | 암호화 오버헤드 ↑, 복구 복잡도 ↑ | 엄격한 검증으로 처리 지연 ↑ | 암호화된 데이터 무결성 검증 어려움 |
| **완화 시** | 평문 저장/전송으로 유출 위험 ↑ | 체크섬 생략으로 변조 미탐지 ↑ | 키 관리 소홀로 양쪽 모두 약화 |
| **균형 전략** | 하드웨어 가속 암호화(AES-NI), 계층별 암호화 | 비동기/증분 무결성 검증, Merkle Tree | 인증된 암호화(AEAD: AES-GCM, ChaCha20-Poly1305) |

> **원칙**: **"비즈니스 영향도(BIA) 분석" → 자산 중요도 분류 → CIA 우선순위 차등 적용**
> - 군사/금융/의료: **C ≈ I > A** (기밀성·무결성 최우선)
> - 전자상거래/스트리밍: **A > C ≈ I** (가용성이 매출 직결)
> - 퍼블릭 웹/오픈 데이터: **I > A > C** (무결성이 신뢰 기반)

---

### 관련 표준 및 프레임워크

| 표준/프레임워크 | CIA 연계 내용 |
|----------------|---------------|
| **ISO/IEC 27001:2022** | Annex A 통제 항목이 CIA 3대 목표에 매핑 (A.5~A.8) |
| **NIST SP 800-53 Rev.5** | AC(접근 제어), SC(시스템 통신 보호), SI(시스템 무결성), CP(비상 계획) 패밀리 |
| **NIST CSF 2.0** | Govern, Identify, Protect, Detect, Respond, Recover 6대 기능에 CIA 내재화 |
| **PCI DSS v4.0** | 요구사항 3(저장 데이터 보호=C), 6(보안 시스템 개발=I), 10(로그 모니터링=A) |
| **GDPR** | 제32조(처리 보안) — 기밀성, 무결성, 가용성, 복원력 명시 |

---

### 확장 모델: Parkerian Hexad (파커리안 헥사드)

Donn Parker가 CIA 3요소에 **3가지 추가**하여 제안한 6요소 모델:

| 추가 요소 | 정의 |
|-----------|------|
| **Possession/Control (소유/통제)** | 정보가 권한 있는 주체의 **물리적/논리적 통제 하에 있는가** (도난된 암호화 랩톱 = 기밀성 유지지만 소유권 상실) |
| **Authenticity (진정성/출처성)** | 정보의 **출처·저자·생성 시각이 진짜인가** (위조된 디지털 서명 = 무결성 통과하지만 진정성 위반) |
| **Utility (유용성)** | 정보가 **목적에 맞게 쓸모 있는 형태인가** (암호키 분실로 복호화 불가 = 기밀성/무결성/가용성 모두 충족하지만 유용성 0) |

---

### 출처
- 한국어 위키백과: ["CIA 트라이어드"](https://ko.wikipedia.org/wiki/CIA_트라이어드) — 3대 원칙 정의 및 상세
- 한국어 위키백과: ["정보보안"](https://ko.wikipedia.org/wiki/정보보안) — 보안 목표 및 관리체계
- 한국어 위키백과: ["ISO/IEC 27001"](https://ko.wikipedia.org/wiki/ISO/IEC_27001) — 국제 표준 요구사항
- 한국어 위키백과: ["NIST"](https://ko.wikipedia.org/wiki/미국_국립표준기술연구소) — SP 800 시리즈, CSF 프레임워크
- 한국어 위키백과: ["암호학"](https://ko.wikipedia.org/wiki/암호학) — 기밀성/무결성 구현 기법
- 한국어 위키백과: ["고가용성"](https://ko.wikipedia.org/wiki/고가용성) — 가용성 아키텍처 패턴
- 한국어 위키백과: ["파커리안 헥사드"](https://ko.wikipedia.org/wiki/파커리안_헥사드) — CIA 확장 모델

---

## 관련 위키 링크
- [[dlp]] — DLP (Data Loss Prevention) — CIA 중 기밀성(Confidentiality) 보호를 위한 실무 기술
- [[drm]] — DRM (Digital Rights Management) — 디지털 콘텐츠 사용 통제를 위한 기술
- [[reconnaissance]] — Reconnaissance (정찰) — 공격 전 CIA 약점 파악을 위한 정보 수집 단계
- [[sql-injection]] — SQL Injection — 무결성(데이터 변조) 및 기밀성(데이터 유출) 침해 공격
- [[xss]] — XSS — 무결성(페이지 변조) 및 기밀성(세션 탈취) 침해 공격
