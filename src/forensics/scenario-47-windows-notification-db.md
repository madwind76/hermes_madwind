---
title: 윈도우 알림 센터 DB 분석 (Windows Notification Center DB)
created: 2026-06-28
updated: 2026-06-28
type: ctf-challenge
tags: [ctf, ctf-challenge, forensics, windows, notification, wpndatabase, sqlite, xml-toast]
confidence: high
---

# 윈도우 알림 센터 DB 분석 (Windows Notification Center DB)

> **난이도**: 초급  
> **소요 시간**: 15~20분  
> **참고 picoCTF 문제**: 윈도우 앱 아티팩트 및 사용자 알림 이력 분석 (wpndatabase.db 포렌식)

## 1. 배경 시나리오
사내 정보 유출 사고 조사 대상자인 피의자는 업무 중 보안 승인 키가 포함된 중요 인스턴트 메시지를 메신저 팝업 알림으로 수신한 후, 증거를 인멸하기 위해 해당 메신저 프로그램 자체를 즉시 제어판에서 완전 제거(Uninstall)했습니다. 그러나 윈도우 OS는 팝업 형태로 화면 우측 하단에 생성되는 모든 앱 알림 창의 텍스트 본문(Toast Notification)을 로컬 사용자 앱 데이터 폴더 하위의 **알림 센터 데이터베이스(`wpndatabase.db`)**에 SQLite 포맷으로 임시 저장하여 이력을 관리합니다. 피의자 계정의 알림 데이터베이스 파일을 분석하여 **수신되었던 알림 팝업 속의 보안 플래그**를 찾아내십시오.

## 2. 제공 파일
* `wpndatabase.db` (피의자 윈도우 프로필에서 복구한 알림 센터 DB 파일 - SQLite 포맷)

## 3. 문제 목표
윈도우 알림 센터의 캐싱 기법 및 데이터베이스 저장 경로(`%LOCALAPPDATA%\Microsoft\Windows\Notifications\wpndatabase.db`)를 파악하고, SQLite 쿼리 도구를 사용하여 알림 레코드 테이블 내부의 XML 토스트 페이로드 데이터를 추출 및 필터링하여 기밀 텍스트를 복구합니다.

## 4. 의도한 풀이 흐름
1. **데이터베이스 확인**:
   * 제공된 `wpndatabase.db` 파일을 SQLite 뷰어 도구(`DB Browser for SQLite` 등)로 로드합니다.
   * CLI 환경의 경우 터미널에서 `sqlite3`를 통해 데이터베이스 스키마와 테이블 목록을 쿼리합니다:
     ```bash
     sqlite3 wpndatabase.db ".tables"
     ```
   * 이력 보존 테이블인 **Notification** 테이블의 존재를 식별합니다.
2. **테이블 쿼리 및 데이터 정제**:
   * `Notification` 테이블의 컬럼 스키마를 확인합니다. 각 알림의 데이터 본문은 **Payload** 컬럼에 XML 포맷 문자열로 저장되어 있습니다.
   * `Payload` 데이터 필드 중 플래그 키워드(`picoCTF`)가 수록되어 있는지 검색 질의를 날립니다:
     ```sql
     SELECT Payload FROM Notification WHERE Payload LIKE '%picoCTF%';
     ```
3. **XML 데이터 파싱 및 플래그 획득**:
   * 쿼리 결과로 출력되는 토스트 알림 명세 XML 데이터를 획득합니다:
     ```xml
     <toast><visual><binding template="ToastText02"><text id="1">Security Alert</text><text id="2">Your secure code is picoCTF{w1nd0ws_n0tific4t1on_c3nt3r_r3c0v3ry}</text></binding></visual></toast>
     ```
   * 알림 텍스트 노드 `<text id="2">` 영역에 기록되어 있는 비밀 코드를 추출합니다:
     `picoCTF{w1nd0ws_n0tific4t1on_c3nt3r_r3c0v3ry}`

## 5. 정답(플래그) 규칙 및 예시
* **플래그 형식**: `picoCTF{<flag_string>}`
* **예시**: `picoCTF{w1nd0ws_n0tific4t1on_c3nt3r_r3c0v3ry}`

## 6. 출제자 노트 & 파일 제작 가이드
* **아티팩트 제작 방법**:
  1. Windows 10/11 가상 머신에서 임의의 유틸리티(예: 파워셸의 BurntToast 모듈 등)를 사용하여 모의 알림을 발생시킵니다:
     `New-BurntToastNotification -Text "Security Alert", "Your secure code is picoCTF{w1nd0ws_n0tific4t1on_c3nt3r_r3c0v3ry}"`
  2. 로컬 앱 데이터 저장 경로로 진입합니다:
     `%LOCALAPPDATA%\Microsoft\Windows\Notifications\`
  3. 숨김 해제 후 해당 폴더 내의 SQLite 파일인 `wpndatabase.db` 파일을 확보합니다.
  4. 테스트 데이터 외에 타임라인 리셋에 방해되지 않는 더미 시스템 알림 수십 개만 유지한 채 SQLite 데이터베이스를 정제하여 배포 아티팩트로 지정합니다.
* **출제 포인트**: 
  * 사용자가 침해 소프트웨어를 완전히 삭제하여 앱 데이터 폴더가 날아가더라도, 윈도우 OS 수준에서 알림 패널 히스토리 보존 목적으로 타사 앱의 내용을 취합 및 영구 SQLite DB로 기록하는 구조(Windows Notifications Forensics)를 활용해 추적 사각지대를 극복하게 유도합니다.

## 7. 트러블슈팅 및 힌트
* **Q. sqlite3 구동 시 'database is locked' 에러가 납니다.**
  * A. 윈도우 로컬에서 실시간 구동 중인 알림 서비스를 완전히 끄지 않은 상태에서 활성 `wpndatabase.db`에 쓰기/읽기 동시 트랜잭션이 충돌해 발생할 수 있습니다. 본 문제에서 제공되는 독립 복제본 `wpndatabase.db` 파일을 사용하는 경우 락 에러 없이 정상 쿼리가 가능합니다.
* **Q. 알림 센터 DB에서 삭제된 과거 알림 데이터는 어떻게 복구하나요?**
  * A. 사용자가 알림 센터 우측 슬라이드 바에서 '모두 지우기'를 누르면 SQLite 테이블 내에서 레코드가 삭제됩니다. 이 경우 바로 다음 시나리오에서 다루는 **SQLite 프리리스트/미할당 공간 카빙** 기법을 적용하여 지워진 XML 텍스트 레코드 조각을 수동 발굴해야 복원할 수 있습니다.

## 8. 학습 포인트
* **윈도우 알림 센터 캐시 구조**: 다양한 어플리케이션(UWP 및 데스크톱 앱)의 Toast 팝업 내용이 OS 중앙 리포지토리(`wpndatabase.db`)에 수집 보존되는 원리를 파악합니다.
* **SQLite XML 구조체 파싱**: SQLite의 텍스트 필드 내부에 직렬화되어 매핑된 XML 노드 명세에서 특정 ID 기반 데이터만을 추출하는 쿼리 및 정제 기법을 훈련합니다.
