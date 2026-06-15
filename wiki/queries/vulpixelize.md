---
title: vulpixelize — web ctf note
created: 2026-06-13
updated: 2026-06-13
type: query
tags: [ctf, web, research]
sources: [https://blog.nella17.tw/p/hitcon-ctf-2021-writeups/, https://ctftime.org/task/18312, https://ctftime.org/writeup/31677, https://github.com/orangetw/My-CTF-Web-Challenges]
confidence: medium
---

# Vulpixelize

> 이 페이지는 **HITCON CTF 2021 Vulpixelize 공개 writeup**을 바탕으로 정리한 학습용 진행 노트입니다.

## 1. 요약
- 플랫폼: HITCON CTF 2021
- 점수 / 난이도: 232 pts
- 문제 유형: web / browser feature
- 핵심 개념: [[dns-rebinding-ctf-patterns]], [[web-ctf-master-checklist]]
- 현재 상태: 공개 writeup 기반으로 풀이 흐름 정리 완료

## 2. 공격면
| Route / Service | Method | Auth | Input | Output | Notes |
|------|------|------|------|------|------|
| snapshot URL | GET | No | arbitrary URL | 64x64 screenshot | 이미지 캡처 서비스 |
| localhost flag | GET | internal | /flag | rendered text | 내부 서비스 타깃 |
| browser features | JS / iframe | No | text fragments / CSS | visual leakage | unintended solve path |

## 3. 가설
- 작은 스냅샷이라도 텍스트 조각을 조합할 수 있습니다.
- 또는 DNS rebinding으로 localhost를 같은 출처처럼 다룰 수 있습니다.
- Host 검증이 약하면 내부 `/flag` 접근이 가능합니다.

## 4. 실험 기록
### 시도 1
- payload: screenshot review
- 관찰: 출력 크기와 흐림 정도를 봅니다.
- 해석: 텍스트를 분리할 전략을 세웁니다.
### 시도 2
- payload: text fragment payload
- 관찰: 브라우저 feature를 시험합니다.
- 해석: flag 조각이 보이는지 확인합니다.
### 시도 3
- payload: DNS rebinding
- 관찰: 0.0.0.0 / localhost 접근을 교체합니다.
- 해석: 내부 flag 엔드포인트를 읽습니다.

## 5. 연결된 개념
- [[dns-rebinding-ctf-patterns]]
- [[web-ctf-master-checklist]]


## 6. 회고
- 막힌 지점: 화면 캡처가 작아도 브라우저 기능이 우회 포인트가 됩니다.
- 우회 포인트: DNS rebinding과 text fragment 둘 다 가능성을 열어둡니다.
- 다음에 먼저 볼 것: Host 검증과 내부 서비스가 직접 바인딩되는지 여부입니다.
