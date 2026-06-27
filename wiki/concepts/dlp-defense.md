---
title: DLP — 방어
created: 2026-06-12
updated: 2026-06-21
type: concept
tags: [security, glossary, dlp, data-loss-prevention, data-exfiltration, compliance, gdpr, hipaa, insider-threat]
sources: [https://ko.wikipedia.org/wiki/데이터_유출_방지, https://ko.wikipedia.org/wiki/정보_보호]
confidence: high
---
> [[dlp]]의 후반부입니다.

## 참고 URL
- [ko.wikipedia.org](https://ko.wikipedia.org/wiki/데이터_유출_방지)
- [ko.wikipedia.org](https://ko.wikipedia.org/wiki/정보_보호)

## Step 3: 전문 용어 설명 (위키백과 기반)
### 컴플라이언스 및 규제 연계 (Compliance Mapping)

| 규제/표준 | 주요 요구사항 | DLP 역할 |
|----------|--------------|----------|
| **개인정보보호법 (한국)** | 개인정보 유출 방지, 접근 통제, 암호화, 접속기록 보관 | PII(주민번호, 여권, 운전면허, 외국인등록번호) 탐지·차단·암호화, 접속 로그 |
| **GDPR (EU)** | 개인정보 보호 원칙, 데이터 주체 권리, 72시간 내 유출 신고, DPIA | EU 거주자 개인정보(이름, 이메일, IP, 쿠키 ID) 탐지, 유출 시 알림 자동화 |
| **HIPAA (미국 의료)** | PHI(보호대상 건강정보) 보호, 최소 필요 원칙, 감사 추적 | 의료기록번호, 환자명, 진단코드(ICD-10), 처방전 탐지·모니터링 |
| **PCI-DSS (결제카드)** | 카드번호(PAN) 저장/전송/처리 보호, 마스킹, 암호화 | 카드번호(Luhn 검증), 트랙 데이터, CVV 탐지·마스킹·암호화 |
| **ISMS-P (한국 인증)** | 정보보호 관리체계, 개인정보 처리단계별 보호조치 | 데이터 분류, 접근통제, 유출방지, 암호화, 로그 관리 증적 제공 |
| **NIST 800-53 / 800-171** | 통제 항목(AC, AU, SC, SI, MP) 매핑 | 데이터 분류(SC-28), 전송 보호(SC-8), 감사(AU-2), 미디어 보호(MP-4) |

### DLP 도입 시 고려사항 (Deployment Considerations)

| 단계 | 핵심 체크포인트 |
|------|-----------------|
| **1. 데이터 식별/분류** | 데이터 맵핑(어디에 뭐가 있나), 분류 체계 정의(공개/내부/기밀/최기밀), 크라운 주얼 식별 |
| **2. 정책 설계** | 부서/역할/데이터 유형별 차등 정책, 예외 처리 프로세스(승인 워크플로), 단계적 적용(모니터링→경고→차단) |
| **3. 채널 우선순위** | 고위험 채널 우선(이메일, 웹 업로드, USB), 레거시 채널(FTP, 팩스) 포함 여부 |
| **4. 성능/사용자 경험** | 엔드포인트 오버헤드(CPU/메모리/디스크 I/O), 네트워크 지연(인라인 모드), 거짓 양성으로 인한 업무 방해 최소화 |
| **5. 옵스/거버넌스** | 알림 티어링(High/Med/Low), 티켓팅 연동(ServiceNow/Jira), 주기적 정책 튜닝(오탐/미탐 분석), 분기별 리뷰 |
| **6. 법적/윤리적** | 직원 모니터링 동의/고지(취업규칙, 개인정보처리방침), 수집 최소화, 목적 외 이용 금지, 보관 기간 준수 |

### 주요 DLP 벤더 (2024 Gartner Magic Quadrant 기준)

| 벤더 | 제품군 | 강점 | 배포 형태 |
|------|--------|------|-----------|
| **Broadcom (Symantec)** | Symantec DLP | 가장 성숙, 광범위한 채널(네트워크/엔드포인트/클라우드/이메일/스토리지), 강력한 지문/ML | 온프레미스/하이브리드/클라우드 |
| **Forcepoint** | Forcepoint DLP | 사용자 행동 분석(UBA) 통합, 위험 적응형 보호, 클라우드 네이티브 | SaaS/하이브리드 |
| **Microsoft** | Purview DLP (MIP) | M365/Windows/Edge/Teams 네이티브 통합, 라벨링(AIP) 연동, 제로 트러스트 | 클라우드(SaaS) |
| **Digital Guardian (Fortra)** | Digital Guardian DLP | 데이터 인식 엔드포인트, 코드/설계도/CAD 파일 특화, 오프라인/에어갭 지원 | 온프레미스/클라우드 |
| **Netskope** | Netskope DLP | CASB 네이티브, 실시간 인라인/아웃오브밴드, 셰도우 IT 탐지 | SSE/SASE 플랫폼 |
| **Zscaler** | Zscaler DLP | 프록시 기반, SSL 검사, 클라우드 네이티브, 제로 트러스트 익스체인지 | SSE/SASE |
| **IBM** | Security Guardium DSP | DB 중심, 데이터 활동 모니터링(DAM) 강점, 메인프레임/클라우드 DB 지원 | 온프레미스/클라우드 |
| **한국: 파수닷컴** | Fasoo DLP / Document Security | 문서 보안(DRM) 강점, 한국 공공/금융 레퍼런스 다수, 화면 워터마크 | 온프레미스/클라우드 |
| **한국: 소만사** | Somansa DLP / Privacy-i | 네트워크/엔드포인트/이메일/웹 통합, 가성비, 컴플라이언스 특화 | 온프레미스/클라우드 |
| **한국: 이스트시큐리티** | 알약 DLP | 알약 AV/EDR 연계, 중소기업 대상, 쉬운 관리 | 온프레미스/클라우드 |

### MITRE ATT&CK 매핑 (DLP 탐지/차단 관련)

| Tactic | Technique ID | Technique Name | DLP 대응 |
|--------|-------------|----------------|----------|
| **Collection** | T1005 | Data from Local System | 엔드포인트 에이전트: 대량 파일 읽기/압축/복사 차단/알림 |
| | T1039 | Data from Network Shares | 파일 서버/NAS DLP: 비정상 대량 접근/다운로드 탐지 |
| | T1041 | Exfiltration Over C2 Channel | 네트워크 DLP/CASB: C2 트래픽 내 데이터 페이로드 탐지 |
| | T1567 | Exfiltration Over Web Service | CASB/프록시: 클라우드 스토리지/웹훅/코드 레포 업로드 차단 |
| **Exfiltration** | T1048 | Exfiltration Over Alternative Protocol | DNS/이메일/IM/게이밍 프로토콜 내 데이터 탐지 |
| | T1052 | Exfiltration Over Physical Medium | USB/외장하드/프린터 포트 제어, 출력물 워터마크 |
| **Impact** | T1485 | Data Destruction | 중요 파일 삭제/암호화/변조 시도 탐지(랜섬웨어/와이퍼) |
| | T1486 | Data Encrypted for Impact | 대량 파일 엔트로피 상승/확장자 변경/랜섬 노트 생성 탐지 |

---


## 관련 위키 링크

- [[edr]] — EDR (엔드포인트 행위 모니터링과 DLP 연계: 파일리스 유출 탐지)
- [[command-and-control]] — C2 (C2 채널을 통한 데이터 유출 탐지)
- [[actions-on-objectives]] — 목표 달성 (데이터 유출이 공격자 최종 목적)
- [[real-world-breach-cases]] — 실제 침해 사례 (데이터 유출 사례 분석: Capital One, Equifax, Marriott 등)
- [[exploitation]] — 익스플로잇 (취약점 악용 후 데이터 수집/유출 단계)

---

## 참고 문헌

- 한국어 위키백과: [데이터 유출 방지](https://ko.wikipedia.org/wiki/데이터_유출_방지)
- 한국어 위키백과: [정보 유출](https://ko.wikipedia.org/wiki/정보_유출)
- 한국어 위키백과: [개인정보보호법](https://ko.wikipedia.org/wiki/개인정보보호법)
- 한국어 위키백과: [GDPR](https://ko.wikipedia.org/wiki/GDPR)
## 관련 위키 링크
- [[dlp]] — 인덱스 페이지
- [[dlp-core]] — 분할 페이지
- [[rce]]
