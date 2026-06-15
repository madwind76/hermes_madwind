---
title: One Line PHP Challenge
created: 2026-06-13
updated: 2026-06-16
type: query
tags: [ctf, web, research]
sources: [https://github.com/orangetw/My-CTF-Web-Challenges, https://blog.kaibro.tw/2018/10/24/HITCON-CTF-2018-Web/, https://hacktricks.wiki/en/pentesting-web/file-inclusion/via-php_session_upload_progress.html]
confidence: medium
---

# One Line PHP Challenge

> 이 페이지는 **HITCON CTF 2018 One Line PHP Challenge 공개 writeup**을 바탕으로 정리한 학습용 진행 노트입니다.

## 1. 요약
- 플랫폼: HITCON CTF 2018
- 점수 / 난이도: web challenge
- 문제 유형: php / lfi
- 핵심 개념: [[lfi-rfi]], [[path-traversal-ctf-patterns]], [[web-ctf-master-checklist]]
- 현재 상태: 공개 writeup 기반으로 풀이 흐름 정리 완료

## 2. 공격면
| Route / Service | Method | Auth | Input | Output | Notes |
|------|------|------|------|------|------|
| upload form | POST | No | filename | processed file | PHP 파일 처리 포인트 |
| wrapper path | GET | No | php:// / phar:// | file contents | wrapper abuse 가능 |
| session progress | POST | No | upload progress | temporary session file | LFI bait |

## 3. 가설
- 단순 파일 읽기처럼 보여도 PHP wrapper가 핵심입니다.
- session upload progress 파일을 포함할 수 있으면 RCE가 가능합니다.
- 공격은 파일 업로드와 포함 경로를 동시에 엮어야 합니다.

## 4. 실험 기록
### 시도 1
- payload: file upload review
- 관찰: 파일명과 처리 로직을 봅니다.
- 해석: 리소스 경로가 노출되는지 확인합니다.
### 시도 2
- payload: wrapper probing
- 관찰: php://와 phar://를 시험합니다.
- 해석: 로컬 파일 포함 가능성을 찾습니다.
### 시도 3
- payload: session progress abuse
- 관찰: session 저장 경로를 포함합니다.
- 해석: 코드 실행으로 이어지는지 확인합니다.

## 5. 연결된 개념
- [[lfi-rfi]]
- [[path-traversal-ctf-patterns]]
- [[web-ctf-master-checklist]]

## 6. 회고
- 막힌 지점: 파일 확장자보다 wrapper와 session 파일이 중요했습니다.
- 우회 포인트: LFI → PHP wrapper → deserialization/RCE 경로입니다.
- 다음에 먼저 볼 것: 업로드 처리와 내부 임시 파일 경로입니다.
