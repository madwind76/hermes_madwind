---
title: 정찰형 Web CTF 실전 1페이지 요약
created: 2026-06-15
updated: 2026-06-21
type: concept
tags: [ctf, web, reconnaissance, onepage, robots-txt, hidden-file, directory-discovery]
sources: [/home/kisec/wiki/concepts/web-recon-hidden-file-discovery-checklist.md, /home/kisec/wiki/concepts/web-recon-hidden-file-discovery-ctf-hub.md]
confidence: high
---

# 정찰형 Web CTF 실전 1페이지 요약

## 참고 URL
- [Reference](/home/kisec/wiki/concepts/web-recon-hidden-file-discovery-checklist.md)
- [Reference](/home/kisec/wiki/concepts/web-recon-hidden-file-discovery-ctf-hub.md)

## 1. 이 페이지의 목적
이 페이지는 **`robots.txt`, 숨은 경로, 숨김 파일, 소스 코드 단서**를 빠르게 점검할 때 보는 실전용 요약판입니다.

## 2. 30초 점검 순서
1. 메인 페이지에서 **소스 보기**를 먼저 합니다.
2. `/robots.txt`를 확인합니다.
3. JS/CSS/HTML에서 경로 문자열을 찾습니다.
4. `.htaccess`, `.DS_Store`, backup 파일 가능성을 봅니다.
5. 추측한 경로는 직접 요청해서 **응답 코드**를 확인합니다.

## 3. 꼭 보는 신호
| 신호 | 의미 | 다음 행동 |
|------|------|----------|
| `robots.txt`의 `Disallow` | 숨은 경로 후보 | 직접 접근 |
| 주석/경로 문자열 | 다음 단계 힌트 | 같은 패턴 추적 |
| `403` | 존재하지만 차단됨 | 인증/헤더/경로 변형 확인 |
| `404` | 경로 추측 실패 가능 | 파일명 규칙 재점검 |
| `302` | 우회/리다이렉트 가능성 | Location 추적 |

## 4. 자주 나오는 패턴
- `robots.txt` → 숨은 디렉터리
- 소스 코드 → 경로 힌트
- 숨김 파일 → 구조 복원
- trailing slash 차이 → 접근 제어 차이
- 정적 파일명 규칙 → 다음 경로 추측

## 5. 실전 체크리스트
- [ ] `/robots.txt` 확인
- [ ] 소스 코드 확인
- [ ] 정적 자원 확인
- [ ] 숨김 파일 가능성 확인
- [ ] trailing slash 테스트
- [ ] 응답 코드 비교
- [ ] 실패 경로도 기록
- [ ] 재사용 가능한 패턴 분리

## 6. 빠른 판별
- `robots.txt`와 경로가 핵심이면 → [[hidden-directory-discovery-ctf-patterns]]
- 로그인 후 요청 추적이면 → [[post-auth-hidden-request-recon-ctf-patterns]]
- 소스 인스펙션이 핵심이면 → [[source-inspection-minification-ctf-patterns]]
- 개념 전체를 묶어 보려면 → [[web-recon-hidden-file-discovery-ctf-hub]]

## 7. 실전에서 자주 놓치는 것
- 경로를 **읽고 끝내는 것**이 아니라 실제 요청까지 해야 합니다.
- 파일명만 바꾸지 말고 **확장자와 슬래시**도 같이 바꿔봅니다.
- 성공 경로뿐 아니라 **실패한 시도**도 기록해야 재사용이 쉽습니다.
- `robots.txt`는 출발점이지 답이 아닙니다.

## 8. 마지막 한 줄
**소스 → robots.txt → 숨은 경로 → 숨김 파일 → 응답 차이** 순서로 보면 대부분의 정찰형 Web CTF는 구조가 보입니다.

## 같이 보면 좋은 페이지
- [[web-recon-hidden-file-discovery-checklist]]
- [[web-recon-hidden-file-discovery-ctf-hub]]
- [[hidden-directory-discovery-ctf-patterns]]
- [[reconnaissance]]
