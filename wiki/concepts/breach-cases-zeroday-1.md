---
title: 실제 침해 사례 — 제로데이 및 최신 사례 (Part 1)
created: 2026-06-13
updated: 2026-06-21
type: concept
tags: [security, zero-day, breach, real-world]
sources: [CISA KEV, vendor advisories, public incident reports]
confidence: high
---

# 실제 침해 사례 — 제로데이 및 최신 사례 (Part 1)

> [[breach-cases-zeroday-latest]]의 분할 페이지입니다.

### 23. Stuxnet (2010) ⭐ (시뮬레이션 한정 ⭐⭐)
| 항목 | 내용 |
|------|------|
| **공격 기법** | 4개 제로데이 + PLC 코드 변조 → 원심분리기 물리적 파괴 |
| **실습 도구** | Minimega ICS 시뮬레이터, 가상 PLC (OpenPLC) |
| **실습 내용** | ICS 공격 시뮬레이션, 방어 심층 설계 |
| **교육 포인트** | 물리적 사이버 공격, 국가 주도 APT, OT 보안 |
| **비고** | 전체 재현은 OT 하드웨어 필요, 개념 시뮬레이션만 가능 |

#### 사고 상세
| 세부 항목 | 내용 |
|----------|------|
| **발생일** | 2005년경 ~ 2010-06 |
| **발견일** | 2010-06-17 (VirusBlokAda 연구원) |
| **공격 타임라인** | 2005~2007: 초기 버전으로 이란 나탄즈 원심분리기 공격 시작 → 2010-06: 웜 변종이 USB 통해 실수로 외부 유출 → 2010-09: NYT 보도로 미국/이스라엘 공동 개발 확인 → 2010-11: 이란 원심분리기 1,000개 파손 확인 |
| **피해 규모** | 이란 나탄즈 농축 시설. IR-1 원심분리기 1,000~2,000개 물리적 파괴. 이란 핵 프로그램 수년 지연. 피해 수십억 달러 |
| **발견 경로** | VirusBlokAda(벨라루스) 연구원 Sergei Ulasen이 이란 고객 PC에서 이상 웜 발견 → Kaspersky 분석 → 역사상 가장 정교한 악성코드로 기록 |
| **배후** | 미국(NSA/CIA) & 이스라엘(Unit 8200). \"Olympic Games\" 작전. 공식 확인되지 않았으나 널리 인정됨 |

### 24. Operation Aurora (2009) ⭐⭐
| 항목 | 내용 |
|------|------|
| **공격 기법** | IE 제로데이 (CVE-2010-0249) + 표적 피싱 → 구글 등 침투 |
| **실습 도구** | 피싱 시뮬레이션 + 레거시 브라우저 VM |
| **실습 내용** | 표적 피싱 인식, 브라우저 보안 강화, APT 탐지 |
| **교육 포인트** | 국가 배후 APT의 초기 사례, 구글 중국 철수 계기 |

#### 사고 상세
| 세부 항목 | 내용 |
|----------|------|
| **발생일** | 2009-12 ~ 2010-01 |
| **발견일** | 2010-01-12 (Google) |
| **공격 타임라인** | 2009-12: 중국 해커가 Google 직원에 맞춤형 피싱 이메일 (가짜 Adobe Reader 업데이트) 발송 → IE 0-day 악용 → Google 기업 네트워크 침투 → Git 저장소·소스코드·인권 활동가 계정 접근 → Adobe, Juniper, Yahoo! 동시 공격 → 2010-01-12: Google 역사적 발표 (\"중국에서 정교한 사이버 공격\") → 중국 철수 협상 |
| **피해 규모** | Google: 34개 기업 계정 침해 (인권 활동가 등). 소스코드 탈취. 다수 기업 동시 피해 |
| **발견 경로** | Google 보안팀이 Git 소스 저장소 접근 로그에서 비정상 활동 발견 → 포렌식 |
| **배후** | 중국 BERSERK BEAR (APT3, Comment Crew). 2010년 이후 미국 정부 공식 귀속 |

---

## 참고 URL
- [Reference](CISA KEV)
- [Reference](vendor advisories)
- [Reference](public incident reports)

## 🆕 2023-2025 최신 사례 (10건)

### 25. React2Shell / Vite Dev Server (2025) ⭐⭐⭐
| 항목 | 내용 |
|------|------|
| **공격 기법** | CVE-2025-30203 — Vite dev server `__launch-editor` path traversal → RCE |
| **CVE** | CVE-2025-30203, CVE-2025-30204 |
| **실습 도구** | Vite Docker 이미지 (공식), 취약 버전 dev server 구성 |
| **실습 내용** | dev 서버 path traversal → 소스코드 탈취 → RCE 체인 |
| **교육 포인트** | 개발 서버 노출 위험, path traversal, dev 의존성 보안 |
| **Docker** | Vite 공식 Docker 이미지로 즉시 구성 가능 |
| **난이도** | 초급 |

#### 사고 상세
| 세부 항목 | 내용 |
|----------|------|
| **발생일** | 2025-04 (공개) |
| **발견일** | 2025-03 (Vite 보안팀, 외부 연구자) |
| **공격 타임라인** | Vite dev server의 `__launch-editor` 엔드포인트를 통한 path traversal 발견 → `server.fs.deny` 우회로 임의 파일 접근 → RCE까지 체인 가능 → CVE-2025-30203/30204 발급 → 2025-04 패치 |
| **피해 규모** | Vite 사용하는 수많은 오픈소스 프로젝트 dev 서버 노출 시 RCE 위험 |
| **발견 경로** | 보안 연구자가 Vite 코드 감사 중 발견 |
| **배후** | 취약점 자체. PoC 공개 후 다수의 공격자 활용 |

| **PoC** | [GitHub CVE-2025-30203 PoC](https://github.com/ally-petitt/CVE-2025-30203-PoC) |

### 26. BPFDoor (Linux BPF 백도어) (2022) ⭐⭐
| 항목 | 내용 |
|------|------|
| **공격 기법** | CVE-2022-36120, CVE-2022-39193 — BPF 바이트코드 검증 우회 → 커널 레벨 백도어 |
| **CVE** | CVE-2022-36120, CVE-2022-39193 |
| **실습 도구** | VM 기반 (Linux + BPF 샘플), bpftrace 탐지, 메모리 포렌식 |
| **실습 내용** | BPF 백도어 탐지 (SELinux/bpftrace), 메모리 포렌식, 네트워크 트래픽 분석 |
| **교육 포인트** | eBPF의 이중성 (강력한 도구 vs 백도어), APT41 TTPs, 커널 레벨 위협 탐지 |
| **Docker** | VM 필요 (커널 모듈 조작), Docker만으로는 부족 |
| **난이도** | 고급 |

#### 사고 상세
| 세부 항목 | 내용 |
|----------|------|
| **발생일** | 2019년경 (최초 활동) |
| **발견일** | 2022-05 (Mandiant 공개) |
| **공격 타임라인** | APT41이 Linux BPF 시스템 콜을 활용한 정교한 백도어 개발 → 유저랜드-커널 통신 채널 은닉 → 원격 명령 실행 및 지속성 유지 → 2022-05 Mandiant 분석 공개 |
| **피해 규모** | 주로 데스크톱/서버 Linux 시스템. 특정 기업 표적 공격 (정확한 규모 미공개) |
| **발견 경로** | Mandiant 사고 대응 중 Linux 시스템에서 비정상 BPF 바이트코드 발견 |
| **배후** | APT41 (중국, WINNTI / BARIUM) |

| **참고** | [Mandiant BPFDoor 분석](https://www.mandiant.com/resources/blog/bpfdoor-linux-backdoor), [Unit42 분석](https://unit42.paloaltonetworks.com/bpfdoor/) |

### 27. Ivanti Connect Secure (2024) ⭐⭐⭐
| 항목 | 내용 |
|------|------|
| **공격 기법** | CVE-2023-46805 (인증 우회) + CVE-2024-21887 (명령 주입) → RCE 체인 |
| **CVE** | CVE-2023-46805, CVE-2024-21887, CVE-2024-22024 |
| **실습 도구** | Ivanti ICS 시뮬레이션 Docker, nuclei 템플릿 |
| **실습 내용** | 인증 우회 → 명령 주입 체인 실습, 웹셸 배포, C2 탐지 |
| **교육 포인트** | VPN 게이트웨이가 새로운 공격 표면, 인증 우회 + RCE 다단계 체인, 중국 APT(UNC5221) TTPs |
| **Docker** | 비공식 Ivanti ICS 모의 컨테이너 사용 가능 |
| **난이도** | 중급 |

#### 사고 상세
| 세부 항목 | 내용 |
|----------|------|
| **발생일** | 2024-01 (공개) |
| **발견일** | 2023-12 (Volexity, Google TAG) |
| **공격 타임라인** | 2023-12: Volexity/Google TAG가 Ivanti ICS 0-day 체인 제보 → CVE-2023-46805 + CVE-2024-21887 → 인증 우회 후 RCE → 중국 APT(UNC5221)가 전 세계 Ivanti 기기 공격 → 2024-01: 공개 및 패치 → 수만 대 Ivanti 기기 감염 확인 |
| **피해 규모** | 전 세계 수만 개 Ivanti Connect Secure 기기 감염. 미국 CISA 긴급 지시문 발령 |
| **발견 경로** | Volexity + Google Threat Analysis Group (TAG)이 고객 환경에서 0-day 공격 탐지 |
| **배후** | UNC5221 (중국 위협 그룹) |

| **PoC** | [CVE-2024-21887 PoC (horizon3ai)](https://github.com/horizon3ai/CVE-2024-21887), [CVE-2023-46805 체인 PoC](https://github.com/Chocapikk/CVE-2023-46805) |

### 28. Atlassian Confluence (CVE-2023-22527) (2023) ⭐⭐⭐
| 항목 | 내용 |
|------|------|
| **공격 기법** | CVE-2023-22527 — Velocity 템플릿 인젝션 → RCE (CVSS 10) |
| **CVE** | CVE-2023-22527 (CVSS 10), CVE-2023-22515, CVE-2024-21677 |
| **실습 도구** | Atlassian Confluence Docker (공식 이미지 취약 버전) |
| **실습 내용** | 템플릿 인젝션 실습, OGNL 표현식 평가, RCE 체인 |
| **교육 포인트** | 템플릿 엔진의 양날의 검, CVSS 10 취약점, 협업 툴이 공격 표면으로 |
| **Docker** | Atlassian 공식 Docker 이미지 사용 가능 |
| **난이도** | 초~중급 |

#### 사고 상세
| 세부 항목 | 내용 |
|----------|------|
| **발생일** | 2023-11 (공개) |
| **발견일** | 2023-10 (Atlassian 보안팀) |
| **공격 타임라인** | Confluence Server/Data Center의 Velocity 템플릿 엔진에서 표현식 인젝션 발견 → `pages/exportpdf.action` 엔드포인트를 통한 명령 주입 가능 → CVSS 10.0 → 전체 인터넷 스캔 시작 → 랜섬웨어 그룹이 Confluence 서버 통해 침투 |
| **피해 규모** | 수만 개 Confluence 서버. 랜섬웨어 그룹의 초기 침투 경로로 활발히 악용 |
| **발견 경로** | Atlassian 내부 보안 감사 + 외부 연구자 제보 |
| **배후** | 다수의 랜섬웨어 그룹 (LockBit 등) |

| **PoC** | [Exploit-DB 51711](https://www.exploit-db.com/exploits/51711), [CVE-2023-22515 PoC](https://github.com/assetnote/CVE-2023-22515) |



## 관련 위키 링크
- [[breach-cases-zeroday-latest]] — 제로데이 및 최신 사례 메인 페이지
- [[rce]] — 다수 최신 사례의 공통 결과
- [[exploitation]] — 공격 체인에서 사용된 기술
