---
title: urlapp
created: 2026-06-13
updated: 2026-06-16
type: query
tags: [ctf, web, research]
sources: [https://ctftime.org/task/10636, https://ctftime.org/writeup/18603, https://whitesnake1004.tistory.com/704, https://furutsuki.hatenablog.com/entry/2020/03/13/112204]
confidence: medium
---

# urlapp

> 이 페이지는 **zer0pts CTF 2020 urlapp 공개 writeup**을 바탕으로 정리한 학습용 진행 노트입니다.

## 1. 요약
- 플랫폼: zer0pts CTF 2020
- 점수 / 난이도: 426 pts
- 문제 유형: web / redis
- 핵심 개념: [[redis-ssrf-command-injection-ctf-patterns]], [[ssrf]], [[web-ctf-master-checklist]]
- 현재 상태: 공개 writeup 기반으로 풀이 흐름 정리 완료

## 2. 공격면
| Route / Service | Method | Auth | Input | Output | Notes |
|------|------|------|------|------|------|
| app.rb | Ruby | No | URL input | redis-backed response | 내부 Redis 연결 존재 |
| redis socket | TCP | internal | raw command | Redis reply | SSRF/command injection surface |
| result handling | HTTP | No | response text | output stream | 명령 결과가 노출 |

## 3. 가설
- 앱이 Redis로 직접 연결되므로 command surface가 작습니다.
- URL 또는 key 조작으로 Redis 명령을 우회 삽입할 수 있습니다.
- 명령 주입이 가능하면 replication이나 key manipulation으로 확장됩니다.

## 4. 실험 기록
### 시도 1
- payload: source inspection
- 관찰: Redis 소켓 연결 부분을 확인합니다.
- 해석: 입력이 raw command로 변환되는지 봅니다.
### 시도 2
- payload: Redis probing
- 관찰: 명령어와 key를 바꿔봅니다.
- 해석: BITOP / 문자열 조작 가능성을 봅니다.
### 시도 3
- payload: RCE chain
- 관찰: Redis 특수 기능으로 확장합니다.
- 해석: 결국 flag path를 읽는지 확인합니다.

## 5. 연결된 개념
- [[redis-ssrf-command-injection-ctf-patterns]]
- [[ssrf]]
- [[web-ctf-master-checklist]]

## 6. 회고
- 막힌 지점: 표면은 URL 처리지만 실제론 Redis 프로토콜이 핵심입니다.
- 우회 포인트: 내부 소켓 연결과 Redis 특수 명령 조합입니다.
- 다음에 먼저 볼 것: app.rb의 소켓 연결과 금지 명령 목록입니다.
