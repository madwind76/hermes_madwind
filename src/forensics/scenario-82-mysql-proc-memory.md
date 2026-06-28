---
title: 리눅스 프로세스 메모리 속 데이터베이스 쿼리 추출 (Linux mysql process memory dump)
created: 2026-06-28
updated: 2026-06-28
type: ctf-challenge
tags: [ctf, ctf-challenge, forensics, linux, memory, mysql, database, process-dump, strings]
confidence: high
---

# 리눅스 프로세스 메모리 속 데이터베이스 쿼리 추출 (Linux mysql process memory dump)

> **난이도**: 초중급  
> **소요 시간**: 25~30분  
> **참고 picoCTF 문제**: 데이터베이스 가상 메모리 기밀 쿼리 카빙 (Linux mysqld Memory 분석)

## 1. 배경 시나리오
사내 중요 고객 기밀 정보가 담긴 데이터베이스 서버에 원격 관리자 계정을 도용한 불법 조회(Data Exfiltration) 행위가 일어난 것으로 의심됩니다. 공격자가 데이터를 조회한 직후 DB 서버 로그 및 히스토리 파일을 강제로 훼손해 두어 파일시스템 증적 조사가 불가능한 상황입니다. 다행히도 이상 징후가 지속되던 런타임 당시에 데이터베이스 핵심 데몬인 **MySQL Server (`mysqld`)** 프로세스의 가상 메모리를 강제 덤프(Core Dump)하여 보존하는 데 성공했습니다. 수집된 이진 메모리 파일 `mysql_server_memory.dmp`를 분석하여, **동작 중 메모리 힙 버퍼에 평문 상태로 일시 잔재해 남아있던 공격자의 기밀 조회 SQL 쿼리문 속의 플래그**를 구출하십시오.

## 2. 제공 파일
* `mysql_server_memory.dmp` (MySQL 서비스 데몬 `mysqld` 프로세스의 가상 메모리 세그먼트 공간에서 수집 덤프한 코어 파일)

## 3. 문제 목표
관계형 데이터베이스 서비스(MySQL/MariaDB 등)가 원격 또는 로컬 클라이언트로부터 접속 요청을 수신하고 SQL 쿼리를 해석 및 처리할 때, 성능 최적화(파싱/캐싱) 목적으로 메모리 힙 영역에 평문 상태의 쿼리 원본을 일시 보존하는 구간이 존재함을 이해하고, 프로세스 덤프 바이너리에서 평문 쿼리를 색인해 냅니다.

## 4. 의도한 풀이 흐름
1. **메모리 덤프 가독 문자열 스캔**:
   * 제공된 `mysql_server_memory.dmp` 파일에서 문자열 데이터를 격리 수집하기 위해 `strings` 명령어를 실행하고 플래그 포맷을 검색합니다:
     ```bash
     strings mysql_server_memory.dmp | grep "picoCTF"
     ```
2. **평문 SQL 쿼리 획득**:
   * 검색 결과, `mysqld` 프로세스가 쿼리 문맥 파싱을 위해 메모리에 구성한 힙 버퍼 영역 주소에서 다음과 같이 비인가 접속자가 날린 SQL 쿼리 레코드를 식별해 냅니다:
     `SELECT flag FROM secrets WHERE token = 'picoCTF{mysql_query_dump_m3m_carv3d}'`
3. **플래그 도출**:
   * SQL 쿼리문 내부에 박제되어 있던 최종 플래그 값을 획득합니다:
     `picoCTF{mysql_query_dump_m3m_carv3d}`

## 5. 정답(플래그) 규칙 및 예시
* **플래그 형식**: `picoCTF{<flag_string>}`
* **예시**: `picoCTF{mysql_query_dump_m3m_carv3d}`

## 6. 출제자 노트 & 파일 제작 가이드
* **아티팩트 제작 방법**:
  1. 테스트 리눅스 환경에 MySQL 또는 MariaDB 데이터베이스 서비스를 활성화합니다.
  2. 임의의 셸 또는 데이터베이스 클라이언트를 사용하여 기밀 플래그가 주입된 쿼리를 강제 기동합니다:
     `SELECT flag FROM secrets WHERE token = 'picoCTF{mysql_query_dump_m3m_carv3d}';`
  3. 쿼리 기동 직후(데이터베이스가 기동 세션을 메모리에 적재 보존 중인 타이밍), 실행 중인 `mysqld` 프로세스의 PID를 획득하여 코어 덤프를 생성합니다:
     `gcore -o mysql_server_memory <mysqld_PID>`
  4. 덤프된 바이너리 이미지 내에 위 SQL 쿼리 텍스트 라인이 깨짐 없이 평문 잔재하는지 strings 검수를 수행하고, 분석 가치가 높은 유효 힙 페이지 영역을 조절 격리하여 `mysql_server_memory.dmp` 배포 파일로 저장합니다.
* **출제 포인트**: 
  * 디바이스 상의 시스템 및 애플리케이션 감사 로그(Audit Logs, DB Query History)가 안티 포렌식 공격에 의해 소거된 극단적인 기밀 유출 상황에 맞서, 휘발성 메모리 상에 상주 가동 중인 데이터베이스 프로세스 덤프(Database Process Memory Forensics) 분석을 가동하여 피의자가 수행한 민감 SQL 쿼리 구문을 역추적 및 규명하는 고급 침해 분석 기법을 학습시킵니다.

## 7. 트러블슈팅 및 힌트
* **Q. mysql 프로세스를 덤프할 때 권한 문제가 발생합니다.**
  * A. MySQL 데몬 프로세스는 보안상 root가 아닌 `mysql` 전용 가상 시스템 사용자 계정 권한으로 백그라운드 구동됩니다. 따라서 일반 사용자 권한으로는 해당 프로세스의 가상 메모리 주소 매핑(/proc/<PID>/mem)을 읽어들일 수 없으므로, 반드시 root 관리자 권한을 확보한 상태에서 `gcore`나 `dd` 덤프 커맨드를 수행해야 덤프 동작이 성립합니다.
* **Q. 메모리 내의 SQL 쿼리는 로그오프 후에도 남아있나요?**
  * A. 클라이언트 세션이 닫히면 MySQL 엔진은 해당 가상 세션에 할당했던 커넥션 메모리 풀을 반환(`free`) 처리합니다. 하지만 운영체제 및 프로세스 런타임 힙 메모리 관리 정책상, 해당 반환 영역은 다른 신규 데이터로 완전히 덮어써지기(Overwrite) 전까지는 이전 작성 평문 바이트 흔적이 힙 슬랙(Heap Slack) 공간에 고스란히 영구 고착화되어 보존되므로 사고 발생 수 시간 이내라면 충분히 덤프 카빙으로 역추적 가능합니다.

## 8. 학습 포인트
* **데이터베이스 메모리 할당 체계**: 관계형 DB 데몬의 런타임 쿼리 해석 및 세션 버퍼(Connection Pool) 적재 정책을 학습합니다.
* **프로세스 덤프 카빙**: 안티 포렌식(DB 로그 삭제) 공격을 우회하기 위해, 가상 메모리 프로세스 덤프를 카빙 파싱하여 중요 평문 기밀(SQL Queries)을 복원 및 식별하는 분석 기법을 습득합니다.
