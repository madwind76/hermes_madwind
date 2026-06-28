---
title: 윈도우 알림 센터 DB 내 삭제된 메시지 복구 (SQLite WAL Page Carving)
created: 2026-06-28
updated: 2026-06-28
type: ctf-challenge
tags: [ctf, ctf-challenge, forensics, windows, sqlite, wal, write-ahead-log, notification-db, carving, xml]
confidence: high
---

# 윈도우 알림 센터 DB 내 삭제된 메시지 복구 (SQLite WAL Page Carving)

> **난이도**: 초중급  
> **소요 시간**: 25~30분  
> **참고 picoCTF 문제**: SQLite WAL 트랜잭션 캐시 삭제 레코드 복원 (Windows Notification WAL Carving)

## 1. 배경 시나리오
공격자가 윈도우 시스템에서 랜섬웨어를 가동하기 직전, 내부 위협 대응 시스템이 사용자 화면 우측 하단에 알림 메시지(Toast Notification)로 띄웠던 악성코드 차단 통지 및 기밀 암호 변수 알림 내용을 수사관들보다 먼저 확인했습니다. 피의자는 증적을 없애기 위해 즉시 윈도우 알림 센터 창을 클릭하여 알림을 일괄 삭제했고, 이로 인해 알림 보존 SQLite 데이터베이스인 `wpndatabase.db` 내 테이블 레코드가 완전히 삭제(Delete) 처리되었습니다. 하지만 SQLite 데이터베이스는 트랜잭션 동기화 및 쓰기 성능 최적화를 위해 **WAL (Write-Ahead Log)** 기법을 차용합니다. 메인 DB 테이블에서는 즉각 삭제되었더라도, 백그라운드 트랜잭션 기록 버퍼 파일인 **`wpndatabase.db-wal`** 영역에는 동기화 주기가 돌아와 비할당 페이지로 리사이클 처리되기 전까지는 마지막 트랜잭션 페이지(XML 본문) 흔적이 고스란히 물리 보존됩니다. 확보한 WAL 바이너리 파일인 `wpndatabase_wal_dump.bin`을 분석하여 **삭제 유실되었던 원래의 알림 메시지 XML 속에 포함되어 있던 플래그**를 획득하십시오.

## 2. 제공 파일
* `wpndatabase_wal_dump.bin` (사용자 PC 알림 센터 프로필 디렉터리에서 적출한 wpndatabase.db-wal 원시 이진 캐시 파일)

## 3. 문제 목표
SQLite 데이터베이스의 트랜잭션 로깅 매커니즘인 WAL(Write-Ahead Log) 파일의 구조적 저장 규칙(프레임 헤더, 페이지 동기화 원리 및 삭제 데이터 잔재 특징)을 파악하고, 바이너리 헥스 스캔을 가동해 포장 수록된 유니코드 XML 토스트 알림 본문 스트림을 디코드해 복원합니다.

## 4. 의도한 풀이 흐름
1. **이진 WAL 캐시 파일 정적 분석**:
   * 제공된 `wpndatabase_wal_dump.bin` 파일에 윈도우 알림 메시지 데이터(통상 XML 스키마 형태로 보존됨)가 보존되어 있는지 확인하기 위해 `strings` 명령어를 실행하고 플래그 포맷을 검색합니다:
     ```bash
     strings wpndatabase_wal_dump.bin | grep "picoCTF"
     ```
2. **XML 토스트 알림 스트림 획득**:
   * 검색 결과, WAL 페이지 트랜잭션 프레임 내에 직렬화 보존되어 있던 삭제된 알림 XML 본문 내역을 식별해 냅니다:
     ```xml
     <toast launch="args"><visual><binding template="ToastGeneric"><text id="1">Security Alert</text><text id="2">Flag: picoCTF{sqlite_wal_p4g3_c4rv3d_uccessfully}</text></binding></visual></toast>
     ```
3. **최종 플래그 도출**:
   * 구출된 토스트 XML 내부에 명기되어 있던 최종 플래그 값을 획득합니다:
     `picoCTF{sqlite_wal_p4g3_c4rv3d_uccessfully}`

## 5. 정답(플래그) 규칙 및 예시
* **플래그 형식**: `picoCTF{<flag_string>}`
* **예시**: `picoCTF{sqlite_wal_p4g3_c4rv3d_uccessfully}`

## 6. 출제자 노트 & 파일 제작 가이드
* **아티팩트 제작 방법**:
  1. Windows 10/11 가상 머신 환경에서 기밀 플래그 `picoCTF{sqlite_wal_p4g3_c4rv3d_uccessfully}` 값을 본문에 포함하는 사용자 토스트 알림을 임의로 발생시킵니다 (파워셸 `New-BurntToastNotification` 모듈 등을 활용 가능). (이 시점에 윈도우 셸이 알림 센터 데이터베이스 `wpndatabase.db`에 쓰기 동작을 유도하고, 관련 트랜잭션 정보가 `-wal` 캐시 파일에 선제 기입됩니다)
  2. 알림 센터를 수동으로 켜서 해당 알림 카드를 클릭 삭제 처리합니다.
  3. 알림 데이터베이스 저장 경로로 진입합니다:
     `%LOCALAPPDATA%\Microsoft\Windows\Notifications\wpndatabase.db`
  4. 메인 DB가 락이 걸린 틈을 이용해 백업되어 있던 `-wal` 트랜잭션 로그 파일인 `wpndatabase.db-wal` 전체를 로우 레벨로 덤프 복제하여 `wpndatabase_wal_dump.bin` 배포 이미지 파일로 저장해 제공합니다.
* **출제 포인트**: 
  * 로컬 애플리케이션 SQLite 데이터베이스 본문에서 데이터가 삭제(Delete Transaction)되어 DB 테이블상으로는 공란인 복잡한 안티 포렌식 위협 환경에서, 데이터베이스 저수준 로깅 아키텍처(SQLite WAL Transaction Page Forensics)의 물리 프레임 흔적을 역추적 파싱하여 소거되었던 XML 감사 알림 이력을 완벽히 입증 복구해 내는 전문 수사 역량을 검증합니다.

## 7. 트러블슈팅 및 힌트
* **Q. WAL(Write-Ahead Log) 파일이란 무엇이며 메인 DB와 어떻게 연동하나요?**
  * A. WAL 파일은 SQLite가 트랜잭션 충돌을 방지하고 쓰기 속도를 고속화하기 위해 사용하는 임시 로그 파일입니다. 사용자가 데이터를 쓰거나 변경할 때 메인 DB인 `.db` 파일에 즉시 쓰지 않고, `-wal` 파일의 프레임 페이지에 먼저 덧붙여(Append-only) 쓴 뒤 백그라운드 동기화 주기가 돌아오면 메인 DB로 일괄 병합(Checkpoint/Commit)합니다. 따라서 체크포인트가 수행되어 파일 크기가 갱신되기 전 단계라면, 메인 DB에서 SQL `DELETE` 구문으로 완전 소거된 데이터 레코드라도 `-wal` 파일 내의 과거 기록 트랜잭션 페이지 프레임에는 평문 상태로 온전히 잔재하므로 복구 조사의 제1 순위 아티팩트로 활용됩니다.
* **Q. strings 검색 시 문자열이 왜 깨지거나 누락되어 출력되나요?**
  * A. 윈도우 알림 센터 DB 내의 XML 토스트 본문 문자열은 데이터베이스 인코딩 규격상 **유니코드 UTF-16LE** 포맷으로 바인딩되어 적재되는 경우가 흔합니다. 일반적인 strings 명령어는 8비트 ASCII 문자 위주로만 파싱하므로, 유니코드 흔적을 찾으려면 strings 도구에 유니코드 전용 인코딩 옵션(`-e l` - 16-bit little-endian)을 덧붙여 수행해야 누락 없이 정확한 전체 XML 문자열을 화면에 복구 인쇄할 수 있습니다:
     `strings -e l wpndatabase_wal_dump.bin | grep "picoCTF"`

## 8. 학습 포인트
* **SQLite 데이터베이스 WAL 구조**: write-ahead logging 프레임 레이아웃 배치 명세 및 삭제 트랜잭션의 물리적 캐시 잔재 원리를 학습합니다.
* **알림 센터 아티팩트 복구**: 윈도우 시스템 감사 과정에서 SQLite WAL 미할당 가상 페이지 영역을 수동 카빙하여, 소멸되었던 기밀 XML 알림 본문 데이터를 안전하게 환원해 증적을 규명하는 역량을 갖춥니다.
