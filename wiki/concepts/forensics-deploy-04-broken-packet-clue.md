---
title: 깨진 패킷 속 단서 배포 노트
created: 2026-06-24
updated: 2026-06-24
type: concept
tags: [ctf, education, forensics, challenge-development, lab]
sources: [https://github.com/kisec/wiki/blob/main/concepts/forensics-scenario-production-plan.md, https://github.com/kisec/wiki/blob/main/concepts/forensics-scenario-deployment-readme.md]
confidence: medium
---

# 깨진 패킷 속 단서 배포 노트

## 참가자용 README
패킷에 흩어진 데이터를 재조립해 원래 파일을 복원하세요.

## 제공 파일
- `capture.pcapng`
- `flows.txt`
- `payload-map.csv`

## 제출 형식
- `picoCTF{<restored_payload>}`

## 출제자 노트
- 정답 payload는 2~4조각이면 충분합니다.
- 정상 트래픽은 1~2개만 섞습니다.
- Wireshark의 stream follow를 쓰게 만듭니다.

## 초기화
- 캡처 파일 재배치
- 흐름 매핑 CSV 복구
- 잡음 트래픽 재삽입
