---
title: urlapp — Final Writeup Sample
created: 2026-06-13
updated: 2026-06-13
type: query
tags: [ctf, web, research]
sources: [https://ctftime.org/task/10636, https://ctftime.org/writeup/18603, https://whitesnake1004.tistory.com/704, https://furutsuki.hatenablog.com/entry/2020/03/13/112204]
confidence: medium
---

# urlapp — Final Writeup Sample

> 이 문서는 **공개 writeup을 바탕으로 재구성한 최종 요약 예시**입니다.

## 1. 문제 요약
- 플랫폼: zer0pts CTF 2020
- 점수 / 난이도: 426 pts
- 핵심 취약점: Ruby 앱이 내부 Redis와 통신하는 구조를 악용해 Redis 명령 주입과 RCE로 이어지는 문제입니다.
- 관련 개념: [[redis-ssrf-command-injection-ctf-patterns]], [[ssrf]], [[web-ctf-master-checklist]]

## 2. 풀이 흐름
1. Ruby 앱이 Redis에 어떻게 연결되는지 확인합니다.
2. 입력이 Redis 명령으로 바뀌는 지점을 찾습니다.
3. Redis 기능을 악용해 내부 상태를 바꿉니다.
4. RCE 또는 flag read 경로로 넘어갑니다.

## 3. 핵심 관찰
| 단계 | 관찰 | 해석 |
|------|------|------|
| internal socket | 앱이 Redis로 직접 연결합니다. | 외부에서 못 보던 내부 프로토콜이 노출됩니다. |
| command path | 입력이 Redis 명령과 합쳐집니다. | SSRF가 곧 command injection이 됩니다. |
| 결과 | flag 획득 경로를 확보합니다. | Redis misuse가 핵심입니다. |

## 4. 방어 관점
- 내부 Redis 연결을 사용자 입력과 분리해야 합니다.
- SSRF 입력은 scheme / host allowlist로 제한해야 합니다.
- Redis는 인증과 네트워크 분리를 적용해야 합니다.

## 5. 회고
- 이 문제는 Ruby 앱이 내부 Redis와 통신하는 구조를 악용해 Redis 명령 주입과 RCE로 이어지는 문제입니다.
- 다음에 재사용할 체크리스트:
  - [ ] 입력 검증과 저장 검증이 동일한가
  - [ ] 브라우저 / 서버 / 프록시의 신뢰 경계가 분리되어 있는가
  - [ ] 내부 서비스가 외부에서 간접 접근되는가
  - [ ] 우회에 필요한 브라우저 기능이나 프로토콜이 있는가

## 6. 연결된 개념
- [[redis-ssrf-command-injection-ctf-patterns]]
- [[ssrf]]
- [[web-ctf-master-checklist]]
