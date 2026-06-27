---
title: Wiki Maintenance Operations
created: 2026-06-14
updated: 2026-06-21
type: concept
tags: [wiki, maintenance, operations, automation]
sources: [/home/kisec/wiki/concepts/wiki-maintenance-checklist.md, /home/kisec/wiki/queries/web-ctf-master-checklist.md, /home/kisec/wiki/index.md, /home/kisec/wiki/log.md]
confidence: high
---

# Wiki Maintenance Operations

> **목적**: 매일 새벽 4시에 수행되는 wiki 자동 점검 작업의 운영 규칙을 세분화한 실행 문서입니다.
> **적용 대상**: `concepts/`, `queries/`, `entities/`, `comparisons/`, `index.md`, `log.md`, asset 파일, reciprocal links
> **기준 문서**: [[wiki-maintenance-checklist]]

## 참고 URL
- [Reference](/home/kisec/wiki/concepts/wiki-maintenance-checklist.md)
- [Reference](/home/kisec/wiki/queries/web-ctf-master-checklist.md)
- [Reference](/home/kisec/wiki/index.md)
- [Reference](/home/kisec/wiki/log.md)

## 1. 운영 원칙

1. **최소 수정 원칙**을 우선합니다. 필요한 라인만 고칩니다.
2. **존재하는 페이지 우선**입니다. 새 페이지를 만들기 전에 기존 페이지로 대체할 수 있는지 확인합니다.
3. **문제 원인별로 분리 처리**합니다. 링크, 중복, 인덱스, 로그, asset을 한 번에 섞어 고치지 않습니다.
4. **검증 없는 추측 금지**입니다. 파일에 실제로 보이는 것만 반영합니다.
5. **대칭성보다 정확성**을 우선합니다. 역링크는 의미가 맞을 때만 추가합니다.

## 2. 실행 단계

### 2.1 Discovery
- wiki 전체에서 wikilink를 찾습니다.
- `index.md`의 현재 카운트와 `log.md`의 최신 변경을 확인합니다.
- orphan 후보와 중복 후보를 찾습니다.
- asset 참조를 대조합니다.

### 2.2 Triage
각 이슈는 아래 5개 범주 중 하나로 분류합니다.

| 범주 | 설명 | 기본 조치 |
|------|------|----------|
| Broken link | 대상이 없는 wikilink | 대체 페이지로 교체, 없으면 일반 텍스트화 |
| Missing reciprocal | 허브/상위 개념에 역링크 부재 | 의미가 맞는 경우만 역링크 추가 |
| Orphan | inbound link가 없는 페이지 | 허브/이웃 페이지에서 1~2개 연결 추가 |
| Duplicate | 유사/중복 페이지 | 유지 페이지 하나 선택 후 링크 이전 |
| Drift | index/log/asset 불일치 | 실제 파일 상태 기준으로 동기화 |

### 2.3 Fix
- 한 번에 하나의 범주만 처리합니다.
- 수정 범위는 최소화합니다.
- 링크를 바꿀 때는 **대상 페이지가 실제 존재하는지** 바로 확인합니다.
- 중복 병합은 링크 업데이트 후에만 삭제를 진행합니다.

### 2.4 Verify
- 수정한 파일을 다시 읽습니다.
- 새 링크가 실제 페이지로 연결되는지 확인합니다.
- `index.md`의 페이지 수와 수정된 행을 재검증합니다.
- `log.md`는 실제 변경이 있을 때만 1회 기록했는지 확인합니다.

## 3. 상세 운영 규칙

### 3.1 Broken link 처리 규칙
1. ``page-name``가 존재하지 않으면 우선 대체 대상 검색을 수행합니다.
2. 동일 주제의 기존 페이지가 있으면 링크를 그쪽으로 바꿉니다.
3. 대체가 없고 본문 가치도 낮으면 일반 텍스트로 낮춥니다.
4. 링크를 삭제한 경우, 문장 의미가 깨지지 않는지 확인합니다.

### 3.2 Reciprocal link 처리 규칙
1. hub page, topic map, overview page에는 하위 페이지 링크를 둡니다.
2. 하위 페이지에는 hub로 돌아오는 링크를 둘 수 있지만, 자기참조는 금지합니다.
3. 관련성이 약하면 역링크를 추가하지 않습니다.
4. 이미 충분히 연결되어 있으면 중복 역링크를 만들지 않습니다.

### 3.3 Orphan 처리 규칙
1. orphan이지만 재사용 가치가 있으면 관련 허브에 1개 이상 연결합니다.
2. orphan이 사실상 중복이면 유지 페이지로 통합합니다.
3. orphan이 일회성 노트이면 유지 여부를 별도로 판단합니다.
4. 고립 페이지가 늘어나면 `concepts/`의 상위 허브 구조를 먼저 점검합니다.

### 3.4 Duplicate 처리 규칙
1. 제목, 태그, 첫 단락, 관련 링크를 비교합니다.
2. 검색성이 좋은 제목과 더 많은 inbound link를 가진 페이지를 유지합니다.
3. 유일한 내용은 유지 페이지로 이동합니다.
4. 삭제 전후에 링크가 끊기지 않았는지 확인합니다.

### 3.5 Index / Log 운영 규칙
1. `index.md`는 실제 파일 상태를 반영해야 합니다.
2. 페이지 추가/삭제/이동이 있으면 카운트와 날짜를 함께 갱신합니다.
3. `log.md`는 한 번의 정리 작업당 1개 엔트리만 남깁니다.
4. 같은 변경을 중복 기록하지 않습니다.
5. 표 행의 파이프 개수는 기존 형식을 유지합니다.

### 3.6 Asset 운영 규칙
1. SVG/HTML/image 참조가 있으면 파일 존재를 확인합니다.
2. 필요하지만 없으면 재생성하고, 불필요하면 참조를 제거합니다.
3. asset이 본문 의미를 보강하지 않으면 참조를 축소합니다.
4. 시각화 파일은 위키 본문과 내용이 일치해야 합니다.

## 4. 자동 수정 허용 범위

자동화는 아래 범위까지만 수행합니다.
- 기존 문구의 링크 교체
- 명백한 중복 링크 제거
- 허브 페이지에 1~2개 정도의 적절한 역링크 추가
- `index.md`의 row 추가/수정
- `log.md`의 1회성 정리 엔트리 추가
- 존재하지 않는 asset 참조 제거

자동화가 피해야 하는 작업은 다음과 같습니다.
- 새 문서의 대규모 신설
- 근거 없는 내용 추가
- 대체 페이지가 불명확한 상태에서의 삭제
- 의미가 약한 역링크 남발
- 다른 주제까지 연쇄 수정하는 대규모 리라이트

## 5. 중단 조건
다음 중 하나라도 발생하면 해당 범주의 자동 수정을 멈춥니다.
- 대체 페이지 후보가 여러 개로 갈리는 경우
- 삭제 대상이 실제로 사용 중인지 불명확한 경우
- index/log의 숫자 불일치 원인을 파일만으로 바로 확인할 수 없는 경우
- asset을 복구할 근거가 부족한 경우

이 경우에는 보수적으로 정리하고, 나머지는 다음 점검 주기로 넘깁니다.

## 6. 점검 산출물
운영 작업 후에는 아래 항목이 남아야 합니다.
- 수정된 파일 목록
- 수정 이유 요약
- index count 변화
- log entry 1개
- 남은 수동 검토 항목

## 7. 관련 문서
- [[wiki-maintenance-checklist]]
- [[web-ctf-master-checklist]]
- web-ctf-llmwiki-workflow
- [[web-ctf-writeup-topic-map]]
- [[source-inspection-minification-ctf-patterns]]
