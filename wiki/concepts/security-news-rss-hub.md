---
title: Security News RSS Hub
created: 2026-06-20
updated: 2026-06-26
type: concept
tags: [workflow, wiki, research, hub]
sources:
  - raw/articles/20260620_security_news_rss.md
  - concepts/security-news-rss-catalog.md
  - concepts/security-news-rss-operations-checklist.md
  - concepts/security-news-rss-region-split.md
  - concepts/security-news-shorts-priority-summary.md
  - concepts/security-news-shorts-script-template.md
  - raw/articles/20260626_cve-newly-discovered-202606.md
  - raw/articles/20260626_weekly_newsletter_20260622-20260626.md
  - raw/articles/20260626_weekly_trend_report_20260622-20260626.md
  - raw/articles/20260626_weekly_deep_analysis_report_20260622-20260626.md
  - raw/articles/20260626_monthly_trend_report_202606.md
confidence: high
---

# Security News RSS Hub

이 페이지는 보안 뉴스 RSS 작업을 위한 **상위 허브**입니다.

먼저 가능한 한 넓게 수집하고, 그다음 사건군으로 묶어 주간/월간 보고서에 넣는 흐름을 기준으로 정리합니다.

- `[[security-news-trend-collection-schema]]` : 주간/월간 보고서용 수집 정의
- `[[security-news-newsletter-format]]` : 분류별 기사 + 2~3줄 한글 요약 뉴스레터 형식
- `[[security-news-weekly-newsletter-template]]` : 주간 뉴스레터 템플릿
- `[[security-news-monthly-newsletter-template]]` : 월간 뉴스레터 템플릿
- `[[security-news-newsletter-publishing-checklist]]` : 발행 전 최종 검수 체크리스트
- `[[security-news-publishing-input-form-template]]` : 발행 자동화용 입력 폼 템플릿
- `[[security-news-publishing-input-form-json-template]]` : JSON 버전 입력 폼 템플릿
- `[[security-news-publishing-form-fields-googleform-notion]]` : Google Form / Notion 필드 목록
- `[[security-news-publishing-automation-input-schema]]` : 자동화 스크립트용 입력 스키마
- `[[security-news-publishing-sample-data]]` : 발행 자동화용 예시 데이터 3건
- `[[security-news-collection-workflow-checklist]]` : 보안 뉴스 수집 운영 체크리스트
- `[[security-news-daily-weekly-monthly-work-template]]` : 일간/주간/월간 작업 템플릿
- `[[security-news-rss-catalog]]` : 전체 카탈로그
- `[[security-news-rss-operations-checklist]]` : 등록/운영 체크리스트
- `[[security-news-rss-region-split]]` : 국내/해외 분리 보기
- `[[security-news-shorts-priority-summary]]` : 쇼츠대본용 우선순위 요약
- `[[security-news-shorts-script-template]]` : 실제 대본 템플릿

## 6월 누계 보고서 family (2026-06-26)

- [6월 신규 취약점 종합 (NVD 6,743 + CISA KEV 22)](raw/articles/20260626_cve-newly-discovered-202606.md)
- [6/22~26 주간 뉴스레터 (표준 양식 편집본)](raw/articles/20260626_weekly_newsletter_20260622-20260626.md)
- [6/22~26 주간 분석 보고서 (요약)](raw/articles/20260626_weekly_trend_report_20260622-20260626.md)
- [6/22~26 주간 심층 분석 보고서 (MITRE ATT&CK + Kill Chain + IOC + Sigma 룰)](raw/articles/20260626_weekly_deep_analysis_report_20260622-20260626.md)
- [6월 월간 보고서 (4주 통합, 328건 기사)](raw/articles/20260626_monthly_trend_report_202606.md)

## 참고 URL
- [Reference](raw/articles/20260620_security_news_rss.md)
- [Reference](concepts/security-news-rss-catalog.md)
- [Reference](concepts/security-news-rss-operations-checklist.md)
- [Reference](concepts/security-news-rss-region-split.md)
- [Reference](concepts/security-news-shorts-priority-summary.md)
- [Reference](concepts/security-news-shorts-script-template.md)

## 1. 사용 목적

1. **수집 대상 선별**
   - RSS 후보를 위키에 기록합니다.
   - 허브/안내 페이지와 직접 RSS를 구분합니다.

2. **우선순위 결정**
   - 속보성, 공신력, 설명 난이도를 기준으로 읽는 순서를 정합니다.

3. **쇼츠대본 작성**
   - 상위 후보를 골라 템플릿에 넣고 30~60초 분량으로 압축합니다.

4. **운영 정리**
   - DB는 실제 구독과 상태 관리.
   - 위키는 설명, 분류, 재사용 가능한 기준 정리.

## 2. 권장 흐름

1. `[[security-news-rss-catalog]]` 에서 전체 RSS를 확인합니다.
2. `[[security-news-rss-region-split]]` 로 국내/해외를 나눠 봅니다.
3. `[[security-news-rss-operations-checklist]]` 로 등록/스캔을 처리합니다.
4. `[[security-news-shorts-priority-summary]]` 에서 쇼츠 후보를 고릅니다.
5. `[[security-news-shorts-script-template]]` 으로 대본을 씁니다.

## 3. 운영 원칙

- **직접 RSS는 DB**, **허브/안내는 위키**
- **국내/해외는 분리**, 필요할 때만 합쳐서 비교
- **속보형/공신력형/분석형**을 함께 보되, 쇼츠에서는 우선순위를 둠
- **중복 제거**와 **출처 확인**을 먼저 하고, 그 다음에 요약

## 4. 관련 문서

- `[[security-news-rss-catalog]]`
- `[[security-news-rss-operations-checklist]]`
- `[[security-news-rss-region-split]]`
- `[[security-news-shorts-priority-summary]]`
- `[[security-news-shorts-script-template]]`
