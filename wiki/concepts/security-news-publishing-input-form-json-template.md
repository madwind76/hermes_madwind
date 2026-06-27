---
title: Security News Publishing Input Form JSON Template
created: 2026-06-20
updated: 2026-06-21
type: concept
tags: [workflow, wiki, research, report, newsletter, template, automation, json]
sources: [concepts/security-news-publishing-input-form-template.md, concepts/security-news-publishing-sample-data.md]
confidence: high
---

# Security News Publishing Input Form JSON Template

이 문서는 보안 뉴스 발행 자동화용 입력 폼을 **JSON 형태**로 표현한 템플릿입니다.  
스크립트 연동, API 전달, 자동 검증에 바로 사용할 수 있도록 구성합니다.

## 참고 URL
- [Reference](concepts/security-news-publishing-input-form-template.md)
- [Reference](concepts/security-news-publishing-sample-data.md)

## 1. JSON 예시

```json
{
  "report_type": "weekly",
  "report_period": "2026-W25",
  "language": "ko",
  "audience": "security",
  "owner": "woojin nam",
  "items": [
    {
      "incident_id": "2026-06-20-cisa-cve-2026-xxxx",
      "headline": "CVE-2026-XXXX exploited in the wild",
      "category": "cve",
      "region": "global",
      "severity": "critical",
      "status": "active",
      "source_primary": "CISA",
      "source_secondary": ["BleepingComputer", "Vendor Advisory"],
      "published_at": "2026-06-20",
      "detected_at": "2026-06-20",
      "summary_1": "야생 공격에 악용되는 취약점이 공개됐습니다.",
      "summary_2": "영향 제품군이 넓고 즉시 패치가 필요한 상황입니다.",
      "summary_3": "해당 버전 사용 여부를 먼저 확인해야 합니다.",
      "impact": "RCE",
      "action_required": "patch",
      "trend_tags": ["cve", "exploit-in-the-wild", "patch"],
      "clusters": ["browser-zero-day"],
      "priority": "p1"
    }
  ]
}
```

## 2. JSON 구조 설명

| 키 | 타입 | 설명 |
|---|---|---|
| `report_type` | string | `weekly`, `monthly`, `newsletter` |
| `report_period` | string | 기간 식별자 |
| `language` | string | 출력 언어, 보통 `ko` |
| `audience` | string | 독자층 |
| `owner` | string | 작성자 또는 운영자 |
| `items` | array | 사건군 또는 기사 항목 목록 |

## 3. 아이템 필드 설명

| 키 | 타입 | 설명 |
|---|---|---|
| `incident_id` | string | 내부 식별자 |
| `headline` | string | 대표 제목 |
| `category` | string | 분류 |
| `region` | string | 지역 |
| `severity` | string | 심각도 |
| `status` | string | 상태 |
| `source_primary` | string | 대표 출처 |
| `source_secondary` | array[string] | 보조 출처 |
| `published_at` | string | 최초 공개일 |
| `detected_at` | string | 수집일 |
| `summary_1` | string | 1줄 요약 |
| `summary_2` | string | 2줄 요약 |
| `summary_3` | string | 3줄 요약 |
| `impact` | string | 영향 |
| `action_required` | string | 필요한 조치 |
| `trend_tags` | array[string] | 태그 |
| `clusters` | array[string] | 클러스터 |
| `priority` | string | 우선순위 |

## 4. 관련 문서

- `[[security-news-publishing-input-form-template]]`
- `[[security-news-publishing-sample-data]]`
- `[[security-news-publishing-automation-input-schema]]`
- `[[security-news-newsletter-format]]`
