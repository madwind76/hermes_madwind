---
title: Forbidden Paths — picoCTF 2022 LFI writeup
created: 2026-06-19
updated: 2026-06-21
type: query
tags: [ctf, web, lfi, path-traversal, directory-traversal, file-read]
sources: [https://medium.com/@ahmednarmer1/ctf-day-38-89735a37ed5f, https://hackmd.io/@fearnot/picoCTF_Web]
confidence: high
---

# Forbidden Paths — picoCTF 2022 LFI writeup

> 파일명 입력 폼으로 `../../../../flag.txt`를 입력하면 접근 제한 없이 flag 파일을 읽을 수 있습니다.

## 참고 URL
- [medium.com](https://medium.com/@ahmednarmer1/ctf-day-38-89735a37ed5f)
- [hackmd.io](https://hackmd.io/@fearnot/picoCTF_Web)


## 1. 한 줄 요약
- 웹에서 파일명을 입력받아 `/usr/share/nginx/html/` 아래에서 읽습니다.
- 입력 필터가 없으므로 `../`로 상위 디렉토리로 이동할 수 있습니다.
- `../../../../flag.txt`를 입력하면 flag를 읽습니다.

## 2. 취약점 흐름
| 단계 | 관찰 | 의미 |
|------|------|------|
| 1 | 파일명 입력 폼 존재 | 서버가 파일을 읽어 표시 |
| 2 | 예시에 `.txt` 파일명 힌트 | path traversal 가능성 |
| 3 | `../../../../flag.txt` 입력 | flag 파일 접근 성공 |

## 3. 핵심 payload
```
../../../../flag.txt
```

## 4. 연결된 개념
- [[lfi-rfi]]
- [[lfi-rfi-core]]
- [[file-upload-path-traversal-writeup-survey]]
- [[web-ctf-writeup-family-hub]]

## 5. 참고 소스
- [Ahmed Narmer — CTF Day 38](https://medium.com/@ahmednarmer1/ctf-day-38-89735a37ed5f)
