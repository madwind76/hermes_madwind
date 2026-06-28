---
title: 레지스트리에 남겨진 흔적 (Registry Echoes)
created: 2026-06-28
updated: 2026-06-28
type: ctf-challenge
tags: [ctf, ctf-challenge, forensics, windows, registry, persistence, usbstor]
confidence: high
---

# 레지스트리에 남겨진 흔적 (Registry Echoes)

> **난이도**: 초중급  
> **소요 시간**: 25~30분  
> **참고 picoCTF 문제**: 일반적인 DFIR 침해 사고 분석 시나리오 (Windows Registry 아티팩트 연계)

## 1. 배경 시나리오
보안 위협 팀은 사내 내부망에서 지속적으로 악성 도메인 접속을 발생시키는 임직원 PC 1대를 격리 조치했습니다. 해당 PC의 디스크 전체를 이미징하기 전, 빠른 위협 파악을 위해 윈도우 핵심 설정을 담고 있는 레지스트리 하이브(Registry Hive) 파일들을 추출했습니다. 분석가는 레지스트리 내부를 탐색하여 **악성코드가 부팅 시 자동으로 작동하도록 등록한 프로그램 이름**과 **공격자가 중요 파일을 빼돌리기 위해 마지막으로 마운트한 USB 외장 장치의 일련번호**를 찾아야 합니다.

## 2. 제공 파일
* `SYSTEM` (윈도우 시스템 레지스트리 하이브 파일)
* `SOFTWARE` (윈도우 소프트웨어 설정 레지스트리 하이브 파일)
* `NTUSER.DAT` (해당 의심 사용자 프로필 레지스트리 하이브 파일)

## 3. 문제 목표
윈도우 레지스트리의 핵심 하이브 파일을 분석 툴(RegRipper, Registry Explorer 등) 또는 파이썬 파서를 사용해 파싱하고, 자동 실행(Autorun) 설정과 USB 연결 흔적(USBSTOR) 데이터를 복구 및 결합하여 플래그를 조립합니다.

## 4. 의도한 풀이 흐름
1. **분석 환경 설정**:
   * Windows GUI 환경에서는 `Registry Explorer` 도구를 다운로드하여 하이브 파일들을 가져옵니다.
   * Linux CLI 환경에서는 RegRipper(`rip.sh` 또는 `rip.pl`) 도구를 준비합니다.
2. **지속성 확보 흔적(Autorun) 분석**:
   * `SOFTWARE` 하이브 파일의 다음 경로를 조회합니다:
     `Microsoft\Windows\CurrentVersion\Run` 또는 `RunOnce`
   * 혹은 사용자 개별 설정인 `NTUSER.DAT` 내의 동일 자동 실행 키 경로를 점검합니다.
   * 분석을 통해 비정상적인 경로에서 호출되는 수상한 프로세스 실행 값(예: `C:\Users\Public\updater.exe`)과 프로그램 명(`updater.exe`)을 확보합니다.
3. **USB 마운트 흔적(USBSTOR) 분석**:
   * `SYSTEM` 하이브 파일에서 외장 매체 연결 이력이 기록되는 다음 경로로 이동합니다:
     `CurrentControlSet\Enum\USBSTOR`
   * 등록된 USB 장치 목록 중 가장 최근에 마운트(작동)한 기기의 벤더 정보와 고유 일련번호(Serial Number) 키 값을 확인합니다.
     (예: `Disk&Ven_SanDisk&Prod_Cruzer&Rev_1.00\AA29184B0291&0` 하위의 `AA29184B0291`)
4. **플래그 조립**:
   * 찾아낸 프로그램 명칭과 USB 일련번호 문자열을 언더스코어(`_`)로 연결해 최종 플래그를 작성합니다.
   * 최종 플래그: `picoCTF{updater.exe_AA29184B0291}`

## 5. 정답(플래그) 규칙 및 예시
* **플래그 형식**: `picoCTF{<process_name>_<usb_serial_number>}`
* **예시**: `picoCTF{updater.exe_AA29184B0291}`

## 6. 출제자 노트 & 파일 제작 가이드
* **아티팩트 제작 방법**:
  1. 가상 머신(Windows 10/11)을 기동합니다.
  2. 임의의 파일 `C:\Users\Public\updater.exe`를 임시로 만들어 두고, 레지스트리 편집기(`regedit`)를 실행하여 `HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Run` 키 하위에 `SystemUpdate` 라는 이름의 문자열 값으로 경로를 추가 등록합니다.
  3. 시리얼 번호가 확인 가능한 USB 메모리 스틱을 가상 머신에 1회 마운트 해제합니다.
  4. 윈도우 OS의 활성 레지스트리 잠금을 피하기 위해 별도 도구(예: FTK Imager)를 띄워 `C:\Windows\System32\config\SYSTEM`, `SOFTWARE` 파일 및 `C:\Users\<계정명>\NTUSER.DAT` 파일을 추출하여 아티팩트로 저장 및 배포합니다.
* **출제 포인트**: 
  * 윈도우 환경 침해 분석의 핵심인 지속성 메커니즘과 호스트 기반 흔적(Artifact) 중 가장 기본이 되는 레지스트리 트리 구조 탐색법을 체계화합니다.

## 7. 트러블슈팅 및 힌트
* **Q. SYSTEM 파일 내의 CurrentControlSet 경로가 존재하지 않습니다.**
  * A. 오프라인 레지스트리 파일 내에서 `CurrentControlSet`은 직접 나타나지 않으며, `ControlSet001` 또는 `ControlSet002`와 같은 이름으로 저장되어 있습니다. 통상 `SYSTEM` 하이브의 `Select` 키 내에 명시된 `Current` 값(예: 1인 경우 `ControlSet001`)을 추적하여 대체 분석하여야 합니다.
* **Q. USBSTOR 일련번호 맨 끝에 &0 이 붙어 있습니다. 이것도 일련번호의 일부인가요?**
  * A. 윈도우 하부 버스 드라이버에서 인식하는 인스턴스 구분 지시자(`&0`, `&1` 등)는 실제 USB 시리얼 번호에 포함되지 않는 윈도우만의 접미사입니다. 앰퍼샌드(`&`) 문자 직전까지의 문자열만 순수 고유 일련번호로 추출해야 올바른 답안으로 처리됩니다.

## 8. 학습 포인트
* **윈도우 포렌식 흔적**: 시스템 설정과 사용자 행위 정보가 중앙 집중되어 관리되는 윈도우 레지스트리의 특성을 파악합니다.
* **지속성(Persistence) 분석**: 공격자가 내부 침투 후 흔히 사용하는 시작 프로그램 우회 등록 및 그 흔적을 레지스트리 파일 파싱을 통해 식별하는 IR 조사 기법을 체계적으로 이해합니다.
