---
title: File Upload CTF Template
created: 2026-06-13
updated: 2026-06-21
type: query
tags: [ctf, web, file-upload]
sources: [https://medium.com/cyberx/ctf-hacker101-tempimage-27f397893408, https://www.snyk.io/blog/fetch-the-flag-ctf-2022-writeup-file-explorer/, https://github.com/snwau/picoCTF-2025-Writeup/blob/main/Web%20Exploitation/n0s4n1ty%201/n0s4n1ty%201.md, https://medium.com/@pragusga/picoctf-2025-n0s4n1ty-1-file-upload-to-rce-82f458e7706a]
confidence: medium
---

# File Upload CTF Template

## 참고 URL
- [medium.com](https://medium.com/cyberx/ctf-hacker101-tempimage-27f397893408)
- [www.snyk.io](https://www.snyk.io/blog/fetch-the-flag-ctf-2022-writeup-file-explorer/)
- [Original writeup](https://github.com/snwau/picoCTF-2025-Writeup/blob/main/Web%20Exploitation/n0s4n1ty%201/n0s4n1ty%201.md)
- [medium.com](https://medium.com/@pragusga/picoctf-2025-n0s4n1ty-1-file-upload-to-rce-82f458e7706a)


## 1. 요약
- 플랫폼:
- 문제명:
- URL:
- 목표:
- 현재 상태:

## 2. 입력점
| Route | Method | Auth | Input | Output | Notes |
|------|------|------|------|------|------|
| | | | file / avatar / attachment / image | | 업로드 후보 |

## 3. 가설
- 가설 1: 확장자 또는 MIME 검증이 취약하다.
- 가설 2: 저장 경로 또는 접근 URL이 예측 가능하다.
- 가설 3: 업로드 후 실행 경로가 존재한다.

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
- [[file-upload]]
- [[file-upload-core]]
- [[file-upload-defense]]
- [[path-traversal]]
- [[rce]]

## 6. 회고
- 막힌 지점:
- 우회 포인트:
- 다음에 먼저 볼 것:
- 재사용 체크리스트:
  - [ ] 확장자 검증 확인
  - [ ] MIME / 매직바이트 확인
  - [ ] 저장 경로 및 실행 여부 확인
