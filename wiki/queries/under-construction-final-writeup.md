---
title: under-construction — final writeup sample
created: 2026-06-13
updated: 2026-06-13
type: query
tags: [ctf, web, research]
sources: [https://blog.shameerkashif.me/blog/2023/writeup-under-construction-google-ctf-2023/, https://ctftime.org/writeup/37351, https://ctftime.org/writeup/37549, https://ctftime.org/writeup/37330]
confidence: medium
---

# Under Construction — Final Writeup Sample

> 이 문서는 **공개 writeup을 바탕으로 재구성한 최종 요약 예시**입니다.

## 1. 문제 요약
- 플랫폼: Google CTF 2023
- 점수 / 난이도: web
- 핵심 취약점: Flask와 PHP 사이의 다중 파라미터 처리 차이를 이용해 gold tier 계정을 만드는 문제입니다.
- 관련 개념: [[parameter-tampering-ctf-patterns]], [[web-ctf-master-checklist]]

## 2. 풀이 흐름
1. Flask와 PHP가 파라미터를 다르게 해석하는 지점을 찾습니다.
2. tier 값을 두 번 보내 검증과 저장을 분리합니다.
3. gold tier 계정을 만들어 로그인합니다.
4. FLAG가 출력되는 응답을 확인합니다.

## 3. 핵심 관찰
| 단계 | 관찰 | 해석 |
|------|------|------|
| validation | Flask는 첫 번째 tier를 검사합니다. | 검증이 저장과 분리됩니다. |
| forwarding | PHP는 다른 tier 값을 봅니다. | raw request가 문제의 중심입니다. |
| 결과 | gold 계정으로 FLAG가 노출됩니다. | parameter pollution의 전형입니다. |

## 4. 방어 관점
- 검증과 저장이 동일한 파서 기준을 써야 합니다.
- 다중 파라미터 입력은 명시적으로 거부해야 합니다.
- 프록시로 요청을 넘길 때 raw body를 재해석하지 않아야 합니다.

## 5. 회고
- 이 문제는 Flask와 PHP 사이의 다중 파라미터 처리 차이를 이용해 gold tier 계정을 만드는 문제입니다.
- 다음에 재사용할 체크리스트:
  - [ ] 입력 검증과 저장 검증이 동일한가
  - [ ] 브라우저 / 서버 / 프록시의 신뢰 경계가 분리되어 있는가
  - [ ] 내부 서비스가 외부에서 간접 접근되는가
  - [ ] 우회에 필요한 브라우저 기능이나 프로토콜이 있는가

## 6. 연결된 개념
- [[parameter-tampering-ctf-patterns]]
- [[web-ctf-master-checklist]]
