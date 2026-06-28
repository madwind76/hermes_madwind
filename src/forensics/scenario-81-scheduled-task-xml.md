---
title: 윈도우 원격 예약 작업 등록 분석 (Windows Schedule Tasks XML Persistence)
created: 2026-06-28
updated: 2026-06-28
type: ctf-challenge
tags: [ctf, ctf-challenge, forensics, windows, task-scheduler, xml, persistence, powershell]
confidence: high
---

# 윈도우 원격 예약 작업 등록 분석 (Windows Schedule Tasks XML Persistence)

> **난이도**: 초급  
> **소요 시간**: 15~20분  
> **참고 picoCTF 문제**: 원격 작업 스케줄러 등록 변조 및 영속성 식별 (Windows Scheduled Task XML 분석)

## 1. 배경 시나리오
공격자가 사내 핵심 AD 서버에 침투한 후, 관리자 권한을 상실하더라도 매일 시스템 기동 시 자동으로 악성 다운로더를 트리거하여 접속을 재수립하도록 **예약 작업(Scheduled Task)**을 생성했습니다. 침해대응 조사관은 윈도우 작업 스케줄러 서비스가 예약 작업 설정을 XML 파일로 직렬화하여 영구 적재하는 디렉터리(`C:\Windows\System32\Tasks\`) 하위에서 비정상적인 파일 `MaliciousTask.xml`을 확보했습니다. 이 XML 구성 파일을 정적 분석하여 **공격자가 주기 실행 대상으로 등록해 둔 실행 매개변수 속의 플래그**를 도출하십시오.

## 2. 제공 파일
* `MaliciousTask.xml` (사용자 환경에서 수집한 악성 예약 작업 스키마 정보가 기록된 XML 파일)

## 3. 문제 목표
윈도우 작업 스케줄러 아티팩트의 저장 원리 및 내부 XML 스키마 구조(특히 트리거 조건을 기술하는 **Triggers** 태그, 실제 기동 동작을 정의하는 **Actions** 및 **Exec** 태그)를 이해하고, 추가된 비정상 악성 명령 매개변수를 역추적합니다.

## 4. 의도한 풀이 흐름
1. **XML 설정 파일 구조 검사**:
   * 제공된 `MaliciousTask.xml` 파일을 텍스트 에디터나 브라우저를 통해 엽니다.
   * 작업 스케줄러 XML의 핵심 노드인 `<Actions>` 섹션을 탐색합니다.
2. **실행 명령 및 인수 추출**:
   * `<Actions>` 하위의 `<Exec>` 노드를 점검하여 구동 프로그램과 매개인수 값을 식별합니다:
     * **실행 프로그램 (`<Command>`)**: `powershell.exe`
     * **실행 인수 (`<Arguments>`)**: `-NoProfile -WindowStyle Hidden -Command "$FLAG='picoCTF{sched_t4sk_xml_persistence_detect}'; [System.IO.File]::WriteAllText('C:\temp\output.txt', $FLAG)"`
3. **플래그 도출**:
   * 파워셸 실행 인수 뒤에 주입된 평문 변수 `$FLAG` 데이터로부터 최종 플래그를 정립합니다:
     `picoCTF{sched_t4sk_xml_persistence_detect}`

## 5. 정답(플래그) 규칙 및 예시
* **플래그 형식**: `picoCTF{<flag_string>}`
* **예시**: `picoCTF{sched_t4sk_xml_persistence_detect}`

## 6. 출제자 노트 & 파일 제작 가이드
* **아티팩트 제작 방법**:
  1. Windows 테스트 환경에서 관리자 권한 명령창 또는 파워셸을 켭니다.
  2. 기밀 플래그 매개변수를 포함하는 파워셸 구동 예약 작업을 등록합니다:
     `Register-ScheduledTask -TaskName "MaliciousTask" -Trigger (New-ScheduledTaskTrigger -AtStartup) -Action (New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-NoProfile -WindowStyle Hidden -Command `"$FLAG='picoCTF{sched_t4sk_xml_persistence_detect}'; [System.IO.File]::WriteAllText('C:\temp\output.txt', $FLAG)`"") -User "NT AUTHORITY\SYSTEM"`
  3. 작업 스케줄러 실제 저장 경로로 이동합니다:
     `C:\Windows\System32\Tasks\`
  4. 생성된 `MaliciousTask` XML 파일을 복제 추출하고, 이를 `MaliciousTask.xml` 이름으로 배포합니다.
* **출제 포인트**: 
  * 윈도우 영속성(Persistence) 킬체인 중 가장 표준적이면서 흔히 도용되는 작업 스케줄러 아티팩트(Scheduled Tasks Forensics) 분석에 대한 XML 데이터 파싱 능력을 테스트하고, 비인가 기동 프로세스 인자를 판독하는 기본 보안 감사 역량을 기르게 합니다.

## 7. 트러블슈팅 및 힌트
* **Q. 예약 작업 생성 시점 등의 타임라인 정보도 XML에 남나요?**
  * A. 네, 그렇습니다. XML 상단 메타데이터 필드 내의 `<Date>` (작업 등록 날짜) 및 `<Author>` (생성 주체 사용자 식별자) 태그를 대조하면 공격자가 언제 어떤 권한으로 이 악성 작업을 등록해 두었는지 타임라인을 정밀하게 연동 매핑할 수 있습니다.
* **Q. 디바이스에서 예약 작업을 등록할 때 사용되는 레지스트리 경로도 연관성이 있나요?**
  * A. 네, 그렇습니다. 윈도우 커널은 백그라운드 스케줄 감사 관리를 위해 다음 레지스트리 경로에도 동일 태그 정보를 캐시 저장합니다:
     `HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Schedule\TaskCache\Tasks`
     디스크 상의 XML 파일이 삭제되더라도 레지스트리 하이브의 이 TaskCache 키 영역에 흔적이 영구 보존되므로 교차 포렌식 증적으로 가치가 높습니다.

## 8. 학습 포인트
* **윈도우 작업 스케줄러(Task Scheduler) 아키텍처**: 시스템 시작 시점 이식 및 자동 실행 조건(Trigger)에 따라 구동 프로세스(Exec Action)를 매칭하는 윈도우 핵심 라이프사이클을 이해합니다.
* **영속성 탐지(Persistence Hunting)**: `C:\Windows\System32\Tasks\` 하위 구성 파일 일괄 스캔을 통해 탐지 시스템을 기만하는 우회 명령 인자를 식별 복구하는 능력을 갖춥니다.
