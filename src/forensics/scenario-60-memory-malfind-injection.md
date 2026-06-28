---
title: Volatility 3를 이용한 악성 dll 인젝션 분석 (Memory Injection Malfind)
created: 2026-06-28
updated: 2026-06-28
type: ctf-challenge
tags: [ctf, ctf-challenge, forensics, memory, volatility, malfind, process-injection, shellcode]
confidence: high
---

# Volatility 3를 이용한 악성 dll 인젝션 분석 (Memory Injection Malfind)

> **난이도**: 초중급  
> **소요 시간**: 25~30분  
> **참고 picoCTF 문제**: 메모리 인젝션 백도어 탐지 및 카빙 (Volatility Malfind 플러그인 응용)

## 1. 배경 시나리오
윈도우 파일 서버 침해 조사 도중, 공격자가 정상 윈도우 시스템 프로세스인 `explorer.exe` 내부에 악성 DLL 파일 및 셸코드를 강제 삽입(Injection)하여 실행시킨 정황이 포착되었습니다. 정상 파일의 실행 경로를 빌려 가기 때문에 일반 디스크 파일 검사로는 악성 바이너리가 검출되지 않습니다. 분석팀은 RAM 메모리를 덤프하여 Volatility 3를 구동하고, 프로세스 가상 메모리 공간 중 비정상적인 보호 속성을 가졌거나 인젝션 징후가 강한 섹터를 탐지하는 **malfind** 플러그인을 가동해 결과 리포트 `volatility_malfind_output.txt`를 추출했습니다. 이 덤프 데이터를 분석하여 **인젝션된 메모리 페이지 시작 위치에 잔재하는 헥스 바이트 스트림(플래그)**을 복원해 내야 합니다.

## 2. 제공 파일
* `volatility_malfind_output.txt` (Volatility 3의 `windows.malfind` 플러그인을 돌려 획득한 메모리 인젝션 의심 세그먼트 분석 리포트)

## 3. 문제 목표
윈도우의 메모리 인젝션 기법(VirtualAllocEx, WriteProcessMemory API를 활용해 target 프로세스의 VAD 속성을 `PAGE_EXECUTE_READWRITE`로 변경 및 로딩하는 기법)의 특성을 이해하고, Volatility `malfind` 결과창의 헥스 데이터 덤프를 디코딩하여 플래그를 카빙합니다.

## 4. 의도한 풀이 흐름
1. **Malfind 분석 리포트 확인**:
   * 제공된 `volatility_malfind_output.txt` 텍스트 파일을 엽니다.
   * `malfind` 결과는 인젝션이 의심되는 메모리 블록마다 프로세스 정보와 메모리 주소 범위, 보호 속성(Protection), 그리고 해당 영역 선두 64바이트의 헥스 덤프(Hex Dump) 및 디스어셈블리(Disassembly) 코드를 테이블 형태로 제공합니다.
2. **비정상 보호 속성 및 헥스 덤프 스캔**:
   * 각 프로세스 세그먼트 중 보호 속성이 `PAGE_EXECUTE_READWRITE` (RWX, 읽고 쓰고 실행 가능한 속성)이면서, 동시에 메모리 시작 부분에 실행 명령어 또는 데이터 흔적이 담긴 블록을 조회합니다.
   * 탐색 중 `explorer.exe` (PID: 3400) 프로세스의 주소 영역 중 한 섹터의 헥스 덤프(Hex Dump) 부분에서 비정상적인 아스키 바이트 배열을 식별합니다:
     ```text
     Process: explorer.exe Pid: 3400 Address: 0xdf81ab090000
     Protection: PAGE_EXECUTE_READWRITE
     
     0xdf81ab090000  70 69 63 6f 43 54 46 7b 6d 61 6c 66 69 6e 64 5f   picoCTF{malfind_
     0xdf81ab090010  69 6e 6a 65 63 74 69 6f 6e 5f 64 65 74 65 63 74   injection_detect
     0xdf81ab090020  65 64 7d 00 00 00 00 00 00 00 00 00 00 00 00 00   ed}.............
     ```
3. **바이너리 디코딩 및 플래그 획득**:
   * 우측의 아스키 해석 텍스트 뷰나 좌측의 헥스 바이트 스트림(`70 69 63 6f...`)을 디코딩하여 문자열을 획득합니다:
     `picoCTF{malfind_injection_detected}`

## 5. 정답(플래그) 규칙 및 예시
* **플래그 형식**: `picoCTF{<flag_string>}`
* **예시**: `picoCTF{malfind_injection_detected}`

## 6. 출제자 노트 & 파일 제작 가이드
* **아티팩트 제작 방법**:
  1. Windows 가상 머신 상에서 모의 셸코드 인젝션 툴을 작동시킵니다. 이 툴은 `explorer.exe` 가상 메모리 공간을 강제 할당(`PAGE_EXECUTE_READWRITE`)하고 그 주소에 플래그 바이트 스트림 `picoCTF{malfind_injection_detected}`를 수록합니다.
  2. 메모리 덤프 이미지를 획득하여 `windows.malfind` 플러그인을 수행시킵니다:
     `python3 vol.py -f memory.dmp windows.malfind > volatility_malfind_output.txt`
  3. 덤프 리포트 상에서 정상 윈도우 스레드 구동(더미) 정보들과 함께, 위 `explorer.exe` 인젝션 페이지 주소 영역의 Hex 데이터가 명확하게 인쇄 출력되는 것을 검수하여 배포용 텍스트 파일로 지정합니다.
* **출제 포인트**: 
  * 메모리 포렌식의 진수이자 정수인 동적 프로세스 인젝션 탐지(Process Injection Forensics) 기법에 대한 VAD(Virtual Address Descriptor) 보호 플래그 상관 관계를 정립하고, malfind 툴의 기표 필드를 판별하는 훈련을 유도합니다.

## 7. 트러블슈팅 및 힌트
* **Q. malfind가 PAGE_EXECUTE_READWRITE(RWX)인 모든 메모리 블록을 악성으로 오판하지 않나요?**
  * A. 네, 그렇습니다. 자바 가상머신(JVM)이나 모던 브라우저의 JIT(Just-In-Time) 컴파일러 엔진 역시 런타임 최적화를 위해 특정 가상 메모리 공간을 `PAGE_EXECUTE_READWRITE` 속성으로 확보해 활용하므로 malfind 상에 무수히 많이 탐지되어 노이즈로 섞이게 됩니다. 따라서 실제 악성을 구분하기 위해서는 탐지된 메모리의 첫 부분에 **PE 포맷 헤더(`MZ` 마크)**가 존재하는지, 혹은 부적절한 기계어 제어 명령 흐름(Shellcode Loop)이 포함되어 있는지 strings 및 disasm 코드를 교차 비교해야 오탐(False Positive)을 제거할 수 있습니다.
* **Q. VAD(Virtual Address Descriptor)는 무엇인가요?**
  * A. 윈도우 커널이 특정 프로세스의 가상 주소 공간 할당 내역을 계층적으로 인덱싱해 추적하기 위해 메모리에 구성하는 트리 데이터 구조체입니다. Volatility의 `malfind`나 `vadinfo`는 이 VAD 트리를 횡단 스캔하여 개별 메모리 페이지의 보호 권한 플래그와 주소 범위를 고속 파싱해 냅니다.

## 8. 학습 포인트
* **메모리 인젝션 기법**: 정상 프로세스의 권한을 기생 활용하기 위해 API(VirtualAllocEx 등) 수준에서 가상 메모리를 조작하는 백도어 구동 매커니즘을 파악합니다.
* **VAD(Virtual Address Descriptor) 트리 포렌식**: 가상 메모리 맵의 보호 속성을 추적하여 JIT 컴파일러 오탐을 거르고, 정밀한 쉘코드 데이터 영역을 카빙해 복원해 내는 역량을 기릅니다.
