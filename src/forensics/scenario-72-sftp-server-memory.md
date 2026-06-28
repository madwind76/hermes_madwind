---
title: 리눅스 프로세스 메모리 속 파일 전송 데이터 추출 (Linux sftp-server process core dump)
created: 2026-06-28
updated: 2026-06-28
type: ctf-challenge
tags: [ctf, ctf-challenge, forensics, linux, memory, sftp, process-dump, strings, data-carving]
confidence: high
---

# 리눅스 프로세스 메모리 속 파일 전송 데이터 추출 (Linux sftp-server process core dump)

> **난이도**: 초중급  
> **소요 시간**: 25~30분  
> **참고 picoCTF 문제**: 프로세스 가상 메모리 기밀 정보 카빙 (Linux sftp-server Memory 분석)

## 1. 배경 시나리오
사내 연구망 서버에서 내부 기밀 설계 도면 및 텍스트 데이터가 외부로 불법 유출되고 있는 정황이 실시간 네트워크 패킷 대역폭 점검을 통해 감지되었습니다. 위협 대응팀은 공격자가 SSH 연동 보안 통신인 SFTP(Secure File Transfer Protocol) 서비스를 이용해 파일 전송을 개시한 것을 실시간 파악하고, 전송 대상 파일이 디스크 상에서 이미 소거되었거나 패킷이 완전히 암호화된 상태임을 고려하여, 실시간 전송을 담당하는 **sftp-server** 프로세스의 가상 메모리를 즉시 강제 덤프(Core Dump) 처리했습니다. 덤프 파일 `sftp_server_memory.dmp`를 분석하여, **전송 도중 sftp-server의 커널 메모리 버퍼 영역에 일시 탑재되어 흐르던 평문 파일 내용 속의 플래그**를 구출하십시오.

## 2. 제공 파일
* `sftp_server_memory.dmp` (SFTP 데이터 송수신 세션 동작 중 sftp-server 활성 프로세스 가상 메모리 세그먼트에서 덤프한 이진 코어 덤프 파일)

## 3. 문제 목표
리눅스의 OpenSSH sftp-server 서비스가 로컬 스토리지로부터 데이터를 읽어 소켓을 통해 전송하거나 그 반대로 동작할 때, 프로세스 힙/프라이빗 가상 메모리에 데이터 청크(Data Chunk) 버퍼 스트림을 임시 캐시하여 핸들링하는 동작 특성을 파악하고, 프로세스 덤프 바이너리에서 평문 버퍼 영역을 카빙해 내는 기술을 학습합니다.

## 4. 의도한 풀이 흐름
1. **이진 덤프 파일 정적 분석**:
   * 제공된 `sftp_server_memory.dmp` 파일은 프로세스의 가상 메모리 맵 전체를 저장하고 있어 평문 텍스트와 이진 제어 레지스터 데이터가 혼재되어 있습니다.
   * 메모리에 흐르던 아스키 문자열을 수집하기 위해 `strings` 명령어를 가동하고 플래그 포맷을 필터 검색합니다:
     ```bash
     strings sftp_server_memory.dmp | grep "picoCTF"
     ```
2. **SFTP 전송 버퍼 흔적 카빙**:
   * 검색 결과, sftp-server 프로세스가 전송 패킷 조립을 위해 할당한 힙 메모리 데이터 청크 세그먼트 부근에서 다음과 같은 평문 전송 캐시 스트림을 식별합니다:
     `[SFTP_TX_BUFFER] data_chunk: picoCTF{sftp_transf3r_m3m_buf_carv3d}`
3. **플래그 도출**:
   * 버퍼에 실려 전송되고 있던 핵심 기밀 문자열로부터 최종 플래그를 정립합니다:
     `picoCTF{sftp_transf3r_m3m_buf_carv3d}`

## 5. 정답(플래그) 규칙 및 예시
* **플래그 형식**: `picoCTF{<flag_string>}`
* **예시**: `picoCTF{sftp_transf3r_m3m_buf_carv3d}`

## 6. 출제자 노트 & 파일 제작 가이드
* **아티팩트 제작 방법**:
  1. 테스트 리눅스 서버에서 SSH/SFTP 데몬을 구동합니다.
  2. 원격 SFTP 클라이언트 소프트웨어(예: WinSCP, FileZilla 또는 sftp CLI)를 사용해 서버에 접속한 뒤, 플래그가 주입된 중요 텍스트 파일을 유출 전송(Get/Download)합니다:
     `get sensitive_flag.txt`
  3. 전송이 처리되고 있는 런타임 세션 도중, 서버 백그라운드에서 구동되고 있는 하위 `sftp-server` 서비스 핸들러 프로세스의 PID를 획득합니다:
     `ps aux | grep sftp-server`
  4. GDB 도구 또는 `/proc/<PID>/mem` 카빙 기법을 이용해 sftp-server 프로세스 전체 가상 메모리를 덤프합니다:
     `gcore -o sftp_server_memory <PID>`
  5. 생성된 코어 덤프 바이너리에서 기밀 플래그 텍스트가 임시 보존되어 있던 데이터 청크 힙 영역을 식별해 낸 후, 분석 가치가 높은 메모리 페이지 대역을 부분 분할하여 `sftp_server_memory.dmp` 배포 파일로 저장합니다.
* **출제 포인트**: 
  * 암호화 네트워크 패킷(SSH/SFTP) 유출 사고 시, 패킷 복호화 키 분석 외에 종단점(Endpoint) 호스트 서버의 가상 메모리 프로세스 덤프(Process Memory Forensics) 분석을 병행하여 전송 중인 기밀 데이터를 평문 상태로 즉각 획득해 내는 DFIR 실무 대응 역량을 배양합니다.

## 7. 트러블슈팅 및 힌트
* **Q. sftp-server 프로세스는 파일 전송이 끝난 후에도 메모리에 버퍼를 보존하나요?**
  * A. 원칙적으로는 전송 루프 블록이 종료되면 버퍼 메모리가 반환(`free()`)되어 해제됩니다. 하지만 리눅스 메모리 관리 기법 상 `free` 처리된 영역은 새로운 다른 프로세스가 메모리를 재요청해 물리 페이지에 덮어쓰기(Overwrite) 전까지는 기존 원본 바이트가 힙 슬랙(Heap Slack) 영역에 고스란히 영구 방치되므로, 파일 전송이 종료된 직후에 프로세스를 덤프하더라도 크리덴셜 및 전송 평문 데이터를 충분히 발굴할 수 있습니다.
* **Q. 대용량 바이너리에서 strings 대신 특정 버퍼 시그니처 구조체를 기준으로 정밀 파싱하고 싶습니다.**
  * A. 파이썬 `mmap` 라이브러리를 사용하면 좋습니다. 메모리 덤프 파일을 매핑한 뒤, sftp 프로토콜 데이터의 시작 식별 바이트나 특정 파일 전송 세션 제어 헤더 오프셋 구조를 스캔하여 픽셀 이미지나 다중 전송 텍스트 데이터의 바이트 배열만 자동 오프셋 계산하여 파일로 카빙해 낼 수 있어 편리합니다.

## 8. 학습 포인트
* **리눅스 SFTP 데몬 동작 및 메모리 버퍼 체계**: SFTP 파일 전송 프로토콜 핸들링 시, 내부 데이터 블록이 메모리 힙 구조체에 적재되는 캐싱 특성을 배웁니다.
* **프로세스 힙 슬랙(Heap Slack) 카빙**: 자원 반환 후에도 덮어씌워지지 않아 RAM 상에 잔재하는 가상 메모리 이진 바이트 스트림을 카빙하여 증적을 환원하는 메모리 분석론을 마스터합니다.
