---
title: 스테가노 우편물 배포 노트
created: 2026-06-24
updated: 2026-06-24
type: concept
tags: [ctf, education, forensics, challenge-development, lab]
sources: [https://github.com/kisec/wiki/blob/main/concepts/forensics-scenario-production-plan.md, https://github.com/kisec/wiki/blob/main/concepts/forensics-scenario-deployment-readme.md]
confidence: medium
---

# 스테가노 우편물 배포 노트

## 참가자용 README
우편 엽서처럼 보이는 이미지에 숨은 메시지를 찾아 복원하세요.

## 제공 파일
- `postcard.png`
- `caption.txt`
- `metadata.log`

## 제출 형식
- `picoCTF{<decoded_message>}`

## 출제자 노트
- base64 1회 또는 단순 치환 1회로 끝나게 만듭니다.
- 가짜 문자열은 1개만 섞습니다.
- 메타데이터를 놓쳐도 strings가 보조 단서가 되어야 합니다.

## 초기화
- 이미지 메타데이터 복원
- 숨은 문자열 재삽입
- 캡션 파일 원복
