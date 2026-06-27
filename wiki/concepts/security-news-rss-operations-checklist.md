---
title: Security News RSS Operations Checklist
created: 2026-06-20
updated: 2026-06-21
type: concept
tags: [workflow, wiki, checklist, research]
sources: [raw/articles/20260620_security_news_rss.md, concepts/security-news-rss-catalog.md]
confidence: high
---

# Security News RSS Operations Checklist

보안 뉴스 RSS 운영은 **수집 대상 선정**, **구독 등록**, **정기 스캔**, **정리/배포**를 분리하면 관리가 쉽습니다.

- **blogwatcher DB**: 실제 구독 목록, 읽음 상태, 스캔 상태
- **Wiki**: 카탈로그, 우선순위, 허브 페이지 메모, 쇼츠대본용 분류

이 페이지는 `[[security-news-rss-catalog]]` 를 실제 운영할 때 쓰는 체크리스트입니다.  
하이브리드 방식의 핵심은 **직접 RSS는 DB**, **허브/안내는 위키**입니다.

## 참고 URL
- [Reference](raw/articles/20260620_security_news_rss.md)
- [Reference](concepts/security-news-rss-catalog.md)

## 1. 운영 원칙

1. **직접 RSS만 DB에 넣습니다.**
   - `blogwatcher-cli import` 대상은 직접 RSS입니다.
   - 허브 페이지는 참고용으로만 둡니다.

2. **국내와 해외를 분리합니다.**
   - 국내: KISA, KrCERT, 데일리시큐, 보안뉴스
   - 해외: CISA, NCSC, BleepingComputer, Krebs on Security, SecurityWeek, Fortinet, The Hacker News, Cisco

3. **속보형 / 공신력형 / 분석형으로 나눕니다.**
   - 속보형: 보안뉴스, BleepingComputer, The Hacker News, 데일리시큐
   - 공신력형: KISA/KrCERT, CISA, NCSC
   - 분석형: Krebs on Security, SecurityWeek, Fortinet

4. **쇼츠대본 후보는 바로 표시합니다.**
   - 제목만 보고도 한 줄 요약이 가능한지 먼저 봅니다.
   - 임팩트가 약하면 카탈로그에만 남기고 본문화는 미룹니다.

## 2. 등록 전 체크리스트

- [ ] 직접 RSS URL인지 확인했는가
- [ ] 허브/안내 페이지와 구분했는가
- [ ] 국내/해외 분류가 맞는가
- [ ] 중복 피드가 아닌가
- [ ] 제목이 검색/운영에 적절한가
- [ ] 쇼츠대본 후보인지 표시했는가
- [ ] 위키의 카탈로그와 DB의 구독 목록이 일치하는가

## 3. 등록 작업 순서

1. **위키 카탈로그 갱신**
   - 새 피드가 왜 필요한지, 어떤 분류인지 기록합니다.

2. **OPML 정리**
   - 직접 RSS만 추려서 OPML을 갱신합니다.

3. **DB import**
   - blogwatcher DB에 반영합니다.

4. **초기 스캔**
   - 새 피드가 실제로 읽히는지 확인합니다.

5. **위키 로그 기록**
   - 어떤 피드를 추가했는지, 어떤 허브를 참고했는지 적습니다.

## 4. 실행 예시

```bash
# blogwatcher DB 상태를 확인합니다.
# 예상 출력: 등록된 블로그 목록 또는 "No blogs tracked yet"
blogwatcher-cli --db ~/.blogwatcher-cli/blogwatcher-cli.db blogs

# 직접 RSS OPML을 import 합니다.
# 예상 출력: Imported N blog(s), skipped M duplicate(s)
blogwatcher-cli --db ~/.blogwatcher-cli/blogwatcher-cli.db import /home/kisec/.hermes/research/20260620_blogwatcher_security_rss.opml

# import 결과를 다시 확인합니다.
# 예상 출력: Tracked blogs (...) 목록
blogwatcher-cli --db ~/.blogwatcher-cli/blogwatcher-cli.db blogs

# 초기 스캔을 실행합니다.
# 예상 출력: 새 글 목록 또는 스캔 요약
blogwatcher-cli --db ~/.blogwatcher-cli/blogwatcher-cli.db scan
```

## 5. 쇼츠대본용 선별 기준

- **속보성**: 지금 당장 말할 가치가 있는가
- **영향도**: 실무자에게 실제로 중요한가
- **이해 쉬움**: 30~60초 안에 설명 가능한가
- **시사성**: CVE, 침해사고, 벤더 공지 중 무엇인지 구분되는가
- **중복성**: 이미 비슷한 뉴스가 여러 번 나온 건 아닌가

## 7. 트러블슈팅

### 6.1 RSS가 import되지 않을 때
- [ ] URL이 실제 RSS인지 확인합니다.
- [ ] 허브 페이지를 넣지 않았는지 확인합니다.
- [ ] 중복 피드로 스킵된 것은 아닌지 확인합니다.
- [ ] `blogwatcher-cli --help`로 현재 명령을 다시 봅니다.

### 6.2 스캔 결과가 비어 있을 때
- [ ] 아직 새 글이 없는 시간대인지 확인합니다.
- [ ] 피드가 정상 응답하는지 허브 페이지에서 다시 확인합니다.
- [ ] DB 경로가 맞는지 확인합니다.

### 6.3 위키와 DB가 어긋날 때
- [ ] 위키 카탈로그를 먼저 수정합니다.
- [ ] OPML을 다시 생성합니다.
- [ ] DB를 재import하거나 개별 add/remove로 맞춥니다.

## 8. 출처별 현황 집계 파이프라인

이 파이프라인은 **수집본 여러 개를 사람이 직접 세지 않도록** 만드는 단계입니다.  
기본값은 **unique original_article_url 기준**, 보조값은 **raw snapshot 기준**입니다.

```bash
# 수집본 여러 개를 한 번에 집계합니다.
# 예상 출력: raw snapshot total / unique-URL total / 출처별 요약 테이블
python3 /home/kisec/wiki/scripts/security_news_source_pipeline.py \
  --input-glob '/home/kisec/wiki/raw/articles/*security_news_source_collection*.md' \
  --output /home/kisec/wiki/raw/articles/security_news_source_summary.md

# 생성된 요약본을 확인합니다.
# 예상 출력: 출처별 unique counts와 alias normalization 메모
python3 /home/kisec/wiki/scripts/security_news_source_pipeline.py \
  --input-glob '/home/kisec/wiki/raw/articles/*security_news_source_collection*.md' \
  --output /home/kisec/wiki/raw/articles/security_news_source_summary.md \
  --json-output /home/kisec/wiki/raw/articles/security_news_source_summary.json

# 새 수집본 템플릿을 만들 때는 collected_at / saved_at을 분리합니다.
# 예상 출력: frontmatter가 포함된 새 markdown 템플릿 파일 경로
python3 /home/kisec/wiki/scripts/security_news_source_pipeline.py \
  --emit-template /home/kisec/wiki/raw/articles/YYYYMMDD_HHMM_security_news_source_collection.md \
  --title 'YYYYMMDD_HHMM Security News Source Collection' \
  --created YYYY-MM-DD \
  --updated YYYY-MM-DD \
  --collected-at 'YYYY-MM-DD HH:MM KST' \
  --saved-at 'YYYY-MM-DD HH:MM:SS KST' \
  --scope blogwatcher-12h \
  --source blogwatcher-cli \
  --source direct-rss
```

## 9. 관련 문서

- `[[security-news-rss-catalog]]`
- `[[wiki-maintenance-checklist]]`
- `[[wiki-maintenance-operations]]`
