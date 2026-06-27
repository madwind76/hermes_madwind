---
title: picoCTF 2024 forensics survey
created: 2026-06-22
updated: 2026-06-22
type: query
tags: [ctf, picoctf, forensics, survey, writeup, picoctf2024]
sources: [https://github.com/Cajac/picoCTF-writeups/blob/main/picoCTF_2024/Forensics/README.md, https://github.com/Cajac/picoCTF-writeups/tree/main/picoCTF_2024/Forensics]
confidence: medium
---

# picoCTF 2024 forensics survey

> 결론부터 말씀드리면, **picoCTF 2024 Forensics 문제는 공개 writeup 기준 8개 확인됩니다.**
> 이번 정리는 연도 전체를 바로 훑을 수 있게 만든 뒤, 문제별 leaf writeup으로 내려가도록 구성했습니다.

## 참고 URL
- [picoCTF 2024 Forensics README](https://github.com/Cajac/picoCTF-writeups/blob/main/picoCTF_2024/Forensics/README.md)
- [picoCTF 2024 Forensics directory](https://github.com/Cajac/picoCTF-writeups/tree/main/picoCTF_2024/Forensics)

## 1. 확인 결과
| Challenge | Level | 분류 | 페이지 |
| --- | --- | --- | --- |
| Blast from the past | Medium | 이미지 / 스테고 / 숨은 정보 | [[blast-from-the-past-final-writeup]] |
| CanYouSee | Easy | 이미지 / 스테고 / 숨은 정보 | [[canyousee-final-writeup]] |
| Dear Diary | Medium | 디스크 / 파일시스템 | [[dear-diary-final-writeup]] |
| Mob psycho | Medium | 이미지 / 스테고 / 숨은 정보 | [[mob-psycho-final-writeup]] |
| Scan Surprise | Easy | 이미지 / 스테고 / 숨은 정보 | [[scan-surprise-final-writeup]] |
| Secret of the Polyglot | Easy | 이미지 / 스테고 / 숨은 정보 | [[secret-of-the-polyglot-final-writeup]] |
| Verify | Easy | 디스크 / 파일시스템 | [[verify-final-writeup]] |
| endianness-v2 | Easy | 파일 / 바이트오더 / 이미지 복원 | [[endianness-v2-final-writeup]] |

## 2. 재분류 기준
1. **네트워크 / PCAP** 문제는 패킷 흐름과 스트림 재조립이 핵심입니다.
2. **디스크 / 파일시스템** 문제는 파일 구조, 파티션, 확장자, 무결성 확인이 핵심입니다.
3. **이미지 / 스테고** 문제는 숨은 레이어, 메타데이터, OCR, 파일 내부 단서를 봅니다.
4. **텍스트 / 숨은 문자열** 문제는 문자열 검색, 인코딩 해제, 대용량 로그 탐색으로 접근합니다.

## 3. 세부 카테고리
- [[picoctf-2024-forensics-network-hub]]
- [[picoctf-2024-forensics-stego-hub]]
- [[picoctf-2024-forensics-disk-hub]]
- [[picoctf-2024-forensics-memory-hub]]
- [[picoctf-2024-forensics-windows-hub]]

## 4. 관련 페이지
- [[picoctf-2024-topic-map]]
- [[picoctf-2024-forensics-family-hub]]
- [[forensics-writeup-family-hub]]
