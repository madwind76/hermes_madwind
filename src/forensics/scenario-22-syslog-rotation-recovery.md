---
title: 잘려진 로그 조각의 복원 (Syslog Rotation Recovery)
created: 2026-06-28
updated: 2026-06-28
type: ctf-challenge
tags: [ctf, ctf-challenge, forensics, log, log-rotation, syslog, auth-log, zgrep]
confidence: high
---

# 잘려진 로그 조각의 복원 (Syslog Rotation Recovery)

> **난이도**: 초중급  
> **소요 시간**: 20~25분  
> **참고 picoCTF 문제**: 시스템 감사 로그 유실 복구 및 분석 (리눅스 Logrotate 아티팩트 추적)

## 1. 배경 시나리오
보안 위협 팀은 사내 중요 형상 관리 서버에 관리자 권한으로 로그인한 비인가 흔적을 확인하고 웹 관리 콘솔을 대조했습니다. 침해사고 대응 시점, 피해 시스템의 `/var/log/auth.log` 및 `/var/log/syslog` 활성 로그 파일은 크기가 0바이트로 초기화되어 있거나 삭제되어 비어 있었습니다. 공격자가 추적을 피하기 위해 감사 서비스(rsyslog) 활성 로그를 소거한 것입니다. 그러나 다행히 리눅스 커널 데몬의 **로그 로테이션(Logrotate) 정책**에 의해 과거 시점에 압축 백업된 과거 로그 조각들이 그대로 남아 있었습니다. 이 로테이트된 로그를 분석해 해킹 당시 사용된 계정명과 최초 로그인 성공 시각(HHMM), 그리고 침입자 IP를 찾아야 합니다.

## 2. 제공 파일
* `rotated_logs.zip` (로테이션되어 압축 보존 중이던 로그 파일 묶음)
  * 포함 파일: `auth.log.1`, `auth.log.2.gz`, `auth.log.3.gz`, `syslog.1`, `syslog.2.gz`

## 3. 문제 목표
리눅스의 로그 로테이션(Logrotate) 아카이빙 메커니즘을 이해하고, 압축 해제 없이 압축된 텍스트 로그 파일 내부를 쿼리할 수 있는 도구(`zcat`, `zgrep` 등)를 활용하여 지워진 활성 로그 이전 단계의 침투 타임라인 로그를 복원하여 세부 정보(로그인 계정명, IP, 시각)를 찾아냅니다.

## 4. 의도한 풀이 흐름
1. **아카이브 압축 해제**:
   * 제공된 `rotated_logs.zip` 파일의 압축을 해제하여 개별 로그 파일 구조를 확인합니다.
2. **압축 로그 검색 도구 활용**:
   * 활성 로그(`auth.log`)가 지워진 것을 확인한 후, 순차적으로 백업된 `auth.log.1`, `auth.log.2.gz`, `auth.log.3.gz`를 추적합니다.
   * `gz` 압축 로그는 압축을 일일이 풀지 않고 `zgrep` 명령어로 다이렉트 검색이 가능합니다:
     ```bash
     zgrep -i "Accepted" auth.log.3.gz
     ```
   * 혹은 최근 성공한 로그인 이력을 전체적으로 출력합니다:
     ```bash
     zgrep "Accepted publickey" auth.log.*.gz
     ```
3. **침해 이벤트 라인 식별**:
   * 검색 결과 `auth.log.3.gz` 파일 내부에서 다음과 같이 외부 대역으로부터 관리자 계정 권한으로 로그인에 성공한 이벤트 로그를 탐지합니다:
     `Jun 23 18:42:01 target-server sshd[1204]: Accepted publickey for backup_admin from 192.168.12.99 port 48218 ssh2: RSA ...`
   * 로그 상세 정보 추출:
     * 로그인 계정: `backup_admin`
     * 공격자 IP: `192.168.12.99`
     * 최초 성공 시간: `18:42` (현지 시각 기준 1842)
4. **플래그 구성**:
   * 계정명, IP, 시각(HHMM) 정보를 언더스코어로 조합해 플래그를 제출합니다:
     `picoCTF{backup_admin_192.168.12.99_1842}`

## 5. 정답(플래그) 규칙 및 예시
* **플래그 형식**: `picoCTF{<account_name>_<attacker_ip>_<HHMM>}`
* **예시**: `picoCTF{backup_admin_192.168.12.99_1842}`

## 6. 출제자 노트 & 파일 제작 가이드
* **아티팩트 제작 방법**:
  1. 가상 리눅스 환경에서 `logrotate` 동작을 시뮬레이션하거나 수동으로 로그 시나리오를 구성합니다.
  2. `auth.log` 원시 파일에 비인가 접속 기록을 삽입합니다:
     `Jun 23 18:42:01 server sshd[1204]: Accepted publickey for backup_admin from 192.168.12.99 port 48218 ssh2: RSA ...`
  3. 이 로그가 담긴 텍스트 파일을 `gzip` 명령을 이용해 강제로 로테이트 압축 파일 형태로 변조하여 생성합니다:
     `gzip -c auth.log > auth.log.3.gz`
  4. 침해 발생일 이후의 최근 며칠간 정상 활동 이력(로그인 성공/실패 소량)을 `auth.log.1`과 `auth.log.2.gz`에 섞어 타임라인의 현실성을 갖춥니다.
  5. 활성 파일 `auth.log`는 빈 파일(0바이트)로 두어 공격자가 흔적을 지웠음을 나타내고, 이를 한데 모아 `rotated_logs.zip`으로 아카이빙합니다.
* **출제 포인트**: 
  * 리눅스의 표준 로그 보존 체계와 `logrotate` 설정에 따른 아티팩트 잔재를 활용해 안티 포렌식 행위를 극복하는 모니터링 분석력을 기릅니다.

## 7. 트러블슈팅 및 힌트
* **Q. zgrep 명령어를 윈도우 환경에서 사용할 수 없나요?**
  * A. 윈도우 파워셸 환경의 경우 `zgrep`이 내장되어 있지 않으므로 7-Zip 등을 통해 `gz` 압축을 수동 해제한 뒤 `Select-String` 명령을 사용하거나, 리눅스 WSL 환경으로 전환하여 CLI 유틸리티를 사용하는 쪽이 더 편리합니다.
* **Q. syslog와 auth.log 중 침입 흔적은 어디서 주로 검출되나요?**
  * A. 데비안/우분투 계열 리눅스는 사용자 로그인 및 권한 상승(sudo) 기록을 `/var/log/auth.log`에 독립 보존하며, 레드햇/센트오에스 계열은 `/var/log/secure`에 저장합니다. `syslog`나 `messages`는 시스템 일반 작동 로그를 다루므로 인증 흔적은 `auth` 또는 `secure`를 우선 조회해야 합니다.

## 8. 학습 포인트
* **로그 로테이션(Log Rotation)**: 로그의 무한 비대를 방지하기 위해 파일 크기나 날짜 주기에 따라 압축 이동시키는 리눅스 파일 관리 구조를 상세히 이해합니다.
* **압축 텍스트 분석**: CPU 및 디스크 I/O 자원을 절약하며 대규모 데이터 압축 파일 내 특정 패턴을 고속 탐색하는 기법(zgrep, zcat, zless 등)을 실무에 적용합니다.
