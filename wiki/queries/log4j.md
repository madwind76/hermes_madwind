---
title: log4j — web ctf note
created: 2026-06-13
updated: 2026-06-13
type: query
tags: [ctf, web, research]
sources: [https://ctftime.org/writeup/34548, https://www.sigflag.at/blog/2022/writeup-googlectf2022-log4j/, https://intrigus.org/research/2022/07/18/google-ctf-2022-log4j2-writeup/]
confidence: medium
---

# Log4J

> 이 페이지는 **Google CTF 2022 Log4J 공개 writeup**을 바탕으로 정리한 학습용 진행 노트입니다.

## 1. 요약
- 플랫폼: Google CTF 2022
- 점수 / 난이도: web challenge
- 문제 유형: web / java
- 핵심 개념: [[rce]], [[web-ctf-master-checklist]]
- 현재 상태: 공개 writeup 기반으로 풀이 흐름 정리 완료

## 2. 공격면
| Route / Service | Method | Auth | Input | Output | Notes |
|------|------|------|------|------|------|
| Flask front-end | POST | No | chat input | stdout / stderr | 입력이 Java 앱으로 전달 |
| Java logger | runtime | No | args / env | log output | FLAG가 환경변수에 있음 |
| lookup engine | log4j | No | lookup string | resolved value | JavaLookup / env lookup |

## 3. 가설
- 클래식 JNDI 대신 lookup / exception 메시지가 핵심입니다.
- stderr로 돌아오는 오류에 환경변수 값이 섞일 수 있습니다.
- JavaLookup의 인자 검증 실패를 이용하면 flag가 노출됩니다.

## 4. 실험 기록
### 시도 1
- payload: logger input review
- 관찰: 사용자 입력이 logger.info 경로로 들어가는지 확인합니다.
- 해석: 오류 출력에 집중합니다.
### 시도 2
- payload: lookup payload
- 관찰: env lookup과 JavaLookup을 결합합니다.
- 해석: flag가 문자열로 풀리는지 봅니다.
### 시도 3
- payload: stderr capture
- 관찰: 에러 메시지를 그대로 읽습니다.
- 해석: 환경변수 노출 여부를 확인합니다.

## 5. 연결된 개념
- [[rce]]
- [[web-ctf-master-checklist]]


## 6. 회고
- 막힌 지점: JNDI가 아니라 다른 lookup 경로가 핵심이었습니다.
- 우회 포인트: exception 메시지에 resolved value가 남는 점입니다.
- 다음에 먼저 볼 것: logger 설정, lookup 지원 범위, stderr 반환입니다.
