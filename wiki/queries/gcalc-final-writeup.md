---
title: gCalc — Final Writeup Sample
created: 2026-06-13
updated: 2026-06-13
type: query
tags: [ctf, web, research]
sources: [https://blog.orange.tw/2018/06/google-ctf-2018-quals-web-gcalc.html, https://orange-tw.blogspot.com/2018/06/?m=1, https://github.com/eskildsen/google-ctf-2018, https://github.com/EmpireCTF/empirectf/blob/master/writeups/2018-06-23-Google-CTF-Quals/README.md]
confidence: medium
---

# gCalc — Final Writeup Sample

> 이 문서는 **공개 writeup을 바탕으로 재구성한 최종 요약 예시**입니다.

## 1. 문제 요약
- 플랫폼: Google CTF 2018 Quals
- 점수 / 난이도: 326 pts
- 핵심 취약점: new Function 기반 계산기 XSS와 CSP 제약을 Google Analytics로 우회하는 문제입니다.
- 관련 개념: [[web-inspector-ctf-patterns]], [[xss]], [[web-ctf-master-checklist]]

## 2. 풀이 흐름
1. expr가 JS 실행으로 이어지는지 확인합니다.
2. vars 객체의 키를 payload로 사용합니다.
3. CSP가 허용하는 이미지 채널을 찾습니다.
4. Google Analytics 요청으로 cookie를 외부로 보냅니다.

## 3. 핵심 관찰
| 단계 | 관찰 | 해석 |
|------|------|------|
| expression engine | new Function 경로가 있습니다. | 계산기가 곧 JS 실행기입니다. |
| filter bypass | 소문자화 필터를 우회합니다. | 입력 정규화가 공격에 약합니다. |
| exfil | img-src 허용 채널이 있습니다. | CSP가 있어도 유출이 가능할 수 있습니다. |

## 4. 방어 관점
- new Function / eval 계열을 피해야 합니다.
- CSP는 허용 도메인을 최소화해야 합니다.
- 클라이언트 값은 신뢰하지 말고 서버 쪽에서 검증해야 합니다.

## 5. 회고
- 이 문제는 new Function 기반 계산기 XSS와 CSP 제약을 Google Analytics로 우회하는 문제입니다.
- 다음에 재사용할 체크리스트:
  - [ ] 입력 검증과 저장 검증이 동일한가
  - [ ] 브라우저 / 서버 / 프록시의 신뢰 경계가 분리되어 있는가
  - [ ] 내부 서비스가 외부에서 간접 접근되는가
  - [ ] 우회에 필요한 브라우저 기능이나 프로토콜이 있는가

## 6. 연결된 개념
- [[web-inspector-ctf-patterns]]
- [[xss]]
- [[web-ctf-master-checklist]]
