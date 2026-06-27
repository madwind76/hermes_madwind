---
title: Command injection writeup survey
created: 2026-06-19
updated: 2026-06-21
type: query
tags: [ctf, web, survey, writeup, command-injection, os-command-injection, shell-injection, rce]
sources: [https://raw.githubusercontent.com/Yahyahcini/hacker101-ctf-writeups/main/Photo%20Gallery/README.md, https://ctftime.org/task/10636, https://ctftime.org/writeup/18603]
confidence: high
---

# Command injection writeup survey

## 참고 URL
- [raw source](https://raw.githubusercontent.com/Yahyahcini/hacker101-ctf-writeups/main/Photo%20Gallery/README.md)
- [CTFtime writeup](https://ctftime.org/task/10636)
- [CTFtime writeup](https://ctftime.org/writeup/18603)


## 1. 목적
서버가 사용자 입력을 쉘 명령이나 내부 command path에 흘려보내는 writeup을 비교합니다.

## 2. 비교 대상
| 문제 | 주된 primitive | 보조 primitive | 한 줄 요약 |
|---|---|---|---|
| Photo Gallery | SQLi → command injection | source leak | SQLi로 소스를 읽고 파일명 처리에서 쉘 주입으로 넘어갑니다. |
| urlapp | Redis command injection surface | SSRF | 내부 Redis 명령 경로가 외부 입력에 노출됩니다. |

## 3. 공통 관찰
1. 명령 주입은 `;`, `|`, `&&` 같은 문자만의 문제가 아니라 **명령을 조합하는 설계** 자체의 문제입니다.
2. 내부 서비스나 파일명 목록을 쉘에 넘기는 순간 RCE로 이어질 수 있습니다.
3. SQLi나 SSRF가 먼저 보이더라도, 최종 착지점이 command injection인 경우가 많습니다.

## 4. 관련 개념
- [[command-injection]]
- [[command-injection-defense]]
- [[redis-ssrf-command-injection-ctf-patterns]]
- [[web-ctf-writeup-family-hub]]
- [[photo-gallery-final-writeup]]
- [[urlapp-final-writeup]]

## 5. 다음 읽을 거리
- [[photo-gallery-final-writeup]]
- [[urlapp-final-writeup]]
