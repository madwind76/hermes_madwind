---
title: Security News Publishing Sample Data
created: 2026-06-20
updated: 2026-06-21
type: concept
tags: [workflow, wiki, research, report, newsletter, automation, sample]
sources: [concepts/security-news-publishing-input-form-template.md, concepts/security-news-newsletter-format.md, concepts/security-news-trend-collection-schema.md]
confidence: high
---

# Security News Publishing Sample Data

이 문서는 발행 자동화용 입력 폼을 시험하기 위한 **예시 데이터 3건**입니다.  
주간 보고서, 월간 보고서, 뉴스레터 초안 생성 테스트에 그대로 사용할 수 있습니다.

## 참고 URL
- [Reference](concepts/security-news-publishing-input-form-template.md)
- [Reference](concepts/security-news-newsletter-format.md)
- [Reference](concepts/security-news-trend-collection-schema.md)

## 1. 주간 보고서용 예시

```yaml
report_type: weekly
report_period: 2026-W25
language: ko
audience: security
owner: woojin nam
items:
  - incident_id: 2026-06-20-cisa-cve-2026-xxxx
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
    summary_1: 야생 공격에 악용되는 취약점이 공개됐습니다.
    summary_2: 영향 제품군이 넓고 즉시 패치가 필요한 상황입니다.
    summary_3: 해당 버전 사용 여부를 먼저 확인해야 합니다.
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

## 2. 월간 보고서용 예시

```yaml
report_type: monthly
report_period: 2026-06
language: ko
audience: executive
owner: woojin nam
items:
  - incident_id: 2026-06-edge-device-theme
    headline: Edge device RCE campaigns repeated across multiple vendors
    category: campaign
    region: global
    severity: high
    status: monitoring
    source_primary: SecurityWeek
    source_secondary:
      - CISA
      - Vendor Blog
      - Krebs on Security
    published_at: 2026-06-03
    detected_at: 2026-06-20
    summary_1: 여러 벤더의 엣지 장비에서 연속적으로 취약점이 보고됐습니다.
    summary_2: 한 달 동안 같은 공격면이 반복적으로 등장해 주의가 필요합니다.
    summary_3: 다음 달에도 패치와 노출 점검 우선순위를 높여야 합니다.
    impact: RCE
    action_required: monitoring
    trend_tags:
      - campaign
      - edge
      - rce
      - vendor-bulk-patch
    clusters:
      - edge-device-rce
    priority: p1
```

## 3. 뉴스레터용 예시

```yaml
report_type: newsletter
report_period: 2026-06-15~2026-06-21
language: ko
audience: general
owner: woojin nam
items:
  - article_title: KISA warns of active exploitation in Korean web app products
    article_url: https://example.org/kisa-warning
    publisher: KISA/KrCERT
    article_type: advisory
    short_summary: 국내 웹앱 제품에서 악용 정황이 확인됐습니다.\n영향 대상 버전이 명확해 빠른 확인이 필요합니다.\n사용 중인 서비스라면 즉시 업데이트 여부를 점검하세요.
    why_it_matters: 공공기관 권고라 우선 확인 가치가 높습니다.
    what_to_do: patch
    related_incident_id: 2026-06-20-kisa-webapp-advisory
```

## 4. 테스트 포인트

- 주간/월간/뉴스레터 출력이 서로 다른지 확인
- `summary_1~3` 가 자동 요약에 잘 들어가는지 확인
- `clusters` 로 같은 테마가 묶이는지 확인
- `priority` 기준으로 정렬되는지 확인
- `short_summary` 가 뉴스레터 기사 카드에 그대로 들어가는지 확인

## 5. 관련 문서

- `[[security-news-publishing-input-form-template]]`
- `[[security-news-publishing-input-form-json-template]]`
- `[[security-news-publishing-form-fields-googleform-notion]]`
- `[[security-news-publishing-automation-input-schema]]`
- `[[security-news-newsletter-format]]`
- `[[security-news-weekly-newsletter-template]]`
- `[[security-news-monthly-newsletter-template]]`
- `[[security-news-newsletter-publishing-checklist]]`
