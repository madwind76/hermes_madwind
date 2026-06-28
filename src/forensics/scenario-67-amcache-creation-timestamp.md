---
title: 윈도우 AMCACHE를 활용한 유입 바이너리 최초 실행 시각 규명 (Amcache.hve Timestamp)
created: 2026-06-28
updated: 2026-06-28
type: ctf-challenge
tags: [ctf, ctf-challenge, forensics, windows, registry, amcache, timestamp, execution-time, csv]
confidence: high
---

# 윈도우 AMCACHE를 활용한 유입 바이너리 최초 실행 시각 규명 (Amcache.hve Timestamp)

> **난이도**: 초급  
> **소요 시간**: 15~20분  
> **참고 picoCTF 문제**: 최초 실행 시점 타임스탬프 특정 (Windows Amcache Key Last Write Time 분석)

## 1. 배경 시나리오
공격자가 스피어피싱 또는 다운로더를 통해 사내 PC에 최초로 배포한 악성 유입 바이너리 `exfil_agent.exe` 파일의 **실제 최초 실행 시각(First Run Time)**을 증명해야 합니다. 용의자는 해당 파일이 시스템에 적재되어 있던 것은 인정하나 실행은 시키지 않았다고 부인하고 있으며, 프리페치와 이벤트 로그는 삭제되어 부재합니다. 분석가는 윈도우 응용 프로그램 호환성 데이터베이스 하이브 파일인 `Amcache.hve`를 PECmd 또는 AmcacheParser 도구로 추출하여 작성된 `amcache_parsed_applications.csv` 파일을 획득했습니다. 이 데이터를 정밀 진증하여 **해당 악성 바이너리가 최초 구동되었을 때 생성된 레지스트리 키의 최종 수정 시간(Key Last Write Time, 플래그)**을 특정하십시오.

## 2. 제공 파일
* `amcache_parsed_applications.csv` (Amcache.hve 파일 내의 `InventoryApplicationFile` 테이블 항목들을 파싱하여 보관한 콤마 분할 텍스트 파일)

## 3. 문제 목표
윈도우 Amcache 하이브 파일이 갖는 메타데이터 기록 메커니즘을 이해하고, 특정 프로그램이 시스템에서 최초 실행될 때 관련 키 스키마가 처음 구성되면서 기록되는 레지스트리 키 최종 쓰기 시각(Key Last Write Time)이 디지털 포렌식 관점에서 최초 실행 시각으로 매핑되는 인과관계를 학습합니다.

## 4. 의도한 풀이 흐름
1. **CSV 데이터 분석**:
   * 제공된 `amcache_parsed_applications.csv` 파일을 스프레드시트 또는 텍스트 에디터로 엽니다.
   * 각 프로그램 레코드 행에서 파일명(`exfil_agent.exe`)을 검색합니다.
2. **최초 실행 시각 특정 (Key Last Write Time 추출)**:
   * 윈도우 AppCompat Appraiser 서비스는 어떤 프로그램이 생전 처음 기동될 때, 해당 프로그램의 고유 정보(SHA-1 해시, 파일 크기, 컴파일 타임스탬프)를 저장하기 위해 `Amcache.hve` 레지스트리에 새로운 하위 서브 키를 동적 생성합니다.
   * 이 때문에 해당 서브 키 자체의 최종 생성/쓰기 일시(`Key Last Write Time` 또는 `Last Write Timestamp`)가 바로 대상 파일의 **실측 최초 실행 시각**과 초 단위까지 완벽히 매핑됩니다.
   * `exfil_agent.exe` 엔트리의 속성 필드를 조회합니다:
     * **파일명 (File Name)**: `exfil_agent.exe`
     * **해시 (SHA-1)**: `b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7`
     * **키 최종 쓰기 시간 (Key Last Write Time)**: `2026-06-28 10:45:15`
3. **플래그 도출**:
   * 획득한 타임스탬프 문자열을 지정된 규격 포맷(YYYY-MM-DD_HH:MM:SS)으로 치환하여 최종 플래그를 정립합니다:
     `picoCTF{2026-06-28_10:45:15}`

## 5. 정답(플래그) 규칙 및 예시
* **플래그 형식**: `picoCTF{YYYY-MM-DD_HH:MM:SS}`
* **예시**: `picoCTF{2026-06-28_10:45:15}`

## 6. 출제자 노트 & 파일 제작 가이드
* **아티팩트 제작 방법**:
  1. Windows 10/11 가상 머신에 테스트용 공격 파일 `exfil_agent.exe`를 임의 다운로드 대역에 배치합니다.
  2. 해당 프로그램 `exfil_agent.exe`를 정확히 `2026-06-28 10:45:15` 타임스탬프 부근에 더블 클릭하여 실행합니다. (이때 AppCompat Appraiser가 구동 파일 이벤트를 백그라운드 수집하여 Amcache 하이브 내에 신규 서브 키 항목을 등록하고 Registry Key Write를 실행합니다)
  3. `C:\Windows\appcompat\Programs\Amcache.hve` 파일(잠겨 있으므로 볼륨 복사 또는 로컬 덤프 추출)을 획득합니다.
  4. `AmcacheParser.exe`를 가동하여 CSV 보고서를 출력합니다.
  5. 출력된 CSV 내의 `exfil_agent.exe` 행의 `LastWriteTimestamp` 속성값을 챌린지 요구 시각으로 가공하여 정제된 CSV 파일 `amcache_parsed_applications.csv`로 내보내어 배포합니다.
* **출제 포인트**: 
  * 윈도우 호환성 관리 체계(Windows AppCompat Appraiser)가 갖는 고유한 시간 로깅 정책(Registry Key Last Write Timestamp = Execution Time)의 포렌식적 활용도를 입증하고, 파일 자체의 MACB 수정 일시가 공격자에 의해 타임스톰핑으로 왜곡되었더라도 Amcache에 영구 기록된 실제 최초 실행 시각을 정밀 격리 특정해 내는 역량을 배양합니다.

## 7. 트러블슈팅 및 힌트
* **Q. Amcache에 파일 정보가 등록되었으나 실행 시간 정보가 왜 파일 생성일이나 수정일과 다른가요?**
  * A. 공격자가 디스크에 악성코드를 내려받아 배치한 시간이 `10:00:00` (파일 생성/수정일)이더라도, 실제로 이를 더블 클릭해 작동시킨 시간이 `10:45:15`라면, Amcache 레지스트리 키가 생성(Last Write)되는 시점은 후자인 실행 시점이 됩니다. 따라서 타임스톰핑 도구로 디스크 메타데이터 파일 속성을 덮어써서 교란했더라도 Amcache Registry Key Last Write Time은 OS 레지스트리 커널이 수동 생성하므로 우회가 불가능해 신뢰성이 우수합니다.
* **Q. Amcache.hve의 Registry Key Last Write Time은 윈도우 레지스트리의 어떤 구조적 특징을 대변하나요?**
  * A. 윈도우 레지스트리는 각 키(Key)마다 최하단 서브 노드나 속성이 변경될 때 커널이 키 헤더에 자체 수정 시각(Last Write Time)을 64비트 FILETIME 구조로 자동 기표합니다. 파일시스템과 달리 레지스트리는 사용자가 임의로 이 타임스탬프를 수정할 수 있는 API를 제공하지 않으므로 안티 포렌식 행위에 강력한 내성을 가집니다.

## 8. 학습 포인트
* **윈도우 AppCompat 메타데이터 구조**: OS 애플리케이션 안정성 감사 인프라의 로깅 체계 및 기록 매핑 우선순위를 이해합니다.
* **최초 실행 시점 타임스탬프 수립**: 안티 포렌식(타임스톰핑) 공격을 우회하여, 레지스트리 쓰기 타임스탬프(Registry Key Last Write Time)를 활용해 최초 침해 동작 시점을 초 단위로 증명하는 포렌식 능력을 갖춥니다.
