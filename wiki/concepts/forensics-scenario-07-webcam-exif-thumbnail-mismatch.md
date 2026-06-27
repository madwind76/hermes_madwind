---
title: 잠든 웹캠의 EXIF와 썸네일 불일치
created: 2026-06-26
updated: 2026-06-26
type: concept
tags: [ctf, education, forensics, challenge-development, lab, image, exif, thumbnail, antiforensics]
sources: [https://github.com/Cajac/picoCTF-writeups/blob/main/picoCTF_2024/Forensics/README.md, https://github.com/noamgariani11/picoCTF-2025-Writeup/blob/main/README.md]
confidence: medium
---

# 잠든 웹캠의 EXIF와 썸네일 불일치

> 난이도: 초중급
> 소요 시간: 20~30분

## 배경
회의실에서 사용하던 웹캠에서 JPG 한 장이 확보되었습니다. EXIF의 본 이미지 시각(`DateTimeOriginal`)은 **오후 3시**, 그러나 EXIF에 포함된 **임베디드 썸네일의 해상도와 색감**은 다른 시점에 촬영된 모습입니다. 공격자는 본 이미지만 자르고 썸네일은 교체하지 못한 것으로 추정됩니다.

## picoCTF·기존 시나리오 대비 차별점
- picoCTF의 이미지 포렌식([[secret-of-the-polyglot-final-writeup]], `flags are stepic`)은 **데이터 은닉**(LSB/Stepic) 중심.
- 기존 [[forensics-scenario-03-stego-postcard]]도 EXIF 메타데이터를 보지만 **숨은 평문**을 찾는 게 핵심.
- 본 시나리오는 EXIF의 **썸네일과 본 이미지가 일치하지 않는다**는 점에 주목해, **편집 흔적(anti-forensics)** 을 추적합니다.

## 제공 파일
- `webcam_001.jpg` — 본 이미지(1280×720, 약 320KB)
- `embedded_thumb.jpg` — EXIF에서 분리한 썸네일(별도 추출본, 비교용)
- `exif_dump.txt` — `exiftool` 출력 전문
- `case-note.md` — 회의 일정 (참석자 4명, 회의 시간 14:00~16:00)

## 문제 목표
본 이미지와 썸네일이 서로 다른 시각에 만들어졌다는 점을 입증하고, **썸네일 촬영 시점의 회의 참석자 이름**을 플래그로 추출합니다.

## 의도한 풀이 흐름
1. `exiftool webcam_001.jpg` 로 본 이미지의 `DateTimeOriginal`, `Software`, `Make`, `Model`, `ThumbnailOffset`을 확인합니다.
2. `exiftool -b -ThumbnailImage webcam_001.jpg > thumb.jpg` 로 임베디드 썸네일을 분리합니다.
3. `identify` 또는 `exiftool`로 썸네일의 `DateTimeOriginal`을 확인합니다. **본 이미지와 시각이 다름**을 기록합니다.
4. 썸네일 시각이 `case-note.md` 회의 시간 안의 **이전 회의**에 해당함을 추론합니다.
5. `Software`, `Camera Owner Name`, `Artist` 필드를 추가로 확인해 편집 도구 흔적을 추적합니다.
6. 썸네일 EXIF의 `Artist` 또는 `ImageDescription`에 남은 **이전 회의 참석자 이름**을 찾습니다.
7. 이름 + 시각 차이로 답안 문자열을 만듭니다.

## 정답 규칙
- `picoCTF{<attendee>_<delta_minutes>}`
- 예시: `picoCTF{dhkim_120}` (썸네일이 본 이미지보다 120분 먼저 촬영)
- 시각 차이(`delta_minutes`)는 분 단위 정수

## 출제자 노트
- 썸네일 EXIF의 `Artist` 또는 `ImageDescription`을 단서로 두고, 본 이미지 EXIF에서는 `Artist`를 빈 값으로 두세요.
- 본 이미지 EXIF에 **Adobe Lightroom / Photoshop** 흔적을 한 줄 남기면 편집 도구 단서도 함께 보입니다.
- 썸네일 시각 차이는 **90분, 120분**처럼 회의록 단위와 매칭 가능한 값으로 설정합니다.
- 단순히 "시간이 다르다"가 아니라, **다른 회의에 쓰던 이미지를 그대로 썸네일로 둔 상태에서 본 이미지만 잘라 붙였음**이 추론 가능하도록 단서를 배치합니다.

## 트러블슈팅
| 증상 | 원인 | 해결 |
|---|---|---|
| 썸네일 추출이 안 됨 | EXIF에 썸네일 미포함 | `exiftool -b -JpgFromRaw`도 시도 |
| EXIF 시각이 둘 다 동일 | 출제자가 의도한 `delta=0` 외 상황 | `Make`/`Model` 불일치도 단서로 사용 |
| `Software`가 모두 동일 | 편집 흔적이 본 이미지에만 남도록 재설계 | 본 이미지에 `Lightroom`, 썸네일은 `Default`로 분리 |
| 한국어 이름 깨짐 | UTF-8 vs CP949 인코딩 차이 | `exiftool -charset` 옵션 또는 직접 hex dump로 확인 |

## 학습 포인트
- EXIF 메타데이터의 다중 채널(`본 이미지`, `썸네일`, `EXIF IFD`, `GPS IFD`)이 **서로 일관되지 않을 수 있음**을 이해합니다.
- 단순 메타데이터 열람을 넘어, **두 채널의 일관성을 비교**해 편집 흔적을 잡아내는 IR 감각을 기릅니다.
- "데이터 은닉"이 아니라 "**데이터 위장/결합**"이라는 anti-forensics 시각을 처음 접합니다.
