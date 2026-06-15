---
title: 실제 침해 사례 — APT / 데이터 유출
created: 2026-06-13
updated: 2026-06-13
type: concept
tags: [security, breach, apt, data-exfiltration, real-world]
sources: [FBI/CISA 경보, Mandiant/FireEye 보고서, Kaspersky/ESET/CrowdStrike 분석]
confidence: high
---

# 실제 침해 사례 — APT / 데이터 유출

> 이 페이지는 9건의 사례를 2개 하위 페이지로 나눈 **인덱스**입니다.
> 자세한 기술 분석은 하위 페이지를 참고합니다.

## 하위 페이지

| 하위 페이지 | 범위 | 주요 사례 |
|------------|------|-----------|
| [[breach-cases-apt-1]] | 7~11 | SolarWinds, Log4j, MOVEit, Heartbleed, EternalBlue |
| [[breach-cases-apt-2]] | 12~16 | Equifax, Capital One, Marriott, Uber, GitLab |

## 개요

APT와 대규모 데이터 유출은 공격자가 **장기간 잠복**하면서 권한을 확대하고, 민감정보를 외부로 유출하는 전형적 시나리오입니다. 실제 사례에서는 **RCE**, **SSRF**, 공급망 침해, 클라우드 오남용이 자주 결합됩니다.

## 빠른 선택 가이드

- 초기 침투와 공급망 분석이 필요하면 → [[breach-cases-apt-1]]
- 클라우드 및 데이터 유출 관점이 중요하면 → [[breach-cases-apt-2]]
- 재현 가능한 실습 환경은 → [[real-world-breach-cases]]

## 관련 위키 링크
- [[real-world-breach-cases]] — 종합 인덱스
- [[breach-cases-apt-1]] — APT / 데이터 유출 Part 1
- [[breach-cases-apt-2]] — APT / 데이터 유출 Part 2
- [[exploitation]] — 공격 체인에서 사용되는 익스플로잇
- [[rce]] — 원격 코드 실행
