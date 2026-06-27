---
title: 잠긴 노트북의 비밀 메모 배포 노트
created: 2026-06-24
updated: 2026-06-24
type: concept
tags: [ctf, education, forensics, challenge-development, lab]
sources: [https://github.com/kisec/wiki/blob/main/concepts/forensics-scenario-production-plan.md, https://github.com/kisec/wiki/blob/main/concepts/forensics-scenario-deployment-readme.md]
confidence: medium
---

# 잠긴 노트북의 비밀 메모 배포 노트

## 참가자용 README
잠긴 노트북에서 남겨진 단서를 찾아 비밀 문자열을 복원하세요.

## 제공 파일
- `disk.dd`
- `memory.raw`
- `notes.txt`
- `recovery-hint.png`

## 제출 형식
- `picoCTF{<recovery_phrase>}`

## 출제자 노트
- 암호화 해제 자체를 목표로 하지 않습니다.
- 메모리와 이미지 중 최소 1개는 반드시 해석이 필요합니다.
- 단서는 2~3개만 배치합니다.

## 초기화
- 디스크 이미지 원복
- 메모리 덤프 재생성
- 이미지 메타데이터 초기화
