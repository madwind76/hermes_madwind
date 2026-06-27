---
title: 메모리 덤프 속 코드 페이지 변환
created: 2026-06-26
updated: 2026-06-26
type: concept
tags: [ctf, education, forensics, challenge-development, lab, memory, encoding, codepage, volatility]
sources: [https://github.com/Cajac/picoCTF-writeups/blob/main/picoCTF_2024/Forensics/README.md, https://www.volatilityfoundation.org/]
confidence: medium
---

# 메모리 덤프 속 코드 페이지 변환

> 난이도: 초중급
> 소요 시간: 30~40분

## 배경
Windows 메모리 덤프가 확보되었습니다. 평소라면 `strings`로 ASCII를 뽑고 끝나겠지만, 이번 덤프에는 **EUC-KR(CP949)**, **Shift-JIS(CP932)**, **UTF-16LE**로 저장된 한국어/일본어 문자열이 섞여 있어 한 번에 검색되지 않습니다. 또한 일부 문자열은 **메모리 페이지 정렬(4KB)** 단위로 분할되어 있습니다. 참가자는 인코딩 변환과 페이지 재조립으로 **사용자가 마지막으로 입력한 메시지**를 복원해야 합니다.

## picoCTF·기존 시나리오 대비 차별점
- picoCTF의 메모리 포렌식([[mob-psycho-final-writeup]] 등)은 ASCII 중심 단서 추출.
- 기존 [[forensics-scenario-02-locked-laptop-secret-memo]]는 메모리에서 "**단서**"를 찾는 형태이며 인코딩 변환은 다루지 않음.
- 본 시나리오는 **인코딩 차이**(EUC-KR/Shift-JIS/UTF-16LE)와 **메모리 페이지 분할**이 동시에 등장합니다.

## 제공 파일
- `win10-mem.raw` — Windows 10 메모리 덤프 (약 220MB, Volatility 2/3 호환)
- `process-list.txt` — `pslist` 출력 (의심 프로세스 3개: `notepad.exe`, `kakao.exe`, `chrome.exe`)
- `note-patterns.txt` — 탐지 후보 문자열 패턴 (한글/일본어 모두 포함, 인코딩 모호)
- `codepage-hint.md` — `chcp` 명령 결과 시뮬레이션 노트 (950, 932, 949, 65001)

## 문제 목표
여러 인코딩으로 분산 저장된 문자열을 통합 검색해, **노트패드 마지막 메시지의 사용자명·문장 일부**를 복원합니다.

## 의도한 풀이 흐름
1. `vol -f win10-mem.raw windows.info` 로 덤프 메타 확인 (Profile: `Win10x64_19041`).
2. `vol -f win10-mem.raw windows.pslist` 로 의심 프로세스 PID 확보.
3. `vol -f win10-mem.raw -o out/ windows.dumpfiles --pid <notepad_pid>` 로 노트패드 매핑 파일을 덤프합니다.
4. 덤프된 파일에 대해 `strings -e l` (UTF-16LE) 시도:
   ```bash
   strings -e l out/notepad.exe/<addr>.dmp | grep -i '회의'
   ```
5. 같은 파일을 `iconv -f cp949 -t utf-8`로 변환하며 다시 검색:
   ```bash
   cat out/notepad.exe/<addr>.dmp | iconv -f CP949 -t UTF-8//IGNORE | grep '회의'
   ```
6. `note-patterns.txt`의 일본어 패턴은 `iconv -f CP932 -t UTF-8`로 변환합니다.
7. 4KB 페이지 경계에서 문자열이 끊기는 경우, 인접 페이지를 `dd`로 이어 붙인 뒤 다시 검색합니다.
8. 각 인코딩에서 발견한 단어들을 사용자명·시각과 매칭해 최종 문장을 복원합니다.

## 정답 규칙
- `picoCTF{<username>_<keyword1>_<keyword2>}`
- 예시: `picoCTF{skim_회의록_확정}`
- UTF-8 인코딩으로 제출해야 함

## 출제자 노트
- 덤프 안에 EUC-KR, Shift-JIS, UTF-16LE 문자열을 **각각 최소 2개씩** 분산 배치합니다.
- `notepad.exe`의 매핑 파일 외에 `kakao.exe`, `chrome.exe`에도 **같은 키워드**가 다른 인코딩으로 남아 있게 하면, 참가자가 인코딩을 추론할 단서가 됩니다.
- 4KB 페이지 경계로 끊긴 문자열은 **2건**만 둡니다.
- Volatility 2/3 호환을 위해 `$Profile` 자동 추론이 되는 덤프 포맷으로 저장합니다.

## 트러블슈팅
| 증상 | 원인 | 해결 |
|---|---|---|
| `vol` 실행 시 profile 미스매치 | 덤프가 다른 Win10 빌드 | `vol -f win10-mem.raw banners.Banners` 로 정확 식별 |
| 한글이 깨짐 | CP949 → UTF-8 변환 누락 | `iconv -f CP949 -t UTF-8//IGNORE` 명시 |
| 일본어가 깨짐 | CP932 추측 실패 | `nkf --guess` 또는 `file -i`로 추정 |
| 페이지 경계 문자열 누락 | 단일 페이지만 검색 | `dd if=win10-mem.raw bs=4096 skip=N count=2` 로 인접 페이지 결합 |
| `strings -e l` 결과가 0건 | UTF-16LE BOM/엔디언 오인 | `strings -e b` (big-endian)도 시도 |

## 학습 포인트
- 메모리 포렌식에서 **인코딩은 자동으로 풀리지 않는다**는 점을 이해합니다.
- `strings`, `iconv`, `dd`, `vol` 도구를 **체인**으로 엮어 IR 작업을 구성하는 감각을 기릅니다.
- 4KB 페이지 경계, BOM, 엔디언 같은 **저수준 메모리 구조**가 결과에 어떻게 영향을 주는지 학습합니다.
