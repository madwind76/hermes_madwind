---
title: Command Injection CTF Template
created: 2026-06-13
updated: 2026-06-21
type: query
tags: [ctf, web, command-injection]
sources: [https://raw.githubusercontent.com/Yahyahcini/hacker101-ctf-writeups/main/Photo%20Gallery/README.md, https://ctftime.org/task/10636, https://ctftime.org/writeup/18603]
confidence: medium
---

# Command Injection CTF Template

## 참고 URL
- [raw source](https://raw.githubusercontent.com/Yahyahcini/hacker101-ctf-writeups/main/Photo%20Gallery/README.md)
- [CTFtime writeup](https://ctftime.org/task/10636)
- [CTFtime writeup](https://ctftime.org/writeup/18603)


## 1. 요약
- 플랫폼:
- 문제명:
- URL:
- 목표:
- 현재 상태:

## 2. 입력점
| Route | Method | Auth | Input | Output | Notes |
|------|------|------|------|------|------|
| | | | host / ip / ping / traceroute / lookup | | 명령 실행 후보 |

## 3. 가설
- 가설 1: 입력이 셸 명령에 직접 연결된다.
- 가설 2: 구분자 또는 인코딩으로 우회할 수 있다.
- 가설 3: 결국 [[rce]] 또는 [[command-injection-core]]으로 이어진다.

## 4. 실험 기록
### 시도 1
- payload:
- 관찰:
- 해석:
- 다음 가설:

### 시도 2
- payload:
- 관찰:
- 해석:
- 다음 가설:

## 5. 연결된 개념
- [[command-injection]]
- [[command-injection-core]]
- [[command-injection-defense]]
- [[rce]]

## 6. 회고
- 막힌 지점:
- 우회 포인트:
- 다음에 먼저 볼 것:
- 재사용 체크리스트:
  - [ ] 구분자 우회 확인
  - [ ] 필터링 문자 확인
  - [ ] 출력 기반 RCE 확인
