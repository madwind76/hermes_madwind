---
title: 윈도우 원격 도구 가동 이력 프리페치 분석 (Remote Access Tool Execution - AnyDesk)
created: 2026-06-28
updated: 2026-06-28
type: ctf-challenge
tags: [ctf, ctf-challenge, forensics, windows, prefetch, rat, anydesk, execution-history, pecmd]
confidence: high
---

# 윈도우 원격 도구 가동 이력 프리페치 분석 (Remote Access Tool Execution - AnyDesk)

> **난이도**: 초급  
> **소요 시간**: 15~20분  
> **참고 picoCTF 문제**: 비인가 원격 제어 프로그램 실행 흔적 역추적 (Windows Prefetch Referenced Files 분석)

## 1. 배경 시나리오
공격자가 핵심 직원의 계정 자격을 도용한 후, 시스템 원격 화면 제어를 위해 상용 원격 데스크톱 소프트웨어인 **AnyDesk**(`anydesk.exe`)를 비인가 수단으로 몰래 설치 및 구동하여 사내 중요 데이터를 화면 캡처 및 유출한 정황이 감지되었습니다. 공격자는 실행 직후 자신의 AnyDesk 설치 디렉터리와 최근 실행 문서를 지우고 도망쳤습니다. 하지만 윈도우 OS는 응용 프로그램이 최초 구동될 때 런타임 최적화를 위해 호출한 라이브러리와 폴더 목록을 기록하는 프리페치 파일(`.pf`) 내부에 **최초 실행 10초 이내에 로딩/참조한 파일 목록(Referenced Files)**을 영구적으로 직렬화하여 박제합니다. 확보한 AnyDesk 프리페치 파일인 `ANYDESK.EXE-E6C87C5F.pf`를 분석하여, **프로그램이 실행될 때 함께 호출되었던 비정상 참조 파일 경로 속의 플래그**를 획득하십시오.

## 2. 제공 파일
* `ANYDESK.EXE-E6C87C5F.pf` (사용자 환경에서 수집한 AnyDesk 실행 대응 윈도우 프리페치 바이너리 파일)

## 3. 문제 목표
윈도우 프리페치(Prefetch) 메타데이터 파일 구조의 세부 속성(실행 횟수, 볼륨 이력 외에 프로그램 가동 시 10초 동안 로딩되는 DLL 및 참조 파일 경로 목록)을 이해하고, 전문 프리페치 파서 도구(PECmd 등)를 활용하여 인젝션되거나 참조된 공격 증적 파일을 식별합니다.

## 4. 의도한 풀이 흐름
1. **프리페치 아티팩트 파싱**:
   * 제공된 `ANYDESK.EXE-E6C87C5F.pf` 파일을 분석하기 위해 Eric Zimmerman의 `PECmd.exe` 도구를 실행합니다.
     `PECmd.exe -f ANYDESK.EXE-E6C87C5F.pf`
   * 또는 리눅스 터미널의 파이썬 기반 프리페치 파서 스크립트를 사용하여 내부 스트림 데이터를 텍스트화합니다.
2. **참조 파일 목록 (Referenced Files) 감사**:
   * 파싱 결과 리포트 하단부의 **Referenced Files (참조된 파일 목록)** 섹션으로 스크롤합니다.
   * 프리페치는 프로그램 기동에 관여한 수십 개의 DLL 라이브러리 및 임시 설정 파일 절대 경로를 나열합니다:
     * `\DEVICE\HARDDISKVOLUME2\WINDOWS\SYSTEM32\NTDLL.DLL`
     * `\DEVICE\HARDDISKVOLUME2\USERS\ADMIN\APPDATA\ROAMING\ANYDESK\SYSTEM.CONF`
   * 참조 목록 중 사용자 데스크톱 경로 아래에 등록되어 실행 단계에서 로딩 이력이 남은 다음의 의심스러운 텍스트 파일 엔트리를 포착합니다:
     `\DEVICE\HARDDISKVOLUME2\USERS\ADMIN\DESKTOP\picoCTF{anyd3sk_pf_tr4c3s_r3mot3_conn}.TXT`
3. **플래그 도출**:
   * 탐색된 텍스트 파일명 자체에서 최종 플래그 값을 획득합니다:
     `picoCTF{anyd3sk_pf_tr4c3s_r3mot3_conn}`

## 5. 정답(플래그) 규칙 및 예시
* **플래그 형식**: `picoCTF{<flag_string>}`
* **예시**: `picoCTF{anyd3sk_pf_tr4c3s_r3mot3_conn}`

## 6. 출제자 노트 & 파일 제작 가이드
* **아티팩트 제작 방법**:
  1. Windows 10/11 가상 머신의 관리자 바탕화면(`C:\Users\admin\Desktop\`) 하위에 기밀 플래그 파일 `picoCTF{anyd3sk_pf_tr4c3s_r3mot3_conn}.txt`를 사전 생성해 놓습니다.
  2. AnyDesk 공식 설치 파일 또는 포터블 버전을 가동합니다.
  3. AnyDesk 가동 직후 최초 10초 이내에 바탕화면에 있던 위 `picoCTF{...}.txt` 파일을 AnyDesk의 파일 전송(File Transfer) 창으로 드래그 앤 드롭하여 로드하거나 탐색기 연동을 유도합니다. (이때 프리페치 드라이버가 AnyDesk 프로세스의 해당 파일 핸들 액세스를 기록 스트림에 수집합니다)
  4. 프리페치 보존 폴더(`C:\Windows\Prefetch\`)로 이동하여 수정 타임스탬프가 최신인 `ANYDESK.EXE-XXXXXXXX.pf` 파일을 FTK Imager로 안전 덤프 추출합니다.
  5. 덤프 파일을 배포 파일로 유저에게 배포합니다.
* **출제 포인트**: 
  * 원격 제어 도구(AnyDesk, TeamViewer 등 상용 RAT)를 이용한 정보 반출 위협 발생 시, 공격자가 해당 툴을 기동하여 로드했던 내부 파일들의 초기 인덱스 목록이 프리페치 참조 아티팩트(Prefetch Referenced Files Analysis) 내에 고스란히 영구 기록되는 현상을 규명하여 용의 행위를 증명하는 고급 실무 프로세스를 교육합니다.

## 7. 트러블슈팅 및 힌트
* **Q. 프리페치는 어떻게 프로그램 실행 10초 이내의 파일 목록을 기억할 수 있나요?**
  * A. 윈도우의 프리페치 드라이버(`%SystemRoot%\System32\Drivers\rxtg.sys` 또는 cache manager)는 응용 프로그램이 메모리에 로딩되어 초기 실행을 수행할 때 발생하는 모든 디스크 읽기/쓰기 파일 I/O 시스템 콜을 10초 동안 강제로 추적(Trace)합니다. 이를 메모리에 임시 보관한 뒤 프로그램 종료 혹은 버퍼 동기화 단계에서 해당 실행 파일 이름의 `.pf` 파일 내 "참조 파일 목록 테이블"에 직렬화 저장하기 때문에 포렌식 수사관에게 골드 마인(Gold Mine)으로 기능합니다.
* **Q. 참조 파일 목록 파싱 시 \DEVICE\HARDDISKVOLUME2 와 같은 경로는 어떻게 해석하나요?**
  * A. 프리페치는 파일시스템 드라이브 문자(C:, D:) 대신 윈도우 NT 커널 오브젝트 관리자의 물리 장치 경로 형식(`\DEVICE\HARDDISKVOLUME`)으로 위치를 보존합니다. 일반적인 시스템 환경에서 `HARDDISKVOLUME2`는 윈도우가 설치되어 구동되는 활성 시스템 드라이브인 `C 드라이브` 볼륨과 1대1 매핑되므로 손쉽게 물리 절대 경로로 환원해 추론할 수 있습니다.

## 8. 학습 포인트
* **윈도우 프리페치(Prefetch) I/O 모니터링 원리**: 프로그램 실행 초기(10초)에 발생하는 시스템 드라이버 파일 로딩 이력 수집 명세를 완벽히 습득합니다.
* **비인가 원격 도구 감사**: AnyDesk 등 상용 원격제어 소프트웨어의 가동 흔적을 추적하여 침해 당시 로드했던 민감 기밀 자산의 리스트를 프리페치 아티팩트를 통해 교차 재구성하는 분석 능력을 갖춥니다.
