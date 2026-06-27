---
title: LFI / Path traversal writeup survey
created: 2026-06-19
updated: 2026-06-21
type: query
tags: [ctf, web, survey, writeup, lfi, path-traversal, directory-traversal, file-read, lfi-rfi]
sources: [https://medium.com/@ahmednarmer1/ctf-day-38-89735a37ed5f, https://github.com/Yahyahcini/hacker101-ctf-writeups, https://github.com/orangetw/My-CTF-Web-Challenges, https://blog.kaibro.tw/2018/10/24/HITCON-CTF-2018-Web/, https://hacktricks.wiki/en/pentesting-web/file-inclusion/via-php_session_upload_progress.html]
confidence: high
---

# LFI / Path traversal writeup survey

## 참고 URL
- [medium.com](https://medium.com/@ahmednarmer1/ctf-day-38-89735a37ed5f)
- [Yahyahcini/hacker101-ctf-writeups](https://github.com/Yahyahcini/hacker101-ctf-writeups)
- [orangetw/My-CTF-Web-Challenges](https://github.com/orangetw/My-CTF-Web-Challenges)
- [blog.kaibro.tw](https://blog.kaibro.tw/2018/10/24/HITCON-CTF-2018-Web/)
- [hacktricks.wiki](https://hacktricks.wiki/en/pentesting-web/file-inclusion/via-php_session_upload_progress.html)


## 1. 목적
파일 경로 조작을 통해 서버 파일을 읽는 writeup을 비교합니다.

## 2. 비교 대상

| 문제 | 주된 primitive | 보조 primitive | 한 줄 요약 |
|---|---|---|---|
| Forbidden Paths | absolute/relative path traversal | directory climbing | `../../../../flag.txt`로 웹루트 밖 파일을 읽습니다. |
| Photo Gallery | SQLi → command injection | source leak | SQLi로 소스를 읽고, 경로 조작이 포함된 복합 공격입니다. |
| One Line PHP Challenge | PHP wrapper + session.upload_progress | file inclusion | 업로드/세션 파일을 포함해 LFI에서 RCE로 이어집니다. |

## 3. 공통 관찰
1. path traversal은 입력 검증이 없으면 `../`로 어떤 디렉토리든 접근 가능합니다.
2. 단순 traversal은 필터가 없으면 매우 빠르게 풀립니다.
3. file upload + path traversal 체인은 더 복합적인 공격으로 이어집니다.
4. PHP wrapper, session 파일, include 경로가 보이면 LFI/RFI로 범위를 넓혀야 합니다.

## 4. 관련 개념
- [[lfi-rfi]]
- [[lfi-rfi-core]]
- [[file-upload-path-traversal-writeup-survey]]
- [[web-ctf-writeup-family-hub]]
- [[forbidden-paths-final-writeup]]
- [[photo-gallery-final-writeup]]
- [[one-line-php-challenge-final-writeup]]

## 5. 다음 읽을 거리
- [[forbidden-paths-final-writeup]]
- [[photo-gallery-final-writeup]]
- [[one-line-php-challenge-final-writeup]]
