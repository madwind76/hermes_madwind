---
title: Race condition writeup survey
created: 2026-06-19
updated: 2026-06-21
type: query
tags: [ctf, web, survey, writeup, race-condition, burp, timing]
sources: [https://medium.com/@divyanshurds.kumar/writeup-picoctf-2025-pachinko-2dcb85b3202f, https://beerpwn.github.io/ctf/2020/darkCTF/web/Chain%20Race/]
confidence: high
---

# Race condition writeup survey

## 참고 URL
- [medium.com](https://medium.com/@divyanshurds.kumar/writeup-picoctf-2025-pachinko-2dcb85b3202f)
- [beerpwn.github.io](https://beerpwn.github.io/ctf/2020/darkCTF/web/Chain%20Race/)


## 1. 목적
동시 요청을 이용한 race condition 공격 패턴과 Burp Suite 활용법을 정리합니다.

## 2. 비교 대상
| 문제 | 주된 primitive | 보조 primitive | 한 줄 요약 |
|---|---|---|---|
| Pachinko | fuzzing + race condition | parameter tampering | NAND simulator 요청을 Burp Intruder로 fuzzing하고 race window를 공략합니다. |
| Chain Race (DarkCTF 2020) | SSRF → race condition | internal service | SSRF로 내부 서비스를 연결하고 race window를 이용해 검증을 우회합니다. |

## 3. 공통 관찰
1. race condition은 요청 순서/타이밍에 의존하는 로직을 동시 요청으로 깨는 방식입니다.
2. Burp Turbo Intruder가 race payload 전송에 가장 널리 쓰입니다.
3. race window는 밀리초 단위이므로 단일 패킷 병렬 전송이 중요합니다.

## 4. 관련 개념
- [[race-condition-ctf-patterns]]
- [[parameter-tampering-ctf-patterns]]
- [[web-ctf-writeup-family-hub]]
- [[pachinko-final-writeup]]

## 5. 다음 읽을 거리
- [[pachinko-final-writeup]]
