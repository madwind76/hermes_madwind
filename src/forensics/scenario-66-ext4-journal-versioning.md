---
title: 리눅스 ext4 저널 트랜잭션 기반 파일 내용 변천사 추적 (ext4 Journal Versioning Analysis)
created: 2026-06-28
updated: 2026-06-28
type: ctf-challenge
tags: [ctf, ctf-challenge, forensics, disk, ext4, journal, versioning, transaction, file-history]
confidence: high
---

# 리눅스 ext4 저널 트랜잭션 기반 파일 내용 변천사 추적 (ext4 Journal Versioning Analysis)

> **난이도**: 초중급  
> **소요 시간**: 25~30분  
> **참고 picoCTF 문제**: 파일 변조 이력 추적 및 이전 버전 복원 (ext4 Journal Versioning 분석)

## 1. 배경 시나리오
보안 사고 용의자가 사용하던 리눅스 가상 이미지에서 중요 파일인 `config.ini`를 분석했습니다. 하지만 현재 파일시스템 상에 존재하는 최종 활성 파일 내역에는 플래그 정보가 지워진 상태의 더미 데이터만 기입되어 있습니다. 침해 조사관은 용의자가 수동으로 텍스트를 여러 번 덮어쓰기(Overwrite)하여 기존 데이터를 소거하려 시도했음을 파악하고, ext4 저널 디바이스(JBD2)가 보존하는 트랜잭션 링 버퍼(Ring Buffer) 영역을 정밀 검사했습니다. 저널 공간에서 연속적인 변경 이력 블록들이 격출된 `journal_blocks_dump.txt` 파일이 제공됩니다. 이 저널 변경 히스토리 중 **두 번째 버전(Transaction 1025)의 원본 데이터 블록에 기록되어 있었던 플래그**를 식별하십시오.

## 2. 제공 파일
* `journal_blocks_dump.txt` (ext4 파일시스템의 저널 영역에서 수집된, 특정 파일 수정 타임라인에 부합하는 연속된 저널 트랜잭션 데이터 블록의 헥사 덤프 및 텍스트 대조 파일)

## 3. 문제 목표
ext4 파일시스템의 트랜잭션 기반 저널 메커니즘(JBD2가 디스크 영구 동기화 전에 변경 예정 블록들을 저널 디스크 섹터에 순차 작성하는 방식)을 이해하고, 저널 버퍼에 임시 보존되는 동일 물리 데이터 블록의 버전별 변천사(Versioning)를 역추적해 기밀 데이터를 구출합니다.

## 4. 의도한 풀이 흐름
1. **저널 블록 구성 진단**:
   * 제공된 `journal_blocks_dump.txt` 텍스트 파일을 엽니다.
   * 파일 내부에는 트랜잭션 시퀀스 번호(Transaction ID) 순으로 정렬된 복수의 데이터 블록 덤프가 수록되어 있습니다:
     * **Block A (Transaction 1024)**: 수정 이력 최초 버전
       `[Data: ... picoCTF{ext4_journ4l_v3rs1on_one_t1me} ...]`
     * **Block B (Transaction 1025)**: 두 번째 수정 버전
       `[Data: ... picoCTF{ext4_journ4l_v3rs1on_two_t1me} ...]`
     * **Block C (Transaction 1026 - 최종 커밋)**: 현재 디스크 활성 상태와 동일한 소거 완료된 버전
       `[Data: Overwritten dummy content ...]`
2. **요구 트랜잭션 대조 및 카빙**:
   * 본 시나리오의 요구 사양은 최종 지워지기 바로 전 단계인 **두 번째 버전 (Transaction ID: 1025)** 레코드의 내용 복원입니다.
   * `Transaction 1025` 헤더에 속하는 Block B의 바이너리/텍스트 데이터를 격리 대조합니다.
3. **플래그 도출**:
   * 해당 트랜잭션 블록 영역 내에 보존되어 있던 문자열을 획득합니다:
     `picoCTF{ext4_journ4l_v3rs1on_two_t1me}`

## 5. 정답(플래그) 규칙 및 예시
* **플래그 형식**: `picoCTF{<flag_string>}`
* **예시**: `picoCTF{ext4_journ4l_v3rs1on_two_t1me}`

## 6. 출제자 노트 & 파일 제작 가이드
* **아티팩트 제작 방법**:
  1. 테스트용 ext4 디바이스 이미지를 마운트합니다.
  2. 기밀 파일 `config.ini`를 생성하고 첫 플래그를 입력합니다:
     `echo "picoCTF{ext4_journ4l_v3rs1on_one_t1me}" > config.ini; sync`
  3. 다른 값을 덮어써서 두 번째 버전을 기표합니다:
     `echo "picoCTF{ext4_journ4l_v3rs1on_two_t1me}" > config.ini; sync`
  4. 최종 더미 데이터로 덮어써서 흔적을 지웁니다:
     `echo "Overwritten dummy content" > config.ini; sync`
  5. `debugfs` 도구를 구동하여 저널 로그 영역(Inode 8)을 추출하고, 전용 파서 또는 바이너리 오프셋 스캔을 통해 동일 블록 오프셋에 대해 생성된 트랜잭션 1024, 1025, 1026에 해당하는 블록 덤프 데이터를 분리합니다.
  6. 각 트랜잭션 번호 헤더 정보와 헥스 바이트 내용을 통합 구성한 `journal_blocks_dump.txt`를 생성해 문제를 배포합니다.
* **출제 포인트**: 
  * 사용자가 파일의 내용을 변경하고 동기화(Commit)를 거듭해 현재 디스크 상의 활성 본문 메타데이터에서는 과거 흔적이 유실되었을 때, ext4 저널 아티팩트의 트랜잭션 영구 적재 링 버퍼 성질(ext4 Journal Versioning Analysis)을 활용해 과거 유출 기밀의 히스토리를 입체적으로 재구성 복원해 내는 실전적 조사 프로세스를 교육합니다.

## 7. 트러블슈팅 및 힌트
* **Q. 트랜잭션 시퀀스 ID는 저널 블록 내에서 어떻게 구분하나요?**
  * A. JBD2 저널 헤더(Journal Block Header) 영역에는 매직 시그니처(`0xC03B3998`)와 함께 해당 블록이 속한 트랜잭션 시퀀스 번호(32비트 빅엔디언 값)가 기표되어 있어 정교한 정적 분류가 가능합니다.
* **Q. 저널이 이미 덮어씌워져 유실된 경우는 어떻게 하나요?**
  * A. ext4 저널 영역은 크기가 고정된 원형 큐(Circular Queue) 형태로 가동되므로, 변경량이 지나치게 많아지면 오래된 과거 트랜잭션 데이터부터 수동 덮어쓰기(Overwrite)되어 영구 유실됩니다. 따라서 사건 감지 직후 볼륨 마운트를 즉시 차단(Read-Only로 전환)하여 저널 데이터가 런타임 수동 덮어씌워지는 것을 최우선으로 제어해야 저널 이력 복구를 성립시킬 수 있습니다.

## 8. 학습 포인트
* **ext4 저널링 트랜잭션 생명주기**: 변경 사항이 임시 기표(Log)되고 물리 볼륨에 최종 커밋(Commit)되는 저널 상태 천이 사양을 배웁니다.
* **데이터 버전 관리 포렌식**: 삭제 및 덮어쓰기로 훼손된 증적에 대응해 파일시스템 저널 블록 히스토리를 역연산하여 과거 임의 시점의 원본 데이터를 복구해 내는 전문 포렌식 응용력을 학습합니다.
