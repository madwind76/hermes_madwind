---
title: 윈도우 AMCACHE에 잔재하는 지워진 프로그램 컴파일 링커 해시 특정 (Amcache.hve Program Linker Hash)
created: 2026-06-28
updated: 2026-06-28
type: ctf-challenge
tags: [ctf, ctf-challenge, forensics, windows, registry, amcache, linker-hash, pe-checksum, csv]
confidence: high
---

# 윈도우 AMCACHE에 잔재하는 지워진 프로그램 컴파일 링커 해시 특정 (Amcache.hve Program Linker Hash)

> **난이도**: 초급  
> **소요 시간**: 15~20분  
> **참고 picoCTF 문제**: 소거된 프로그램 PE 해더 속성 식별 (Windows Amcache Linker Hash 분석)

## 1. 배경 시나리오
공격자가 중요 호스트 컴퓨터에 침투해 독자 설계한 맞춤형 공격 바이너리인 `custom_backdoor_v5.exe`를 구동한 후 흔적을 인멸하기 위해 디스크에서 영구 삭제하고 임시 디렉터리까지 세차게 포맷했습니다. 이 바이너리의 SHA-1 파일 해시나 기본 파일 메타데이터도 확인이 불가한 상황입니다. 하지만 윈도우 OS의 애플리케이션 호환성 레지스트리인 **Amcache.hve** 파일 내의 `Root\InventoryApplicationFile` 영역은 시스템에서 기동되었던 개별 PE 실행 파일의 다양한 내부 메타데이터 필드들(컴파일 링크 시각, PE 체크섬 해시 정보 등)을 영구 보존합니다. 수집한 Amcache 개별 파일 실행 이력 테이블 보고서인 `amcache_pe_files.csv`를 검색하여, **지워진 공격 프로그램(`custom_backdoor_v5.exe`)에 대해 Amcache가 보존해 둔 PE 고유 컴파일러 링커 해시 값(플래그)**을 역추적해 찾아내십시오.

## 2. 제공 파일
* `amcache_pe_files.csv` (Amcache.hve 레지스트리 내부의 InventoryApplicationFile 정보를 파싱하여 생성한 CSV 데이터 테이블 리포트)

## 3. 문제 목표
윈도우 Amcache.hve 파일의 `InventoryApplicationFile` 서브 키에 기록되는 개별 이진 PE 헤더 속성 정보(파일명, 파일 크기, SHA-1, 컴파일러 링커 해시/Linker Hash 및 PE 체크섬)의 존재 가치와 기록 구조를 이해하고, 이를 역추적합니다.

## 4. 의도한 풀이 흐름
1. **CSV 리포트 내 대상 탐색**:
   * 제공된 `amcache_pe_files.csv` 파일을 엽니다.
   * 파일 이름 컬럼 목록에서 훼손 삭제 대상 프로그램인 `custom_backdoor_v5.exe`가 기입된 행을 찾습니다.
2. **링커 해시 (Linker Hash) 속성 추출**:
   * Amcache 레지스트리는 프로그램의 최초 로딩 시, 운영체제가 해당 PE 파일의 헤더를 해석하여 컴파일에 기여한 고유 빌드 식별자인 **Linker Hash (또는 PE Checksum)** 정보를 추출 수집해 저장합니다.
   * `custom_backdoor_v5.exe` 행의 속성 데이터 컬럼들을 확인 대조합니다:
     * **파일명 (File Name)**: `custom_backdoor_v5.exe`
     * **파일 크기 (Size)**: `124416` (Bytes)
     * **SHA-1 해시**: `7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b`
     * **링커 해시 (Linker Hash)**: `picoCTF{0a9b8c7d6e5f4a3b2c1d0e9f8a7b6c5d}`
3. **플래그 도출**:
   * 해당 링커 해시 컬럼에 기록된 값으로부터 최종 플래그를 정립합니다:
     `picoCTF{0a9b8c7d6e5f4a3b2c1d0e9f8a7b6c5d}`

## 5. 정답(플래그) 규칙 및 예시
* **플래그 형식**: `picoCTF{<Linker_Hash_value>}`
* **예시**: `picoCTF{0a9b8c7d6e5f4a3b2c1d0e9f8a7b6c5d}` (해시 데이터 알파벳은 소문자로 표기합니다)

## 6. 출제자 노트 & 파일 제작 가이드
* **아티팩트 제작 방법**:
  1. 테스트 Windows PC 환경에서 컴파일된 자작 프로그램 `custom_backdoor_v5.exe`를 준비합니다. 이때 PE 헤더 컴파일 빌드 옵션 상의 링커 체크섬/해시 고유값 필드 영역에 플래그 규격인 `0a9b8c7d6e5f4a3b2c1d0e9f8a7b6c5d` 값이 매핑 생성되도록 이진 구성을 수립합니다.
  2. 프로그램을 작동시키면 Windows Compatibility Telemetry Engine(호환성 평가 시스템)이 가동하여 실행 PE 파일의 링커 고유 속성을 `Amcache.hve` 레지스트리의 `InventoryApplicationFile\<SHA-1>` 서브 키 경로로 자동 적재합니다.
  3. `Amcache.hve` 파일을 ftkimager 등을 활용해 적출합니다.
  4. `AmcacheParser.exe`를 가동해 `InventoryApplicationFile` 대응 CSV 리포트를 생성합니다:
     `AmcacheParser.exe -f Amcache.hve --csv output_dir`
  5. 출력 보고서 중 `*InventoryApplicationFile.csv` 내에서 해당 악성 파일의 등록 링커 해시(LinkerHash) 행을 확인 정제한 뒤 `amcache_pe_files.csv` 파일로 빌드해 유저에게 제공합니다.
* **출제 포인트**: 
  * 실행 바이너리 자체가 완전히 마스킹되거나 카빙 복구할 수 없는 상태라 하더라도, OS 텔레메트리 보존 목적으로 백그라운드 저장소(`Amcache.hve`)에 컴파일 제품 프로필 명세와 함께 하드코딩되는 PE 링커 고유 해시 흔적(Amcache Linker Hash Forensics)을 역색인하여 공격 증적을 복원해 내는 조사 기법을 훈련시킵니다.

## 7. 트러블슈팅 및 힌트
* **Q. Linker Hash 값은 일반적인 MD5나 SHA-1 파일 해시와 어떻게 다른가요?**
  * A. MD5/SHA-1 파일 해시는 파일 본문의 단 1바이트 데이터만 바뀌어도 완전히 어긋나는 전체 무결성 검증용 해시입니다. 반면, `Linker Hash`는 PE 파일 헤더 구성 중 컴파일러 링킹 사양 및 빌드 구조 정보만을 기반으로 생성되는 특화 해시로, 프로그램 본문 리소스 데이터(이미지, 자막 텍스트, 플래그 등)가 미세하게 변경 수정되더라도 동일한 컴파일러와 링커 환경에서 기동 빌드되었다면 고유하게 동일 해시를 유지하는 특성을 지닙니다. 이를 통해 공격 도구의 패킹 변조 유형 및 패밀리 제품군 여부를 역추적하는 매우 강력한 분류 증적으로 차용됩니다.
* **Q. Amcache.hve 하이브의 수정 타임스탬프를 통해 유용하게 알 수 있는 것은 무엇인가요?**
  * A. Amcache 내의 개별 파일 SHA-1 서브 키의 **Last Write Time**은 해당 바이너리가 시스템에 최초 감지(설치 또는 최초 실행)된 시간에 정확히 정렬되므로, 공격 악성코드가 로컬 운영체제에 최초로 침투 이식된 동작 타임라인을 파악하는 결정적인 보안 타임라인 증적으로 삼을 수 있습니다.

## 8. 학습 포인트
* **윈도우 Amcache 텔레메트리 PE 감사 스키마**: 호환성 원격 모니터링 감사 엔진의 데이터 수집 스펙 및 `InventoryApplicationFile` 제품 프로파일 적재 원리를 학습합니다.
* **소프트웨어 PE 링커 해시 감사**: 소거된 미확인 PE 파일에 대해 Amcache에 잔재하는 헤더 메타데이터 레코드를 파싱하여 컴파일 아이덴티티를 입증하는 디지털 포렌식 기법을 내재화합니다.
