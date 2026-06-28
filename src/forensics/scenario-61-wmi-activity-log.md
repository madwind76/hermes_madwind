---
title: 윈도우 원격 실행 WMI 실행 로그 분석 (WMI Activity Operational Event 5857/5858)
created: 2026-06-28
updated: 2026-06-28
type: ctf-challenge
tags: [ctf, ctf-challenge, forensics, windows, event-log, evtx, wmi, event-5858, lateral-movement]
confidence: high
---

# 윈도우 원격 실행 WMI 실행 로그 분석 (WMI Activity Operational Event 5857/5858)

> **난이도**: 초중급  
> **소요 시간**: 20~25분  
> **참고 picoCTF 문제**: 원격 WMI 명령 오남용 흔적 추적 (WMI Activity Operational EVTX 분석)

## 1. 배경 시나리오
공격자가 도용한 도메인 관리자 계정을 사용하여 대내 보안망 서버에 WMI(Windows Management Instrumentation) 원격 쿼리를 주입, 비인가 원격 정찰 명령을 시도한 흔적이 관찰되었습니다. 공격자는 탐색 속도를 높이기 위해 불특정 다수의 잘못된 WMI 클래스를 임의로 호출하다가 실패 로그를 대거 잔재시켰습니다. 윈도우 운영체제는 WMI 서비스가 처리한 쿼리 및 연동 오류 내역을 전용 로그 채널인 `Microsoft-Windows-WMI-Activity/Operational.evtx` 에 정밀하게 적록합니다. 피해 서버에서 격리해 낸 이 WMI 감사 이벤트 로그 파일을 정적 분석하여 **공격자가 호출했으나 유효하지 않아 에러(HRESULT: 0x80041010)를 일으켰던 WMI 클래스 이름 속의 플래그**를 알아내십시오.

## 2. 제공 파일
* `WMI-Activity_Operational.evtx` (윈도우 WMI 동작 감사 기록 이벤트 로그 파일)

## 3. 문제 목표
윈도우 WMI 감사의 주요 로깅 이벤트인 **이벤트 ID 5858 (WMI query/method execution error)**의 명세 구조(Operation, Query, ResultCode, ClientProcessId 등)를 이해하고, 오류 발생 반환 코드(`0x80041010` - WBEM_E_INVALID_CLASS) 상태를 조회하여 공격자가 인가한 원본 명령 매개변수를 역추적합니다.

## 4. 의도한 풀이 흐름
1. **이벤트 로그 파싱 및 에러 필터링**:
   * 제공된 `WMI-Activity_Operational.evtx` 로그 파일을 이벤트 뷰어나 `EvtxECmd` 등의 도구를 통해 파싱합니다.
   * WMI 엔진의 쿼리 실패 흔적을 감사하기 위해 **이벤트 ID 5858** 항목들을 필터링합니다.
2. **에러 코드 대조 및 클래스 무효 상태 분석**:
   * Event ID 5858의 각 상세 데이터 내역 중 에러 결과를 의미하는 `ResultCode` 또는 `HResult` 값이 `0x80041010` (존재하지 않는 잘못된 WMI 클래스 참조 에러)인 항목을 정밀 스캔합니다.
   * 해당 오류 레코드의 `Operation` 또는 `Query` 필드에 주입된 원본 WQL 쿼리문을 대조합니다:
     * **이벤트 ID**: `5858`
     * **에러 코드 (HResult)**: `0x80041010`
     * **주입된 쿼리 (Query)**: `SELECT * FROM picoCTF{wmi_act1v1ty_op3rat1on_evtx}`
     * **클라이언트 PID**: `2940`
3. **플래그 도출**:
   * 존재하지 않는 잘못된 클래스로 참조되어 0x80041010 에러를 발동시켰던 대상 클래스명인 플래그를 도출합니다:
     `picoCTF{wmi_act1v1ty_op3rat1on_evtx}`

## 5. 정답(플래그) 규칙 및 예시
* **플래그 형식**: `picoCTF{<flag_string>}`
* **예시**: `picoCTF{wmi_act1v1ty_op3rat1on_evtx}`

## 6. 출제자 노트 & 파일 제작 가이드
* **아티팩트 제작 방법**:
  1. Windows 10/11 또는 Windows Server 환경에서 파워셸을 켭니다.
  2. 기밀 플래그 이름으로 설정된 비실존 클래스를 강제로 호출하는 잘못된 WMI 원격 쿼리를 의도적으로 기동하여 5858 이벤트를 발생시킵니다:
     `Get-WmiObject -Query "SELECT * FROM picoCTF{wmi_act1v1ty_op3rat1on_evtx}"`
     (이 경우 해당 클래스가 데이터베이스에 등록되어 있지 않으므로 0x80041010 - Invalid Class 에러를 반환합니다)
  3. 윈도우 감사 파일이 위치한 경로에서 WMI 전용 작동 로그를 수집합니다:
     `C:\Windows\System32\Winevt\Logs\Microsoft-Windows-WMI-Activity%4Operational.evtx`
  4. 덤프 파일을 격리해 가공하여 챌린지 문제 파일로 유저에게 배포합니다.
* **출제 포인트**: 
  * 공격자가 내부 정찰 및 횡적 이동(Lateral Movement) 시 가장 애용하는 WMI 인터페이스 오남용 행위에 대해, 시스템 관리 로그(`System.evtx`, `Security.evtx`)에 남지 않아 쉽게 놓치기 쉬운 전용 WMI 동작 감사 기록 채널(WMI Operational Log Forensics)을 역추적하는 고급 분석 기법을 훈련시킵니다.

## 7. 트러블슈팅 및 힌트
* **Q. ResultCode인 0x80041010의 구체적인 명세는 어떻게 확인하나요?**
  * A. 윈도우 WMI API 계열의 리턴 코드는 COM/WBEM 오류 규격을 따릅니다. 마이크로소프트 공식 기술 문서에서 `WBEM_E_INVALID_CLASS` 상수가 `0x80041010`에 매핑됨을 대조할 수 있으며, 이는 호출한 스키마 클래스가 WMI 템플릿(CIM Repository)에 아예 등록되어 있지 않음을 뜻합니다.
* **Q. ClientProcessId 필드는 어떤 유용성을 가지나요?**
  * A. Event ID 5858은 악성 쿼리를 수행해 달라고 WMI 서비스에 원격/로컬로 심부름을 보낸 '발주 주체(Client)' 프로세스의 PID(`ClientProcessId`) 정보를 보존합니다. 침해 사고 추적 시 이 PID를 프리페치나 Sysmon ID 1 프로세스 실행 로그와 대조하면, 어떤 악성코드 파일이 배후에서 WMI를 조작했는지 실행 흐름을 최종 규명해 낼 수 있어 가치가 매우 높습니다.

## 8. 학습 포인트
* **윈도우 WMI 통신 아키텍처**: 원격 제어 및 진단 인프라인 WMI 분산 서비스(WmiPrvSE.exe)의 동작 및 쿼리 처리 스키마를 습득합니다.
* **WMI Activity 감사 포렌식**: 윈도우 감사 사각지대에 위치한 `WMI-Activity/Operational.evtx` 로그 구조를 활용하여 우회 침투 쿼리를 역추적 및 진단하는 전문 능력을 구축합니다.
