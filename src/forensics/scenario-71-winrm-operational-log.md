---
title: 윈도우 원격 명령 WinRM 서비스 로그 분석 (WinRM Operational Event ID 81/91/134)
created: 2026-06-28
updated: 2026-06-28
type: ctf-challenge
tags: [ctf, ctf-challenge, forensics, windows, event-log, evtx, winrm, event-134, lateral-movement]
confidence: high
---

# 윈도우 원격 명령 WinRM 서비스 로그 분석 (WinRM Operational Event ID 81/91/134)

> **난이도**: 초중급  
> **소요 시간**: 20~25분  
> **참고 picoCTF 문제**: 원격 관리 서비스 오남용 흔적 추적 (WinRM Operational EVTX 분석)

## 1. 배경 시나리오
공격자가 도메인 환경 하에서 WMI와 더불어 가장 널리 활용하는 원격 관리 및 횡적 이동 기법인 **WinRM (Windows Remote Management)** 파워셸 원격 세션을 통해 핵심 파일 서버에 무단 접속했습니다. 공격자는 일반적인 보안 관제 시스템의 탐지를 피하기 위해 접속하자마자 자격을 증명하는 환경변수를 주입하고 기밀 유출 도구를 기동했습니다. 보안 운영팀은 WinRM 연동 이력을 전담해 상세 추적하는 전용 로그 채널인 `Microsoft-Windows-WinRM/Operational.evtx` 파일을 획득했습니다. 이 이벤트 로그를 분석하여 **원격 세션 수립 단계에서 클라이언트가 서버로 주입(전송)했던 명령 환경 변수 내의 플래그**를 획득하십시오.

## 2. 제공 파일
* `WinRM_Operational.evtx` (윈도우 WinRM 동작 감사 기록 이벤트 로그 파일)

## 3. 문제 목표
윈도우 WinRM 전용 감사 로그(`WinRM/Operational.evtx`) 내에서 비정상적인 원격 연결 및 세션 생성을 증명하기 위해 요구되는 핵심 이벤트 구조(특히 **이벤트 ID 81 - Processing user request for a shell**, **이벤트 ID 91 - Creating a shell**, **이벤트 ID 134 - Connection information**)를 이해하고, 클라이언트의 유입 명령 인자를 디코딩합니다.

## 4. 의도한 풀이 흐름
1. **이벤트 로그 파싱 및 키 이벤트 필터링**:
   * 제공된 `WinRM_Operational.evtx` 로그를 이벤트 뷰어 또는 `EvtxECmd` 도구로 파싱합니다.
   * 원격 셸 발주 및 세션 초기화 정보가 밀접하게 로깅되는 **이벤트 ID 81** 또는 **이벤트 ID 134** 레코드를 위주로 필터링합니다.
2. **세션 파라미터 및 원격 명령행 분석**:
   * 필터링된 이벤트의 상세 XML 본문 영역을 검색합니다.
   * `Event ID 81` (Shell Create request) 내의 `Command` 또는 `Environment` 관련 데이터 요소를 점검합니다.
   * 원격 클라이언트에서 파워셸 셸 세션을 시작할 때 다음의 명령 매개변수가 전송 및 수립되었음을 탐지합니다:
     * **이벤트 ID**: `81`
     * **작업 유형**: `Shell Creation`
     * **사용자 계정**: `CONTOSO\ad-admin`
     * **주입된 명령어**: `powershell.exe -NoProfile -ExecutionPolicy Bypass -Command "$env:FLAG='picoCTF{winrm_op3rat1on4l_log_audited}'; [System.IO.File]::WriteAllText('C:\Windows\Temp\log.txt', $env:FLAG)"`
3. **플래그 도출**:
   * 파워셸 원격 명령의 환경변수 선언문 `$env:FLAG` 부분에 평문 적재되어 유입된 최종 플래그를 추출합니다:
     `picoCTF{winrm_op3rat1on4l_log_audited}`

## 5. 정답(플래그) 규칙 및 예시
* **플래그 형식**: `picoCTF{<flag_string>}`
* **예시**: `picoCTF{winrm_op3rat1on4l_log_audited}`

## 6. 출제자 노트 & 파일 제작 가이드
* **아티팩트 제작 방법**:
  1. Windows Server 2019/2022 환경에서 WinRM 서비스를 활성화합니다: `winrm quickconfig`
  2. 원격 호스트 PC에서 WinRM 세션을 맺고 플래그 변수가 주입된 파워셸 원격 명령을 주입 실행합니다:
     `Enter-PSSession -ComputerName TargetServer -Credential ad-admin`
     또는 CLI 일회성 구동 명령어 실행:
     `Invoke-Command -ComputerName TargetServer -ScriptBlock { $env:FLAG='picoCTF{winrm_op3rat1on4l_log_audited}'; [System.IO.File]::WriteAllText('C:\Windows\Temp\log.txt', $env:FLAG) }`
  3. 대상 서버 시스템의 다음 경로에서 WinRM 동작 로그를 획득합니다:
     `C:\Windows\System32\Winevt\Logs\Microsoft-Windows-WinRM%4Operational.evtx`
  4. 로그 내에서 침투 시간대 부근의 81번, 91번, 134번 이벤트 레코드들을 격리 정제하여 배포 아티팩트로 사용합니다.
* **출제 포인트**: 
  * 기업 인프라 환경에서 원격 명령 제어에 상시 활용되는 WinRM 프로토콜의 침해 흔적 조사 기법을 강화하고, 일반 프로세스 기동 흔적 외에 원격지 접속 계정명과 연동 커맨드라인 매개변수를 전용 채널(`WinRM/Operational.evtx`)을 통해 유기적으로 역추적해 내는 전문 포렌식 분석 역량을 검증합니다.

## 7. 트러블슈팅 및 힌트
* **Q. 이벤트 ID 134와 81의 차이는 무엇인가요?**
  * A. `Event ID 134`는 들어오는 네트워크 원격 접속 자체를 수신(Connection Accepted)하여 원격 IP 및 포트 정보를 기표하는 수준에 그치지만, `Event ID 81`은 인증 완료 후 원격지 사용자 컨텍스트 하에 실질적으로 명령 인터프리터(cmd, powershell) 인스턴스를 메모리에 로딩(Shell/Process Request)하는 시점을 증명하므로, 구체적인 주입 매개변수는 81번 이벤트에서 온전히 수집됩니다.
* **Q. 보안(Security) 로그에 기록되는 원격 터미널 실행 기록(Event ID 4624 Logon Type 3 또는 9)과의 연계 분석은 어떻게 하나요?**
  * A. WinRM 원격 연결이 성공하면 보안 로그에는 `Logon Type 3` (Network Logon) 또는 Kerberos 위임을 뜻하는 `Logon Type 9` (NewCredentials) 로그가 기표됩니다. 이때 기표된 `TargetLogonId` 값을 기반으로 WinRM Operational 로그의 세션 ID와 매핑하면, 동일 타임라인 상의 물리 네트워크 접속 세션의 주체와 수행한 구체적 커맨드라인을 1대1로 정확히 규명해 낼 수 있습니다.

## 8. 학습 포인트
* **윈도우 WinRM 통신 아키텍처**: HTTP/HTTPS 프로토콜 기반의 WS-Management 사양에 입각한 윈도우 원격 관리 인프라의 동작 구조를 이해합니다.
* **WinRM Operational 감사 로그 분석**: `WinRM/Operational.evtx` 내의 주요 이벤트 아이디(81, 91, 134)의 데이터 구조를 활용하여 악성 우회 원격 주입 스크립트를 역파싱하는 기술을 마스터합니다.
