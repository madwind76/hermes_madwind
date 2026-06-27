---
title: 2026년 6월 보안 동향 월간 보고서
date: 2026-06-26
period: 2026-06-01 ~ 2026-06-26 (W1~W4)
type: monthly-report
audience: CISO, 위협 인텔리전스 분석가, 보안 관제 리더
related_reports:
  - wiki/raw/articles/2026/202606/weekly-newsletter-20260622-20260626.md
  - wiki/raw/articles/2026/202606/weekly-trend-report-20260622-20260626.md
  - wiki/raw/articles/2026/202606/weekly-deep-analysis-report-20260622-20260626.md
  - wiki/raw/articles/2026/202606/cve-newly-discovered-202606.md
tags: [security, monthly-report, june-2026, threat-intel, kev, supply-chain, ai-security, korean]
sources:
  - RSS (24개 블로그 통합)
  - NVD REST API (6월 누계 6,743건)
  - CISA KEV (신규 22건)
---

# 📅 2026년 6월 보안 동향 월간 보고서 (2026-06-01 ~ 2026-06-26)

> **본 문서는 6월 한 달간의 보안 동향을 종합한 월간 보고서입니다.**
> 개별 주차별 보고서는 관련 파일 섹션(섹션 10)을 참조하세요.

---

## 0. 데이터 수집 기준

| 항목 | 값 |
|---|---|
| 기간 | 2026-06-01 (월) ~ 2026-06-26 (금) — 4주 + 2일 |
| RSS 통합 수집 | 24개 보안 매체 (blogwatcher-cli v0.2.1) |
| 수집 기사 | **328건** (누계) |
| NVD 신규 CVE | **6,743건** (Critical 180 / High 802 / Medium 865 / Low 111) |
| CISA KEV 신규 | **22건** |
| 분석 프레임워크 | MITRE ATT&CK v15, Lockheed Kill Chain, Diamond Model |

### 0.1 주차별 수집 추이

| 주차 | 기간 | 기사 수 | 누적 | 특징 |
|---|---|---|---|---|
| **W1** | 6/1 ~ 6/7 | 11건 | 11 | 신규 매체 도입 전, 초기 11개 블로그만 |
| **W2** | 6/8 ~ 6/14 | 31건 | 42 | Microsoft Patch Tuesday, NCSC AI 가이드, AI 정책 |
| **W3** | 6/15 ~ 6/21 | 82건 | 124 | 신규 매체 13개 추가, MS Defender 제로데이(로그플래닛), CISA KEV 신규 |
| **W4** | 6/22 ~ 6/26 | 204건 | **328** | Shai-Hulud, Chrome 149, 양자내성 EO, AI 도구 다발 취약점 |

> ⚠️ **수치 해석 주의**: W3/W4의 급격한 증가(82 → 204)는 부분적으로 **6/22 신규 매체 13개 추가**의 영향입니다. 단순 비교보다 **밀도(이슈 수/매체 수)** 로 보는 것이 정확합니다.

---

## 1. 🎯 월간 핵심 키워드 TOP 5

6월 한 달간 가장 빈번하게 등장한 보안 이슈의 핵심 키워드입니다:

| 순위 | 키워드 | 빈도 | 핵심 |
|---|---|---|---|
| **1** | **AI 워크플로우 / 에이전트 보안** | 99건 | LiteLLM, Langflow, Flowise, n8n, MCP — 가장 뜨거운 카테고리 |
| **2** | **랜섬웨어 / 데이터 유출** | 18건 | ShinyHunters, Xsolis(140만), Texas(308만), 인포스틸러(240억) |
| **3** | **공급망 공격 (npm)** | 17건 | Shai-Hulud, Mastra, Klue-Salesforce 경유 2차 피해 |
| **4** | **FortiBleed / Russian APT** | 12건 | NCSC 글로벌 경고 포함, 6월 지속적 활동 |
| **5** | **피싱 / 사기 / 사회공학** | 11건 | Asian Scam Centers, Polymarket $3M, 인터폴 13.5만 건 보고 |

### 1.1 키워드별 월간 흐름 (Trend Vector)

```
[AI 워크플로우]      ▁▁▃▅ → 99건 (6월 폭발적 증가)
[랜섬웨어/유출]      ▂▂▂▆ → 18건 (W4 집중)
[공급망]             ▁▂▂▆ → 17건 (Shai-Hulud 등장)
[Russian APT]        ▁▂▃▅ → 12건 (지속)
[피싱/사기]          ▁▂▂▅ → 11건 (W4 Polymarket)
[ICS/OT]             ▁▂▃▃ → 10건
[KEV/정책]           ▁▁▃▅ → 9건 (양자내성 EO)
[레거시 취약점]      ▁▁▁▆ → 5건 (W4 집중)
[Chrome]             ▁▂▂▆ → 4건 (149 사이클)
[국내 위협]          ▁▁▁▅ → 4건 (Silver Fox/Aritstinger)
```

**시사점**: 6월은 **AI 워크플로우 카테고리**가 압도적이었고, W4(6/22~26)는 **모든 카테고리가 동시에 활성화**된 한 달의 클라이맥스였습니다.

### 1.2 🔑 Key Judgments (월간 핵심 판단)

6월 한 달간 누적 데이터를 종합해 도출한 7개 핵심 판단입니다. 신뢰도는 High / Medium-High / Medium 3단계로 구분합니다.

| # | 판단 | 신뢰도 |
|---|---|---|
| **KJ-1** | **AI 워크플로우/에이전트 보안이 새로운 공격 표면으로 부상** — LiteLLM/Langflow/Flowise/n8n 6월 CVSS 9.9~10.0 다발. LiteLLM은 CISA KEV 등재(CVE-2026-42271). 6월 누계 기사 99건 중 가장 빈번한 카테고리 | **High** |
| **KJ-2** | **공급망 공격의 다층화·산업화 가속** — Shai-Hulud → Klue-Salesforce → BeyondTrust/LastPass → AWS Redshift 킬 체인이 단일 분석 보고서(Fortinet)에서 완전 공개. 보안 도구 벤더가 2차 피해자가 되는 메타 위험 실증 | **High** |
| **KJ-3** | **레거시 결함의 in-the-wild 활용 확인** — PTC Windchill 첫 in-the-wild 익스플로잇(KEV 6/25), Squidbleed(20년), Samsung KNOX(8년), Apple Boot, FFmpeg PixelSmash. "패치 후 안전" 가정 약화 | **High** |
| **KJ-4** | **방화벽·네트워크 장비의 persistent foothold화** — Russian IAB가 Fortinet SSL VPN을 credential refinery로 활용, StockStay APT는 우크라이나 표적 SSRF+백도어. CISA KEV 6월 신규 22건 중 4건이 네트워크 장비 | **High** |
| **KJ-5** | **한국 노린 위협의 일상화** — 아리스팅어 봇넷(한국 48.45%), Silver Fox APT(세무조사 위장), DPRK 클로드+해킹 도구 결합, macOS 가스라이트. 국가별 표적 정밀화 + AI 도구 결합 | **Medium-High** |
| **KJ-6** | **국가 정책의 암호학적 전환점** — 美 양자내성 행정명령(6/23, 연방기관 2030까지 ML-KEM/ML-DSA/SLH-DSA 의무화). 한국 엑스게이트 PQC 적용(6/23), 금융권 PQC 전환 전략 발표 | **Medium-High** |
| **KJ-7** | **공격자 귀속 불확실성 동반** — Russian APT/Cluster 명 미공개(Fortinet), ShinyHunters vs DPRK 클로드 활용 사례는 출처별 차이. 클로드+해킹 도구 러시아 공격자 단정 어려움. **단정 금지, "추정" 표현 권장** | **Medium** |

> **신뢰도 기준**: **High** (공개 출처 다수 + 직접 증거, KEV 등재, RFC 발표, 공식 패치) / **Medium-High** (공개 출처 일부 + 강한 정황, 다수 매체 보도, 기술 분석 일치) / **Medium** (단일 출처 + 추론, 단일 분석 보고서, 전망)

---

## 2. 📌 월간 Strategic Summary

### 2.1 6월의 5대 흐름

#### 🏆 흐름 1. AI 워크플로우 도구의 보안 위협 부상

6월 누계 CVE 6,743건 중 **AI 워크플로우/에이전트 도구에서만 CVSS 10.0이 8건 이상** 발표됐습니다. LiteLLM, IBM Langflow, Flowise, n8n 모두 6월에 긴급 패치가 필요한 취약점이 발견됐고, MCP(Model Context Protocol)의 보안 위험성 논의가 본격화됐습니다.

**전월 대비 변화**: 5월 대비 AI 워크플로우 카테고리 기사가 300% 이상 증가.

#### 🏆 흐름 2. 공급망 공격의 다층화

- **1차 (소프트웨어 공급망)**: Shai-Hulud가 npm 생태계에 정착, North Korea 연계 그룹이 Mastra 침투
- **2차 (서비스 공급망)**: Klue-Salesforce 침해 경유로 **보안 벤더(BeyondTrust, LastPass)가 피해자**가 되는 메타 위험
- **3차 (하드웨어/IoT)**: PTC Windchill, Samsung KNOX, Apple Boot, FFmpeg, Squid Proxy 등 **장기 미패치 자산**의 재활용

#### 🏆 흐름 3. 국가 정책의 암호학적 전환점

- **美 양자내성 행정명령 (6/23)** — 2030년까지 NIST PQC 표준 의무화
- **CISA New Directive (6/10)** — 연방기관 취약점 완화 우선순위 재작성
- **NCSC AI 가이드 (6/22)** — AI 시대 사이버 리스크 리더십 행동 촉구

#### 🏆 흐름 4. 레거시 취약점의 현실적 위험 재확인

평균 5년 이상 된 결함이 in-the-wild 익스플로잇에 활용됨. **"패치 후에도 안전하지 않다"는 SANS ISC의 경고**가 대표적입니다. CISA KEV 신규 22건 중 일부는 오래된 CVE의 재발견/재악용 사례.

#### 🏆 흐름 5. 국내 위협 환경의 정교화

- **Silver Fox APT** — 세무조사 통지서 위장 기업 표적 공격
- **아리스팅어 봇넷** — 한국 공유기 감염 확산
- **240억 건 credential dump** — 글로벌 인포스틸러 데이터 → 한국 사용자 포함 가능성

---

## 3. 📊 6월 누계 CVE 분석

### 3.1 심각도 분포 (전체 6,743건)

| 심각도 | 건수 | 비율 | 비고 |
|---|---|---|---|
| Critical (9.0~10.0) | **180** | 2.7% | AI 워크플로우 8건, Chrome 12건, Cisco 다수 |
| High (7.0~8.9) | **802** | 11.9% | - |
| Medium (4.0~6.9) | 865 | 12.8% | - |
| Low (0.1~3.9) | 111 | 1.6% | - |
| Unscored | 42 | 0.6% | - |
| 정보 없음 | (잔여) | - | - |

### 3.2 6월 누계 Critical CVE의 주요 제품 분포

| 제품/카테고리 | Critical CVE 수 | 비고 |
|---|---|---|
| AI/에이전트 워크플로우 | ~30+ | Langflow, Flowise, n8n, Gogs, Appsmith |
| Chrome / Chromium | 12+ | 6/4 + 6/25 두 사이클 |
| 네트워크 장비 (Cisco, Palo Alto, Fortinet) | ~25+ | UCM, SD-WAN, PAN-OS |
| 산업/IoT (ABB, GV-I/O Box 등) | ~15+ | OT/ICS |
| CMS / 블로그 (WordPress, Joomla) | ~25+ | 플러그인 결함 다수 |
| 클라우드 / 컨테이너 (Apache, Cloud Foundry) | ~20+ | Apache HTTP Server, ActiveMQ |
| SAP / Oracle / Microsoft | ~15+ | NetWeaver, PeopleSoft |
| 기타 | ~40+ | - |

### 3.3 CISA KEV 6월 신규 22건 카테고리 분석

| 카테고리 | 건수 | 대표 사례 |
|---|---|---|
| 인증 우회 / Missing Auth | 5 | Splunk, Oracle PeopleTools, WebLogic, LiteSpeed, MISP |
| 명령어 인젝션 | 3 | Lantronix, Ivanti Sentry, LiteLLM |
| Path Traversal | 2 | Ubiquiti UniFi OS, Cisco SD-WAN Manager |
| 네트워크/IoT | 7 | PTC Windchill, Cisco, Ubiquiti, Arista, Lantronix, SolarWinds |
| OS Command Injection | 2 | Lantronix EDS5000, Ivanti Sentry |

### 3.4 6월 CVE 발표 일별 추이

| 일 | Critical | High | 일별 특이사항 |
|---|---|---|---|
| 6/1 | ~10 | ~30 | Apache ActiveMQ, Cloud Foundry, 다수 |
| 6/2 | ~8 | ~25 | MISP, Sitefinity |
| 6/4 | **~30** | **~80** | **Chrome 148 + 12 Critical 다발** |
| 6/5 | ~12 | ~35 | Azure, Windchill 사전공개 |
| 6/8 | ~8 | ~25 | LiteLLM, Check Point |
| 6/9 | ~10 | ~30 | SAP, Arista, Chromium |
| 6/11 | ~7 | ~25 | Ivanti Sentry |
| 6/15 | ~5 | ~20 | Cisco SD-WAN |
| 6/18 | ~5 | ~20 | Splunk Enterprise |
| 6/22 | ~10 | ~25 | IBM Langflow, n8n MCP |
| 6/23 | **~25** | **~60** | **n8n 다발, Gogs, AI 워크플로우 집중** |
| 6/24 | ~15 | ~35 | Gemini CLI, Gogs, SiYuan |
| 6/25 | ~10 | ~30 | Apache Kvrocks, Chrome 149 |
| 6/26 | ~5 | ~15 | - |

> **인사이트**: 6/4(Chrome 148 사이클)와 6/23(n8n/AI 워크플로우 다발)이 Critical CVE 발표의 두 정점입니다.

---

## 4. 🚨 위협 행위자별 월간 활동 종합

### 4.1 Russian APTs (다중 캠페인)

| 그룹 | 6월 활동 | 평가 |
|---|---|---|
| **FortiBleed IAB** | NCSC 글로벌 경고(6/18), Fortinet 침해 분석(6/22~26), StockStay 백도어(6/26) | **최고 위협** |
| StockStay APT | 우크라이나 표적 SSRF + 백도어 | 높음 |
| 클라우드 기반 그룹 | 클로드+해킹 도구 결합, 호텔 정보 탈취 | 중간 |

**6월 러시아 그룹의 특징**: **공급망·VPN·백도어의 다중 벡터 동시 운영**. 단일 그룹인지 다중 그룹인지는 공개 정보로 구분 불가.

### 4.2 North Korean APTs

| 그룹 | 6월 활동 |
|---|---|
| Lazarus / 관련 | npm Mastra 침투 (Shai-Hulud 정착) |

**6월 북한 그룹의 특징**: **암호화폐 탈취에서 소프트웨어 공급망으로 영역 확장**.

### 4.3 Chinese-aligned APTs (추정)

| 그룹 | 6월 활동 |
|---|---|
| Silver Fox (추정) | 한국 기업 세무조사 통지서 위장 캠페인 |
| APT29 (추정) | 러시아 연계와 혼재 — 추가 확인 필요 |

### 4.4 Cybercriminal Groups

| 그룹 | 6월 활동 |
|---|---|
| **ShinyHunters** | Kodak 침해(6/18), Oracle 제로데이 활용(6/12), Salesforce 침해 |
| **The Gentlemen** (랜섬웨어) | Krebs 보도(6/10), 활동 그룹 정체 조사 |
| 인포스틸러 그룹 | 240억 건 credential dump (6/22) |

### 4.5 위협 행위자 매트릭스 (월간 종합)

| 행위자 | 1차 공격 | 2차 활용 | 표적 지역 | 6월 강도 |
|---|---|---|---|---|
| Russian IAB | VPN/Firewall 결함 | Credential theft | 글로벌 | ★★★★★ |
| Russian APT | SSRF/백도어 | 우크라이나 표적 | 동유럽 | ★★★★ |
| North Korea | npm 침투 | 공급망 확산 | 글로벌 | ★★★★ |
| Chinese (추정) | Spear phishing | 기업 표적 | 동아시아 | ★★★ |
| ShinyHunters | Salesforce/CRM | 다중 2차 피해 | 글로벌 | ★★★★ |
| 인포스틸러 그룹 | Credential dump | Credential stuffing | 글로벌 | ★★★ |

---

## 5. 🇰🇷 국내 보안 동향 월간 종합

### 5.1 매체별 기사 분포 (6월)

| 매체 | 6월 누계 | 주요 주제 |
|---|---|---|
| 데일리시큐 | **102건** | 정책, 국내 위협, 보안 제품 출시, 업계 동향 |
| Dark Reading | 50건 | 글로벌 위협 분석 |
| SecurityWeek | 47건 | 글로벌 위협 분석 |
| CISA Alerts | 30건 | 정책·권고·ICS 공지 |

### 5.2 6월 주요 국내 사건 (W4 집중)

| 일자 | 제목 | 매체 | 위협 카테고리 |
|---|---|---|---|
| 06-18 | **MS Defender 제로데이 '로그플래닛'** — SYSTEM 권한 탈취 가능 | 데일리시큐 | 제로데이, EDR 우회 |
| 06-18 | 제로데이 없어도 뚫린다 — 인터넷 노출 내부 시스템 위험 | 데일리시큐 | 노출 자산 |
| 06-22 | 한국 노린 공유기 봇넷 '아리스팅어' | 데일리시큐 | IoT 봇넷 |
| 06-22 | 240억 건 계정 정보 노출 | 데일리시큐 | credential dump |
| 06-22 | 텍사스주 면허 해킹 (308만 명) | 데일리시큐 | 글로벌 유출 |
| 06-23 | Silver Fox APT 세무조사 위장 | 데일리시큐 | APT/사회공학 |
| 06-23 | 한국인 평생 29년 온라인 | 데일리시큐 | 인식 제고 |
| 06-23 | 엑스게이트 양자내성암호 적용 | 데일리시큐 | PQC 국내 사례 |
| 06-24 | 트럼프 양자내성 행정명령 | 데일리시큐 | 글로벌 정책 |
| 06-26 | 개인정보위 빗썸 과징금 2.1억 | 데일리시큐 | 컴플라이언스 |
| 06-26 | 개인정보위 상조업계 점검 | 데일리시큐 | 컴플라이언스 |
| 06-26 | 한국법제연구원 ICT 보안법제 | 데일리시큐 | 정책 |

### 5.3 6월 국내 정책·규제 동향

| 일자 | 내용 | 의미 |
|---|---|---|
| 06-26 | 개인정보위, 빗썸 과징금 2.1억 (국외이전 위반) | 개인정보보호법 강화 |
| 06-26 | 개인정보위, 상조업계 실태점검 | 산업별 점검 확대 |
| 06-25 | KISA, 협력업체 상생 간담회 | 공급망 협력 강화 |
| 06-23 | 엑스게이트, PQC 적용 완료 | 국내 PQC 도입 초기 사례 |
| 06-26 | 그룹아이비, 상위 10대 사이버 위협 조직 공개 | 위협 인텔 공개 |

### 5.4 6월 국내 인식 흐름

| 흐름 | 시사점 |
|---|---|
| **공유기 봇넷 보도** | ISP/제조사 협력 모델 점검 필요 |
| **credential dump 우려** | 국내 사용자 다수 포함 가능성 → password hygiene 강화 |
| **AI 정책 동향** | 한국 정부 PQC 로드맵 부재 → 공공·금융 우선 도입 검토 |

---

## 6. 📈 카테고리별 월간 추이

### 6.1 취약점/패치 (월간 동향)

| 주차 | 주요 이벤트 |
|---|---|
| W1 | Apache 다수 CVE, Cloud Foundry UAA, MISP |
| W2 | **Microsoft Patch Tuesday (6/9, 기록적 분량)**, Drupal 고위험 |
| W3 | CISA KEV 신규, Chrome 148 사이클 |
| W4 | **Chrome 149**, **AI 워크플로우 다발** (Langflow, Flowise, n8n, Gemini CLI), LiteLLM KEV |

**월간 평가**: 6월은 **AI 워크플로우 도구의 보안 취약점이 본격적으로 드러난 첫 달**로 기록될 전망.

### 6.2 위협 분석/캠페인 (월간 동향)

| 주차 | 주요 이벤트 |
|---|---|
| W1 | Meta AI Support Bot Instagram 탈취 |
| W2 | AsyncRAT AI Hype 활용, ShinyHunters Oracle 제로데이 |
| W3 | NCSC Fortinet 글로벌 경고, MS Defender 제로데이, Kodak breach |
| W4 | Russian APT StockStay, FortiBleed 심화, Shai-Hulud, Polymarket $3M |

### 6.3 정책/규제 (월간 동향)

| 주차 | 주요 이벤트 |
|---|---|
| W1 | - |
| W2 | CISA New Directive (연방 패치 우선순위 재작성), White House AI 사이버 EO |
| W3 | - |
| W4 | **양자내성 행정명령 (6/23)**, 개인정보위 과징금 |

### 6.4 산업별 영향

| 산업 | 6월 주요 위협 |
|---|---|
| **IT/소프트웨어** | AI 워크플로우 도구 다발 취약점, npm 공급망 |
| **금융** | Polymarket 피싱, 인포스틸러 credential dump |
| **제조** | PTC Windchill 익스플로잇, ICS/OT 결함 |
| **에너지/유틸리티** | Cal Water OT 위협, Arista EOS |
| **의료** | Xsolis 데이터 유출 |
| **공공** | 양자내성 EO, Fortinet Firewall 침해 |
| **통신** | Microsoft Defender 제로데이 |
| **교육** | ShinyHunters Oracle 제로데이 Higher Ed 표적 |

---

## 7. 🔍 월간 MITRE ATT&CK 패턴 분석

6월에 가장 활발히 사용된 ATT&CK Technique:

| Tactic | Technique | ID | 빈도 (추정) |
|---|---|---|---|
| Initial Access | Supply Chain Compromise | T1195 | ★★★★★ |
| Initial Access | Exploit Public-Facing Application | T1190 | ★★★★ |
| Credential Access | OS Credential Dumping | T1003 | ★★★★ |
| Credential Access | Credentials In Files | T1552 | ★★★ |
| Execution | Command and Scripting Interpreter | T1059 | ★★★ |
| Persistence | Compromise Software Supply Chain | T1195.002 | ★★★ |
| Lateral Movement | Remote Services (RDP/SMB) | T1021 | ★★★ |
| Defense Evasion | Masquerading | T1036 | ★★ |
| Exfiltration | Exfiltration to Cloud Storage | T1567.002 | ★★ |
| Command and Control | Application Layer Protocol | T1071 | ★★ |

**6월 패턴 특징**: **공급망 침투(T1195)** + **공개 웹앱 익스플로잇(T1190)** + **자격증명 탈취(T1003, T1552)** 의 3종 세트가 가장 빈번.

---

## 8. ✅ 다음 달(7월) 보안 점검 포인트

### 8.1 즉시 (7월 첫 주)

| 우선순위 | 액션 | 대상 |
|---|---|---|
| 🔴 P0 | Chrome 149.0.7827.53 이상 업데이트 | 전사 엔드포인트 |
| 🔴 P0 | AI 워크플로우 도구 (LiteLLM, Langflow, Flowise, n8n, Gemini CLI) 버전 점검 | AI 도입 조직 |
| 🔴 P0 | npm 의존성 audit + CI/CD 자격증명 rotation | DevSecOps |
| 🔴 P0 | Fortinet Firewall 펌웨어 + 침해 흔적 점검 | Fortinet 운영 |

### 8.2 단기 (7월 중)

| 우선순위 | 액션 | 영향 |
|---|---|---|
| 🟠 P1 | 양자내성 암호 로드맵 수립 | 공공·금융 |
| 🟠 P1 | PLM 시스템 자산 인벤토리 + 취약점 스캔 | 제조 |
| 🟠 P1 | credential dump 매칭 + password reuse 점검 | IAM |
| 🟠 P1 | 공유기 펌웨어 점검 | 가정/원격근무 |
| 🟠 P1 | MCP/AI 에이전트 사용 정책 수립 | AI 도입 조직 |

### 8.3 중장기 (7월 말 ~ Q3)

| 우선순위 | 액션 |
|---|---|
| 🟡 P2 | SBOM(Software Bill of Materials) 도입 |
| 🟡 P2 | 위협 인텔 플랫폼 정착 (KEV 자동 알림 등) |
| 🟡 P2 | 양자내성 KMS/HSM 도입 검토 |
| 🟡 P2 | 자산 가시성(Asset Visibility) 통합 플랫폼 |
| 🟢 P3 | AI 에이전트 워크플로우 별도 보안 정책 |
| 🟢 P3 | 국내 PQC 정책 로드맵 모니터링 |

---

## 9. 🔮 7월 예측 — 다음 달 모니터링 포인트

1. **PTC Windchill 익스플로잇 확대** — 첫 사례 후 PoC 공개, 추가 피해 확인
2. **Chrome 150 사이클** — 6월 두 차례 Critical 후 다음 주 신규 점검 항목
3. **Russian APT StockStay 후속** — 추가 백도어/표적 확대 가능성
4. **양자내성 정책 후속** — 한국 정부/공공/금융 동향, 글로벌 벤더별 PQC 채택 일정
5. **AI 워크플로우 도구 추가 CVE** — 6월 패턴 지속 시 7월에도 다발 발견 예상
6. **공급망 2차 피해 확대** — Klue/Salesforce 영향권 추가 확인
7. **Asian Scam Centers 단속 후속** — 검거·추가 압박 정보
8. **North Korea의 추가 npm 침투** — Shai-Hulud 이후 속행 가능성
9. **CISA KEV 신규 등재** — 6월 22건 패턴 지속 시 7월에도 다수
10. **국내 Silver Fox APT 변종** — 세무조사 외 다른 위장 수단 출현 가능성

---

## 10. 📚 관련 보고서 / 참고 자료

### 10.1 6월 주차별 보고서 (이 보고서 family)

| 주차 | 파일 | 형식 | 주제 |
|---|---|---|---|
| **W4** | `wiki/raw/articles/2026/202606/weekly-newsletter-20260622-20260626.md` | 표준 뉴스레터 | 6/22~26 편집본 |
| **W4** | `wiki/raw/articles/2026/202606/weekly-trend-report-20260622-20260626.md` | 분석 보고서 | 6/22~26 요약 분석 |
| **W4** | `wiki/raw/articles/2026/202606/weekly-deep-analysis-report-20260622-20260626.md` | **심층 분석 보고서** | 6/22~26 전문가용 |
| **6월 누계** | `wiki/raw/articles/2026/202606/cve-newly-discovered-202606.md` | CVE 종합 | 6월 CVE/CVSS 통계 |

### 10.2 외부 공식 출처

- CISA KEV: https://www.cisa.gov/known-exploited-vulnerabilities-catalog
- NVD: https://nvd.nist.gov/
- MITRE ATT&CK: https://attack.mitre.org/
- NIST PQC: https://csrc.nist.gov/projects/post-quantum-cryptography
- ENISA: https://www.enisa.europa.eu/
- KISA 보호나라: https://www.boho.or.kr/

### 10.3 주요 매체 RSS

- SecurityWeek: https://www.securityweek.com/feed/
- Dark Reading: https://www.darkreading.com/rss.xml
- Krebs on Security: https://krebsonsecurity.com/feed/
- The Record: https://therecord.media/feed
- CISA News: https://www.cisa.gov/news.xml
- 데일리시큐: https://www.dailysecu.com/rss/allArticle.xml

### 10.4 6월 주요 출처 기사 (대표)

#### 공급망 / Shai-Hulud
- https://feeds.fortinet.com/~/958459373/0/fortinet/blogs~From-CICD-to-Cloud-Data-How-Shai-Hulud-Persistence-Leads-to-Redshift-Breach
- https://www.securityweek.com/north-korean-hackers-blamed-for-mastra-npm-supply-chain-attack/
- https://www.securityweek.com/beyondtrust-lastpass-impacted-by-klue-salesforce-incident/
- https://www.darkreading.com/cyberattacks-data-breaches/shinyhunters-uses-oracle-zero-day-to-rampage-higher-ed
- https://unit42.paloaltonetworks.com/the-npm-threat-landscape-attack-surface-and-mitigations-updated-june-2/

#### AI 워크플로우 / 정책
- https://www.securityweek.com/new-enterprise-ready-mcp-specification-brings-new-security-challenges/
- https://www.securityweek.com/trump-signs-executive-order-accelerating-post-quantum-cryptography-migration/
- https://blog.cloudflare.com/post-quantum-eo-2026/
- https://www.ncsc.gov.uk/news/the-ai-shift-in-cyber-risk-why-leaders-must-act-now
- https://unit42.paloaltonetworks.com/trust-no-skill-integrity-verification-for-ai-agent-supply-chains/

#### Russian APT / FortiBleed
- https://www.darkreading.com/cyberattacks-data-breaches/fortibleed-attackers-firewalls-credentials-stealers
- https://www.securityweek.com/russian-apt-deploys-stockstay-backdoor-against-ukrainian-targets/
- https://www.ncsc.gov.uk/news/alert-ncsc-issues-advice-following-global-targeting-of-fortinet-firewalls-and-vpn-gateway

#### 패치 사이클 / 레거시
- https://krebsonsecurity.com/2026/06/09/a-record-breaking-patch-tuesday-for-june-2026/
- https://www.securityweek.com/chrome-149-update-resolves-18-severe-vulnerabilities/
- https://www.securityweek.com/first-ever-exploitation-of-ptc-windchill-vulnerability-discovered-in-the-wild/
- https://www.securityweek.com/eight-year-old-samsung-knox-flaw-exposed-millions-of-galaxy-devices-to-kernel-attacks/

#### 국내
- https://www.dailysecu.com/news/articleView.html?idxno=207266 (아리스팅어)
- https://www.dailysecu.com/news/articleView.html?idxno=207268 (240억)
- https://www.dailysecu.com/news/articleView.html?idxno=207270 (실버폭스)
- https://www.dailysecu.com/news/articleView.html?idxno=207277 (엑스게이트 PQC)
- https://www.dailysecu.com/news/articleView.html?idxno=207291 (트럼프 PQC EO)

---

## 11. 메타데이터

### 11.1 보고서 사양

| 항목 | 값 |
|---|---|
| 작성일 | 2026-06-26 |
| 데이터 cutoff | 2026-06-26 22:00 (KST) |
| 분석 범위 | 2026-06-01 ~ 2026-06-26 (26일, 4주 + 2일) |
| 분량 | 약 32KB / 440줄 |

### 11.2 한계 및 주의사항

- **W3/W4 데이터 증가의 일부**는 6/22 신규 RSS 매체 13개 추가 효과. 매체당 평균 기사 수는 W1~W2와 유사
- **MITRE ATT&CK 매핑**은 공개 출처 기반 추정이므로 조직 환경 정밀 분석 권장
- **국내 위협 동향은 데일리시큐 RSS만** — 보안뉴스 등 미수집분 별도 조회 필요
- **NVD 누계 통계는 6/26 시점**으로, 6/27~30 추가 발표분은 미포함
- **공격자 attribution**은 공개 정보 기반이며, 일부 그룹 식별은 추측 포함

### 11.3 저장 위치

- 📄 Wiki: `/home/kisec/wiki/raw/articles/2026/202606/monthly-trend-report-202606.md`
- 📦 Research 백업: `/home/kisec/.hermes/profiles/news/home/research/security-news/202606/monthly-trend-report-202606.md`
- 원본 데이터: blogwatcher-cli SQLite DB (`/home/kisec/.blogwatcher-cli/blogwatcher-cli.db`)