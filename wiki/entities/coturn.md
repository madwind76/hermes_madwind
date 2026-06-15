---
title: Coturn
created: 2026-06-13
updated: 2026-06-16
type: entity
tags: [tool, coturn, turn, stun, webrtc]
sources: [https://github.com/coturn/coturn, https://github.com/coturn/coturn/wiki/turnserver, https://ctftime.org/task/13011]
confidence: high
---

# Coturn

## 정의
Coturn은 TURN/STUN 서버를 구현한 오픈소스 소프트웨어입니다. WebRTC에서 NAT 뒤의 피어를 중계하는 데 사용됩니다.

## Web CTF에서의 역할
- WebRTC 챌린지의 relay layer로 자주 등장합니다.
- 인증이 비어 있거나 기본 설정이면 내부 네트워크로 TCP proxy가 될 수 있습니다.
- Redis, HTTP, SSH 같은 내부 서비스로 접근하는 발판이 되기도 합니다.

## 관련 예시
- [[csaw-2020-webrtc]]
- [[webrtc-turn-proxying-ctf-patterns]]
