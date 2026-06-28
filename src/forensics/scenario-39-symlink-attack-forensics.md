---
title: 리눅스 심볼릭 링크 공격 분석 (Symlink Attack Analysis)
created: 2026-06-28
updated: 2026-06-28
type: ctf-challenge
tags: [ctf, ctf-challenge, forensics, linux, symlink, race-condition, auditd, audit-log]
confidence: high
---

# 리눅스 심볼릭 링크 공격 분석 (Symlink Attack Analysis)

> **난이도**: 초중급  
> **소요 시간**: 20~25분  
> **참고 picoCTF 문제**: 리눅스 특권 상승 및 파일시스템 경쟁 조건 감사 (Auditd 로그 분석)

## 1. 배경 시나리오
사내 중요 자산 서버에서 일반 사용자 계정 권한을 가진 내부 침입자가 루트(root) 권한으로 주기적으로 작동하던 백업 크론탭 스크립트를 공격했습니다. 이 스크립트는 임시 디렉터리 `/tmp/session_report.log` 파일에 결과를 기록하는 구조였습니다. 공격자는 이 쓰기 동작이 일어나기 직전, `/tmp/session_report.log` 명칭의 파일을 지우고 동일한 이름의 **심볼릭 링크(Symbolic Link)**를 생성해 시스템 루트 경로 하위의 기밀 플래그 파일로 연결함으로써 루트 프로세스가 플래그 파일 영역에 의도치 않은 데이터를 덮어쓰거나 열람하도록 유도했습니다. 감사 시스템(`auditd`)에 기록된 `/tmp` 디렉터리 파일시스템 감사 로그 `tmp_audit.log` 파일이 복구되었습니다. 이 로그를 분석해 **심볼릭 링크 공격의 타깃이 되었던 플래그 정보**를 복원해야 합니다.

## 2. 제공 파일
* `tmp_audit.log` (리눅스 커널 auditd 모듈이 수집한 임시 폴더 내 파일시스템 시스템 콜 로그 파일)

## 3. 문제 목표
리눅스의 심볼릭 링크 경쟁 조건(Symlink Race Condition) 취약성의 공격 기법을 이해하고, 리눅스 커널 감사 로그(`auditd`) 내에서 심볼릭 링크 생성 시스템 콜(`symlink`, 시스템콜 번호 83) 관련 엔트리를 식별 및 파싱하여 공격자가 대상으로 삼았던 원본 파일 절대 경로(플래그 포함)를 추출해 냅니다.

## 4. 의도한 풀이 흐름
1. **시스템 콜 추적**:
   * 제공된 `tmp_audit.log` 파일에서 심볼릭 링크 생성을 담당하는 시스템 호출 행을 검색합니다.
   * 리눅스에서 심볼릭 링크는 `symlink` 시스템 콜을 통해 수행되므로, 대소문자 구분 없이 해당 키워드를 필터링합니다:
     ```bash
     grep -i "symlink" tmp_audit.log
     ```
2. **감사 레코드 필드 매칭**:
   * 검색 결과 다음과 같은 구조의 `auditd` 레코드 필드 묶음을 식별합니다:
     ```text
     type=SYSCALL msg=audit(1719543822.428:1024): arch=c000003e syscall=83 success=yes exit=0 ... exe="/usr/bin/ln" key="tmp_watch"
     type=PATH msg=audit(1719543822.428:1024): item=0 name="/tmp/session_report.log" inode=98213 dev=08:01 mode=0120777 ...
     type=PATH msg=audit(1719543822.428:1024): item=1 name="/root/flag_picoCTF{syml1nk_r4c3_c0nd1t1on_d3t3ct3d}.txt" ...
     ```
   * *주: `syscall=83`은 x86_64 아키텍처에서 `sys_symlink` 호출을 의미합니다.*
3. **공격 대상 파일명 카빙**:
   * 두 번째 `PATH` 레코드에서 심볼릭 링크의 원본 지향점(Target)을 짚는 `item=1` 데이터 필드의 `name` 값을 검토합니다.
   * 공격자가 루트 권한의 파일을 탈취하기 위해 링크 링크를 생성했던 대상 파일의 경로 및 파일명을 복원합니다:
     `/root/flag_picoCTF{syml1nk_r4c3_c0nd1t1on_d3t3ct3d}.txt`
4. **최종 플래그 획득**:
   * 파일명 내부에 기재된 플래그 문자열을 추출합니다:
     `picoCTF{syml1nk_r4c3_c0nd1t1on_d3t3ct3d}`

## 5. 정답(플래그) 규칙 및 예시
* **플래그 형식**: `picoCTF{<flag_string>}`
* **예시**: `picoCTF{syml1nk_r4c3_c0nd1t1on_d3t3ct3d}`

## 6. 출제자 노트 & 파일 제작 가이드
* **아티팩트 제작 방법**:
  1. 리눅스 서버 환경에서 `/etc/audit/rules.d/audit.rules` 설정에 `/tmp` 디렉터리 쓰기 감시 룰을 주입하고 auditd 데몬을 기동합니다:
     `-w /tmp -p wa -k tmp_watch`
  2. 일반 사용자 권한으로 셸에 진입해 루트 권한 파일명을 표적으로 링크를 생성시킵니다:
     `ln -s /root/flag_picoCTF{syml1nk_r4c3_c0nd1t1on_d3t3ct3d}.txt /tmp/session_report.log`
  3. 생성된 감사 로그(`/var/log/audit/audit.log`)를 열어 방금 가동한 `ln` 명령어 관련 SYSCALL 및 PATH 타입 로그들을 획득합니다.
  4. 다른 불필요한 이벤트는 지우고 본 시스템콜 흐름을 증명하는 10여 줄의 핵심 로그만 정제하여 `tmp_audit.log` 파일로 구성해 배포합니다.
* **출제 포인트**: 
  * 공유 디렉터리(/tmp)의 권한 취약성을 노리는 대표적 권한상승 공격 기법(Link Attack)을 감사 추적 로그 관점에서 대응하고, 커널 시스템 콜(syscall 83) 수준의 로그를 분석해 내는 숙련도를 함양합니다.

## 7. 트러블슈팅 및 힌트
* **Q. PATH 레코드의 item=0과 item=1은 각각 무엇을 의미하나요?**
  * A. `symlink` 시스템 콜 감사에서 `item=0`은 새로 생성되는 링크 파일의 경로(Linkpath, 여기서는 `/tmp/session_report.log`)를 나타내고, `item=1`은 링크가 실제로 바라보는 원본 대상 경로(Target, 여기서는 `/root/flag_...`)를 정의합니다.
* **Q. 로그 속의 msg=audit(1719543822.428:1024) 에 들어 있는 숫자는 무엇인가요?**
  * A. 앞부분의 `1719543822.428`은 이벤트가 기록된 에포크(Epoch) 타임스탬프 시각이며, 뒤의 `1024`는 감사 프레임의 고유 일련번호(Event ID)입니다. 동일한 시각과 일련번호를 가진 여러 개의 type 엔트리(SYSCALL, PATH, CWD 등)가 하나의 논리적인 동작 세트를 구성하므로 이 아이디로 로그들을 묶어 교차 검증해야 합니다.

## 8. 학습 포인트
* **심볼릭 링크 레이스 컨디션**: 루트 권한 백그라운드 프로세스가 파일 생성 전 검증하지 않는 시간차(TOCTOU) 취약성을 악용하는 심볼릭 링크 공격 수법을 학습합니다.
* **리눅스 Auditd 로그 분석**: OS 커널 레벨의 파일 감시 도구 아키텍처와 이벤트 타입(SYSCALL, PATH)별 데이터 매핑 구조를 마스터합니다.
