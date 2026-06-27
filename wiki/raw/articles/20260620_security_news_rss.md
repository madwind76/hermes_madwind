---
sha256: 1c33312a67812941195f3e16f8b48a70394e1e9d783db87210ebfb2b0e81111b
source: /home/kisec/.hermes/research/20260620_security_news_rss.md
archived: 2026-06-20
---

# 2026-06-20 보안 뉴스 RSS 카탈로그 원자료

> 목적: blogwatcher/OPML로 수집할 보안 뉴스 RSS를 선별하기 위한 원자료.
> 기준: 국내/해외/허브 페이지를 구분하고, 실제 구독용은 직접 RSS 위주로 유지한다.
> 수집 원칙: RSS는 *피드 주소*이고, 기사 카드/보고서에는 **원본 기사 URL**을 반드시 함께 기록한다.

---

## 국내 직접 RSS

| 이름 | 주소 | 비고 |
|---|---|---|
| KISA KrCERT 취약점 정보 | https://knvd.krcert.or.kr/rss/security/info | 직접 RSS |
| KISA KrCERT 보안공지 | https://knvd.krcert.or.kr/rss/security/notice | 직접 RSS |
| 데일리시큐 | https://www.dailysecu.com/rss/allArticle.xml | 국내 보안 뉴스 RSS |

## 국내 허브/안내 페이지

| 이름 | 주소 | 비고 |
|---|---|---|
| 보안뉴스 RSS 서비스 | https://www.boannews.com/custom/news_rss.asp | 카테고리별 RSS 허브 |
| KISA 취약점 정보 포털 RSS 안내 | https://knvd.krcert.or.kr/footer/rss | RSS 목록 안내 페이지 |
| KISA 보호나라 보안공지 | https://www.boho.or.kr/kr/bbs/view.do?bbsId=B0000133&pageIndex=1&nttId=71916&menuNo=205020 | 보안공지 예시 페이지 |
| 이스트시큐리티 알약 블로그 | https://blog.alyac.co.kr/ | 공식 보안 블로그, RSS 주소는 추가 확인 권장 |

## 해외 직접 RSS

| 이름 | 주소 | 비고 |
|---|---|---|
| CISA News | https://www.cisa.gov/news.xml | 직접 RSS |
| CISA Blog | https://www.cisa.gov/cisa/blog.xml | 직접 RSS |
| CISA Cybersecurity Alerts & Advisories | https://www.cisa.gov/cybersecurity-advisories/all.xml | 직접 RSS |
| UK NCSC All RSS feeds | https://www.ncsc.gov.uk/api/1/services/v1/all-rss-feed.xml | 직접 RSS |
| BleepingComputer | https://www.bleepingcomputer.com/feed/ | 직접 RSS |
| Krebs on Security | https://krebsonsecurity.com/feed/ | 직접 RSS |
| SecurityWeek | https://www.securityweek.com/feed/ | 직접 RSS |
| Fortinet Blogs | https://feeds.fortinet.com/fortinet/blogs | 직접 RSS |
| Fortinet Threat Research | https://feeds.fortinet.com/fortinet/blog/threat-research | 직접 RSS |
| The Hacker News | https://thehackernews.com/feeds/posts/default?alt=rss | 직접 RSS |
| Cisco Security RSS | https://sec.cloudapps.cisco.com/security/center/rss.x?i=44 | 직접 RSS |

## 해외 허브/안내 페이지

| 이름 | 주소 | 비고 |
|---|---|---|
| BleepingComputer RSS Feeds | https://www.bleepingcomputer.com/rss-feeds/ | 피드 목록 페이지 |
| NCSC RSS feeds | https://www.ncsc.gov.uk/information/rss-feeds | 피드 안내 페이지 |
| CISA Subscribe to Updates | https://www.cisa.gov/about/contact-us/subscribe-updates-cisa | 구독 안내 페이지 |
| Fortinet RSS Feeds | https://www.fortinet.com/rss-feeds | 피드 안내 페이지 |
| SecurityWeek Home | https://www.securityweek.com/ | 홈/피드 진입점 |
| Krebs on Security Home | https://krebsonsecurity.com/ | 홈/피드 진입점 |
| The Hacker News RSS label page | https://thehackernews.com/search/label/Rss%20feeds | RSS 관련 카테고리 페이지 |

## 운영 메모

- **실제 구독 상태는 DB**, **선별 기준과 카탈로그는 위키**에 둔다.
- blogwatcher에는 **직접 RSS**만 넣고, 허브/안내 페이지는 참고용으로 남긴다.
- 허브 페이지는 새 피드가 생겼는지 확인하는 용도이고, 자동 스캔 대상은 아니다.
- RSS로 수집한 개별 기사도 최종 수집본에는 반드시 **원본 기사 URL**을 저장한다.

## 관련 파일

- 연구 원문: `~/.hermes/research/20260620_security_news_rss.md`
- blogwatcher용 OPML: `~/.hermes/research/20260620_blogwatcher_security_rss.opml`
- 허브 포함 OPML: `~/.hermes/research/20260620_blogwatcher_security_rss_combined_dedup.opml`
- import 스크립트: `~/.hermes/research/20260620_blogwatcher_import_security_rss.sh`
