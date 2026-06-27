---
title: Security News RSS Region Split
created: 2026-06-20
updated: 2026-06-21
type: concept
tags: [workflow, wiki, research, comparison]
sources: [raw/articles/20260620_security_news_rss.md, concepts/security-news-rss-catalog.md, concepts/security-news-rss-operations-checklist.md]
confidence: high
---

# Security News RSS Region Split

보안 뉴스 RSS는 **국내**와 **해외**를 나눠서 운영하면 우선순위 설정과 쇼츠대본 작성이 쉬워집니다.

- **국내**: KISA, KrCERT, 데일리시큐, 보안뉴스 중심
- **해외**: CISA, NCSC, BleepingComputer, Krebs on Security, SecurityWeek, Fortinet, The Hacker News, Cisco 중심

이 페이지는 `[[security-news-rss-catalog]]` 의 분류를 더 단순하게 보기 위한 운영용 보조 페이지입니다.  
실제 구독 상태는 DB에 두고, 이 페이지는 **어느 지역 소스를 우선 읽을지**를 정하는 데 사용합니다.

## 참고 URL
- [Reference](raw/articles/20260620_security_news_rss.md)
- [Reference](concepts/security-news-rss-catalog.md)
- [Reference](concepts/security-news-rss-operations-checklist.md)

## 1. 국내 우선 소스

| 이름 | 유형 | 용도 |
|---|---|---|
| KISA KrCERT 취약점 정보 | 직접 RSS | 취약점/공지 모니터링 |
| KISA KrCERT 보안공지 | 직접 RSS | 보안 권고/공지 수집 |
| 데일리시큐 | 직접 RSS | 국내 보안 뉴스 속보 |
| 보안뉴스 RSS 서비스 | 허브 | 카테고리별 RSS 확인 |
| KISA 취약점 정보 포털 RSS 안내 | 허브 | RSS 목록 확인 |
| KISA 보호나라 보안공지 | 허브 | 보안공지 진입점 |
| 이스트시큐리티 알약 블로그 | 허브 | 분석형 보안 블로그 |

## 2. 해외 우선 소스

| 이름 | 유형 | 용도 |
|---|---|---|
| CISA News | 직접 RSS | 공신력 있는 공지/속보 |
| CISA Blog | 직접 RSS | 정책/실무 관점 읽기 |
| CISA Cybersecurity Alerts & Advisories | 직접 RSS | 취약점/권고 알림 |
| UK NCSC All RSS feeds | 직접 RSS | 영국 보안 업데이트 |
| BleepingComputer | 직접 RSS | 속보형 취약점/침해사고 |
| Krebs on Security | 직접 RSS | 심층 분석형 |
| SecurityWeek | 직접 RSS | 분석+산업 동향 |
| Fortinet Blogs | 직접 RSS | 벤더 분석/연구 |
| Fortinet Threat Research | 직접 RSS | 위협 연구 중심 |
| The Hacker News | 직접 RSS | 속보형 보안 뉴스 |
| Cisco Security RSS | 직접 RSS | 벤더 보안 공지 |
| BleepingComputer RSS Feeds | 허브 | 피드 목록 |
| NCSC RSS feeds | 허브 | 피드 안내 |
| CISA Subscribe to Updates | 허브 | 구독 진입점 |
| Fortinet RSS Feeds | 허브 | 피드 안내 |
| SecurityWeek Home | 허브 | 홈/피드 진입점 |
| Krebs on Security Home | 허브 | 홈/피드 진입점 |
| The Hacker News RSS label page | 허브 | RSS 관련 카테고리 페이지 |

## 3. 운영 규칙

1. **국내와 해외를 따로 본다**
   - 국내는 정책/공공기관/국내 뉴스 추적에 유리합니다.
   - 해외는 속보와 벤더 분석을 빠르게 보기 좋습니다.

2. **목적에 따라 먼저 읽는 쪽을 다르게 둔다**
   - 쇼츠대본 후보 탐색: 해외 속보형 + 국내 공공기관
   - 공신력 검증: KISA/KrCERT + CISA + NCSC
   - 심층 해설: Krebs + SecurityWeek + Fortinet

3. **허브 페이지는 참고용으로만 둔다**
   - 허브는 새 직접 RSS를 찾는 도구입니다.
   - blogwatcher DB에는 넣지 않습니다.

## 4. 관련 문서

- `[[security-news-rss-catalog]]`
- `[[security-news-rss-operations-checklist]]`
- `[[wiki-maintenance-checklist]]`
