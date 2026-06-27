---
title: 사내 메신저 유출 로그
created: 2026-06-24
updated: 2026-06-24
type: concept
tags: [ctf, education, forensics, challenge-development, lab]
sources: [https://github.com/Cajac/picoCTF-writeups/blob/main/picoCTF_2024/Forensics/README.md, https://github.com/Cajac/picoCTF-writeups/blob/main/picoCTF_2025/Forensics/README.md]
confidence: medium
---

# 사내 메신저 유출 로그

> 난이도: 초급
> 소요 시간: 15~20분

## 배경
사내 업무 PC에서 수상한 파일 실행과 USB 연결이 있었고, 이후 메신저를 통해 외부로 파일이 유출된 정황이 발견되었습니다.

## 제공 파일
- `Security.evtx`
- `System.evtx`
- `Users.csv`
- `execution-notes.txt`

## 문제 목표
어떤 계정이 가장 먼저 수상한 행동을 했는지, 그리고 어떤 파일이 외부로 빠져나갔는지 확인합니다.

## 의도한 풀이 흐름
1. `Security.evtx`에서 로그인 실패/성공 이벤트를 확인합니다.
2. `System.evtx`에서 USB 연결과 프로세스 생성 시각을 확인합니다.
3. `execution-notes.txt`에서 의심 파일명과 계정명을 대조합니다.
4. 파일명, 계정명, 시각을 합쳐 플래그를 만듭니다.

## 정답 규칙
- `picoCTF{<username>_<filename>_<HHMM>}`
- 예시: `picoCTF{jlee_payroll.xlsx_0934}`

## 제작 포인트
- 이벤트 ID는 8~12개만 남깁니다.
- 계정명은 2~3개만 등장시키면 적당합니다.
- 정상 업무 이벤트와 섞어 타임라인을 읽게 만듭니다.
