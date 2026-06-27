---
title: Security News Publishing Automation Input Schema
created: 2026-06-20
updated: 2026-06-21
type: concept
tags: [workflow, wiki, research, report, newsletter, template, automation, schema]
sources: [concepts/security-news-publishing-input-form-template.md, concepts/security-news-publishing-input-form-json-template.md, concepts/security-news-publishing-sample-data.md]
confidence: high
---

# Security News Publishing Automation Input Schema

이 문서는 주간/월간 보고서와 뉴스레터를 생성하는 **자동화 스크립트용 입력 스키마**입니다.  
목표는 외부 RSS 수집 결과를 이 구조로 정규화한 뒤, 후속 렌더러가 동일한 출력 형식을 만들게 하는 것입니다.

## 참고 URL
- [Reference](concepts/security-news-publishing-input-form-template.md)
- [Reference](concepts/security-news-publishing-input-form-json-template.md)
- [Reference](concepts/security-news-publishing-sample-data.md)

## 1. 스키마 목적

1. 수집 원문을 정규화합니다.
2. 사건군과 기사를 분리합니다.
3. 주간/월간/뉴스레터 출력 타입을 하나의 구조로 통합합니다.
4. 자동 검증에서 누락 필드를 바로 찾습니다.

## 2. 최상위 구조

| 필드 | 타입 | 필수 | 설명 |
|---|---|---|---|
| `report_type` | string | Yes | `weekly`, `monthly`, `newsletter` |
| `report_period` | string | Yes | 출력 기간 |
| `language` | string | Yes | 보통 `ko` |
| `audience` | string | Yes | 독자층 |
| `owner` | string | Yes | 운영자 |
| `items` | array | Yes | 출력 대상 목록 |

## 3. item 공통 스키마

```yaml
# 자동화 스크립트용 입력 스키마 예시
report_type: weekly
report_period: 2026-W25
language: ko
audience: security
owner: woojin nam
items:
  - id: unique-item-id
    kind: incident
    title: 대표 제목
    category: cve
    severity: critical
    status: active
    primary_source: CISA
    secondary_sources:
      - BleepingComputer
      - Vendor Advisory
    published_at: 2026-06-20
    detected_at: 2026-06-20
    summary:
      - 1줄 요약
      - 2줄 요약
      - 3줄 요약
    impact: RCE
    action_required: patch
    tags:
      - cve
      - exploit-in-the-wild
      - patch
    clusters:
      - browser-zero-day
    priority: p1
```

## 4. 필수 검증 규칙

- `report_type` 은 반드시 셋 중 하나여야 합니다.
- `items` 는 최소 1개 이상이어야 합니다.
- `summary` 는 3개 문장을 권장합니다.
- `priority` 는 `p1`, `p2`, `p3` 중 하나로 제한합니다.
- `category` 와 `status` 는 고정된 열거형 값으로 처리합니다.

## 5. 출력 단계별 매핑

| 자동화 단계 | 입력 필드 | 출력 결과 |
|---|---|---|
| 정규화 | `items[]` | 중복 제거된 사건군 목록 |
| 분류 | `category`, `clusters`, `tags` | 주간/월간/뉴스레터 섹션 |
| 편집 | `summary`, `impact`, `action_required` | 기사 카드 또는 보고서 블록 |
| 우선순위화 | `priority`, `severity` | 노출 순서 |

## 6. 관련 문서

- `[[security-news-publishing-input-form-template]]`
- `[[security-news-publishing-input-form-json-template]]`
- `[[security-news-publishing-form-fields-googleform-notion]]`
- `[[security-news-publishing-sample-data]]`
