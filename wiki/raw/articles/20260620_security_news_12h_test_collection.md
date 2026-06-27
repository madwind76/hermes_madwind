---
title: 2026-06-20 Security News 12h Test Collection
created: 2026-06-20
updated: 2026-06-20
type: test-collection
scope: manual-test
sources: [boannews, dailysecu]
---

# 2026-06-20 보안뉴스 12시간 테스트 수집본

> 목적: 12시간 자동 수집 흐름이 **원본 기사 URL**을 정상적으로 모으는지 확인하기 위한 테스트 결과입니다.
> 기준: RSS 피드 URL은 제외하고, 기사 원본 URL만 기록합니다.

## 테스트 결과 요약

- 수집 흐름: **정상 확인**
- RSS 피드 URL 혼입: **없음**
- 원본 기사 URL 포함: **확인됨**
- 주간보고서 생성: **실행하지 않음**

## 국내 후보

| 제목 | 태그 | 원본 기사 URL | 비고 |
|---|---|---|---|---|
| 마이크로소프트 디펜더 제로데이 3종, 실제 공격 악용 가능성 제기...2 | 데일리시큐 | https://www.dailysecu.com/news/articleView.html?idxno=206306 | 원본 기사 URL 확인 |
| 마이크로소프트, '제로 데이 퀘스트 2026'서 클라우드·AI 취약점 제보에 ... | 데일리시큐 | https://www.dailysecu.com/news/articleView.html?idxno=206281 | 원본 기사 URL 확인 |
| 폰투온 베를린 2026 폐막…47개 제로데이 공개, 한국 아웃오브바운스 최종 3위 | 데일리시큐 | https://www.dailysecu.com/news/articleView.html?idxno=206759 | 원본 기사 URL 확인 |
| 아이반티 EPMM '사전 인증 RCE' 제로데이 취약점 악용…긴급 ... | 데일리시큐 | https://www.dailysecu.com/news/articleView.html?idxno=204817 | 원본 기사 URL 확인 |
| 금융보안원, 2026년 조직개편·정기 인사…모의해킹 6명→20명 확대 | 데일리시큐 | https://www.dailysecu.com/news/articleView.html?idxno=203826 | 원본 기사 URL 확인 |

## 보안뉴스 후보

| 제목 | 태그 | 원본 기사 URL | 비고 |
|---|---|---|---|---|
| 보안뉴스 전체기사/SECURITY 목록 | 보안뉴스 | https://www.boannews.com/media/list.asp?mkind=1 | 기사 목록 진입점 |
| 보안뉴스 SECURITY 목록 | 보안뉴스 | https://www.boannews.com/media/s_list.asp?skind=i | 기사 목록 진입점 |
| '선제적 보안'으로 패러다임 전환... 뚫리고 막으면 늦는다 | 보안뉴스 | https://m.boannews.com/html/detail.html?tab_type=1&idx=141322 | 기사 원본 URL 확인 |

## 결론

이번 테스트에서는 **수집본이 RSS가 아니라 원본 기사 URL 중심으로 정리될 수 있음**을 확인했습니다.

다음 단계에서는 이 테스트 형식을 바탕으로:
1. 최근 12시간 기사들을 더 넓게 모으고,
2. 중복 URL을 제거하고,
3. `wiki/raw/articles/YYYYMMDD[_HHMM]_security_news_source_collection.md` 형식으로 자동 저장하고, frontmatter에는 `collected_at`과 `saved_at`을 분리해 기록하면 됩니다.
