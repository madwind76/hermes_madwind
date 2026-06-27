---
title: EDR — 운영
created: 2026-06-12
updated: 2026-06-21
type: concept
tags: [security, glossary, edr, endpoint, detection, response, xdr, mdr, antivirus, epp]
sources: [https://ko.wikipedia.org/wiki/엔드포인트_탐지_및_대응, https://ko.wikipedia.org/wiki/안티바이러스_소프트웨어]
confidence: high
---
> [[edr]]의 후반부입니다.

## 참고 URL
- [ko.wikipedia.org](https://ko.wikipedia.org/wiki/엔드포인트_탐지_및_대응)
- [ko.wikipedia.org](https://ko.wikipedia.org/wiki/안티바이러스_소프트웨어)

## Step 3: 전문 용어 설명 (위키백과 기반)
### 자동 대응 (Response Actions) 유형

| 대응 액션 | 설명 | 주의사항 |
|----------|------|----------|
| **네트워크 격리 (Quarantine)** | 단말을 별도 VLAN/방화벽 정책으로 격리, 관리 콘솔만 통신 허용 | 업무 중단 최소화 위해 필수 서비스(업데이트, 관리) 허용 목록 필요 |
| **프로세스 종료 (Process Kill)** | 악성 프로세스 트리 전체 종료 (자식 프로세스 포함) | 정상 프로세스 오탐 시 서비스 장애 가능 → 시뮬레이션 모드 테스트 필수 |
| **파일 격리/삭제 (File Quarantine/Delete)** | 악성 파일 원격 격리(백업 후 삭제) 또는 완전 삭제 | 롤백 기능 제공 제품 선호 (랜섬웨어 복구용) |
| **호스트 롤백 (Host Rollback)** | 랜섬웨어 암호화 파일 원상 복구 (VSS, 스냅샷, 저널 활용) | SentinelOne, Cortex XDR, Microsoft Defender 등에서 제공 |
| **사용자 세션 종료 / 패스워드 리셋** | 침해된 계정 세션 무효화, 강제 패스워드 변경 | AD/Entra ID 연동 필요 |
| **스크립트/명령 실행** | 사용자 정의 복구 스크립트 실행 (레지스트리 복구, 서비스 재시작 등) | 승인 워크플로 권장 |

### MITRE ATT&CK 매핑 (EDR 관련 주요 기법 탐지)

| Tactic | Technique ID | Technique Name | EDR 탐지 포인트 |
|--------|-------------|----------------|-----------------|
| **Execution** | T1059.001 | PowerShell | 스크립트 블록 로깅(4104), AMSI, 모듈 로드 |
| | T1059.003 | Windows Command Shell | 프로세스 생성(4688), 인수 분석 |
| | T1059.005 | Visual Basic | 매크로 실행, wscript/cscript |
| **Persistence** | T1547.001 | Registry Run Keys | 레지스트리 변경 모니터링 |
| | T1053.005 | Scheduled Task | 작업 스케줄러 이벤트(4698/4702) |
| **Privilege Escalation** | T1055 | Process Injection | OpenProcess, WriteProcessMemory, CreateRemoteThread |
| | T1003.001 | LSASS Memory | lsass.exe 접근(OpenProcess PROCESS_VM_READ), Sekurlsa |
| **Defense Evasion** | T1027 | Obfuscated Files | 엔트로피, 패킹 탐지, 메모리 스캔 |
| | T1070.004 | File Deletion | 파일 삭제 감사(4660/4663), USN 저널 |
| | T1562.001 | Disable Security Tools | 서비스 중단, 레지스트리 변경, WMI 이벤트 |
| **Credential Access** | T1003 | OS Credential Dumping | LSASS, SAM, NTDS.dit, DPAPI |
| | T1558.003 | Kerberoasting | TGS 요청(4769) 이상 패턴, RC4_HMAC |
| **Discovery** | T1082 | System Information Discovery | systeminfo, whoami, net view, AD 쿼리 |
| | T1018 | Remote System Discovery | 포트 스캔, SMB 세션, RPC 바인딩 |
| **Lateral Movement** | T1021.004 | Pass the Hash | NTLM 인증(Type 3), 세션 생성(4624 LogonType 9) |
| | T1021.002 | SMB/Windows Admin Shares | IPC$/ADMIN$ 연결, 파일 복사 |
| **Collection** | T1005 | Data from Local System | 대량 파일 읽기/압축/암호화 |
| | T1039 | Data from Network Shares | SMB 트래픽 폭증, 비정상 접근 |
| **Command and Control** | T1071.001 | Web Protocols | 비콘 주기성, JA3, 도메인 평판 |
| | T1573.001 | Encrypted Channel | TLS 인증서 분석, SNI, 인증서 투명성 |
| **Exfiltration** | T1041 | Exfiltration Over C2 | 업로드 트래픽 패턴, 청크 분할 |
| | T1567.002 | Exfiltration to Cloud Storage | rclone, azcopy, aws s3 cp 실행 |
| **Impact** | T1486 | Data Encrypted for Impact | 대량 파일 변경(엔트로피 상승), 확장자 변경, 랜섬 노트 생성 |

### 주요 EDR 벤더 및 제품 (2024년 기준)

| 벤더 | 제품명 | 특징 | 배포 형태 |
|------|--------|------|-----------|
| **CrowdStrike** | Falcon Insight / Falcon Complete | 클라우드 네이티브, 경량 에이전트, 위협 인텔리전스 강점, 매니지드 서비스(MDR) | SaaS |
| **Microsoft** | Defender for Endpoint (MDE) | Windows 네이티브 통합, M365 생태계 연동, ATT&CK 매핑 우수, 자동 조사 | 클라우드/하이브리드 |
| **SentinelOne** | Singularity Platform | 자율형 AI, 롤백(랜섬웨어 복구) 강점, 온프레미스/에어갭 지원 | SaaS/온프레미스 |
| **Palo Alto Networks** | Cortex XDR / XSIAM | 네트워크+엔드포인트+클라우드 통합, XSIAM으로 SOC 자동화 | SaaS |
| **Trend Micro** | Vision One (Apex One) | 다계층 탐지, 가상 패치, 취약점 쉴드 | SaaS/온프레미스 |
| **Elastic** | Elastic Defend / Elastic Security | 오픈코어(Elastic Stack 기반), SIEM+EDR 통합, 룰 커스터마이징 자유도 높음 | SaaS/온프레미스/하이브리드 |
| **Cisco (Secure Endpoint)** | Secure Endpoint (구 AMP) | 탈레스/시스코 탈로스 인텔리전스, 네트워크 텔레메트리 연계 | SaaS |
| **VMware (Carbon Black)** | Carbon Black Cloud | 행위 기반, 컨테이너/워크로드 보안, VMware 생태계 통합 | SaaS |
| **한국: 안랩** | AhnLab EDR | 국내 환경 최적화, 한글 지원, 공공기관 레퍼런스 다수 | 온프레미스/클라우드 |
| **한국: 이스트시큐리티** | 알약 EDR | 알약 AV 연계, 가성비, 중소기업 대상 | 온프레미스/클라우드 |

### EDR 도입 시 고려사항 (구축/운영)

| 영역 | 체크포인트 |
|------|------------|
| **에이전트 배포** | GPO/MECM/Intune/Jamf 활용, 예외 그룹(서버/레거시/OT) 분리, 재부팅 관리 |
| **성능 영향** | CPU/메모리/디스크/네트워크 오버헤드 벤치마크(보통 1~3% CPU, 100~300MB RAM) |
| **알림 피로도** | 티어링(High/Medium/Low), 억제 규칙, 자동 티켓팅(ServiceNow/Jira) 연동 |
| **로그 보관** | 핫(실시간/7~30일) + 웜(90~180일) + 콜드(1년+) 계층, 압축/파티션 전략 |
| **개인정보/컴플라이언스** | PII 수집 최소화(사용자명 마스킹), GDPR/개인정보보호법 준수, 데이터 소재국 |
| **통합** | SIEM(Splunk/Elastic/QRadar), SOAR, 티켓팅, ITSM, 위협 인텔리전스(TIP), NAC, 방화벽 |
| **운영 인력** | 티어 1(트리아지), 티어 2(분석/대응), 티어 3(헌팅/포렌식/룰 튜닝), 24/7 SOC 여부 |
| **테스트/검증** | ATT&CK 평가(Atomic Red Team, Caldera), 레드팀 연습, 시뮬레이션 모드 검증 |

---


## 관련 위키 링크

- [[command-and-control]] — C2 (EDR이 탐지하는 주요 공격 단계)
- [[exploitation]] — 익스플로잇 (EDR이 행위 분석으로 탐지)
- [[installation]] — 설치/지속성 (EDR이 레지스트리/태스크/서비스 변경 탐지)
- [[actions-on-objectives]] — 목표 달성 (랜섬웨어/데이터 유출 탐지 및 롤백)
- [[real-world-breach-cases]] — 실제 침해 사례 (EDR 탐지/대응 사례 분석)

---

## 참고 문헌

- 한국어 위키백과: [엔드포인트 탐지 및 대응](https://ko.wikipedia.org/wiki/엔드포인트_탐지_및_대응)
- 한국어 위키백과: [엔드포인트 보안](https://ko.wikipedia.org/wiki/엔드포인트_보안)
- 한국어 위키백과: [안티바이러스](https://ko.wikipedia.org/wiki/안티바이러스)
- 한국어 위키백과: [확장 탐지 및 대응](https://ko.wikipedia.org/wiki/확장_탐지_및_대응)
## 관련 위키 링크
- [[edr]] — 인덱스 페이지
- [[edr-core]] — 분할 페이지
- [[rce]]
