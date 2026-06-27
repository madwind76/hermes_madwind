---
title: 외장 드라이브 흔적 (NTFS MFT·USN Journal)
created: 2026-06-26
updated: 2026-06-26
type: concept
tags: [ctf, education, forensics, challenge-development, lab, disk, ntfs, mft, usn]
sources: [https://github.com/Cajac/picoCTF-writeups/blob/main/picoCTF_2024/Forensics/README.md, https://learn.microsoft.com/en-us/windows/win32/fileio/change-journals]
confidence: medium
---

# 외장 드라이브 흔적 (NTFS MFT·USN Journal)

> 난이도: 초중급
> 소요 시간: 25~35분

## 배경
중요 자료가 USB로 반출된 정황이 있습니다. 해당 외장 드라이브는 회수되지 않았지만, 호스트 PC의 디스크 이미지에는 NTFS 메타데이터가 남아 있습니다. 참가자는 NTFS의 두 핵심 메타 채널(`$MFT`, `$UsnJrnl:$J`)을 직접 읽어 **누가, 언제, 어떤 파일을 복사하려 했는지** 복원해야 합니다.

## picoCTF·기존 시나리오 대비 차별점
- picoCTF 2024/2025 Forensics 중 NTFS `$MFT`/`$UsnJrnl` 분석 문제는 등장하지 않음.
- 기존 [[forensics-scenario-02-locked-laptop-secret-memo]]는 BitLocker + 메모리 덤프 조합으로, **암호화 해제 후 단서 수집**이 중심.
- 본 시나리오는 암호화되지 않은 NTFS 볼륨에서 **파일시스템 메타 흔적**만으로 활동 사실을 입증하는 데 초점.

## 제공 파일
- `host-disk.dd` — 호스트 PC의 시스템 디스크 이미지 (NTFS, 약 80MB 슬라이스)
- `case-brief.md` — 사건 개요 + 의심 파일명 목록 (`proposal.docx`, `Q3-roadmap.pptx`)
- `tools-hint.txt` — 권장 도구 목록 (`icat`, `fls`, `analyzeMFT`, `MFTExplorer`, `RegRipper`)

## 문제 목표
`$MFT` 엔트리와 `$UsnJrnl:$J` 레코드에서 외장 드라이브의 시리얼/문자열을 찾아, 반출 정황을 입증하는 **사용자·시각·파일명** 트리오를 복원합니다.

## 의도한 풀이 흐름
1. `fls -o 0 host-disk.dd` 로 루트 엔트리를 확인하고 `$MFT`, `$UsnJrnl`의 MFT entry 번호를 찾습니다.
2. `icat -o 0 host-disk.dd <mft_entry> > $MFT` 로 `$MFT`를 추출합니다.
3. `analyzeMFT $MFT -o mft.csv` 로 엔트리별 타임스탬프·파일명·부모 디렉터리를 확인합니다.
4. 외장 드라이브 흔적(`E:\`, `USB`, `Removable`)이 등장하는 `$MFT` 엔트리를 찾습니다.
5. `icat -o 0 host-disk.dd <usnjrnl_entry>` 로 `$UsnJrnl:$J`를 추출하고 `analyzeUsnJrnl`로 파싱합니다.
6. USN 레코드의 `Reason`(`0x00000002`=데이터 확장, `0x00000100`=이름 변경) 과 타임스탬프를 결합해 **시각·행위**를 확정합니다.
7. `case-brief.md`의 의심 파일명과 USN `FileName`을 매칭해 플래그 문자열을 조립합니다.

## 정답 규칙
- `picoCTF{<username>_<HHMM>_<filename_stem>}`
- 예시: `picoCTF{skim_2247_roadmap}`
- `$MFT` 표준정보(STDINFO)와 `$UsnJrnl`의 시각이 일치해야 정답 인정

## 출제자 노트
- `$MFT`는 약 2,000개 엔트리 수준으로 잘라 냅니다.
- USN 레코드 약 1,000건 중 의심 외장 흔적은 8~12건만 남깁니다.
- 외장 드라이브 문자열 `USB`, `E:\` 외에 시리얼 번호 일부(`AA31-...`)를 1건 섞어 분석 깊이를 자연스럽게 만듭니다.
- 정상 사용자(예: `jsung`)의 평소 작업 6건과 함께 섞어 **트래픽 노이즈**를 만듭니다.

## 트러블슈팅
| 증상 | 원인 | 해결 |
|---|---|---|
| `analyzeMFT`에서 parent_seq 깨짐 | `$MFT` 일부 잘림 | `icat`로 다시 추출, dd 블록 크기 확인 |
| `$UsnJrnl:$J`가 비어 보임 | `$J`가 아닌 `$MAX`를 추출 | `$J`의 MFT entry 직접 지정 |
| USN 시각이 1970년/이상함 | 파일시스템 UTC 미보정 | `TZ=UTC` 명시 후 재해석 |
| 외장 흔적이 안 보임 | 외장 마운트 로그가 아니라 일반 USB 부팅 흔적만 남은 경우 | `$LogFile` 보조 활용 |

## 학습 포인트
- NTFS 메타데이터(`$MFT`, `$UsnJrnl`)가 실제 IR에서 어떤 증거력을 갖는지 이해합니다.
- USN `Reason` 플래그의 의미를 통해 **어떤 I/O 동작이 발생했는지** 추론하는 습관을 기릅니다.
- 단순 문자열 검색을 넘어 **메타 레코드**를 읽는 포렌식 감각을 익힙니다.

## 관련 페이지
- [[forensics-writeup-family-hub]] — 포렌식 패턴 허브
- [[forensics-disk-hub]] — 디스크 포렌식 허브
- [[forensics-scenario-02-locked-laptop-secret-memo]] — 암호화 디스크 + 메모리 단서 수집 (대비 시나리오)
