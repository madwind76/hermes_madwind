---
title: ZIP 내부 파일 시간 불일치로 원본 위치 추적
created: 2026-06-26
updated: 2026-06-26
type: concept
tags: [ctf, education, forensics, challenge-development, lab, archive, zip, crc32, timestamp]
sources: [https://github.com/Cajac/picoCTF-writeups/blob/main/picoCTF_2024/Forensics/README.md]
confidence: medium
---

# ZIP 내부 파일 시간 불일치로 원본 위치 추적

> 난이도: 초중급
> 소요 시간: 25~35분

## 배경
외부로 유출된 ZIP 파일이 확보되었습니다. ZIP 헤더에 보이는 **압축 시각**과 **수정 시각(mod time/date)** 이 의도적으로 조작된 흔적이 있으며, **각 엔트리의 CRC32**가 **언컴프레스 크기와 본문에서 계산한 CRC32**와 일치하지 않습니다. 참가자는 CRC32와 시각 메타데이터의 불일치를 활용해 **원래 파일이 호스트 PC의 어느 경로에 있었는지** 추정해야 합니다.

## picoCTF·기존 시나리오 대비 차별점
- picoCTF는 ZIP/아카이브 포렌식 문제가 거의 없고, 있다고 해도 단순 암호 해제(`Vault Door` 등 Crypto 계열)에 머무름.
- 기존 시나리오는 ZIP을 다루지 않음.
- 본 시나리오는 ZIP **로컬 헤더와 엔트리 헤더의 시각 메타**, **외부 속성(External Attributes)**, **CRC32 불일치**를 한꺼번에 활용합니다.

## 제공 파일
- `leak.zip` — 압축 대상 파일 6개 (그중 2개가 시각 조작 + CRC32 mismatch)
- `crc_table.txt` — 각 엔트리의 CRC32와 계산값 비교표 (출제자 제공 단서)
- `host-fs-summary.md` — 호스트 PC에 있던 파일/디렉터리 목록(원래 위치 후보)

## 문제 목표
시각과 CRC32 메타가 어긋난 엔트리를 찾고, **원래 저장 경로**와 **최종 유출 시각**을 복원합니다.

## 의도한 풀이 흐름
1. `unzip -l leak.zip` 으로 엔트리 목록과 `Date`, `Time`, `Length`, `CRC-32`를 확인합니다.
2. `zipinfo -v leak.zip` 또는 `python -m zipfile -l leak.zip` 로 외부 속성(`external_attr`)을 확인합니다.
3. `crc_table.txt`의 값과 ZIP 헤더 CRC32를 비교해 **불일치 엔트리**를 찾습니다.
4. 불일치 엔트리를 압축 해제하여 실제 데이터의 CRC32를 계산합니다:
   ```bash
   unzip leak.zip 'suspicious/*' -d out/
   python3 -c "import zlib,sys;print(hex(zlib.crc32(open(sys.argv[1],'rb').read())) )" out/suspicious/doc.docx
   ```
5. 헤더 시각(`Date Time`)과 실제 파일시스템의 mtime(외부 속성 `0x20` 비트)이 다른 경우, **원래 mtime**을 외부 속성에서 복원합니다.
6. `host-fs-summary.md`의 후보 경로 중 `외부 속성 디렉터리 비트`와 일치하는 위치를 찾습니다.
7. 시각 차이와 경로 정보를 결합해 플래그를 만듭니다.

## 정답 규칙
- `picoCTF{<original_path_stem>_<original_mtime_HHMM>}`
- 예시: `picoCTF{projects_secur1ty_2047}`
- 시각은 24시간제 HHMM, 경로 stem은 슬래시(`/`)를 언더스코어로 치환

## 출제자 노트
- ZIP의 `version made by` 필드는 Windows(`0x000A`) 또는 Unix(`0x0003`)를 분리해 **두 운영체제에서 만든 흔적**이 섞이게 만듭니다.
- 외부 속성 상위 16비트(Unix 모드)에서 디렉터리 구분(`0o40755`)을 명시적으로 노출하면 경로 추적이 자연스럽습니다.
- 정상 엔트리 4개 + 조작 엔트리 2개로 구성합니다.
- CRC32 불일치는 **실제 본문 CRC32로 헤더만 덮어쓴 형태**로 만들면, 참가자가 계산으로 확인해야 깨달을 수 있습니다.

## 트러블슈팅
| 증상 | 원인 | 해결 |
|---|---|---|
| `unzip`이 CRC32 에러로 멈춤 | 의도된 불일치 | `unzip -o`로 강제 해제 후 별도 검증 |
| `external_attr`이 0 | Windows ZIP (Unix 모드 미저장) | `zipinfo -v` 대신 `xxd`로 raw 헤더 직접 파싱 |
| 원래 경로를 못 찾겠음 | 디렉터리 비트 누락 | `host-fs-summary.md`의 디렉터리 후보와 비교 |
| 시각이 둘 다 다름 | 의도된 더블 조작 | 외부 속성 mtime 우선, 그 다음 헤더 시각 |

## 학습 포인트
- ZIP의 **로컬 헤더/엔트리 헤더/외부 속성**이 각각 다른 정보를 담고 있다는 점을 이해합니다.
- 메타데이터의 **일관성 검사**만으로도 편집 흔적을 잡아낼 수 있다는 IR 감각을 기릅니다.
- CRC32가 본문과 헤더에 **각각** 존재한다는 사실과, **둘의 불일치**가 곧 위변조의 신호임을 학습합니다.

## 관련 페이지
- [[forensics-writeup-family-hub]] — 포렌식 패턴 허브
- [[forensics-disk-hub]] — 디스크/파일 메타 허브
- [[forensics-scenario-04-broken-packet-clue]] — PCAP 페이로드 재조립 (대비 시나리오)
