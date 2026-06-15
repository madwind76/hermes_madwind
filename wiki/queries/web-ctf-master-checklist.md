---
title: Web CTF Master Checklist
created: 2026-06-13
updated: 2026-06-16
type: query
tags: [ctf, web, research]
sources: []
confidence: medium
---

# Web CTF Master Checklist

## 1. 시작 전
- [ ] 플랫폼 / 문제명 / URL 기록
- [ ] 인증 필요 여부 기록
- [ ] 초기 화면 캡처
- [ ] 주입점 후보 3개 이상 메모

## 2. 공격면 점검
- [ ] URL 파라미터 확인
- [ ] POST/JSON 확인
- [ ] 헤더 입력점 확인
- [ ] 파일 업로드 확인
- [ ] 관리자 기능 확인

## 3. 가설 관리
- [ ] 사실과 가설을 분리했는가
- [ ] 한 번에 한 가설만 검증하는가
- [ ] 실패 payload도 기록했는가
- [ ] 응답 차이를 표로 남겼는가

## 4. 개념 승격
- [ ] 반복 기법을 concept page로 분리했는가
- [ ] 관련 페이지를 wikilink로 연결했는가
- [ ] 개념 페이지와 문제 페이지가 양방향 연결되는가

## 5. 마무리
- [ ] 핵심 취약점 1문장 요약
- [ ] 우회 포인트 3개 요약
- [ ] 재사용 체크리스트 작성
- [ ] log.md 업데이트

## 6. 연결 개념
- [[ssrf]]
- [[idor]]
- [[ssti]]
- [[broken-access-control]]
- [[wiki-maintenance-checklist]]
- [[wiki-maintenance-operations]]