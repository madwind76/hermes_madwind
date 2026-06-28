---
title: 윈도우 WMI 영속성 악성코드 추적 (WMI Event Consumer Persistence)
created: 2026-06-28
updated: 2026-06-28
type: ctf-challenge
tags: [ctf, ctf-challenge, forensics, windows, wmi, persistence, objects-data, event-consumer, base64]
confidence: high
---

# 윈도우 WMI 영속성 악성코드 추적 (WMI Event Consumer Persistence)

> **난이도**: 초중급  
> **소요 시간**: 25~30분  
> **참고 picoCTF 문제**: 시스템 자동 실행 및 영속성 기법 식별 (Windows WMI Repository 포렌식)

## 1. 배경 시나리오
특정 윈도우 서버가 재부팅되거나 시스템 사용 후 수 분이 지나면 백그라운드에서 악성 프로세스가 자동으로 다시 켜지는 기이한 증상이 포착되었습니다. 조사 결과, 공격자는 일반적인 레지스트리 자동 실행 키(Run Key)나 윈도우 예약 작업(Scheduled Tasks)이 아닌, 윈도우 관리 도구인 **WMI(Windows Management Instrumentation)**의 이벤트 구독 메커니즘을 사용해 영속성(Persistence) 백도어를 유지하고 있었습니다. 윈도우 WMI 리포지토리 폴더(`C:\Windows\System32\wbem\Repository\`)에서 개체 정보베이스 데이터인 `OBJECTS.DATA` 파일을 적출했습니다. 이 데이터베이스를 정밀 분석하여 **등록되어 자동 구동되던 악성 명령어 속의 플래그**를 획득해야 합니다.

## 2. 제공 파일
* `OBJECTS.DATA` (윈도우 WMI 객체 정보 리포지토리 바이너리 파일)

## 3. 문제 목표
윈도우 WMI 영속성의 기본 구성 요소인 이벤트 필터(`__EventFilter`), 이벤트 소비자(`__EventConsumer`), 그리고 이 둘을 묶는 바인딩(`__FilterToConsumerBinding`) 모델의 상호 관계를 이해하고, `OBJECTS.DATA` 리포지토리 파일에서 등록된 셸 실행 소비자 객체를 카빙/파싱하여 플래그를 추출합니다.

## 4. 의도한 풀이 흐름
1. **WMI 영속성 매커니즘 파악**:
   * WMI 영속성 공격은 특정 트리거 조건(예: 시스템 시작 후 5분 등)을 정의하는 `__EventFilter`와 실제 실행할 동작(예: PowerShell 구동)을 기술하는 `__EventConsumer` 오브젝트를 생성한 후, 이를 `__FilterToConsumerBinding`으로 바인딩하여 백그라운드 영구 동작을 수행합니다.
2. **리포지토리 분석 도구 가동**:
   * **도구 활용**: 파이썬 오픈소스 분석 도구인 `PyWMIPersistenceFinder.py`를 가동하여 제공된 `OBJECTS.DATA`를 쿼리합니다.
     ```bash
     python3 PyWMIPersistenceFinder.py OBJECTS.DATA
     ```
   * **수동 스캔**: 도구가 없는 경우, WMI 소비자 유형 중 주로 명령행을 가동시키는 `CommandLineEventConsumer` 또는 VBS/JS 코드를 실행시키는 `ActiveScriptEventConsumer` 문자열 키워드로 `OBJECTS.DATA` 바이너리 내부를 `strings` 추출 및 grep 필터링합니다.
3. **악성 바인딩 및 페이로드 검출**:
   * 분석 결과 덤프 내부에서 다음과 같이 `CommandLineTemplate` 속성에 파워셸 인코딩 명령어를 장착해 둔 소비자를 식별합니다:
     ```text
     Consumer Type: CommandLineEventConsumer
     Consumer Name: SystemUpdater
     CommandLineTemplate: powershell.exe -enc cGljb0NURnt3bWlfZXZlbnRfY29uc3VtZXJfYmFja2Rvb3J9
     ```
4. **Base64 디코딩 및 플래그 획득**:
   * 인코딩된 문자열(`cGljb0NURnt3bWlfZXZlbnRfY29uc3VtZXJfYmFja2Rvb3J9`)을 복구하여 디코딩을 진행합니다:
     `echo "cGljb0NURnt3bWlfZXZlbnRfY29uc3VtZXJfYmFja2Rvb3J9" | base64 -d`
   * 최종 플래그를 획득합니다:
     `picoCTF{wmi_event_consumer_backdoor}`

## 5. 정답(플래그) 규칙 및 예시
* **Phish 형식**: `picoCTF{<flag_string>}`
* **예시**: `picoCTF{wmi_event_consumer_backdoor}`

## 6. 출제자 노트 & 파일 제작 가이드
* **아티팩트 제작 방법**:
  1. Windows 테스트 가상 머신에서 관리자 권한 파워셸을 열고, WMI 인스턴스를 수동 생성 주입합니다:
     ```powershell
     $Filter = Set-WmiInstance -Namespace root\subscription -Class __EventFilter -Arguments @{Name='SystemUpdater';EventNamespace='root\cimv2';QueryLanguage="WQL";Query="SELECT * FROM __InstanceModificationEvent WITHIN 60 WHERE TargetInstance ISA 'Win32_LocalTime' AND TargetInstance.Hour = 1"}
     $Consumer = Set-WmiInstance -Namespace root\subscription -Class CommandLineEventConsumer -Arguments @{Name='SystemUpdater';CommandLineTemplate="powershell.exe -enc cGljb0NURnt3bWlfZXZlbnRfY29uc3VtZXJfYmFja2Rvb3J9"}
     Set-WmiInstance -Namespace root\subscription -Class __FilterToConsumerBinding -Arguments @{Filter=$Filter;Consumer=$Consumer}
     ```
  2. 시스템 WMI 리포지토리 경로 `C:\Windows\System32\wbem\Repository\` 로 이동하여 실시간 데이터베이스 파일인 `OBJECTS.DATA`를 덤프해 냅니다.
  3. `OBJECTS.DATA` 파일만 독립 추출하여 정상 분석 도구 및 strings 정적 필터링으로 정상 파싱되는지 크로스 검증한 후 아티팩트를 배포합니다.
* **출제 포인트**: 
  * 고급 수준의 공격 기법인 파일리스(Fileless) 및 비 레지스트리 기반 WMI 영속성 기법(WMI Forensics)의 탐지 논리를 습득하고, 윈도우 OS의 관리 정보 통합 데이터 파일 내부를 저수준으로 해독해 유효 위협 인자를 식별하는 능력을 증진합니다.

## 7. 트러블슈팅 및 힌트
* **Q. OBJECTS.DATA를 텍스트 에디터로 열었는데 시스템 인코딩 정보가 섞여 있어 읽기 너무 힘듭니다.**
  * A. `OBJECTS.DATA` 파일은 WMI 개체의 메타 데이터가 정형 이진 구조로 압축 매핑된 바이너리 데이터베이스입니다. 단순 메모장으로 열면 대부분의 텍스트가 특수문자와 공백바이트(\x00)로 인해 깨져 보이므로, 가독 문자열만 정제해 추출해 주는 `strings` 명령을 실행하거나 `PyWMIPersistenceFinder.py` 스크립트를 경유하여 정규화된 텍스트로 보시는 것을 적극 권장합니다.
* **Q. WMI 영속성이 발견되었을 때 시스템에서 이를 강제 삭제하려면 어떻게 하나요?**
  * A. 파워셸 명령행을 가동하여 인스턴스를 소거해야 합니다:
     `Get-WmiObject -Namespace root\subscription -Class __EventFilter -Filter "Name='SystemUpdater'" | Remove-WmiObject`
     동일하게 `CommandLineEventConsumer` 및 `__FilterToConsumerBinding` 인스턴스도 해당 Name 키 값을 기준으로 조회하여 파이프라인 `Remove-WmiObject`로 완전히 소멸시킬 수 있습니다.

## 8. 학습 포인트
* **윈도우 WMI(Windows Management Instrumentation)**: OS 구성 요소를 스크립트로 질의/제어하기 위해 동작하는 WMI 서브시스템 및 구독 필터링 체계를 이해합니다.
* **WMI 영속성 아티팩트**: 디스크 상에 파일이 실재하지 않아 탐지가 까다로운 파일리스 악성코드의 물리 흔적인 WMI 데이터베이스(`OBJECTS.DATA`)를 색인해 해독하는 DFIR 절차를 확립합니다.
