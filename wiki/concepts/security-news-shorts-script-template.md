---
title: Security News Shorts Script Template
created: 2026-06-20
updated: 2026-06-21
type: concept
tags: [workflow, wiki, research, summary, template]
sources: [raw/articles/20260620_security_news_rss.md, concepts/security-news-shorts-priority-summary.md, concepts/security-news-rss-catalog.md]
confidence: high
---

# Security News Shorts Script Template

보안 뉴스 쇼츠대본은 **한 줄 훅 → 핵심 사실 → 왜 중요한지 → 한 줄 마무리** 순서로 쓰면 가장 안정적입니다.

이 템플릿은 `[[security-news-shorts-priority-summary]]` 에서 고른 뉴스 후보를 30~60초 분량으로 압축할 때 사용합니다.

## 참고 URL
- [Reference](raw/articles/20260620_security_news_rss.md)
- [Reference](concepts/security-news-shorts-priority-summary.md)
- [Reference](concepts/security-news-rss-catalog.md)

## 1. 기본 구조

1. **훅(Hook)**
   - 시청자가 바로 멈출 한 줄
   - 예: “이번 주 보안 이슈는 이 한 줄로 정리됩니다.”

2. **핵심 사실(Facts)**
   - 제품명, CVE, 영향, 상태를 짧게 전달
   - 숫자와 키워드를 먼저 줍니다

3. **왜 중요한지(Impact)**
   - 공격자 관점: 어떻게 악용되는가
   - 방어자 관점: 무엇을 바로 확인해야 하는가

4. **마무리(Call to action)**
   - 패치/업데이트/점검 요청
   - “해당 제품을 쓰신다면 지금 버전 확인이 필요합니다.” 같은 식으로 끝냅니다

## 2. 템플릿 문장

### 2.1 한 건 요약형

> [훅] [제품/서비스]에서 [취약점/사고]가 나왔습니다.
> [핵심 사실] [CVE/이름], [영향], [상태]입니다.
> [중요성] 공격자는 [악용 방식]을 노릴 수 있고, 방어자는 [점검 포인트]를 확인해야 합니다.
> [마무리] 지금 바로 [패치/업데이트/로그 확인]을 해두는 것이 좋습니다.

### 2.2 비교형

> [훅] 이번 뉴스는 “속보”보다 “영향”이 더 중요합니다.
> [핵심 사실] [A]는 [영향], [B]는 [영향]입니다.
> [중요성] 하나는 즉시 패치, 다른 하나는 모니터링이 우선입니다.
> [마무리] 둘 다 해당되면 우선순위를 나눠 대응하세요.

### 2.3 경고형

> [훅] 이 이슈는 그냥 넘어가면 안 됩니다.
> [핵심 사실] [제품/기관]에서 [문제]가 확인됐고, [상태]입니다.
> [중요성] 이미 알려진 공격 패턴과 연결될 수 있습니다.
> [마무리] 영향 범위를 먼저 확인하고, 외부 노출 여부를 점검하세요.

## 3. 제작 체크리스트

- [ ] 제목만 봐도 한 줄 훅이 나오는가
- [ ] CVE / 제품명 / 영향이 한 번에 보이는가
- [ ] 30~60초 안에 설명 가능한가
- [ ] 공신력 소스로 한 번 더 확인했는가
- [ ] 방어자 관점의 행동 지침이 포함됐는가
- [ ] 과장된 표현 없이도 충분히 긴장감이 있는가

## 4. 권장 스크립트 길이

- **15초**: 훅 + 핵심 사실 1개 + 마무리 1개
- **30초**: 훅 + 핵심 사실 2개 + 영향 + 마무리
- **60초**: 훅 + 배경 + 핵심 사실 + 영향 + 방어 조치

## 5. 실전 작성 순서

1. `[[security-news-shorts-priority-summary]]` 에서 상위 후보를 고릅니다.
2. `[[security-news-rss-catalog]]` 에서 직접 RSS와 출처를 확인합니다.
3. 공신력 소스(CISA, KISA/KrCERT, NCSC 등)로 사실을 검증합니다.
4. 템플릿에 맞춰 30~60초 분량으로 압축합니다.
5. 필요하면 `[[security-news-rss-operations-checklist]]` 기준으로 후속 정리를 합니다.

## 6. 예시 골격

```text
[훅]
이번 보안 뉴스는 패치가 늦으면 바로 위험해질 수 있습니다.

[핵심 사실]
이번 이슈는 [제품명]의 [취약점/사고]로, [영향]이 확인됐습니다.

[중요성]
공격자는 [악용 방식]을 노릴 수 있고, 방어자는 [점검 포인트]를 확인해야 합니다.

[마무리]
해당 제품을 쓰고 있다면 버전 확인과 업데이트를 먼저 하세요.
```

## 7. 관련 문서

- `[[security-news-shorts-priority-summary]]`
- `[[security-news-rss-catalog]]`
- `[[security-news-rss-operations-checklist]]`
- `[[security-news-rss-region-split]]`
