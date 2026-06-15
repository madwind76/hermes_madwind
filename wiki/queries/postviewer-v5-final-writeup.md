---
title: Postviewer v5 — Final Writeup Sample
created: 2026-06-13
updated: 2026-06-13
type: query
tags: [ctf, web, research]
sources: [https://ctftime.org/writeup/40351, https://gist.github.com/terjanq/e66c2843b5b73aa48405b72f4751d5f8, https://ctftime.org/event/2718/tasks/]
confidence: medium
---

# Postviewer v5 — Final Writeup Sample

> 이 문서는 **공개 writeup을 바탕으로 재구성한 최종 요약 예시**입니다.

## 1. 문제 요약
- 플랫폼: Google CTF 2025
- 점수 / 난이도: 474 pts
- 핵심 취약점: SafeContentFrame의 salt 생성과 메시지 전달을 노린 race condition 풀이입니다.
- 관련 개념: [[scf-sandbox-ctf-patterns]], [[web-ctf-master-checklist]]

## 2. 풀이 흐름
1. SCF shim과 파일 렌더링 흐름을 확인합니다.
2. non-cached 파일로 salt 누출을 유도합니다.
3. PRNG를 복구해 다음 salt를 예측합니다.
4. 예측된 origin에 페이로드를 심습니다.
5. 관리자 봇의 flag 파일을 같은 origin에서 읽습니다.

## 3. 핵심 관찰
| 단계 | 관찰 | 해석 |
|------|------|------|
| 파일 분기 | non-cached 경로에서 random salt가 사용됩니다. | 예측 가능한 난수는 샌드박스 신뢰를 무너뜨립니다. |
| 메시지 흐름 | postMessage가 salt 전달 통로입니다. | 신뢰 경계를 다시 설계해야 합니다. |
| 최종 성공 | 예측된 origin에서 flag iframe을 읽습니다. | race condition이 실질 취약점입니다. |

## 4. 방어 관점
- 임의값은 예측 불가능한 CSPRNG로 생성해야 합니다.
- 샌드박스 메시지는 전송자와 수신자를 엄격히 검증해야 합니다.
- 렌더링과 공유 기능을 같은 origin 신뢰 모델에 묶지 않아야 합니다.

## 5. 회고
- 이 문제는 SafeContentFrame의 salt 생성과 메시지 전달을 노린 race condition 풀이입니다.
- 다음에 재사용할 체크리스트:
  - [ ] 입력 검증과 저장 검증이 동일한가
  - [ ] 브라우저 / 서버 / 프록시의 신뢰 경계가 분리되어 있는가
  - [ ] 내부 서비스가 외부에서 간접 접근되는가
  - [ ] 우회에 필요한 브라우저 기능이나 프로토콜이 있는가

## 6. 연결된 개념
- [[scf-sandbox-ctf-patterns]]
- [[web-ctf-master-checklist]]
