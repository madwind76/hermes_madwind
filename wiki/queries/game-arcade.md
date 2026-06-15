---
title: Game Arcade
created: 2026-06-13
updated: 2026-06-16
type: query
tags: [ctf, web, research]
sources: [https://ctftime.org/writeup/39221, https://gist.github.com/terjanq/27230afcee73ee75484ac14ac53e78bc, https://ctftime.org/task/28606]
confidence: medium
---

# Game Arcade

> 이 페이지는 **Google CTF 2024 Game Arcade 공개 writeup**을 바탕으로 정리한 학습용 진행 노트입니다.

## 1. 요약
- 플랫폼: Google CTF 2024
- 점수 / 난이도: 333 pts
- 문제 유형: client-side web / xss
- 핵심 개념: [[scf-sandbox-ctf-patterns]], [[web-ctf-master-checklist]], [[xss]]
- 현재 상태: 공개 writeup 기반으로 풀이 흐름 정리 완료

## 2. 공격면
| Route / Service | Method | Auth | Input | Output | Notes |
|------|------|------|------|------|------|
| game UI | GET | No | game data | popup render | 샌드박스 내부 렌더링 |
| password storage | JS | No | cookie / localStorage | DOM sink | innerHTML sink 존재 |
| shim URL | GET | No | hash + origin | sandbox origin | double-hash 검증 우회 |

## 3. 가설
- 실제 취약점은 게임 로직이 아니라 샌드박스 origin 검증입니다.
- 더블 해시 경로를 이용하면 공격자 페이지를 신뢰 origin처럼 보이게 할 수 있습니다.
- admin의 cookie / localStorage가 XSS sink로 이어집니다.

## 4. 실험 기록
### 시도 1
- payload: challenge source review
- 관찰: 게임과 shim 관계를 확인합니다.
- 해석: origin 계산 경로를 확보합니다.
### 시도 2
- payload: double-hash 검증
- 관찰: 허용되지 않은 origin이 통과되는지 봅니다.
- 해석: 임의 코드 실행 가능성을 찾습니다.
### 시도 3
- payload: data exfiltration
- 관찰: cookie 또는 localStorage를 외부로 전송합니다.
- 해석: flag가 저장된 저장소를 읽습니다.

## 5. 연결된 개념
- [[scf-sandbox-ctf-patterns]]
- [[web-ctf-master-checklist]]
- [[xss]]

## 6. 회고
- 막힌 지점: XSS 자체보다 origin 계산 버그가 먼저 풀려야 했습니다.
- 우회 포인트: double-hash shim과 cookie sink의 조합입니다.
- 다음에 먼저 볼 것: sandbox URL 생성과 브라우저별 차이입니다.
