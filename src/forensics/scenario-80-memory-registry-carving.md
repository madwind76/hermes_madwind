---
title: Volatility 3를 이용한 메모리 적재 레지스트리 하이브 수동 파싱 (Memory Registry Hive Carving)
created: 2026-06-28
updated: 2026-06-28
type: ctf-challenge
tags: [ctf, ctf-challenge, forensics, memory, volatility, registry, hivelist, hivescan, carving]
confidence: high
---

# Volatility 3를 이용한 메모리 적재 레지스트리 하이브 수동 파싱 (Memory Registry Hive Carving)

> **난이도**: 초중급  
> **소요 시간**: 25~30분  
> **참고 picoCTF 문제**: 메모리 내 레지스트리 적재 정보 분석 및 카빙 (Volatility Hivelist 활용)

## 1. 배경 시나리오
공격자가 디스크 흔적 소거용 랜섬웨어 악성코드를 기동하여 C 드라이브 전체의 시스템 구성 파일 및 레지스트리 하이브 파일들(`.dat`, `.hve` 등)을 암호화/파괴했습니다. 그러나 운 좋게도 파괴 직전 시점의 서버 RAM 메모리 덤프가 수집 보존되어 있습니다. 윈도우 OS는 동작 중에 레지스트리 정보를 RAM의 커널 가상 주소 공간에 통째로 적재하여 참조하므로, 디스크 파일이 소멸되었더라도 메모리 덤프에서 물리 메모리 오프셋을 역추적해 하이브 데이터를 추출 카빙할 수 있습니다. 수집된 메모리 분석 결과 리포트인 `volatility_registry_hivelist.txt` 파일을 분석하여, **피의자 계정인 `suspect` 사용자의 사용자 레지스트리 하이브(`NTUSER.DAT`)가 적재되어 있던 물리 메모리 시작 주소(Physical Offset, 플래그)**를 도출하십시오.

## 2. 제공 파일
* `volatility_registry_hivelist.txt` (Volatility 3의 `windows.registry.hivelist` 플러그인을 가동해 RAM 내에 상주 로딩된 활성 레지스트리 목록을 덤프한 텍스트 파일)

## 3. 문제 목표
윈도우가 가동 중에 디스크의 레지스트리 하이브를 메모리 페이지 풀(Pool)에 어떻게 매핑 및 적재하는지 원리를 파악하고, Volatility `hivelist` 출력 결과 테이블의 필드(Virtual Address, Physical Address, Hive Name) 매핑 구성을 디코드해 덤프 대상 물리 메모리 오프셋을 획득합니다.

## 4. 의도한 풀이 흐름
1. **레지스트리 하이브 리스트 테이블 관찰**:
   * 제공된 `volatility_registry_hivelist.txt` 텍스트 파일을 엽니다.
   * `hivelist` 결과의 컬럼 배치를 파악합니다:
     `Virtual Address | Physical Address | Name`
2. **타깃 레지스트리 식별 (suspect 계정의 NTUSER.DAT 검색)**:
   * 피의자가 사용했던 프로필 설정 흔적을 구출하기 위해 `Name` 필드에서 사용자 `suspect` 계정의 개인 레지스트리 파일명인 `NTUSER.DAT` 경로가 기입된 엔트리를 찾습니다:
     `\Users\suspect\NTUSER.DAT`
   * 해당 행을 대조 검색합니다:
     ```text
     0xf800045d6000  0x3f1a2000  \Users\suspect\NTUSER.DAT
     ```
3. **물리 메모리 오프셋 (Physical Address) 추출**:
   * 검색된 레코드 행에서 `Physical Address` (두 번째 열)의 값인 16진수 메모리 물리 주소 오프셋을 추출합니다:
     `0x3f1a2000`
     *(참고: Virtual Address인 0xf800045d6000은 커널 가상 메모리 매핑 공간을 뜻하므로, 덤프 카빙 시에 직접 사용할 물리 RAM 오프셋은 Physical Address 값을 적용해야 합니다)*
4. **플래그 조립**:
   * 계정명 및 구한 물리 주소를 포맷에 맞춰 최종 플래그로 정립합니다:
     `picoCTF{suspect_ntuser_physical_0x3f1a2000}`

## 5. 정답(플래그) 규칙 및 예시
* **플래그 형식**: `picoCTF{<user_name>_ntuser_physical_<hex_offset>}`
* **예시**: `picoCTF{suspect_ntuser_physical_0x3f1a2000}` (오프셋의 16진수 알파벳은 소문자로 표기합니다)

## 6. 출제자 노트 & 파일 제작 가이드
* **아티팩트 제작 방법**:
  1. Windows VM 테스트 환경에서 `suspect` 라는 명칭의 사용자 로컬 계정을 신규 추가하고 로그인을 수행해 `NTUSER.DAT` 레지스트리를 빌드합니다.
  2. 시스템 메모리 덤프를 가동하여 Raw 덤프 이미지 `memory.raw`를 생성합니다.
  3. Volatility 3 프레임워크를 가동해 메모리 적재 레지스트리 주소 목록을 출력합니다:
     `python3 vol.py -f memory.raw windows.registry.hivelist > volatility_registry_hivelist.txt`
  4. 출력 결과 파일 내에 `\Users\suspect\NTUSER.DAT` 대응 물리 주소가 `0x3f1a2000` 대역 부근에 정상적으로 바인딩 인쇄되는지 검수하여 배포 텍스트 파일로 사용합니다.
* **출제 포인트**: 
  * 디스크 기반 증적이 소거된 복합적인 침해 사고 환경에 직면하여, RAM 메모리 분석 도구를 가동해 메모리에 임시 페이지 뷰로 적재되어 활성 서비스 중이던 레지스트리 하이브의 물리 위치(Memory Registry Hive Forensics)를 성공적으로 특정하고 카빙 오프셋을 도출해 내는 대응 역량을 기릅니다.

## 7. 트러블슈팅 및 힌트
* **Q. Volatility 3에서 특정 레지스트리 하이브의 키 값을 직접 덤프하여 파싱하는 명령어는 무엇인가요?**
  * A. `windows.registry.printkey` 플러그인을 가동하면 메모리 내의 레지스트리 값을 디바이스에서 직접 열람할 수 있습니다:
     `python3 vol.py -f memory.raw windows.registry.printkey --offset 0x3f1a2000 --key "Software\Microsoft\Windows\CurrentVersion\Run"`
     위와 같이 `--offset` 옵션에 구한 물리/가상 주소를 매핑하고 대상 서브 키 경로를 전달하면, 오프라인 레지스트리 파서 없이도 메모리 상에 기표된 자동 실행 악성 백도어 레코드의 상세 인자 값을 커맨드라인에서 다이렉트로 복원해 볼 수 있어 효율적입니다.
* **Q. 메모리에서 추출한 레지스트리 파일의 무결성은 어떻게 입증하나요?**
  * A. RAM에서 레지스트리를 덤프하여 저장하면, 윈도우 커널이 메모리 관리를 위해 덧붙인 페이지 풀 헤더 및 매핑 슬랙이 끼어 들어갈 수 있습니다. 덤프된 바이너리의 첫 4바이트가 레지스트리 하이브 표준 시그니처인 **`regf`** (`72 65 67 66`) 매직 바이트로 정상 개시하는지 검사함으로써 덤프가 정상적으로 성립했음을 정적으로 검증할 수 있습니다.

## 8. 학습 포인트
* **윈도우 메모리 레지스트리 매핑 아키텍처**: 레지스트리 하이브 파일이 RAM의 페이지 풀 커널 메모리에 적재 및 매핑되어 서비스되는 라이프사이클을 파악합니다.
* **메모리 아티팩트 카빙**: Volatility 하이브 매핑 리포트를 기반으로, 손상된 시스템 구성을 가상/물리 주소 오프셋 구조를 통해 역추적해 구출해 내는 메모리 분석 기법을 구축합니다.
