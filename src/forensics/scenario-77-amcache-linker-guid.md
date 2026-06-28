---
title: 윈도우 AMCACHE에 잔재하는 지워진 프로그램 컴파일 고유 GUID 특정 (Amcache.hve Program GUID)
created: 2026-06-28
updated: 2026-06-28
type: ctf-challenge
tags: [ctf, ctf-challenge, forensics, windows, registry, amcache, program-guid, execution-history, csv]
confidence: high
---

# 윈도우 AMCACHE에 잔재하는 지워진 프로그램 컴파일 고유 GUID 특정 (Amcache.hve Program GUID)

> **난이도**: 초급  
> **소요 시간**: 15~20분  
> **참고 picoCTF 문제**: 소거된 프로그램 메타데이터 식별 (Windows Amcache Application GUID 분석)

## 1. 배경 시나리오
내부망 데이터 침투에 사용되었던 자작 악성코드 파일이 디스크 상에서 흔적조차 남지 않게 완전 파쇄(Wipe)되어 유실되었습니다. 해당 프로그램 파일의 해시나 경로는 프리페치에서도 삭제되어 사건 규명에 난항을 겪고 있습니다. 하지만 윈도우 OS의 애플리케이션 호환성 캐시인 **Amcache.hve** 레지스트리 내부의 `Root\InventoryApplication` 서브 키 영역은 시스템에 영구 인스톨되거나 구동되었던 응용 프로그램 고유 정보(프로그램 고유 GUID, 버그 리포팅 컴포넌트 정보 등)를 지속적으로 캐시 보존합니다. 수집한 Amcache 프로그램 구동 테이블 보고서인 `amcache_programs_list.csv`를 검색하여, **공격에 활용되었던 독자적 악성 백도어 파일(`custom_exfil_backdoor`)의 컴파일 등록 고유 GUID 식별자(플래그)**를 역추적해 찾으십시오.

## 2. 제공 파일
* `amcache_programs_list.csv` (Amcache.hve 파일 내의 InventoryApplication 목록을 파싱하여 가독 가능하게 가공한 CSV 리포트 파일)

## 3. 문제 목표
윈도우 Amcache.hve 아티팩트의 세부 기록 분과인 `InventoryApplication` 서브 키의 저장 스펙(프로그램 이름, 버전, 배포사, 컴파일 GUID 등 설치 프로그램 카탈로그화 명세)을 이해하고, 지워진 바이너리의 물리 GUID 흔적을 발굴해 냅니다.

## 4. 의도한 풀이 흐름
1. **CSV 리포트 내 프로그램 검색**:
   * 제공된 `amcache_programs_list.csv` 파일을 엽니다.
   * 각 프로그램 항목 중 유출 도구 명칭인 `custom_exfil_backdoor` 항목이 명시된 행을 검색합니다.
2. **프로그램 고유 ID (GUID) 속성 분석**:
   * Amcache 레지스트리는 프로그램의 최초 로딩 시, 운영체제가 해당 응용 프로그램을 고유하게 인덱싱하기 위해 UUID/GUID 형식의 **Program ID** 또는 **Application ID** 값을 하이브 노드명으로 할당 정의합니다.
   * `custom_exfil_backdoor` 행의 데이터 속성을 확인합니다:
     * **프로그램 이름 (Program Name)**: `custom_exfil_backdoor`
     * **배포사 (Publisher)**: `Unknown Developer`
     * **프로그램 버전 (Version)**: `1.0.0.4`
     * **프로그램 ID (Program ID / GUID)**: `picoCTF{3f8a9b0c-1d2e-3f4a-5b6c-7d8e9f0a1b2c}`
3. **플래그 도출**:
   * 해당 프로그램 ID 컬럼에 적혀 있는 고유 컴파일 식별자인 최종 플래그를 획득합니다:
     `picoCTF{3f8a9b0c-1d2e-3f4a-5b6c-7d8e9f0a1b2c}`

## 5. 정답(플래그) 규칙 및 예시
* **플래그 형식**: `picoCTF{<GUID_value>}`
* **예시**: `picoCTF{3f8a9b0c-1d2e-3f4a-5b6c-7d8e9f0a1b2c}`

## 6. 출제자 노트 & 파일 제작 가이드
* **아티팩트 제작 방법**:
  1. 테스트 Windows PC 환경에서 컴파일된 자작 프로그램 `custom_exfil_backdoor.exe`를 구동합니다. 이때 프로그램 리소스 컴파일 단계에서 고유 컴파일 번호인 GUID 필드에 플래그 규격인 `3f8a9b0c-1d2e-3f4a-5b6c-7d8e9f0a1b2c` 값을 주입 매핑해 둡니다.
  2. 프로그램을 작동시키면 Windows Compatibility Telemetry Engine(호환성 평가 시스템)이 작동하여 가동 바이너리 고유 GUID를 `Amcache.hve` 레지스트리의 `InventoryApplication\<GUID>` 서브 키 경로로 자동 적재합니다.
  3. `Amcache.hve` 파일(ftkimager 등을 활용)을 적출합니다.
  4. `AmcacheParser.exe`를 실행하여 `InventoryApplication` 대응 CSV 출력을 생성합니다:
     `AmcacheParser.exe -f Amcache.hve --csv output_dir`
  5. 출력 보고서 중 `*InventoryApplication.csv` 내에서 해당 악성 파일의 등록 GUID 행을 확인 정제한 뒤 `amcache_programs_list.csv` 파일로 빌드해 유저에게 제공합니다.
* **출제 포인트**: 
  * 실행 바이너리 자체가 완전히 마스킹되거나 카빙 복구할 수 없는 상태라 하더라도, OS 텔레메트리 보존 목적으로 백그라운드 저장소(`Amcache.hve`)에 컴파일 제품 프로필 명세와 함께 하드코딩되는 애플리케이션 식별 GUID 흔적(Amcache Program Inventory Forensics)을 역색인하여 공격 증적을 복원해 내는 조사 기법을 훈련시킵니다.

## 7. 트러블슈팅 및 힌트
* **Q. InventoryApplicationFile과 InventoryApplication의 차이는 무엇인가요?**
  * A. `InventoryApplicationFile`은 개별 실행 바이너리 파일 하나하나의 물리 위치, 크기, SHA-1 파일 해시 정보 등을 상세 기록하지만, `InventoryApplication`은 해당 프로그램이 속한 소프트웨어 패키지 제품 자체(설치 프로그램 카탈로그, 배포사명, 버전 정보, 통합 컴파일 GUID 등)를 인덱싱해 관리하는 단위입니다. 따라서 실행 바이너리 속성(해시) 외에 패키지 제품의 고유 아이덴티티를 추적할 때는 후자인 `InventoryApplication` 영역을 필독 파싱해야 합니다.
* **Q. Amcache.hve 하이브의 수정 타임스탬프를 통해 유용하게 알 수 있는 것은 무엇인가요?**
  * A. Amcache 내의 개별 프로그램 GUID 서브 키의 **Last Write Time**은 해당 프로그램이 시스템에 최초 감지(설치 또는 최초 실행)된 시간에 정확히 정렬되므로, 공격 악성코드 제품군이 로컬 운영체제에 최초로 침투 이식된 동작 타임라인을 파악하는 결정적인 보안 타임라인 증적으로 삼을 수 있습니다.

## 8. 학습 포인트
* **윈도우 Amcache 텔레메트리 스키마**: 호환성 원격 모니터링 감사 엔진의 데이터 수집 스펙 및 `InventoryApplication` 제품 프로파일 적재 원리를 학습합니다.
* **소프트웨어 고유 GUID 식별**: 소거된 미확인 바이너리에 대해 Amcache에 잔재하는 제품 메타데이터 레코드를 파싱하여 컴파일 아이덴티티를 입증하는 디지털 포렌식 기법을 내재화합니다.
