---
title: 실제 침해 사례 — APT / 데이터 유출 (Part 1)
created: 2026-06-13
updated: 2026-06-13
type: concept
tags: [security, breach, apt, data-exfiltration, real-world]
sources: [FBI/CISA 경보, Mandiant/FireEye 보고서, Kaspersky/ESET/CrowdStrike 분석]
confidence: high
---

# 실제 침해 사례 — APT / 데이터 유출 (Part 1)

> [[breach-cases-apt]]의 분할 페이지입니다.

### 7. SolarWinds SUNBURST (2020) ⭐⭐
| 항목 | 내용 |
|------|------|
| **공격 기법** | 공급망 — Orion DLL에 백도어 삽입 (CVE-2020-10148) |
| **실습 도구** | Invoke-AtomicRedTeam T1195 (Supply Chain), Orion 유사 CI/CD 시뮬레이션 |
| **실습 내용** | 업데이트 바이너리 변조 탐지, DNS 이상 징후 분석, 포렌식 타임라인 재구성 |
| **교육 포인트** | 공급망 공격 탐지의 어려움, SBOM(소프트웨어 자재 명세서) 필요성 |
| **비고** | 전체 재현은 어렵지만 탐지/포렌식 실습은 가능 |

#### 사고 상세
| 세부 항목 | 내용 |
|----------|------|
| **발생일** | 2020-03 (최초 감염) |
| **발견일** | 2020-12-08 (FireEye) |
| **공격 타임라인** | 2019년 말: SolarWinds Orion 빌드 환경 침투 → 2020-03: 악성 업데이트(SUNBURST 백도어) 포함 정식 빌드 출시 → 수천 고객 배포 (FireEye, 美 정부기관 다수 포함) → 2020-12-08: FireEye가 보안 도구 도난 사실 공개 → SUNBURST 백도어 확인 → 역사상 최대 공급망 공격으로 기록 |
| **피해 규모** | 18,000개 조직이 악성 업데이트 다운로드. FireEye(레드팀 도구 도난), US 재무부/상무부/국토안보부/에너지부, 유럽 기관. 정확한 유출 데이터 규모 미공개 |
| **발견 경로** | FireEye Mandiant 포렌식: SolarWinds 업데이트 디지털 서명이 정상임에도 비정상 행위 발견 → SUNBURST 악성코드 역공학 |
| **배후** | APT29 (Cozy Bear, Nobelium) — 러시아 SVR. 2021-04 미국 정부 공식 귀속 |

### 8. Log4j / Log4Shell (2021) ⭐⭐⭐ (최우수)
| 항목 | 내용 |
|------|------|
| **공격 기법** | CVE-2021-44228 — Log4j JNDI 인젝션 → 원격 코드 실행 |
| **실습 도구** | **Vulhub 공식 지원** (`vulhub/log4j/CVE-2021-44228`), LDAP 서버, JNDIExploit |
| **실습 내용** | 취약점 스캔 → LDAP 서버 구축 → RCE → WAF 우회 탐지 |
| **교육 포인트** | 오픈소스 라이브러리 의존성 위험, JNDI 인젝션 원리, 인터넷 전체 영향 |
| **난이도** | 초급~중급 |

#### 사고 상세
| 세부 항목 | 내용 |
|----------|------|
| **발생일** | 2021-12-09 (공개) |
| **발견일** | 2021-11-24 (Alibaba 연구원) |
| **공격 타임라인** | 2021-11-24: Alibaba Cloud Chen Zhaojun이 Log4j JNDI 인젝션 취약점 발견 → Apache에 비공개 보고 → 2021-12-09: Apache 패치 발표와 동시에 PoC 인터넷 공개 → 전 세계적 스캔·익스플로잇 폭발 (웜, 랜섬웨어, 채굴기) → 2021-12-14: CISA 긴급 지시문 발령 → 수개월간 지속적 패치 |
| **피해 규모** | 수백만 시스템 취약 (대부분의 Java 기업 앱). Microsoft, AWS, Cloudflare, Minecraft Java Edition 직격. 대응 비용 약 100억 달러 추정 |
| **발견 경로** | Alibaba Cloud 보안 연구원 Chen Zhaojun이 Log4j 코드 감사 중 취약점 발견 → Apache 보안팀에 보고 |
| **배후** | 무기화한 해커 그룹 다수 (Conti, Khonsari 랜섬웨어 등). 최초 발견은 중국 연구원, 익스플로잇은 전 세계 해커 |

### 9. MOVEit Transfer (2023) ⭐⭐⭐
| 항목 | 내용 |
|------|------|
| **공격 기법** | CVE-2023-34362 — SQL 인젝션 → Clop 랜섬웨어 배포 |
| **실습 도구** | 커뮤니티 MOVEit 취약 컨테이너, SQLi 실습 가능 |
| **실습 내용** | 웹 익스플로잇 → 데이터 탈취 → DFIR 로그 분석 |
| **교육 포인트** | 관리형 파일 전송 시스템의 위험, SQLi의 현대적 영향 |

#### 사고 상세
| 세부 항목 | 내용 |
|----------|------|
| **발생일** | 2023-05-27 |
| **발견일** | 2023-05-28 (보안 연구원) |
| **공격 타임라인** | 2023-05-27: Clop 조직이 MOVEit SQL 인젝션(CVE-2023-34362) 익스플로잇 시작 → 2023-06-05: Clop 협박 웹사이트에 피해자 목록 공개 → 2023-06-15: FBI/CISA 경보 발령 |
| **피해 규모** | 2,500+ 조직. PwC(이메일·파일), Shell, BBC, Aer Lingus, 미국 에너지부, 루이지애나 주정부. **8,000만+ 개인 기록 유출 추정** |
| **발견 경로** | ZDI 등 보안 연구원이 MOVEit 웹로그에서 비정상 SQL 쿼리 패턴 발견 → Mandiant 포렌식으로 Clop 활동 확인 |
| **배후** | Clop (러시아어권, 2020년부터 활동). FBI/CISA 공식 귀속 |

### 10. Heartbleed (2014) ⭐⭐⭐
| 항목 | 내용 |
|------|------|
| **공격 기법** | CVE-2014-0160 — OpenSSL TLS Heartbeat read over-run |
| **실습 도구** | **Vulhub 공식 지원** (`openssl/heartbleed`), `heartbleed.py` PoC |
| **실습 내용** | 메모리 덤프 추출 (키/쿠키/비밀번호), Snort/Suricata 탐지 룰 작성 |
| **교육 포인트** | 메모리 안전, 오픈소스 감사 중요성, TLS 구현 취약점 |
| **난이도** | 초급 |

#### 사고 상세
| 세부 항목 | 내용 |
|----------|------|
| **발생일** | 2014-04-07 (공개) |
| **발견일** | 2014-04-01 (Google Security + Codenomicon) |
| **공격 타임라인** | 2011-12~2012-03: OpenSSL 1.0.1 릴리스 과정에서 기여자가 실수로 버그 유입 → 2014-04-01: Google Neel Mehta가 SSL Heartbeat 구현에서 메모리 오버리드 발견 → Codenomicon도 독립 발견 → 2014-04-07: 패치 및 전 세계 공개 |
| **피해 규모** | 최대 50만+ 웹 서버 (HTTPS, VPN, SSH). Yahoo, Stack Exchange, OKCupid 등. 인증서 폐기·재발급 비용 수억 달러 |
| **발견 경로** | Google Security (Neel Mehta)가 fuzzing 중 메모리 충돌 발견 + Codenomicon 동시 발견 |
| **배후** | 실수로 도입된 코딩 오류. NSA 등이 사전 악용했을 가능성 제기 (Edward Snowden 문서) |

### 11. EternalBlue (2017) ⭐⭐⭐
| 항목 | 내용 |
|------|------|
| **공격 기법** | MS17-010 — SMBv1 RCE |
| **실습 도구** | Vulhub `smb/ms17-010`, Metasploit, AutoBlue.py |
| **실습 내용** | SMB 취약점 탐지 → RCE → 시스템 장악 |
| **교육 포인트** | 레거시 프로토콜 위험, SMBv1 비활성화 필요성 |
| **난이도** | 초급 |

#### 사고 상세
| 세부 항목 | 내용 |
|----------|------|
| **발생일** | 2017-04-14 (유출) |
| **발견일** | 2017-04-14 (Shadow Brokers) |
| **공격 타임라인** | 2000년대 후반: NSA Equation Group이 SMBv1 취약점 익스플로잇 EternalBlue 개발 → 2016년: Shadow Brokers가 NSA 내부 도구 도난 → 2017-04-14: EternalBlue 포함 NSA 도구 인터넷 전면 공개 (MS는 3월 패치 배포) → 이후 WannaCry/NotPetya/Adylkuzz 등에 활용 |
| **피해 규모** | WannaCry(20만 시스템), NotPetya(100억 달러+). 수많은 랜섬웨어가 EternalBlue를 전파 경로로 사용 |
| **발견 경로** | Shadow Brokers가 GitHub 및 WikiLeaks 통해 공개. Kaspersky 등 분석 |
| **배후** | NSA Equation Group (미국) — 취약점 개발. Shadow Brokers (러시아 지원 추정) — 유출 |



## 관련 위키 링크
- [[breach-cases-apt]] — APT / 데이터 유출 메인 페이지
- [[exploitation]] — 실제 침해 시 사용된 익스플로잇 기술
- [[rce]] — RCE가 관여한 사례들
