---
title: Security News Publishing Input Form Template
created: 2026-06-20
updated: 2026-06-21
type: concept
tags: [workflow, wiki, research, report, newsletter, template, automation]
sources: [raw/articles/20260620_security_news_rss.md, concepts/security-news-newsletter-publishing-checklist.md, concepts/security-news-newsletter-format.md, concepts/security-news-trend-collection-schema.md]
confidence: high
---

# Security News Publishing Input Form Template

이 템플릿은 보안 뉴스 **주간 보고서 / 월간 보고서 / 뉴스레터**를 자동으로 생성하기 위한 입력 폼입니다.  
목표는 수집된 사건을 사람이 손으로 다시 해석하지 않아도 되도록, **구조화된 입력값**을 먼저 채우는 것입니다.

## 참고 URL
- [Reference](raw/articles/20260620_security_news_rss.md)
- [Reference](concepts/security-news-newsletter-publishing-checklist.md)
- [Reference](concepts/security-news-newsletter-format.md)
- [Reference](concepts/security-news-trend-collection-schema.md)

## 1. 사용 목적

- 주간 보고서 자동 초안 생성
- 월간 보고서 자동 초안 생성
- 뉴스레터 자동 편집
- 기사 묶음의 중복 제거와 분류 자동화

## 2. 입력 폼 구조

### 2.1 문서 메타

| 필드 | 설명 | 예시 |
|---|---|---|
| `report_type` | 출력 문서 종류 | `weekly`, `monthly`, `newsletter` |
| `report_period` | 대상 기간 | `2026-W25`, `2026-06`, `2026-06-15~2026-06-21` |
| `language` | 출력 언어 | `ko` |
| `audience` | 대상 독자 | `general`, `security`, `ops`, `executive` |
| `owner` | 작성자/운영자 | `woojin nam` |

### 2.2 사건군 입력

| 필드 | 설명 |
|---|---|
| `incident_id` | 내부 식별자 |
| `headline` | 대표 제목 |
| `category` | `cve`, `breach`, `advisory`, `vendor_notice`, `campaign` |
| `region` | `kr`, `global` |
| `severity` | `critical`, `high`, `medium`, `low` |
| `status` | `new`, `active`, `patched`, `mitigated`, `monitoring` |
| `source_primary` | 대표 출처 |
| `source_secondary` | 보조 출처 목록 |
| `published_at` | 최초 공개일 |
| `detected_at` | 수집일 |
| `summary_1` | 1줄 요약 |
| `summary_2` | 2줄 요약 |
| `summary_3` | 3줄 요약 |
| `impact` | 영향 요약 |
| `action_required` | 필요한 조치 |
| `trend_tags` | 집계 태그 |
| `clusters` | 묶을 추세 클러스터 |
| `priority` | `p1`, `p2`, `p3` |

### 2.3 기사 카드 입력

| 필드 | 설명 |
|---|---|
| `article_title` | 기사 제목 |
| `article_url` | 원문 링크 |
| `publisher` | 매체 또는 기관 |
| `article_type` | `breaking`, `analysis`, `advisory`, `explain` |
| `short_summary` | 2~3줄 한글 요약 |
| `why_it_matters` | 왜 중요한지 |
| `what_to_do` | 무엇을 해야 하는지 |
| `related_incident_id` | 연결 사건군 |

## 3. 권장 YAML 예시

```yaml
# 보안 뉴스 발행 자동화 입력 예시
report_type: weekly
report_period: 2026-W25
language: ko
audience: security
owner: woojin nam
items:
  - incident_id: 2026-06-20-cisa-cve-xxxx
    headline: CVE-2026-XXXX exploited in the wild
    category: cve
    region: global
    severity: critical
    status: active
    source_primary: CISA
    source_secondary:
      - BleepingComputer
      - Vendor Advisory
    published_at: 2026-06-20
    detected_at: 2026-06-20
    summary_1: 취약점이 야생 공격에 악용되고 있습니다.
    summary_2: 영향 제품군이 넓고 패치가 시급합니다.
    summary_3: 해당 버전 사용 여부를 즉시 확인해야 합니다.
    impact: RCE
    action_required: patch
    trend_tags:
      - cve
      - exploit-in-the-wild
      - patch
    clusters:
      - browser-zero-day
    priority: p1
```

## 4. 주간용 입력 규칙

- 이번 주에 새로 등장한 사건을 우선 입력합니다.
- 대표 기사와 보조 출처를 분리합니다.
- `priority` 는 긴급도 기준으로 정합니다.
- 요약은 짧고 즉시 읽히게 작성합니다.

## 5. 월간용 입력 규칙

- 같은 사건군을 하나로 묶습니다.
- 전월 대비 변화가 드러나도록 `clusters` 를 채웁니다.
- 단기 속보보다 반복 테마를 더 중요하게 둡니다.
- 월간 해석용 필드로 `trend_tags` 와 `priority` 를 함께 사용합니다.

## 6. 뉴스레터용 입력 규칙

- 기사별 2~3줄 한글 요약을 반드시 채웁니다.
- 분류는 `취약점 / 패치`, `침해사고 / 유출`, `정부 / 기관 권고`, `벤더 / 제품 공지`, `위협 분석 / 캠페인` 중 하나로 맞춥니다.
- 중복 기사는 같은 `incident_id` 에 연결합니다.

## 7. 출력 연결

이 입력 폼은 아래 문서와 함께 사용합니다.

- `[[security-news-trend-collection-schema]]`
- `[[security-news-newsletter-format]]`
- `[[security-news-weekly-newsletter-template]]`
- `[[security-news-monthly-newsletter-template]]`
- `[[security-news-newsletter-publishing-checklist]]`

## 8. 관련 문서

- `[[security-news-rss-hub]]`
- `[[security-news-newsletter-format]]`
- `[[security-news-newsletter-publishing-checklist]]`
- `[[security-news-publishing-input-form-template]]`
- `[[security-news-publishing-input-form-json-template]]`
- `[[security-news-publishing-form-fields-googleform-notion]]`
- `[[security-news-publishing-automation-input-schema]]`
- `[[security-news-collection-workflow-checklist]]`
- `[[security-news-daily-weekly-monthly-work-template]]`
