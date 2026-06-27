---
title: Path Traversal CTF Patterns
created: 2026-06-13
updated: 2026-06-21
type: concept
tags: [ctf, web, path-traversal, research]
sources: []
confidence: medium
---

# Path Traversal CTF Patterns

## 참고 URL
- 외부 원문 URL 없음 (내부 정리 페이지)

## 정의
Web CTF에서 Path Traversal은 **파일 경로 입력을 조작해 의도하지 않은 파일을 읽게 만드는 문제 유형**입니다.

## CTF에서 자주 보이는 신호
- `file=`, `path=`, `download=`, `page=`
- 이미지, 로그, 설정 파일 접근
- 상대 경로 또는 인코딩 우회

## 실험 순서
1. 기본 파일명 입력
2. `../` 계열 확인
3. URL 인코딩/이중 인코딩 확인
4. LFI 전환 가능성 확인

## 관찰 포인트
- 에러 메시지
- 존재 여부 차이
- 응답 길이
- 파일 일부 노출

## 방어 포인트
- 정규화된 경로 검증
- allowlist 기반 접근
- 루트 디렉토리 고정
- 민감 파일 분리

## 연결 개념
- [[path-traversal]]
- [[path-traversal-core]]
- [[lfi-rfi]]
- [[broken-access-control]]
