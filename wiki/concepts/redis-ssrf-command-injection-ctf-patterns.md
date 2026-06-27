---
title: Redis SSRF / Command Injection
created: 2026-06-13
updated: 2026-06-21
type: concept
tags: [ctf, web, redis, ssrf, command-injection]
sources: [https://ctftime.org/task/10636, https://ctftime.org/writeup/18603, https://whitesnake1004.tistory.com/704, https://furutsuki.hatenablog.com/entry/2020/03/13/112204]
confidence: medium
---

# Redis SSRF / Command Injection

## 참고 URL
- [CTFtime writeup](https://ctftime.org/task/10636)
- [CTFtime writeup](https://ctftime.org/writeup/18603)
- [whitesnake1004.tistory.com](https://whitesnake1004.tistory.com/704)
- [furutsuki.hatenablog.com](https://furutsuki.hatenablog.com/entry/2020/03/13/112204)

## 정의
웹앱이 내부 Redis에 직접 연결하거나, 사용자 입력을 Redis 명령으로 변환해 버리는 문제입니다.

## 왜 중요한가
Redis는 인증이 없거나 내부 바인딩이 느슨하면, 단순 데이터 저장소가 아니라 공격 통로가 됩니다.

## 관찰 포인트
- `TCPSocket.open("redis", 6379)` 같은 내부 연결
- URL 입력이 Redis 명령으로 이어지는지 여부
- `BITOP`, `SLAVEOF`, `CONFIG SET` 같은 민감 명령
- 내부 호스트명 / 컨테이너 네트워크

## 공격 패턴
1. 웹 입력이 Redis 쪽으로 전달되는 흐름을 확인합니다.
2. raw command를 직접 보낼 수 있는지 시험합니다.
3. replication 또는 key rewriting 기능으로 확장합니다.
4. 읽기 / 쓰기 / RCE 경로를 확보합니다.

## 방어 포인트
- Redis를 내부망에만 두고 인증을 적용합니다.
- 앱에서 raw command 조립을 피합니다.
- SSRF 입력은 allowlist 기반으로 검증합니다.

## 관련 예시
- [[urlapp]]
