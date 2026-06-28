---
title: 브라우저에 남겨진 은밀한 활동 (Browser History Tracks)
created: 2026-06-28
updated: 2026-06-28
type: ctf-challenge
tags: [ctf, ctf-challenge, forensics, browser, chrome, sqlite, database, sql]
confidence: high
---

# 브라우저에 남겨진 은밀한 활동 (Browser History Tracks)

> **난이도**: 초급  
> **소요 시간**: 15~20분  
> **참고 picoCTF 문제**: 웹 브라우저 사용자 행동 흔적 분석 (Chrome History SQLite DB 쿼리 연계)

## 1. 배경 시나리오
사내 자산 유출 사고의 유력한 피의자로 지목된 내부자가 격리 조치 전 본인의 PC에서 크롬(Chrome) 브라우저의 방문 기록과 쿠키를 모두 수동으로 지웠다고 주장했습니다. 하지만 포렌식 분석가는 사용자 홈 디렉터리 하부의 크롬 사용자 프로필 경로에서 삭제되지 않고 동기화 중이던 SQLite 데이터베이스 파일인 `History` 파일을 추출하는 데 성공했습니다. 이 파일에 저장된 방문 주소와 파라미터 값을 분석해 **피의자가 접속했던 비밀 C2 서버 주소 및 주소 뒤에 파라미터 값으로 전달된 플래그**를 획득해야 합니다.

## 2. 제공 파일
* `History` (구글 크롬 브라우저의 방문 이력이 담긴 SQLite 3 데이터베이스 파일)

## 3. 문제 목표
크롬 브라우저의 방문 기록 보존 구조를 이해하고, SQLite 클라이언트 도구(sqlite3 CLI 또는 DB Browser for SQLite)를 사용해 데이터베이스 테이블 구조를 파악한 뒤, 특정 도메인 검색 쿼리를 실행하여 접속 주소 내 파라미터에 은닉된 플래그 정보를 획득합니다.

## 4. 의도한 풀이 흐름
1. **데이터베이스 확인**:
   * 리눅스 터미널에서 `file History` 명령어를 실행하여 파일이 SQLite 3 데이터베이스 포맷인지 재점검합니다.
2. **SQLite 데이터베이스 접속**:
   * 터미널에서 CLI 도구로 접속하거나 GUI 도구로 파일을 엽니다:
     `sqlite3 History`
3. **스키마 및 테이블 파악**:
   * `.tables` 명령어를 입력해 테이블 목록을 확인합니다. 주요 테이블인 `urls` (방문한 URL 정보)와 `visits` (방문 시간 및 유입 정보) 테이블을 확인합니다.
   * `urls` 테이블의 스키마를 확인합니다:
     `.schema urls`
4. **URL 검색 및 필터링 쿼리 수행**:
   * 피의자가 접속한 기밀 또는 외부 도메인 흔적을 찾기 위해 `url` 컬럼에 대해 쿼리를 실행합니다:
     ```sql
     SELECT id, url, title, visit_count FROM urls WHERE url LIKE '%picoCTF%';
     ```
   * 혹은 최근 방문한 모든 외부 도메인 주소들을 정렬하여 비정상적인 IP/도메인을 조회합니다:
     ```sql
     SELECT url FROM urls ORDER BY last_visit_time DESC LIMIT 20;
     ```
   * 쿼리 결과로 출력된 특정 레코드에서 다음 형태의 비밀 주소를 발견합니다:
     `http://secret-c2-portal.xyz/login?token=picoCTF{sqlite_brows1ng_history_unlocked}`
5. **플래그 입력**: URL 파라미터 값으로 전달된 플래그 문자열을 추출하여 제출합니다.

## 5. 정답(플래그) 규칙 및 예시
* **플래그 형식**: `picoCTF{<flag_string>}`
* **예시**: `picoCTF{sqlite_brows1ng_history_unlocked}`

## 6. 출제자 노트 & 파일 제작 가이드
* **아티팩트 제작 방법**:
  1. 분석용 크롬 또는 크로미움(Chromium) 브라우저를 기동합니다.
  2. 주소창에 플래그가 포함된 모의 주소를 입력해 강제 접속합니다:
     `http://secret-c2-portal.xyz/login?token=picoCTF{sqlite_brows1ng_history_unlocked}`
  3. 브라우저를 닫고 크롬 사용자 프로필 디렉터리로 이동합니다:
     * Windows: `%LOCALAPPDATA%\Google\Chrome\User Data\Default\`
     * Linux: `~/.config/google-chrome/Default/`
  4. 해당 디렉터리 내의 `History` 파일을 복제합니다.
  5. 복제한 `History` 파일을 SQLite 편집기로 열어 다른 불필요한 개인 사생활 정보나 도메인 기록을 삭제(`DELETE FROM urls WHERE url NOT LIKE '%secret-c2%';` 등)하여 문제를 정제하고 경량화한 뒤 배포합니다.
* **출제 포인트**: 
  * 사용자의 모든 웹 서핑 행적을 추적할 수 있는 1차 아티팩트인 웹 브라우저 데이터베이스의 내부 스키마를 이해하고, 대용량 레코드 속에서 관계형 데이터베이스 쿼리 언어(SQL)를 사용해 필요한 침해 단서를 발굴하는 법을 실습합니다.

## 7. 트러블슈팅 및 힌트
* **Q. sqlite3 명령을 실행했는데 'database is locked' 에러가 뜹니다.**
  * A. 현재 해당 `History` 파일이 크롬 브라우저 프로세스에 의해 실시간으로 물려 사용 중일 때 발생합니다. 크롬 브라우저를 완전히 종료(프로세스 킬)하거나, `History` 파일을 다른 작업 디렉터리로 복사하여 복사본 파일에 대해 접속을 수행하십시오.
* **Q. URLs 테이블의 last_visit_time 시각 값이 1601년으로 시작하는 긴 숫자로 나옵니다.**
  * A. 크롬 브라우저는 시간을 UNIX 타임스탬프가 아닌, 1601년 1월 1일을 기준으로 하는 **Windows Webkit epoch (Microseconds since 1601/01/01)**을 사용합니다. 이를 사람이 읽을 수 있게 변환하려면 SQL 상에서 `datetime(last_visit_time / 1000000 - 11644473600, 'unixepoch')` 공식을 결합해 쿼리해야 합니다.

## 8. 학습 포인트
* **브라우저 아티팩트 구조**: 대표적인 웹 브라우저인 크롬이 사용자 활동 로그를 로컬 SQLite DB 파일 구조로 보존하는 메커니즘을 상세히 터득합니다.
* **데이터베이스 포렌식**: 텍스트 분석에 그치지 않고, 관계형 정형 데이터 구조에 직접 쿼리를 날려 용의자의 은밀한 접속 경로 및 웹 요청 헤더 매개변수(Parameter)를 역공학으로 복구하는 절차를 경험합니다.
