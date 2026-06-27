---
title: 엔디언이 뒤집힌 증거물 배포 노트
created: 2026-06-24
updated: 2026-06-24
type: concept
tags: [ctf, education, forensics, challenge-development, lab]
sources: [https://github.com/kisec/wiki/blob/main/concepts/forensics-scenario-production-plan.md, https://github.com/kisec/wiki/blob/main/concepts/forensics-scenario-deployment-readme.md]
confidence: medium
---

# 엔디언이 뒤집힌 증거물 배포 노트

## 참가자용 README
바이트 순서가 뒤집힌 증거물에서 메시지를 복원하세요.

## 제공 파일
- `artifact.bin`
- `hex-dump.txt`
- `notes.txt`

## 제출 형식
- `picoCTF{<recovered_text>}`

## 출제자 노트
- 압축/암호화보다 byte swap이 핵심입니다.
- 2바이트 단위가 기본이고, 확장 시 4바이트 단위를 추가합니다.
- 일부만 뒤집어 적당한 혼동을 줍니다.

## 초기화
- 바이너리 원본 재생성
- 헥스 덤프 원복
- 단서 노트 재삽입
