---
title: path traversal ctf template — 진행 노트
created: 2026-06-13
updated: 2026-06-13
type: query
tags: [ctf, web, path-traversal]
sources: []
confidence: medium
---

# Path Traversal CTF Template

## 1. 요약
- 플랫폼:
- 문제명:
- URL:
- 목표:
- 현재 상태:

## 2. 입력점
| Route | Method | Auth | Input | Output | Notes |
|------|------|------|------|------|------|
| | | | file / path / name / download | | 경로 조작 후보 |

## 3. 가설
- 가설 1: 상대 경로가 필터링되지 않는다.
- 가설 2: 인코딩 변형으로 필터를 우회할 수 있다.
- 가설 3: LFI 또는 파일 읽기로 이어질 수 있다.

## 4. 실험 기록
### 시도 1
- payload:
- 관찰:
- 해석:
- 다음 가설:

### 시도 2
- payload:
- 관찰:
- 해석:
- 다음 가설:

## 5. 연결된 개념
- [[path-traversal]]
- [[path-traversal-core]]
- [[path-traversal-defense]]
- [[lfi-rfi]]

## 6. 회고
- 막힌 지점:
- 우회 포인트:
- 다음에 먼저 볼 것:
- 재사용 체크리스트:
  - [ ] ../ 계열 차단 확인
  - [ ] 인코딩 우회 확인
  - [ ] 파일 읽기 전환 여부 확인
