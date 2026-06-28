---
title: 다중 아티팩트 종합 침해 사건 타임라인 재구성 (Multi-Artifact Incident Timeline Reconstruction)
created: 2026-06-28
updated: 2026-06-28
type: ctf-challenge
tags: [ctf, ctf-challenge, forensics, timeline-analysis, multi-artifact, dfir, event-log, prefetch, lnk-file, amcache, csv]
confidence: high
---

# 다중 아티팩트 종합 침해 사건 타임라인 재구성 (Multi-Artifact Incident Timeline Reconstruction)

> **난이도**: 중급 (종합)  
> **소요 시간**: 35~40분  
> **참고 picoCTF 문제**: 다중 시스템 감사 타임라인 교차 상관관계 분석 (DFIR Timeline Reconstruction)

## 1. 배경 시나리오
사내 AD 도메인 컨트롤러 시스템에 대한 정교한 표적 공격(APT)이 수행되어 관리자 계정이 탈취되고 여러 내부 중요 기밀 문서가 유출되었습니다. 침해 대응팀(DFIR)은 서버에서 추출한 여러 핵심 포렌식 아티팩트들(윈도우 보안 이벤트 로그, 프리페치 실행 이력, LNK 최근 바로가기 메타데이터, Amcache 애플리케이션 등록 테이블)을 파싱하여 사건 관련 시간대 항목들을 비정렬 상태로 취합한 종합 마일스톤 보고서인 `incident_timeline_reconstruction.csv`를 확보했습니다. 각 아티팩트별 발생 시간대는 제각각 흩어져 섞여 있으나, **모든 사건 엔트리를 UTC 시간 순서대로 정밀 정렬(Chronological Sorting)하여 배치**하면, 각 행에 할당되어 파편화되어 있던 **데이터 단편(Data Fragment) 문자열들이 순서대로 조립되어 하나의 완성된 플래그**를 구성하게 됩니다. 취합된 다중 아티팩트 타임라인 데이터를 시간 순으로 분석 및 재정렬하여 최종 플래그를 구출하십시오.

## 2. 제공 파일
* `incident_timeline_reconstruction.csv` (보안 로그, 프리페치, LNK, Amcache 시간 흔적을 무작위 순서로 병합해 기입해 둔 CSV 타임라인 파일)

## 3. 문제 목표
디지털 포렌식 및 침해 사고 조사(DFIR)의 핵심 연산 기법인 다중 소스 아티팩트 타임라인(Timeline Analysis) 정렬 및 교차 비교 분석의 중요성을 습득하고, 다양한 시스템 감사 아티팩트들의 시간 기표 속성(Event Logon Time, Prefetch Last Run, LNK Target Creation, Amcache Last Write)을 통합 분석합니다.

## 4. 의도한 풀이 흐름
1. **타임라인 CSV 데이터 적재 및 구조 파악**:
   * 제공된 `incident_timeline_reconstruction.csv` 파일을 엽니다.
   * 테이블 컬럼 구조를 확인합니다:
     `Timestamp | Artifact Type | Source File/Key | Description | Data Fragment`
2. **시간(Timestamp) 컬럼 기점 오름차순 정렬**:
   * 각 아티팩트 행은 시간 흐름과 무관하게 무작위 셔플링되어 섞여 있습니다.
   * 스프레드시트 도구(Excel, LibreOffice Calc 등)의 정렬 기능을 활용하거나, 파이썬 스크립트 또는 셸 명령어(`sort`)를 사용하여 **Timestamp (첫 번째 열) 값을 기준으로 과거에서 현재(오름차순) 순으로 행들을 정렬**합니다:
     * 파이썬 정렬 예시:
       ```python
       import pandas as pd
       df = pd.read_csv('incident_timeline_reconstruction.csv')
       # Timestamp 열을 datetime으로 변환 후 정렬
       df['Timestamp'] = pd.to_datetime(df['Timestamp'])
       sorted_df = df.sort_values(by='Timestamp')
       # 정렬된 Data Fragment 컬럼 문자열 결합
       flag = "".join(sorted_df['Data Fragment'].tolist())
       print(flag)
       ```
3. **정렬된 시간 순서 매핑 대조**:
   * 시간 순서 정렬이 정상 완료되었을 때의 레코드 타임라인 순서는 다음과 같이 환원됩니다:
     1. `2026-06-28 10:00:15` | Security Event ID 4624 | CONTOSO\admin 로그인 성공 | **`pico`**
     2. `2026-06-28 10:05:30` | LNK Target Timestamp | USB 내 attack.exe 인덱스 생성 | **`CTF{`**
     3. `2026-06-28 10:12:45` | Amcache.hve Key Write | malware_loader 최초 감지 등록 | **`mult`**
     4. `2026-06-28 10:20:10` | Windows Prefetch pf | VPN_Client.exe 최초 가동 | **`i_ar`**
     5. `2026-06-28 10:25:35` | Security Event ID 7045 | 백도어 서비스 신규 설치 등록 | **`t1fa`**
     6. `2026-06-28 10:30:00` | Windows Shellbags | Secret_Data 공유 폴더 오픈 접근 | **`ct_t`**
     7. `2026-06-28 10:35:15` | Security Event ID 4624 | 원격 침투용 세션 수립 성공 | **`1mel`**
     8. `2026-06-28 10:40:40` | Windows Prefetch pf | AnyDesk.exe 화면 제어 툴 기동 | **`1n3_`**
     9. `2026-06-28 10:45:20` | Security Event ID 1102 | 흔적 은닉 목적 감사 로그 강제 삭제 | **`sor`**
     10. `2026-06-28 10:50:55` | Memory Dump | sftp-server 프로세스 강제 core 백업 | **`t3d}`**
4. **플래그 결합 및 도출**:
   * 정렬된 순서대로 `Data Fragment` 아스키 조각들을 결합하여 최종 플래그를 도출합니다:
     `picoCTF{multi_art1fact_t1mel1n3_sort3d}`

## 5. 정답(플래그) 규칙 및 예시
* **플래그 형식**: `picoCTF{<flag_string>}`
* **예시**: `picoCTF{multi_art1fact_t1mel1n3_sort3d}`

## 6. 출제자 노트 & 파일 제작 가이드
* **아티팩트 제작 방법**:
  1. 기밀 플래그 문자열인 `picoCTF{multi_art1fact_t1mel1n3_sort3d}`를 10개의 파편 문자열 조각(`pico`, `CTF{`, `mult`, `i_ar`, `t1fa`, `ct_t`, `1mel`, `1n3_`, `sor`, `t3d}`)으로 세분화합니다.
  2. 침해 시나리오 시간적 인과 순서에 맞춰 10개 아티팩트의 생성 날짜/시간 타임스탬프를 과거 순서대로 균등 매핑합니다.
  3. 순서대로 정렬 기입한 행 데이터를 작성한 뒤, 학생들이 직관적으로 연산하기 어렵도록 데이터 정렬 순서를 강제로 무작위 셔플링(Shuffle)하여 섞습니다.
  4. 셔플된 최종 상태 데이터를 `incident_timeline_reconstruction.csv` 파일로 빌드 저장하여 학생 배포 챌린지 파일로 확정 제공합니다.
* **출제 포인트**: 
  * 본 챌린지는 100종의 초급 포렌식 문제 셋을 최종 마무리하는 **종합 문제(Capstone Challenge)**로 기능합니다. 수사관이 현장에서 직면하게 되는 단편화된 포렌식 개별 흔적들(Event Logs, Prefetch, LNK, Amcache, Shellbags, Process Dumps)의 발생 타임스탬프를 UTC 타임라인 기준 오름차순으로 정교하게 연동 정렬(DFIR Timeline Cross-Correlation)함으로써, 침입 킬체인 단계를 논리적으로 입증하고 기밀 플래그를 정립해 내는 최고 수준의 종합 분석 기틀을 다지도록 설계되었습니다.

## 7. 트러블슈팅 및 힌트
* **Q. CSV 파일 정렬 시 10:00:15 과 10:05:30 중 어느 것이 더 과거인가요?**
  * A. 시간 정렬은 오름차순(과거 -> 최신) 순으로 해야 합니다. 즉, 오전 10시 0분 15초(`10:00:15`)에 일어난 사건이 오전 10시 5분 30초(`10:05:30`)에 발생한 사건보다 먼저 발생한 과거의 흔적이므로 정렬 테이블 상단에 위치해야 문자열이 꼬이지 않고 정확한 순서로 정렬이 완성됩니다.
* **Q. 리눅스 CLI 환경에서 도구 없이 순수 Bash 명령어로만 행 정렬 및 플래그 결합을 하려면 어떻게 하나요?**
  * A. `sort` 명령어와 `awk` 유틸리티를 조합하여 커맨드라인 한 줄로 손쉽게 해결할 수 있습니다:
     ```bash
     # CSV 헤더 행을 제외하고 첫 번째 열(Timestamp) 기준으로 정렬 후 5번째 열(Fragment)만 합쳐 출력
     tail -n +2 incident_timeline_reconstruction.csv | sort -t',' -k1 | cut -d',' -f5 | tr -d '\n'
     ```
     위 명령 파이프라인을 사용하면 엑셀 등 GUI 스프레드시트 가동 없이도 1초 만에 완성 플래그를 다이렉트로 결합 추출할 수 있어 수사 속도를 비약적으로 높일 수 있습니다.

## 8. 학습 포인트
* **다중 아티팩트 타임라인 교차 상관관계(Cross-Correlation) 분석**: 윈도우/리눅스 통합 이종 감사 이력을 동일 타임스탬프 스키마 상으로 환원 비교하는 DFIR 마일스톤 설계 능력을 갖춥니다.
* **침해 사고 조사 종합 킬체인 규명**: 계정 로그인부터 영속성 수립, 기밀 폴더 오픈, 원격 화면 제어 및 마지막 흔적 인멸에 이르는 전체 위협 수명 주기를 시간 순으로 입증 및 규명하는 디지털 포렌식 분석가로 최종 성장합니다.
