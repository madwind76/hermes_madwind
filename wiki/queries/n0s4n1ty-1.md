---
title: n0s4n1ty 1
created: 2026-06-13
updated: 2026-06-21
type: query
tags: [ctf, web, file-upload, rce]
sources: [https://github.com/snwau/picoCTF-2025-Writeup/blob/main/Web%20Exploitation/n0s4n1ty%201/n0s4n1ty%201.md, https://medium.com/@pragusga/picoctf-2025-n0s4n1ty-1-file-upload-to-rce-82f458e7706a, https://www.youtube.com/watch?v=duP8S-IqVuQ]
confidence: medium
---

# n0s4n1ty 1

> 이 페이지는 **picoCTF 2025 공개 writeup**을 바탕으로 정리한 학습용 진행 노트입니다.

## 참고 URL
- [Original writeup](https://github.com/snwau/picoCTF-2025-Writeup/blob/main/Web%20Exploitation/n0s4n1ty%201/n0s4n1ty%201.md)
- [medium.com](https://medium.com/@pragusga/picoctf-2025-n0s4n1ty-1-file-upload-to-rce-82f458e7706a)
- [www.youtube.com](https://www.youtube.com/watch?v=duP8S-IqVuQ)


## 1. 요약
- 플랫폼: picoCTF 2025
- 난이도: Easy
- 문제 유형: Web Exploitation
- 핵심 개념: [[file-upload]], [[rce]], [[web-ctf-master-checklist]]
- 현재 상태: 공개 writeup 기반으로 풀이 흐름 정리 완료
- 최종 정리: [[n0s4n1ty-1-final-writeup]]

## 2. 공격면
| Route | Method | Auth | Input | Output | Notes |
|------|------|------|------|------|------|
| /upload.php | POST | No | profile image file | upload path | 업로드 위치가 공개됨 |
| /uploads/<file> | GET | No | filename | file contents / execution | 업로드 파일이 직접 접근 가능 |

## 3. 가설
- 가설 1: 업로드 파일의 확장자 검증이 약합니다.
- 가설 2: PHP 파일이 그대로 실행될 수 있습니다.
- 가설 3: `sudo` 권한을 통해 `/root/flag.txt` 접근이 가능할 수 있습니다.

## 4. 실험 기록
### 시도 1
- payload: `dummy.png`
- 관찰: `uploads/dummy.png` 경로가 응답에 노출됨
- 해석: 업로드 파일이 직접 서빙됩니다.
- 다음 가설: 임의 파일 업로드 및 실행 가능성 확인

### 시도 2
- payload: `webshell.php` with `<?php system($_GET['cmd']); ?>`
- 관찰: `cmd=id` 실행 시 `www-data` 권한이 반환됨
- 해석: 업로드된 PHP가 실행됩니다.
- 다음 가설: `sudo -l`로 권한 확인 후 `/root` 접근 시도

### 시도 3
- payload: `sudo -l`
- 관찰: `www-data`가 `NOPASSWD: ALL`로 보임
- 해석: 임의 명령 실행이 가능합니다.
- 다음 가설: `sudo cat /root/flag.txt` 실행

## 5. 연결된 개념
- [[file-upload-ctf-patterns]]
- [[file-upload-core]]
- [[file-upload-defense]]
- [[rce]]
- [[command-injection]]

## 6. 회고
- 막힌 지점: 업로드 후 실행 확인 전까지는 일반 이미지 업로드처럼 보였습니다.
- 우회 포인트: PHP 확장자 업로드와 공개 디렉토리 실행이 핵심입니다.
- 다음에 먼저 볼 것: 업로드 경로, 실행 여부, sudo 권한
- 재사용 체크리스트:
  - [ ] 업로드 경로가 직접 접근 가능한가
  - [ ] 확장자/ MIME 검증이 우회되는가
  - [ ] 업로드 파일이 실제로 실행되는가
  - [ ] 권한 상승 단서가 있는가
