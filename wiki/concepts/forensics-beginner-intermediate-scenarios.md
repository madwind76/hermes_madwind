---
title: 초중급용 포렌식 문제 시나리오 10선
created: 2026-06-24
updated: 2026-06-26
type: concept
tags: [ctf, education, forensics, challenge-development, lab]
sources: [https://github.com/Cajac/picoCTF-writeups/blob/main/picoCTF_2024/Forensics/README.md, https://github.com/Cajac/picoCTF-writeups/blob/main/picoCTF_2025/Forensics/README.md, https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-event-reference.html, https://learn.microsoft.com/en-us/windows/win32/fileio/change-journals]
confidence: medium
---

# 초중급용 포렌식 문제 시나리오 10선

## 개요
위키의 포렌식 패턴을 바탕으로 만든 초중급용 CTF 시나리오 허브입니다. **시리즈 1(1~5)** 은 picoCTF 패턴과 겹치지 않는 현실적 IR 입문 시나리오, **시리즈 2(6~10)** 은 picoCTF/기존 시나리오가 다루지 않은 파일시스템·이미지 메타·아카이브·메모리 인코딩·클라우드 로그 패턴을 추가한 확장 시나리오입니다.

## 사용 방법
1. 아래 10개 시나리오 중 하나를 고릅니다.
2. 각 시나리오 페이지에서 파일 구성과 풀이 흐름을 확인합니다.
3. 필요하면 `forensics-writeup-family-hub`와 연결해 실제 패턴으로 치환합니다.

## 시나리오 목록 — 시리즈 1 (1~5)
| # | 시나리오 | 난이도 | 링크 |
|---|---|---|---|
| 1 | 사내 메신저 유출 로그 | 초급 | [[forensics-scenario-01-messenger-leak-log]] |
| 2 | 잠긴 노트북의 비밀 메모 | 초중급 | [[forensics-scenario-02-locked-laptop-secret-memo]] |
| 3 | 스테가노 우편물 | 초급 | [[forensics-scenario-03-stego-postcard]] |
| 4 | 깨진 패킷 속 단서 | 초중급 | [[forensics-scenario-04-broken-packet-clue]] |
| 5 | 엔디언이 뒤집힌 증거물 | 초급~초중급 | [[forensics-scenario-05-endianness-evidence]] |

## 시나리오 목록 — 시리즈 2 (6~10, 신규)
| # | 시나리오 | 난이도 | 링크 | picoCTF와 차별점 |
|---|---|---|---|---|
| 6 | 외장 드라이브 흔적 (NTFS MFT·USN Journal) | 초중급 | [[forensics-scenario-06-ntfs-mft-usn-trail]] | NTFS `$MFT`+`$UsnJrnl` 메타 분석은 picoCTF에 없음 |
| 7 | 잠든 웹캠의 EXIF와 썸네일 불일치 | 초중급 | [[forensics-scenario-07-webcam-exif-thumbnail-mismatch]] | EXIF thumbnail mismatch(anti-forensics) |
| 8 | ZIP 내부 파일 시간 불일치로 원본 위치 추적 | 초중급 | [[forensics-scenario-08-zip-crc-timestamp-anomaly]] | ZIP CRC32/외부 속성/시각 메타 3중 검증 |
| 9 | 메모리 덤프 속 코드 페이지 변환 | 초중급 | [[forensics-scenario-09-memory-codepage-chain]] | EUC-KR/Shift-JIS/UTF-16LE 인코딩 + 4KB 페이지 분할 |
| 10 | 클라우드 활동 로그 (CloudTrail 시뮬레이션) | 초중급 | [[forensics-scenario-10-cloudtrail-iam-correlate]] | AWS CloudTrail JSON + IAM 정책 상관 분석 |

## 공통 설계 원칙
- 아티팩트는 1~3개로 제한합니다.
- 정답 규칙은 한 문장으로 설명 가능해야 합니다.
- 초급은 메타데이터/문자열, 초중급은 2개 이상의 아티팩트 결합을 목표로 합니다.
- 시리즈 2는 **anti-forensics 흔적**(썸네일 mismatch, ZIP 메타 조작, 비정상 키 사용)을 한 단계 더 다룹니다.

## 참고 페이지
- [[forensics-scenario-production-plan]]
- [[forensics-writeup-family-hub]]
- [[picoctf-2024-forensics-survey]]
- [[picoctf-2025-forensics-survey]]
- [[forensics-disk-hub]]
- [[forensics-network-hub]]
- [[forensics-stego-hub]]
- [[forensics-memory-hub]]
- [[forensics-windows-hub]]
