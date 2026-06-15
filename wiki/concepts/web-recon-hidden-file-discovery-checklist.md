---
title: Web reconnaissance and hidden file discovery checklist
created: 2026-06-15
updated: 2026-06-15
type: concept
tags: [ctf, web, reconnaissance, checklist, robots-txt, hidden-file, directory-discovery]
sources: [/home/kisec/wiki/concepts/web-recon-hidden-file-discovery-ctf-hub.md, /home/kisec/wiki/concepts/hidden-directory-discovery-ctf-patterns.md, /home/kisec/wiki/queries/web-ctf-master-checklist.md]
confidence: high
---

# 정찰형 Web CTF 체크리스트

## Step 1. 한 줄 정의
이 체크리스트는 **웹 CTF에서 `robots.txt`, 숨은 경로, 숨김 파일, 소스 코드, 디렉터리 구조를 체계적으로 확인해 문제 유형을 빠르게 특정하기 위한 점검표**입니다.

## Step 2. 사용 원칙
- **한 번 훑기**보다 **증거를 남기며 반복 확인**하는 방식이 좋습니다.
- 추측한 경로는 반드시 **실제 요청**으로 검증합니다.
- `robots.txt`만 보지 말고 **소스, 정적 자원, 응답 헤더, 파일명 패턴**을 함께 봅니다.
- 결과는 나중에 개념 페이지로 승격할 수 있도록 **가설/사실/확인 완료**를 분리합니다.

## 3. 시작 전 체크
- [ ] 문제명, 플랫폼, URL을 기록했는가
- [ ] 로그인 필요 여부를 확인했는가
- [ ] 기본 페이지 스크린샷 또는 노트를 남겼는가
- [ ] 페이지 소스와 정적 자원 목록을 확인했는가
- [ ] `robots.txt` 접근 여부를 확인했는가

## 4. 정찰 체크
### 4.1 공개 자원
- [ ] `/robots.txt` 확인
- [ ] `.htaccess`, `.DS_Store`, 백업 파일 가능성 점검
- [ ] 소스 코드 주석, 경로 문자열, base64 흔적 확인
- [ ] JS/CSS 파일에서 숨은 엔드포인트 확인

### 4.2 경로 추측
- [ ] trailing slash 유무를 비교했는가
- [ ] 디렉터리 listing 가능성을 확인했는가
- [ ] 흔한 이름(`admin`, `hidden`, `secret`, `backup`, `tmp`)을 시도했는가
- [ ] 파일명 규칙이 반복되는지 확인했는가

### 4.3 요청/응답 차이
- [ ] 200/302/403/404 차이를 기록했는가
- [ ] Content-Type, Length, Location, Server 헤더를 비교했는가
- [ ] 본문에 힌트성 문구가 있는지 확인했는가
- [ ] 동일 경로의 GET/HEAD 차이를 확인했는가

## 5. 증거 기록 템플릿
| 항목 | 내용 |
|------|------|
| 확인한 경로 | `/robots.txt`, `/admin/`, `/secret/` 등 |
| 응답 코드 | 200 / 302 / 403 / 404 |
| 발견 단서 | 파일명, 주석, 링크, 경로 문자열 |
| 다음 가설 | 다음에 시도할 경로 또는 파일 |
| 상태 | 미확인 / 확인 중 / 확정 |

## 6. 유형 판별 체크
아래 항목 중 무엇이 보이는지에 따라 세부 개념으로 내려갑니다.

- [ ] `robots.txt`와 숨은 경로가 핵심이면 → [[hidden-directory-discovery-ctf-patterns]]
- [ ] 로그인 후 숨은 요청이 핵심이면 → [[post-auth-hidden-request-recon-ctf-patterns]]
- [ ] 소스 인스펙션이 핵심이면 → [[source-inspection-minification-ctf-patterns]]
- [ ] 단순 정찰 개념을 정리하려면 → [[reconnaissance]]

## 7. 대표 문제와 연결
- [[where-are-the-robots-final-writeup]]
- [[roboto-sans-final-writeup]]
- [[scavenger-hunt-final-writeup]]
- [[secrets-final-writeup]]

## 8. 마무리 기준
- [ ] 실제 정답 경로를 재현했는가
- [ ] 사용한 단서들을 순서대로 적었는가
- [ ] 실패한 경로도 기록했는가
- [ ] 재사용 가능한 패턴을 개념 페이지로 분리했는가
- [ ] 관련 문서에 wikilink를 연결했는가

## 9. 같이 보면 좋은 페이지
- [[web-recon-hidden-file-discovery-ctf-hub]]
- [[web-recon-hidden-file-discovery-onepage]]
- [[hidden-directory-discovery-ctf-patterns]]
- [[reconnaissance]]
- [[web-ctf-master-checklist]]
- [[web-ctf-writeup-curation]]
