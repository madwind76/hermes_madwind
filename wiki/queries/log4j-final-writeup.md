---
title: Log4J — Final Writeup Sample
created: 2026-06-13
updated: 2026-06-13
type: query
tags: [ctf, web, research]
sources: [https://ctftime.org/writeup/34548, https://www.sigflag.at/blog/2022/writeup-googlectf2022-log4j/, https://intrigus.org/research/2022/07/18/google-ctf-2022-log4j2-writeup/]
confidence: medium
---

# Log4J — Final Writeup Sample

> 이 문서는 **공개 writeup을 바탕으로 재구성한 최종 요약 예시**입니다.

## 1. 문제 요약
- 플랫폼: Google CTF 2022
- 점수 / 난이도: web challenge
- 핵심 취약점: Log4j lookup 기능과 Java exception 경로를 이용해 환경변수를 노출시키는 문제입니다.
- 관련 개념: [[rce]], [[web-ctf-master-checklist]]

## 2. 풀이 흐름
1. Flask가 Java 입력을 어떻게 전달하는지 확인합니다.
2. Log4j lookup과 JavaLookup을 시험합니다.
3. stderr를 통해 환경변수 FLAG를 확인합니다.
4. 오류 메시지에 남은 값을 회수합니다.

## 3. 핵심 관찰
| 단계 | 관찰 | 해석 |
|------|------|------|
| 입력 흐름 | 사용자 메시지가 logger로 들어갑니다. | 로그가 곧 공격 표면입니다. |
| lookup | 해석된 문자열이 오류 메시지에 남습니다. | lookup 확장 기능이 원인입니다. |
| 결과 | FLAG 환경변수를 얻습니다. | 전통적 JNDI 없이도 누출이 가능합니다. |

## 4. 방어 관점
- 로그 함수에 사용자 입력을 직접 넘기지 않아야 합니다.
- lookup 기능을 최소화하고 오류 메시지에 비밀을 넣지 않아야 합니다.
- 환경변수는 애플리케이션 로그와 분리해야 합니다.

## 5. 회고
- 이 문제는 Log4j lookup 기능과 Java exception 경로를 이용해 환경변수를 노출시키는 문제입니다.
- 다음에 재사용할 체크리스트:
  - [ ] 입력 검증과 저장 검증이 동일한가
  - [ ] 브라우저 / 서버 / 프록시의 신뢰 경계가 분리되어 있는가
  - [ ] 내부 서비스가 외부에서 간접 접근되는가
  - [ ] 우회에 필요한 브라우저 기능이나 프로토콜이 있는가

## 6. 연결된 개념
- [[rce]]
- [[web-ctf-master-checklist]]
