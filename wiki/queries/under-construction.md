---
title: under-construction — web ctf note
created: 2026-06-13
updated: 2026-06-13
type: query
tags: [ctf, web, research]
sources: [https://blog.shameerkashif.me/blog/2023/writeup-under-construction-google-ctf-2023/, https://ctftime.org/writeup/37351, https://ctftime.org/writeup/37549, https://ctftime.org/writeup/37330]
confidence: medium
---

# Under Construction

> 이 페이지는 **Google CTF 2023 Under Construction 공개 writeup**을 바탕으로 정리한 학습용 진행 노트입니다.

## 1. 요약
- 플랫폼: Google CTF 2023
- 점수 / 난이도: web
- 문제 유형: web / parameter pollution
- 핵심 개념: [[parameter-tampering-ctf-patterns]], [[web-ctf-master-checklist]]
- 현재 상태: 공개 writeup 기반으로 풀이 흐름 정리 완료

## 2. 공격면
| Route / Service | Method | Auth | Input | Output | Notes |
|------|------|------|------|------|------|
| Flask signup | POST | No | tier parameter | validated user data | 첫 번째 tier만 검사 |
| PHP account migrator | POST | No | raw request | PHP-side parsed data | 다른 파서가 두 번째 값을 봄 |
| login page | POST | No | credentials | flag response | gold tier면 FLAG 노출 |

## 3. 가설
- 검증 계층과 저장 계층이 서로 다른 파라미터 해석기를 씁니다.
- 같은 이름의 tier를 두 번 보내면 서로 다른 값이 보일 수 있습니다.
- gold tier만 허용되는 분기에서 우회가 가능할 것입니다.

## 4. 실험 기록
### 시도 1
- payload: signup validation
- 관찰: tier를 두 번 전송합니다.
- 해석: 첫 값과 둘째 값이 다르게 보이는지 봅니다.
### 시도 2
- payload: raw request forwarding
- 관찰: Flask가 PHP에 그대로 전달하는지 확인합니다.
- 해석: migrator가 다른 값을 보도록 만듭니다.
### 시도 3
- payload: gold login
- 관찰: gold 계정으로 로그인합니다.
- 해석: FLAG가 응답에 붙는지 확인합니다.

## 5. 연결된 개념
- [[parameter-tampering-ctf-patterns]]
- [[web-ctf-master-checklist]]


## 6. 회고
- 막힌 지점: 파라미터 하나를 보는지 둘을 보는지 계층마다 달랐습니다.
- 우회 포인트: parameter pollution과 raw request forwarding입니다.
- 다음에 먼저 볼 것: 다중 파라미터와 프레임워크별 파싱 차이입니다.
