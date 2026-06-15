---
title: Wiki Maintenance Checklist
created: 2026-06-14
updated: 2026-06-14
type: concept
tags: [wiki, maintenance, checklist, workflow]
sources: [/home/kisec/wiki/concepts/web-ctf-writeup-topic-map.md, /home/kisec/wiki/queries/web-ctf-master-checklist.md, /home/kisec/wiki/index.md, /home/kisec/wiki/log.md]
confidence: high
---

# Wiki Maintenance Checklist

> **목적**: wiki link 작업과 데이터 정리를 매일 같은 기준으로 점검하기 위한 실행 체크리스트입니다.
> **적용 범위**: `concepts/`, `queries/`, `entities/`, `comparisons/`, `index.md`, `log.md`, 연관 asset 파일

## 1. 점검 순서

1. **Broken wikilinks**부터 확인합니다.
2. **Reciprocal links**를 보강합니다.
3. **Orphan pages**를 찾고 필요한 경우 연결을 추가합니다.
4. **Duplicate / near-duplicate** 페이지를 정리합니다.
5. **index.md**와 **log.md**를 동기화합니다.
6. **asset reference**를 확인합니다.
7. 마지막으로 전체 파일을 다시 읽어 **검증**합니다.

## 2. 실제 점검 체크리스트

### 2.1 Broken wikilinks
- [ ] `[[wikilink]]` 대상 페이지가 실제로 존재하는가
- [ ] 존재하지 않는 링크는 대체 페이지로 교체했는가
- [ ] 대체 대상이 없으면 일반 텍스트로 바꿨는가
- [ ] 자기참조 링크는 남기지 않았는가
- [ ] 외부 URL을 `[[...]]`로 잘못 감싸지 않았는가

### 2.2 Reciprocal links
- [ ] hub page에서 하위 페이지로 링크했는가
- [ ] 하위 페이지에서 hub page로 역링크가 있는가
- [ ] 중복되거나 불필요한 역링크는 없는가
- [ ] 관련 페이지끼리만 연결했는가

### 2.3 Orphan pages
- [ ] inbound link가 없는 페이지를 확인했는가
- [ ] 재사용 가치가 있는 orphan에는 1~2개 연결을 추가했는가
- [ ] 중복 페이지면 링크를 유지 페이지로 옮겼는가
- [ ] 불필요한 고아 페이지는 정리 대상으로 표시했는가

### 2.4 Duplicate / near-duplicate
- [ ] 제목이 비슷한 페이지를 비교했는가
- [ ] 태그와 첫 섹션 요약을 함께 비교했는가
- [ ] 더 좋은 제목과 링크 구조를 가진 페이지를 유지했는가
- [ ] 중복 페이지의 유일한 내용은 보존 페이지로 이동했는가

### 2.5 Index consistency
- [ ] `index.md`에 페이지가 정확히 1회만 등록되어 있는가
- [ ] 페이지 추가/삭제 후 카운트를 갱신했는가
- [ ] `마지막 업데이트` 날짜를 갱신했는가
- [ ] 섹션 이동 시 해당 행만 수정했는가
- [ ] 수정 후 index 라인을 다시 읽어 확인했는가

### 2.6 Log consistency
- [ ] 실제 변경이 있을 때만 `log.md`를 추가/갱신했는가
- [ ] 변경 요약이 한눈에 보이게 적혀 있는가
- [ ] 중복 로그가 생기지 않았는가
- [ ] `index.md`와 `log.md`의 내용이 서로 어긋나지 않는가

### 2.7 Asset references
- [ ] 참조하는 SVG/HTML/image 파일이 존재하는가
- [ ] 필요한데 누락된 asset은 재생성했는가
- [ ] 굳이 필요 없는 asset 링크는 제거했는가
- [ ] 본문 설명과 asset 내용이 서로 맞는가

## 3. 검증 명령 예시

```bash
# wiki 전체에서 깨진 링크 후보를 빠르게 훑습니다.
# 예상 출력: 링크 문자열 목록 또는 매칭 라인
search_files --pattern '\[\[[^]]+\]\]' --path /home/kisec/wiki  # 실제 환경에서는 search_files 도구 사용을 권장합니다.

# index.md의 페이지 수와 마지막 업데이트를 확인합니다.
# 예상 출력: "마지막 업데이트" / "전체 페이지" 라인
grep -n '마지막 업데이트\|전체 페이지' /home/kisec/wiki/index.md  # index 동기화 상태를 확인합니다.

# log.md에 오늘자 정리 기록이 있는지 확인합니다.
# 예상 출력: 오늘 날짜의 maintenance entry
grep -n 'wiki cleanup\|maintenance' /home/kisec/wiki/log.md  # 실제 작업 기록을 확인합니다.
```

## 4. 판단 기준

### 유지 기준
- 다른 페이지가 이미 참조하고 있는가
- 같은 개념을 더 명확하게 설명하는가
- 재사용 가치가 있는가
- 허브 페이지와의 연결이 자연스러운가

### 병합 기준
- 제목만 다르고 내용이 거의 같은가
- 링크 대상이 완전히 겹치는가
- 한쪽이 명백히 더 잘 정리되어 있는가

### 제거 기준
- 실질적 가치가 없고 중복만 남는가
- 대체 페이지가 이미 충분히 존재하는가
- 링크를 수정한 뒤에도 고립된가

## 5. 작업 후 확인
- [ ] 수정한 파일을 다시 읽었는가
- [ ] 링크 타깃이 실제로 존재하는가
- [ ] index.md 반영이 맞는가
- [ ] log.md에 실제 변경만 기록되었는가
- [ ] 새 asset 링크가 깨지지 않았는가
- [ ] 변경이 없었다면 "정리할 내용 없음"만 출력하는가

## 6. 관련 문서
- web-ctf-llmwiki-workflow
- [[web-ctf-master-checklist]]
- [[wiki-maintenance-operations]]
- [[web-ctf-writeup-topic-map]]
- [[web-inspector-ctf-patterns]]
- [[source-inspection-minification-ctf-patterns]]
