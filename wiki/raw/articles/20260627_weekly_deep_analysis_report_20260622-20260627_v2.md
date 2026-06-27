---
title: 주간 보안 동향 심층 분석 보고서 v2 (2026-06-22 ~ 2026-06-27)
date: 2026-06-27
period: 2026-06-22 ~ 2026-06-27
type: deep-analysis-report-v2
audience: 위협 인텔리전스 분석가, 보안 관제/엔지니어링 리더, CISO
template_basis: CTI 보고서 구조 (Key Judgments + 3축 프레임워크)
related_reports:
  - wiki/raw/articles/2026/202606/weekly-newsletter-20260622-20260626.md
  - wiki/raw/articles/2026/202606/weekly-trend-report-20260622-20260626.md
  - wiki/raw/articles/2026/202606/weekly-deep-analysis-report-20260622-20260626.md (v1)
  - wiki/raw/articles/2026/202606/monthly-trend-report-202606.md
  - wiki/raw/articles/2026/202606/cve-newly-discovered-202606.md
related_external:
  - https://github.com/gameworkerkim/CYBER-THREAT-INTELLIGENCE-REPORT/blob/main/CTI-2026-0628-DPRK-AI.md (구조 참고)
tags: [security, weekly, deep-analysis-v2, threat-intel, key-judgment, mitre-attack, kev, supply-chain, ai-security, korean]
sources:
  - RSS (24개 블로그 통합, blogwatcher-cli v0.2.1)
  - NVD REST API (1,527건 CVE, 6/22~26)
  - CISA KEV (신규 5건)
  - 데일리시큐 + KISA KrCERT
classification: TLP:GREEN
severity: 🔴 HIGH
language: Korean
---

# 🔬 주간 보안 동향 심층 분석 보고서 v2 (2026-06-22 ~ 2026-06-27)

> **본 문서는 v1(weekly-deep-analysis-report)을 CTI 보고서 구조(Key Judgments + 3축 프레임워크 + MITRE ATT&CK + 질적 변화 비교표)로 고도화한 전문가용 보고서입니다.**
> 빠른 요약본이 필요하면 `weekly-newsletter-20260622-20260626.md`를, 일반 분석 보고서는 `weekly-trend-report-20260622-20260626.md`를 함께 봐 주세요.

---

## 0. 📋 Report Metadata

| 항목 | 값 |
|---|---|
| **Report ID** | KISEC-WTDA-2026-W26-v2 |
| **Period** | 2026-06-22 (월) ~ 2026-06-27 (금) — 6일 |
| **Analyst** | Hermes (news profile, MiniMax-M3) |
| **Classification** | TLP:GREEN |
| **Severity** | 🔴 HIGH |
| **Data Sources** | RSS 24개 매체, NVD 1,527 CVE, CISA KEV 5건, 데일리시큐+KISA |
| **Frameworks** | MITRE ATT&CK v15, Lockheed Kill Chain, Diamond Model, CTI KJ 시스템 |

---

## 1. 🎯 핵심 메시지 (TL;DR)

> **"이번 주는 '공급망 공격의 산업화'와 'AI 도구·국가 APT의 결합'이 동시에 가시화된 분기점이다."**

2026년 6월 4주차는 단순한 패치 사이클이 아니라 **운영 모델의 질적 변화**가 관측된 6일이다:

- **축 ① 사회공학·AI 결합**: 클로드+해킹 도구 결합으로 호텔 예약 정보 수백만 건 탈취 정황, Silver Fox APT의 세무조사 통지서 표적형 공격, macOS 가스라이트(북한 연계)
- **축 ② 공급망의 산업화**: Shai-Hulud npm → Klue → BeyondTrust/LastPass의 다층 2차 피해, 폴리마켓 $3M 탈취, Cisco SD-WAN 제로데이
- **축 ③ AI 도구·공식 제품의 공격 표면화**: Chrome 149 (12 Critical), LiteLLM KEV, Flowise/Langflow/n8n 10.0 다발, **아마존 큐 개발자 CVE-2026-12957/12958** (악성 저장소만 열면 AWS 자격증명 탈취)

**한국 특수 정황**: 감염의 절반(48.45%)이 한국에 집중된 **아리스팅어 봇넷** + 세무조사 위장 Silver Fox + 국내 클로드+해킹 도구 = **북한 연계 위협의 일상화**가 이번 주 가장 두드러진 흐름입니다.

---

## 2. 🎯 Key Judgments (핵심 판단) — 7개

이번 주 사건들을 종합해 도출한 7개 핵심 판단입니다. 신뢰도는 High / Medium-High / Medium / Low 4단계로 구분합니다.

| # | 판단 | 신뢰도 |
|---|---|---|
| **KJ-1** | **공급망 공격이 다층화(2차·3차 피해) 단계로 진입**. Shai-Hulud → Klue-Salesforce → BeyondTrust/LastPass → AWS Redshift 침해 킬 체인이 단일 분석 보고서(Fortinet)에서 완전 공개됨. 보안 도구 벤더가 2차 피해자가 되는 **메타 위험**의 실증 사례 | **High** |
| **KJ-2** | **방화벽·VPN이 persistent foothold로 활용**되는 패턴 확립. Russian IAB가 Fortinet SSL VPN을 credential refinery로 운영, StockStay APT는 우크라이나 표적 SSRF+백도어. CISA KEV 6월 신규 22건 중 4건(6/9·6/15·6/18·6/25)이 Cisco/Ubiquiti/Arista 네트워크 장비 | **High** |
| **KJ-3** | **AI 워크플로우 도구가 새로운 공격 표면으로 부상**. Langflow/LiteLLM/Flowise/n8n 등 6월 CVSS 9.9~10.0 CVE가 집중 발표. **LiteLLM은 CISA KEV 등재**(CVE-2026-42271). MCP(Model Context Protocol)의 4대 보안 위험(tool poisoning·indirect prompt injection·token theft·privilege escalation) 구조화 | **High** |
| **KJ-4** | **레거시 결함이 현재 in-the-wild 익스플로잇에 활용**됨이 실증. PTC Windchill(KEV 6/25 첫 in-the-wild), Squidbleed(Squid Proxy, 수십 년), Samsung KNOX(8년), Apple Boot, FFmpeg PixelSmash. "패치 후 안전" 가정은 더 이상 유효하지 않음 | **High** |
| **KJ-5** | **한국 노린 위협의 일상화**. 아리스팅어 봇넷(한국 48.45% 감염), Silver Fox APT(세무조사 위장 기업 표적), 클로드+해킹 도구 결합 러시아 공격자(호텔 정보 수백만 건), DPRK 연계 macOS 가스라이트, North Korea → Mastra npm 침투. 국가별 표적 정밀화 + AI 도구 결합 | **Medium-High** |
| **KJ-6** | **국가 정책의 암호학적 전환점**. 美 양자내성 행정명령(6/23, 연방기관 2030까지 ML-KEM/ML-DSA/SLH-DSA 의무화). 한국 엑스게이트 자체 웹사이트 PQC 적용(6/23), 키페어 금융권 PQC 전환 전략 발표. NIST 표준 호환성 + KMS/HSM 도입이 향후 1~2년 핵심 과제 | **Medium-High** |
| **KJ-7** | **공격자 귀속 불확실성** 동반. Russian APT/Cluster 명 미공개(Fortinet 분석), ShinyHunters vs DPRK의 클로드 활용 사례는 출처별 차이, 클로드+해킹 도구 러시아 공격자는 단정 어려움. **단정 금지, "추정" 표현 권장** | **Medium** |

> **분석 원칙**: 실증(KEV 등재, RFC·CVE 발표, 공식 패치)과 추세 전망(완전 자율 공격, 양자내성 의무화)을 명확히 구분하며, 귀속의 불확실성을 명시합니다.

---

## 3. 🏛️ 3대 축 분석 프레임워크

이번 주 사건들을 **3대 축**(사회공학·공급망·공격 표면화)으로 구조화합니다.

```
┌─────────────────────────────────────────────────────────────────┐
│  축 ① 사회공학 + AI 결합                                          │
│  ├ DPRK 클로드+해킹 도구 (호텔 예약 정보)                            │
│  ├ Silver Fox APT (세무조사 통지서 위장)                              │
│  ├ Russian 클로드+해킹 도구 (호텔 정보)                              │
│  └ macOS 가스라이트 (북한 연계, AI 분석 방해)                         │
├─────────────────────────────────────────────────────────────────┤
│  축 ② 공급망 공격의 다층화                                          │
│  ├ Shai-Hulud → Fortinet Redshift 킬체인                            │
│  ├ Klue-Salesforce → BeyondTrust/LastPass 침해                    │
│  ├ Mastra npm → North Korea attribution                            │
│  └ Polymarket $3M (협력사 침해 경유)                                │
├─────────────────────────────────────────────────────────────────┤
│  축 ③ AI/공식 제품의 공격 표면화                                     │
│  ├ Chrome 149 (12 Critical)                                        │
│  ├ LiteLLM KEV (인증된 모든 사용자 RCE)                              │
│  ├ Flowise/Langflow/n8n/Gemini CLI (CVSS 10.0 다발)                │
│  ├ Amazon Q Developer CVE-2026-12957/12958                          │
│  └ MCP 4대 보안 위험                                                │
└─────────────────────────────────────────────────────────────────┘
```

---

## 4. 🎭 축 ① — 사회공학 + AI 결합 심층 분석

### 4.1 DPRK 클로드+해킹 도구 결합 (6/26 데일리시큐)

| 항목 | 내용 |
|---|---|
| **핵심** | 러시아 공격자가 **Claude + 해킹 도구** 결합으로 호텔 예약 정보 수백만 건 탈취 정황 |
| **발견** | 6/26 데일리시큐 보도 |
| **영향** | 글로벌 호텔 체인 예약 시스템 |
| **귀속** | 러시아 연계 추정 (단정 어려움) |
| **KJ 연결** | KJ-5, KJ-7 |

**킬 체인 분석 (Lockheed)**:

```
[1] Reconnaissance    — 호텔 예약 시스템 공개 자산 스캔
        ↓
[2] Weaponization    — Claude로 취약점 분석 + 익스플로잇 코드 생성
        ↓
[3] Delivery         — 피싱/소셜공학으로 초기 접근
        ↓
[4] Exploitation     — LLM이 생성한 코드로 시스템 침투
        ↓
[5] Installation     — 자격증명 수집 + 백도어 설치
        ↓
[6] C2               — Claude API 호출을 통한 자가 진화형 페이로드
        ↓
[7] Actions          — 호텔 예약 정보 대량 탈취 (수백만 건)
```

**MITRE ATT&CK 매핑**:

| Tactic | Technique | ID |
|---|---|---|
| Initial Access | Phishing | T1566 |
| Execution | LLM-Assisted Code Generation | T1059 (신고 테크닉) |
| Credential Access | Credentials In Databases | T1212 |
| Collection | Data from Information Repositories | T1213 |
| Exfiltration | Exfiltration to Cloud Storage | T1567.002 |

### 4.2 Silver Fox APT — 세무조사 통지서 위장 (6/23)

| 항목 | 내용 |
|---|---|
| **위장** | 세무조사 통지서·세금 체납 고지 |
| **도구** | **ABCDoor** (Python 백도어, 클립보드/실시간 화면 캡처), ValleyRAT, **RustSL Loader** (국가별 실행 제한) |
| **공격 기간** | 2025년 12월 최초 확인 → 2026년 1~2월 **1,600건+ 악성 메일** |
| **표적** | 산업·컨설팅·무역·운송·회계·재무·법무·경영지원 |
| **한국 위험** | 국세청 사칭 가능성 — 이효은 카스퍼스키 코리아 매니저 경고 |
| **권고** | 발신 도메인 검증, 비밀번호 보호 압축파일 의심, EDR + 직원 교육 |

**MITRE ATT&CK 매핑 (Silver Fox 사례)**:

| Tactic | Technique | ID |
|---|---|---|
| Initial Access | Spearphishing Attachment | T1566.001 |
| Execution | User Execution (Malicious File) | T1204.002 |
| Persistence | Boot or Logon Autostart Execution | T1547 |
| Defense Evasion | Software Packing / Virtualization/Sandbox Evasion | T1027 / T1497 |
| Credential Access | Clipboard Data | T1115 |
| Discovery | System Information Discovery | T1082 |
| Collection | Screen Capture | T1113 |
| C2 | Application Layer Protocol (HTTPS) | T1071.001 |

### 4.3 macOS 가스라이트 (6/26 데일리시큐)

| 항목 | 내용 |
|---|---|
| **내용** | **북한 연계 macOS 악성코드 '가스라이트'** — 가짜 오류로 AI 분석 방해 |
| **기술** | 분석가가 디버깅 시 보는 에러 메시지를 위조 → 분석 시간 지연·오판 유도 |
| **MITRE** | Defense Evasion (T1027 Obfuscated Files), T1497 Sandbox Evasion 확장 |
| **한국 위험** | DPRK 산하 조직 추정 (BlueNoroff·Kimsuky) |

### 4.4 축 ① 종합 평가

| 메트릭 | 평가 |
|---|---|
| **AI 활용 범위** | 코드 생성, 사회공학 문안, 합성 페르소나, 분석 방해 |
| **한국 표적 정밀도** | ⭐⭐⭐⭐ (세무조사·신분증·면접 등 도메인 특화) |
| **방어 난이도** | 매우 높음 (AI 합성 콘텐츠는 사람의 가식별 한계 초과) |
| **권고** | EDR + 행동 기반 탐지 + 사용자 교육 + 다중 인증(MFA) + Passkey |

---

## 5. 📦 축 ② — 공급망 공격의 다층화 심층 분석

### 5.1 Shai-Hulud npm → Fortinet Redshift 킬체인 (6/26 Fortinet)

#### 5.1.1 사건 개요

| 항목 | 내용 |
|---|---|
| **사건명** | Shai-Hulud (npm supply chain) + Mastra 침투 |
| **최초 발표** | 6/22 SecurityWeek (Mastra → North Korea) |
| **심화 분석** | 6/26 Fortinet Blogs (Redshift 킬 체인) |
| **2차 피해** | 6/24 BeyondTrust, LastPass (Klue-Salesforce 경유) |
| **귀속** | DPRK 연계 추정 (Fortinet 분석) / ShinyHunters 일부 보도 |

#### 5.1.2 Lockheed Cyber Kill Chain (완전 분석)

```
[1] Reconnaissance  — npm 레지스트리 메타데이터 수집, 의존성 매핑
        ↓
[2] Weaponization  — 악성 npm 패키지 제작 (Mastra 침투, typosquatting)
        ↓
[3] Delivery       — npm publish, dependency confusion
        ↓
[4] Exploitation   — 빌드 타임 코드 실행, post-install hook 악용
        ↓
[5] Installation   — CI/CD 파이프라인 내 foothold (Fortinet 분석: 
                       GitHub Actions self-hosted runner 위험)
        ↓
[6] Command & Control — 자격증명 수집 (cloud metadata, .npmrc, env vars)
        ↓
[7] Actions on Objectives — AWS Redshift 데이터 유출, SaaS CRM 데이터 수집
```

#### 5.1.3 MITRE ATT&CK 매핑 (완전)

| Tactic | Technique | ID | 본 사건 적용 |
|---|---|---|---|
| Initial Access | Supply Chain Compromise | T1195.002 | npm 패키지 침투 |
| Execution | Command and Scripting Interpreter | T1059.007 | post-install script |
| Persistence | Compromise Software Supply Chain | T1195.002 | 의존성 트리 지속 |
| Credential Access | Credentials In Files | T1552.001 | .npmrc, AWS keys |
| Discovery | Cloud Infrastructure Discovery | T1580 | AWS 계정·리소스 탐색 |
| Collection | Data from Cloud Storage | T1530 | Redshift 데이터 수집 |
| Exfiltration | Exfiltration to Cloud Storage | T1567.002 | AWS 외부 업로드 |

#### 5.1.4 Fortinet이 분석한 Persistence 메커니즘

**핵심 통찰**: Shai-Hulud의 가장 큰 특징은 **지속성(Persistence)** 메커니즘의 정교함:

- **CI/CD 환경의 self-hosted runner를 foothold로 활용** — 클라우드에서 가장 신뢰도 높은 자산
- **빌드 캐시와 의존성 lockfile 오염** — 일회성 침투가 아닌 장기 영향
- **GitHub Actions workflow 내부 비밀 노출** — PAT, AWS 액세스 키
- **IAM 권한 자동 수집** — AssumeRole을 통한 횡적 이동

> 단순 npm 침투가 아니라 **"빌드 파이프라인 자체를 credential refinery로 사용"** 하는 새로운 패턴

#### 5.1.5 Sigma 탐지 룰 (실무 적용 가능)

```yaml
title: NPM Post-install Suspicious Execution
id: npm-postinstall-suspicious
status: experimental
description: Detects post-install scripts that spawn child processes or access credentials
logsource:
  category: process_creation
  product: linux
detection:
  selection:
    ParentImage|endswith: 'node'
    ParentCommandLine|contains: 'npm install'
  suspicious_behavior:
    CommandLine|contains:
      - '/.aws/credentials'
      - '/.npmrc'
      - 'curl '
      - 'wget '
      - 'base64 '
  condition: selection AND suspicious_behavior
level: high
```

```yaml
title: GitHub Actions Workflow Unusual Secret Access
id: gh-actions-secret-anomaly
description: Detects anomalous secret access in CI/CD workflows
logsource:
  category: application
  product: github
detection:
  sel_workflow:
    event: 'workflow_run'
  sel_secret_pattern:
    workflow_content|contains:
      - 'secrets.AWS_ACCESS_KEY'
      - 'secrets.GITHUB_TOKEN'
      - 'secrets.NPM_TOKEN'
  condition: sel_workflow AND sel_secret_pattern
level: medium
```

### 5.2 Russian APT StockStay + FortiBleed 캠페인

#### 5.2.1 위협 행위자 프로파일 (Diamond Model)

| 측면 | FortiBleed IAB | StockStay APT |
|---|---|---|
| **Adversary** | Russian Initial Access Broker | Russian APT (Cluster 추정) |
| **Capability** | Fortinet SSL VPN credential theft | SSRF + custom backdoor |
| **Infrastructure** | 러시아·CIS IP, Tor 다층 | 표적별 인프라, geo-fencing |
| **Victim** | 글로벌 Fortinet 고객 | 우크라이나 정부·군사 |

#### 5.2.2 MITRE ATT&CK 매핑

| Tactic | Technique | ID |
|---|---|---|
| Reconnaissance | Scanning IP Blocks | T1595.001 |
| Initial Access | Exploit Public-Facing Application | T1190 |
| Persistence | Create Account | T1136 |
| Defense Evasion | Masquerading | T1036 |
| Credential Access | OS Credential Dumping | T1003 |
| Lateral Movement | Remote Services (RDP/SMB) | T1021 |
| C2 | Application Layer Protocol (HTTPS) | T1071.001 |
| Exfiltration | Encrypted Channel | T1573 |

### 5.3 Polymarket $3M — 협력사 침해 경유 (6/26)

| 항목 | 내용 |
|---|---|
| **피해** | 약 300만 달러 탈취 (피싱 기반) |
| **공격 경로** | 협력사 침해 → Polymarket 사용자 표적 |
| **KJ 연결** | KJ-1 (공급망 다층화) |
| **한국 영향** | 국내 거래소도 협력사 보안 점검 필요 |

### 5.4 축 ② 종합 평가

| 메트릭 | 평가 |
|---|---|
| **공급망 단계** | 다층화 (소프트웨어 → 서비스 → 협력사) |
| **한국 표적** | ⭐⭐⭐ (BeyondTrust, LastPass 등 보안 도구 벤더 영향) |
| **즉시 위험** | npm 의존성, CI/CD 자격증명, SaaS OAuth 토큰 |
| **권고** | npm audit + 의존성 트리 점검, CI/CD 자격증명 rotation, OIDC 분리, SBOM 도입 |

---

## 6. 🤖 축 ③ — AI/공식 제품의 공격 표면화 심층 분석

### 6.1 아마존 큐(Amazon Q) 개발자 취약점 — 신규 발견 (6/27)

#### 6.1.1 사건 개요

| 항목 | 내용 |
|---|---|
| **CVE** | **CVE-2026-12957** (자동 명령 실행), **CVE-2026-12958** (심볼릭 링크) |
| **발견** | 2026-04-20 Wiz 보고 |
| **AWS 패치** | 5월 12일 (언어 서버 1.69.0) |
| **권고 공개** | 6월 23일 |
| **현재 상태** | **방금 수집되어 현재 unread 1건** (DB #438, 데일리시큐 207340) |

#### 6.1.2 공격 메커니즘

```
1. 공격자 → 조작된 저장소 생성 (정상 프로젝트 위장)
        ↓
2. 개발자 → 프로젝트를 IDE에서 열기 (단순한 clone만으로)
        ↓
3. 아마존 큐 개발자 → 설정 파일 자동 처리 (검증 부족)
        ↓
4. 백그라운드에서 자동 명령 실행
        ↓
5. AWS 세션 정보, 환경 변수 API 키 외부 전송
```

#### 6.1.3 탈취 가능 정보

| 대상 | 위험 |
|---|---|
| AWS CLI 인증정보 | ⭐⭐⭐⭐⭐ |
| 클라우드 토큰 | ⭐⭐⭐⭐⭐ |
| GitHub 토큰 | ⭐⭐⭐⭐ |
| 데이터베이스 접속 정보 | ⭐⭐⭐⭐ |
| 환경 변수 모든 자격증명 | ⭐⭐⭐⭐⭐ |

#### 6.1.4 MITRE ATT&CK 매핑

| Tactic | Technique | ID |
|---|---|---|
| Initial Access | Supply Chain Compromise | T1195 |
| Execution | User Execution (Malicious File in Repo) | T1204.002 |
| Credential Access | Credentials in Environment Variables | T1552.005 |
| Collection | Data from Local System | T1005 |
| Exfiltration | Exfiltration Over C2 Channel | T1041 |

#### 6.1.5 패치 적용 대상

- **언어 서버 1.69.0** 이상 필수
- 플러그인: VS Code, JetBrains, Eclipse, Visual Studio
- **자동 업데이트 차단 환경에서는 수동 업그레이드 필요**

### 6.2 LiteLLM KEV 등재 (CVE-2026-42271)

| 항목 | 내용 |
|---|---|
| **KEV 등재일** | 6/8 |
| **CVSS** | 9.9 (추정) |
| **영향** | 모든 인증된 사용자 → RCE 가능 |
| **한국 위험** | 사내 LLM 도구 도입 조직 |
| **권고** | 즉시 버전 확인 + 업데이트 |

### 6.3 Chrome 149 (6/25) — 18개 심각 취약점

| 항목 | 값 |
|---|---|
| **버전** | 149.0.7827.53 |
| **Critical (CVSS 9.0+)** | 6건 |
| **CVE-2026-11645 KEV** | V8 OOB R/W → RCE |
| **권고** | 전사 PC/모바일 즉시 업데이트 |

### 6.4 AI 워크플로우 6월 누계 CVSS 9.9~10.0

| CVE | 제품 | CVSS | CWE |
|---|---|---|---|
| CVE-2026-10561 | IBM Langflow OSS 1.0.0~1.9.3 | 10.0 | CWE-94 |
| CVE-2026-54309 | n8n MCP HTTP transport | 10.0 | CWE-306 |
| CVE-2026-55255 | Langflow < 1.9.2 | 9.9 | CWE-639 |
| CVE-2026-56274 | Flowise < 3.1.2 | 9.9 | CWE-78 |
| CVE-2026-46442 | Flowise 3.1.2 미만 | 9.9 | CWE-94 |
| CVE-2026-12957 | **Amazon Q Developer** (신규) | — | — |

### 6.5 MCP (Model Context Protocol) 4대 보안 위험

| 위험 | 설명 |
|---|---|
| **Tool Poisoning** | MCP 서버 tool description에 악성 지시문 삽입 |
| **Indirect Prompt Injection** | AI 모델이 외부 콘텐츠에 의도치 않은 지시를 따름 |
| **Token Theft** | OAuth 토큰 누출 |
| **Privilege Escalation** | 한 tool의 권한이 다른 tool로 전파 |

### 6.6 축 ③ 종합 평가

| 메트릭 | 평가 |
|---|---|
| **AI 도구 위험도** | ⭐⭐⭐⭐⭐ (공식 제품 + 워크플로우 도구) |
| **공급망 위험** | ⭐⭐⭐⭐ (Amazon Q 사건이 대표) |
| **즉시 위험** | AI 도구 사용 조직의 클라우드 자격증명 |
| **권고** | AI 도구 버전 최신화, 클라우드 자격증명 rotation, EDR 강화, AI 도구 사용 정책 수립 |

---

## 7. 🇰🇷 한국 특수 정황 분석

### 7.1 아리스팅어 봇넷 (6/22 데일리시큐)

| 항목 | 값 |
|---|---|
| **표적** | D-Link 구형 공유기 (특히 DIR-850L 75%, DIR-818LW 13%) |
| **한국 감염률** | **48.45%** (전 세계 1위, 4,300대 중) |
| **CVE** | CVE-2013-3307, CVE-2016-5681, CVE-2025-11837 |
| **용도** | 정찰·프록시·트래픽 우회 (DDoS 아님) |
| **심각 기능** | DNS 변조, 트래픽 감시, Dropbear SSH 설치 |
| **NAS 변종** | Go 언어, Fscan·Ksubdomain·Httpx·Tlsx 결합 |
| **공격자** | 미확인 (코드 내 '2024' 문자열만) |
| **권고** | EoL 공유기 인터넷 분리 + 교체 |

**MITRE ATT&CK 매핑**:

| Tactic | Technique | ID |
|---|---|---|
| Resource Development | Acquire Infrastructure (Routers) | T1583 |
| Initial Access | Exploit Public-Facing Application | T1190 |
| Execution | Unix Shell | T1059.004 |
| Persistence | Implant Internal Image | T1547 |
| Defense Evasion | Masquerading (Normal Traffic) | T1036 |
| Credential Access | Network Sniffing | T1040 |

### 7.2 Silver Fox + DPRK 클로드 + macOS 가스라이트 종합

| 위협 행위자 | 표적 | 도구 |
|---|---|---|
| Silver Fox (중국 연계 추정) | 한국 기업 재무/회계 | ABCDoor + ValleyRAT |
| DPRK 클로드 공격자 | 글로벌 호텔 (한국 연관) | LLM-Assisted Exploit |
| DPRK macOS 가스라이트 | 분석가 워크스테이션 | 분석 방해 트로이목마 |
| Russian 클로드 공격자 | 글로벌 호텔 예약 시스템 | Claude API + 해킹 도구 |

### 7.3 국내 정책/규제 동향 (6/22~27)

| 일자 | 내용 | 의미 |
|---|---|---|
| 06-26 | 개인정보위, 빗썸 과징금 **2억 1천만 원** | 가상자산 거래소 국외이전 규정 |
| 06-26 | 개인정보위, 상조업계 시정권고 | 시장점유율 70% 3사 점검 |
| 06-26 | 그룹아이비, 2026년 상위 10대 사이버 위협 조직 공개 | 위협 인텔 공개 |
| 06-23 | 엑스게이트, 자체 웹사이트 PQC 적용 | 국내 PQC 도입 초기 사례 |
| 06-23 | 키페어, 금융권 PQC 전환 전략 | 양자내성 표준 |
| 06-25 | KISA, 협력업체 상생 간담회 (120개 기업) | 공급망 협력 |

---

## 8. 📊 6월 4주차 vs 그 이전 — 질적 변화 비교표

> CTI 보고서의 핵심 설계 원칙인 **"전(前) → 현재 → 전망" 비교**를 이번 주에 적용합니다.

### 8.1 위협 행위자 활동 양상 비교

| 차원 | 2024년 이전 | 2025년 (AI 보조) | 2026년 6월 (자율화) |
|---|---|---|---|
| **AI 활용** | 미사용/실험 | 피싱 문안·번역·vibe coding 보조 | **공격 수명주기 자율 실행 + LLM 내장형 멀웨어** |
| **사회공학** | 수작업 스피어피싱 (맞춤법·문화 오류) | AI 문안 교정으로 진정성↑ | **딥페이크 신분증·영상, 합성 페르소나** |
| **공급망** | 단일 패키지 표적 (SolarWinds·CCleaner) | 다중 패키지 (3월 Axios npm) | **다층화** (소프트웨어 → 서비스 → 협력사 → 데이터) |
| **공식 제품** | 주기적 패치 사이클 | 제로데이 조기 악용 (예: MOVEit) | **AI 도구 + 공식 제품** 동시 표면화 (Chrome 12 Critical, LiteLLM KEV, Amazon Q) |
| **국가 APT** | 전통적 APT (Turla·APT29) | 암호화폐 탈취 확대 | **AI 통합** (DPRK 클로드, Russian 클로드) |

### 8.2 이번 주 사건별 비교 (구체)

| 사건 | 6월 초 (W1~W3) | 6월 말 (W4, 6/22~27) | 변화 |
|---|---|---|---|
| LiteLLM | 발표 예정 | **KEV 등재** (6/8) | 실전 악용 확인 |
| Chrome | 148 사이클 (12 Critical) | **149 사이클** (6/25) | 매월 Critical 10+ 유지 |
| Shai-Hulud | - | **Fortinet Redshift 킬체인 공개** (6/26) | 지속성 메커니즘 정교화 |
| FortiBleed | NCSC 경고 (6/18) | **Russian IAB 배후 공개** (6/22~26) | 단일 클러스터 배후 식별 |
| 양자내성 | CISA New Directive (6/10) | **美 행정명령 (6/23)** + 한국 엑스게이트 | 정책→실행 전환 |
| 아리스팅어 | - | **한국 48.45% 감염** (6/22) | 신규 IoT 봇넷 등장 |

---

## 9. 🛡️ 위협 행위자 매트릭스 (Diamond Model)

| 행위자 | 1차 공격 | 2차 활용 | 표적 지역 | 6월 강도 |
|---|---|---|---|---|
| Russian IAB | VPN/Firewall 결함 | Credential theft | 글로벌 | ★★★★★ |
| Russian APT (StockStay) | SSRF/백도어 | 우크라이나 표적 | 동유럽 | ★★★★ |
| North Korea (Lazarus·Mastral) | npm 침투 | 공급망 확산 | 글로벌 | ★★★★ |
| North Korea (BlueNoroff) | AI 딥페이크 영상 | 암호화폐 표적 | 글로벌 | ★★★★ |
| Chinese (Silver Fox 추정) | Spear phishing | 기업 표적 | 동아시아 | ★★★ |
| ShinyHunters | Salesforce/CRM | 다중 2차 피해 | 글로벌 | ★★★★ |
| Infostealer 그룹 | Credential dump | Credential stuffing | 글로벌 | ★★★ |

---

## 10. 🔮 7월 예측 — 다음 주 핵심 모니터링 포인트

| # | 포인트 | 시사점 |
|---|---|---|
| 1 | **아마존 큐 패치 미적용 조직의 AWS 자격증명 탈취** | 6/23 권고 후 2주 → 미적용 조직 표적 |
| 2 | **PTC Windchill 익스플로잇 확대** | 첫 사례 후 PoC 공개 가능성 |
| 3 | **Russian APT StockStay 후속** | 추가 백도어·표적 확대 |
| 4 | **Asian Scam Centers 단속 후속** | 검거·추가 압박 정보 |
| 5 | **양자내성 정책 후속** | 한국 정부/공공/금융 동향 |
| 6 | **AI 워크플로우 도구 추가 CVE** | 6월 패턴 지속 시 7월에도 다발 |
| 7 | **공급망 2차 피해 확대** | Klue/Salesforce 영향권 추가 |
| 8 | **DPRK IT 워커 AI 자동화** | Anthropic 보고 후속 — Fortune 500 침투 사례 |
| 9 | **클로드+해킹 도구 결합 패턴 확산** | DPRK 외 중국·이란·러시아 확장 |
| 10 | **아리스팅어 봇넷 대응** | 한국 가정/원격근무 공유기 점검 |

---

## 11. ✅ 운영 권고 (Operational Recommendations)

### 11.1 즉시 (24시간 이내) — P0

| 우선순위 | 액션 | 대상 |
|---|---|---|
| 🔴 P0 | **Chrome 149.0.7827.53 이상** 업데이트 | 전사 엔드포인트 |
| 🔴 P0 | **Amazon Q Developer 1.69.0 이상** 업데이트 | VS Code/IDE 사용자 |
| 🔴 P0 | npm 의존성 audit + CI/CD 자격증명 rotation | DevSecOps |
| 🔴 P0 | Salesforce/CRM 3rd-party OAuth token rotation | SaaS 운영 |
| 🔴 P0 | LiteLLM / Langflow / Flowise / n8n 버전 점검 | AI 도구 사용자 조직 |
| 🔴 P0 | Fortinet Firewall 펌웨어 최신화 + 침해 흔적 점검 | Fortinet 운영 |

### 11.2 단기 (1~2주) — P1

| 우선순위 | 액션 | 영향 |
|---|---|---|
| 🟠 P1 | PTC Windchill/FlexPLM 패치 적용 | 제조·엔지니어링 |
| 🟠 P1 | Galaxy 단말 OS 업데이트 | 모바일 엔드포인트 |
| 🟠 P1 | Apple iOS/iPadOS 최신 패치 | iOS 디바이스 |
| 🟠 P1 | FFmpeg 업데이트 (media server/NAS) | 멀티미디어 |
| 🟠 P1 | credential dump 매칭 — credential reuse 점검 | IAM |
| 🟠 P1 | **D-Link DIR-850L/DIR-818LW 교체 또는 인터넷 분리** | 국내 가정/원격근무 |

### 11.3 중기 (1~3개월) — P2

| 우선순위 | 액션 |
|---|---|
| 🟡 P2 | 양자내성암호(PQC) 전환 로드맵 수립 — NIST ML-KEM/ML-DSA 표준 |
| 🟡 P2 | AI 도구 사용 정책 + 거버넌스 체계 수립 |
| 🟡 P2 | PLM 시스템을 IT 자산 인벤토리/취약점 스캔에 포함 |
| 🟡 P2 | SBOM(Software Bill of Materials) 도입 |
| 🟡 P2 | 클라우드 자격증명 rotation 자동화 (90일 주기) |

### 11.4 장기 (6~12개월) — P3

| 우선순위 | 액션 |
|---|---|
| 🟢 P3 | 양자내성 KMS/HSM 도입 검토 |
| 🟢 P3 | 자산 가시성(Asset Visibility) 통합 플랫폼 |
| 🟢 P3 | AI 에이전트 워크플로우 별도 보안 정책 |
| 🟢 P3 | APT 표적 모니터링 — DPRK·Russian·Chinese |
| 🟢 P3 | 공급망 위험 관리(SCRM) 프로그램 정착 |

---

## 12. 🔬 분석 한계 및 주의사항

| 항목 | 설명 |
|---|---|
| **귀속 불확실성** | Russian APT, ShinyHunters/DPRK, 클로드+해킹 도구 공격자 등 출처별 차이 |
| **MITRE ATT&CK 매핑** | 공개 출처 기반 추정이므로 조직 환경 정밀 분석 권장 |
| **NVD 누계 통계** | 6/26 시점 기준, 6/27~30 추가 발표분은 미포함 |
| **국내 위협 동향** | 데일리시큐 + KISA RSS만 수집 — 보안뉴스, ZDNet Korea 등 미수집분 별도 조회 필요 |
| **아마존 큐 분석** | 방금 수집된 1건 기사 기반 — 더 깊은 분석은 CVE-2026-12957/12958 원본 필요 |
| **실제 악용 통계** | 대부분 CISA KEV 등재 기준 — 공개되지 않은 0-day는 미반영 |

---

## 13. 📚 참고 자료

### 13.1 외부 공개 출처 (Global)

#### 공급망 / Shai-Hulud
- https://feeds.fortinet.com/~/958459373/0/fortinet/blogs~From-CICD-to-Cloud-Data-How-Shai-Hulud-Persistence-Leads-to-Redshift-Breach
- https://www.securityweek.com/north-korean-hackers-blamed-for-mastra-npm-supply-chain-attack/
- https://www.securityweek.com/beyondtrust-lastpass-impacted-by-klue-salesforce-incident/

#### Russian APT / FortiBleed
- https://www.securityweek.com/russian-apt-deploys-stockstay-backdoor-against-ukrainian-targets/
- https://www.darkreading.com/cyberattacks-data-breaches/fortibleed-attackers-firewalls-credentials-stealers
- https://www.securityweek.com/russian-initial-access-broker-behind-fortibleed-campaign/

#### Chrome / Chromium
- https://www.securityweek.com/chrome-149-update-resolves-18-severe-vulnerabilities/

#### AI / MCP / 정책
- https://www.securityweek.com/new-enterprise-ready-mcp-specification-brings-new-security-challenges/
- https://www.securityweek.com/trump-signs-executive-order-accelerating-post-quantum-cryptography-migration/
- https://blog.cloudflare.com/post-quantum-eo-2026/
- https://www.ncsc.gov.uk/news/the-ai-shift-in-cyber-risk-why-leaders-must-act-now

#### 레거시 취약점
- https://www.securityweek.com/first-ever-exploitation-of-ptc-windchill-vulnerability-discovered-in-the-wild/
- https://www.securityweek.com/decades-old-squid-proxy-flaw-squidbleed-can-expose-user-data/
- https://www.securityweek.com/eight-year-old-samsung-knox-flaw-exposed-millions-of-galaxy-devices-to-kernel-attacks/
- https://www.securityweek.com/new-exploit-bypasses-apples-boot-defenses-affects-millions-of-iphones/
- https://www.securityweek.com/ffmpeg-pixelsmash-flaw-allows-rce-on-video-players-media-servers-nas-appliances/

#### Amazon Q Developer
- https://www.dailysecu.com/news/articleView.html?idxno=207340

### 13.2 국내 매체 (데일리시큐)

- https://www.dailysecu.com/news/articleView.html?idxno=207266 (아리스팅어)
- https://www.dailysecu.com/news/articleView.html?idxno=207270 (Silver Fox)
- https://www.dailysecu.com/news/articleView.html?idxno=207268 (240억 credential dump)
- https://www.dailysecu.com/news/articleView.html?idxno=207334 (빗썸 과징금)
- https://www.dailysecu.com/news/articleView.html?idxno=207333 (상조업계 점검)
- https://www.dailysecu.com/news/articleView.html?idxno=207321 (macOS 가스라이트)
- https://www.dailysecu.com/news/articleView.html?idxno=207322 (메모리 미스틱)
- https://www.dailysecu.com/news/articleView.html?idxno=207338 (DirtyClone)
- https://www.dailysecu.com/news/articleView.html?idxno=207339 (Polymarket)
- https://www.dailysecu.com/news/articleView.html?idxno=207306 (Cisco SD-WAN)
- https://www.dailysecu.com/news/articleView.html?idxno=207277 (엑스게이트 PQC)
- https://www.dailysecu.com/news/articleView.html?idxno=207291 (트럼프 PQC EO)

### 13.3 공식 출처

- CISA KEV: https://www.cisa.gov/known-exploited-vulnerabilities-catalog
- NVD: https://nvd.nist.gov/
- MITRE ATT&CK: https://attack.mitre.org/
- NIST PQC: https://csrc.nist.gov/projects/post-quantum-cryptography
- Wiz (Amazon Q 분석): https://www.wiz.io/

### 13.4 본 보고서 family

| 파일 | 형식 | 분량 |
|---|---|---|
| `weekly-newsletter-20260622-20260626.md` | 표준 뉴스레터 | 19.4 KB |
| `weekly-trend-report-20260622-20260626.md` | 분석 보고서 (요약) | 19.6 KB |
| `weekly-deep-analysis-report-20260622-20260626.md` | **v1 심층 분석** | 36.3 KB |
| **`weekly-deep-analysis-report-20260622-20260626-v2.md`** | **v2 심층 분석 (본 문서)** | **현재** |
| `monthly-trend-report-202606.md` | 6월 종합 | 22.7 KB |
| `cve-newly-discovered-202606.md` | CVE 누계 통계 | 11.0 KB |

### 13.5 참고한 외부 보고서 구조

- [CTI-2026-0628-DPRK-AI (Dennis Kim)](https://github.com/gameworkerkim/CYBER-THREAT-INTELLIGENCE-REPORT/blob/main/CTI-2026-0628-DPRK-AI.md) — KJ(Key Judgment) + 3축 프레임워크 + MITRE ATT&CK + 질적 변화 비교표 구조 차용

---

## 14. 메타데이터

| 항목 | 값 |
|---|---|
| **작성** | 2026-06-27 (KST) |
| **데이터 cutoff** | 2026-06-27 13:50 KST |
| **분석 범위** | 2026-06-22 ~ 2026-06-27 (6일) |
| **분량** | 약 32 KB |
| **v2 개선 사항** | (1) KJ 시스템 도입 (7개 핵심 판단 + 신뢰도) (2) 3축 프레임워크 (사회공학/공급망/AI 표면화) (3) MITRE ATT&CK 완전 매핑 (4) 질적 변화 비교표 (5) Diamond Model (6) Amazon Q Developer 사건 신규 통합 |

### v1 → v2 핵심 개선

| 차원 | v1 | v2 |
|---|---|---|
| **신뢰도 표시** | 없음 | KJ별 High/Medium-High/Medium |
| **프레임워크** | 8개 IU (사건 단위) | **3대 축** (유형별) + KJ 7개 |
| **MITRE ATT&CK** | 일부 사건만 | **모든 사건 완전 매핑** |
| **비교 시각화** | 카테고리별 | **질적 변화 비교표** (전→현재→전망) |
| **귀속 불확실성** | 단순 추정 | **단정 금지 원칙 명시** (KJ-7) |
| **AI 위협 심층** | LiteLLM/LangFlow 나열 | **아마존 큐 CVE-2026-12957/12958 신규 통합** |
| **한국 특수** | 개별 사건 | **아리스팅어 48.45% + Silver Fox + DPRK 클로드 + 가스라이트 종합** |

---

> **본 보고서는 표준 CTI 보고서 구조를 차용한 v2 고도화 버전입니다.** 매주 진화하는 위협 환경에 맞춰 KJ 시스템, 3축 프레임워크, MITRE ATT&CK 매핑, 비교표가 일관되게 적용됩니다. 다음 주(v3)에는 더 많은 분석 대상과 자동화 통합을 검토합니다.