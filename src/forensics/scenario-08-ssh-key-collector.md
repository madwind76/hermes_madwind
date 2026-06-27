---
title: SSH 열쇠 수집가 (The SSH Key Collector)
created: 2026-06-28
updated: 2026-06-28
type: ctf-challenge
tags: [ctf, ctf-challenge, forensics, disk, ext4, sleuthkit, ssh-key]
confidence: high
---

# SSH 열쇠 수집가 (The SSH Key Collector)

> **난이도**: 초중급  
> **소요 시간**: 25~30분  
> **참고 picoCTF 문제**: `operation-oni` (picoCTF 2022)

## 1. 배경 시나리오
사내 원격 배포 서버가 침해사고를 당했습니다. 조사관들은 용의자 계정의 PC에서 사용했던 가상 머신(VM)의 디스크 이미지 파일인 `suspect_disk.dd`를 획득했습니다. 침해사고 직전, 용의자가 서버 접근용 SSH 개인키를 급하게 삭제하고 흔적을 지운 것으로 추정됩니다. 분석가는 이 디스크 이미지를 분석해 삭제된 흔적이나 홈 디렉터리에 남아 있는 SSH 키(`id_rsa` 또는 `id_ed25519`)를 추출해 내야 합니다.

## 2. 제공 파일
* `suspect_disk.dd` (용의자 리눅스 VM의 ext4 파티션 Raw 디스크 이미지, 약 50MB)

## 3. 문제 목표
리눅스 파일시스템(ext4) 디스크 이미지의 파티션을 파악하고, Sleuthkit 도구 혹은 루프백 마운트를 사용해 시스템 내부 파일 구조를 탐색하여 홈 디렉터리 내 `.ssh` 폴더 아래 숨겨진(또는 삭제된) SSH 개인키를 복구합니다. 최종적으로 복구한 개인키의 지문(Fingerprint, SHA256 해시값)을 도출해 플래그를 인증합니다.

## 4. 의도한 풀이 흐름
1. **파티션 레이아웃 분석**:
   * `mmls suspect_disk.dd` 명령어로 이미지 내에 파티션이 어떻게 나뉘어 있는지 확인합니다.
   * 단일 파티션 이미지인 경우 `fsstat suspect_disk.dd`로 파일시스템이 ext4인지 점검합니다.
2. **파일 시스템 탐색 (Sleuthkit 활용)**:
   * `fls -r -o 0 suspect_disk.dd` 명령을 이용해 디렉터리를 재귀적으로 탐색하여 사용자 홈 디렉터리 경로를 찾습니다.
   * 홈 디렉터리(예: `/home/ubuntu/` 또는 `/root/`) 내부에서 `.ssh` 디렉터리가 존재하는지 확인합니다.
   * `id_rsa` 혹은 `id_ed25519` 와 같은 SSH 개인키 파일명의 아이노드(Inode) 번호를 식별합니다.
3. **개인키 파일 카빙**:
   * 알아낸 아이노드 번호(예: `14256`)를 바탕으로 `icat -o 0 suspect_disk.dd 14256 > recovered_key` 명령을 실행해 파일 내용을 디스크 이미지 밖으로 복구합니다.
4. **키 지문(Fingerprint) 도출**:
   * 복구된 개인키에 대해 권한을 부여하고 SSH 키 지문을 추출합니다.
     `ssh-keygen -l -f recovered_key`
   * 출력되는 지문 해시값(예: `SHA256:dGhpcyBpcyBhIHNhbXBsZSBrZXkgZmluZ2VycHJpbnQ...`)을 획득합니다.
5. **플래그 입력**: 획득한 SHA256 해시 부분을 포맷에 맞게 조립합니다.
   (예: `picoCTF{SHA256:dGhpcyBpcyBhIHNhbXBsZSBrZXkgZmluZ2VycHJpbnQ}`)

## 5. 정답(플래그) 규칙 및 예시
* **플래그 형식**: `picoCTF{SHA256:<sha256_hash_string>}`
* **예시**: `picoCTF{SHA256:dGhpcyBpcyBhIHNhbXBsZSBrZXkgZmluZ2VycHJpbnQ}`

## 6. 출제자 노트 & 파일 제작 가이드
* **아티팩트 제작 방법**:
  1. 가상 환경에서 임의의 SSH 키 쌍을 생성합니다:
     `ssh-keygen -t ed25519 -f temp_key`
  2. 50MB 크기의 가상 ext4 디스크를 빌드합니다:
     `dd if=/dev/zero of=suspect_disk.dd bs=1M count=50`
     `mkfs.ext4 suspect_disk.dd`
  3. 디스크 이미지를 마운트하고 내부에 `/home/ubuntu/.ssh/` 구조를 만들어 생성한 `temp_key` 개인키를 위치시킵니다.
  4. 정상적인 마운트 분석 흐름 외에, Sleuthkit 사용 숙련도 평가를 위해 키 파일을 강제로 `rm` 명령어로 삭제(Unlink)하되 메타데이터 데이터 블록 흔적이 덮어씌워지지 않게 조작하여 `fls`에 `* d/d` (Deleted) 상태로 검출되도록 설계하는 난이도 조절도 가능합니다.
* **출제 포인트**: 
  * 디스크 이미지를 직접 호스트 OS에 루프백 마운트하거나, Sleuthkit 도구 모음(`mmls`, `fls`, `icat`)을 사용해 저수준에서 파일시스템 내부 흔적을 복구하는 디스크 포렌식 기초를 실습합니다.

## 7. 트러블슈팅 및 힌트
* **Q. fls 결과가 너무 많아서 한눈에 보기 어렵습니다.**
  * A. 파이프 명령어를 사용하여 `.ssh` 키워드를 필터링하십시오:
     `fls -r -p suspect_disk.dd | grep -i "\.ssh"`
* **Q. icat을 실행했는데 'Inode not found' 에러가 납니다.**
  * A. 오프셋(`-o`) 값이 누락되었는지 점검하십시오. `mmls`로 디스크 내 ext4 파티션이 시작하는 시작 섹터(예: `2048`)를 알아낸 후 `-o 2048`과 같이 섹터 오프셋 옵션을 주어야 원활한 파싱이 됩니다.

## 8. 학습 포인트
* **디스크 구조 해석**: Raw 디스크 이미지(`*.dd` 또는 `*.img`)의 섹터 배치 구조를 이해하고 특정 파일시스템 파티션의 논리 시작 주소를 역산하는 법을 학습합니다.
* **삭제 파일 복구(Unallocated Data Extraction)**: 파일시스템의 메타 데이터 노드가 해제(Delete)되더라도 물리 데이터 블록이 남아 있을 때 아이노드를 추적하여 바이너리 데이터를 안전하게 복원하는 과정을 실습합니다.
