---
title: gcalc — web ctf note
created: 2026-06-13
updated: 2026-06-13
type: query
tags: [ctf, web, research]
sources: [https://blog.orange.tw/2018/06/google-ctf-2018-quals-web-gcalc.html, https://orange-tw.blogspot.com/2018/06/?m=1, https://github.com/eskildsen/google-ctf-2018, https://github.com/EmpireCTF/empirectf/blob/master/writeups/2018-06-23-Google-CTF-Quals/README.md]
confidence: medium
---

# gCalc

> 이 페이지는 **Google CTF 2018 Quals gCalc 공개 writeup**을 바탕으로 정리한 학습용 진행 노트입니다.

## 1. 요약
- 플랫폼: Google CTF 2018 Quals
- 점수 / 난이도: 326 pts
- 문제 유형: web / xss
- 핵심 개념: [[web-inspector-ctf-patterns]], [[xss]], [[web-ctf-master-checklist]]
- 현재 상태: 공개 writeup 기반으로 풀이 흐름 정리 완료

## 2. 공격면
| Route / Service | Method | Auth | Input | Output | Notes |
|------|------|------|------|------|------|
| calculator | GET | No | expr / vars | evaluated output | new Function 사용 |
| vars JSON | parse | No | custom keys | Object.create(null) | 공격자 키 삽입 가능 |
| CSP | header | No | img-src / child-src | limited exfil | Google Analytics가 열려 있음 |

## 3. 가설
- 표면상 계산기지만 실제로는 JS 실행이 가능할 것입니다.
- toLowerCase 필터를 우회할 다른 함수 호출 경로가 있습니다.
- CSP는 완전하지 않으며 이미지 채널로 유출이 가능합니다.

## 4. 실험 기록
### 시도 1
- payload: expr review
- 관찰: Function constructor 경로를 봅니다.
- 해석: 임의 JS 실행 가능성을 확인합니다.
### 시도 2
- payload: vars key abuse
- 관찰: vars 객체의 마지막 키를 꺼냅니다.
- 해석: alert 같은 코드 조각을 실행합니다.
### 시도 3
- payload: GA exfiltration
- 관찰: img 태그로 cookie를 보냅니다.
- 해석: CSP 허용 채널로 유출합니다.

## 5. 연결된 개념
- [[web-inspector-ctf-patterns]]
- [[xss]]
- [[web-ctf-master-checklist]]

## 6. 회고
- 막힌 지점: 수학 계산기가 아니라 JS expression interpreter였습니다.
- 우회 포인트: vars key 조작과 허용된 이미지 채널입니다.
- 다음에 먼저 볼 것: sanitize 규칙과 CSP의 허용 도메인입니다.
