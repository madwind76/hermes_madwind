---
title: Sourceless
created: 2026-06-13
updated: 2026-06-16
type: query
tags: [ctf, web, research]
sources: [https://gist.github.com/terjanq/4cb40653760c1ba8c33ee06be098d508, https://ctftime.org/event/2718/tasks/, https://ctftime.org/team/23929/]
confidence: medium
---

# Sourceless

> 이 페이지는 **Google CTF 2025 Sourceless 공개 writeup**을 바탕으로 정리한 학습용 진행 노트입니다.

## 1. 요약
- 플랫폼: Google CTF 2025
- 점수 / 난이도: 298 pts
- 문제 유형: client-side web
- 핵심 개념: [[xssi-file-exfiltration-ctf-patterns]], [[web-ctf-master-checklist]], [[web-inspector-ctf-patterns]]
- 현재 상태: 공개 writeup 기반으로 풀이 흐름 정리 완료

## 2. 공격면
| Route / Service | Method | Auth | Input | Output | Notes |
|------|------|------|------|------|------|
| bot | visit | No | arbitrary URL | navigation | simple puppeteer bot |
| file:// | GET | No | local file | script / error | file scheme 접근이 핵심 |
| IndexedDB | browser storage | No | blob payload | persistent file | 페이로드 보관 |

## 3. 가설
- 문제는 원격 URL이 아니라 file:// 처리와 브라우저 에러 메시지입니다.
- Error prototype / charset 조합으로 flag를 복원할 수 있습니다.
- Firefox용 Puppeteer 설정이 보안 경계를 약화시켰을 수 있습니다.

## 4. 실험 기록
### 시도 1
- payload: error interception
- 관찰: 에러 메시지에서 flag 조각을 추출합니다.
- 해석: 문자열 복호화 루틴을 맞춥니다.
### 시도 2
- payload: IndexedDB persistence
- 관찰: 페이로드를 file:// 경로로 저장합니다.
- 해석: 봇이 접근할 고정 경로를 만듭니다.
### 시도 3
- payload: file:// navigation
- 관찰: 저장된 HTML을 실행합니다.
- 해석: flag.txt 포함 경로를 트리거합니다.

## 5. 연결된 개념
- [[xssi-file-exfiltration-ctf-patterns]]
- [[web-ctf-master-checklist]]
- [[web-inspector-ctf-patterns]]

## 6. 회고
- 막힌 지점: 원격 HTTP가 아니라 로컬 file scheme이 진입점이었습니다.
- 우회 포인트: XSSI + 에러 인터셉션 + 저장소 영속성 조합입니다.
- 다음에 먼저 볼 것: Puppeteer 브라우저 종류와 file-origin 정책입니다.
