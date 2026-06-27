---
title: CSAW Quals 2020 WebRTC
created: 2026-06-13
updated: 2026-06-21
type: query
tags: [ctf, web, webrtc, turn, redis, proxy]
sources: [https://ctftime.org/task/13011, https://ctftime.org/writeup/23439, https://ctftime.org/writeup/23438, https://ctftime.org/writeup/23407, https://ctftime.org/writeup/23410, https://github.com/team0se7en/CTF-Writeups/blob/master/CsawQuals20/WebRTC/README.md, https://github.com/zoeyg/public-write-ups/blob/master/csaw-2020/web-real-time-chat.md]
confidence: medium
---

# CSAW Quals 2020 WebRTC

> 이 페이지는 **CSAW Quals 2020 WebRTC 공개 writeup**을 바탕으로 정리한 학습용 진행 노트입니다.

## 참고 URL
- [CTFtime writeup](https://ctftime.org/task/13011)
- [CTFtime writeup](https://ctftime.org/writeup/23439)
- [CTFtime writeup](https://ctftime.org/writeup/23438)
- [CTFtime writeup](https://ctftime.org/writeup/23407)
- [CTFtime writeup](https://ctftime.org/writeup/23410)
- [Original writeup](https://github.com/team0se7en/CTF-Writeups/blob/master/CsawQuals20/WebRTC/README.md)
- [Original writeup](https://github.com/zoeyg/public-write-ups/blob/master/csaw-2020/web-real-time-chat.md)


## 1. 요약
- 플랫폼: CSAW CTF Qualification Round 2020
- 난이도: 450 pts
- 문제 유형: Web
- 핵심 개념: [[webrtc-turn-proxying-ctf-patterns]], [[coturn]], [[web-ctf-master-checklist]]
- 현재 상태: 공개 writeup 기반으로 풀이 흐름 정리 완료

## 2. 공격면
| Route / Service | Method | Auth | Input | Output | Notes |
|------|------|------|------|------|------|
| `/` | GET | No | session link / RTC UI | chat page | WebRTC signaling frontend |
| `/rtc.js` | GET | No | TURN configuration | ICE server config | `username` / `credential` 비어 있음 |
| `/app.py` API | GET/POST | No/Yes | session state, logging | JSON / chat data | 일부 writeup에서 red herring으로 평가 |
| `TURN :3478` | UDP/TCP | No | STUN/TURN messages | relay allocation | 내부 네트워크 TCP proxy로 악용 |
| `Redis :6379` | internal | No | raw Redis commands | internal state | 최종 공격 대상 |

## 3. 가설
- 가설 1: Flask 앱 자체보다 TURN relay 설정이 핵심입니다.
- 가설 2: 인증 없는 TURN 서버를 통해 내부 Redis로 TCP를 전달할 수 있습니다.
- 가설 3: Redis replication / module loading 체인으로 flag를 읽을 수 있습니다.

## 4. 실험 기록
### 시도 1
- payload: `turn:web.chal.csaw.io:3478` 설정 확인
- 관찰: `username`과 `credential`이 비어 있습니다.
- 해석: 인증 없는 TURN relay 가능성이 큽니다.
- 다음 가설: 프록시 도구로 relay 동작을 검증합니다.

### 시도 2
- payload: `turner -server web.chal.csaw.io:3478 -u '' -p ''`
- 관찰: HTTP 프록시처럼 relay가 열리고 외부 목적지 접근이 가능합니다.
- 해석: TURN server가 내부 네트워크로 가는 TCP proxy 역할을 할 수 있습니다.
- 다음 가설: Redis에 raw command를 전달합니다.

### 시도 3
- payload: 프록시 경유 `INFO\r\n`
- 관찰: Redis 응답이 반환됩니다.
- 해석: 내부 Redis에 직접 연결된 상태입니다.
- 다음 가설: replication 또는 rogue server 체인을 적용합니다.

### 시도 4
- payload: `SLAVEOF` / rogue server / `MODULE LOAD`
- 관찰: flag 파일 읽기 또는 shell 실행으로 이어집니다.
- 해석: Redis replication + module loading 체인이 최종 익스플로잇입니다.

## 5. 연결된 개념
- [[webrtc-turn-proxying-ctf-patterns]]
- [[coturn]]
- [[web-ctf-master-checklist]]

## 6. 회고
- 막힌 지점: 앱 로직보다 네트워크 릴레이 계층을 먼저 봐야 합니다.
- 우회 포인트: TURN proxying → 내부 Redis → replication/module chain
- 다음에 먼저 볼 것: `Dockerfile`, `supervisord.conf`, `rtc.js`, 내부 서비스 바인딩
- 재사용 체크리스트:
  - [ ] TURN 서버 인증이 비어 있는가
  - [ ] 내부 서비스로 TCP relay가 가능한가
  - [ ] Redis / SSH / HTTP 등 내부 서비스가 노출되는가
  - [ ] replication 또는 module loading이 가능한가
  - [ ] 초기 프론트엔드가 red herring인지 확인했는가
