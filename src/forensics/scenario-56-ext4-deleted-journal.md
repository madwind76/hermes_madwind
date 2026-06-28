---
title: 리눅스 삭제된 파일의 디스크 inode 매핑 복구 (ext4 Deleted File Recovery)
created: 2026-06-28
updated: 2026-06-28
type: ctf-challenge
tags: [ctf, ctf-challenge, forensics, disk, ext4, journal, jbd2, file-recovery, strings]
confidence: high
---

# 리눅스 삭제된 파일의 디스크 inode 매핑 복구 (ext4 Deleted File Recovery)

> **난이도**: 초중급  
> **소요 시간**: 25~30분  
> **참고 picoCTF 문제**: 디스크 볼륨 파일시스템 삭제 복구 (Linux ext4 저널링 포렌식)

## 1. 배경 시나리오
사내 중요 보안 규정을 유포하고 즉시 파일시스템 상에서 삭제한 피의자의 리눅스 서버 가상 디스크 이미지를 수집했습니다. ext4 파일시스템 특성상, 파일이 `rm` 명령어로 삭제되면 해당 파일의 메타데이터를 담은 inode 정보(파일 크기, 데이터 블록 포인터 등)가 즉시 0으로 초기화되므로 슬루스킷(`fls`, `icat`)과 같은 기본적인 Inode 추적 도구로는 복구가 불가능합니다. 하지만 ext4는 갑작스러운 시스템 비정상 종료 시 파일시스템 무결성을 보존하기 위해 데이터 변경 사항을 기록해 두는 **저널(Journal, JBD2)** 메커니즘(기본 Inode 8에 자동 할당)을 유지합니다. 획득한 원시 저널 스트림 데이터 `ext4_journal.bin`을 분석하여 **삭제되어 유실되었던 기밀 텍스트 속의 플래그**를 복구하십시오.

## 2. 제공 파일
* `ext4_journal.bin` (피해 ext4 파일시스템의 Journal 백업 영역에서 직접 덤프한 원시 이진 데이터 파일)

## 3. 문제 목표
리눅스의 보편적 파일시스템인 ext4의 파일 삭제 메커니즘과 트랜잭션 저널링(JBD2 - Journaling Block Device) 엔진의 동작 구조를 파악하고, 저널 바이너리 블록에 임시 동기화되어 남아 있는 미커밋/과거 변경 데이터 섹터를 디코드하여 지워진 원본 파일 본문을 카빙해 냅니다.

## 4. 의도한 풀이 흐름
1. **파일시스템 삭제 한계 인지**:
   * ext3 파일시스템과 달리, ext4에서는 파일 삭제 시 데이터 포인터인 블록 맵(Block Map) 정보가 inode 구조체 내에서 완전히 초기화되어 빈 공간으로 할당 해제됨을 인지합니다.
2. **저널 바이너리 분석**:
   * 제공된 파일 `ext4_journal.bin`은 ext4 저널링 시스템의 원시 디스크 덤프입니다.
   * 트랜잭션 커밋 과정에서 원시 텍스트 블록 전체가 저널 영역에 백업 기표되어 잔재하므로, `strings` 명령어 및 필터링을 활용해 가독 스트링 내에 플래그 키워드가 존재하는지 검색합니다:
     ```bash
     strings ext4_journal.bin | grep "picoCTF"
     ```
3. **플래그 데이터 추출**:
   * 검색 결과 저널 블록 데이터 슬라이스 내부에서 다음의 평문 텍스트 라인을 획득합니다:
     `Important secrets: picoCTF{ext4_jbd2_journ4l_recovery}`
   * 획득한 최종 플래그를 정립합니다:
     `picoCTF{ext4_jbd2_journ4l_recovery}`

## 5. 정답(플래그) 규칙 및 예시
* **플래그 형식**: `picoCTF{<flag_string>}`
* **예시**: `picoCTF{ext4_jbd2_journ4l_recovery}`

## 6. 출제자 노트 & 파일 제작 가이드
* **아티팩트 제작 방법**:
  1. 테스트 리눅스 환경에서 빈 디스크 이미지를 생성하고 ext4 포맷을 적용합니다:
     `dd if=/dev/zero of=test.img bs=1M count=20 && mkfs.ext4 test.img`
  2. 디스크를 마운트하고 기밀 파일 `sensitive.txt`를 생성합니다:
     `echo "Important secrets: picoCTF{ext4_jbd2_journ4l_recovery}" > /mnt/test/sensitive.txt`
  3. 디스크 동기화(`sync`)를 수행하여 저널 및 물리 디스크에 정상 기표되도록 유도합니다.
  4. 대상을 강제 삭제합니다: `rm /mnt/test/sensitive.txt`
  5. 언마운트 후, `debugfs` 도구를 구동하여 ext4 파일시스템의 저널 영역(기본 Inode 8)의 데이터를 덤프해 냅니다:
     `debugfs -R "dump <8> ext4_journal.bin" test.img`
  6. 덤프된 `ext4_journal.bin` 파일 내에 플래그 평문 데이터 블록이 온전히 보존되어 있는지 검수하여 분석 파일로 제공합니다.
* **출제 포인트**: 
  * 리눅스 침해 사고 분석에서 안티 포렌식(파일 삭제) 수법에 대응하여, inode 정보가 유실된 ext4 파일시스템 하드디스크의 한계를 저널링 트랜잭션 흔적(ext4 Journal Forensics) 추적 기법을 통해 원본 내용을 안정적으로 구출하는 고급 디스크 분석 기법을 학습시킵니다.

## 7. 트러블슈팅 및 힌트
* **Q. debugfs에서 cat <8> 명령을 내렸을 때 저널 데이터가 보이지 않는 이유가 무엇인가요?**
  * A. 저널 영역은 일반 평문 파일 스트림이 아닌 파일시스템의 블록 단위 변경 기록을 담는 특수 구조체로 채워져 있으므로 디버그 파일시스템 셸 상에서 직접 텍스트 가독이 되지 않습니다. 반드시 로컬 바이너리 파일로 `dump` 처리를 한 뒤 `strings`나 저널 전용 파서 도구(ext4magic 등)로 정밀 스캔해야 합니다.
* **Q. ext4magic 도구를 가동하면 어떻게 되나요?**
  * A. ext4magic은 저널 아티팩트를 자동 분석해 주는 전문 복구 유틸리티입니다:
     `ext4magic test.img -r -f sensitive.txt`
     위 명령을 가동하면 파일시스템 저널에 보존된 과거 트랜잭션 블록 맵 정보를 분석하여, 삭제되어 완전히 깨진 inode 정보를 과거 시점 데이터로 역생성해 원본 파일을 온전히 자동 복원해 줍니다.

## 8. 학습 포인트
* **ext4 파일 삭제 메커니즘**: ext3와ext4 파일시스템의 삭제 정책(Block Allocation 및 Extent Tree 소거)의 차이점과 포렌식적 복구 한계성을 배웁니다.
* **JBD2(Journaling Block Device) 저널 복구**: 리눅스 저널 영역(Inode 8)의 물리 저장 특징을 파악하여 삭제된 중요 자산의 비파괴 복구 프로세스를 습득합니다.
