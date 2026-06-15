---
title: Roboto Sans — picoCTF web writeup
created: 2026-06-15
updated: 2026-06-15
type: query
tags: [ctf, web, reconnaissance, robots-txt, hidden-path, source-inspection]
sources: [https://medium.com/@ahmednarmer1/ctf-day-29-7f76f92d5fb5, https://azt3c.medium.com/picoctf-2022-roboto-sans-challenge-writeup-59156b94fdc7]
confidence: high
---

# Roboto Sans — picoCTF web writeup

> `robots.txt`와 숨겨진 경로를 조합해 flag로 이어지는 페이지를 찾아내는 picoCTF Web Exploitation 문제입니다.

## 1. 한 줄 요약
- 핵심은 **`robots.txt`를 통해 숨은 경로를 찾는 것**입니다.
- 경로를 열어보면 flag가 있는 위치에 도달합니다.
- 문제의 초점은 취약점 악용보다 **정찰과 경로 발견**입니다.

## 2. 문제 흐름
| 단계 | 관찰 | 의미 |
|------|------|------|
| 1 | 초기 화면은 단순함 | 숨은 단서가 있을 가능성 큼 |
| 2 | `/robots.txt` 확인 | 공개 힌트 파일 확보 |
| 3 | 비공개 경로 발견 | hidden path 후보 확보 |
| 4 | 해당 경로 접근 | flag 페이지 탐색 |
| 5 | flag 확인 | 문제 해결 |

## 3. 분석 포인트
```text
# robots.txt와 숨은 경로를 함께 확인합니다.
# 예상 결과: Disallow 또는 비공개 경로가 flag 페이지로 이어집니다.
```

## 4. 공격자 관점
1. 웹사이트 루트와 일반 링크를 먼저 봅니다.
2. `/robots.txt`를 열어 숨은 디렉터리 정보를 확인합니다.
3. 경로가 있으면 바로 접근해 봅니다.
4. 추가로 페이지 소스도 함께 확인합니다.
5. flag가 노출되는지 점검합니다.

## 5. 방어자 관점
- `robots.txt`에 민감한 디렉터리를 쓰지 않습니다.
- 숨겨야 할 자원은 인증/인가로 보호합니다.
- 민감한 파일명이나 경로를 추측하기 쉽게 두지 않습니다.
- 공개 경로와 내부 경로를 분리합니다.

## 6. 같이 보면 좋은 페이지
- [[hidden-directory-discovery-ctf-patterns]]
- [[where-are-the-robots-final-writeup]]
- [[scavenger-hunt-final-writeup]]
- [[web-ctf-writeup-curation]]

## 7. 참고 소스
- [Ahmed Narmer — CTF Day(29): Roboto Sans](https://medium.com/@ahmednarmer1/ctf-day-29-7f76f92d5fb5)
- [azt3c — PicoCTF 2022: Roboto Sans & Inspect HTML](https://azt3c.medium.com/picoctf-2022-roboto-sans-challenge-writeup-59156b94fdc7)
