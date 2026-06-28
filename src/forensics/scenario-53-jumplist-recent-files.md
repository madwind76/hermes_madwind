---
title: 윈도우 최근 사용 파일 링크 복구 (Recent Files & Jump Lists Forensics)
created: 2026-06-28
updated: 2026-06-28
type: ctf-challenge
tags: [ctf, ctf-challenge, forensics, windows, jumplist, recent-files, ole-cfb, jlecmd]
confidence: high
---

# 윈도우 최근 사용 파일 링크 복구 (Recent Files & Jump Lists Forensics)

> **난이도**: 초중급  
> **소요 시간**: 25~30분  
> **참고 picoCTF 문제**: 최근 열람 파일 이력 복원 및 파싱 (Windows Jump Lists 포렌식)

## 1. 배경 시나리오
사내 중요 설계 기밀이 담긴 이미지 파일이 유출된 정황이 있어 조사 중입니다. 피의자는 대상이 되는 이미지를 PC에서 본 적도 없고 보관한 사실도 없다며 강력하게 부인하고 있으며, 실제 C 드라이브 전체에서 관련 이미지 파일은 모두 삭제되어 검색되지 않습니다. 하지만 윈도우 OS는 사용자가 탐색기 하단 작업 표시줄 앱 아이콘을 우클릭했을 때 나타나는 최근 항목 리스트인 **점프 리스트(Jump Lists)** 아티팩트를 자동으로 생성하여 보존합니다. 피의자 프로필 경로에서 윈도우 사진 뷰어 앱 관련 점프 리스트 임시 파일인 `9b9abc513a3b2b1c.automaticDestinations-ms` 파일을 확보했습니다. 이 점프 리스트 구조를 분석하여 **피의자가 최근 실행(열람)했던 대상 기밀 파일명 속의 플래그**를 알아내십시오.

## 2. 제공 파일
* `9b9abc513a3b2b1c.automaticDestinations-ms` (OLE 복합 구조체 포맷을 띠고 있는 윈도우 자동 점프 리스트 메타 파일)

## 3. 문제 목표
윈도우 점프 리스트의 두 가지 종류(Automatic, Custom)와 구조(OLE Compound File Binary 포맷, DestList 스트림 및 개별 LNK 스트림 데이터)를 파악하고, 점프 리스트 분석 도구(JLECmd 등)를 활용해 내부 최근 열람 파일 이력의 원본 절대 경로 정보를 복원합니다.

## 4. 의도한 풀이 흐름
1. **아티팩트 물리 포맷 식별**:
   * 제공된 `*.automaticDestinations-ms` 파일의 확장자를 헥스 에디터로 검사합니다.
   * 첫 8바이트 시그니처가 `D0 CF 11 E0 A1 B1 1A E1` (Microsoft Compound File Binary, 일명 OLE CFB 매직바이트)임을 식별하여 본 파일이 OLE 저장소 포맷임을 인지합니다.
2. **점프 리스트 파싱 (JLECmd 활용)**:
   * **CLI 분석**: Eric Zimmerman의 점프 리스트 분석기인 `JLECmd.exe`를 사용하여 제공된 파일을 해독합니다:
     `JLECmd.exe -f 9b9abc513a3b2b1c.automaticDestinations-ms --csv output_dir`
   * CSV 결과 보고서 또는 콘솔 상세 출력 정보에서 **DestList** 하부의 파일 참조 엔트리들을 긁어 모읍니다.
   * 각 엔트리는 내부적으로 단축키 LNK 명세와 연동되어 파일 크기, 경로, 실행 시간 정보를 갖고 있습니다.
3. **타깃 실행 경로 추적**:
   * 분석 결과 추출된 경로 목록 중 사용자 데스크톱(Desktop) 경로 아래에 위치했던 특정 비정상 파일명을 탐지합니다:
     `C:\Users\admin\Desktop\picoCTF{jumpl1st_h0lds_rec3nt_act1v1ty}.png`
4. **플래그 도출**:
   * 파일명 자체에서 플래그 문자열을 추출합니다:
     `picoCTF{jumpl1st_h0lds_rec3nt_act1v1ty}`

## 5. 정답(플래그) 규칙 및 예시
* **플래그 형식**: `picoCTF{<flag_string>}`
* **예시**: `picoCTF{jumpl1st_h0lds_rec3nt_act1v1ty}`

## 6. 출제자 노트 & 파일 제작 가이드
* **아티팩트 제작 방법**:
  1. Windows 10/11 가상 머신 바탕화면에 기밀 이미지 `picoCTF{jumpl1st_h0lds_rec3nt_act1v1ty}.png` 파일을 배치합니다.
  2. 윈도우 기본 사진 뷰어 또는 페인트(mspaint.exe) 프로그램을 사용해 이 이미지를 더블 클릭하여 엽니다. (이 시점에 점프 리스트 이력에 강제 업데이트가 일어납니다)
  3. 최근 목록 디렉터리 경로로 이동합니다:
     `%USERPROFILE%\AppData\Roaming\Microsoft\Windows\Recent\AutomaticDestinations\`
  4. 당일 수정 타임스탬프를 지닌 `*.automaticDestinations-ms` 파일 중 페인트 또는 사진 뷰어 앱 고유 AppID(예: mspaint의 경우 `9b9abc513a3b2b1c` 부근) 해시 이름을 가진 파일을 검색해 격리합니다.
  5. 획득한 파일을 배포 파일로 지정합니다.
* **출제 포인트**: 
  * 사용자가 악성 데이터 실행 후 대상 파일을 Shift+Del로 영구 소거하고 안티 포렌식 툴로 덮어써도, 윈도우 OS가 보조 편의를 위해 레코드(Jump List)로 인덱싱하여 남겨두는 런타임 흔적(User Activity Tracking)의 실효성을 증명시킵니다.

## 7. 트러블슈팅 및 힌트
* **Q. 점프 리스트 파일명인 9b9abc513a3b2b1c 같은 이름은 무작위 난수인가요?**
  * A. 아닙니다. 이 파일명은 실행 파일의 절대 경로를 기반으로 계산되는 고유한 **애플리케이션 ID(AppID)** 값의 CRC-64 해시 결과물입니다. 따라서 윈도우 버전이 동일하고 애플리케이션의 설치 경로가 일치하면 모든 PC에서 동일한 파일명 해시를 공유하므로 타깃 분석 대상을 빠르게 지정할 수 있습니다 (예: 윈도우 메모장은 `b91730d84b7202b5.automaticDestinations-ms`를 생성합니다).
* **Q. JLECmd 도구 없이 파이썬에서 파싱하고 싶습니다.**
  * A. OLE 복합 파일 형식을 다루는 `olefile` 파이썬 패키지를 사용하여 내부 스트림 목록을 로드할 수 있습니다. 셸링크 LNK 스트림 목록을 수동 루프 돌아 `DestList` 스트림 하부의 문자열을 카빙하는 방식으로 복잡한 윈도우 가상머신 없이도 리눅스 터미널에서 해독 스크립트를 작성할 수 있습니다.

## 8. 학습 포인트
* **윈도우 점프 리스트(Jump Lists) 구조**: 사용자의 편의 도구(최근 항목) 지원을 위해 OS가 생성하는 OLE CFB 아카이빙 메커니즘을 상세히 이해합니다.
* **사용자 행위 이력 복구**: 파일 본문이 소멸된 극단적인 침해 현장에서 OS 보조 아티팩트(Jump Lists, Link File)의 메타데이터를 역공학으로 해독해 당시 실존했던 파일 증적을 입증하는 분석 논리를 학습합니다.
