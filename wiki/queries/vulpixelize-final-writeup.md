---
title: Vulpixelize — Final Writeup Sample
created: 2026-06-13
updated: 2026-06-13
type: query
tags: [ctf, web, research]
sources: [https://blog.nella17.tw/p/hitcon-ctf-2021-writeups/, https://ctftime.org/task/18312, https://ctftime.org/writeup/31677, https://github.com/orangetw/My-CTF-Web-Challenges]
confidence: medium
---

# Vulpixelize — Final Writeup Sample

> 이 문서는 **공개 writeup을 바탕으로 재구성한 최종 요약 예시**입니다.

## 1. 문제 요약
- 플랫폼: HITCON CTF 2021
- 점수 / 난이도: 232 pts
- 핵심 취약점: 브라우저 캡처와 text fragment / DNS rebinding을 활용해 localhost flag를 읽는 문제입니다.
- 관련 개념: [[dns-rebinding-ctf-patterns]], [[web-ctf-master-checklist]]

## 2. 풀이 흐름
1. 스냅샷 서비스와 내부 flag 경로를 확인합니다.
2. text fragment 또는 이미지 조작으로 조각을 읽습니다.
3. DNS rebinding으로 localhost를 같은 출처처럼 만듭니다.
4. 내부 `/flag` 응답을 수집합니다.

## 3. 핵심 관찰
| 단계 | 관찰 | 해석 |
|------|------|------|
| snapshot | 64x64 캡처가 제공됩니다. | 정보량이 적어도 브라우저 기능이 남습니다. |
| rebinding | 같은 도메인이 내부 IP로 재해석됩니다. | 동일 출처 가정을 무너뜨립니다. |
| 결과 | flag 엔드포인트가 노출됩니다. | 브라우저 feature와 네트워크 트릭이 결합됩니다. |

## 4. 방어 관점
- 내부 서비스는 Host header와 출처 검증을 병행해야 합니다.
- 브라우저 캡처 서비스에서 localhost 접근을 제한해야 합니다.
- 텍스트 처리와 이미지 처리 모두를 공격면으로 봐야 합니다.

## 5. 회고
- 이 문제는 브라우저 캡처와 text fragment / DNS rebinding을 활용해 localhost flag를 읽는 문제입니다.
- 다음에 재사용할 체크리스트:
  - [ ] 입력 검증과 저장 검증이 동일한가
  - [ ] 브라우저 / 서버 / 프록시의 신뢰 경계가 분리되어 있는가
  - [ ] 내부 서비스가 외부에서 간접 접근되는가
  - [ ] 우회에 필요한 브라우저 기능이나 프로토콜이 있는가

## 6. 연결된 개념
- [[dns-rebinding-ctf-patterns]]
- [[web-ctf-master-checklist]]
