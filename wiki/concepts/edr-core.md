---
title: EDR — 핵심
created: 2026-06-12
updated: 2026-06-13
type: concept
tags: [security, glossary, edr, endpoint, detection, response, xdr, mdr, antivirus, epp]
sources: [https://ko.wikipedia.org/wiki/엔드포인트_탐지_및_대응, https://ko.wikipedia.org/wiki/안티바이러스_소프트웨어]
confidence: high
---

# EDR (Endpoint Detection and Response, 엔드포인트 탐지 및 대응) — 보안 용어 해설

## Step 1: 단어 직역 및 쉬운 비유

### 1. 약자 풀이

**EDR** = **E**ndpoint **D**etection **R**esponse

| 약자 | 원래 단어 | 직역 | 의미 |
|------|-----------|------|------|
| **E** | **Endpoint** | 끝점, 단말 | 네트워크에 연결된 단말 기기 (PC, 서버, 모바일, IoT) |
| **D** | **Detection** | 탐지, 감지 | 위협이나 이상 징후를 발견함 |
| **R** | **Response** | 대응, 반응 | 탐지된 위협에 대해 조치함 |

### 2. 의미 조합

> **"엔드포인트(단말)에서 발생하는 모든 행위를 실시간 모니터링하여 위협을 탐지하고, 자동/수동으로 대응·차단·조사하는 통합 보안 솔루션"**

### 3. 강력한 비유: "건물 구석구석 CCTV와 동작감지센서, 자동 잠금장치를 갖춘 슈퍼 경비원"

```
┌────────────────────────────────────────────────────────────┐
│  상황: 회사 건물(네트워크)에 직원들(사용자/프로세스)이       │
│  드나드는데, 기존 경비(백신)는 "수배자 명단(시그니처)"만   │
│  확인하고 통과시킴. EDR은 다른 차원의 경비원임             │
└────────────────────────────────────────────────────────────┘

🛡️  **EDR 경비원의 4가지 초능력**

  ① **전지전능한 눈(가시성/Visibility)**: 
      "건물 모든 방(엔드포인트) 천장에 4K 카메라 설치" → 
      프로세스 실행, 파일 읽기/쓰기, 네트워크 연결, 레지스트리 변경, 
      메모리 할당, DLL 로드, 파워셸/스크립트 실행 **모든 행위 실시간 기록**

  ② **행동 분석가(행위 탐지/Behavioral Detection)**: 
      "수배자 얼굴(시그니처) 몰라도, 수상한 행동 하면 바로 포착" → 
      "word.exe가 powershell 실행 → cmd로 whoami → lsass 메모리 덤프" 
      = **자격증명 탈취 시도** 로 판단 (MITRE ATT&CK 매핑)

  ③ **자동 소방관(자동 대응/Automated Response)**: 
      "불나면(탐지되면) 즉시 스프링클러(격리) 작동" → 
      - 네트워크 격리(Quarantine): 해당 단말만 네트워크 차단
      - 프로세스 종료(Kill): 악성 프로세스 트리 전체 종료
      - 파일 격리/삭제: 악성 파일 원격 삭제
      - 롤백(Rollback): 랜섬웨어 암호화 파일 원상 복구 (일부 제품)

  ④ **탐정(위협 헌팅/Threat Hunting & 포렌식/Forensics)**: 
      "과거 CCTV 돌려보며 침투 경로 추적" → 
      - 타임라인 재구성: 최초 침투 → 수평 이동 → 데이터 유출 전 과정
      - IOC 추출: 해시, IP, 도메인, 파일 경로, 레지스트리 키
      - 헌팅 쿼리: "지난 30일간 mshta.exe가 자식 프로세스 생성한 사례 모두 찾아줘"

💡 **핵심 포인트**: 기존 백신(EPP/AV)은 **"알려진 악성코드 차단(시그니처)"**이 주목적이지만, 
EDR은 **"알려지지 않은 위협까지 행위로 탐지 + 대응 + 조사"**가 목적입니다. 
**"예방(Prevention) → 탐지(Detection) → 대응(Response)"** 전 주기 커버.
```

---

## Step 2: 개념 시각화

![EDR 비유 시각화: 슈퍼 경비원으로 설명하는 EDR — EDR 에이전트(감시자), 엔드포인트(노트북/서버/폰), 실시간 대시보드, 행위 분석, 자동 격리, 위협 헌팅, 포렌식 기록 - 한글 레이블 포함](https://v3b.fal.media/files/b/0a9dfe1e/aymYMpvBhTAp8n6sTk1b2_N9wEhVmd.png)

**이미지 설명**:
- **EDR 에이전트(감시자)** — 각 엔드포인트에 설치된 경량 센서, 커널 레벨 후킹으로 모든 행위 수집
- **엔드포인트(노트북/서버/폰)** — 보호 대상 단말 (Windows, Linux, macOS, 모바일, 컨테이너)
- **실시간 대시보드** — 중앙 관리 콘솔, 알림/경보, 단말 상태, 탐지 현황
- **행위 분석** — 머신러닝/규칙 기반 이상 행위 탐지, MITRE ATT&CK 매핑
- **자동 격리** — 네트워크 쿼런틴, 프로세스 킬, 파일 삭제, 롤백
- **위협 헌팅** — 가설 기반 능동적 위협 탐색, 쿼리 언어(KQL, SQL-like)
- **포렌식 기록** — 전체 행위 로그 저장(보통 30~90일), 타임라인 재구성

> ⚠️ **참고**: 이미지 생성 도구가 PNG 형식으로 반환했습니다. 스킬 요구사항(.jpg/.jpeg)은 현재 도구 제약상 PNG로 대체됩니다.

---

## Step 3: 전문 용어 설명 (위키백과 기반)
### EDR (Endpoint Detection and Response, 엔드포인트 탐지 및 대응)

**정의**: **EDR(Endpoint Detection and Response)**은 엔드포인트(데스크톱, 노트북, 서버, 모바일 기기 등)에서 발생하는 **모든 행위(프로세스, 파일, 네트워크, 레지스트리, 메모리 등)를 지속적으로 모니터링·수집·분석하여, 위협을 탐지하고 자동·수동 대응하며, 사후 조사(포렌식) 및 위협 헌팅을 지원하는 엔드포인트 보안 솔루션**이다. Gartner가 2013년 용어를 정의하며 시장이 형성되었다.

### EDR의 4대 핵심 기능 (Gartner 정의 기반)

| 기능 영역 | 설명 | 세부 역량 |
|----------|------|-----------|
| **탐지 (Detection)** | 알려진/알려지지 않은 위협 식별 | 시그니처, 머신러닝, 행위 분석, 익스플로잇 차단, 파일리스 공격 탐지, MITRE ATT&CK 매핑 |
| **조사 (Investigation)** | 알림 트리아지, 근본 원인 분석 | 타임라인 뷰, 프로세스 트리, 네트워크 연결, 파일/레지스트리 변경, IoC 연계 |
| **대응 (Response)** | 위협 차단 및 복구 | 격리(Network Quarantine), 프로세스 종료, 파일 삭제/격리, 롤백, 스크립트 실행, 원격 셸 |
| **헌팅 (Threat Hunting)** | 능동적 위협 탐색 | 가설 기반 쿼리, MITRE 기법 검색, 퇴행적 분석(RETROHUNT), 커스텀 탐지 룰 작성 |

### EDR vs EPP (Endpoint Protection Platform) vs XDR

| 비교 항목 | **EPP (차세대 백신)** | **EDR** | **XDR (Extended Detection & Response)** |
|----------|----------------------|---------|------------------------------------------|
| **주 목적** | 예방(Prevention) - 알려진/일부 미지 위협 차단 | 탐지·대응·조사 - 사후 가시성 확보 | 통합 탐지·대응 - 다중 텔레메트리 연관 분석 |
| **탐지 방식** | 시그니처, 휴리스틱, ML(파일 중심) | 행위 분석, ML, 익스플로잇 차단 (행위 중심) | 엔드포인트+네트워크+클라우드+이메일+ID 연관 |
| **대응** | 차단, 격리(파일) | 격리(네트워크/프로세스), 킬, 롤백, 조사 | 플랫폼 간 자동화된 연계 대응(SOAR) |
| **가시성** | 단말 내 파일/프로세스 | 단말 전체 행위(커널 레벨) | 전체 IT 인프라 통합 가시성 |
| **헌팅** | 미지원/제한적 | 핵심 기능 (쿼리, 타임라인) | 고도화 (크로스 도메인 헌팅) |
| **대표 제품** | CrowdStrike Falcon Prevent, Microsoft Defender AV, SentinelOne Core | CrowdStrike Falcon Insight, Microsoft Defender for Endpoint, SentinelOne, Cortex XDR, Elastic Defend | Palo Alto Cortex XDR, Microsoft Defender XDR, CrowdStrike Falcon XDR, Trend Vision One |

> **관계**: EPP ⊂ EDR ⊂ XDR (최신 제품은 대부분 EPP+EDR 통합 제공, XDR로 확장 중)

### EDR 아키텍처 핵심 구성요소

| 구성요소 | 역할 | 기술적 구현 |
|----------|------|-------------|
| **에이전트 (Agent/센서)** | 단말 설치, 행위 수집, 로컬 정책 수행 | 커널 드라이버(미니필터, ETW, eBPF), 유저모드 후킹, 메모리 스캔 |
| **수집 파이프라인** | 이벤트 수집·정규화·압축·전송 | Kafka, gRPC, 프로토콜 버퍼, 대역폭 조절, 오프라인 버퍼링 |
| **중앙 콘솔/백엔드** | 저장, 상관관계 분석, 알림, API | 시계열 DB(InfluxDB, Timescale), 그래프 DB(Neo4j), ES/ELK, 클라우드 네이티브 |
| **분석 엔진** | 룰 매칭, ML 추론, 상관관계, ATT&CK 매핑 | 시그마/야라 룰, 온프레미스/클라우드 ML, 스트림 처리(Flink, Kafka Streams) |
| **대응 오케스트레이션** | 자동/반자동 플레이북 실행 | SOAR 통합, API 기반 원격 조치, 롤백 엔진(VSS, 스냅샷) |

### 주요 탐지 기법

| 기법 | 설명 | 예시 |
|------|------|------|
| **시그니처/IOC 매칭** | 알려진 악성 파일 해시, IP, 도메인, 레지스트리 | YARA, ClamAV, STIX/TAXII 피드 |
| **머신러닝 (정적/동적)** | 파일 특징/행위 벡터화 → 악성 확률 산출 | LightGBM, XGBoost, 딥러닝(CNN/Transformer) |
| **행위 기반 (Behavioral)** | 프로세스 트리, API 호출 시퀀스, MITRE 기법 매핑 | `winword.exe → powershell.exe → cmd.exe → whoami` → T1059.001 |
| **익스플로잇 차단 (Exploit Prevention)** | 메모리 보호 우회 시도 차단 (ROP, 스택 피벗, 힙 스프레이) | EMET/CFP 계승, CET/Shadow Stack 활용 |
| **파일리스/메모리 탐지** | 디스크 없는 공격(파워셸, WMI, .NET 어셈블리 로드) 탐지 | AMSI 연동, ETW 모니터링, 메모리 스캔(YARA) |
| **자격증명 접근 탐지** | LSASS 메모리 읽기, DCSync, 패스더해시, NTLM 릴레이 | `sekurlsa::logonpasswords`, `lsadump::dcsync` |


## 관련 위키 링크
- [[edr]] — 인덱스 페이지
- [[edr-defense]] — 분할 페이지
- [[rce]]
