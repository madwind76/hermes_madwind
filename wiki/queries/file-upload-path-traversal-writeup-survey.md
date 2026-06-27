---
title: File upload and path traversal writeup survey
created: 2026-06-19
updated: 2026-06-21
type: query
tags: [ctf, web, survey, writeup, file-upload, path-traversal, unrestricted-upload, rce, lfi-rfi]
sources: [https://medium.com/cyberx/ctf-hacker101-tempimage-27f397893408, https://www.snyk.io/blog/fetch-the-flag-ctf-2022-writeup-file-explorer/, https://github.com/snwau/picoCTF-2025-Writeup/blob/main/Web%20Exploitation/n0s4n1ty%201/n0s4n1ty%201.md, https://medium.com/@pragusga/picoctf-2025-n0s4n1ty-1-file-upload-to-rce-82f458e7706a, https://medium.com/@inferiorak/n0s4n1ty-1-web-exploitation-picoctf-2025-edcde6045088, https://github.com/orangetw/My-CTF-Web-Challenges, https://blog.kaibro.tw/2018/10/24/HITCON-CTF-2018-Web/, https://hacktricks.wiki/en/pentesting-web/file-inclusion/via-php_session_upload_progress.html]
confidence: high
---

# File upload and path traversal writeup survey

## 참고 URL
- [medium.com](https://medium.com/cyberx/ctf-hacker101-tempimage-27f397893408)
- [www.snyk.io](https://www.snyk.io/blog/fetch-the-flag-ctf-2022-writeup-file-explorer/)
- [Original writeup](https://github.com/snwau/picoCTF-2025-Writeup/blob/main/Web%20Exploitation/n0s4n1ty%201/n0s4n1ty%201.md)
- [medium.com](https://medium.com/@pragusga/picoctf-2025-n0s4n1ty-1-file-upload-to-rce-82f458e7706a)
- [medium.com](https://medium.com/@inferiorak/n0s4n1ty-1-web-exploitation-picoctf-2025-edcde6045088)
- [orangetw/My-CTF-Web-Challenges](https://github.com/orangetw/My-CTF-Web-Challenges)
- [blog.kaibro.tw](https://blog.kaibro.tw/2018/10/24/HITCON-CTF-2018-Web/)
- [hacktricks.wiki](https://hacktricks.wiki/en/pentesting-web/file-inclusion/via-php_session_upload_progress.html)


## 1. 목적
파일 업로드와 경로 순회가 결합될 때 어떻게 storage escape, file read, RCE로 이어지는지 비교합니다.

## 2. 비교 대상

| 문제 | 주된 primitive | 보조 primitive | 한 줄 요약 |
|---|---|---|---|
| Tempimage | path traversal | unrestricted upload | 파일명 조작으로 저장 경로를 탈출하고 PHP webshell로 확장합니다. |
| File Explorer | directory traversal | static file serving | URL-encoded traversal로 `/public/` 밖의 flag를 읽습니다. |
| n0s4n1ty 1 | file upload to RCE | privilege escalation | 업로드한 PHP 파일이 실행되고 sudo 권한 확인까지 이어집니다. |
| One Line PHP Challenge | PHP wrapper + session.upload_progress | file inclusion | 업로드/세션 파일을 포함해 RCE로 이어지는 전형적인 LFI/RFI 계열입니다. |

## 3. 공통 관찰
1. 사용자가 준 파일명이나 경로를 서버가 그대로 믿으면 위험합니다.
2. 업로드/서빙 경로가 분리되지 않으면, traversal 한 번으로 실행 경로나 비밀 파일에 닿을 수 있습니다.
3. MIME type, extension, magic bytes만 보는 검증은 자주 우회됩니다.
4. PHP wrapper나 session 관련 내부 파일이 보이면 단순 저장 문제가 아니라 file inclusion으로 확장될 수 있습니다.

## 4. 사례별 메모

### 1) Tempimage
- `filename`이 `move_uploaded_file()`로 흘러들어가 경로 탈출이 가능합니다.
- 파일명 조작 + PHP webshell 결합이 핵심입니다.

### 2) File Explorer
- 정적 파일 서버에서 URL-encoded traversal이 필터를 우회합니다.
- 디코딩 후 검사하지 않으면 상위 디렉터리에 도달할 수 있습니다.

### 3) n0s4n1ty 1
- 업로드된 PHP 파일이 실제로 실행되므로 단순 저장 검증만으로는 부족합니다.
- 업로드 후 `sudo -l`까지 이어지는 권한 상승 관찰이 중요합니다.

### 4) One Line PHP Challenge
- PHP wrapper와 session.upload_progress가 포함 경로가 됩니다.
- 파일 업로드 자체보다 **파일 포함 가능성**을 먼저 의심해야 합니다.

## 5. 관련 개념
- [[file-upload-ctf-patterns]]
- [[path-traversal-ctf-patterns]]
- [[lfi-rfi]]
- [[web-ctf-writeup-storage-upload]]
- [[web-ctf-writeup-family-hub]]
- [[tempimage-final-writeup]]
- [[file-explorer-final-writeup]]
- [[n0s4n1ty-1-final-writeup]]
- [[one-line-php-challenge-final-writeup]]

## 6. 다음 읽을 거리
- [[tempimage-final-writeup]]
- [[file-explorer-final-writeup]]
- [[n0s4n1ty-1-final-writeup]]
- [[one-line-php-challenge-final-writeup]]
