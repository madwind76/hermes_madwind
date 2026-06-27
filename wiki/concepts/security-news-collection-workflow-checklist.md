---
title: Security News Collection Workflow Checklist
created: 2026-06-20
updated: 2026-06-21
type: concept
tags: [workflow, wiki, checklist, research, report, newsletter, collection]
sources: [concepts/security-news-rss-hub.md, concepts/security-news-trend-collection-schema.md, concepts/security-news-newsletter-format.md]
confidence: high
---

# Security News Collection Workflow Checklist

이 문서는 보안 뉴스 수집을 **실제로 운영할 때 매번 확인할 체크리스트**입니다.  
핵심은 *넓게 수집 → 사건군 정리 → 목적별 편집* 순서를 흔들리지 않게 유지하는 것입니다.

## 참고 URL
- [Reference](concepts/security-news-rss-hub.md)
- [Reference](concepts/security-news-trend-collection-schema.md)
- [Reference](concepts/security-news-newsletter-format.md)

## 1. 수집 시작 전

- [ ] 오늘의 범위를 정했는가: `일간`, `주간`, `월간`
- [ ] 오늘 확인할 소스 범위를 정했는가
- [ ] 직접 RSS와 허브/안내 페이지를 구분했는가
- [ ] 국내/해외 소스를 분리했는가
- [ ] 속보형, 공신력형, 분석형 비중을 정했는가

## 2. 수집 중

- [ ] 제목, URL, 발행일, 출처를 함께 저장했는가
- [ ] 기사 원문을 최소한 빠르게 훑어봤는가
- [ ] 같은 사건의 반복 기사도 일단 남겼는가
- [ ] KEV, 야생 공격, 긴급 패치, 공공기관 권고를 따로 표시했는가
- [ ] 기사 수보다 사건군 후보를 우선 생각했는가

## 3. 1차 분류

- [ ] CVE / 취약점으로 분류했는가
- [ ] 침해사고 / 유출로 분류했는가
- [ ] 벤더 공지 / 패치로 분류했는가
- [ ] 정부 / 기관 권고로 분류했는가
- [ ] 위협 분석 / 캠페인으로 분류했는가

## 4. 사건군 정리

- [ ] 같은 사건을 하나의 사건군으로 묶었는가
- [ ] 대표 출처와 보조 출처를 나눴는가
- [ ] 영향 범위와 대응 필요성을 적었는가
- [ ] 우선순위(`p1`, `p2`, `p3`)를 부여했는가
- [ ] 주간/월간 보고서에 들어갈 수 있는 형태인지 확인했는가

## 5. 출력 선택

- [ ] 주간 보고서용 항목을 골랐는가
- [ ] 월간 보고서용 반복 테마를 골랐는가
- [ ] 뉴스레터용 기사 카드로 편집했는가
- [ ] 쇼츠대본 후보를 따로 표시했는가

## 6. 발행 전 검수

- [ ] 기사 제목과 분류가 일치하는가
- [ ] 요약이 2~3줄로 짧고 명확한가
- [ ] 링크와 출처가 정확한가
- [ ] 중복 기사를 과도하게 남기지 않았는가
- [ ] 문서의 `updated` 날짜가 최신인가

## 7. 장애/예외 처리

- [ ] 소스가 응답하지 않으면 대체 출처를 찾는가
- [ ] 같은 이슈가 여러 개로 쪼개지면 사건군을 다시 합치는가
- [ ] 기사 수가 너무 많으면 우선순위로 줄이는가
- [ ] 중요한 사건이 누락되면 소스 범위를 다시 점검하는가

## 8. 관련 문서

- `[[security-news-rss-hub]]`
- `[[security-news-trend-collection-schema]]`
- `[[security-news-newsletter-format]]`
- `[[security-news-newsletter-publishing-checklist]]`
- `[[security-news-publishing-automation-input-schema]]`
