---
title: Security News Publishing Form Fields for Google Form and Notion
created: 2026-06-20
updated: 2026-06-21
type: concept
tags: [workflow, wiki, research, report, newsletter, template, automation, google-form, notion]
sources: [concepts/security-news-publishing-input-form-template.md, concepts/security-news-publishing-input-form-json-template.md]
confidence: high
---

# Security News Publishing Form Fields for Google Form and Notion

이 문서는 **Google Form** 또는 **Notion 데이터베이스**에 그대로 옮기기 위한 필드 목록입니다.  
자동화 이전에 사람이 수동으로 입력할 때 가장 실용적인 형태로 정리합니다.

## 참고 URL
- [Reference](concepts/security-news-publishing-input-form-template.md)
- [Reference](concepts/security-news-publishing-input-form-json-template.md)

## 1. 폼 구성 원칙

- 한 필드는 한 의미만 갖습니다.
- 선택지형 필드는 가능한 한 고정값으로 둡니다.
- 뉴스레터/보고서/월간 요약을 같은 폼으로 입력할 수 있게 공통 필드를 우선 둡니다.

## 2. 권장 필드 목록

### 2.1 문서 메타

| 필드명 | 타입 | 필수 | 비고 |
|---|---|---|---|
| Report Type | Dropdown | Yes | `weekly`, `monthly`, `newsletter` |
| Report Period | Short answer | Yes | `2026-W25`, `2026-06` 등 |
| Language | Dropdown | Yes | 기본값 `ko` |
| Audience | Dropdown | Yes | `general`, `security`, `ops`, `executive` |
| Owner | Short answer | Yes | 작성자 이름 |

### 2.2 사건군 필드

| 필드명 | 타입 | 필수 | 비고 |
|---|---|---|---|
| Incident ID | Short answer | Yes | 내부 식별자 |
| Headline | Short answer | Yes | 대표 제목 |
| Category | Dropdown | Yes | `cve`, `breach`, `advisory`, `vendor_notice`, `campaign` |
| Region | Dropdown | Yes | `kr`, `global` |
| Severity | Dropdown | Yes | `critical`, `high`, `medium`, `low` |
| Status | Dropdown | Yes | `new`, `active`, `patched`, `mitigated`, `monitoring` |
| Primary Source | Short answer | Yes | 대표 출처 |
| Secondary Sources | Paragraph | No | 줄바꿈으로 여러 개 입력 |
| Published At | Date | Yes | 최초 공개일 |
| Detected At | Date | Yes | 수집일 |
| Summary 1 | Paragraph | Yes | 1줄 요약 |
| Summary 2 | Paragraph | Yes | 2줄 요약 |
| Summary 3 | Paragraph | Yes | 3줄 요약 |
| Impact | Short answer | Yes | `RCE`, `LPE`, `data leak` 등 |
| Action Required | Short answer | Yes | `patch`, `monitoring`, `investigate` 등 |
| Trend Tags | Paragraph | No | 쉼표 구분 권장 |
| Clusters | Paragraph | No | 추세 클러스터 |
| Priority | Dropdown | Yes | `p1`, `p2`, `p3` |

### 2.3 뉴스레터 기사 필드

| 필드명 | 타입 | 필수 | 비고 |
|---|---|---|---|
| Article Title | Short answer | Yes | 기사 제목 |
| Article URL | Short answer | Yes | 원문 링크 |
| Publisher | Short answer | Yes | 매체/기관 |
| Article Type | Dropdown | Yes | `breaking`, `analysis`, `advisory`, `explain` |
| Short Summary | Paragraph | Yes | 2~3줄 한글 요약 |
| Why It Matters | Paragraph | Yes | 중요 포인트 |
| What To Do | Short answer | Yes | 대응 행동 |
| Related Incident ID | Short answer | No | 사건군 연결 |

## 3. Notion 데이터베이스 권장 속성

| 속성명 | 타입 | 비고 |
|---|---|---|
| Title | Title | 기사 또는 사건군 제목 |
| Report Type | Select | `weekly` / `monthly` / `newsletter` |
| Category | Select | 분류 |
| Severity | Select | 심각도 |
| Status | Select | 상태 |
| Priority | Select | 우선순위 |
| Published At | Date | 공개일 |
| Detected At | Date | 수집일 |
| Source Primary | URL/Text | 대표 출처 |
| Source Secondary | Text | 보조 출처 목록 |
| Summary 1/2/3 | Text | 요약 3줄 |
| Tags | Multi-select | 추세 태그 |
| Clusters | Multi-select | 클러스터 |

## 4. 관련 문서

- `[[security-news-publishing-input-form-template]]`
- `[[security-news-publishing-input-form-json-template]]`
- `[[security-news-publishing-automation-input-schema]]`
