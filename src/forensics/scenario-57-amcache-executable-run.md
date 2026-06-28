---
title: 윈도우 AMCACHE 애플리케이션 실행 분석 (Amcache.hve Forensics)
created: 2026-06-28
updated: 2026-06-28
type: ctf-challenge
tags: [ctf, ctf-challenge, forensics, windows, registry, amcache, amcacheparser, execution-history]
confidence: high
---

# 윈도우 AMCACHE 애플리케이션 실행 분석 (Amcache.hve Forensics)

> **난이도**: 초급  
> **소요 시간**: 15~20분  
> **참고 picoCTF 문제**: 프로그램 실행 잔재 흔적 추적 (Windows Amcache.hve 포렌식)

## 1. 배경 시나리오
사내 자산 유출 사고 의심자가 외장 저장매체에서 직접 악성 실행 파일을 가져와 구동한 정황이 발견되었습니다. 용의자는 실행 후 해당 프로그램 바이너리를 디스크 상에서 완전히 삭제(Wipe)하고 프리페치(Prefetch) 파일들까지 일괄 삭제하여 실행 흔적을 감추었습니다. 하지만 윈도우 운영체제는 응용 프로그램 호환성 및 안정성 평가를 위해 가동 이력을 기록하는 독자적인 레지스트리 하이브 파일인 **Amcache.hve**(`C:\Windows\appcompat\Programs\Amcache.hve`)를 별도로 유지합니다. 프리페치 삭제를 무력화하는 이 Amcache 하이브 파일을 분석하여, **가동되었던 악성 프로그램의 원본 절대 경로에 숨겨져 있는 플래그**를 획득하십시오.

## 2. 제공 파일
* `Amcache.hve` (윈도우 AppCompat 서브시스템이 보존하는 실행 프로그램 메타데이터 하이브 파일)

## 3. 문제 목표
윈도우 Amcache.hve 아티팩트의 생성 목적 및 저장 구조(하이브 내 `Root\InventoryApplicationFile` 및 `Root\File` 키)를 이해하고, 전문 Amcache 파서 도구(AmcacheParser 등)를 활용하여 삭제된 실행 파일의 원본 절대 경로를 복구합니다.

## 4. 의도한 풀이 흐름
1. **아티팩트 특성 진단**:
   * 제공된 `Amcache.hve` 파일은 윈도우 레지스트리 하이브 구조를 띠고 있어, 일반 텍스트 편집기로는 열리지 않음을 확인합니다.
2. **Amcache 하이브 파싱**:
   * **CLI 도구 가동 (AmcacheParser)**: Eric Zimmerman의 `AmcacheParser.exe`를 사용하여 분석 보고서를 CSV 형식으로 출력합니다.
     `AmcacheParser.exe -f Amcache.hve --csv output_dir`
   * **GUI 도구 가동**: `Registry Explorer`를 실행하여 `Amcache.hve` 파일을 로드하고 `Root\InventoryApplicationFile` 키로 이동하여 레코드를 분석합니다.
3. **비정상 원본 파일 경로 식별**:
   * 파싱 완료된 CSV 목록(특히 `*_UnassociatedFiles.csv` 또는 `File` 테이블)에서 파일 시스템 정상 경로(System32 등)가 아닌 임시 폴더나 외부 볼륨 대역에서 가동되었던 실행 프로그램 항목을 정렬 및 스캔합니다.
   * 조회 결과, 다음의 비정상적인 프로그램 실행 경로 엔트리를 검출합니다:
     * **파일명**: `picoCTF{amc4ch3_hve_r3veals_sha1_hash}.exe`
     * **원본 절대 경로**: `C:\Users\Public\picoCTF{amc4ch3_hve_r3veals_sha1_hash}.exe`
     * **파일 SHA-1 해시**: `8f9b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b`
4. **플래그 도출**:
   * 파일명 혹은 절대 경로 상에 정의되어 있던 플래그 문자열을 추출합니다:
     `picoCTF{amc4ch3_hve_r3veals_sha1_hash}`

## 5. 정답(플래그) 규칙 및 예시
* **플래그 형식**: `picoCTF{<flag_string>}`
* **예시**: `picoCTF{amc4ch3_hve_r3veals_sha1_hash}`

## 6. 출제자 노트 & 파일 제작 가이드
* **아티팩트 제작 방법**:
  1. Windows 10/11 가상 머신의 공용 사용자 디렉터리(`C:\Users\Public\`) 하위에 플래그 명칭의 실행 파일을 배치합니다:
     `C:\Users\Public\picoCTF{amc4ch3_hve_r3veals_sha1_hash}.exe`
  2. 해당 파일을 더블 클릭하여 실행합니다. (이때 Amcache 백그라운드 스레드가 구동 바이너리의 SHA-1 파일 해시, 파일 크기, 경로 정보를 획득하여 하이브에 라이트합니다)
  3. `C:\Windows\appcompat\Programs\Amcache.hve` 파일(잠겨 있으므로 FTK Imager 등으로 안전 덤프)을 획득합니다.
  4. 획득한 Amcache 하이브 파일을 배포 아티팩트로 포장해 사용합니다.
* **출제 포인트**: 
  * 윈도우 침해 사고 침투 흔적 조사 시, 흔히 오염되는 프리페치(Prefetch)나 심백(Shimcache) 영역 외에 공격자가 완전히 지우기 까다롭고 영구적인 SHA-1 파일 해시 정보까지 연동해 보존하는 Amcache 포렌식 역량을 강화합니다.

## 7. 트러블슈팅 및 힌트
* **Q. Amcache.hve와 Shimcache(AppNameCache)의 차이는 무엇인가요?**
  * A. Shimcache는 시스템의 레지스트리 `SYSTEM` 하이브에 기록되며 주로 실행 파일의 절대 경로와 최종 수정 시간만 보존하고 파일의 해시값은 담지 않습니다. 반면 Amcache는 독립된 별도 하이브 파일(`Amcache.hve`)로 관리되며 실행 당시의 파일 **SHA-1 해시 값**과 제품명, 제작사 메타데이터까지 함께 기록되므로 공격 악성코드의 오리지널 해시 일치 여부를 파싱 대조할 수 있어 포렌식 증거력이 훨씬 강력합니다.
* **Q. AmcacheParser 실행 중 파일이 잠겨 열 수 없다는 에러가 발생합니다.**
  * A. 활성 윈도우 OS 시스템에서 실시간으로 Amcache.hve를 읽으려 하면 파일 락 에러가 납니다. Fk Imager를 활용해 볼륨 섀도 복사본이나 Raw 덤프로 추출해야 분석 세션을 확보할 수 있습니다. 챌린지로 제공되는 `Amcache.hve` 복제본은 직접 읽기가 가능합니다.

## 8. 학습 포인트
* **윈도우 Amcache 메커니즘**: 응용 프로그램 호환성 평가 서브시스템의 메타데이터 로깅 원리 및 파일 수집 스키마를 이해합니다.
* **프로그램 실행 이력 복구**: 안티 포렌식 행위(바이너리 삭제, 프리페치 소거)를 극복하기 위해 하이브 레지스트리 분석 도구를 가동해 원본 실행 파일의 경로와 SHA-1 실측 해시를 복원하는 기술을 마스터합니다.
