---
title: 윈도우 프리페치 기반 악성 스크립트 실행 이력 추적 (Powershell Execution - Prefetch)
created: 2026-06-28
updated: 2026-06-28
type: ctf-challenge
tags: [ctf, ctf-challenge, forensics, windows, prefetch, powershell, execution-history, pecmd, metadata]
confidence: high
---

# 윈도우 프리페치 기반 악성 스크립트 실행 이력 추적 (Powershell Execution - Prefetch)

> **난이도**: 초급  
> **소요 시간**: 15~20분  
> **참고 picoCTF 문제**: 삭제된 파워셸 스크립트 실행 흔적 역추적 (Windows Powershell Prefetch Referenced Files 분석)

## 1. 배경 시나리오
공격자가 윈도우 호스트에 침투하여 파워셸(`powershell.exe`)을 가동해 임시 폴더에 받아둔 악성 다운로더 스크립트(`*.ps1`)를 실행시켰습니다. 공격자는 실행 직후 흔적을 인멸하기 위해 파워셸 콘솔 명령 히스토리 파일(`ConsoleHost_history.txt`)을 비우고 임시 폴더 내의 스크립트 본문도 삭제했습니다. 하지만 윈도우 OS는 응용 프로그램 가동 시 최적화를 위해 생성하는 프리페치 파일(`.pf`) 내부에 **최초 실행 10초 이내에 로딩 및 핸들 액세스한 파일 목록(Referenced Files)**을 고스란히 기록해 둡니다. 확보한 파워셸 프리페치 파일인 `POWERSHELL.EXE-4D567B89.pf`를 분석하여, **가동 당시 실행 매개체로 호출되었던 원본 악성 스크립트 파일명 속의 플래그**를 획득하십시오.

## 2. 제공 파일
* `POWERSHELL.EXE-4D567B89.pf` (사용자 PC에서 수집한 PowerShell 실행 대응 윈도우 프리페치 바이너리 파일)

## 3. 문제 목표
윈도우 프리페치(Prefetch) 파일의 세부 데이터 스펙(프로그램 실행 초기 10초 동안 로딩되는 스크립트, DLL 및 리소스 파일 경로 목록)을 이해하고, 전문 프리페치 파서 도구(PECmd 등)를 활용하여 지워진 스크립트 파일의 유입명을 복원합니다.

## 4. 의도한 풀이 흐름
1. **프리페치 아티팩트 파싱**:
   * 제공된 `POWERSHELL.EXE-4D567B89.pf` 파일을 분석하기 위해 Eric Zimmerman의 `PECmd.exe` 도구를 구동합니다:
     `PECmd.exe -f POWERSHELL.EXE-4D567B89.pf`
   * 혹은 리눅스 커맨드라인 환경에서 파이썬 기반 프리페치 파서를 사용하여 아웃풋 텍스트를 획득합니다.
2. **참조 파일 목록 (Referenced Files) 감사**:
   * 도구가 출력한 결과 중 **Referenced Files (참조된 파일 목록)** 섹션으로 이동합니다.
   * 파워셸이 가동되며 로드했던 시스템 DLL 파일들 및 사용자 임시 디렉터리 경로 내의 파일 흔적을 대조합니다:
     * `\DEVICE\HARDDISKVOLUME2\WINDOWS\SYSTEM32\POWERSHELL.EXE`
     * `\DEVICE\HARDDISKVOLUME2\USERS\ADMIN\APPDATA\LOCAL\TEMP\picoCTF{ps_script_pf_run_detected}.PS1`
   * 임시 폴더(`Temp`) 하위에서 파워셸에 의해 최초 10초 이내에 핸들 로드되어 기록에 남은 비정상 악성 스크립트 파일명을 포착합니다.
3. **플래그 도출**:
   * 탐색된 스크립트 파일명 자체에서 최종 플래그 값을 획득합니다:
     `picoCTF{ps_script_pf_run_detected}`

## 5. 정답(플래그) 규칙 및 예시
* **플래그 형식**: `picoCTF{<flag_string>}`
* **예시**: `picoCTF{ps_script_pf_run_detected}`

## 6. 출제자 노트 & 파일 제작 가이드
* **아티팩트 제작 방법**:
  1. Windows 10/11 가상 머신의 임시 폴더(`C:\Users\admin\AppData\Local\Temp\`) 하위에 기밀 플래그 파일 `picoCTF{ps_script_pf_run_detected}.ps1`을 사전 생성해 놓습니다.
  2. 파워셸을 켜고 해당 스크립트를 로드 구동시킵니다:
     `powershell.exe -File C:\Users\admin\AppData\Local\Temp\picoCTF{ps_script_pf_run_detected}.ps1`
     (이 구동 직후 프리페치 모니터 드라이버가 파워셸 프로세스의 해당 ps1 파일 핸들 오픈 이력을 프리페치 참조 리스트 버퍼에 기록합니다)
  3. `C:\Windows\Prefetch\` 경로로 진입하여 타임스탬프가 갱신된 `POWERSHELL.EXE-XXXXXXXX.pf` 파일을 안전 복제하여 적출합니다.
  4. 적출한 바이너리를 학생 수검용 파일로 배포 포장합니다.
* **출제 포인트**: 
  * 스크립트 실행 이력 자체를 지우고 도망친 지능형 공격 분석 시, 윈도우 OS 캐시 메커니즘(Windows Prefetch Referenced Files)에 의해 파워셸 인스턴스가 런타임에 로드했던 파일 경로 목록에 고스란히 남아 있는 흔적을 역파싱하여 악성 스크립트 존재 자체를 역규명하는 디지털 포렌식 실무 능력을 배양합니다.

## 7. 트러블슈팅 및 힌트
* **Q. 파워셸을 단순히 cmd 창에서 기동한 경우에도 프리페치에 ps1 파일 흔적이 남나요?**
  * A. 네, 그렇습니다. 파워셸 스크립트가 실행될 때 파워셸 인터프리터(`powershell.exe`)가 대상 스크립트의 소스 코드를 읽어들이기 위해 해당 파일 핸들을 오픈합니다. 이 동작은 프로그램 가동 초기 10초 이내에 수반되는 핵심 디스크 I/O 작업에 해당하므로, 윈도우 프리페치 수집 규칙에 따라 해당 스크립트의 물리 경로가 프리페치 내부의 "참조 파일 목록" 테이블에 고스란히 영구 적재되게 됩니다.
* **Q. 프리페치가 없는 리눅스 환경에서는 스크립트 로드 흔적을 어떻게 찾나요?**
  * A. 리눅스 환경의 경우 시스템 감사 로그(`auditd`)에서 파일 오픈 관련 시스템 콜(`open`, `openat` 등) 이벤트를 활성화하여 추적하고 있거나, 배시 셸의 명령어 히스토리(`.bash_history`) 내에 기입된 인자값을 분석하여 실행되었던 셸 스크립트 경로명을 규명해야 합니다.

## 8. 학습 포인트
* **윈도우 프리페치(Prefetch) I/O 감사**: 프로그램 시작 10초 이내에 수반되는 디스크 참조 이력 수집 명세를 완벽히 습득합니다.
* **비인가 스크립트 흔적 감사**: 파워셸 콘솔 기록이 유실된 환경에서 프리페치 참조 파일 목록을 역추적하여, 가동 시 사용되었던 스크립트 파일명을 성공적으로 파악하는 분석 능력을 갖춥니다.
