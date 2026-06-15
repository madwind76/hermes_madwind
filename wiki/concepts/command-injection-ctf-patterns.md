---
title: command injection ctf patterns — web ctf 전용 패턴 초안
created: 2026-06-13
updated: 2026-06-13
type: concept
tags: [ctf, web, command-injection, research]
sources: []
confidence: medium
---

# Command Injection CTF Patterns

## 정의
Web CTF에서 Command Injection은 **서버가 외부 입력을 셸 명령에 연결하는 지점에서 명령 분리가 가능한지 확인하는 문제 유형**입니다.

## CTF에서 자주 보이는 신호
- ping, traceroute, lookup, scan, hostname 체크
- 결과를 터미널 형식으로 보여주는 기능
- 에러 출력이 셸과 유사함

## 실험 순서
1. 기본 명령 호출 확인
2. 구분자 우회 확인
3. 인코딩/필터 우회 확인
4. 출력 기반 명령 실행 확인
5. RCE 전환 가능성 확인

## 관찰 포인트
- 에러/성공 메시지 차이
- 지연 시간
- 출력 형식
- 공백, 세미콜론, 파이프, 앰퍼샌드 필터링

## 방어 포인트
- 셸 호출 제거
- argument array 사용
- allowlist 검증
- 최소 권한 실행

## 연결 개념
- [[command-injection]]
- [[command-injection-core]]
- [[command-injection-defense]]
- [[rce]]
