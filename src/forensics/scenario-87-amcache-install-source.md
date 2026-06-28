---
title: 윈도우 AMCACHE에 기록된 프로그램 최초 설치 소스 디렉터리 경로 추적 (Amcache.hve Source Path)
created: 2026-06-28
updated: 2026-06-28
type: ctf-challenge
tags: [ctf, ctf-challenge, forensics, windows, registry, amcache, install-source, entry-source, csv]
confidence: high
---

# 윈도우 AMCACHE에 기록된 프로그램 최초 설치 소스 디렉터리 경로 추적 (Amcache.hve Source Path)

> **난이도**: 초급  
> **소요 시간**: 15~20분  
> **참고 picoCTF 문제**: 악성 실행 유입 경로 특정 (Windows Amcache Install Source 분석)

## 1. 배경 시나리오
사내 도메인 제어 시스템에서 악성 백도어 파일인 `malware_loader.exe`가 동작하다가 실시간 위협 차단 솔루션에 탐지되었습니다. 위협 행위자는 추적을 차단하기 위해 원본 실행 파일 및 관련 스크립트 파일을 디스크에서 강제 소거했습니다. 하지만 윈도우 호환성 텔레메트리 캐시 데이터베이스인 **Amcache.hve** 레지스트리 내부의 `Root\InventoryApplication` 서브 키 영역은 응용 프로그램이 최초 인스톨 혹은 유입될 때 가졌던 컴파일 스펙과 함께 **최초 설치/배포 디렉터리 소스 경로(Install Source Directory / InstallSource)** 메타데이터를 영구 보존합니다. 수집한 Amcache 앱 인덱스 상세 파싱 리포트인 `amcache_install_details.csv`를 검색하여, **해당 악성 프로그램이 최초 기동/설치될 당시 참조했던 원래의 소스 디렉터리 경로명 속의 플래그**를 획득하십시오.

## 2. 제공 파일
* `amcache_install_details.csv` (Amcache.hve 데이터베이스 내의 InventoryApplication 제품 설치 세부 내역을 파싱하여 정제한 CSV 리포트 파일)

## 3. 문제 목표
윈도우 Amcache.hve 아티팩트의 `InventoryApplication` 서브 키 레코드 속성 정보(프로그램 이름, 설치 날짜, 배포 경로, 설치 소스 파일시스템 경로 정보)의 존재 가치와 텔레메트리 수집 원리를 이해하고, 이로부터 공격 프로그램의 최초 배포처 흔적을 식별해 냅니다.

## 4. 의도한 풀이 흐름
1. **CSV 리포트 내 프로그램 매핑**:
   * 제공된 `amcache_install_details.csv` 리포트 파일을 스프레드시트 또는 텍스트 편집기(또는 Python, awk 활용)를 통해 엽니다.
   * 프로그램 이름 컬럼 목록에서 침투 탐지 대상 바이너리인 `malware_loader` 항목이 기재된 행을 대조 검색합니다.
2. **설치 소스 경로 (Install Source Directory) 감사**:
   * Amcache는 윈도우 응용 프로그램 호환 평가 시, 프로그램의 패키지가 기동 및 마운트되었던 디렉터리 위치를 **InstallSource** 또는 **Install Source Directory** 정보 필드에 기록합니다.
   * `malware_loader` 행의 세부 속성 데이터 컬럼들을 대조합니다:
     * **프로그램 이름 (Program Name)**: `malware_loader`
     * **설치 날짜 (Installed Date)**: `2026-06-28 10:30:15`
     * **배포사 (Publisher)**: `APT attacker group`
     * **설치 소스 경로 (Install Source Directory)**: `C:\Users\Public\Downloads\picoCTF{amcache_inst4ll_s0urc3_tr4c3d}`
3. **플래그 도출**:
   * 해당 소스 경로 필드의 맨 마지막 디렉터리 문자열 속에 매핑 탑재되어 있는 플래그 값을 획득합니다:
     `picoCTF{amcache_inst4ll_s0urc3_tr4c3d}`

## 5. 정답(플래그) 규칙 및 예시
* **플래그 형식**: `picoCTF{<flag_string>}`
* **예시**: `picoCTF{amcache_inst4ll_s0urc3_tr4c3d}`

## 6. 출제자 노트 & 파일 제작 가이드
* **아티팩트 제작 방법**:
  1. 테스트 Windows PC 환경의 공용 다운로드 임시 폴더 경로인 `C:\Users\Public\Downloads\picoCTF{amcache_inst4ll_s0urc3_tr4c3d}` 폴더를 생성합니다.
  2. 해당 폴더 내부에서 컴파일된 자작 백도어 `malware_loader.exe`를 배치하여 1회 설치 실행합니다. (이때 호환성 원격 모니터링 엔진이 해당 실행 파일의 상위 폴더 경로를 `InstallSource` 속성 값으로 취득하여 Amcache 하이브 레지스트리에 영구 박제합니다)
  3. `C:\Windows\AppCompat\Programs\Amcache.hve` 파일을 복제 적출합니다.
  4. `AmcacheParser` 도구를 가동해 `InventoryApplication` 아웃풋 CSV 보고서를 생성합니다.
  5. 생성된 보고서 내에서 `malware_loader`에 연계되어 보존된 `InstallSource` 절대 경로 행을 격리하고 CSV 파일로 조립 구성하여 `amcache_install_details.csv` 최종 배포 파일로 저장합니다.
* **출제 포인트**: 
  * 파일이 안전 소거(Wiped)되어 흔적을 잃었을 경우에도, OS 백그라운드 제품 인벤토리 데이터베이스(Amcache Install Catalog Forensics)를 역추적 파싱하여 피의자가 외부 공유 드라이브나 숨김 공용 다운로드 경로를 활용해 은밀히 도구를 이식 실행한 유입 흔적을 물리 규명하는 사고 대응 기법을 강화시킵니다.

## 7. 트러블슈팅 및 힌트
* **Q. Amcache.hve 파일이 현재 Windows 사용 중이라며 복사되지 않습니다.**
  * A. Amcache.hve 레지스트리 하이브는 Windows OS가 활성 구동 중일 때 항상 잠금 상태(In Use Lock)로 커널에 의해 점유됩니다. 따라서 런타임 환경에서 직접 복사하려면 관리자 권한 프롬프트 하에 볼륨 섀도 복사본 서비스(VSS)를 이용하거나, `FTK Imager` 등의 물리 로우 레벨 파일시스템 오프셋 바이패스 복사 모듈을 수행해 적출해야 파일 잠금을 우회해 안전하게 복제할 수 있습니다.
* **Q. InstallSource 경로 정보가 기입되지 않고 비어(NULL) 있는 응용 프로그램은 왜 그런가요?**
  * A. 윈도우의 공식 설치 패키지(MSI, Advanced Installer 등) 형태가 아닌, 컴파일된 실행 파일 하나만 독립적으로 단독 가동(Standalone Portable Executable)시킨 경우에는 최초 실행에 특화된 호환 감사 트리만 생성되고 설치 소스 경로 속성 정보는 공란으로 보존될 수 있습니다. 이럴 때는 상위 컴포넌트 정보 대신 하위 개별 실행 바이너리 정보 테이블인 `InventoryApplicationFile` 영역을 조회하여 해당 파일이 위치했던 원본 구동 물리 디렉터리 경로명을 역색인해 내야 합니다.

## 8. 학습 포인트
* **윈도우 Amcache 텔레메트리 스키마**: 호환성 설치 및 패키지 인벤토리 관리 키(`InventoryApplication`)의 데이터 세그먼트 저장 사양을 배웁니다.
* **유입 소스 경로 역추적**: 프로그램 원본 바이너리가 실시간 소거된 침해 현장에서, Amcache 잔재 텔레메트리 경로 메타데이터를 역파싱하여 공격 도구가 유입되었던 최초의 물리 침투 통로를 판독 및 규명하는 역량을 다집니다.
