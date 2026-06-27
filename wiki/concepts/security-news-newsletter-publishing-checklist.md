---
title: Security News Newsletter Publishing Checklist
created: 2026-06-20
updated: 2026-06-21
type: concept
tags: [workflow, wiki, research, report, newsletter, checklist]
sources: [raw/articles/20260620_security_news_rss.md, concepts/security-news-newsletter-format.md, concepts/security-news-weekly-newsletter-template.md, concepts/security-news-monthly-newsletter-template.md, concepts/security-news-trend-collection-schema.md]
confidence: high
---

# Security News Newsletter Publishing Checklist

뉴스레터 발행은 **수집 → 사건군 정리 → 주간/월간 편집 → 발행 전 검수** 순서로 진행합니다.  
이 체크리스트는 보안 뉴스 뉴스레터를 내보내기 전 마지막 확인용입니다.

## 참고 URL
- [Reference](raw/articles/20260620_security_news_rss.md)
- [Reference](concepts/security-news-newsletter-format.md)
- [Reference](concepts/security-news-weekly-newsletter-template.md)
- [Reference](concepts/security-news-monthly-newsletter-template.md)
- [Reference](concepts/security-news-trend-collection-schema.md)

## 1. 수집 확인

- [ ] 이번 주/이번 달 수집이 충분히 넓게 되었는가
- [ ] RSS, 공식 공지, 벤더 블로그, 보안 매체가 함께 들어갔는가
- [ ] 중복 기사가 너무 빨리 제거되지는 않았는가
- [ ] 허브/안내 페이지가 실제 기사와 혼동되지 않았는가

## 2. 사건군 정리 확인

- [ ] 같은 사건이 여러 출처에서 하나로 묶였는가
- [ ] 대표 출처 1~3개와 보조 출처가 구분되었는가
- [ ] 사건 유형이 `CVE / 침해사고 / 권고 / 벤더 공지 / 위협 캠페인` 등으로 분류되었는가
- [ ] 주간/월간 관점에서 묶을 수 없는 항목은 제외되었는가

## 3. 기사 편집 확인

- [ ] 기사마다 2~3줄 한글 요약이 들어갔는가
- [ ] 요약 1줄째는 무엇이 발생했는지 설명하는가
- [ ] 요약 2줄째는 왜 중요한지 설명하는가
- [ ] 요약 3줄째는 무엇을 해야 하는지 안내하는가
- [ ] 과장된 표현 없이도 핵심이 전달되는가
- [ ] 같은 사건의 중복 기사들을 불필요하게 여러 번 넣지 않았는가

## 4. 분류 구조 확인

- [ ] 분류별로 묶였는가
- [ ] `취약점 / 패치`, `침해사고 / 유출`, `정부 / 기관 권고`, `벤더 / 제품 공지`, `위협 분석 / 캠페인` 같은 묶음이 유지되었는가
- [ ] 주간판과 월간판의 기준이 섞이지 않았는가
- [ ] 주간은 긴급성, 월간은 추세와 반복에 맞게 편집되었는가

## 5. 주간판 발행 확인

- [ ] 이번 주 핵심 3~5개가 먼저 보이는가
- [ ] 야생 공격, KEV, 긴급 패치, 공공기관 권고가 앞에 배치되었는가
- [ ] 주간 결론이 1~2줄로 정리되었는가
- [ ] 다음 주에 주의할 포인트가 들어갔는가

## 6. 월간판 발행 확인

- [ ] 반복 테마가 클러스터로 묶였는가
- [ ] 전월 대비 변화가 들어갔는가
- [ ] 업종/지역/제품군별 경향이 보이는가
- [ ] 월간 결론이 해석 중심으로 정리되었는가
- [ ] 다음 달 관찰 포인트가 명시되었는가

## 7. 최종 검수

- [ ] 제목과 분류가 실제 내용과 일치하는가
- [ ] 기사별 링크와 출처가 정확한가
- [ ] 오탈자와 용어 표기가 통일되었는가
- [ ] 문서 상단의 `updated` 날짜가 최신인가
- [ ] 관련 문서 링크가 모두 들어갔는가

## 8. 관련 문서

- `[[security-news-newsletter-format]]`
- `[[security-news-weekly-newsletter-template]]`
- `[[security-news-monthly-newsletter-template]]`
- `[[security-news-trend-collection-schema]]`
- `[[security-news-rss-hub]]`
