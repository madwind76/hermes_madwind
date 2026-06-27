---
title: IDOR CTF Patterns
created: 2026-06-13
updated: 2026-06-21
type: concept
tags: [ctf, web, idor, research]
sources: []
confidence: medium
---

# IDOR CTF Patterns

## 참고 URL
- 외부 원문 URL 없음 (내부 정리 페이지)

## 정의
Web CTF에서 IDOR는 **직접 객체 참조 값이 바뀔 때 다른 사용자의 자원에 접근되는지** 확인하는 문제 유형입니다.

## CTF에서 자주 보이는 신호
- 숫자형 ID, UUID, 파일명, 주문번호
- `/api/user?id=2`, `/download/123`, `/invoice/uuid`
- 소유권 검사가 응답에 따라 달라짐

## 실험 순서
1. 동일 기능에서 객체 식별자 위치 찾기
2. 값만 바꿔서 응답 차이 확인
3. 인증 상태별로 비교
4. 수평/수직 권한 구분

## 관찰 포인트
- 상태 코드 차이
- 필드 누락/추가
- 다른 사용자의 이름/메일 노출
- 에러 메시지의 세부 차이

## 방어 포인트
- 서버측 authorization
- 객체 소유권 검증
- 추측 불가능한 식별자 사용
- 일관된 에러 응답

## 연결 개념
- [[idor]]
- [[broken-access-control]]
- [[privilege-escalation]]
- [[broken-auth]]
