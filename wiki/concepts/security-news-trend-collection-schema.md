---
title: Security News Trend Collection Schema
created: 2026-06-20
updated: 2026-06-21
type: concept
tags: [workflow, wiki, research, report, trend]
sources: [raw/articles/20260620_security_news_rss.md, concepts/security-news-rss-catalog.md, concepts/security-news-rss-hub.md]
confidence: high
---

# Security News Trend Collection Schema

보안 뉴스 수집의 목적이 **주간/월간 보안 동향 보고서 작성**이라면, 흐름은 **1) 최대한 많이 수집 → 2) 사건군으로 정리 → 3) 주간/월간 보고서로 묶기** 입니다.

즉, 수집 단계에서는 넓게 모으고, 정리 단계에서는 아래 3가지를 사건군 단위로 남깁니다.

- **무슨 사건인가**: CVE, 침해사고, 벤더 공지, 정책/권고, 위협 캠페인
- **얼마나 중요한가**: 영향도, 공개성, 야생 공격 여부, 확산 범위
- **어떤 추세에 속하는가**: 주간/월간 보고서에서 묶어 설명할 수 있는 분류

## 참고 URL
- [Reference](raw/articles/20260620_security_news_rss.md)
- [Reference](concepts/security-news-rss-catalog.md)
- [Reference](concepts/security-news-rss-hub.md)

## 1. 수집 기본 원칙

1. **기사 1개 = 보고서 항목 1개가 아닙니다.**
   - 같은 이슈가 여러 매체에 반복되면 하나의 사건군으로 묶습니다.
   - 보고서에는 대표 출처 1~3개만 남기고 나머지는 보조 출처로 둡니다.

2. **피드 1개 = 보고서 축 1개가 아닙니다.**
   - RSS는 수집 경로일 뿐, 보고서 구조는 사건 기준으로 다시 편집합니다.

3. **허브 페이지는 수집 대상이 아니라 메타데이터용입니다.**
   - 피드 목록/안내 페이지는 참고용이며, 보고서 항목에는 직접 들어가지 않습니다.

4. **주간과 월간은 같은 원자료를 다르게 집계합니다.**
   - 주간: 새로 뜬 이슈, 야생 공격, 패치 긴급도 중심
   - 월간: 반복 패턴, 벤더별 빈도, 업종 영향, 누적 추세 중심

## 2. 저장 단위

### 2.1 Incident Unit
가장 작은 저장 단위는 **사건군(incident unit)** 입니다.

| 필드 | 설명 | 예시 |
|---|---|---|
| `incident_id` | 내부 식별자 | `2026-06-20-cisa-cve-xxxx` |
| `headline` | 대표 제목 | `CVE-2026-XXXX exploited in the wild` |
| `event_type` | 사건 유형 | `cve`, `rce`, `lpe`, `advisory`, `breach`, `campaign` |
| `region` | 지역 분류 | `kr`, `global` |
| `source_tier` | 출처 등급 | `official`, `vendor`, `media`, `analysis` |
| `source_primary` | 대표 출처 | `CISA`, `KISA/KrCERT`, `BleepingComputer` |
| `source_secondary` | 보조 출처 목록 | `[...]` |
| `published_at` | 최초 공개일 | `2026-06-20` |
| `detected_at` | 수집일 | `2026-06-20` |
| `status` | 현재 상태 | `new`, `exploit_in_the_wild`, `patched`, `mitigated`, `monitoring` |
| `impact` | 영향 요약 | `RCE`, `LPE`, `data leak`, `service disruption` |
| `severity` | 심각도 | `critical`, `high`, `medium`, `low` |
| `affected_assets` | 영향 대상 | 제품명/서비스명 |
| `exploitation` | 악용 상태 | `none`, `proof_of_concept`, `active`, `known_exploited` |
| `mitigation` | 대응 요약 | 패치/차단/권고/설정 변경 |
| `one_line_summary` | 1문장 요약 | 보고서 본문용 |
| `trend_tags` | 추세 태그 | `cve`, `patch`, `kev`, `ransomware` |
| `report_buckets` | 주간/월간 분류 | `weekly:urgent`, `monthly:vendor_patch` |
| `confidence` | 신뢰도 | `high`, `medium`, `low` |

### 2.2 Trend Cluster
동일 계열 사건을 묶는 **추세 클러스터**를 별도로 둡니다.

| 필드 | 설명 |
|---|---|
| `cluster_id` | 같은 흐름을 묶는 그룹 ID |
| `theme` | 예: `browser zero-day`, `edge device RCE`, `ransomware`, `cloud misconfig` |
| `included_incidents` | 포함된 사건군 목록 |
| `weekly_note` | 이번 주 한 줄 해석 |
| `monthly_note` | 이번 달 누적 해석 |

## 3. 권장 태그 체계

보고서용 태그는 기존 taxonomy를 활용하되, 아래처럼 **집계 목적 태그**를 추가로 붙입니다.

- **공격/영향 태그**: `cve`, `rce`, `lpe`, `dos`, `ransomware`, `data-loss`, `breach`
- **운영 태그**: `patch`, `advisory`, `kev`, `mitigation`, `monitoring`
- **추세 태그**: `zero-day`, `exploit-in-the-wild`, `vendor-bulk-patch`, `supply-chain`, `cloud`, `identity`, `browser`, `endpoint`
- **지역 태그**: `kr`, `global`
- **출처 태그**: `official`, `vendor`, `media`, `analysis`

## 4. 주간 보고서용 집계 규칙

주간 보고서는 “지금 당장 알아야 하는 것”에 집중합니다.

1. **최상위 항목**
   - 야생 공격 중
   - KEV 등록
   - 대규모 패치
   - 광범위한 서비스 영향
   - 국내 공공기관 권고

2. **보조 항목**
   - 기술 분석이 길지만 영향이 아직 제한적
   - 벤더 블로그에서 나온 초기 분석
   - 반복 기사들

3. **주간 한 줄 결론 예시**
   - “이번 주는 브라우저/엣지 장비 패치와 KEV 등록 이슈가 중심입니다.”

## 5. 월간 보고서용 집계 규칙

월간 보고서는 “패턴과 반복”에 집중합니다.

1. **반복되는 테마를 묶습니다.**
   - 특정 벤더의 연속 패치
   - 같은 공격면의 반복 출현
   - 특정 지역/업종에서 집중된 이슈

2. **빈도와 변화량을 기록합니다.**
   - 전월 대비 증가/감소
   - 야생 공격 전환 비율
   - 패치 공지 대비 실제 악용 비율

3. **월간 한 줄 결론 예시**
   - “이번 달은 인증 우회와 edge device RCE가 반복되었고, 공공기관 권고 비중이 높았습니다.”

## 6. 수집 흐름

1. RSS에서 원문을 확인합니다.
2. 같은 사건을 여러 출처에서 묶습니다.
3. 사건군 단위로 필드를 채웁니다.
4. 주간/월간 보고서에 들어갈 클러스터를 만듭니다.
5. 쇼츠가 필요하면 `[[security-news-shorts-priority-summary]]` 와 `[[security-news-shorts-script-template]]` 를 보조로 사용합니다.
6. 뉴스레터가 필요하면 `[[security-news-newsletter-format]]` 에 따라 분류별 기사와 2~3줄 한글 요약으로 편집합니다.

## 7. 제외 기준

- 피드 목록만 있는 허브 페이지
- 제목은 자극적이지만 영향이 불명확한 글
- 중복 기사만 많은 항목
- 보고서 축으로 묶을 수 없는 단일 링크

## 8. 관련 문서

- `[[security-news-rss-catalog]]`
- `[[security-news-rss-hub]]`
- `[[security-news-rss-operations-checklist]]`
- `[[security-news-rss-region-split]]`
- `[[security-news-shorts-priority-summary]]`
- `[[security-news-shorts-script-template]]`
