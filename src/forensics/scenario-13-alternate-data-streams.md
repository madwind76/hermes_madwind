---
title: 보이지 않는 데이터 스트림 (Alternate Data Streams)
created: 2026-06-28
updated: 2026-06-28
type: ctf-challenge
tags: [ctf, ctf-challenge, forensics, ntfs, ads, file-system, getfattr]
confidence: high
---

# 보이지 않는 데이터 스트림 (Alternate Data Streams)

> **난이도**: 초급  
> **소요 시간**: 15~20분  
> **참고 picoCTF 문제**: Windows NTFS 환경 고유 기법 (Alternate Data Streams 분석)

## 1. 배경 시나리오
의심 계정이 중요 소스 코드를 보관하고 있던 NTFS 파일시스템 드라이브 백업 디렉터리를 분석 중입니다. 디렉터리 내에 `notice.txt`라는 정상 안내용 텍스트 파일이 한 개 있고, 파일 크기는 겨우 25바이트에 불과합니다. 그러나 침입자가 사용한 은닉 공격 기법 분석 보고서에 따르면, 공격자가 NTFS 볼륨의 특수 기능인 **대체 데이터 스트림(Alternate Data Streams, ADS)**을 오용하여 일반 파일 목록 조회를 우회한 채 플래그 데이터를 숨겨 놓았을 것이란 징후가 감지되었습니다.

## 2. 제공 파일
* `ntfs_drive.dd` (NTFS 파일시스템 구조를 지닌 소형 볼륨 파일, 약 20MB)

## 3. 문제 목표
NTFS 파일시스템의 대체 데이터 스트림(ADS) 은닉 기법을 이해하고, 파일시스템 이미지를 마운트하거나 전문 파일시스템 분석 도구를 사용하여 `notice.txt` 파일에 추가로 결합되어 있는 보이지 않는 스트림 데이터를 추출해 플래그를 확보합니다.

## 4. 의도한 풀이 흐름
1. **분석 방법 선정**:
   * **Linux CLI 환경**: 디스크 이미지를 마운트하여 분석하거나, `ntfsprogs` 유틸리티 모음을 사용합니다.
   * **Windows 환경**: 파워셸(PowerShell) 명령어 또는 `dir /r` 명령어를 활용합니다.
2. **리눅스 환경에서의 분석 (ntfsprogs 사용)**:
   * `ntfsinfo -F /notice.txt ntfs_drive.dd` 명령을 이용해 해당 파일에 다른 데이터 속성(Data Attribute)이 붙어 있는지 확인합니다.
   * `$DATA` 속성이 디폴트 외에 추가 이름(예: `flag.txt`)으로 등록되어 있는 것을 탐지합니다.
     (예: `Attribute Name: flag.txt`)
   * `ntfscat -a flag.txt ntfs_drive.dd notice.txt` 명령어로 대체 스트림에 입력된 내용을 추출하여 플래그를 확인합니다.
3. **디스크 마운트 후 분석 (Linux getfattr 사용)**:
   * 이미지를 마운트합니다: `mount -t ntfs-3g ntfs_drive.dd /mnt`
   * `getfattr -d /mnt/notice.txt` 또는 `getfattr -h -d /mnt/notice.txt` 명령으로 대체 속성을 확인합니다.
   * `cat /mnt/notice.txt:flag.txt` 또는 `cat /mnt/notice.txt` 뒤에 숨겨진 스트림 경로를 지정하여 데이터를 읽어옵니다.
4. **윈도우 환경에서의 분석 (Cmd/PowerShell 사용)**:
   * 해당 드라이브에서 `dir /r` 명령을 치면 `notice.txt:flag.txt:$DATA` 형태의 숨겨진 스트림 파일이 즉시 가시화됩니다.
   * 파워셸의 `Get-Item -Path notice.txt -Stream *` 명령으로 스트림 목록을 식별하고, `Get-Content -Path notice.txt -Stream flag.txt` 명령으로 은닉 텍스트를 출력합니다.

## 5. 정답(플래그) 규칙 및 예시
* **플래그 형식**: `picoCTF{<flag_string>}`
* **예시**: `picoCTF{ntfs_hidden_alternate_data_stream}`

## 6. 출제자 노트 & 파일 제작 가이드
* **아티팩트 제작 방법**:
  1. 가상 NTFS 볼륨 파일을 생성하여 포맷합니다.
     `dd if=/dev/zero of=ntfs_drive.dd bs=1M count=20`
     `mkfs.ntfs -F ntfs_drive.dd` (테스트용이므로 강제 포맷 플래그 `-F` 지정)
  2. 리눅스에서 `ntfs-3g` 드라이버를 사용해 마운트하거나, 윈도우 환경에서 해당 볼륨을 로드합니다.
  3. 기본 내용 작성: `echo "This is a public notice." > notice.txt`
  4. 대체 스트림에 플래그 은닉:
     `echo "picoCTF{ntfs_hidden_alternate_data_stream}" > notice.txt:flag.txt`
  5. 마운트를 해제하고 최종 `ntfs_drive.dd` 이미지를 배포합니다.
* **출제 포인트**: 
  * 탐색기나 기본 `ls` 명령어 상으로는 감지되지 않는 NTFS 파일시스템 구조 레벨의 데이터 은닉(ADS) 취약성과 그 조사가 가지는 포렌식 실무적 가치를 체험하게 합니다.

## 7. 트러블슈팅 및 힌트
* **Q. 리눅스에서 mount 명령어로 마운트했는데 notice.txt:flag.txt 파일이 보이지 않습니다.**
  * A. 대체 데이터 스트림은 POSIX 표준 파일 구조가 아니므로 일반 마운트 상태의 디렉터리 내에서는 숨겨져 나타나지 않습니다. `ntfscat` 명령으로 파일시스템 raw 데이터에서 직접 속성 명칭을 읽거나, `mount -t ntfs-3g` 마운트 옵션 설정 시 스트림 처리를 활성화하도록 튜닝해야 합니다.
* **Q. getfattr 명령어로 속성이 비어 있다고 나옵니다.**
  * A. 마운트 드라이버가 NTFS의 대체 스트림을 확장 속성(xattr)으로 올바르게 노출하도록 마운트했는지 검사하거나, 로컬 툴 의존성이 낮고 가장 간편한 `ntfsprogs` 패키지의 전용 명령어(`ntfsinfo`, `ntfscat`)를 사용하는 쪽을 권장합니다.

## 8. 학습 포인트
* **대체 데이터 스트림(Alternate Data Streams)**: NTFS 파일시스템이 리소스 포크(Resource Fork) 호환을 위해 유지하는 메타데이터 결합 구조와 이를 이용한 악성코드 은닉 원리를 이해합니다.
* **파일시스템 저수준 유틸리티**: 마운트 과정 없이 원본 파일시스템 원시 이미지 레벨에서 다이렉트로 개별 인덱싱 메타 구조를 쿼리해 파싱하는 분석 기법을 터득합니다.
