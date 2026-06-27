---
title: Scavenger Hunt — picoCTF web writeup
created: 2026-06-15
updated: 2026-06-21
type: query
tags: [ctf, web, reconnaissance, robots-txt, htaccess, ds-store, source-inspection]
sources: [https://medium.com/@ahmednarmer1/ctf-day-17-24ec4fd7a7e5, https://medium.com/@tolentinojesusanthony/scavenger-hunt-picoctf-dc37004ed0e3, https://medium.com/@bl0ss0mx5/picogym-web-exploitation-writeup-scavenger-hunt-easy-picoctf-bf254302f920]
confidence: high
---

# Scavenger Hunt — picoCTF web writeup

> 웹페이지 곳곳에 흩어진 단서를 모아 `robots.txt`, 숨은 경로, `.htaccess`, `.DS_Store` 등을 따라가며 flag를 찾는 picoCTF Web Exploitation 문제입니다.

## 참고 URL
- [medium.com](https://medium.com/@ahmednarmer1/ctf-day-17-24ec4fd7a7e5)
- [medium.com](https://medium.com/@tolentinojesusanthony/scavenger-hunt-picoctf-dc37004ed0e3)
- [medium.com](https://medium.com/@bl0ss0mx5/picogym-web-exploitation-writeup-scavenger-hunt-easy-picoctf-bf254302f920)


## 1. 한 줄 요약
- 핵심은 **한 번에 끝내는 취약점**이 아니라 **흩어진 단서 수집**입니다.
- `robots.txt`와 소스/숨김 파일이 주요 단서입니다.
- 여러 파일 조각을 이어 붙여 최종 경로에 도달합니다.

## 2. 문제 흐름
| 단계 | 관찰 | 의미 |
|------|------|------|
| 1 | 페이지 소스와 보이는 링크를 확인 | 초기 단서 수집 |
| 2 | `robots.txt` 접근 | 숨긴 경로 후보 확인 |
| 3 | `.htaccess`, `.DS_Store` 같은 숨김 파일 발견 | 웹 서버 구성 단서 확보 |
| 4 | 숨은 페이지와 파일을 순차적으로 추적 | flag 위치 접근 |
| 5 | 최종 페이지에서 flag 확인 | 문제 해결 |

## 3. 분석 포인트
```text
# 보이는 링크만 보지 말고 robots.txt, hidden file, directory listing 여부를 함께 확인합니다.
# 예상 결과: 여러 개의 조각을 모아 최종 경로에 도달하고 flag를 획득합니다.
```

## 4. 공격자 관점
1. 페이지 소스와 링크를 먼저 확인합니다.
2. `/robots.txt`를 열어 숨은 디렉터리 힌트를 찾습니다.
3. `.htaccess`, `.DS_Store`처럼 잘 숨겨진 파일도 확인합니다.
4. 각 조각을 메모하고 경로를 조합합니다.
5. 최종 경로에 도달하면 flag를 확인합니다.

## 5. 방어자 관점
- `robots.txt`는 보안 통제가 아니라 검색 엔진 힌트입니다.
- 숨김 파일에 민감한 정보나 경로 힌트를 두지 않습니다.
- 디렉터리 listing과 불필요한 메타 파일 노출을 막습니다.
- 공개 자원만으로 전체 경로가 재구성되지 않도록 설계합니다.

## 6. 같이 보면 좋은 페이지
- [[reconnaissance]]
- [[hidden-directory-discovery-ctf-patterns]]
- [[path-traversal-core]]
- [[source-inspection-minification-ctf-patterns]]

## 7. 참고 소스
- [Ahmed Narmer — CTF Day(17): Scavenger Hunt](https://medium.com/@ahmednarmer1/ctf-day-17-24ec4fd7a7e5)
- [Anthony Tolentino — Scavenger Hunt: picoCTF](https://medium.com/@tolentinojesusanthony/scavenger-hunt-picoctf-dc37004ed0e3)
- [bl0ss0mx5 — picoGym Web Exploitation Writeup | Scavenger Hunt](https://medium.com/@bl0ss0mx5/picogym-web-exploitation-writeup-scavenger-hunt-easy-picoctf-bf254302f920)
