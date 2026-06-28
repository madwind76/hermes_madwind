---
title: 윈도우 이벤트 로그 원격 실행 분석 (Windows Event Remote Execution)
created: 2026-06-28
updated: 2026-06-28
type: ctf-challenge
tags: [ctf, ctf-challenge, forensics, windows, event-log, evtx, sysmon, process-creation, base64]
confidence: high
---

# 윈도우 이벤트 로그 원격 실행 분석 (Windows Event Remote Execution)

> **난이도**: 초급  
> **소요 시간**: 15~20분  
> **참고 picoCTF 문제**: 원격 명령 셸 흔적 추적 (Windows Event Log EVTX 및 Sysmon 프로세스 감사)

## 1. 배경 시나리오
사내 파일 배포용 윈도우 서버에 공격자가 원격 제어 프로토콜(WinRM)을 경유하여 침투했습니다. 해커는 파워셸 명령어를 활용해 백도어를 은밀히 실행시킨 후 즉시 연결을 끊었습니다. 다행히 해당 서버에는 프로세스 실행을 정밀 모니터링하는 **Sysmon(System Monitor)** 에이전트가 작동 중이었고, 당시의 감사 이벤트 로그 파일인 `Sysmon.evtx` 파일이 확보되었습니다. 이 이벤트 로그를 분석하여 **원격으로 실행된 파워셸 프로세스의 명령줄 인수 내에 인코딩되어 숨겨진 플래그**를 확보해야 합니다.

## 2. 제공 파일
* `Sysmon.evtx` (윈도우 Sysmon 모니터링 감사 로그 파일)

## 3. 문제 목표
윈도우 이벤트 로그(EVTX)의 구조와 Sysmon 프로세스 생성 감사 이벤트(Event ID 1)의 명세 포맷을 이해하고, 로그 분석 도구(EvtxECmd, Event Viewer 또는 python-evtx)를 사용하여 CommandLine 데이터를 필터링 및 복구해 은닉 플래그를 찾아냅니다.

## 4. 의도한 풀이 흐름
1. **분석 방식 선정**:
   * **Windows GUI**: 윈도우 내장 `이벤트 뷰어(Event Viewer)`로 `Sysmon.evtx` 파일을 엽니다.
   * **Linux/Windows CLI**: Eric Zimmerman의 `EvtxECmd.exe`를 구동하거나 파이썬 `evtx` 라이브러리로 XML 데이터 파싱 스크립트를 작동시킵니다.
2. **이벤트 필터링 (Event ID 1 추적)**:
   * Sysmon 로그에서 프로세스 생성 이벤트를 가리키는 **Event ID 1 (Process Creation)** 항목만 필터링하여 스캔합니다:
     * 윈도우 이벤트 뷰어의 경우 '현재 로그 필터링' -> ID 값에 `1` 입력.
     * CLI 도구 사용 시:
       `EvtxECmd.exe -f Sysmon.evtx --xml output.xml`
3. **의심 프로세스 검색 (PowerShell 명령어 추출)**:
   * 생성된 프로세스 목록 중 실행 이미지 파일 경로가 `powershell.exe`인 항목을 탐색합니다.
   * 해당 이벤트 상세 데이터 내의 **CommandLine** 필드 데이터를 대조하여 아래의 비정상 실행 이력을 식별합니다:
     `powershell.exe -NonInteractive -EncodedCommand cGljb0NURntzeXNtb25fZXZ0eF9wcm9jZXNzX2NyZWF0aW9uX2xvZ2dlZH0=`
4. **Base64 디코딩 및 플래그 획득**:
   * 인코딩 명령 인자(`-EncodedCommand`) 뒤의 문자열(`cGljb0NURntzeXNtb25fZXZ0eF9wcm9jZXNzX2NyZWF0aW9uX2xvZ2dlZH0=`)을 추출하여 디코딩합니다:
     `echo "cGljb0NURntzeXNtb25fZXZ0eF9wcm9jZXNzX2NyZWF0aW9uX2xvZ2dlZH0=" | base64 -d`
   * 해독된 플래그 값을 획득합니다:
     `picoCTF{sysmon_evtx_process_creation_logged}`

## 5. 정답(플래그) 규칙 및 예시
* **플래그 형식**: `picoCTF{<flag_string>}`
* **예시**: `picoCTF{sysmon_evtx_process_creation_logged}`

## 6. 출제자 노트 & 파일 제작 가이드
* **아티팩트 제작 방법**:
  1. Sysmon이 설치된 Windows 가상 머신을 구동합니다. (Sysmon config 설정 시 commandline 로깅 활성화)
  2. 파워셸을 열고 플래그가 들어간 모의 명령을 실행합니다:
     `powershell.exe -NonInteractive -EncodedCommand cGljb0NURntzeXNtb25fZXZ0eF9wcm9jZXNzX2NyZWF0aW9uX2xvZ2dlZH0=`
  3. `C:\Windows\System32\Winevt\Logs\Microsoft-Windows-Sysmon%4Operational.evtx` 파일을 획득합니다.
  4. 다른 불필요한 시스템 이벤트 로그가 너무 많은 노이즈로 섞이지 않게 해당 침해 이벤트 행 전후로 약 100~200개 이벤트만 남기고 로그를 정제하여 `Sysmon.evtx` 파일로 포장해 배포합니다.
* **출제 포인트**: 
  * 원격 공격 기법 추적 시 기본 윈도우 보안 이벤트 로그가 기록하지 못하는 프로세스 전체 명령어 및 해시 정보 등의 증적(Sysmon Forensics) 분석 관점을 학습하게 합니다.

## 7. 트러블슈팅 및 힌트
* **Q. CommandLine 필드가 보이지 않고 단순 ProcessName만 기록되어 있습니다.**
  * A. Sysmon이 아닌 윈도우 기본 4688 이벤트 로그(프로세스 생성 감사)의 경우, 정책 설정(명령줄 감사 활성화)이 누락되어 있으면 인자 값이 표시되지 않습니다. 이 문제에 제공되는 `Sysmon.evtx`는 Sysmon 에이전트 로그이므로 XML 데이터 내의 `CommandLine` 스키마 필드에 실행 값이 안전하게 기록되어 있습니다.
* **Q. EvtxECmd 파싱 결과가 너무 방대합니다.**
  * A. 파싱 옵션 중 `--csv`를 사용해 엑셀 형식으로 변환한 다음, 'CommandLine' 열을 기준 삼아 `powershell` 또는 `cmd` 키워드로 정렬/필터링을 가하면 분석 시간을 수 분에서 수 초로 단축할 수 있습니다.

## 8. 학습 포인트
* **윈도우 이벤트 로그(EVTX) 구조**: XML 기반 바이너리 이벤트 로그 포맷인 EVTX의 파싱 원리와 속도 최적화 기법을 습득합니다.
* **Sysmon 감사 모니터링**: 윈도우 침해 사고 조사에서 Sysmon Event ID 1(프로세스 생성), 3(네트워크 연결) 등이 지니는 실무적 포렌식 위상과 행위 추적 절차를 이해합니다.
