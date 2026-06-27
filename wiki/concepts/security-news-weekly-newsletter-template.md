---
title: Security News Weekly Newsletter Template
created: 2026-06-20
updated: 2026-06-21
type: concept
tags: [workflow, wiki, research, report, newsletter, weekly]
sources: [raw/articles/20260620_security_news_rss.md, concepts/security-news-newsletter-format.md, concepts/security-news-trend-collection-schema.md]
confidence: high
---

# Security News Weekly Newsletter Template

주간 뉴스레터는 **이번 주에 바로 알아야 할 보안 뉴스**를 빠르게 읽히는 형태로 정리합니다.  
목표는 “많이 읽히는 편집본”이며, 분석 보고서처럼 길게 쓰지 않습니다.

## 참고 URL
- [Reference](raw/articles/20260620_security_news_rss.md)
- [Reference](concepts/security-news-newsletter-format.md)
- [Reference](concepts/security-news-trend-collection-schema.md)

## 1. 주간 편집 원칙

1. **이번 주 신규 이슈를 우선 배치합니다.**
   - 야생 공격, KEV 등록, 긴급 패치, 공공기관 권고를 먼저 둡니다.

2. **기사마다 2~3줄 한글 요약을 붙입니다.**
   - 무엇이 발생했는지
   - 왜 중요한지
   - 무엇을 해야 하는지

3. **중복 기사는 하나로 묶습니다.**
   - 같은 사건은 대표 기사 1개만 앞에 두고, 보조 출처는 짧게 덧붙입니다.

4. **주간 결론은 짧게 씁니다.**
   - 이번 주의 대표 테마 1~2개만 남깁니다.

## 2. 추천 섹션 구조

### A. 이번 주 핵심 3~5개
- 가장 긴급한 항목만 먼저 노출
- 공격 중인 CVE, 주요 패치, 대형 유출, 기관 권고 중심

### B. 분류별 기사 묶음
- `취약점 / 패치`
- `침해사고 / 유출`
- `정부 / 기관 권고`
- `벤더 / 제품 공지`
- `위협 분석 / 캠페인`

### C. 한 줄 주간 결론
- 이번 주의 핵심 흐름
- 다음 주에 주의할 포인트

## 3. 기사 카드 형식

| 항목 | 내용 |
|---|---|
| 제목 | 기사 제목 |
| 분류 | CVE, 침해사고, 권고 등 |
| 출처 | 대표 출처 |
| 요약 1 | 핵심 내용 1줄 |
| 요약 2 | 영향/배경 1줄 |
| 요약 3 | 대응/의미 1줄 |
| 태그 | `cve`, `rce`, `kev`, `patch`, `breach` 등 |

## 4. 주간 요약 작성 규칙

- **1줄째**: 무엇이 발생했는지
- **2줄째**: 왜 중요한지
- **3줄째**: 무엇을 해야 하는지

## 5. 편집 흐름

1. `[[security-news-trend-collection-schema]]` 에서 사건군을 모읍니다.
2. 이번 주 신규/긴급 항목을 먼저 고릅니다.
3. 같은 사건을 묶고 중복을 줄입니다.
4. 기사마다 2~3줄 한글 요약을 붙입니다.
5. 마지막에 이번 주 결론 1~2줄을 정리합니다.

## 6. 관련 문서

- `[[security-news-newsletter-format]]`
- `[[security-news-trend-collection-schema]]`
- `[[security-news-rss-hub]]`
