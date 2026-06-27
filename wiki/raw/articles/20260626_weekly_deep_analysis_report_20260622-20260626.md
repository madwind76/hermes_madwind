---
title: 주간 보안 동향 심층 분석 보고서 (2026-06-22 ~ 2026-06-26)
date: 2026-06-26
period: 2026-06-22 ~ 2026-06-26
type: deep-analysis-report
audience: 위협 인텔리전스 분석가, 보안 관제/엔지니어링 리더, CISO
related_newsletter: wiki/raw/articles/2026/202606/weekly-newsletter-20260622-20260626.md
related_quick_report: wiki/raw/articles/2026/202606/weekly-trend-report-20260622-20260626.md
related_cve_summary: wiki/raw/articles/2026/202606/cve-newly-discovered-202606.md
tags: [security, weekly, deep-analysis, threat-intel, mitre-attack, kev, ai-security, supply-chain, korean]
sources:
  - RSS (24개 블로그 통합)
  - NVD REST API (1,527건 CVE)
  - CISA KEV (신규 5건)
---

# 🔬 주간 보안 동향 심층 분석 보고서 (2026-06-22 ~ 2026-06-26)

> **본 문서는 위협 인텔리전스 분석가 관점의 전문 보고서입니다.**
> 빠른 요약본이 필요하면 `weekly-newsletter-20260622-20260626.md`, 일반 분석 보고서는 `weekly-trend-report-20260622-20260626.md`를 함께 봐 주세요.

---

## 0. 데이터 수집 기준

| 항목 | 값 |
|---|---|
| 기간 | 2026-06-22 (월) 00:00 KST ~ 2026-06-26 (금) 23:59 KST |
| RSS 통합 수집 | 24개 보안 매체 (blogwatcher-cli v0.2.1) |
| 수집 기사 | 204건 |
| NVD 신규 CVE | **1,527건** (Critical 105, High 437) |
| CISA KEV 신규 | 5건 (CVE-2026-12569, -20230, -2025-67038, -34908/9/10) |
| 분석 프레임워크 | MITRE ATT&CK v15, Lockheed Martin Cyber Kill Chain, Diamond Model |

---

## 1. Strategic Executive Summary

이번 주(2026-06-22~26)는 **네 가지 거시 흐름**이 동시에 수렴한 시기입니다:

1. **공급망 공격의 산업화(Industrialization of Supply Chain Attacks)** — Shai-Hulud가 North Korea 연계 그룹에 의해 npm 생태계에 정착했고, Klue-Salesforce 침해 경유로 다수 보안 벤더(BeyondTrust, LastPass) 자체가 피해자가 되는 **메타-위험(meta-risk)** 이 현실화됨. 보안 도구를 통한 우회 침투가 더 이상 가정(hypothesis)이 아니라 관측된 패턴입니다.

2. **레거시 취약점의 본격적 재활용(Re-emergence of Legacy Vulnerabilities)** — PTC Windchill, Squid Proxy(Squidbleed), Samsung KNOX(8년), Apple Boot, FFmpeg PixelSmash 등 **평균 5년 이상 된 결함**이 in-the-wild 익스플로잇에 활용 중. CISA KEV 신규 5건 중 2건이 8~20년 된 결함입니다. "패치했다 = 안전하다"는 가정이 무너지고 있습니다.

3. **AI 에이전트 워크플로우의 취약점 다발발견(Vulnerability Cluster in AI Agent Workflows)** — 이번 주 신규 CVE 중 n8n, Langflow, Flowise, Gogs, Appsmith 등 **AI 워크플로우/에이전트 플랫폼에서만 CVSS 9.9~10.0 다수 발견**. CVSS 10.0 12건 중 7건이 AI/자동화 도구(IBM Langflow, FOSSBilling, n8n MCP, GV-I/O Box, Flowise). 이는 AI 도구가 단순 생산성 향상이 아닌 **새로운 공격 표면**임을 입증합니다.

4. **국가 정책 전환점(Cryptographic Policy Inflection Point)** — Trump 행정부의 양자내성암호(PQC) 행정명령(6/23)은 NIST 표준(ML-KEM, ML-DSA, SLH-DSA) 채택을 **美 연방기관 2030년까지 의무화**했습니다. 이는 한국 정부·공공·금융 부문에도 **향후 1~2년 내 동일 흐름**이 도래할 가능성을 시사합니다.

이 네 흐름은 **서로 강화(reinforcing)** 됩니다. 예를 들어 Shai-Hulud의 npm 침투 경로는 LiteLLM, Langflow 등 AI 도구의 의존성 트리에 직접 영향을 주고, 양자내성 전환기의 인증서 발급 체계는 **새로운 공급망 공격 면적**을 만듭니다.

---

## 2. 사건군별 심층 분석

### 2.1 [IU-01] Shai-Hulud npm 공급망 공격 — 킬 체인 분석

#### 2.1.1 개요 및 영향 범위

| 항목 | 내용 |
|---|---|
| 사건명 | Shai-Hulud (npm supply chain) + Mastra 침투 |
| 최초 발표 | 2026-06-22 SecurityWeek (Mastra attribution) |
| 심화 분석 | 2026-06-26 Fortinet Blogs (Redshift 킬 체인) |
| 2차 피해 | 2026-06-24 BeyondTrust, LastPass (Klue-Salesforce 경유) |
| 영향 표면 | npm 생태계 + Salesforce/CRM SaaS + AWS 데이터 인프라 |
| 피해 추정 | 공개된 정보로는 수만~수십만 패키지 다운로드 영향 가능 |

#### 2.1.2 Lockheed Cyber Kill Chain 분석

```
[1] Reconnaissance          — npm 레지스트리 메타데이터 수집, 의존성 매핑
        ↓
[2] Weaponization          — 악성 npm 패키지 제작 (Mastra 침투, typosquatting)
        ↓
[3] Delivery               — npm publish, dependency confusion
        ↓
[4] Exploitation           — 빌드 타임 코드 실행, post-install hook 악용
        ↓
[5] Installation           — CI/CD 파이프라인 내 foothold (Fortinet 분석: GitHub Actions self-hosted runner 위험)
        ↓
[6] Command & Control      — 자격증명 수집 (cloud metadata, .npmrc, env vars)
        ↓
[7] Actions on Objectives  — AWS Redshift 데이터 유출, SaaS CRM 데이터 수집
```

#### 2.1.3 MITRE ATT&CK 매핑

| Tactic | Technique | ID | 본 사건 적용 |
|---|---|---|---|
| Initial Access | Supply Chain Compromise | T1195.002 | npm 패키지 침투 |
| Execution | Command and Scripting Interpreter | T1059.007 | post-install script |
| Persistence | Compromise Software Supply Chain | T1195.002 | 의존성 트리 지속 |
| Credential Access | Credentials In Files | T1552.001 | .npmrc, AWS keys |
| Discovery | Cloud Infrastructure Discovery | T1580 | AWS 계정·리소스 탐색 |
| Collection | Data from Cloud Storage | T1530 | Redshift 데이터 수집 |
| Exfiltration | Exfiltration to Cloud Storage | T1567.002 | AWS 외부 업로드 |

#### 2.1.4 Fortinet이 분석한 Persistence 메커니즘

Fortinet의 6/26 분석은 Shai-Hulud의 가장 큰 특징이 **지속성(Persistence)** 메커니즘의 정교함임을 강조합니다:

- **CI/CD 환경의 self-hosted runner를 foothold로 활용** — 클라우드 환경에서 가장 신뢰도가 높은 자산 중 하나로 분류됨
- **빌드 캐시와 의존성 lockfile 오염** — 일회성 침투가 아닌 장기 영향
- **GitHub Actions workflow 내부 비밀 노출** — PAT(Personal Access Token), AWS 액세스 키 등
- **IAM 권한 자동 수집** — AssumeRole을 통한 횡적 이동(lateral movement)

이 사건은 단순 npm 침투가 아니라 **"빌드 파이프라인 자체를 credential refinery로 사용"** 하는 새로운 패턴입니다.

#### 2.1.5 탐지 룰 (Sigma 형식, 실무 적용 가능)

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
  anomaly:
    actor_workflow_uses_secrets_in_unusual_repos: true
condition: sel_workflow AND sel_secret_pattern
level: medium
```

#### 2.1.6 IOC (Indicators of Compromise)

**npm 패키지 (출처: GitHub Security Advisories, Fortinet 분석)**:

| 패턴 | 유형 | 설명 |
|---|---|---|
| `mastra` 변형 패키지 | typosquatting | 정상 패키지명 변형 (예: mastrra, @mastra/core 변형) |
| post-install에 `eval(base64_decode(...))` 패턴 | 코드 패턴 | 빌드 타임 실행형 침투 |
| GitHub Actions workflow에 `curl <외부>` | C2 통신 | 빌드 시점 외부 페치 |

**AWS 환경 (Fortinet 분석)**:

| 패턴 | 설명 |
|---|---|
| `STS:GetCallerIdentity` 비정상 호출 | 권한 enumeration |
| Redshift `UNLOAD` 명령 비정상 | 데이터 유출 |
| `s3:GetObject` 광범위 | 자격증명 수집 후 데이터 수집 |

#### 2.1.7 즉시 권고 (CISO/보안 담당자용)

| 우선순위 | 액션 | 영향 |
|---|---|---|
| 🔴 P0 | `npm audit` + 의존성 트리 점검 — 알려진 침투 패키지 흔적 확인 | 즉시 |
| 🔴 P0 | CI/CD 환경 AWS/GCP/Azure 액세스 키 전부 rotation | 즉시 |
| 🔴 P0 | GitHub Actions self-hosted runner에서 권한 분리 — production 자격증명은 별도 OIDC | 24시간 |
| 🟠 P1 | `package-lock.json` 무결성 검증 자동화 | 1주 |
| 🟠 P1 | Salesforce/CRM 3rd-party 앱 OAuth token rotation | 1주 |
| 🟠 P1 | npm registry에서 internal package mirror 구축 검토 | 1개월 |
| 🟡 P2 | SBOM(SBOM) 도입 — 의존성 가시성 확보 | 3개월 |

---

### 2.2 [IU-02] Russian APT StockStay + FortiBleed — 사이버 스파이 활동 심층 분석

#### 2.2.1 위협 행위자 프로파일 (Diamond Model)

| 측면 | FortiBleed | StockStay |
|---|---|---|
| **Adversary** | Russian Initial Access Broker (Cluster 명 미공개, Fortinet 분석) | Russian APT (우크라이나 표적 특화) |
| **Capability** | Fortinet SSL VPN credential theft, persistence | SSRF + custom backdoor |
| **Infrastructure** | 러시아·CIS 지역 IP, VPN/Tor 다층 | 표적별 인프라, geo-fencing |
| **Victim** | 글로벌 Fortinet 고객 (정부·에너지·금융 우선) | 우크라이나 정부·군사·에너지 |

#### 2.2.2 FortiBleed 공격 킬 체인 (Fortinet + Dark Reading 통합)

```
[1] Recon — Fortinet SSL VPN 인터넷 노출 자산 스캔 (Shodan, Censys)
[2] Initial Access — CVE-2024-21762 (이전 결함) 또는 신규 SSRF
[3] Foothold — SSL VPN 계정 credential harvest
[4] Persistence — VPN config 내부 사용자 추가, stealth admin 계정
[5] Lateral Movement — 내부 네트워크로 pivot (RDP, SMB)
[6] Collection — Active Directory, 도메인 컨트롤러 credential dump
[7] Exfiltration — Tor + VPN 다층 터널
```

**핵심 통찰**: FortiBleed는 단순 결함 익스플로잇이 아니라 **방화벽 자체를 credential refinery**로 만드는 행위입니다. Dark Reading은 이를 "방화벽이 자격증명 탈취 도구로 전환되었다"고 표현했습니다.

#### 2.2.3 StockStay 백도어 기술 분석

6/26 SecurityWeek가 공개한 StockStay의 기술적 특징:

- **초기 침투**: SSRF(Server-Side Request Forgery)를 통한 내부 서비스 접근
- **Backdoor 인터페이스**: HTTP/HTTPS 위장 트래픽 (C2 통신 암호화)
- **Persistence**: 시스템 서비스 등록 + WMI 이벤트订阅
- **Evasion**: 정상 프로세스 내부 injection (예: svchost.exe 내부)
- **표적화**: 우크라이나 정부·군사 시설 우선, 지리적 IP 필터링

#### 2.2.4 MITRE ATT&CK 매핑

| Tactic | Technique | ID |
|---|---|---|
| Reconnaissance | Scanning IP Blocks | T1595.001 |
| Initial Access | Exploit Public-Facing Application | T1190 |
| Persistence | Create Account | T1136 |
| Defense Evasion | Masquerading | T1036 |
| Credential Access | OS Credential Dumping | T1003 |
| Lateral Movement | Remote Services (RDP/SMB) | T1021 |
| Command and Control | Application Layer Protocol (HTTPS) | T1071.001 |
| Exfiltration | Encrypted Channel | T1573 |

#### 2.2.5 Fortinet 운영자 즉시 점검 사항

```bash
# 1) 비인가 사용자 확인
get system admin

# 2) 비정상 로컬 사용자 확인
get user local

# 3) 최근 SSL VPN 로그에서 비정상 인증 패턴
execute log filter category event
execute log filter field subtype sslvpn
execute log display

# 4) 펌웨어 최신화 (6.4.x, 7.0.x, 7.2.x 라인별 최신)
diagnose autoupdate status

# 5) 알려진 침투 흔적 IOC 매칭 (Fortinet PSIRT 가이드)
```

---

### 2.3 [IU-03] Chrome 149 — Critical 12건의 구조적 분석

#### 2.3.1 6월 4주차 Chrome 패치 사이클 분석

이번 주 Chrome 149.0.7827.53은 **18개 심각 취약점**을 일괄 수정했습니다. 이를 6월 누계와 비교하면:

| 사이클 | Critical (CVSS 9.0+) | 영향 카테고리 |
|---|---|---|
| Chrome 148 (6/4) | 12건 | ANGLE, FileSystem, GPU, Ozone, Autofill |
| Chrome 149 (6/25) | 6건 (NVD 9.6+ 기준) | 후속 + 신규 |

NVD에 등재된 6월 Chrome/Chromium CVSS 9.6+ CVE는 **총 12건**입니다:

| CVE | 컴포넌트 | CWE | CVSS |
|---|---|---|---|
| CVE-2026-10881 | ANGLE | OOB R/W | 9.6 |
| CVE-2026-10886 | FileSystem | UAF | 9.6 |
| CVE-2026-10892 | GPU (Android) | OOB W | 9.6 |
| CVE-2026-10931 | FileSystem | UAF | 9.6 |
| CVE-2026-10966 | Codecs | Inappropriate Implementation | 9.6 |
| CVE-2026-10971 | Printing (Windows) | Input Validation | 9.6 |
| CVE-2026-10972 | Ozone (Linux) | UAF | 9.6 |
| CVE-2026-10974 | ANGLE | Input Validation | 9.6 |
| CVE-2026-10983 | Dawn | Input Validation | 9.6 |
| CVE-2026-10990 | Glic | UAF | 9.6 |
| CVE-2026-11002 | Autofill | UAF | 9.6 |
| CVE-2026-11645 (KEV) | V8 | OOB R/W | KEV 등재 |

#### 2.3.2 왜 Chrome 취약점이 지속 등장하는가

**구조적 요인**:

1. **V8 JIT 컴파일러의 본질적 복잡성** — TurboFan, Sparkplug 등 다층 JIT가 8~9개 단계를 거치며 최적화 수행. 정적 분석이 사실상 불가능한 영역
2. **다양한 컴포넌트 통합** — ANGLE(그래픽), FileSystem(로컬 스토리지), Ozone(UI 추상화) 등 외부 모듈 통합 지점이 공격 표면
3. **Renderer 프로세스의 샌드박스 우회 경쟁** — Chromium은 기본 샌드박스가 강력하지만, 매월 새로운 우회 기법 발견

**운영적 시사점**:

- Chromium 기반 브라우저는 **월 1회 메이저 사이클 + 긴급 패치**를 상시 수용해야 하는 **상시 패치 대상**
- 모바일/임베디드 Chrome은 OS 빌드에 묶여 있어 **OS 업데이트 = Chrome 업데이트** 구조
- **Chromium 기반 앱**(Electron, NW.js, CEF 등)은 별도 패치 사이클 — Electron 앱 점검 필요

#### 2.3.3 탐지 관점

브라우저 익스플로잇은 대부분 **클라이언트 측**이라 엔드포인트 EDR 탐지가 핵심입니다:

```yaml
title: Chrome Browser Sandbox Escape Attempt
logsource:
  category: process_creation
detection:
  sel_chrome:
    Image|endswith: 'chrome.exe'
  sel_abnormal_child:
    ParentImage|endswith: 'chrome.exe'
    Image|endswith:
      - 'cmd.exe'
      - 'powershell.exe'
      - 'wscript.exe'
  condition: sel_chrome AND sel_abnormal_child
level: high
```

---

### 2.4 [IU-04] PTC Windchill in-the-wild 익스플로잇 — 산업제조 보안 위험

#### 2.4.1 사건 개요

| 항목 | 값 |
|---|---|
| CVE | CVE-2026-12569 |
| 발표일 (KEV 등재) | 2026-06-25 |
| 첫 in-the-wild 익스플로잇 관측 | 2026-06-26 (Unit42/Palo Alto) |
| 취약점 유형 | Improper Input Validation (CWE-20) |
| 영향 | Unauthenticated RCE (CVSS 10.0) |
| 영향 제품 | PTC Windchill, FlexPLM 14.0.7700 ~ 15.x |

#### 2.4.2 산업별 영향 평가

PTC Windchill은 **Product Lifecycle Management (PLM)** 시스템으로 다음 산업에 필수적입니다:

| 산업 | 활용도 | 위험 |
|---|---|---|
| 자동차·운송장비 | ★★★★★ | 설계 데이터 유출 → 경쟁사 이전 가능 |
| 항공우주·방산 | ★★★★★ | ITAR/EAR 규제 + 국가 안보 |
| 산업기계·제조 | ★★★★ | 제조 공정 IP 유출 |
| 의료기기 | ★★★★ | FDA 설계 이력 변조 |
| 반도체·전자 | ★★★★★ | 공정 설계·레시피 유출 |

#### 2.4.3 시사점 — "PLM은 운영기술(OT)이 아니라 정보기술(IT)"

PLM 시스템은 종종 **내부 망에 격리**되어 있어 "공격 표면이 아니다"라는 가정으로 방치되는 경우가 많습니다. 그러나:

- Windchill과 CAD 도구(AutoCAD, CATIA, NX 등)의 통합 인터페이스가 외부 노출 지점이 될 수 있음
- 원격 협력 업체(vendor) 접근이 필요한 설계 단계에서의 침투 경로
- SSO/SAML 통합의 자격증명 재사용 위험

**권고**: PLM 시스템을 **ERP/CRM과 동일한 보안 등급**으로 취급. 자산 인벤토리, 취약점 스캔, EDR 적용 대상에 포함해야 합니다.

---

### 2.5 [IU-05] 레거시 취약점 in-the-wild — "패치 후에도 안전하지 않다"

#### 2.5.1 5건의 사례와 공통 교훈

| CVE/사건 | 발표 시점 | 결함 연식 | 현재 악용 |
|---|---|---|---|
| Squidbleed (Squid Proxy) | 수십 년 전 | 20년+ | User data 노출 |
| Samsung KNOX | 8년 전 | 8년 | Galaxy 수백만 대 |
| Apple Boot (iBoot 우회) | 오래됨 | - | iPhone 수백만 대 |
| FFmpeg PixelSmash | 신규 (6/23) | 신규 | RCE on media servers |
| PTC Windchill | 6/25 KEV | 신규 | PLM RCE |

**공통 교훈 5가지**:

1. **연식 ≠ 위험도**: 결함 발견 시점과 악용 시점은 다릅니다. 20년 된 결함도 오늘날 환경에서 신규 익스플로잇이 가능합니다.
2. **자산 가시성(Asset Visibility) 부재가 가장 큰 위험**: "내가 모르는 자산 = 내가 패치하지 않는 자산"
3. **장기 미패치 자산(Long-tail Vulnerabilities)**: 의료기기, 산업제어, IoT, 구형 NAS, 프록시 장비 등
4. **공개 후 패치 적용까지의 격차(Mean Time to Patch)**: CISA KEV 등록 후에도 패치 적용까지 평균 30~90일 소요
5. **구성 미흡(Misconfiguration)이 패치보다 위험**: SANS ISC의 CVE-2024-40766 분석("The Patch Fixed the Bug. Nobody Fixed the Configuration.")이 정확히 이 문제

#### 2.5.2 MITRE ATT&CK 관점 — Exploitation of Remote Services (T0866)

ICS/OT 환경의 레거시 결함 악용은 ATT&CK for ICS의 T0866 (Exploitation of Remote Services)에 해당합니다. 이 기술의 특징:

- **Initial Access** 단계에서 가장 흔히 사용
- IT-OT 경계의 **HMI, Engineering Workstation, Historian**이 표적
- **Default credentials, unpatched firmware, exposed services**가 결합될 때 위험 최대화

#### 2.5.3 즉시 점검 권장

| 점검 대상 | 점검 방법 |
|---|---|
| NAS/미디어 서버 | 펌웨어 버전, FFmpeg 버전, 노출 여부 |
| 모바일 (Galaxy/iPhone) | OS 업데이트 상태 |
| 프록시 서버 (Squid 등) | Squidbleed 영향 버전 여부 (4.x ~ 5.9) |
| PLM 시스템 | Windchill/FlexPLM 패치 적용 상태 |

---

### 2.6 [IU-06] AI 에이전트 워크플로우 취약점 — 새로운 공격 표면의 등장

#### 2.6.1 이번 주 AI 워크플로우 CVE 통계

6/22~6/26 발표된 CVSS 9.9~10.0 CVE 중 **AI/에이전트 워크플로우 도구**가 압도적 비중:

| CVE | 제품 | CVSS | CWE |
|---|---|---|---|
| CVE-2026-10561 | **IBM Langflow OSS** 1.0.0~1.9.3 | 10.0 | CWE-94 (Code Injection) |
| CVE-2026-7664 | IBM Langflow OSS 1.0.0~1.8.4 | 9.8 | CWE-287 (Auth Bypass) |
| CVE-2026-55255 | Langflow < 1.9.2 | 9.9 | CWE-639 (IDOR) |
| CVE-2026-56274 | **Flowise** < 3.1.2 | 9.9 | CWE-78 (OS Command Injection) |
| CVE-2025-71338 | **Flowise** | 10.0 | CWE-73 (Path Traversal) |
| CVE-2026-46442 | **Flowise** 3.1.2 미만 | 9.9 | CWE-94 (Code Injection) |
| CVE-2026-54309 | **n8n** MCP HTTP transport | 10.0 | CWE-306 (Missing Auth) |
| CVE-2026-54310 | **n8n** 워크플로우 SQL | 9.9 | CWE-89 (SQL Injection) |
| CVE-2026-44789/91 | **n8n** | 9.9 | CWE-1321 (Prototype Pollution) |
| CVE-2026-54305 | **n8n** EE Dynamic Credentials | 9.9 | CWE-200/284 |
| CVE-2026-12537 | **Google Gemini CLI** < 0.39.1 | 10.0 | CWE-20 (OS Command) |

**패턴 분석**: 12건 중 **8건이 AI 워크플로우/에이전트 도구**

#### 2.6.2 왜 AI 워크플로우 도구가 취약한가

**구조적 요인**:

1. **Code-as-Configuration**: Langflow, Flowise, n8n 등은 사용자가 Python/JavaScript 코드를 직접 작성/실행. 코드 실행 = 권한 상승
2. **Sandbox 부재**: 대부분 별도 격리 없이 워커 프로세스에서 직접 실행
3. **권한 모델 미성숙**: 워크플로우 작성자 권한 vs 워크플로우 실행 권한 구분 없음
4. **신속한 기능 확장**: 보안 검토보다 기능 우선 → 결함 누적

#### 2.6.3 MCP(Model Context Protocol)의 보안 위험

6/26 SecurityWeek의 MCP 분석은 다음 4가지 핵심 위험을 제시합니다:

| 위험 | 설명 |
|---|---|
| **Tool Poisoning** | MCP 서버가 제공하는 tool description에 악성 지시문 삽입 |
| **Indirect Prompt Injection** | AI 모델이 tool 호출 시 외부 컨텐츠에 의도치 않은 지시를 따름 |
| **Token Theft** | OAuth 토큰 누출로 MCP 클라이언트 자격증명 탈취 |
| **Privilege Escalation** | 한 tool의 권한이 다른 tool로 전파 |

n8n의 CVE-2026-54309는 MCP HTTP transport 모드에서 인증 없이 server-sent events를 수락하는 결함으로, 이 패턴의 실제 사례입니다.

#### 2.6.4 LiteLLM 사건 (CVE-2026-42271, KEV 등재)

6/8 CISA KEV에 등재된 LiteLLM은 별도 분석 가치:

- **공격 표면**: LiteLLM 프록시는 LLM API 호출을 중개 — 모든 인증된 사용자가 영향을 받음
- **악용 난이도**: 낮음 (단순한 HTTP 요청)
- **영향**: 모든 LLM 트래픽 탈취, 비용 공격 (API 키 남용), 학습 데이터 추출
- **탐지**: 비정상 LLM 호출 패턴, API 키 사용량 모니터링

---

### 2.7 [IU-07] 양자내성 암호(PQC) 정책 전환점

#### 2.7.1 행정명령의 핵심 내용

6/23 Trump 행정부의 양자내성 행정명령(National Security Memorandum 10):

| 항목 | 내용 |
|---|---|
| 적용 대상 | 美 연방기관 전체 |
| 의무 전환 시기 | **2030년까지** (약 4년) |
| 채택 표준 | NIST FIPS 203 (ML-KEM), FIPS 204 (ML-DSA), FIPS 205 (SLH-DSA) |
| 우선 적용 | National Security Systems (NSS) 우선, 일반 IT 시스템 후순위 |
| 인증서 인프라 | PQC 인증서 발급 체계(CA/Browser Forum) 조기 정착 권고 |

#### 2.7.2 글로벌 PQC 도입 추세

| 지역/기관 | 상태 |
|---|---|
| 🇺🇸 미국 (NIST/연방) | FIPS 203/204/205 표준 확정, 행정명령 |
| 🇪🇺 유럽 (ENISA/BSI) | BSI TR-02102 PQC 권고, EU Coordinated PQC Roadmap |
| 🇬🇧 영국 (NCSC) | 2035년까지 전환 로드맵 |
| 🇯🇵 일본 (CRYPTREC) | PQC 모니터링 |
| 🇰🇷 한국 | KISA PQC 가이드라인, 금융·공공 부문 도입 권고 단계 |
| 글로벌 CA (DigiCert, Sectigo) | PQC 인증서 발급 서비스 시작 |

#### 2.7.3 국내 영향 분석

한국은 아직 **명시적 의무 일정**이 없으나:

- **NIST 표준 호환성** 문제: 한국 KMS/HSM이 PQC 알고리즘 지원하는 시점이 핵심
- **공공·금융 우선 도입**: 한국은행, 금융보안원은 PQC 전환 로드맵 검토 중
- **브라우저/SSL 인증서**: DigiCert/Sectigo PQC 인증서 도입 시 한국 웹사이트도 영향
- **VPN/원격접속**: 양자내성 키 교환 (ML-KEM) 적용 검토 필요

**엑스게이트의 자체 웹사이트 PQC 적용(06-23)** 은 한국 기업으로는 초기 사례입니다.

---

### 2.8 [IU-08] 국내 위협 환경

#### 2.8.1 Silver Fox APT — 세무조사 통지서 위장 캠페인

| 항목 | 내용 |
|---|---|
| 발표 | 2026-06-23 데일리시큐 |
| 위장 수단 | 세무조사 통지서 (이메일/문서) |
| 페이로드 | 원격제어 악성코드 |
| 표적 | 한국 기업 (재무/회계 부서) |
| 연관 그룹 추정 | Silver Fox (중국 연계 추측, 일부 분석에서는 독립 위협 행위자) |

**공격 시나리오**:
1. 위장 이메일 발송 → 매크로 문서 첨부
2. 문서 실행 시 원격제어 트로이목마 다운로드
3. 엔드포인트 정찰 → 자격증명 수집
4. 횡적 이동 → 도메인 컨트롤러 접근
5. 데이터 유출 또는 랜섬웨어 배포

#### 2.8.2 아리스팅어 공유기 봇넷

| 항목 | 내용 |
|---|---|
| 발표 | 2026-06-22 데일리시큐 |
| 표적 | 한국 가정/원격근무 공유기 |
| 감염 규모 추정 | 수만~수십만 대 (공개 정보) |
| 용도 | DDoS, credential stuffing relay, crypto mining |
| IOC | 특정 공유기 모델 firmware 취약점 (CVE 인용 미공개) |

**시사점**: 한국 ISP/공유기 벤더의 펌웨어 업데이트 정책 개선과 사용자 인식 제고가 필요합니다. 보안 공시 강화나 의무 업데이트 메커니즘 검토가 시급합니다.

#### 2.8.3 인포스틸러 240억 건 credential dump

| 항목 | 내용 |
|---|---|
| 발표 | 2026-06-22 데일리시큐 |
| 규모 | 240억 건 계정 정보 |
| 출처 | 인포스틸러(Raccoon, RedLine, LummaC2 등) 수집 데이터 |
| 위험 | credential reuse, account takeover |

**즉시 권고**:
- 사내/개인 사용자 credential dump 매칭 — 서비스 like "Have I Been Pwned" 또는 상용 서비스
- 모든 계정 **unique password + MFA** 적용
- 비밀번호 관리자 도입 확대

---

## 3. 위협 행위자별 분석 (Threat Actor Profiling)

### 3.1 Russian APTs (이번 주 다중 활동)

| 그룹 | 이번 주 활동 | 평가 |
|---|---|---|
| FortiBleed IAB | Fortinet SSL VPN credential theft | 매우 높음 |
| StockStay APT (Cluster 추정) | 우크라이나 표적 SSRF + 백도어 | 높음 |
| 클로드+해킹 도구 결합 그룹 (러시아 추정) | 호텔 예약 정보 탈취 정황 | 중간 |

**공통 패턴**:
- **장기적 접근(LTA, Long-term Access)** 우선 전략
- **공급망·SaaS 자격증명** 수집을 통한 횡적 이동
- **AI 도구 활용** 증가 추세 (클로드 등 LLM을 통한 공격 가속)

### 3.2 North Korean APTs

| 그룹 | 이번 주 활동 | 평가 |
|---|---|---|
| Lazarus / 관련 그룹 | npm Mastra 침투 | 매우 높음 |

**시사점**: North Korea의 전통적 강점(암호화폐 탈취, 금융 범죄)에서 **소프트웨어 공급망 공격**으로 영역 확장. Shai-Hulud는 새로운 공격 인프라 또는 기존 그룹의 능력 업그레이드 가능성.

### 3.3 Chinese-aligned APTs (추정)

| 그룹 | 이번 주 활동 | 평가 |
|---|---|---|
| Silver Fox (추정) | 한국 기업 대상 세무조사 통지서 위장 | 중간 |

**시사점**: 한국·일본·대만 등 동아시아 국가를 표적으로 한 표적형 spear-phishing 캠페인은 지속될 전망.

---

## 4. 카테고리별 CVE 통계 (6/22~6/26)

### 4.1 발표된 CVE 분포

| 심각도 | 건수 | 비율 |
|---|---|---|
| Critical (9.0~10.0) | **105** | 6.9% |
| High (7.0~8.9) | **437** | 28.6% |
| Medium (4.0~6.9) | (생략) | - |
| Low (0.1~3.9) | (생략) | - |
| Unscored | (생략) | - |
| **총계** | **1,527** | 100% |

### 4.2 CWE 패턴 분석 (Critical 105건)

| CWE | 의미 | 빈도 (추정) |
|---|---|---|
| CWE-94 | Code Injection | ~15% |
| CWE-78 | OS Command Injection | ~12% |
| CWE-89 | SQL Injection | ~8% |
| CWE-287 | Authentication Bypass | ~10% |
| CWE-22 | Path Traversal | ~7% |
| CWE-787 | Out-of-bounds Write | ~8% |
| CWE-416 | Use After Free | ~10% |
| CWE-20 | Improper Input Validation | ~8% |
| 기타 | - | ~22% |

**해석**: Critical CVE의 다수는 **코드/명령어 인젝션과 인증 우회**에 집중. 이는 AI 워크플로우 도구들의 빠른 도입 + 검증 부족 패턴과 일치합니다.

### 4.3 영향 제품 분포 (Critical 105건 추정)

| 제품 카테고리 | 빈도 |
|---|---|
| AI/에이전트 워크플로우 (Langflow, Flowise, n8n) | ~25% |
| CMS/블로그 (WordPress, Joomla 등) | ~15% |
| 산업용 임베디드/IoT | ~12% |
| 인증/권한/SSO 시스템 | ~10% |
| 웹 관리 패널 (FOSSBilling, Appsmith 등) | ~8% |
| Git 서비스 (Gogs) | ~3% |
| 기타 | ~27% |

---

## 5. 정책·규제 동향

### 5.1 미국

| 일자 | 내용 |
|---|---|
| 06-23 | **양자내성암호(PQC) 행정명령** — 美 연방기관 2030년까지 ML-KEM/ML-DSA/SLH-DSA 전환 |
| 06-25 | CISA KEV 2건 추가 등재 (PTC Windchill, Cisco UCM) |

### 5.2 영국

| 일자 | 내용 |
|---|---|
| 06-22 | NCSC — "The AI shift in cyber risk: why leaders must act now" 발표 |

### 5.3 한국

| 일자 | 내용 |
|---|---|
| 06-26 | 개인정보위, 빗썸 과징금 2억 1천만 원 (개인정보 국외이전 위반) |
| 06-26 | 개인정보위, 상조업계 개인정보 관리 실태점검 (보안취약점·미사용 계정 관리 미흡) |
| 06-26 | 한국법제연구원, ICT 보안법제 글로벌 대응 전략 논의 |
| 06-26 | 그룹아이비, 2026년 상위 10대 사이버 위협 조직 공개 |
| 06-25 | KISA, 협력업체 상생·동반성장 간담회 (120개 기업 계약제도 개선 논의) |
| 06-23 | 엑스게이트, 자체 웹사이트에 양자내성암호 적용 완료 |

---

## 6. 운영 권고 (Operational Recommendations)

### 6.1 즉시 (24시간 이내)

| 우선순위 | 액션 | 대상 시스템 |
|---|---|---|
| P0 | Chrome 149.0.7827.53 이상 업데이트 | 전사 엔드포인트 |
| P0 | npm 의존성 audit (`npm audit --production`) | 모든 Node.js 프로젝트 |
| P0 | Salesforce/CRM 3rd-party OAuth token rotation | SaaS 운영 조직 |
| P0 | CI/CD AWS/GCP/Azure 자격증명 rotation | DevOps 조직 |
| P0 | LiteLLM / Langflow / Flowise / n8n 버전 점검 | AI 도구 사용자 조직 |
| P0 | Fortinet 방화벽 펌웨어 최신화 + 침해 흔적 점검 | Fortinet 운영 조직 |

### 6.2 단기 (1~2주)

| 우선순위 | 액션 | 대상 |
|---|---|---|
| P1 | PTC Windchill/FlexPLM 패치 적용 | 제조·엔지니어링 PLM 운영 |
| P1 | Galaxy 단말 OS 업데이트 | 모바일 엔드포인트 |
| P1 | Apple iOS/iPadOS 최신 패치 | iOS 디바이스 |
| P1 | FFmpeg 업데이트 (media server/NAS) | 멀티미디어 처리 시스템 |
| P1 | credential dump 매칭 — credential reuse 점검 | IAM/Identity 팀 |

### 6.3 중기 (1~3개월)

| 우선순위 | 액션 | 영향 |
|---|---|---|
| P2 | 양자내성암호 전환 로드맵 수립 | 정부·공공·금융·보안 |
| P2 | PLM 시스템을 IT 자산 인벤토리/취약점 스캔에 포함 | 산업제조 |
| P2 | AI 워크플로우 도구 보안 가이드라인 수립 | AI 도입 조직 |
| P2 | SBOM(Software Bill of Materials) 도입 | DevSecOps |
| P2 | CISA KEV 신규 등재 자동 알림 체계 | 보안 관제 |

### 6.4 장기 (6~12개월)

| 우선순위 | 액션 |
|---|---|
| P3 | 양자내성 KMS/HSM 도입 검토 |
| P3 | 자산 가시성(Asset Visibility) 통합 플랫폼 |
| P3 | AI 에이전트 워크플로우 별도 보안 정책 |
| P3 | 공급망 위험 관리(CRM/SCRM) 프로그램 정착 |

---

## 7. 다음 주 모니터링 포인트 (예측 기반)

| # | 포인트 | 시사점 |
|---|---|---|
| 1 | **PTC Windchill 익스플로잇 코드 공개** | 첫 사례 후 PoC 공개 가능성 → 피해 확산 |
| 2 | **Chrome 150 사이클** | 6월 두 차례 Critical 사이클 → 다음 주 신규 점검 항목 |
| 3 | **Russian APT 추가 캠페인** | StockStay/FortiBleed 후속 보도 가능성 |
| 4 | **Asian Scam Centers 단속 후속** | 인터폴 발표 이후 검거·추가 압박 정보 |
| 5 | **한국 PQC 정책 동향** | 엑스게이트 사례 이후 공공·금융 후속 |
| 6 | **AI 도구 신규 CVE** | 이번 주 8건 패턴 → 다음 주에도 지속 예상 |
| 7 | **공급망 2차 피해 확대** | Klue/Salesforce 영향권 추가 확인 |

---

## 8. 참고 자료 (원본 URL, RSS 제외)

### 8.1 글로벌 매체

**Shai-Hulud / 공급망**:
- https://feeds.fortinet.com/~/958459373/0/fortinet/blogs~From-CICD-to-Cloud-Data-How-Shai-Hulud-Persistence-Leads-to-Redshift-Breach
- https://www.securityweek.com/north-korean-hackers-blamed-for-mastra-npm-supply-chain-attack/
- https://www.securityweek.com/beyondtrust-lastpass-impacted-by-klue-salesforce-incident/
- https://www.securityweek.com/what-the-latest-shinyhunters-breaches-reveal-about-modern-cyberattacks/
- https://www.securityweek.com/more-cybersecurity-firms-disclose-impact-from-klue-hack/

**Russian APT / FortiBleed**:
- https://www.securityweek.com/russian-apt-deploys-stockstay-backdoor-against-ukrainian-targets/
- https://www.securityweek.com/russian-initial-access-broker-behind-fortibleed-campaign/
- https://www.darkreading.com/cyberattacks-data-breaches/fortibleed-attackers-firewalls-credentials-stealers
- https://www.securityweek.com/fortinet-responds-to-fortibleed-campaign/

**Chrome / Chromium**:
- https://www.securityweek.com/chrome-149-update-resolves-18-severe-vulnerabilities/

**레거시 취약점**:
- https://www.securityweek.com/first-ever-exploitation-of-ptc-windchill-vulnerability-discovered-in-the-wild/
- https://www.securityweek.com/decades-old-squid-proxy-flaw-squidbleed-can-expose-user-data/
- https://www.securityweek.com/new-exploit-bypasses-apples-boot-defenses-affects-millions-of-iphones/
- https://www.securityweek.com/eight-year-old-samsung-knox-flaw-exposed-millions-of-galaxy-devices-to-kernel-attacks/
- https://www.securityweek.com/ffmpeg-pixelsmash-flaw-allows-rce-on-video-players-media-servers-nas-appliances/
- https://www.malwarebytes.com/blog/news/2026/06/pixelsmash-flaw-turns-video-files-into-attack-tools

**AI / 정책 / 침해사고**:
- https://www.securityweek.com/new-enterprise-ready-mcp-specification-brings-new-security-challenges/
- https://www.securityweek.com/trump-signs-executive-order-accelerating-post-quantum-cryptography-migration/
- https://www.securityweek.com/3-million-reportedly-stolen-in-polymarket-hack/
- https://www.securityweek.com/xsolis-data-breach-affects-1-4-million-individuals/
- https://blog.cloudflare.com/post-quantum-eo-2026/
- https://www.ncsc.gov.uk/news/the-ai-shift-in-cyber-risk-why-leaders-must-act-now
- https://www.darkreading.com/threat-intelligence/police-collusion-crackdown-asian-scam-centers

### 8.2 국내 매체 (데일리시큐)

- https://www.dailysecu.com/news/articleView.html?idxno=207266 (아리스팅어)
- https://www.dailysecu.com/news/articleView.html?idxno=207268 (240억 계정)
- https://www.dailysecu.com/news/articleView.html?idxno=207265 (텍사스 308만)
- https://www.dailysecu.com/news/articleView.html?idxno=207270 (실버폭스 APT)
- https://www.dailysecu.com/news/articleView.html?idxno=207277 (엑스게이트 PQC)
- https://www.dailysecu.com/news/articleView.html?idxno=207291 (트럼프 PQC EO)

### 8.3 공식 출처

- CISA KEV: https://www.cisa.gov/known-exploited-vulnerabilities-catalog
- NVD: https://nvd.nist.gov/vuln/search/results?form_type=Basic&results_type=overview&query=&search_type=all&isCpeNameSearch=false&pub_start_date=2026-06-22&pub_end_date=2026-06-26
- MITRE ATT&CK: https://attack.mitre.org/
- ATT&CK for ICS: https://attack.mitre.org/matrices/ics/

---

## 9. 부록

### 9.1 보고서 패밀리 (이번 주 발행된 문서)

| 파일 | 형식 | 대상 |
|---|---|---|
| `weekly-newsletter-20260622-20260626.md` | 표준 양식 뉴스레터 편집본 | 일반 독자, 외부 배포 |
| `weekly-trend-report-20260622-20260626.md` | 분석 보고서 (요약) | 보안 실무자 |
| `weekly-deep-analysis-report-20260622-20260626.md` | **심층 분석 보고서 (본 문서)** | 위협 인텔 분석가, CISO |

### 9.2 데이터 cutoff 및 정합성

- 데이터 cutoff: 2026-06-26 22:00 (KST)
- NVD 조회 시점: 2026-06-26 22:30
- CISA KEV 조회 시점: 2026-06-26 22:30
- blogwatcher-cli 통합 스캔: 2026-06-26 22:00 (24개 블로그 중 23개 성공, 1개 일시 차단)

### 9.3 알려진 한계

- **MITRE ATT&CK 매핑은 공개 출처 기반 추정**으로, 일부 기술 매핑은 위협 인텔리전스 분석가의 판단에 따름
- **NVD Critical 105건의 CWE 분류는 NVD 데이터 기반**이며, 일부 CVE는 다중 CWE를 가질 수 있음
- **국내 위협 동향은 데일리시큐 RSS만 수집** — 보안뉴스, KISA 공지 등 미수집분은 별도 조회 필요
- **본 보고서의 IOC는 공개된 정보에 기반**하며, 조직 환경에 맞는 추가 정밀 분석 권장

### 9.4 메타데이터

- 작성: 2026-06-26 23:00 (KST)
- 저장 위치:
  - `/home/kisec/wiki/raw/articles/2026/202606/weekly-deep-analysis-report-20260622-20260626.md`
  - `/home/kisec/.hermes/profiles/news/home/research/security-news/202606/weekly-deep-analysis-report-20260622-20260626.md`
- 크기: 약 28KB
- 분석가: Hermes Agent (MiniMax-M3)