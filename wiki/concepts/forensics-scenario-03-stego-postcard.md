---
title: 스테가노 우편물
created: 2026-06-24
updated: 2026-06-24
type: concept
tags: [ctf, education, forensics, challenge-development, lab]
sources: [https://github.com/Cajac/picoCTF-writeups/blob/main/picoCTF_2024/Forensics/README.md, https://github.com/Cajac/picoCTF-writeups/blob/main/picoCTF_2025/Forensics/README.md]
confidence: medium
---

# 스테가노 우편물

> 난이도: 초급
> 소요 시간: 15~25분

## 배경
홍보용 사진처럼 보이는 이미지에 메타데이터와 이미지 내부 문자열이 섞여 있습니다.

## 제공 파일
- `postcard.png`
- `caption.txt`
- `metadata.log`

## 문제 목표
사진 속에 숨은 메시지를 찾아 암호문을 원래 문장으로 되돌립니다.

## 의도한 풀이 흐름
1. `exiftool`로 메타데이터를 봅니다.
2. `strings`로 이미지 내부 평문을 확인합니다.
3. `zsteg` 또는 유사 도구로 숨은 문자열을 확인합니다.
4. `caption.txt`의 힌트와 문자열을 결합합니다.
5. base64 또는 단순 치환을 풀어 최종 문장을 얻습니다.

## 정답 규칙
- `picoCTF{<decoded_message>}`
- 예시: `picoCTF{meet_me_at_midnight}`

## 제작 포인트
- 이미지 하나로 해결되게 하되 메타데이터와 숨은 문자열이 서로 보완되도록 합니다.
- 난이도를 낮추려면 base64 1회로 충분하게 만듭니다.
- 난이도를 높이려면 메타데이터 확인 후에만 두 번째 채널이 보이게 합니다.
