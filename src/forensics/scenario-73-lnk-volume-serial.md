---
title: 윈도우 최근 폴더 단축 아이콘 링크 분석 (Shell Link LNK Files Forensics)
created: 2026-06-28
updated: 2026-06-28
type: ctf-challenge
tags: [ctf, ctf-challenge, forensics, windows, lnk-file, shell-link, volume-serial, lecmd, metadata]
confidence: high
---

# 윈도우 최근 폴더 단축 아이콘 링크 분석 (Shell Link LNK Files Forensics)

> **난이도**: 초급  
> **소요 시간**: 15~20분  
> **참고 picoCTF 문제**: 외장 매체 연결 흔적 규명 (Windows LNK Shell Link 포렌식)

## 1. 배경 시나리오
보안 유출 용의자 PC의 최근 사용 문서 폴더(`%APPDATA%\Microsoft\Windows\Recent\`)에서 특정 외부 저장매체(USB 드라이브)를 참조하고 있던 단축 링크 파일인 `secret_document.lnk` 아티팩트를 수집했습니다. 용의자는 해당 파일이 원래 하드디스크 C 드라이브에 저장되어 있던 것을 열었을 뿐 외부 저장장치를 연결해 복제해 간 적이 없다고 부인하고 있습니다. 하지만 윈도우의 바로가기(`.lnk`) 링크 파일은 대상 원본 파일의 경로 외에도, 저장되어 있던 물리 볼륨의 시리얼 번호(Volume Serial Number) 및 드라이브 유형 정보를 헤더에 고스란히 담아 보존합니다. 수집한 LNK 파일의 메타데이터를 파싱하여, **해당 문서가 담겨 있던 외장 볼륨의 시리얼 번호(플래그)**를 획득하십시오.

## 2. 제공 파일
* `secret_document.lnk` (사용자의 최근 사용 문서 목록에서 수집한 윈도우 셸 링크 바로가기 파일)

## 3. 문제 목표
윈도우 바로가기 링크 파일(Shell Link Binary File) 내부의 핵심 구조(특히 **LinkInfo** 데이터 구조체 내의 **VolumeID** 블록 필드)를 이해하고, 전문 LNK 파싱 도구(LECmd 등)를 이용하여 볼륨 시리얼 번호, 드라이브 타입, 대상 맥 주소(MAC Address) 등의 하드웨어 고유 증적을 추출해 매핑합니다.

## 4. 의도한 풀이 흐름
1. **LNK 메타데이터 파싱**:
   * 제공된 바로가기 파일 `secret_document.lnk`를 분석 전용 도구인 Eric Zimmerman의 `LECmd.exe`를 구동해 파싱합니다.
     `LECmd.exe -f secret_document.lnk`
   * 혹은 리눅스 CLI 환경의 오픈소스 LNK 파서 유틸리티(`lnk-parse` 등) 또는 파이썬 `pylnk3` 패키지를 가동합니다.
2. **볼륨 메타데이터 및 시리얼 식별**:
   * 도구의 파싱 결과 출력 데이터에서 **VolumeID** 정보 영역을 대조합니다:
     * **드라이브 유형 (Drive Type)**: `Removable Disk (이동식 디스크, USB)`
     * **볼륨 이름 (Volume Label)**: `SECURE_USB`
     * **볼륨 시리얼 번호 (Volume Serial Number)**: `A4B3-C2D1`
     * **대상 로컬 절대 경로 (Local Path)**: `F:\Secret\flag.txt`
3. **최종 플래그 조립**:
   * 획득한 볼륨 시리얼 번호 `A4B3-C2D1`을 문제 요구 규격 포맷에 대입하여 최종 플래그를 정립합니다:
     `picoCTF{A4B3-C2D1_volume_serial_linked}`

## 5. 정답(플래그) 규칙 및 예시
* **플래그 형식**: `picoCTF{<volume_serial>_volume_serial_linked}`
* **예시**: `picoCTF{A4B3-C2D1_volume_serial_linked}`

## 6. 출제자 노트 & 파일 제작 가이드
* **아티팩트 제작 방법**:
  1. 포맷된 이동식 USB 디스크를 준비합니다. 이때 해당 USB 볼륨의 시리얼 번호가 `A4B3-C2D1`로 할당되도록 볼륨 시리얼 수정 도구(Volume Serial Changer 등)를 활용하거나 수동 제어합니다.
  2. 해당 USB 드라이브를 Windows 10/11 가상머신에 마운트(예: F 드라이브) 시킵니다.
  3. F 드라이브 하위에 `Secret` 폴더를 생성하고 텍스트 파일 `flag.txt`를 위치시킵니다.
  4. 윈도우 탐색기에서 해당 `flag.txt` 파일을 더블 클릭하여 켭니다. (이 시점에 윈도우 셸이 사용자 최근 사용 아티팩트 보존 디렉터리에 해당 바로가기 파일 `secret_document.lnk`를 즉시 생성 및 적재합니다)
  5. 사용자 경로 `%USERPROFILE%\AppData\Roaming\Microsoft\Windows\Recent\secret_document.lnk` 파일을 덤프 획득하여 배포용 챌린지 파일로 포장합니다.
* **출제 포인트**: 
  * 사용자가 파일 참조 후 USB를 뽑아 증거인멸을 꾀하더라도, 로컬 PC에 적재되는 LNK 아티팩트의 링크 인포 메타데이터(LNK File Volume Metadata Forensics) 분석을 통해 소유하고 있던 USB 장치 볼륨의 물리 아이덴티티 시리얼(Volume Serial Number)과 연동 맥 주소를 추출해 용의 장치를 꼼짝없이 특정하는 디지털 감사 기법을 훈련시킵니다.

## 7. 트러블슈팅 및 힌트
* **Q. LNK 파일 내부에 기록되는 MAC 주소는 누구의 MAC 주소인가요?**
  * A. 바로가기 파일이 최초로 작성될 때, 해당 LNK 파일이 참조하는 대상 파일이 존재하는 호스트의 **네트워크 카드(NIC) 맥 주소**가 `TrackerDataBlock` 구조체 내에 직렬화되어 박제됩니다. 이를 통해 용의자가 기밀 파일을 원격 공유 네트워크 드라이브(NAS 등)에서 복사해 온 것인지, 혹은 본인 로컬 시스템에서 단독 제작한 것인지 여부를 물리 카드의 MAC 주소를 대조하여 규명해 낼 수 있어 위협 역추적 시 매우 요긴합니다.
* **Q. 볼륨 시리얼 번호가 A4B3-C2D1 인지 어떻게 검증하나요?**
  * A. 윈도우 명령창(cmd)에서 `vol F:` 명령을 수행하면 `볼륨 일련 번호는 A4B3-C2D1입니다` 형태로 16진수 문자열 출력이 일치함을 수동 확인할 수 있습니다.

## 8. 학습 포인트
* **윈도우 바로가기 LNK 이진 명세**: 셸 링크 바이너리 포맷(LinkFlags, LinkInfo, HeaderSize, TargetIDList) 및 볼륨 정보를 담는 데이터 슬롯 배열을 이해합니다.
* **외장 매체 소유권 입증 포렌식**: LNK 파일에 고착되어 영구 보존되는 볼륨 일련번호 메타데이터를 역파싱하여, 특정 물리 저장매체가 시스템에 연동 및 활동했던 이력을 논리적으로 증명하는 능력을 기릅니다.
