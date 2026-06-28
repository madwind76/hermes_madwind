---
title: ext4 저널링 기반 유출 데이터 압축 아카이브 조각 복구 (ext4 Journal Compression Carving)
created: 2026-06-28
updated: 2026-06-28
type: ctf-challenge
tags: [ctf, ctf-challenge, forensics, disk, ext4, journal, zip-carving, file-recovery, binwalk, foremost]
confidence: high
---

# ext4 저널링 기반 유출 데이터 압축 아카이브 조각 복구 (ext4 Journal Compression Carving)

> **난이도**: 초중급  
> **소요 시간**: 25~30분  
> **참고 picoCTF 문제**: 삭제된 압축 아카이브 물리 카빙 복구 (ext4 Journal File Carving)

## 1. 배경 시나리오
공격자가 웹 서버 내부의 여러 민감 소스코드를 `exfil_data.zip` 파일로 다중 압축 아카이빙한 뒤 외부로 전송하고, 흔적을 지우기 위해 해당 zip 아카이브를 리눅스 터미널에서 `rm` 명령어로 삭제했습니다. ext4 파일시스템 특성상 Inode 테이블의 블록 포인터가 초기화되어 디바이스 상에서 파일 포인팅 흔적을 잃었으나, 파일시스템의 백그라운드 트랜잭션을 로깅하는 **저널링 디바이스(JBD2)** 내에 해당 압축 파일이 기표 및 동기화 처리될 때 복사되었던 디스크 물리 블록들의 잔재가 여전히 존재할 가능성이 높습니다. 수집된 저널 영역의 디스크 덤프 파일인 `ext4_journal_carve.bin`을 분석하여 **삭제 유실되었던 압축 아카이브 파일을 복구하고 내부의 플래그 텍스트**를 획득하십시오.

## 2. 제공 파일
* `ext4_journal_carve.bin` (피해 ext4 디바이스의 저널 링 버퍼 영역 전체를 통째로 카빙해 낸 원시 바이너리 덤프 파일)

## 3. 문제 목표
ext4 저널 디바이스(Inode 8)에 시스템 파일 쓰기 및 수정 동작 시 복사 적재되는 저널 트랜잭션 데이터 블록의 성질을 이해하고, 파일 카빙 도구(`binwalk`, `foremost`) 또는 수동 헥스 스캔을 통해 ZIP 포맷 고유 시그니처 구조(`50 4B 03 04` 등)를 검출해 정상 압축 파일로 디스크 카빙 복구해 냅니다.

## 4. 의도한 풀이 흐름
1. **바이너리 매직 헤더 스캔**:
   * 제공된 `ext4_journal_carve.bin` 파일 내에 압축 파일 조각이 잔재하는지 확인하기 위해 파일 카빙 분석 도구인 `binwalk`를 가동해 정적 시그니처 맵을 출력합니다:
     ```bash
     binwalk ext4_journal_carve.bin
     ```
   * 분석 결과, 바이너리 중간 특정 오프셋(예: `0x1A4000`) 부근에서 ZIP 아카이브 시작 시그니처인 **`50 4B 03 04`** (아스키 문자 `PK\x03\x04`에 해당)가 탐지됨을 파악합니다.
2. **압축 파일 카빙 (Carving) 수행**:
   * **도구 활용**: `foremost` 또는 `binwalk` 추출 옵션을 사용하여 저널 바이너리 내부의 임베디드 파일들을 자동 분리해 냅니다:
     ```bash
     binwalk -e ext4_journal_carve.bin
     ```
     또는
     ```bash
     foremost -t zip -i ext4_journal_carve.bin -o output_dir
     ```
   * **수동 카빙**: 헥스 에디터로 파일을 열고 `50 4B 03 04` (Local File Header) 시작 오프셋부터, ZIP의 물리 종단을 알리는 구조체인 `50 4B 05 06` (End of Central Directory, EOCD) 헤더 바이트 정보와 그 뒤의 가변 주석 바이트 크기(기본 18바이트)를 포함해 물리 섹터 크기만큼 블록을 복제(`dd` 활용) 컷팅해 냅니다.
3. **압축 해제 및 플래그 획득**:
   * 카빙되어 정상적으로 복구된 ZIP 아카이브 파일의 압축을 풉니다:
     `unzip exfil_data.zip`
   * 압축이 정상 해제되어 추출된 `flag.txt` 텍스트 파일을 열고 내부 플래그를 확보합니다:
     `picoCTF{ext4_journ4l_z1p_f1l3_c4rv3d}`

## 5. 정답(플래그) 규칙 및 예시
* **플래그 형식**: `picoCTF{<flag_string>}`
* **예시**: `picoCTF{ext4_journ4l_z1p_f1l3_c4rv3d}`

## 6. 출제자 노트 & 파일 제작 가이드
* **아티팩트 제작 방법**:
  1. 기밀 플래그 파일 `flag.txt`를 생성합니다:
     `echo "picoCTF{ext4_journ4l_z1p_f1l3_c4rv3d}" > flag.txt`
  2. 해당 파일을 zip 포맷으로 기밀 패킹합니다:
     `zip exfil_data.zip flag.txt`
  3. 테스트 ext4 볼륨에 해당 `exfil_data.zip` 파일을 복사 적재한 뒤, 디스크 동기화(`sync`)를 수행해 저널 데이터 디스크립터 영역에 ZIP 이진 스트림 전체가 온전히 라이트(Write Log)되도록 유도합니다.
  4. 파일을 강제 삭제합니다: `rm exfil_data.zip; sync`
  5. `debugfs` 툴의 `dump <8> ext4_journal_carve.bin` 명령을 실행해 저널 영역 바이트 전체를 적출합니다.
  6. 덤프된 저널 이미지 내에 `50 4B 03 04` 매직 헤더와 zlib 디플레이트 데이터가 손상 없이 유지되어 기계적 카빙 복구가 성공하는지 최종 검수한 후 학생용 챌린지 파일로 유포합니다.
* **출제 포인트**: 
  * 리눅스 디스크 포렌식에서 안티 포렌식(파일 완전 삭제) 위협 발생 시, 단순 Inode 목록 복구 툴의 한계를 저널링 시스템 트랜잭션 블록 카빙 기법(ext4 Journal Carving)으로 우회 돌파하는 심도 있는 파일시스템 복원 실무 능력을 측정합니다.

## 7. 트러블슈팅 및 힌트
* **Q. ZIP 파일 카빙 시 파일의 종단을 정확히 끊는 시그니처 헥스 바이트는 무엇인가요?**
  * A. ZIP 파일 포맷은 헤더 종류에 따라 다음과 같이 고유 4바이트 매직을 구분합니다:
    * `50 4B 03 04` (PK\x03\x04): 개별 압축 파일의 로컬 헤더 (Local File Header)
    * `50 4B 01 02` (PK\x01\x02): 디렉터리 디스크립터 헤더 (Central Directory Header)
    * `50 4B 05 06` (PK\x05\x06): 압축 파일의 전체 종단 구조체 헤더 (End of Central Directory, EOCD)
    따라서 수동 카빙 시에는 EOCD 시작 위치인 `50 4B 05 06` 바이트 오프셋을 찾고 그 뒤에 위치하는 디렉터리 상세 메타데이터 바이트(통상 18~22바이트)까지를 온전히 포함해서 데이터를 잘라내야 압축 관리자가 깨진 아카이브로 오인하지 않고 정상 해독을 마칩니다.
* **Q. 카빙 복구한 ZIP 파일의 압축을 풀 때 'bad zipfile offset' 오류가 발생하며 튕깁니다.**
  * A. 저널 영역에서 파일 조각을 덤프할 때, ZIP 데이터 앞부분에 저널 자체의 메타데이터 블록(JBD2 Block Tag/Descriptor)이 중간중간 수바이트 씩 수동 덮어써져 있거나 끼어 들어간 경우 zlib 압축 포맷이 무너져 해제 에러가 납니다. 이 경우에는 `zip -FF exfil_data.zip --out repaired.zip` 등 ZIP 구조 복구 유틸리티를 수행해 손상된 중간 인덱스를 복구 재구성해 주어야 해제가 성공합니다.

## 8. 학습 포인트
* **ZIP 아카이브 포맷 스펙**: 로컬 파일 헤더, 센트럴 디렉터리 및 EOCD의 구조적 결합 규칙을 상세히 학습합니다.
* **비할당/저널 영역 디스크 카빙**: 파일시스템 카빙 유틸리티(Binwalk, Foremost)의 원리를 이해하고, 저널링 파일 트랜잭션 데이터를 역추적해 기밀 증적을 환원하는 포렌식 복구력을 구축합니다.
