---
title: 실제 침해 사례 기반 실습 교육 — 종합 가이드
created: 2026-06-10
updated: 2026-06-13
type: concept
tags: [security, training, lab, real-world, breach, ransomware, apt, supply-chain, cloud, zero-day]
sources: [FBI/CISA 경보, Mandiant/FireEye 보고서, Kaspersky/ESET/CrowdStrike 분석, 법정 문서, 회사 공개 자료]
confidence: high
---

# 실제 침해 사례 기반 실습 교육 — 종합 인덱스

> [현재 페이지는 인덱스입니다] 44건의 실제 침해 사례가 5개 하위 페이지로 분할되어 있습니다.
> 각 사례는 Docker/VM 기반 실습 가능 여부, 도구 가용성, 교육적 가치로 평가되어 있습니다.

---

## 사례 분류 및 링크

| 분류 | 건수 | 페이지 | 주요 사례 |
|------|:---:|--------|-----------|
| 🟠 **랜섬웨어** | 6건 | [[breach-cases-ransomware]] | WannaCry, NotPetya, Ryuk, REvil, Conti, LockBit |
| 🟣 **APT / 데이터 유출** | 9건 | [[breach-cases-apt]] | SolarWinds, Colonial Pipeline, Equifax, Capital One, OPM, Target, Home Depot, Anthem, eBay |
| 🔗 **공급망 공격** | 4건 | [[breach-cases-supply-chain]] | SolarWinds, Kaseya, Codecov, 3CX |
| ☁️ **클라우드 보안** | 3건 | [[breach-cases-cloud]] | Capital One, Uber, Twilio |
| 💥 **제로데이 / 최신** | 22건 | [[breach-cases-zeroday-latest]] | Stuxnet, EternalBlue, Log4j, ProxyShell, Spring4Shell 등 |

---

## 평가 기준

| 등급 | 의미 | 예시 |
|:----:|------|------|
| ⭐⭐⭐ | Docker Compose + PoC 즉시 사용 가능, Vulhub 공식 지원 | Log4j, EternalBlue, Heartbleed |
| ⭐⭐ | 일부 구성 필요, 도구/스크립트는 공개됨 | SolarWinds 시뮬레이션, Capital One SSRF |
| ⭐ | 개념 증명 수준, 직접 Lab 구축 필요 | Stuxnet, Pegasus |

---

## 📊 실습 우선순위 추천 (Top 10)

| 순위 | 사례 | 등급 | Docker | 교육 가치 |
|:----:|------|:----:|:------:|:---------:|
| 1 | Log4Shell | ⭐⭐⭐ | ✅ | 10/10 |
| 2 | EternalBlue | ⭐⭐⭐ | ✅ | 10/10 |
| 3 | Heartbleed | ⭐⭐⭐ | ✅ | 9/10 |
| 4 | ProxyShell | ⭐⭐⭐ | ✅ | 9/10 |
| 5 | Spring4Shell | ⭐⭐⭐ | ✅ | 8/10 |
| 6 | WannaCry | ⭐⭐⭐ | ✅ | 8/10 |
| 7 | Shellshock | ⭐⭐⭐ | ✅ | 8/10 |
| 8 | Dirty COW | ⭐⭐ | - | 7/10 |
| 9 | Struts2 | ⭐⭐⭐ | ✅ | 7/10 |
| 10 | Sudo Baron Samedit | ⭐⭐ | - | 7/10 |

## 🔧 실습 도구 통합 환경

| 도구 | 용도 | 설치 |
|------|------|------|
| Vulhub | Docker Compose 기반 취약 환경 | `~/vulhub/` |
| Metasploitable2 | 종합 취약 VM | `~/VMs/Metasploitable2/` |
| DVWA | 웹 취약점 연습 | `~/labs/dvwa/` |

## 📋 참고 저장소

- Vulhub: https://github.com/vulhub/vulhub (150+ Docker 취약 환경)
- Metasploit: `msfconsole` 경로 내장
- CISA Known Exploited Vulnerabilities: https://www.cisa.gov/known-exploited-vulnerabilities-catalog

## 사고 정보 출처

- FBI/CISA 공식 경보 (CISA ICS-CERT, FBI FLASH)
- Mandiant/FireEye/FortiGuard/Kaspersky/ESET/CrowdStrike 분석 보고서
- DOJ 기소장, 의회 청문회 증언, 회사 공식 공개 자료

---

## 관련 위키 링크
- [[breach-cases-ransomware]] — 랜섬웨어 사례 (6건)
- [[breach-cases-apt]] — APT / 데이터 유출 사례 (9건)
- [[breach-cases-supply-chain]] — 공급망 공격 사례 (4건)
- [[breach-cases-cloud]] — 클라우드 보안 사례 (3건)
- [[breach-cases-zeroday-latest]] — 제로데이 및 2023-2025 최신 사례 (22건)
- [[exploitation]] — Exploitation (익스플로잇) — 사례별 사용된 공격 기술
- [[rce]] — RCE (Remote Code Execution) — 다수 사례의 핵심 취약점 유형