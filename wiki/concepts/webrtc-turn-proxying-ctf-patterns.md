---
title: WebRTC TURN Proxying
created: 2026-06-13
updated: 2026-06-16
type: concept
tags: [ctf, web, webrtc, turn, proxy, redis]
sources: [https://ctftime.org/task/13011, https://ctftime.org/writeup/23439, https://ctftime.org/writeup/23438, https://ctftime.org/writeup/23407, https://ctftime.org/writeup/23410, https://github.com/coturn/coturn, https://github.com/team0se7en/CTF-Writeups/blob/master/CsawQuals20/WebRTC/README.md, https://github.com/zoeyg/public-write-ups/blob/master/csaw-2020/web-real-time-chat.md]
confidence: medium
---

# WebRTC TURN Proxying

## 정의
TURN(Traversal Using Relays around NAT)은 NAT 뒤의 피어 간 통신을 중계하는 프로토콜입니다. CTF에서는 이 relay가 내부 서비스로의 TCP proxy로 오용되는 경우가 많습니다.

## 왜 중요한가
웹 UI는 정상적으로 보여도, 실질적인 취약점은 WebRTC signaling이 아니라 **TURN 서버 설정**에 있을 수 있습니다.

## 관찰 포인트
- `rtc.js`의 `iceServers` 설정
- 빈 `username` / `credential`
- `coturn` / `turnserver` 프로세스
- 내부 Redis, SSH, HTTP 서비스 바인딩
- Dockerfile의 `0.0.0.0` 바인딩

## 공격 패턴
1. 애플리케이션 파일에서 TURN 서버 주소를 찾습니다.
2. 인증 정보가 비어 있거나 약한지 확인합니다.
3. TURN relay가 외부/내부 목적지로 TCP 연결을 중계하는지 검증합니다.
4. 내부 서비스에 raw protocol을 전달합니다.
5. Redis, SMTP, SSH 등 내부 서비스의 특수 기능으로 이어갑니다.

## 방어 포인트
- TURN 서버에 인증과 허용 목록을 적용합니다.
- 내부 서비스는 외부에서 직접 접근할 수 없게 분리합니다.
- 컨테이너 네트워크와 호스트 네트워크를 명확히 분리합니다.
- Redis 같은 서비스는 `0.0.0.0` 바인딩을 피하고 인증을 설정합니다.

## 관련 예시
- [[csaw-2020-webrtc]]
- [[coturn]]

## 관련 도구
- turner
- redis-rogue-server
- wireshark
