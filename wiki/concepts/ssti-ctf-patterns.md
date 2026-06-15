---
title: SSTI CTF Patterns
created: 2026-06-13
updated: 2026-06-16
type: concept
tags: [ctf, web, ssti, research]
sources: []
confidence: medium
---

# SSTI CTF Patterns

## 정의
Web CTF에서 SSTI는 **사용자 입력이 템플릿 엔진의 문법으로 해석되는지** 확인하는 문제 유형입니다.

## CTF에서 자주 보이는 신호
- `{{ }}`, `${ }`, `<%= %>` 같은 특수 문법
- 미리보기, 메시지 렌더링, 이메일 템플릿
- 입력값 일부가 그대로 렌더링됨

## 실험 순서
1. 템플릿 문법 반응 확인
2. 엔진 식별
3. 변수 출력
4. 필터 우회
5. 코드 실행 가능성 확인

## 관찰 포인트
- 에러 메시지
- 출력 변형
- 이스케이프 여부
- 필터링 패턴

## 방어 포인트
- 템플릿과 입력 분리
- 이스케이프 강제
- 화이트리스트 렌더링
- 서버측 검증

## 연결 개념
- [[ssti]]
- [[ssti-core]]
- [[jinja2-filter-bypass]]
- [[jinja2-template-engine]]
- [[rce]]
- [[command-injection]]

## 관련 writeup
- [[ssti1-final-writeup]] — picoCTF 2025 Jinja2 SSTI 입문 문제

## 관련 writeup
- [[ssti2-final-writeup]] — picoCTF 2025 SSTI2 필터 우회 문제
