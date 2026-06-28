---
title: 윈도우 서비스 등록 백도어 탐지 (Windows Service Creation / Event 7045)
created: 2026-06-28
updated: 2026-06-28
type: ctf-challenge
tags: [ctf, ctf-challenge, forensics, windows, event-log, evtx, service-creation, event-7045, base64]
confidence: high
---

# 윈도우 서비스 등록 백도어 탐지 (Windows Service Creation / Event 7045)

> **난이도**: 초급  
> **소요 시간**: 15~20분  
> **참고 picoCTF 문제**: 시스템 영속성 백도어 진단 및 분석 (Windows System Event Log 분석)

## 1. 배경 시나리오
공격자가 윈도우 서버 시스템의 통제 권한을 획득한 후, 시스템 백그라운드에서 최고 권한(`LocalSystem`)으로 자동 기동되는 악성 서비스를 등록해 영속성을 공고히 한 징후가 식별되었습니다. 보안 관제팀은 새로운 서비스 등록 이벤트를 감사하기 위해 윈도우 시스템 이벤트 로그 파일인 `System.evtx` 파일을 적출했습니다. 이 이벤트 로그를 분석하여 **새롭게 추가 등록된 악성 서비스 실행 파일의 명령 인자 내에 인코딩된 플래그**를 획득하십시오.

## 2. 제공 파일
* `System.evtx` (윈도우 시스템 감사용 이벤트 로그 파일)

## 3. 문제 목표
윈도우 시스템 이벤트 로그(System.evtx) 내에서 서비스 신규 등록 행위가 남기는 고유한 흔적인 **이벤트 ID 7045 (A service was installed in the system)** 아티팩트의 필드 명세(서비스명, 실행 경로, 서비스 시작 유형, 계정 권한)를 이해하고, 비정상적인 외부 툴 서비스 인자를 역추적합니다.

## 4. 의도한 풀이 흐름
1. **로그 파일 로드 및 필터링**:
   * 제공된 `System.evtx` 파일을 윈도우 `이벤트 뷰어(Event Viewer)` 또는 분석 도구(`EvtxECmd`)로 로드합니다.
   * 서비스 등록 여부 감사를 수행하기 위해 **이벤트 ID 7045**로 로그 항목들을 필터링합니다.
     * CLI 파싱 예시:
       `EvtxECmd.exe -f System.evtx --xml output.xml`
2. **비정상 서비스 및 실행 경로 검사**:
   * 필터링된 이벤트 목록 중 서비스 명칭이나 실행 경로가 비정상적인 행을 조회합니다.
   * `Service Name`이 `Windows Defender Core Update` 와 같이 정상 보안 툴인 것처럼 위장되어 있으나, 실제 실행 파일 경로(`ImagePath` / `Service File Name`)가 임시 폴더 대역을 가리키는 다음 이벤트를 식별합니다:
     * **서비스 이름**: `Windows Defender Core Update`
     * **서비스 파일 이름 (ImagePath)**: `C:\Windows\Temp\updater.exe --token cGljb0NURntzeXN0ZW1fc2VydmljZV9iYWNrZG9vcl9jcmVhdGVkfQ==`
     * **서비스 시작 유형**: `시스템 시작 (Auto Start)`
     * **서비스 계정**: `LocalSystem`
3. **인자 디코딩 및 플래그 획득**:
   * 실행 파일의 `--token` 매개변수 뒤편에 자리한 Base64 인코딩 문자열(`cGljb0NURntzeXN0ZW1fc2VydmljZV9iYWNrZG9vcl9jcmVhdGVkfQ==`)을 분리해 냅니다.
   * Base64 디코딩 명령을 가동합니다:
     `echo "cGljb0NURntzeXN0ZW1fc2VydmljZV9iYWNrZG9vcl9jcmVhdGVkfQ==" | base64 -d`
   * 최종 복구된 플래그를 확인합니다:
     `picoCTF{system_service_backdoor_created}`

## 5. 정답(플래그) 규칙 및 예시
* **플래그 형식**: `picoCTF{<flag_string>}`
* **예시**: `picoCTF{system_service_backdoor_created}`

## 6. 출제자 노트 & 파일 제작 가이드
* **아티팩트 제작 방법**:
  1. Windows 테스트 환경에서 관리자 권한 명령 프롬프트를 엽니다.
  2. 시스템 신규 서비스를 등록하는 `sc` 명령을 실행합니다:
     `sc create "Windows Defender Core Update" binPath= "C:\Windows\Temp\updater.exe --token cGljb0NURntzeXN0ZW1fc2VydmljZV9iYWNrZG9vcl9jcmVhdGVkfQ==" start= auto obj= LocalSystem`
  3. 이벤트 뷰어를 가동해 `원도우 로그` -> `시스템(System)` 영역에 이벤트 ID `7045`가 정상 생성된 것을 확인합니다.
  4. 로그 파일 `C:\Windows\System32\Winevt\Logs\System.evtx` 파일을 획득하고, 침해 당시 이벤트 부근으로 정제하여 배포 아티팩트로 지정합니다.
* **출제 포인트**: 
  * 윈도우 영속성 획득 기법 중 가장 대표적인 서비스 등록 아티팩트(Windows Service Forensics) 추적 능력을 평가하고, 일반 프로세스 실행 로그(ID 4688) 외에 시스템 레벨 감사 채널(Event ID 7045)이 제공하는 상세 속성 탐지력을 학습시킵니다.

## 7. 트러블슈팅 및 힌트
* **Q. 보안(Security) 이벤트 로그의 Event ID 4697도 서비스 등록을 기록하지 않나요?**
  * A. 네, 그렇습니다. 보안 로그의 `4697` 이벤트 역시 새로운 서비스가 시스템에 설치될 때 기록을 발생시킵니다. 그러나 보안 감사 정책 설정에서 '보안 시스템 확장 감사'가 비활성화되어 있는 시스템의 경우 4697은 누락될 수 있으나, 서비스 제어 데몬의 자체 보고 로그에 해당하는 시스템 로그의 `7045` 이벤트는 기본 활성 보존되므로 7045가 더 높은 신뢰도를 갖습니다.
* **Q. ImagePath의 실행 파일이 디스크에 존재하지 않으면 어떻게 해야 하나요?**
  * A. 서비스가 등록될 때 OS 커널은 실행 파일의 실재 여부를 검증하지 않고 서비스 스키마에 레코드를 먼저 등록합니다. 따라서 공격자가 등록 직후 바이너리 파일을 카빙 삭제했더라도, `System.evtx` 내의 설치 로그(7045)는 정상 적재되어 있으므로 명령 이력을 안전하게 복원할 수 있습니다.

## 8. 학습 포인트
* **윈도우 서비스(Windows Services) 아키텍처**: 시스템 권한(`LocalSystem`, `NetworkService`) 하위에서 구동되는 백그라운드 데몬 서비스 로딩 원리를 이해합니다.
* **시스템 이벤트 채널 분석**: 윈도우 시스템 감사 채널(`System.evtx`) 내 Event ID 7045 명세 구조와 이를 활용한 영속성 수립 행위 역추적 절차를 마스터합니다.
