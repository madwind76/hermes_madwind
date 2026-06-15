---
title: game-arcade — final writeup sample
created: 2026-06-13
updated: 2026-06-13
type: query
tags: [ctf, web, research]
sources: [https://ctftime.org/writeup/39221, https://gist.github.com/terjanq/27230afcee73ee75484ac14ac53e78bc, https://ctftime.org/task/28606]
confidence: medium
---

# Game Arcade — Final Writeup Sample

> 이 문서는 **공개 writeup을 바탕으로 재구성한 최종 요약 예시**입니다.

## 1. 문제 요약
- 플랫폼: Google CTF 2024
- 점수 / 난이도: 333 pts
- 핵심 취약점: SCF double-hash 취약점과 XSS를 결합해 관리자 브라우저 데이터를 읽는 문제입니다.
- 관련 개념: [[scf-sandbox-ctf-patterns]], [[web-ctf-master-checklist]], [[xss]]

## 2. 풀이 흐름
1. 게임 렌더링과 shim URL을 분석합니다.
2. double-hash 우회를 통해 공격 origin을 실행합니다.
3. XSS로 admin cookie 또는 localStorage를 획득합니다.
4. flag가 담긴 값을 외부로 전송합니다.

## 3. 핵심 관찰
| 단계 | 관찰 | 해석 |
|------|------|------|
| origin 계산 | shim이 첫 번째 hash만 신뢰하는 경로가 있습니다. | 안전해야 할 검증이 우회됩니다. |
| XSS sink | password가 HTML로 삽입됩니다. | 클라이언트 저장소도 공격 표면입니다. |
| 결과 | admin 저장값이 유출됩니다. | 샌드박스와 XSS가 결합된 전형적 웹 CTF입니다. |

## 4. 방어 관점
- iframe sandbox와 origin 검증은 단일 로직으로 단순하게 유지해야 합니다.
- 클라이언트 저장소에 민감정보를 두지 않아야 합니다.
- HTML sink는 텍스트 렌더링으로 대체해야 합니다.

## 5. 회고
- 이 문제는 SCF double-hash 취약점과 XSS를 결합해 관리자 브라우저 데이터를 읽는 문제입니다.
- 다음에 재사용할 체크리스트:
  - [ ] 입력 검증과 저장 검증이 동일한가
  - [ ] 브라우저 / 서버 / 프록시의 신뢰 경계가 분리되어 있는가
  - [ ] 내부 서비스가 외부에서 간접 접근되는가
  - [ ] 우회에 필요한 브라우저 기능이나 프로토콜이 있는가

## 6. 연결된 개념
- [[scf-sandbox-ctf-patterns]]
- [[web-ctf-master-checklist]]
- [[xss]]
