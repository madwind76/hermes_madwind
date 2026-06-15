---
title: csaw-2020-webrtc — final writeup sample
created: 2026-06-13
updated: 2026-06-13
type: query
tags: [ctf, web, webrtc, turn, redis, proxy]
sources: [https://ctftime.org/task/13011, https://ctftime.org/writeup/23439, https://ctftime.org/writeup/23438, https://ctftime.org/writeup/23407, https://ctftime.org/writeup/23410, https://github.com/team0se7en/CTF-Writeups/blob/master/CsawQuals20/WebRTC/README.md, https://github.com/zoeyg/public-write-ups/blob/master/csaw-2020/web-real-time-chat.md]
confidence: medium
---

# CSAW Quals 2020 WebRTC — Final Writeup Sample

> 이 문서는 **공개 writeup을 바탕으로 재구성한 최종 요약 예시**입니다.

## 1. 문제 요약
- 플랫폼: CSAW CTF Qualification Round 2020
- 난이도: 450 pts
- 핵심 취약점: 인증 없는 TURN relay를 통한 내부 Redis 접근
- 관련 개념: [[webrtc-turn-proxying-ctf-patterns]], [[coturn]], [[web-ctf-master-checklist]]

## 2. 풀이 흐름
1. `Dockerfile`과 `supervisord.conf`에서 `gunicorn`, `coturn`, `redis`가 함께 실행됨을 확인합니다.
2. `rtc.js`에서 TURN 서버 주소와 빈 credentials를 확인합니다.
3. `turner` 같은 도구로 TURN relay가 실제로 동작하는지 검증합니다.
4. TURN proxy를 통해 내부 Redis에 raw command를 전달합니다.
5. Redis replication 또는 rogue master 체인으로 파일 읽기 또는 RCE를 획득합니다.
6. `/flag.txt`를 읽어 flag를 확인합니다.

## 3. 핵심 관찰
| 단계 | 관찰 | 해석 |
|------|------|------|
| 파일 분석 | Redis가 내부용인데 `--bind 0.0.0.0` | 네트워크 경계가 약함 |
| `rtc.js` | TURN credentials 비어 있음 | relay 인증 우회 가능성 |
| TURN proxy | 내부 주소로 TCP 전달 가능 | 내부 Redis 접근 가능 |
| Redis 조작 | `INFO`, `SLAVEOF`, `MODULE LOAD`가 가능 | 최종 권한 상승/파일 읽기 경로 |

## 4. 방어 관점
- TURN 서버는 반드시 인증과 접근 제어를 적용해야 합니다.
- Redis는 외부에 바인딩하지 말고 비밀번호와 ACL을 설정해야 합니다.
- 내부 서비스라도 같은 컨테이너/호스트 네트워크에 있다고 가정하면 안 됩니다.
- 웹 프론트엔드의 RTC 기능은 본 취약점의 본질이 아닐 수 있습니다.

## 5. 회고
- 이 문제는 WebRTC 자체보다 **TURN relay misconfiguration**이 핵심입니다.
- 다음에 재사용할 체크리스트:
  - [ ] TURN/STUN 서버의 인증 여부를 확인했는가
  - [ ] 내부 서비스로의 TCP relay 가능성을 점검했는가
  - [ ] Redis 같은 내부 서비스가 `0.0.0.0`에 바인딩되어 있지 않은가
  - [ ] replication / module loading 기능을 악용할 수 있는가

## 6. 연결된 개념
- [[webrtc-turn-proxying-ctf-patterns]]
- [[coturn]]
- [[web-ctf-master-checklist]]
