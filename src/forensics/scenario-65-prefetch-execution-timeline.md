---
title: 윈도우 프리페치 기반 애플리케이션 실행 순서 복구 (Windows Prefetch Timeline Analysis)
created: 2026-06-28
updated: 2026-06-28
type: ctf-challenge
tags: [ctf, ctf-challenge, forensics, windows, prefetch, execution-timeline, timeline, csv]
confidence: high
---

# 윈도우 프리페치 기반 애플리케이션 실행 순서 복구 (Windows Prefetch Timeline Analysis)

> **난이도**: 초급  
> **소요 시간**: 15~20분  
> **참고 picoCTF 문제**: 악성 실행 이력 전후 상황 규명 (Windows Prefetch Timeline 분석)

## 1. 배경 시나리오
사내 윈도우 PC에서 악성 바이너리가 다운로드 및 작동한 위협 정황이 식별되었습니다. 침해 대응팀은 침입자가 시스템 진입 후 어떤 프로그램들을 사용하여 정찰을 수행하고 백도어를 연동했는지 타임라인 순으로 실행 행위를 증명해야 합니다. 조사관은 프리페치 디렉터리(`C:\Windows\Prefetch\`) 하위의 `.pf` 메타데이터 파일들을 일괄 파싱하여 생성한 애플리케이션 통합 기동 기록 테이블인 `prefetch_timeline.csv` 파일을 확보했습니다. 이 CSV 데이터의 마지막 실행 시간(Last Run Time) 속성을 기준으로 타임라인을 정렬하여, **악성코드 파일인 `malware.exe`가 구동되기 직전과 직후에 각각 긴밀히 연동 실행된 프로세스 명칭 조합(플래그)**을 특정하십시오.

## 2. 제공 파일
* `prefetch_timeline.csv` (PECmd 등의 파서로 프리페치 디렉터리를 일괄 파싱하여 프로그램 실행 시점들을 기록한 CSV 타임라인 파일)

## 3. 문제 목표
윈도우 프리페치(Prefetch) 아티팩트의 기록 특성(프로그램 최초/최근 실행 횟수, Windows 8 이상부터 최대 8개의 과거 실행 타임스탬프를 보존하는 다중 실행 시각 레코드 정보)을 이해하고, 시간 정렬 대조를 통해 악성 프로세스 구동 전후의 실행 흐름을 규명합니다.

## 4. 의도한 풀이 흐름
1. **CSV 데이터 구조 검사**:
   * 제공된 `prefetch_timeline.csv` 파일을 엽니다.
   * 각 프로그램의 실행 메타 데이터 필드들을 식별합니다:
     `Executable Name | Run Count | Last Run Time | Previous Run Time 1 | Previous Run Time 2`
2. **타임라인 정렬 (Chronological Sorting)**:
   * 프로그램들의 최신 실행 시간 속성인 `Last Run Time` 컬럼 데이터를 오름차순(시간이 과거에서 미래로 흐르도록) 정렬합니다.
   * 사건 당시인 `2026-06-28 10:20:00` 근처의 프로세스 기동 타임라인을 좁혀 관찰합니다:
     * `2026-06-28 10:18:25`: `whoami.exe` (실행 횟수: 1)
     * `2026-06-28 10:19:10`: `powershell.exe` (실행 횟수: 3)
     * **`2026-06-28 10:20:00`: `malware.exe` (실행 횟수: 1)**
     * `2026-06-28 10:20:45`: `cmd.exe` (실행 횟수: 5)
     * `2026-06-28 10:21:30`: `ipconfig.exe` (실행 횟수: 1)
3. **직전/직후 실행 프로세스 판별**:
   * `malware.exe` 가 실행된 시점인 `10:20:00` 바로 직전(`10:19:10`)에 작동한 파일은 `powershell.exe` 임을 확인합니다.
   * `malware.exe` 가 실행된 시점인 `10:20:00` 바로 직후(`10:20:45`)에 작동한 파일은 `cmd.exe` 임을 확인합니다.
4. **플래그 결합**:
   * 요구된 포맷(직전파일명_직후파일명_run_sequence)에 매핑하여 최종 플래그를 정립합니다:
     `picoCTF{powershell.exe_cmd.exe_run_sequence}`

## 5. 정답(플래그) 규칙 및 예시
* **플래그 형식**: `picoCTF{<process_before>_<process_after>_run_sequence}`
* **예시**: `picoCTF{powershell.exe_cmd.exe_run_sequence}`

## 6. 출제자 노트 & 파일 제작 가이드
* **아티팩트 제작 방법**:
  1. Windows 10/11 가상 머신에서 명령 프롬프트를 열고 다음 도구들을 순서대로 실행시킵니다:
     - `whoami`
     - 파워셸 구동 (`powershell.exe -Command "Write-Output 'Trigger'"` 등)
     - 모의 악성 실행 파일 작동 (`malware.exe`)
     - 명령 프롬프트 서브 셸 작동 (`cmd.exe`)
     - `ipconfig`
  2. 시스템 프리페치 보존 경로(`C:\Windows\Prefetch\`)로 이동하여 위 5가지 프로세스 고유 해시명이 부여된 `.pf` 파일들이 갱신되었는지 검증합니다 (예: `POWERSHELL.EXE-XXXXXXXX.pf`, `MALWARE.EXE-XXXXXXXX.pf` 등).
  3. Eric Zimmerman의 `PECmd` 유틸리티를 가동하여 프리페치 디바이스 데이터를 CSV 파일로 덤프합니다:
     `PECmd.exe -d C:\Windows\Prefetch --csv output_dir`
  4. 도출된 `prefetch_timeline.csv` 파일의 불필요한 백그라운드 노이즈 레코드들을 정리하고, 타임라인 침투 순서가 직관적으로 확인되도록 데이터를 필터 가공하여 학생용 챌린지 파일로 지정합니다.
* **출제 포인트**: 
  * 윈도우 포렌식에서 프로그램 기동 증적을 대변하는 대표적인 실행 아티팩트인 프리페치(Prefetch Forensics)를 활용하여, 위협 시나리오 분석 시 악성 행위자의 횡적 거동 순서 및 침투 타임라인(Activity Timeline Reconstruction)을 수립하는 문제 해결 능력을 평가합니다.

## 7. 트러블슈팅 및 힌트
* **Q. 프리페치 파일명 뒤에 붙는 8자리 헥사코드(예: POWERSHELL.EXE-D6C96C5F.pf)는 어떤 의미인가요?**
  * A. 해당 8자리 16진수 문자열은 실행 파일이 위치하는 **부모 폴더의 절대 경로**와 연동 파라미터 정보 등을 활용하여 운영체제가 계산해 낸 고유 해시값입니다. 동일한 `malware.exe` 파일이 구동되었더라도 `C:\temp\malware.exe`에서 켜진 경우와 `C:\Windows\System32\malware.exe`에서 켜진 경우의 프리페치 해시가 달라 별도의 `.pf` 파일로 개별 박제되므로, 공격 바이너리의 최초 구동지 물리 위치를 특정하는 핵심 이정표로 삼을 수 있습니다.
* **Q. 프리페치는 Windows Server 에디션에서도 기본적으로 작동하나요?**
  * A. 아닙니다. 데스크톱 생산성을 타깃으로 설계된 일반 Windows Client (7, 10, 11 등) 에디션에서는 기본 기능이 활성화되어 있으나, 서버 에디션(Windows Server 2016, 2019, 2022 등)에서는 성능 부하 방지를 위해 레지스트리 설정 상에서 기본 프리페치 활성화 플래그가 비활성화(Disabled) 상태로 출하되는 경우가 많아 침해조사 시 Amcache나 Shimcache 등의 타 아티팩트를 교차 점검해야 합니다.

## 8. 학습 포인트
* **윈도우 프리페치(Prefetch) 구조 및 속성**: 실행 가속 서비스의 작동 원리 및 시스템 파일 기동 횟수/시간 보존 명세를 파악합니다.
* **실행 타임라인 재구성**: 다수의 파싱된 프리페치 로그를 타임라인으로 병합하여, 침해 사고 발생 정황을 연대기 순(Chronology)으로 재구성해 내는 포렌식 추론 능력을 구축합니다.
