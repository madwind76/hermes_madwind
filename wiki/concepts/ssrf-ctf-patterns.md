---
title: SSRF CTF Patterns
created: 2026-06-13
updated: 2026-06-19
type: concept
tags: [ctf, web, ssrf, research]
sources: []
confidence: medium
---

# SSRF CTF Patterns

## 정의
Web CTF에서 SSRF는 **서버가 대신 외부 요청을 수행하는 입력점**을 찾고, 그 요청을 내부 네트워크나 메타데이터 서비스로 유도하는 문제 유형입니다.

## CTF에서 자주 보이는 신호
- URL을 직접 받는 기능
- webhook, import from URL, preview, fetch, screenshot
- redirect 허용
- DNS lookup 지연 또는 timeout 차이

## 실험 순서
1. 외부 URL 요청 여부 확인
2. redirect / scheme / host 우회 확인
3. 내부 IP 및 localhost 접근 확인
4. 메타데이터 엔드포인트 확인

## 관찰 포인트
- 응답 시간
- 에러 메시지
- 사용자 에이전트
- DNS 로그
- 캐시 여부

## 방어 포인트
- allowlist 사용
- scheme 검증
- redirect 차단
- 내부 대역 차단
- 메타데이터 보호

## 연결 개념
- [[ssrf]]
- [[ssrf-core]]
- [[ssrf-defense]]
- [[broken-access-control]]
- [[proxy-mirror-final-writeup]]
