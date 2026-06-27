---
title: Web CTF Writeup — 내부 서비스/프로토콜 악용
created: 2026-06-14
updated: 2026-06-21
type: query
tags: [ctf, web, research, writeup, ssrf, protocol, internal-service]
sources: [https://blog.hokyun.dev/posts/csaw-ctf-2024-quals-writeup/, https://github.com/hyperreality/best-web-ctf-writeups, raw/articles/20260613_web-ctf-writeup-curated.md]
confidence: high
---

# Web CTF Writeup — 내부 서비스/프로토콜 악용

> 서버가 외부 입력으로 내부 요청을 대신 보내는 구조를 다루는 분류입니다.

## 참고 URL
- [blog.hokyun.dev](https://blog.hokyun.dev/posts/csaw-ctf-2024-quals-writeup/)
- [hyperreality/best-web-ctf-writeups](https://github.com/hyperreality/best-web-ctf-writeups)
- [raw/articles/20260613_web-ctf-writeup-curated.md](raw/articles/20260613_web-ctf-writeup-curated.md)


## 1. 핵심 요약
- 이 분류는 **서버가 대신 말해주는 요청**을 만드는 문제입니다.
- SSRF, Redis, gopher, NFS/RPC, 내부 admin bot, 로컬 백엔드 접근이 자주 등장합니다.
- `ssrf`, `redis-ssrf-command-injection-ctf-patterns`, `webrtc-turn-proxying-ctf-patterns`와 연결됩니다.

연결 개념: [[ssrf]], [[redis-ssrf-command-injection-ctf-patterns]], [[webrtc-turn-proxying-ctf-patterns]], [[heap-dump-ctf-patterns]], [[signed-html-email-ctf-patterns]]

## 2. 대표 writeup

| 문제 | 출처 | 핵심 아이디어 |
|------|------|---------------|
| `charlies angels` | CSAW CTF 2024 Quals | 내부 백업 서버와 저장 파이프라인 연결 |
| `urlapp` | zer0pts 2020 | Ruby 앱과 내부 Redis 통신 구조 악용 |
| `Web Real time Chat` | best-web-ctf-writeups | TURN/TCP 프록싱과 내부 네트워크 경계 악용 |
| `BitHug` | picoCTF 2021 | Git 호스팅 서비스의 webhook / access.conf / internal admin 경로 악용 |
| [[head-dump-final-writeup]] | picoCTF 2025 | Swagger UI에서 `/heapdump` 진단 엔드포인트 발견 후 heap snapshot 검색 |
| [[secure-email-service-final-writeup]] | picoCTF 2025 | admin bot이 여는 signed HTML email sink에서 `localStorage` flag 탈취 |

## 3. 자주 보이는 패턴
1. 사용자 입력이 URL/fetch/socket destination이 됨
2. 내부 호스트가 allowlist에 없는데도 우회 가능함
3. 프로토콜 단위로는 막혀도 다른 scheme으로 열림
4. 관리자 봇이 내부 URL을 방문해줌
5. 서비스 간 trust boundary가 명확히 분리되어 있지 않음
6. `/api-docs`나 Swagger UI가 진단 엔드포인트를 노출함

## 4. 읽을 때 확인할 것
- 외부에서 직접 못 보는 내부 포트가 있는지
- redirect, DNS, IP literal, gopher 같은 우회가 가능한지
- 내부 요청의 응답을 관찰할 수 있는지
- admin bot 또는 backend가 동일 origin에서 실행되는지

## 5. 방어 관점
- 서버측 fetch는 scheme/host/IP allowlist를 엄격히 적용합니다.
- 내부망 요청은 egress 정책으로 차단합니다.
- 관리자 봇과 일반 사용자 요청을 분리합니다.
- 프로토콜 변환기와 프록시는 별도 검증을 둡니다.

## 6. 추천 다음 읽기
- [[ssrf]]
- [[redis-ssrf-command-injection-ctf-patterns]]
- [[webrtc-turn-proxying-ctf-patterns]]
- [[heap-dump-ctf-patterns]]
- [[web-ctf-master-checklist]]
