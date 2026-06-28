---
title: 안드로이드 DB 백업 해독 (Android SQLite Backup Decryption)
created: 2026-06-28
updated: 2026-06-28
type: ctf-challenge
tags: [ctf, ctf-challenge, forensics, mobile, android, sqlcipher, sqlite, decryption]
confidence: high
---

# 안드로이드 DB 백업 해독 (Android SQLite Backup Decryption)

> **난이도**: 초중급  
> **소요 시간**: 25~30분  
> **참고 picoCTF 문제**: 모바일 데이터베이스 보안 해독 및 추출 (Android SQLCipher DB 포렌식)

## 1. 배경 시나리오
모바일 메신저 앱을 통해 내부 정보 유출 통로로 사용된 것으로 의심되는 피의자의 안드로이드(Android) 스마트폰 기기를 확보했습니다. 피의자는 메신저 대화방을 나갔다고 진술했으나, 백업 파일 데이터 아카이브 내에서 암호화 보존 중이던 메신저 로컬 데이터베이스 파일 `chat.db`를 발견했습니다. 이 DB는 상용 데이터베이스 암호화 솔루션인 **SQLCipher**로 전체 보호되어 있어 일반 SQLite 뷰어로는 읽을 수 없습니다. 다행히 백업 구성 파일인 `backup_metadata.xml` 내에서 암호 해독을 위한 마스터 키 생성 힌트를 발견했습니다. 두 파일을 연계 분석해 **대화 내용 내에 숨어 있는 플래그 문자열**을 복원해야 합니다.

## 2. 제공 파일
* `chat.db` (SQLCipher로 암호화된 메신저 SQLite 데이터베이스 파일)
* `backup_metadata.xml` (마스터 암호 힌트 및 암호 설정 메타데이터 XML 파일)

## 3. 문제 목표
모바일 앱 포렌식에서 자주 사용되는 암호화 SQLite(SQLCipher) 메커니즘을 이해하고, 메타데이터 XML을 통해 유도한 올바른 해독 키(Key/Passphrase)를 대입하여 DB 잠금을 해제한 뒤 SQL 질의문을 통해 특정 메시지 내의 플래그를 복구합니다.

## 4. 의도한 풀이 흐름
1. **마스터 패스프레이즈 획득 (XML 분석)**:
   * 제공된 `backup_metadata.xml` 파일을 텍스트 뷰어로 열어 구조를 분석합니다.
   * XML 노드 내에서 다음과 같이 패스프레이즈 힌트와 솔트 설정 값을 식별합니다:
     ```xml
     <crypto_config>
         <pbkdf2_iterations>10000</pbkdf2_iterations>
         <salt>4f2a9e3b</salt>
         <passphrase_hint>company_secrets_2026</passphrase_hint>
     </crypto_config>
     ```
   * 해독에 필요한 마스터 암호 키가 `company_secrets_2026` 임을 확정합니다.
2. **SQLCipher 복호화 연계**:
   * 일반 SQLite 파서로 `chat.db`를 읽어들이면 `file is not a database` 또는 `encrypted` 에러가 나며 테이블 조회가 불가함을 사전에 인지합니다.
   * **도구 활용**: `DB Browser for SQLite` (SQLCipher 복호화 확장 지원 버전)을 엽니다.
   * `chat.db`를 선택해 연 뒤, 비밀번호 입력창에서 암호 설정 모드를 `SQLCipher 3` 또는 `SQLCipher 4` 기본값으로 두고 패스워드로 `company_secrets_2026`을 대입합니다.
   * **CLI 활용 (sqlcipher-shell)**:
     ```bash
     sqlcipher chat.db
     ```
     쉘 내부에서 다음 PRAGMA 명령을 차례로 인가해 잠금을 해제합니다:
     ```sql
     PRAGMA key = 'company_secrets_2026';
     .tables
     ```
3. **데이터베이스 쿼리 및 데이터 추출**:
   * 잠금 해제에 성공하여 테이블 스키마가 로드되면 `messages` 테이블을 조회합니다.
   * 플래그 포맷(`picoCTF`)을 포함하는 메시지를 추출하는 쿼리를 작성해 가동합니다:
     ```sql
     SELECT message FROM messages WHERE message LIKE '%picoCTF%';
     ```
   * 대화 결과 튜플에서 다음 플래그가 전송된 레코드를 검출합니다:
     `picoCTF{sqlcipher_mobile_db_decrypted}`

## 5. 정답(플래그) 규칙 및 예시
* **플래그 형식**: `picoCTF{<flag_string>}`
* **예시**: `picoCTF{sqlcipher_mobile_db_decrypted}`

## 6. 출제자 노트 & 파일 제작 가이드
* **아티팩트 제작 방법**:
  1. 리눅스 환경에서 `sqlcipher` 도구를 설치합니다.
  2. 다음 SQL 쉘 세션 명령을 통해 테이블을 만들고 암호화 데이터를 저장합니다:
     ```bash
     sqlcipher chat.db
     ```
     ```sql
     PRAGMA key = 'company_secrets_2026';
     CREATE TABLE messages (id INTEGER PRIMARY KEY, sender TEXT, message TEXT);
     INSERT INTO messages (sender, message) VALUES ('Suspect', 'Flag has been sent: picoCTF{sqlcipher_mobile_db_decrypted}');
     .exit
     ```
  3. 완성된 `chat.db`가 암호화되지 않은 일반 SQLite 뷰어로는 전혀 파싱되지 않는지 이중 검증합니다.
  4. 암호 힌트 명세 노드를 수록한 `backup_metadata.xml` 파일을 별도로 구성하여 배포 아티팩트로 지정합니다.
* **출제 포인트**: 
  * 모바일 앱 포렌식(Android/iOS) 시 단말기 샌드박스 내부의 중요 앱 데이터를 덤프한 후 암호화되어 막히는 상황(SQLCipher Lock)을 극복하고 백업 설정 힌트와 연계해 복구하는 실무 역량을 기릅니다.

## 7. 트러블슈팅 및 힌트
* **Q. 올바른 키를 입력했는데도 여전히 파일이 암호화되어 있어 읽을 수 없다는 에러가 납니다.**
  * A. SQLCipher는 릴리즈 버전(V3, V4 등)에 따라 기본 암호화 팩(KDF 알고리즘, 해시 라운드 수 등) 규격이 다릅니다. 최신 V4 라이브러리로 빌드된 DB를 하위 버전 V3 도구로 열려고 하면 암호가 틀렸다고 에러가 날 수 있으므로, 복호화 툴 설정에서 페이지 크기(Page Size, 주로 4096)와 알고리즘 버전을 변경하며 재시도하십시오.
* **Q. 파이썬 스크립트에서 이를 해독하고 싶습니다.**
  * A. `pysqlcipher3` 패키지를 설치한 후 `db.cursor().execute("PRAGMA key = 'company_secrets_2026'")` 구문을 커넥션 직후 가장 먼저 처리해 주어야 하며, 에러 차단을 위해 설치 시점에 로컬 openssl 라이브러리 빌드 환경이 구비되어 있어야 합니다.

## 8. 학습 포인트
* **SQLCipher 암호화 작동 방식**: SQLite 파일 페이지 단위(Page-by-page)로 AES 암호화를 적용하며 솔트(Salt) 값을 파일 헤더 첫 섹터에 상주시키는 구조를 학습합니다.
* **모바일 아티팩트 해독**: 기기 백업 파일 내에 산재하는 암호화 보존 데이터베이스를 설정 구성 힌트 파일과 교차 조합하여 평문으로 변환해 내는 분석 논리를 이해합니다.
