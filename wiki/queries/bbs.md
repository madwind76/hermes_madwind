---
title: BBS
created: 2026-06-13
updated: 2026-06-16
type: query
tags: [ctf, web, research]
sources: [https://kt.gy/blog/2018/06/googlectf-2018-quals-web-bbs/, https://ctftime.org/writeup/10369, https://ctftime.org/writeup/10366]
confidence: medium
---

# BBS

> 이 페이지는 **Google CTF 2018 Quals BBS 공개 writeup**을 바탕으로 정리한 학습용 진행 노트입니다.

## 1. 요약
- 플랫폼: Google CTF 2018 Quals
- 점수 / 난이도: 453 pts
- 문제 유형: web
- 핵심 개념: [[web-inspector-ctf-patterns]], [[parameter-tampering-ctf-patterns]], [[xss]]
- 현재 상태: 공개 writeup 기반으로 풀이 흐름 정리 완료

## 2. 공격면
| Route / Service | Method | Auth | Input | Output | Notes |
|------|------|------|------|------|------|
| register/login | GET/POST | No | credentials | session | 게시판 계정 흐름 |
| avatar upload | POST | Yes | PNG image | resized avatar | 정상 PNG로만 처리 |
| post iframe | GET | No | p query | decoded post | qs + jQuery ajax 조합 |
| report | POST | No | post path | admin report | path validation bypass |

## 3. 가설
- 시각적으로 보이는 게시판보다 소스와 iframe 렌더링이 중요합니다.
- avatar를 잘라 가져오면 HTML 인젝션이 가능합니다.
- report 엔드포인트는 path normalization에 취약합니다.

## 4. 실험 기록
### 시도 1
- payload: HTML source review
- 관찰: iframe의 ajax settings를 봅니다.
- 해석: p query가 settings object로 해석되는지 확인합니다.
### 시도 2
- payload: Range fetch
- 관찰: avatar의 일부 바이트만 읽습니다.
- 해석: base64 decode 후 XSS가 생기는지 봅니다.
### 시도 3
- payload: report bypass
- 관찰: admin 경로를 path traversal로 우회합니다.
- 해석: 봇에게 crafted post를 제출합니다.

## 5. 연결된 개념
- [[web-inspector-ctf-patterns]]
- [[parameter-tampering-ctf-patterns]]
- [[xss]]

## 6. 회고
- 막힌 지점: PNG 자체보다 Range 기반 재조합이 핵심이었습니다.
- 우회 포인트: qs object construction과 report path bypass입니다.
- 다음에 먼저 볼 것: client-side Ajax 옵션과 서버 측 경로 정규화입니다.
