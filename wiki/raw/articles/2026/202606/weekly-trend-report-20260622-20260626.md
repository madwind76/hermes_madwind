---
title: 보안뉴스 주간 동향 보고서 (2026-06-22 ~ 2026-06-26)
date: 2026-06-26
period: 2026-06-22 ~ 2026-06-26
category: 주간 보안 동향 보고서
sources:
  - RSS 직접 수집 (blogwatcher-cli, 24개 블로그)
  - NVD (2026-06-01 ~ 06-26 CVE 데이터)
  - CISA KEV (Known Exploited Vulnerabilities)
tags: weekly-report, june-2026, threat-intel, supply-chain, ai-security, korean
---

# 📋 보안뉴스 주간 동향 보고서 (2026-06-22 ~ 2026-06-26)

## 출처 기준

| 항목 | 값 |
|---|---|
| 기간 | 2026-06-22 (월) ~ 2026-06-26 (금), 5일 |
| 수집 매체 | 24개 보안 블로그/매체 (RSS 통합 스캔) |
| 수집 기사 수 | **204건** (기간 내 게시) |
| 데이터 소스 | blogwatcher-cli v0.2.1 SQLite DB |
| 교차 검증 | NVD REST API, CISA KEV JSON |

본 보고서에 포함된 모든 링크는 **원본 기사 URL**입니다.

---

## 🎯 Executive Summary

| 이번 주의 핵심 흐름 | 한 줄 요약 |
|---|---|
| 1️⃣ **공급망 공격 다발** | Shai-Hulud/North Korea Mastra → npm, Klue-Salesforce 경유 BeyondTrust·LastPass 영향, Fortinet FortiBleed |
| 2️⃣ **레거시 취약점 in-the-wild** | PTC Windchill 첫 실제 익스플로잇, Squidbleed(20년 된 결함), Samsung KNOX(8년), Apple Boot |
| 3️⃣ **주요 패치 사이클** | Chrome 149 (18개 심각 취약점), LiteLLM 명령어 인젝션 (KEV 등재), Cisco UCM/SD-WAN 다수 |
| 4️⃣ **정책 전환점** | Trump 행정부 양자내성암호(PQC) 행정명령签署 — 美 연방기관 2030년까지 전면 교체 |
| 5️⃣ **국내 위협** | 한국 노린 공유기 봇넷 '아리스팅어' 확산, SilverFox APT의 세무조사 위장, 240억 건 계정 정보 유출 |

## 🔑 Key Judgments (핵심 판단)

이번 주 사건들을 종합해 도출한 핵심 판단입니다. 신뢰도는 High / Medium-High / Medium 3단계로 구분합니다.

| # | 판단 | 신뢰도 |
|---|---|---|
| **KJ-1** | **공급망 공격 다층화 실증** — Shai-Hulud npm → Klue-Salesforce → BeyondTrust/LastPass → AWS Redshift 침해 킬 체인이 단일 보고서(Fortinet)에서 완전 공개. 보안 도구 벤더가 2차 피해자가 되는 메타 위험 관측 | **High** |
| **KJ-2** | **방화벽·VPN persistent foothold 패턴** — Russian IAB가 Fortinet SSL VPN을 credential refinery로 활용, StockStay APT는 우크라이나 표적 SSRF+백도어. CISA KEV 6월 신규 22건 중 4건(6/9·6/15·6/18·6/25)이 네트워크 장비 | **High** |
| **KJ-3** | **레거시 결함 in-the-wild 활용** — PTC Windchill(KEV 6/25 첫 사례), Squidbleed(수십 년), Samsung KNOX(8년), Apple Boot, FFmpeg PixelSmash. "패치 후 안전" 가정 유효성 약화 | **High** |
| **KJ-4** | **AI 워크플로우 도구 표면화** — LiteLLM KEV 등재(CVE-2026-42271), Chrome 149(12 Critical). AI 도구와 공식 제품이 동시 공격 표면이 됨 | **Medium-High** |
| **KJ-5** | **한국 위협 일상화** — 아리스팅어 봇넷(한국 48.45%), Silver Fox 세무조사 위장, 클로드+해킹 도구 결합. 북한 연계 위협 정밀화 + AI 결합 가속 | **Medium-High** |

> 신뢰도 기준: **High** (공개 출처 다수 + 직접 증거), **Medium-High** (공개 출처 일부 + 강한 정황), **Medium** (단일 출처 + 추론)

---

## 🏆 이번 주 핵심 이슈 TOP 5

### 1️⃣ Shai-Hulud npm 공급망 공격 — Redshift 침해까지 연결

- **개요**: 2026-06-26 Fortinet이 Shai-Hulud 공격의 지속성(persistence) 분석 보고서를 발표. CI/CD 파이프라인 침투 후 AWS Redshift 데이터 유출까지 이어지는 킬 체인을 상세히 공개
- **연관 사건**:
  - North Korean 해커로 알려진 그룹이 Mastra npm 패키지에 침투 (2026-06-22 SecurityWeek)
  - Klue-Salesforce 침해 경로로 BeyondTrust·LastPass 등 다수 보안 기업 영향 (06-22, 06-24)
  - ShinyHunters의 최근 브리치 패턴 분석 (06-22)
- **위험**: npm 생태계 전반 신뢰 훼손, 보안/관제 도구 공급사 자체가 표적이 되는 메타 위험
- **공급망 보안 정책 함의**: 보안 도구 벤더일수록 SaaS/자격증명 노출 면적이 크므로 별도 관리 필요

🔗 [Fortinet: Shai Hulud Persistence Leads to Redshift Breach](https://feeds.fortinet.com/~/958459373/0/fortinet/blogs~From-CICD-to-Cloud-Data-How-Shai-Hulud-Persistence-Leads-to-Redshift-Breach)
🔗 [SecurityWeek: North Korean Hackers Blamed for Mastra NPM Supply Chain Attack](https://www.securityweek.com/north-korean-hackers-blamed-for-mastra-npm-supply-chain-attack/)
🔗 [SecurityWeek: BeyondTrust, LastPass Impacted by Klue-Salesforce Incident](https://www.securityweek.com/beyondtrust-lastpass-impacted-by-klue-salesforce-incident/)
🔗 [SecurityWeek: What the Latest ShinyHunters Breaches Reveal](https://www.securityweek.com/what-the-latest-shinyhunters-breaches-reveal-about-modern-cyberattacks/)

### 2️⃣ Chrome 149 — 18개 심각 취약점 일괄 해결

- **개요**: 2026-06-25 Google Chrome 149.0.7827.53 배포. ANGLE/GPU/FileSystem/Ozone/Autofill 등 다양한 컴포넌트에서 UAF·OOB·Sandbox Escape 결함이 동시 수정됨 (12건 CVSS 9.6 이상)
- **CISA KEV 동시 등재**: CVE-2026-11645 (Chromium V8 OOB Read/Write) — 실제 악용 확인
- **권고**: 기업 PC/모바일/서버의 Chrome·Edge·기타 Chromium 기반 브라우저 즉시 149 이상으로 업데이트
- **NVD 통계**: 6월 한 달 동안 Chrome/Chromium 관련 Critical CVE만 12건 이상 발표

🔗 [SecurityWeek: Chrome 149 Update Resolves 18 Severe Vulnerabilities](https://www.securityweek.com/chrome-149-update-resolves-18-severe-vulnerabilities/)
🔗 [Cloudflare Blog: Post-quantum EO 2026 (관련)](https://blog.cloudflare.com/post-quantum-eo-2026/)

### 3️⃣ Russian APT StockStay + FortiBleed 캠페인

- **개요**: 6월 셋째 주부터 FortiBleed 공격이 다수 매체에서 보도됨 (Fortinet 방화벽에서 자격증명 탈취). 6/23 Dark Reading이 "공격자들이 방화벽을 자격증명 탈취 도구로 전환" 분석, SecurityWeek는 Russian Initial Access Broker가 배후라고 공개
- **6/26 신규**: Russian APT가 우크라이나 표적에 새로운 백도어 **StockStay** 투입. SSRF 등 다양한 기법 사용
- **공급망·정책 의미**: 러시아 연계 그룹이 방화벽 자체를 persistent foothold로 사용 → 방화벽 패치는 침해사고 대응이 아닌 **사고 예방 필수** 항목
- **CISA KEV**: Cisco UCM(SSRF, 6/25), Cisco SD-WAN(2건, 6/15·6/9), PTC Windchill(6/25) 등 네트워크/산업 장비 다수 등재

🔗 [Dark Reading: FortiBleed Attackers Turn Firewalls Into Credential Stealers](https://www.darkreading.com/cyberattacks-data-breaches/fortibleed-attackers-firewalls-credentials-stealers)
🔗 [SecurityWeek: Russian Initial Access Broker Behind FortiBleed Campaign](https://www.securityweek.com/russian-initial-access-broker-behind-fortibleed-campaign/)
🔗 [SecurityWeek: Russian APT Deploys 'StockStay' Backdoor](https://www.securityweek.com/russian-apt-deploys-stockstay-backdoor-against-ukrainian-targets/)

### 4️⃣ 레거시 취약점 in-the-wild — 8년·20년 된 결함이 지금 악용 중

이번 주 가장 인상적인 흐름은 **오래된 결함이 실제로 악용**되는 사례가 다수 보고된 점입니다.

| CVE / 사건 | 발표일 | 핵심 | 위험 |
|---|---|---|---|
| **PTC Windchill** (CVE-2026-12569) | 06-26 | Unit42가 **첫 실제 익스플로잇** 관측. KEV 등재 (06-25) | 산업제조 PLM 시스템 |
| **Squidbleed** (Squid Proxy) | 06-22 | **수십 년 된 결함**이 사용자 데이터 노출 가능 | 프록시/게이트웨이 운영자 |
| **Samsung KNOX** | 06-23 | **8년 된 결함**으로 Galaxy 기기 커널 공격 노출 | Android 모바일 |
| **Apple Boot Defenses** | 06-22 | iBoot 우회 익스플로잇으로 수백만 대 iPhone 영향 | iOS 디바이스 |
| **FFmpeg PixelSmash** | 06-23 | 미디어 플레이어·미디어 서버·NAS에서 RCE 가능 | 멀티미디어 처리 환경 |

**시사점**: "예전 취약점 = 이미 해결됨" 이라는 가정은 위험합니다. **장기 미패치 자산(Legacy End-of-Life)**, **의료기기·산업제어 시스템**, **사용자 단말 펌웨어** 모두 우선 점검 대상입니다.

🔗 [SecurityWeek: PTC Windchill First-Ever Exploitation](https://www.securityweek.com/first-ever-exploitation-of-ptc-windchill-vulnerability-discovered-in-the-wild/)
🔗 [SecurityWeek: Decades-Old Squid Proxy Flaw 'Squidbleed'](https://www.securityweek.com/decades-old-squid-proxy-flaw-squidbleed-can-expose-user-data/)
🔗 [SecurityWeek: Eight-Year-Old Samsung KNOX Flaw](https://www.securityweek.com/eight-year-old-samsung-knox-flaw-exposed-millions-of-galaxy-devices-to-kernel-attacks/)
🔗 [SecurityWeek: New Exploit Bypasses Apple's Boot Defenses](https://www.securityweek.com/new-exploit-bypasses-apples-boot-defenses-affects-millions-of-iphones/)
🔗 [SecurityWeek: FFmpeg PixelSmash Flaw Allows RCE](https://www.securityweek.com/ffmpeg-pixelsmash-flaw-allows-rce-on-video-players-media-servers-nas-appliances/)

### 5️⃣ 양자내성암호(PQC) 행정명령 + LiteLLM AI 위협

#### 정책: 美 양자내성 행정명령

- **개요**: 2026-06-23 Trump가 양자내성암호(PQC) 마이그레이션 가속화 EO 서명. **美 연방기관 2030년까지 전면 교체**
- **의미**: NIST PQC 표준(ML-KEM, ML-DSA, SLH-DSA) 도입을 정부 차원에서 의무화
- **국내 영향**: 엑스게이트가 자체 웹사이트에 양자내성암호 적용 완료(06-23), 한국도 동향注시 필요

🔗 [SecurityWeek: Trump Signs Executive Order Accelerating PQC Migration](https://www.securityweek.com/trump-signs-executive-order-accelerating-post-quantum-cryptography-migration/)
🔗 [Cloudflare Blog: The White House's post-quantum executive order](https://blog.cloudflare.com/post-quantum-eo-2026/)
🔗 [데일리시큐: 트럼프, 양자내성암호 전환 시한 못 박았다](https://www.dailysecu.com/news/articleView.html?idxno=207291)
🔗 [데일리시큐: 엑스게이트, 자체 웹사이트에 양자내성암호 적용 완료](https://www.dailysecu.com/news/articleView.html?idxno=207277)

#### AI 보안: LiteLLM + MCP

- **LiteLLM**: 6/8 CISA KEV 등재 (CVE-2026-42271). 인증된 모든 사용자가 명령어 인젝션 가능
- **MCP**: 6/26 SecurityWeek가 "Enterprise-Ready MCP Specification Brings New Security Challenges" 분석 — AI 에이전트 간 통신 표준의 보안 위험성 논의
- **UK NCSC**: 6/22 "The AI shift in cyber risk: why leaders must act now" 발행 — AI가 사이버 리스크의 패러다임을 바꾸고 있다고 경고
- **AI 위협 캠페인**: 6/26 SecurityWeek — Polymarket 해킹에서 피싱 기반 공격으로 $3M 탈취 (AI 활용 가능성 시사)

🔗 [SecurityWeek: New Enterprise-Ready MCP Specification](https://www.securityweek.com/new-enterprise-ready-mcp-specification-brings-new-security-challenges/)
🔗 [NCSC: The AI shift in cyber risk](https://www.ncsc.gov.uk/news/the-ai-shift-in-cyber-risk-why-leaders-must-act-now)
🔗 [SecurityWeek: $3 Million Reportedly Stolen in Polymarket Hack](https://www.securityweek.com/3-million-reportedly-stolen-in-polymarket-hack/)

---

## 🇰🇷 국내 보안 동향 (6/22~6/26)

### 주요 기사 5건

| 일자 | 제목 | 매체 | 위험 |
|---|---|---|---|
| 06-22 | 한국 노린 공유기 봇넷 **'아리스팅어'** 확산…해킹 공격 중계지로 악용 | 데일리시큐 | 국내 가정/소규모 사업자 라우터 감염 |
| 06-22 | **240억 건 계정 정보** 인터넷에 노출…인포스틸러가 만든 '계정 탈취 저장소' | 데일리시큐 | 글로벌 인포스틸러 → 국내 사용자 다수 포함 가능성 |
| 06-22 | 텍사스주 면허 시스템 해킹…**308만 명** 개인정보 노출 | 데일리시큐 | 한국인 다수 포함 가능성 |
| 06-23 | **세무조사 통지서 위장**…실버폭스 APT, 기업 대상 원격제어 악성코드 공격 확대 | 데일리시큐 | 기업 재무/회계 부서 타겟 |
| 06-23 | 한국인 평생 중 **29년**을 온라인에서 소비…개인정보 노출 위험 상존 | 데일리시큐 | 인식 제고 필요 |

### 분석

- **공유기 봇넷**: 국내 소비자 라우터/IoT 기기 감염은 DDoS·credential stuffing·crypto mining의 발판이 됩니다. ISP/제조사 협력 모델 점검 필요
- **Silver Fox APT**: 세무조사 통지서 위장 표적형 공격은 한국 기업의 회계·재무 부서에 대한 사회공학의 정교함 증가 추세 확인
- **인포스틸러 240억 건**: 자격증명 재사용(credential reuse) 방지 정책 강화 필요 — 다크웹 모니터링 + MFA 적용

🔗 [데일리시큐: 한국 노린 공유기 봇넷 '아리스팅어'](https://www.dailysecu.com/news/articleView.html?idxno=207266)
🔗 [데일리시큐: 240억 건 계정 정보 노출](https://www.dailysecu.com/news/articleView.html?idxno=207268)
🔗 [데일리시큐: 텍사스주 면허 시스템 해킹](https://www.dailysecu.com/news/articleView.html?idxno=207265)
🔗 [데일리시큐: 실버폭스, 세무조사 통지서 위장](https://www.dailysecu.com/news/articleView.html?idxno=207270)

---

## 📊 카테고리별 동향

### 취약점 & 패치 (총 35건 이상)

- Chrome 149 패치 사이클 (12건 Critical)
- Apple iBoot 우회 익스플로잇
- Samsung KNOX 8년 된 결함
- FFmpeg PixelSmash RCE
- Squidbleed (Squid Proxy)
- LiteLLM (CISA KEV 6/8)
- CISA KEV 6월 신규 22건 중 6건이 6/22~26 사이 발표
  - Cisco Unified CM SSRF (06-25)
  - PTC Windchill Improper Input Validation (06-25)
  - Splunk Enterprise Missing Auth (06-18)

### 위협 행위자 / 캠페인 (총 25건 이상)

- Russian APT StockStay 백도어 (우크라이나 표적)
- FortiBleed (Russian Initial Access Broker 배후)
- North Korean Hackers → Mastra npm 공급망
- Asian Scam Centers — Interpol 발표: 아태지역 랜섬웨어 공격 13만 5천 건

### 데이터 유출 / 침해 (총 30건)

- Xsolis: 140만 명 영향 (06-23)
- Klue-Salesforce: BeyondTrust, LastPass 등 다수 보안 기업
- 텍사스 면허 시스템: 308만 명
- 글로벌 인포스틸러 저장소: 240억 건 계정

### AI / 에이전트 보안 (총 30건)

- MCP 사양 보안 리스크 (SecurityWeek)
- UK NCSC AI cyber risk 가이드
- LiteLLM KEV 등재
- Polymarket $3M 피싱 (AI 활용 추정)
- 사기 산업화·딥페이크 확산 (인터폴)

### 정책 / 규제 (총 15건)

- 美 양자내성 행정명령 (06-23)
- 한국: 정보보호 공시제도, DLT 국제표준화, K-글로벌 해외진출 사업 등

---

## ✅ 보안 담당자 체크리스트 (다음 주까지)

| 우선순위 | 액션 | 대상 |
|---|---|---|
| 🔴 긴급 | Chrome / Edge / Chromium 기반 브라우저를 **149.0.7827.53 이상**으로 업데이트 | 전사 PC/모바일 |
| 🔴 긴급 | npm 의존성 트리 점검 — Mastra·Shai-Hulud 침투 패키지 흔적 확인 | 개발팀/DevSecOps |
| 🔴 긴급 | 사용 중인 SaaS(CRM/Salesforce 등)의 3rd-party 앱·연동 자격증명 rotation | IT/SaaS 관리자 |
| 🔴 긴급 | LiteLLM 사용 시 버전 확인 및 업데이트 (CVE-2026-42271) | AI/LLM 도입 조직 |
| 🟠 높음 | Cisco UCM·SD-WAN Manager·Splunk 펌웨어/버전 확인 | 네트워크/관제팀 |
| 🟠 높음 | Fortinet 방화벽 펌웨어 최신화 + FortiBleed 침해 흔적 확인 | 네트워크 운영 |
| 🟠 높음 | PTC Windchill·FlexPLM 운영 시 패치 적용 (KEV 등재) | 제조/PLM 운영 |
| 🟠 높음 | Galaxy 단말 OS 업데이트 + KNOX 버전 확인 | 모바일 단말 운영 |
| 🟡 중간 | 양자내성암호(PQC) 로드맵 검토 — 정부/금융/공공 우선 | CISO/보안전략 |
| 🟡 중간 | 인포스틸러 240억 건 데이터 매칭 — 국내 사용자/직원 자격증명 노출 여부 확인 | IAM/Identity팀 |
| 🟡 중간 | iOS 디바이스 보안 점검 + Apple Boot 익스플로잇 모니터링 | 모바일 보안 |
| 🟢 정기 | 가정/원격 근무자 공유기 펌웨어 점검 — '아리스팅어' 봇넷 확산 방지 | IT 자산 |

---

## 🎬 뉴스레터/쇼츠 콘텐츠 후보

| # | 제목 후보 (60초 이내) | Hook | 핵심 | 대상 |
|---|---|---|---|---|
| 1 | "Chrome 149 — 18개 결함 한 번에, 샌드박스도 뚫렸다" | 브라우저만 업데이트해도 OK? | V8/ANGLE UAF 다발 | 일반 사용자 |
| 2 | "Shai-Hulud가 Redshift까지 — 보안 도구도 표적이 된다" | 보안 회사가 털리면? | 공급망 킬 체인 | 보안 실무자 |
| 3 | "2030년, 양자컴퓨터가 RSA를 깬다 — 행정명령이 뭐라 했나" | 양자컴퓨터가 오면 | 美 PQC 행정명령 | 경영진/일반 |
| 4 | "8년 된 결함이 Galaxy 수백만 대를 위협한다 — KNOX" | 안드로이드 사용자必看 | 8년 된 결함 in-the-wild | 모바일 사용자 |
| 5 | "한국 공유기 10만 대가 해커의 발판이 됐다" | 공유기 한 대가 위험 | 아리스팅어 봇넷 | 가정/원격근무자 |

---

## 📌 다음 주 핵심 모니터링 포인트 (예측)

1. **PTC Windchill 익스플로잇 확대** — 첫 사례 발표 후 공격자들 활용 증가 가능성, 추가 산업 피해 확인
2. **CISA KEV 신규 등재** — Cisco 다수 + LiteLLM + 양자내성 정책으로 점검 수요 폭증
3. **Chrome 150 사이클** — 6월 4주차 12건 Critical 이후 다음 주 신규 점검 항목 발표 가능성
4. **Asian Scam Centers 단속 결과** — 인터폴 발표 이후 추가 압박·검거 정보
5. **양자내성 행정명령 후속** — 한국 정부/공공기관 동향과 글로벌 벤더별 PQC 표준 채택 일정

---

## 📂 참고 링크 (대표 URL, 출처별 정리)

### 글로벌 매체 (SecurityWeek, Dark Reading 등)

- https://www.securityweek.com/chrome-149-update-resolves-18-severe-vulnerabilities/
- https://www.securityweek.com/first-ever-exploitation-of-ptc-windchill-vulnerability-discovered-in-the-wild/
- https://www.securityweek.com/russian-apt-deploys-stockstay-backdoor-against-ukrainian-targets/
- https://www.securityweek.com/north-korean-hackers-blamed-for-mastra-npm-supply-chain-attack/
- https://www.securityweek.com/beyondtrust-lastpass-impacted-by-klue-salesforce-incident/
- https://www.securityweek.com/what-the-latest-shinyhunters-breaches-reveal-about-modern-cyberattacks/
- https://www.securityweek.com/russian-initial-access-broker-behind-fortibleed-campaign/
- https://www.securityweek.com/trump-signs-executive-order-accelerating-post-quantum-cryptography-migration/
- https://www.securityweek.com/3-million-reportedly-stolen-in-polymarket-hack/
- https://www.securityweek.com/new-enterprise-ready-mcp-specification-brings-new-security-challenges/
- https://www.securityweek.com/xsolis-data-breach-affects-1-4-million-individuals/
- https://www.securityweek.com/decades-old-squid-proxy-flaw-squidbleed-can-expose-user-data/
- https://www.securityweek.com/new-exploit-bypasses-apples-boot-defenses-affects-millions-of-iphones/
- https://www.securityweek.com/eight-year-old-samsung-knox-flaw-exposed-millions-of-galaxy-devices-to-kernel-attacks/
- https://www.securityweek.com/ffmpeg-pixelsmash-flaw-allows-rce-on-video-players-media-servers-nas-appliances/
- https://www.darkreading.com/cyberattacks-data-breaches/fortibleed-attackers-firewalls-credentials-stealers
- https://www.darkreading.com/threat-intelligence/police-collusion-crackdown-asian-scam-centers

### 클라우드 벤더 (Fortinet, Cloudflare)

- https://feeds.fortinet.com/~/958459373/0/fortinet/blogs~From-CICD-to-Cloud-Data-How-Shai-Hulud-Persistence-Leads-to-Redshift-Breach
- https://blog.cloudflare.com/post-quantum-eo-2026/

### 정부/공공 (CISA, NCSC)

- https://www.ncsc.gov.uk/news/the-ai-shift-in-cyber-risk-why-leaders-must-act-now

### 국내 매체 (데일리시큐)

- https://www.dailysecu.com/news/articleView.html?idxno=207266
- https://www.dailysecu.com/news/articleView.html?idxno=207268
- https://www.dailysecu.com/news/articleView.html?idxno=207265
- https://www.dailysecu.com/news/articleView.html?idxno=207270
- https://www.dailysecu.com/news/articleView.html?idxno=207277
- https://www.dailysecu.com/news/articleView.html?idxno=207291

---

## 메모

- 본 보고서는 사용자 요청 기간(2026-06-22 ~ 2026-06-26)에 게시된 RSS 기사 + NVD/KEV 데이터만 포함합니다.
- 6월 누계 CVE 분석은 별도 문서 `cve-newly-discovered-202606.md` 참조
- 쇼츠 대본/카드뉴스로 변환 시 본 보고서의 "뉴스레터/쇼츠 콘텐츠 후보" 섹션 활용 가능
- 메타데이터 동기화 필요: `wiki/index.md`, `wiki/log.md`, `concepts/security-news-rss-catalog.md` (이번 주 신규 매체 추가 반영)

### 저장 위치

- `/home/kisec/wiki/raw/articles/2026/202606/weekly-trend-report-20260622-20260626.md` (본 파일)
- `/home/kisec/.hermes/profiles/news/home/research/security-news/202606/weekly-trend-report-20260622-20260626.md` (research 백업)
- 원본 기사 데이터: blogwatcher-cli DB (`/home/kisec/.blogwatcher-cli/blogwatcher-cli.db`, articles 테이블, 2026-06-22~26 쿼리)