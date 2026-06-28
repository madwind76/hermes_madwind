---
title: 지워진 SQLite 레코드 복구 (SQLite Free List Page Carving)
created: 2026-06-28
updated: 2026-06-28
type: ctf-challenge
tags: [ctf, ctf-challenge, forensics, db, sqlite, freelist, carving, deleted-records, strings]
confidence: high
---

# 지워진 SQLite 레코드 복구 (SQLite Free List Page Carving)

> **난이도**: 초중급  
> **소요 시간**: 25~30분  
> **참고 picoCTF 문제**: 데이터베이스 무삭제 복구 및 카빙 (SQLite Freelist 및 Slack 분석)

## 1. 배경 시나리오
사내 중요 영업 기밀 유출 혐의자가 메신저 대화방 데이터베이스인 SQLite 파일 `records.db`에서 핵심 유출 이력이 담긴 메시지 레코드를 SQL `DELETE` 명령어로 삭제했습니다. 용의자는 레코드를 완벽히 소거하여 흔적을 지웠다고 주장하고 있으며, 실제 데이터베이스 관리도구로 해당 테이블을 열면 행(Row)들이 전혀 나타나지 않고 비어 있습니다. 하지만 SQLite 데이터베이스는 삭제 명령어 수행 시 파일 크기를 바로 줄이지 않고, 삭제된 레코드가 차지하던 블록을 **프리리스트(Freelist) 페이지** 또는 페이지 내부의 **프리블록(Freeblock) 체인**으로 등록하여 재사용 대기 상태로만 전환합니다. 별도의 `VACUUM` 명령을 내려 최적화하지 않는 한 삭제된 데이터 바이트는 물리적으로 그대로 남아 있습니다. 데이터베이스의 미할당 영역을 수동 카빙하여 **삭제되었던 메시지 속의 플래그**를 구출해야 합니다.

## 2. 제공 파일
* `records.db` (핵심 데이터 행이 SQL DELETE로 지워진 SQLite 데이터베이스 파일)

## 3. 문제 목표
SQLite 데이터베이스의 물리 페이지 구조(Page Header, Freeblock, Freelist Page) 및 데이터 소거 메커니즘을 이해하고, 원시 바이너리 덤프에서 덮어써지지 않고 대기 상태로 잔재하는 원시 텍스트 필드를 문자열 카빙 유틸리티 또는 헥스 스캐닝으로 검출 및 복구해 냅니다.

## 4. 의도한 풀이 흐름
1. **데이터베이스 가상 조회**:
   * 제공된 `records.db` 파일을 일반 SQLite 브라우저로 엽니다.
   * `secrets` 테이블을 열어보지만 데이터가 0건으로 조회되어 논리적으로 삭제된 상태임을 확인합니다.
2. **미할당 및 프리리스트 물리 카빙**:
   * SQLite는 데이터가 삭제되어 프리리스트로 반환되어도 파일 헤더를 재구성해 공간을 비워둘 뿐 기존 레코드 바이트를 `0x00`으로 덮어쓰지(Zero-out) 않습니다.
   * **CLI 덤프 스캔**: 터미널에서 바이너리 평문 문자열 추출 명령어(`strings`)를 가동하여 플래그 헤더(`picoCTF`)를 다이렉트로 스캔합니다:
     ```bash
     strings records.db | grep "picoCTF"
     ```
   * **수동 헥스 분석**: 헥스 에디터로 `records.db` 파일을 열어 하위 페이지 영역 중 미할당 데이터 슬랙 영역에서 지워지지 않은 평문 데이터 구조를 눈으로 직접 탐색합니다.
3. **플래그 도출**:
   * 스캔 결과 프리리스트 바이트 블록 중간에서 원본 레코드 잔재 문자열을 획득합니다:
     `picoCTF{sqlite_freelist_data_carved}`

## 5. 정답(플래그) 규칙 및 예시
* **플래그 형식**: `picoCTF{<flag_string>}`
* **예시**: `picoCTF{sqlite_freelist_data_carved}`

## 6. 출제자 노트 & 파일 제작 가이드
* **아티팩트 제작 방법**:
  1. 리눅스 CLI 환경에서 일반 `sqlite3` 데이터베이스 세션을 엽니다:
     `sqlite3 records.db`
  2. 테이블을 만들고 기밀 플래그 데이터를 인서트합니다:
     ```sql
     CREATE TABLE secrets (id INTEGER PRIMARY KEY, content TEXT);
     INSERT INTO secrets (content) VALUES ("The flag is picoCTF{sqlite_freelist_data_carved}");
     ```
  3. 등록된 데이터를 삭제합니다:
     `DELETE FROM secrets WHERE id = 1;`
     *(이때 절대로 `VACUUM;` 명령을 수행하면 안 됩니다. VACUUM이 가동되면 데이터베이스 엔진이 물리 파일 전체를 재작성하여 삭제된 프리리스트 바이트가 완전히 소멸합니다)*
  4. 세션을 종료하고 `records.db` 파일 바이너리를 추출하여 배포 아티팩트로 사용합니다.
* **출제 포인트**: 
  * 디렉터리 파일 삭제뿐만 아니라, 어플리케이션이 개별 관리하는 관계형 로컬 데이터베이스(SQLite Forensics) 내부의 논리적 삭제 처리가 보존하는 물리 슬랙 잔재 영역의 증거 보존 가치를 체득하게 유도합니다.

## 7. 트러블슈팅 및 힌트
* **Q. strings 명령을 날렸는데 아무것도 나오지 않습니다.**
  * A. 피의자가 삭제 쿼리 실행 직후 `VACUUM` 명령어를 수동 인가했거나, 데이터베이스 자동 압축 옵션(`auto_vacuum`)이 활성화되어 있었을 가능성이 있습니다. 이 문제 아티팩트 `records.db`는 수동 삭제 후 프리리스트가 잔재하도록 구성되었으므로 strings 및 hex 카빙 기법으로 확실히 복원이 가능합니다.
* **Q. 삭제된 레코드가 너무 많아서 깨져 있는 경우, 정확히 바이트 구조를 맞춰 파싱하는 도구는 없나요?**
  * A. sqlparse 패키지나 **sqlitedeletedr** 또는 **SQLiteParser** 등의 전문 복구 스크립트를 사용하면, SQLite 페이지 내부의 프리블록 오프셋 링크 구조체를 추적하여 지워진 테이블의 데이터 타입(정수형, 텍스트형 등)에 맞춰 완벽한 SQL 덤프로 행을 자동 복구해 줍니다.

## 8. 학습 포인트
* **SQLite 데이터베이스 내부 사양**: B-Tree 기반 페이지 분할 구조와 프리블록(Freeblock) 체인, 프리리스트(Freelist) 트렁크/리프 페이지의 동작 방식을 이해합니다.
* **DB 슬랙 카빙(DB Slack Carving)**: 데이터 소거 연산 후 애플리케이션 파일 내부의 비활성 영역을 헥스 레벨로 분석해 증거를 발굴하는 메커니즘을 마스터합니다.
