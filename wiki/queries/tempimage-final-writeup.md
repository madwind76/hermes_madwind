---
title: Tempimage — Hacker101 CTF writeup
created: 2026-06-19
updated: 2026-06-19
type: query
tags: [ctf, web, writeup, file-upload, path-traversal, unrestricted-upload, rce]
sources: [https://raw.githubusercontent.com/Yahyahcini/hacker101-ctf-writeups/main/Tempimage/README.md]
confidence: high
---

# Tempimage — Hacker101 CTF writeup

> 업로드 파일명 조작으로 경로를 탈출하고, PNG 검사만 통과시키는 구조를 이용해 웹셸까지 올리는 file upload writeup입니다.

## 참고 URL
- [raw source](https://raw.githubusercontent.com/Yahyahcini/hacker101-ctf-writeups/main/Tempimage/README.md)


## 1. 한 줄 요약
- 업로드된 파일은 `/files/` 아래에 저장됩니다.
- `filename` 값이 `move_uploaded_file()`로 그대로 전달됩니다.
- 경로 탈출 후 PHP가 실행되는 위치에 파일을 두면 RCE로 이어집니다.

## 2. 문제 구조
| 항목 | 내용 |
|---|---|
| 플랫폼 | Hacker101 CTF |
| 난이도 | Moderate |
| 핵심 아이디어 | path traversal, unrestricted upload, PHP webshell |
| 관련 개념 | [[file-upload-ctf-patterns]], [[path-traversal-ctf-patterns]], [[web-ctf-writeup-storage-upload]] |
| 관련 survey | [[hacker101-web-writeup-survey]] |

## 3. 공격면 정리
1. `doUpload.php` 요청을 Burp로 가로챕니다.
2. `filename=../test.png`로 동작을 확인합니다.
3. `filename=/../../shell.php`처럼 경로를 탈출합니다.
4. PNG 본문 뒤에 PHP webshell을 섞어 업로드합니다.

## 4. 풀이 흐름
```text
# 1) traversal 테스트
filename: ../test.png
# 예상 결과: 서버 경로 구조가 드러나는 오류 또는 반응을 확인합니다.

# 2) 경로 탈출 payload
filename: /../../shell.php
# 예상 결과: /files/ 밖 또는 실행 가능한 위치로 저장됩니다.

# 3) 업로드된 shell 호출
/shell.php?command=ls
# 예상 결과: 파일 목록이 응답으로 돌아옵니다.
```

## 5. 왜 취약한가
- 파일 이름 검증이 없습니다.
- 파일 확장자와 magic bytes만 확인하고 내용을 충분히 검사하지 않습니다.
- 업로드 후 실행 위치와 저장 위치가 분리되지 않았습니다.

## 6. 방어 관점
- 파일명은 서버가 새로 생성합니다.
- 업로드 경로는 고정하고, 확장자만 믿지 않습니다.
- 실행 가능한 디렉터리에 사용자 업로드 파일을 두지 않습니다.

## 7. 다음 연결
- [[hacker101-web-writeup-survey]]
- [[file-upload-ctf-patterns]]
- [[path-traversal-ctf-patterns]]
- [[web-ctf-writeup-storage-upload]]
