---
title: Security News RSS Catalog
created: 2026-06-20
updated: 2026-06-26
type: concept
tags: [workflow, wiki, research, tool]
sources:
  - raw/articles/20260620_security_news_rss.md
  - raw/articles/20260626_weekly_newsletter_20260622-20260626.md
confidence: high
---

# Security News RSS Catalog

보안 뉴스 수집은 **실행용 저장소(DB)** 와 **문서용 저장소(위키)** 를 분리하면 가장 안정적입니다.

- **DB**: `blogwatcher-cli`가 실제로 쓰는 구독 목록, 중복 처리, 스캔 상태
- **Wiki**: RSS 선택 이유, 우선순위, 분류, 운영 메모, 쇼츠대본용 정리

이 페이지는 RSS 카탈로그를 **하이브리드 방식**으로 운영하기 위한 기준 문서입니다. 세부 원자료는 `raw/articles/20260620_security_news_rss.md` 에 보관합니다.

## 참고 URL
- [Reference](raw/articles/20260620_security_news_rss.md)

## 운영 원칙

1. **직접 RSS만 자동 수집**
   - `blogwatcher-cli` / OPML에는 직접 RSS만 넣습니다.
   - 허브 페이지는 새 피드를 찾는 참고용으로만 둡니다.

2. **허브 페이지는 분리 보관**
   - RSS 안내 페이지, 홈 페이지, 피드 목록 페이지는 위키에서만 관리합니다.
   - 실제 자동 스캔 대상은 아닙니다.

3. **국내/해외를 분리**
   - 국내: KISA, KrCERT, 데일리시큐, 보안뉴스
   - 해외: CISA, NCSC, BleepingComputer, Krebs on Security, SecurityWeek, Fortinet, The Hacker News, Cisco

4. **속보형 / 공신력형 / 분석형으로 분류**
   - 속보형: 보안뉴스, BleepingComputer, The Hacker News, 데일리시큐
   - 공신력형: KISA/KrCERT, CISA, NCSC
   - 분석형: Krebs on Security, SecurityWeek, Fortinet

## 카탈로그

### 국내 직접 RSS

| 이름 | URL | 용도 |
|---|---|---|
| KISA KrCERT 취약점 정보 | https://knvd.krcert.or.kr/rss/security/info | 취약점/공지 모니터링 |
| KISA KrCERT 보안공지 | https://knvd.krcert.or.kr/rss/security/notice | 보안 권고/공지 수집 |
| 데일리시큐 | https://www.dailysecu.com/rss/allArticle.xml | 국내 보안 뉴스 속보 |

### 국내 허브/안내

| 이름 | URL | 용도 |
|---|---|---|
| 보안뉴스 RSS 서비스 | https://www.boannews.com/custom/news_rss.asp | 카테고리별 RSS 허브 |
| KISA 취약점 정보 포털 RSS 안내 | https://knvd.krcert.or.kr/footer/rss | RSS 목록 확인 |
| KISA 보호나라 보안공지 | https://www.boho.or.kr/kr/bbs/view.do?bbsId=B0000133&pageIndex=1&nttId=71916&menuNo=205020 | 보안공지 진입점 |
| 이스트시큐리티 알약 블로그 | https://blog.alyac.co.kr/ | 분석형 보안 블로그 |

### 해외 직접 RSS (2026-06-26 갱신, 11 → 24개)

| 이름 | URL | 용도 |
|---|---|---|
| CISA News | https://www.cisa.gov/news.xml | 공신력 있는 공지/속보 |
| CISA Cybersecurity Alerts & Advisories | https://www.cisa.gov/cybersecurity-advisories/all.xml | 취약점/권고 알림 |
| UK NCSC All RSS feeds | https://www.ncsc.gov.uk/api/1/services/v1/all-rss-feed.xml | 공신력 있는 영국 보안 업데이트 |
| Krebs on Security | https://krebsonsecurity.com/feed/ | 심층 분석형 |
| SecurityWeek | https://www.securityweek.com/feed/ | 분석+산업 동향 |
| The Hacker News | https://feeds.feedburner.com/TheHackersNews | 속보형 보안 뉴스 (FeedBurner 최종 URL) |
| Cisco Security RSS | https://sec.cloudapps.cisco.com/security/center/rss.x?i=44 | 벤더 보안 공지 |
| Fortinet Blogs | https://feeds.fortinet.com/fortinet/blogs | 벤더 분석/연구 |
| Fortinet Threat Research | https://feeds.fortinet.com/fortinet/blog/threat-research | 위협 연구 중심 |
| **The Record** | https://therecord.media/feed | Recorded Future 산하, 랜섬웨어/APT 분석 |
| **Dark Reading** | https://www.darkreading.com/rss.xml | 업계 표준 보안 매체 |
| **SANS Internet Storm Center** | https://isc.sans.edu/rssfeed_full.xml | 위협 인텔 일일 다이제스트 |
| **Malwarebytes Labs** | https://www.malwarebytes.com/blog/feed/index.xml | 위협 분석 + 사용자 보호 |
| **Palo Alto Unit 42** | https://unit42.paloaltonetworks.com/feed/ | APT/위협 연구 |
| **CrowdStrike Blog** | https://www.crowdstrike.com/en-us/blog/feed | 위협 인텔 |
| **Microsoft MSRC** | https://msrc.microsoft.com/feed/ | MS 보안 권고 |
| **Cloudflare Blog** | https://blog.cloudflare.com/rss/ | 클라우드/네트워크 보안 |
| **Talos Intelligence** | http://feeds.feedburner.com/feedburner/Talos | 위협 인텔 |
| **Google Project Zero** | https://projectzero.google/feed.xml | 0-day 연구 |

### 해외 허브/안내

| 이름 | URL | 용도 |
|---|---|---|
| BleepingComputer RSS Feeds | https://www.bleepingcomputer.com/rss-feeds/ | 피드 목록 |
| NCSC RSS feeds | https://www.ncsc.gov.uk/information/rss-feeds | 피드 안내 |
| CISA Subscribe to Updates | https://www.cisa.gov/about/contact-us/subscribe-updates-cisa | 구독 진입점 |
| Fortinet RSS Feeds | https://www.fortinet.com/rss-feeds | 피드 안내 |
| SecurityWeek Home | https://www.securityweek.com/ | 홈/피드 진입점 |
| Krebs on Security Home | https://krebsonsecurity.com/ | 홈/피드 진입점 |
| The Hacker News RSS label page | https://thehackernews.com/search/label/Rss%20feeds | 관련 카테고리 페이지 |

## blogwatcher 연동 팁

- **구독 등록**: OPML import는 직접 RSS만 사용합니다.
- **참고 보관**: 허브/안내 페이지는 위키에 남기고 DB에는 넣지 않습니다.
- **실무 운영**: 새 피드 추가 시, 먼저 허브 페이지에서 직접 RSS 주소를 확인한 뒤 DB에 반영합니다.

## 연결 노트

- [[wiki-maintenance-operations]]
- [[wiki-maintenance-checklist]]
