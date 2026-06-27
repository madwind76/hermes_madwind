---
title: Security News Newsletter Format
created: 2026-06-20
updated: 2026-06-21
type: concept
tags: [workflow, wiki, research, report, newsletter]
sources: [raw/articles/20260620_security_news_rss.md, concepts/security-news-trend-collection-schema.md, concepts/security-news-rss-hub.md]
confidence: high
---

# Security News Newsletter Format

뉴스레터는 주간/월간 보안 동향 보고서와 달리, **읽기 쉬운 편집본**이 목적입니다.  
따라서 수집된 보안 뉴스를 **분류별로 묶고**, 각 기사에는 **2~3줄 한글 요약**을 붙여 전달합니다.

## 참고 URL
- [Reference](raw/articles/20260620_security_news_rss.md)
- [Reference](concepts/security-news-trend-collection-schema.md)
- [Reference](concepts/security-news-rss-hub.md)

## 1. 뉴스레터 편집 원칙

1. **분류별로 먼저 묶습니다.**
   - 예: `CVE / 취약점`, `침해사고`, `벤더 공지`, `정부 권고`, `위협 캠페인`

2. **기사마다 2~3줄 한글 요약을 붙입니다.**
   - 제목만 보지 않고, 핵심 영향과 대응 포인트를 함께 적습니다.
   - 너무 길게 쓰지 않고, 기사당 짧고 정확하게 유지합니다.

3. **보고서보다 읽기 쉽게 구성합니다.**
   - 보고서는 분석 중심
   - 뉴스레터는 스캔 가능한 목록 중심

4. **같은 사건은 하나의 묶음으로 처리합니다.**
   - 여러 매체에서 같은 사건을 다뤄도 대표 기사 1건을 중심으로 배치하고, 보조 출처를 함께 표시합니다.

## 2. 추천 섹션 구조

### A. 이번 주 핵심
- 가장 중요한 이슈 3~5개
- 야생 공격, KEV, 대규모 패치, 공공기관 권고 우선

### B. 분류별 기사 묶음
- `취약점 / 패치`
- `침해사고 / 유출`
- `정부 / 기관 권고`
- `벤더 / 제품 공지`
- `위협 분석 / 캠페인`

### C. 한 줄 결론
- 이번 주 어떤 테마가 많았는지
- 다음 주에 주의할 포인트

## 3. 기사 카드 형식

각 기사는 아래 형식으로 적습니다.

| 항목 | 내용 |
|---|---|
| 제목 | 기사 제목 |
| 분류 | CVE, 침해사고, 권고 등 |
| 출처 | 대표 출처 |
| 요약 1 | 핵심 내용 1줄 |
| 요약 2 | 영향/배경 1줄 |
| 요약 3 | 대응/의미 1줄 |
| 태그 | `cve`, `rce`, `kev`, `patch`, `breach` 등 |

### 예시

**예시 기사: CVE-2026-XXXX in the wild**
- 취약점 세부 내용이 공개됐고, 야생 공격 징후가 확인됐습니다.
- 영향 제품은 특정 버전군이며, 익스플로잇 가능성이 높습니다.
- 해당 제품을 쓰는 환경은 즉시 패치와 노출 점검이 필요합니다.

## 4. 요약 작성 규칙

- **1줄째**: 무엇이 발생했는지
- **2줄째**: 왜 중요한지
- **3줄째**: 무엇을 해야 하는지

## 5. 제작 흐름

1. `[[security-news-trend-collection-schema]]` 에서 사건군을 모읍니다.
2. `[[security-news-rss-catalog]]` 와 원문 출처를 확인합니다.
3. 같은 사건을 묶고 중복을 줄입니다.
4. 분류별로 편집한 뒤, 각 기사에 2~3줄 한국어 요약을 붙입니다.
5. 필요하면 `[[security-news-shorts-script-template]]` 를 활용해 짧은 요약도 별도로 만들 수 있습니다.

## 6. 관련 문서

- `[[security-news-trend-collection-schema]]`
- `[[security-news-rss-hub]]`
- `[[security-news-rss-catalog]]`
- `[[security-news-shorts-priority-summary]]`
- `[[security-news-shorts-script-template]]`
- `[[security-news-weekly-newsletter-template]]`
- `[[security-news-monthly-newsletter-template]]`
- `[[security-news-newsletter-publishing-checklist]]`
- `[[security-news-publishing-input-form-template]]`
- `[[security-news-publishing-input-form-json-template]]`
- `[[security-news-publishing-form-fields-googleform-notion]]`
- `[[security-news-publishing-automation-input-schema]]`
- `[[security-news-publishing-sample-data]]`
- `[[security-news-collection-workflow-checklist]]`
- `[[security-news-daily-weekly-monthly-work-template]]`
