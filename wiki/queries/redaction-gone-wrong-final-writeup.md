---
title: Redaction gone wrong — picoCTF 2022 forensics writeup
created: 2026-06-22
updated: 2026-06-22
type: query
tags: [ctf, picoctf, forensics, survey, writeup, picoctf2022]
sources: [https://raw.githubusercontent.com/Cajac/picoCTF-writeups/main/picoCTF_2022/Forensics/Redaction_gone_wrong.md]
confidence: medium
---

# Redaction gone wrong — picoCTF 2022 forensics writeup

## 참고 URL
- [GitHub writeup](https://raw.githubusercontent.com/Cajac/picoCTF-writeups/main/picoCTF_2022/Forensics/Redaction_gone_wrong.md)

## 1. 핵심 요약
Now you DON’T see me. This report has some critical data in it, some of which have been redacted correctly, while some were not.  Can you find an important key that was not redacted properly?

## 2. 풀이 포인트
- 이미지, 문서, 메타데이터, OCR, 숨은 레이어를 확인해 보이지 않는 정보를 찾아냅니다.
- 문제 제목과 설명에서 드러나는 아티팩트 유형부터 먼저 확인한 뒤, 필요한 경우 문자열 검색과 파일 포맷 검사를 병행합니다.

## 3. 같이 보면 좋은 페이지
- [[picoctf-2022-forensics-survey]]
- [[picoctf-2022-forensics-family-hub]]
- [[forensics-writeup-family-hub]]
