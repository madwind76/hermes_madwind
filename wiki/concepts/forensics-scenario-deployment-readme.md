---
title: 초중급용 포렌식 문제 배포용 README / 출제자 노트
created: 2026-06-24
updated: 2026-06-24
type: concept
tags: [ctf, education, forensics, challenge-development, lab]
sources: [https://github.com/Cajac/picoCTF-writeups/blob/main/picoCTF_2024/Forensics/README.md, https://github.com/Cajac/picoCTF-writeups/blob/main/picoCTF_2025/Forensics/README.md, https://github.com/kisec/wiki/blob/main/concepts/forensics-scenario-production-plan.md]
confidence: medium
---

# 초중급용 포렌식 문제 배포용 README / 출제자 노트

## 개요
이 문서는 `forensics-scenario-production-plan`의 5개 시나리오를 실제 배포 폴더 구조와 운영 체크리스트로 바꾼 **허브 문서**입니다.

## 공통 배포 규칙
1. 각 문제는 독립 폴더로 분리합니다.
2. 참가자에게는 README와 문제 파일만 노출합니다.
3. 운영자용 정답 생성 규칙은 별도 `INSTRUCTOR.md` 또는 `answer.txt`로 분리합니다.
4. `start.sh / stop.sh / reset.sh`를 함께 둡니다.
5. 재배포 전에는 `reset.sh`로 깨끗한 상태를 확인합니다.

## 권장 폴더 구조
```text
forensics-challenge-pack/
├── 01-messenger-leak-log/
│   ├── challenge/
│   ├── start.sh
│   ├── stop.sh
│   ├── reset.sh
│   ├── README.md
│   └── INSTRUCTOR.md
├── 02-locked-laptop-secret-memo/
├── 03-stego-postcard/
├── 04-broken-packet-clue/
└── 05-endianness-evidence/
```

## 시나리오별 배포 노트
- [[forensics-deploy-01-messenger-leak-log]]
- [[forensics-deploy-02-locked-laptop-secret-memo]]
- [[forensics-deploy-03-stego-postcard]]
- [[forensics-deploy-04-broken-packet-clue]]
- [[forensics-deploy-05-endianness-evidence]]

## 관련 페이지
- [[forensics-scenario-production-plan]]
- [[forensics-beginner-intermediate-scenarios]]
- [[forensics-writeup-family-hub]]
