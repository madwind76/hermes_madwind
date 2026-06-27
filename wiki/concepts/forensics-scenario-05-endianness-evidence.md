---
title: 엔디언이 뒤집힌 증거물
created: 2026-06-24
updated: 2026-06-24
type: concept
tags: [ctf, education, forensics, challenge-development, lab]
sources: [https://github.com/Cajac/picoCTF-writeups/blob/main/picoCTF_2024/Forensics/README.md, https://github.com/Cajac/picoCTF-writeups/blob/main/picoCTF_2025/Forensics/README.md]
confidence: medium
---

# 엔디언이 뒤집힌 증거물

> 난이도: 초급~초중급
> 소요 시간: 15~25분

## 배경
증거물의 데이터가 깨진 것이 아니라, 바이트 순서가 반대로 저장되어 있어 정상적으로 읽히지 않습니다.

## 제공 파일
- `artifact.bin`
- `hex-dump.txt`
- `notes.txt`

## 문제 목표
파일 안에 들어 있는 메시지를 올바른 바이트 순서로 복원합니다.

## 의도한 풀이 흐름
1. `hex-dump.txt`에서 16진수 덩어리를 확인합니다.
2. 2바이트 또는 4바이트 단위로 뒤집어 봅니다.
3. little-endian / big-endian 가정을 바꿔가며 문자열을 복원합니다.
4. ASCII 또는 UTF-8로 읽히는지 확인합니다.
5. 최종 문자열을 플래그 형식으로 제출합니다.

## 정답 규칙
- `picoCTF{<recovered_text>}`
- 예시: `picoCTF{endianness_matters}`

## 제작 포인트
- 바이트 오더 반전만 핵심으로 두고 압축이나 암호화는 넣지 않는 편이 좋습니다.
- 초급 문제는 2바이트 반전만 사용하면 됩니다.
- 초중급으로 올리려면 헤더 일부만 정상이고 나머지가 뒤집히도록 설계합니다.
