---
title: Reconnaissance (정찰) — 사이버 공격의 첫 단계, 정보 수집의 기술
created: 2026-06-12
updated: 2026-06-21
type: concept
tags: [security, glossary, reconnaissance, recon, cyber-kill-chain, mitre-attck, osint, passive-recon, active-recon]
sources: [https://ko.wikipedia.org/wiki/사이버_킬_체인, https://ko.wikipedia.org/wiki/포트_스캔, https://ko.wikipedia.org/wiki/오픈_소스_인텔리전스, https://ko.wikipedia.org/wiki/MITRE_ATT%26CK, https://ko.wikipedia.org/wiki/사회공학_(보안), https://ko.wikipedia.org/wiki/취약점_스캐너]
confidence: high
---

# Reconnaissance (정찰) — 사이버 공격의 첫 단계, 정보 수집의 기술

## 참고 URL
- [ko.wikipedia.org](https://ko.wikipedia.org/wiki/사이버_킬_체인)
- [ko.wikipedia.org](https://ko.wikipedia.org/wiki/포트_스캔)
- [ko.wikipedia.org](https://ko.wikipedia.org/wiki/오픈_소스_인텔리전스)
- [ko.wikipedia.org](https://ko.wikipedia.org/wiki/MITRE_ATT%26CK)
- [ko.wikipedia.org](https://ko.wikipedia.org/wiki/사회공학_(보안))
- [ko.wikipedia.org](https://ko.wikipedia.org/wiki/취약점_스캐너)

## Step 1: 단어 직역 및 쉬운 비유

### 1. 약자 풀이
**Reconnaissance** = **Recon** (군사/보안 현장 약어)
→ 풀네임: **Reconnaissance** (프랑스어 *reconnaître*에서 유래)

| 영어 단어 | 직역 | 의미 |
|-----------|------|------|
| **Re-** | 다시, 반복적으로 | 지속적이고 반복적인 |
| **Connaissance** | 지식, 앎, 인식 | 정보를 수집하여 아는 것 |
| **Reconnaissance** | 정찰, 수색, 탐지 | **목표에 대한 정보를 체계적으로 수집하는 행위** |

### 2. 의미 조합
> **공격자가 실제 침투(Exploitation) 전에 대상 시스템/네트워크/조직에 대해 공개·비공개 정보를 체계적으로 수집·분석하여 공격 표면(Attack Surface)을 파악하는 사전 작업 단계**

### 3. 강력한 비유: "은행 털기 전, 은행 지도를 그리고 경비원 근무표를 외우는 도둑"

- **은행 = 타겟 시스템/조직 (서버, 네트워크, 직원, 물리 시설)**
- **도둑 = 공격자 (해커, 레드팀, APT 그룹)**
- **은행 외부에서 망원경으로 건물 구조 살핌 = 수동적 정찰 (Passive Recon)**
  - 도메인/서브도메인 열거, DNS 레코드 조회, SSL 인증서 분석, 공개된 직원 정보(LinkedIn), 기술 스택 식별(Wappalyzer), Shodan/Censys 검색
- **은행 정문 앞에서 경비원에게 "계좌 개설하러 왔어요"라며 내부 들여다봄 = 능동적 정찰 (Active Recon)**
  - 포트 스캔(Nmap), 서비스 버전 탐지, 디렉터리 열거(Dirb/Gobuster), API 엔드포인트 탐색, 로그인 페이지 테스트, 소셜 엔지니어링(피싱 메일 발송)
- **버려진 영수증·명함 줍기 = OSINT (Open Source Intelligence)**
  - 쓰레기통 뒤지기(Dumpster Diving) ↔ GitHub 공개 리포에서 하드코딩된 키 찾기, 페이스북/트위터 직원 게시물 분석, 채용공고로 기술 스택 유추
- **경비원 근무 교대 시간·CCTV 사각지대 파악 = 공격 벡터 식별**
  - 열린 포트/서비스 버전 → 알려진 CVE 매핑, 잘못된 권한 설정, 기본 비밀번호, 패치 안 된 소프트웨어, 노출된 관리 인터페이스

**핵심 포인트**: **아직 한 푼도 훔치지 않았는데(침투 안 함), 이미 은행 금고 위치·경비 인원·알람 코드·직원 점심시간까지 다 알고 있는 상태**입니다. 이게 바로 정찰(Reconnaissance) — **공격의 80%는 정찰에서 결정난다**는 말이 있을 정도입니다.

---

## Step 2: 개념 시각화

![Reconnaissance 비유 시각화: 공격자(정찰자), 타겟 시스템(대상 집), 수동적 정찰(망원경 관찰), 능동적 정찰(문 두드리기), 공개 정보(우편함/쓰레기통), 네트워크 정보(와이파이 신호), 방어 시스템(CCTV) - 한글 레이블 포함](https://v3b.fal.media/files/b/0a9df883/s8lx5tEO7AalatS1zY18K_sY5xQgS1.png)

**이미지 설명**:
- **공격자(정찰자)** — 목표 정보를 수집하는 주체
- **타겟 시스템(대상 집)** — 공격 대상 인프라/조직
- **수동적 정찰(망원경 관찰)** — 직접 접촉 없이 공개 정보만 수집 (DNS, SSL, Shodan, LinkedIn 등)
- **능동적 정찰(문 두드리기)** — 대상과 직접 상호작용하며 정보 수집 (포트 스캔, 디렉터리 열거, 피싱 등)
- **공개 정보(우편함/쓰레기통)** — OSINT 소스 (GitHub, 채용공고, SNS, 문서 메타데이터 등)
- **네트워크 정보(와이파이 신호)** — 네트워크 토폴로지, 서비스 배너, 인증서, 헤더 등
- **방어 시스템(CCTV)** — 탐지/차단 장치 (IDS/IPS, WAF, SIEM, 허니팟 등) — 정찰 행위 자체가 로그에 남을 수 있음

> ⚠️ **참고**: 이미지 생성 도구가 PNG 형식으로 반환했습니다. 스킬 요구사항(.jpg/.jpeg)은 현재 도구 제약상 PNG로 대체됩니다.

---

## Step 3: 전문 용어 설명 (Wikipedia 기반)

### 정찰(Reconnaissance, 사이버 보안)

**정의**: 사이버 공격 생명주기(Cyber Kill Chain)의 **첫 번째 단계**로, 공격자가 대상 시스템·네트워크·조직에 대해 **공격 계획을 수립하기 위한 정보를 체계적으로 수집·분석하는 과정**이다.

### 분류: 수동적 vs 능동적 정찰

| 구분 | 수동적 정찰 (Passive Reconnaissance) | 능동적 정찰 (Active Reconnaissance) |
|------|-----------------------------------|--------------------------------|
| **정의** | 대상과 **직접 통신하지 않고** 공개/제3자 소스에서 정보 수집 | 대상 시스템과 **직접 상호작용**하며 정보 수집 |
| **특징** | 탐지 어려움, 로그 미남김, 법적 리스크 낮음 | 탐지 가능(IDS/IPS, 방화벽 로그), 소음 발생, 법적 리스크 존재 |
| **주요 기법** | • OSINT (Open Source Intelligence)<br>• DNS 열거 (Zone Transfer, Subdomain Bruteforce)<br>• SSL/TLS 인증서 투명성 로그 (crt.sh)<br>• 검색 엔진 드로킹 (Google Dorks)<br>• Shodan/Censys/ZoomEye 검색<br>• 소셜 미디어/채용공고 분석<br>• GitHub/GitLab 공개 리포 스캔<br>• 메타데이터 분석 (문서, 이미지 EXIF) | • 포트 스캔 (Nmap, Masscan, Zmap)<br>• 서비스/버전 탐지 (-sV)<br>• OS 핑거프린팅 (-O)<br>• 디렉터리/파일 열거 (Gobuster, Dirb, Feroxbuster)<br>• 취약점 스캔 (Nessus, OpenVAS, Nuclei)<br>• 웹 애플리케이션 크롤링<br>• 소셜 엔지니어링 (피싱, 비싱, 프리텍스팅)<br>• 무선 네트워크 스캐닝 (Airodump-ng) |
| **대표 도구** | theHarvester, Recon-ng, Amass, Subfinder, Sublist3r, SpiderFoot, Maltego, Sherlock, GHDB | Nmap, Masscan, Zmap, Nessus, OpenVAS, Nuclei, Nikto, WPScan, sqlmap, Burp Suite, Metasploit Auxiliary |

### MITRE ATT&CK 매핑 (Enterprise Matrix)

| Tactic | Technique ID | Technique Name | 설명 |
|--------|-------------|----------------|------|
| **Reconnaissance** | **T1590** | Active Scanning | 대상 네트워크/시스템 직접 스캔 |
| | **T1590.001** | Scanning IP Blocks | IP 대역 스캔 |
| | **T1590.005** | Vulnerability Scanning | 취약점 스캔 |
| | **T1592** | Gather Victim Host Information | 호스트 정보 수집 |
| | **T1592.001** | Hardware | 하드웨어 정보 |
| | **T1592.002** | Software | 소프트웨어/버전 정보 |
| | **T1592.003** | Firmware | 펌웨어 정보 |
| | **T1592.004** | Client Configurations | 클라이언트 설정 |
| | **T1593** | Search Open Technical Databases | 기술 데이터베이스 검색 |
| | **T1593.001** | DNS/Passive DNS | DNS/패시브 DNS |
| | **T1593.002** | Certificates | SSL 인증서 |
| | **T1593.003** | WHOIS | WHOIS 레코드 |
| | **T1594** | Search Victim-Owned Websites | 피해자 소유 웹사이트 검색 |
| | **T1595** | Active Directory Reconnaissance | AD 환경 정찰 |
| | **T1596** | Search Open-Source Intelligence | OSINT 수집 |
| | **T1596.001** | Social Media | 소셜 미디어 |
| | **T1596.002** | Code Repositories | 코드 저장소 |
| | **T1596.003** | Job Postings | 채용 공고 |
| | **T1597** | Search Closed-Source Intelligence | 비공개 정보 수집 |
| | **T1598** | Phishing for Information | 정보를 위한 피싱 |

### 정찰 단계에서 수집하는 핵심 정보 (Attack Surface Mapping)

| 정보 카테고리 | 구체적 항목 | 활용 목적 |
|--------------|-------------|----------|
| **네트워크 인프라** | IP 대역, 서브넷, 라우터/방화벽, VPN, 로드밸런서 | 침투 경로 설계, 측면 이동 경로 파악 |
| **도메인/DNS** | 메인 도메인, 서브도메인, DNS 레코드(A, MX, TXT, CNAME), Zone Transfer 가능 여부 | 서브도메인 탈취, 이메일 스푸핑, 내부 네트워크 매핑 |
| **웹 애플리케이션** | 기술 스택(CMS, 프레임워크, 언어), 버전, 디렉터리 구조, API 엔드포인트, 입력 포인트 | 기존 CVE 매핑, 인젝션/파일 업로드/인증 우회 테스트 |
| **서비스/포트** | 열린 포트, 서비스명/버전, 배너 그래빙 결과, 기본 크리덴셜 여부 | 원격 코드 실행(RCE), 권한 상승, 횡적 이동 |
| **인증/권한** | 로그인 페이지, SSO/OAuth 공급자, MFA 유무, 비밀번호 정책, 계정 잠금 임계값 | 크리덴셜 스터핑, 패스워드 스프레이, 세션 하이재킹 |
| **사람/조직** | 직원 이름/이메일/직책, 조직도, 사용 SW/하드웨어, 보안 솔루션, 패치 주기 | 스피어 피싱, 소셜 엔지니어링, 공급망 공격 |
| **유출/노출 데이터** | 과거 데이터 유출 건수, 유출된 크리덴셜, API 키, 인증서, 내부 문서 | 크리덴셜 재사용, 권한 상승, 지속성 확보 |

### 방어 관점: 정찰 탐지 및 완화

| 방어 계층 | 대응 방안 |
|-----------|-----------|
| **네트워크** | IDS/IPS 시그니처 (포트 스캔 패턴 탐지), NetFlow/Zeek 트래픽 분석, 허니팟/허니토큰 배치, Rate Limiting (스캔 속도 제한) |
| **호스트/엔드포인트** | EDR 프로세스/네트워크 연결 모니터링, 불필요한 서비스/포트 비활성화, 방화벽 아웃바운드 차단 |
| **웹/애플리케이션** | WAF (스캐너 User-Agent 차단, 비정상 요청 패턴 탐지), robots.txt 민감 경로 미노출, 에러 메시지 정보 노출 방지 |
| **DNS/도메인** | Zone Transfer 제한 (AXFR 차단), DNSSEC 적용, 서브도메인 와일드카드 최소화, CAA 레코드 설정 |
| **인적/조직** | 소셜 미디어 가이드라인, 채용공고 기술 스택 상세 기재 금지, 피싱 시뮬레이션 훈련, 정보 분류/취급 절차 |
| **위협 인텔리전스** | 자산 공격 표면 지속 모니터링 (ASM 도구), 다크웹/텔레그램 유출 크리덴셜 모니터링, 취약점 패치 우선순위화 (EPSS/CVSS) |

---

### 출처
- 한국어 위키백과: ["사이버 킬 체인"](https://ko.wikipedia.org/wiki/사이버_킬_체인) — 정찰 단계 설명
- 한국어 위키백과: ["포트 스캔"](https://ko.wikipedia.org/wiki/포트_스캔) — 능동적 정찰 대표 기법
- 한국어 위키백과: ["OSINT"](https://ko.wikipedia.org/wiki/오픈_소스_인텔리전스) — 수동적 정찰/공개 정보 수집
- 한국어 위키백과: ["MITRE ATT&CK"](https://ko.wikipedia.org/wiki/MITRE_ATT%26CK) — Reconnaissance tactic 상세
- 한국어 위키백과: ["사회공학 (보안)"](https://ko.wikipedia.org/wiki/사회공학_(보안)) — 능동적 정찰의 인적 요소
- 한국어 위키백과: ["취약점 스캐너"](https://ko.wikipedia.org/wiki/취약점_스캐너) — 자동화된 정찰 도구

---

## 관련 위키 링크
- [[rce]] — RCE (원격 코드 실행) — 정찰 후 익스플로잇으로 이어지는 치명적 취약점
- [[sql-injection]] — SQL Injection — 정찰에서 발견된 입력 포인트 대상 공격
- [[xss]] — XSS — 정찰에서 발견된 클라이언트 사이드 취약점
- [[prompt-injection-ctf]] — 프롬프트 인젝션 — LLM 대상 정찰/공격 유사 기법
