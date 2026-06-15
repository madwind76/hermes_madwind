---
title: BoomShop Final Writeup Sample
created: 2026-06-13
updated: 2026-06-13
type: query
tags: [ctf, web, research]
sources: []
confidence: medium
---

# BoomShop Final Writeup Sample

> 이 문서는 **실제 문제를 가정한 최종 writeup 예시**입니다.

## 1. 문제 요약
- 플랫폼: Example CTF
- 목표: admin flag
- 핵심 취약점: [[idor]] + [[ssrf]] 조합
- 보조 개념: [[broken-access-control]], [[ssrf-ctf-patterns]], [[idor-ctf-patterns]]

## 2. 풀이 흐름
1. 프로필 조회 API에서 객체 식별자가 바뀌는지 확인했습니다.
2. 다른 계정의 정보가 반환되어 IDOR 가능성을 확인했습니다.
3. 관리자 기능 중 URL fetch 기능을 발견했습니다.
4. 내부 호스트 및 redirect 우회를 점검했습니다.
5. 권한이 필요한 export 기능이 정상적으로 차단되지 않는 지점을 찾았습니다.

## 3. 핵심 관찰
| 단계 | 관찰 | 해석 |
|------|------|------|
| profile 조회 | user_id 변경 시 다른 사용자 JSON 반환 | 객체 소유권 검증 누락 |
| fetch 기능 | URL 입력 시 서버에서 요청 수행 | SSRF 후보 |
| admin export | 접근 제어가 일관되지 않음 | broken access control 가능성 |

## 4. 결론
- 실질적인 진입점은 IDOR였습니다.
- IDOR로 노출된 데이터가 SSRF 입력점 탐색에 도움이 되었습니다.
- 최종적으로 관리자 흐름을 재현해 flag 경로를 확보했습니다.

## 5. 회고
- 먼저 봐야 할 것: 객체 식별자, 권한 검사, 서버측 fetch 기능
- 다음에 재사용할 체크리스트:
  - [ ] 객체 ID 변경 테스트
  - [ ] redirect / scheme 우회
  - [ ] 내부 호스트 접근 여부
  - [ ] 동일 기능의 인증/비인증 비교

## 6. 연결된 개념
- [[idor]]
- [[ssrf]]
- [[broken-access-control]]
- [[ssti]]
