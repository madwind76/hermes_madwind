---
title: Web reconnaissance and hidden file discovery — picoCTF hub
created: 2026-06-15
updated: 2026-06-21
type: concept
tags: [ctf, web, reconnaissance, robots-txt, hidden-file, directory-discovery, source-inspection]
sources: [https://medium.com/@hasnain_abid/where-are-the-robots-picoctf-web-exploitation-writeup-82a121cfd935, https://medium.com/@Kamal_S/picoctf-web-exploitation-where-are-the-robots-399111c4dc8e, https://medium.com/@ahmednarmer1/ctf-day-29-7f76f92d5fb5, https://medium.com/@ahmednarmer1/ctf-day-17-24ec4fd7a7e5, https://medium.com/@tolentinojesusanthony/scavenger-hunt-picoctf-dc37004ed0e3, https://medium.com/@bl0ss0mx5/picogym-web-exploitation-writeup-scavenger-hunt-easy-picoctf-bf254302f920]
confidence: high
---

# Web reconnaissance and hidden file discovery — picoCTF hub

## 참고 URL
- [medium.com](https://medium.com/@hasnain_abid/where-are-the-robots-picoctf-web-exploitation-writeup-82a121cfd935)
- [medium.com](https://medium.com/@Kamal_S/picoctf-web-exploitation-where-are-the-robots-399111c4dc8e)
- [medium.com](https://medium.com/@ahmednarmer1/ctf-day-29-7f76f92d5fb5)
- [medium.com](https://medium.com/@ahmednarmer1/ctf-day-17-24ec4fd7a7e5)
- [medium.com](https://medium.com/@tolentinojesusanthony/scavenger-hunt-picoctf-dc37004ed0e3)
- [medium.com](https://medium.com/@bl0ss0mx5/picogym-web-exploitation-writeup-scavenger-hunt-easy-picoctf-bf254302f920)

## Step 1. 한 줄 정의
이 허브는 **웹 CTF에서 정답이 취약점 자체보다도 `robots.txt`, 숨은 경로, 숨김 파일, 소스 코드, 디렉터리 구조 같은 정찰 단서에 숨어 있는 문제들**을 묶어 보는 상위 개념입니다.

## Step 2. 비유
- **비유**: 지도에 없는 보물찾기에서, 표지판과 메모를 따라 숨은 방을 찾아가는 느낌입니다.
- **이미지**: `robots.txt`는 "여기는 가지 마세요"라는 안내판처럼 보이지만, 실제로는 힌트를 주는 출발점이 됩니다.
- **전문 설명**: 웹 애플리케이션의 공개 자원, 디렉터리 경로, 소스 코드, 숨김 파일을 순서대로 확인해 실제 접근 경로를 역추적하는 유형입니다.

## 핵심 신호
| 신호 | 먼저 확인할 것 | 왜 중요한가 |
|------|----------------|--------------|
| `robots.txt` 존재 | `Disallow` 경로 | 숨은 페이지 후보가 드러납니다 |
| 소스 코드 주석 | HTML/JS/CSS 주석, 경로 문자열 | 경로명과 기능 흐름이 노출될 수 있습니다 |
| 숨김 파일 | `.htaccess`, `.DS_Store`, 백업 파일 | 디렉터리 구조와 예외 경로를 알려줍니다 |
| 디렉터리 흔적 | trailing slash, directory listing, 파일명 추측 | 다음 단계 경로를 직접 접근할 수 있습니다 |
| 여러 단서 조합 | `robots.txt` + 소스 + 숨김 파일 | 단일 힌트가 아닌 체인으로 풀리는 경우가 많습니다 |

## 대표 문제 흐름
```text
메인 페이지 확인 -> source inspection -> robots.txt 확인 -> 숨은 경로 접근 -> 숨김 파일/추가 디렉터리 추적 -> flag 획득
```

## 하위 패턴
- [[hidden-directory-discovery-ctf-patterns]] — 소스와 URL 경로로 숨은 디렉터리를 추적하는 기본 패턴
- [[post-auth-hidden-request-recon-ctf-patterns]] — 로그인 후 네트워크 탭/숨은 요청을 추적하는 패턴
- [[reconnaissance]] — 공격 전 정보 수집의 상위 개념
- [[web-recon-hidden-file-discovery-checklist]] — 실제 정찰 절차를 점검하는 체크리스트
- [[web-recon-hidden-file-discovery-onepage]] — 실전용 1페이지 요약판

## 대표 writeup
- [[where-are-the-robots-final-writeup]] — `robots.txt` 기반 숨은 경로 탐색
- [[roboto-sans-final-writeup]] — `robots.txt`와 숨은 경로 결합
- [[scavenger-hunt-final-writeup]] — `robots.txt`, `.htaccess`, `.DS_Store` 조합형 정찰
- [[secrets-final-writeup]] — 소스/디렉터리 경로를 따라가는 전형적 탐색

## 공격자 관점
1. 메인 페이지에서 기능보다 **단서**를 먼저 찾습니다.
2. `/robots.txt`를 열어 숨은 경로를 확인합니다.
3. HTML/JS/CSS 소스에서 경로 문자열과 주석을 찾습니다.
4. `.htaccess`, `.DS_Store`, 백업 파일 같은 숨김 자원도 함께 확인합니다.
5. 경로가 나오면 직접 요청해 최종 페이지까지 추적합니다.

## 방어자 관점
- `robots.txt`에 민감한 경로나 관리 경로를 넣지 않습니다.
- 숨김 파일과 백업 파일을 배포본에 남기지 않습니다.
- 디렉터리 listing을 비활성화하고, 추측 가능한 경로에는 인증을 적용합니다.
- 소스 코드와 정적 자원에 힌트성 문자열을 남기지 않습니다.
- 공개 자원만으로 내부 구조가 쉽게 복원되지 않도록 경로명을 설계합니다.

## 같이 보면 좋은 페이지
- [[reconnaissance]]
- [[hidden-directory-discovery-ctf-patterns]]
- [[web-ctf-writeup-curation]]
- [[web-ctf-writeup-topic-map]]
- [[where-are-the-robots-final-writeup]]
- [[roboto-sans-final-writeup]]
- [[scavenger-hunt-final-writeup]]
- [[secrets-final-writeup]]

## 참고 소스
- [Hasnain Abid — Where Are the Robots?](https://medium.com/@hasnain_abid/where-are-the-robots-picoctf-web-exploitation-writeup-82a121cfd935)
- [Kamal S — picoCTF Web Exploitation: where are the robots](https://medium.com/@Kamal_S/picoctf-web-exploitation-where-are-the-robots-399111c4dc8e)
- [Ahmed Narmer — CTF Day(29): Roboto Sans](https://medium.com/@ahmednarmer1/ctf-day-29-7f76f92d5fb5)
- [Ahmed Narmer — CTF Day(17): Scavenger Hunt](https://medium.com/@ahmednarmer1/ctf-day-17-24ec4fd7a7e5)
- [Anthony Tolentino — Scavenger Hunt: picoCTF](https://medium.com/@tolentinojesusanthony/scavenger-hunt-picoctf-dc37004ed0e3)
- [bl0ss0mx5 — Scavenger Hunt](https://medium.com/@bl0ss0mx5/picogym-web-exploitation-writeup-scavenger-hunt-easy-picoctf-bf254302f920)
