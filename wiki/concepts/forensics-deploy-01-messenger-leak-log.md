---
title: 사내 메신저 유출 로그 배포 노트
created: 2026-06-24
updated: 2026-06-24
type: concept
tags: [ctf, education, forensics, challenge-development, lab]
sources: [https://github.com/kisec/wiki/blob/main/concepts/forensics-scenario-production-plan.md, https://github.com/kisec/wiki/blob/main/concepts/forensics-scenario-deployment-readme.md]
confidence: medium
---

# 사내 메신저 유출 로그 배포 노트

## 참가자용 README
사내 메신저 유출과 관련된 Windows 흔적을 조사해, 어떤 계정이 어떤 파일을 유출했는지 찾아주세요.

## 제공 파일
- `Security.evtx`
- `System.evtx`
- `Users.csv`
- `execution-notes.txt`

## 제출 형식
- `picoCTF{<username>_<filename>_<HHMM>}`

## 출제자 노트
- 계정은 3명 이하로 유지합니다.
- 실행 흔적은 1회만 넣습니다.
- 파일명은 메모와 로그가 교차 검증되도록 배치합니다.

## 초기화
- 로그 파일 재생성
- 메모 파일 원복
- 타임스탬프 재배치
