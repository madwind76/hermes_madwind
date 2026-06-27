---
title: 실제 침해 사례 — 제로데이 및 최신 사례 (Part 2)
created: 2026-06-13
updated: 2026-06-21
type: concept
tags: [security, zero-day, breach, real-world]
sources: [CISA KEV, vendor advisories, public incident reports]
confidence: high
---

# 실제 침해 사례 — 제로데이 및 최신 사례 (Part 2)

> [[breach-cases-zeroday-latest]]의 분할 페이지입니다.

### 29. Palo Alto PAN-OS (CVE-2024-3400) (2024) ⭐⭐⭐
| 항목 | 내용 |
|------|------|
| **공격 기법** | CVE-2024-3400 — GlobalProtect 게이트웨이 명령 주입 → 루트 셸 (CVSS 10) |
| **CVE** | CVE-2024-3400 (CVSS 10), CVE-2025-0108, CVE-2024-0012 |
| **실습 도구** | PAN-OS 시뮬레이터 Docker, GNS3 VM |
| **실습 내용** | GlobalProtect SAML/Cookie 처리 취약점 익스플로잇, 방화벽 명령 주입 |
| **교육 포인트** | 네트워크 장비 보안, 방화벽 자체가 공격 대상, CVSS 10 취약점 |
| **Docker** | PAN-OS 시뮬레이터 이미지 존재 (비공식), GNS3 VM 권장 |
| **난이도** | 중급 |

#### 사고 상세
| 세부 항목 | 내용 |
|----------|------|
| **발생일** | 2024-04 (공개) |
| **발견일** | 2024-03 (Volexity) |
| **공격 타임라인** | GlobalProtect 게이트웨이의 SAML/Cookie 처리에서 명령 주입 발견 → CVSS 10.0 → 중국 APT가 전 세계 PAN-OS 방화벽 공격 → CISA 긴급 지시문 발령 → 2024-04-16: 긴급 패치 |
| **피해 규모** | 전 세계 수천 대 Palo Alto 방화벽 침해. 주정부/대학/통신사 포함 |
| **발견 경로** | Volexity가 고객 환경에서 비정상 방화벽 행위 탐지 |
| **배후** | 중국 APT (UNC? ) |

| **PoC** | [CVE-2024-3400 PoC (horizon3ai)](https://github.com/horizon3ai/CVE-2024-3400), [CVE-2025-0108 PoC](https://github.com/therealcoiff/CVE-2025-0108) |

### 30. VMware vCenter (2023-2024) ⭐⭐
| 항목 | 내용 |
|------|------|
| **공격 기법** | CVE-2023-20887 — vRealize Log Insight 명령 인젝션 RCE |
| **CVE** | CVE-2023-20887, CVE-2024-22252, CVE-2024-22253 |
| **실습 도구** | VMware vRealize Log Insight 취약 컨테이너 |
| **실습 내용** | Log Insight licensing API 명령 인젝션, vCenter DCERPC 프로토콜 결함 실습 |
| **교육 포인트** | 가상화 인프라 보안, SIEM 도구가 공격 경로로 |
| **Docker** | vRealize Log Insight는 컨테이너화 가능, vCenter는 VM 필요 |
| **난이도** | 중급 |

#### 사고 상세
| 세부 항목 | 내용 |
|----------|------|
| **발생일** | 2023-06 (CVE-2023-20887) / 2024-03 (CVE-2024-22252) |
| **발견일** | 각각 공개일 기준 |
| **공격 타임라인** | vRealize Log Insight licensing API 통해 원격 명령 실행 가능 → 랜섬웨어 그룹(Clop, LockBit)이 VMware 인프라 공격 경로로 활용 |
| **피해 규모** | VMware vCenter 사용하는 대규모 엔터프라이즈 환경. 랜섬웨어 초기 침투 경로로 사용됨 |
| **발견 경로** | 보안 연구자 (sinsinology 등) |

| **PoC** | [CVE-2023-20887 PoC](https://github.com/sinsinology/CVE-2023-20887), [CVE-2024-22252 PoC](https://github.com/x0rb3l/CVE-2024-22252) |

### 31. Veeam Backup & Replication (2025) ⭐⭐⭐
| 항목 | 내용 |
|------|------|
| **공격 기법** | CVE-2025-23114 — 백업 에이전트 RCE (CVSS 9.9) |
| **CVE** | CVE-2025-23114 (CVSS 9.9) |
| **실습 도구** | Veeam Backup Docker (비공식 이미지) |
| **실습 내용** | 백업 서버 RCE, 백업 데이터 변조, 공급망 공격 시뮬레이션 |
| **교육 포인트** | 백업 시스템의 이중성 (복구 도구 vs 공격 경로), CVSS 9.9 |
| **Docker** | Veeam Backup Server Docker 이미지로 구성 가능 (비공식) |
| **난이도** | 중급 |

#### 사고 상세
| 세부 항목 | 내용 |
|----------|------|
| **발생일** | 2025-02 |
| **발견일** | 2025-01 (Veeam 보안팀 + 외부 연구자) |
| **공격 타임라인** | Veeam Backup & Replication 백업 에이전트에서 RCE 취약점 발견 → CVSS 9.9 → 백업 인프라 전체 장악 가능 → 공급망 공격으로 확장 위험 |
| **피해 규모** | Veeam 사용하는 전 세계 기업. 백업 데이터 접근으로 랜섬웨어 복구 무력화 가능 |
| **발견 경로** | Veeam 내부 보안 감사 + 외부 연구자 |

| **PoC** | [CVE-2025-23114 PoC](https://github.com/sinsinology/CVE-2025-23114) |

### 32. Fortinet FortiGate SSL VPN (2025) ⭐⭐⭐
| 항목 | 내용 |
|------|------|
| **공격 기법** | CVE-2025-24472 — FortiGate SSL VPN RCE |
| **CVE** | CVE-2025-24472 |
| **실습 도구** | FortiGate VM (GNS3), nuclei 템플릿 |
| **실습 내용** | SSL VPN RCE 실습, 방화벽 침투 시뮬레이션 |
| **교육 포인트** | SSL VPN 지속적 위협, Fortinet 생태계 보안 |
| **Docker** | FortiGate VM 이미지 필요 (GNS3/EVE-NG) |
| **난이도** | 중급 |

#### 사고 상세
| 세부 항목 | 내용 |
|----------|------|
| **발생일** | 2025-04 |
| **발견일** | 2025-03 |
| **공격 타임라인** | FortiGate SSL VPN에서 원격 코드 실행 취약점 발견 → 활발히 악용 |
| **피해 규모** | FortiGate 사용 기업. 랜섬웨어 초기 접근 경로로 활용 |
| **발견 경로** | 보안 연구자 |

| **PoC** | [CVE-2025-24472 PoC](https://github.com/sudo9x/CVE-2025-24472) |

### 33. Apache OFBiz (2025) ⭐⭐⭐
| 항목 | 내용 |
|------|------|
| **공격 기법** | CVE-2025-26865 — SOAP API RCE |
| **CVE** | CVE-2025-26865 |
| **실습 도구** | Apache OFBiz Docker (공식 이미지 취약 버전) |
| **실습 내용** | SOAP API 조작 → RCE 체인 실습, ERP 시스템 보안 |
| **교육 포인트** | 오픈소스 ERP의 보안 위험, SOAP API 취약점, Docker 즉시 실습 가능 |
| **Docker** | Apache OFBiz 공식 Docker 이미지로 즉시 구성 가능 |
| **난이도** | 초~중급 |

#### 사고 상세
| 세부 항목 | 내용 |
|----------|------|
| **발생일** | 2025-03 |
| **발견일** | 2025-02 |
| **공격 타임라인** | Apache OFBiz SOAP API에서 원격 코드 실행 취약점 발견 → Docker 이미지 즉시 패치 |
| **피해 규모** | OFBiz 사용 기업. ERP 시스템 장악 시 내부망 전체 위험 |
| **발견 경로** | 보안 연구자 |

| **PoC** | [CVE-2025-26865 PoC](https://github.com/0xbito/CVE-2025-26865) |

### 34. MongoDB Atlas 인증 우회 (2025) ⭐⭐
| 항목 | 내용 |
|------|------|
| **공격 기법** | CVE-2025-22936 — MongoDB Atlas 인증 우회 → 데이터 접근 |
| **CVE** | CVE-2025-22936 |
| **실습 도구** | MongoDB Docker + 인증 우회 시뮬레이션 |
| **실습 내용** | DB 인증 우회, 클라우드 DB 설정 오류 점검 |
| **교육 포인트** | 클라우드 DB 보안, Atlas 설정 오류 위험 |
| **Docker** | MongoDB 공식 Docker 이미지 사용 가능 |
| **난이도** | 초급 |

#### 사고 상세
| 세부 항목 | 내용 |
|----------|------|
| **발생일** | 2025-01 |
| **발견일** | 2024-12 |
| **공격 타임라인** | MongoDB Atlas 인증 우회 취약점 발견 → DB 데이터 접근 가능 |
| **피해 규모** | MongoDB Atlas 사용 조직. 설정 오류 시 데이터 유출 위험 |
| **발견 경로** | 보안 연구자 |

| **참고** | [NVD CVE-2025-22936](https://nvd.nist.gov/vuln/detail/CVE-2025-22936) |

---

---

## 참고 URL
- [Reference](CISA KEV)
- [Reference](vendor advisories)
- [Reference](public incident reports)

## 관련 위키 링크
- [[real-world-breach-cases]] — 전체 사례 목록 및 실습 우선순위
- [[rce]] — RCE (원격 코드 실행) — 다수 사례의 핵심 취약점 유형
- [[exploitation]] — Exploitation (익스플로잇) — 사례별 공격에 사용된 기술

## 관련 위키 링크
- [[breach-cases-zeroday-latest]] — 제로데이 및 최신 사례 메인 페이지
- [[rce]] — 다수 최신 사례의 공통 결과
- [[exploitation]] — 공격 체인에서 사용된 기술
