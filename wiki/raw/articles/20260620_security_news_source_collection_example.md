---
title: 20260620 Security News Source Collection Example
created: 2026-06-20
updated: 2026-06-20
collected_at: 2026-06-20
saved_at: 2026-06-22 02:16:47 KST
type: source-collection
scope: blogwatcher-12h
sources: [blogwatcher-cli, direct-rss]
---

# 20260620 보안 뉴스 수집본 예시

> 이 파일은 보안뉴스 수집본 템플릿 예시입니다.
> 실제 운영본과 같은 형식을 따르며, 기사 메타정보에 2~3문장 요약을 포함합니다.
> RSS 피드 URL은 제외하고 원본 기사 URL만 기록합니다.

## 수집 결과

- import: Imported 1 blog(s), skipped 0 duplicate(s)
- scan: scan done
- unread_articles: 1

## 기사 목록

| 제목 | 매체 | 태그 | 발행일 | 원본 기사 URL | 분류 | 요약 |
|---|---|---|---|---|---|---|
| FortiBleed: 86,000 Fortinet Device Credentials Compromised | SecurityWeek | SecurityWeek | 2026-06-18 | https://www.securityweek.com/fortibleed-86000-fortinet-device-credentials-compromised/ | credential theft, Fortinet, VPN | Hackers have compiled a database of over 86,000 working credentials for internet-accessible Fortinet firewalls and VPNs. The large-scale credential theft campaign hit roughly half of the internet-accessible Fortinet firewalls and VPNs. |

## 메모

- 예시 파일은 템플릿 확인용입니다.
- 운영본에서는 `blogwatcher-cli` 결과를 기반으로 최신 unread 기사들을 채웁니다.
- 수집 후 unread 항목은 read-all 처리하여 다음 실행 시 새 글만 남깁니다.
