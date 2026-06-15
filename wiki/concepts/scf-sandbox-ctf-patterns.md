---
title: SafeContentFrame Sandbox
created: 2026-06-13
updated: 2026-06-16
type: concept
tags: [ctf, web, client-side, sandbox, race-condition]
sources: [https://ctftime.org/writeup/40351, https://ctftime.org/writeup/39221, https://gist.github.com/terjanq/e66c2843b5b73aa48405b72f4751d5f8, https://gist.github.com/terjanq/27230afcee73ee75484ac14ac53e78bc]
confidence: medium
---

# SafeContentFrame Sandbox

## 정의
SafeContentFrame(SCF)은 활성 콘텐츠를 격리하기 위한 iframe 기반 샌드박스입니다.

## 왜 중요한가
CTF에서는 렌더링 격리보다 **메시지 흐름, salt 생성, origin 확인**이 더 약한 경우가 많습니다.

## 관찰 포인트
- `postMessage`로 전달되는 salt
- shim iframe의 origin 검증
- non-cached / cached 렌더링 분기
- race condition 가능성

## 공격 패턴
1. 샌드박스가 신뢰하는 메시지 경로를 확인합니다.
2. 랜덤 salt나 해시 입력값의 생성 시점을 노립니다.
3. iframe 참조를 확보한 뒤 동일 origin처럼 동작하는 창을 만듭니다.
4. 최종적으로 flag iframe이나 관리자 브라우저를 읽습니다.

## 방어 포인트
- 메시지 송신자와 수신자 검증을 엄격히 합니다.
- 예측 가능한 salt나 세션 키를 쓰지 않습니다.
- 렌더러와 제어 채널을 분리합니다.

## 관련 예시
- [[postviewer-v5]]
- [[game-arcade]]
