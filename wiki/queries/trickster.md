---
title: Trickster
created: 2026-06-14
updated: 2026-06-21
type: query
tags: [ctf, web, research, writeup, file-upload, upload-bypass]
sources: [https://github.com/noamgariani11/picoCTF-2024-Writeup/blob/main/Web%20Exploitation/Trickster.md, https://medium.com/@niceselol/picoctf-2024-trickster-af90f7476e18, https://dev.to/yowise/trickster-picoctf-2024-1j5j, https://brandon-t-elliott.github.io/trickster]
confidence: high
---

# Trickster

> PNG-only 업로드 제한을 **magic bytes**, **더블 확장자**, **웹 실행 가능 업로드 경로**로 우회하는 picoCTF 2024 Web Exploitation 문제입니다.

## 참고 URL
- [Original writeup](https://github.com/noamgariani11/picoCTF-2024-Writeup/blob/main/Web%20Exploitation/Trickster.md)
- [medium.com](https://medium.com/@niceselol/picoctf-2024-trickster-af90f7476e18)
- [dev.to](https://dev.to/yowise/trickster-picoctf-2024-1j5j)
- [brandon-t-elliott.github.io](https://brandon-t-elliott.github.io/trickster)


## 1. 요약
- 플랫폼: picoCTF 2024
- 문제명: Trickster
- 유형: Web Exploitation
- 핵심 아이디어: 업로드 검증이 느슨해 `PNG` 헤더와 `.png.php` 꼼수로 PHP payload를 올릴 수 있습니다.
- 연결 개념: [[file-upload-ctf-patterns]], [[file-upload]], [[web-ctf-writeup-storage-upload]], [[web-inspector-ctf-patterns]]
- 현재 상태: 공개 writeup 4개를 교차 확인해 풀이 흐름을 정리했습니다.

## 2. 공격면
| Route / Resource | Method | Auth | Input | Output | Notes |
|------|------|------|------|------|------|
| `/` | GET | No | navigation | upload form | PNG만 받는다고 안내합니다 |
| `/robots.txt` | GET | No | browser | hidden paths | `/instructions.txt`를 찾는 단서입니다 |
| `/instructions.txt` | GET | No | browser | upload rules | PNG signature 조건을 알려줍니다 |
| `/uploads/` | GET | No | uploaded file | web shell / preview | 업로드된 파일이 웹에서 접근됩니다 |

## 3. 가설
- 파일 확장자 검사만 한다면 `.png.php` 같은 이름이 통과할 수 있습니다.
- 파일 내용은 전체 PNG가 아니어도 **앞부분 magic bytes**만 확인할 수 있습니다.
- 업로드된 파일이 웹 실행 가능한 위치에 저장되면 RCE로 이어질 수 있습니다.

## 4. 실험 기록
### 시도 1
- payload: 디렉터리 열거
- 관찰: `robots.txt`, `uploads`, `instructions.txt` 같은 숨은 경로가 보일 수 있습니다.
- 해석: 업로드 규칙과 저장 위치를 먼저 확인해야 합니다.

### 시도 2
- payload: `instructions.txt` 확인
- 관찰: PNG 파일 형식과 시작 바이트 조건이 드러납니다.
- 해석: 실제 판정은 확장자와 magic bytes의 느슨한 조합일 가능성이 큽니다.

### 시도 3
- payload: PNG 헤더를 붙인 PHP payload 업로드
- 관찰: `.png.php` 형태의 파일이 저장됩니다.
- 해석: 단순 파일 검사가 우회되었습니다.

### 시도 4
- payload: 업로드된 파일 직접 접근
- 관찰: 웹에서 접근 가능한 경우 명령 실행 인터페이스가 됩니다.
- 해석: 웹 루트에 저장된 업로드 파일이 실행 가능했습니다.

### 시도 5
- payload: 상위 디렉터리 탐색 후 `.txt` 파일 확인
- 관찰: 플래그가 들어있는 텍스트 파일을 찾을 수 있습니다.
- 해석: 업로드 위치에서 웹 루트까지 올라가면 flag 회수가 가능합니다.

## 5. 연결된 개념
- [[file-upload-ctf-patterns]]
- [[file-upload]]
- [[web-ctf-writeup-storage-upload]]
- [[web-ctf-writeup-topic-map]]
- [[web-ctf-master-checklist]]

## 6. 회고
- 단순한 이미지 업로드처럼 보여도 저장 경로와 실행 권한이 핵심입니다.
- 파일명 검사만 믿으면 `.png.php` 같은 더블 확장자가 통과할 수 있습니다.
- 다음에 먼저 볼 것: `robots.txt`, `instructions.txt`, 업로드 위치, 실행 권한, magic bytes.
