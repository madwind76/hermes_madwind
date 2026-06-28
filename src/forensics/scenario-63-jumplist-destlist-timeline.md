---
title: 윈도우 최근 폴더 실행 이력 분석 (Jump Lists DestList MRU Timeline)
created: 2026-06-28
updated: 2026-06-28
type: ctf-challenge
tags: [ctf, ctf-challenge, forensics, windows, jumplist, destlist, timeline, mru, csv]
confidence: high
---

# 윈도우 최근 폴더 실행 이력 분석 (Jump Lists DestList MRU Timeline)

> **난이도**: 초중급  
> **소요 시간**: 20~25분  
> **참고 picoCTF 문제**: 사용자 접근 폴더 실행 시간 분석 (Windows Jump Lists Timeline 포렌식)

## 1. 배경 시나리오
특정 비인가 USB 저장 장치가 사내 PC에 마운트된 후 내부의 여러 민감 폴더들이 열람 및 탈취된 기밀 유출 혐의가 포착되었습니다. 피의자는 외장 드라이브를 꽂은 사실만 인정할 뿐 기밀 폴더에 진입해 내부를 훑어본 적은 없다고 부인하고 있습니다. 침해사고 분석가는 윈도우 파일 탐색기(File Explorer, AppID 해시: `1b41ee3a1b423b4c`)가 사용하는 자동 점프 리스트 메타 파일의 내부 구조체인 **DestList(최근 항목 리스트)**를 파싱하여 시간 순 정렬한 `destlist_mru_parsed.csv` 데이터를 확보했습니다. 이 타임라인 데이터를 정밀 분석하여, **사건 당일 피의자가 가장 마지막 시점에 최종 진입(액세스)했던 폴더 경로에 명시된 플래그**를 구하십시오.

## 2. 제공 파일
* `destlist_mru_parsed.csv` (JLECmd를 사용해 윈도우 탐색기 점프 리스트 내 `DestList` 스트림을 파싱한 타임라인 추출 테이블 파일)

## 3. 문제 목표
윈도우 파일 탐색기 점프 리스트 파일(`1b41ee3a1b423b4c.automaticDestinations-ms`)의 `DestList` 엔트리 구조를 이해하고, 각 연결 이력 레코드에 남은 접근 타임스탬프(Access Time) 속성을 기준으로 시간 순 타임라인 분석을 수행하여 마지막 행위 이력을 판별합니다.

## 4. 의도한 풀이 흐름
1. **CSV 데이터 분석**:
   * 제공된 `destlist_mru_parsed.csv` 파일을 텍스트 뷰어나 스프레드시트 툴로 엽니다.
   * 테이블 구조는 다음과 같습니다:
     `EntryNo | MRU | TargetPath | CreationTime | ModificationTime | AccessTime | AppID`
2. **시간 데이터 정렬 (타임라인 구축)**:
   * 피의자의 횡적 행위를 추적하기 위해 `AccessTime` (접근 시간) 컬럼을 기준으로 데이터를 **내림차순 (최신 시각이 맨 위로 오도록)** 정렬합니다.
   * 예시 레코드 대조:
     * `Entry 3`: `2026-06-28 10:14:02` -> `C:\Windows\System32`
     * `Entry 1`: `2026-06-28 10:45:10` -> `D:\Backup`
     * `Entry 4`: `2026-06-28 11:15:30` -> `D:\Backup\picoCTF{destlist_mru_folder_timeline_solved}`
3. **최종 접근 대상 추출**:
   * 가장 최근 시각인 `2026-06-28 11:15:30`에 접근한 것으로 로깅된 대상 폴더 경로(`TargetPath`)를 확보합니다:
     `D:\Backup\picoCTF{destlist_mru_folder_timeline_solved}`
4. **플래그 도출**:
   * 마지막 접근 폴더명에서 최종 플래그를 정립합니다:
     `picoCTF{destlist_mru_folder_timeline_solved}`

## 5. 정답(플래그) 규칙 및 예시
* **플래그 형식**: `picoCTF{<flag_string>}`
* **예시**: `picoCTF{destlist_mru_folder_timeline_solved}`

## 6. 출제자 노트 & 파일 제작 가이드
* **아티팩트 제작 방법**:
  1. 윈도우 가상 머신에 외장 드라이브(D 드라이브)를 할당합니다.
  2. D 드라이브 하위에 기밀 폴더 `picoCTF{destlist_mru_folder_timeline_solved}`를 생성합니다.
  3. 윈도우 탐색기(`explorer.exe`)를 띄워 D 드라이브 내 여러 폴더(`D:\Backup`, `C:\Windows` 등)를 순차적으로 열어본 뒤, 최종적으로 `D:\Backup\picoCTF{destlist_mru_folder_timeline_solved}` 경로로 탐색기 포커스를 이동해 창을 닫습니다. (탐색기 윈도우가 닫힐 때 점프 리스트 `DestList` 구조체에 해당 시점의 최종 AccessTime이 기표됩니다)
  4. 탐색기 전용 자동 점프 리스트 파일(`%USERPROFILE%\AppData\Roaming\Microsoft\Windows\Recent\AutomaticDestinations\1b41ee3a1b423b4c.automaticDestinations-ms`)을 확보합니다.
  5. `JLECmd` CLI 도구를 돌려 파싱 결과 CSV를 출력하고, 이를 `destlist_mru_parsed.csv`로 정제하여 학생들에게 배포합니다.
* **출제 포인트**: 
  * 개별 단축 LNK 이력 외에, 윈도우 탐색기 전용 AppID(`1b41ee3a1b423b4c`)가 갖는 특징을 숙지하고, `DestList` 타임라인 정렬 분석(Timeline Chronology)을 통해 침해 사고 행위의 인과관계 및 행위 순서를 재구성하는 분석가 역량을 교육합니다.

## 7. 트러블슈팅 및 힌트
* **Q. 탐색기가 사용하는 점프 리스트 고유 ID는 왜 항상 1b41ee3a1b423b4c 인가요?**
  * A. 마이크로소프트가 제공하는 빌트인 윈도우 셸 탐색기 실행 바이너리의 절대 설치 경로(`C:\Windows\explorer.exe`)를 윈도우 AppID 생성 알고리즘으로 직렬화한 최종 CRC-64 값이 `1b41ee3a1b423b4c` 이기 때문입니다. 운영체제가 윈도우인 모든 호스트 시스템에서 파일 탐색기의 최근 사용 이력은 이 ID의 점프 리스트 파일에 영구 매핑되어 저장됩니다.
* **Q. MRU 번호와 AccessTime 중 어떤 데이터를 신뢰해야 시간 선후 관계가 명확한가요?**
  * A. 원칙적으로는 두 속성이 지시하는 순서가 수렴합니다. 다만, 윈도우 업데이트나 서드파티 탐색기 도구 사용 시 간혹 MRU 정렬 인덱스가 꼬이는 예외적인 오동작이 발생할 수 있으므로, 각 개별 LNK 스트림이 보유하는 64비트 FILETIME 형식의 `Last Access Time` 속성을 1순위로 대조하는 것이 타임라인 포렌식의 정석입니다.

## 8. 학습 포인트
* **윈도우 탐색기 아티팩트 특성**: 파일 탐색기가 폴더 접근 이력을 개별 사용자 프로필 아래 점프 리스트 형태로 유지하는 구조와 원리를 학습합니다.
* **디지털 포렌식 타임라인 분석**: 수집된 파일시스템 메타데이터(MACB) 중 시간 속성을 정렬하여, 특정 침해 의심 구간 전후의 행위 흐름을 순차적으로 증명해 내는 방법론을 마스터합니다.
