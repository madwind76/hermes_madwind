---
title: 잠긴 노트북의 비밀 메모
created: 2026-06-24
updated: 2026-06-24
type: concept
tags: [ctf, education, forensics, challenge-development, lab]
sources: [https://github.com/Cajac/picoCTF-writeups/blob/main/picoCTF_2024/Forensics/README.md, https://github.com/Cajac/picoCTF-writeups/blob/main/picoCTF_2025/Forensics/README.md]
confidence: medium
---

# 잠긴 노트북의 비밀 메모

> 난이도: 초중급
> 소요 시간: 25~35분

## 배경
회수된 노트북의 디스크는 암호화되어 있지만, 메모 파일과 메모리 덤프 일부가 함께 확보되었습니다.

## 제공 파일
- `disk.dd`
- `memory.raw`
- `notes.txt`
- `recovery-hint.png`

## 문제 목표
암호화된 노트북 내부에서 남겨진 단서를 모아, 사용자가 마지막으로 적어 둔 비밀 문자열을 복원합니다.

## 의도한 풀이 흐름
1. `notes.txt`에서 날짜와 키워드를 확인합니다.
2. `memory.raw`에서 `strings` 또는 메모리 분석으로 단서를 찾습니다.
3. `disk.dd`에서 파티션과 파일시스템 흔적을 식별합니다.
4. `recovery-hint.png`의 메타데이터 또는 숨은 문자열을 확인합니다.
5. 2~3개의 단서를 합쳐 최종 문자열을 얻습니다.

## 정답 규칙
- `picoCTF{<recovery_phrase>}`
- 예시: `picoCTF{stolen_keys_live_here}`

## 제작 포인트
- BitLocker를 직접 깨는 문제보다 단서 수집형으로 설계합니다.
- 메모리 덤프는 작게 유지하고, `strings`로 의미 있는 문구가 나오게 합니다.
- 디스크 이미지에는 파일 흔적 확인이 핵심이 되게 구성합니다.
