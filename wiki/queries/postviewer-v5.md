---
title: Postviewer v5
created: 2026-06-13
updated: 2026-06-16
type: query
tags: [ctf, web, research]
sources: [https://ctftime.org/writeup/40351, https://gist.github.com/terjanq/e66c2843b5b73aa48405b72f4751d5f8, https://ctftime.org/event/2718/tasks/]
confidence: medium
---

# Postviewer v5

> 이 페이지는 **Google CTF 2025 Postviewer v5 공개 writeup**을 바탕으로 정리한 학습용 진행 노트입니다.

## 1. 요약
- 플랫폼: Google CTF 2025
- 점수 / 난이도: 474 pts
- 문제 유형: client-side web
- 핵심 개념: [[scf-sandbox-ctf-patterns]], [[web-ctf-master-checklist]]
- 현재 상태: 공개 writeup 기반으로 풀이 흐름 정리 완료

## 2. 공격면
| Route / Service | Method | Auth | Input | Output | Notes |
|------|------|------|------|------|------|
| frontend | GET | No | file preview | rendered iframe | single frame 렌더링 |
| share endpoint | POST | No | shared content | IndexedDB entry | non-cached 파일 공유 |
| shim iframe | postMessage | No | salt / body / mime | reloadable blob | origin and hash 검증 |
| admin bot | browser visit | No | player URL | flag preview | 5분 제한 |

## 3. 가설
- sandbox 자체보다 salt 생성과 재사용 시점이 취약합니다.
- non-cached 경로에서 random salt가 새어 나올 수 있습니다.
- iframe 참조와 PRNG 예측을 결합하면 flag를 읽을 수 있습니다.

## 4. 실험 기록
### 시도 1
- payload: non-cached 파일 공유
- 관찰: salt 유출 여부를 확인합니다.
- 해석: PRNG 복원에 필요한 단서를 얻습니다.
### 시도 2
- payload: leaked salt 분석
- 관찰: base36 random sequence를 복구합니다.
- 해석: 미래 salt를 예측합니다.
### 시도 3
- payload: cached payload 주입
- 관찰: 예측된 origin에 XSS를 싣습니다.
- 해석: flag iframe 접근 경로를 확보합니다.

## 5. 연결된 개념
- [[scf-sandbox-ctf-patterns]]
- [[web-ctf-master-checklist]]


## 6. 회고
- 막힌 지점: iframe 격리보다 메시지 순서가 더 중요했습니다.
- 우회 포인트: salt 예측 + shared iframe reference + origin 재사용이 핵심입니다.
- 다음에 먼저 볼 것: postMessage 핸들러, hash 계산, cached/non-cached 분기입니다.
