---
title: Volatility 3를 이용한 숨겨진 프로세스 탐지 (Memory Process Hiding)
created: 2026-06-28
updated: 2026-06-28
type: ctf-challenge
tags: [ctf, ctf-challenge, forensics, memory, volatility, rootkit, dkom, process-hiding]
confidence: high
---

# Volatility 3를 이용한 숨겨진 프로세스 탐지 (Memory Process Hiding)

> **난이도**: 초중급  
> **소요 시간**: 25~30분  
> **참고 picoCTF 문제**: 메모리 루트킷 및 은닉 프로세스 감사 (Volatility Psxview/Psscan 구조 분석)

## 1. 배경 시나리오
사내 핵심 자산 서버에 원격 접속 백도어가 구동되고 있다는 경보를 인지했으나, 윈도우 기본 "작업 관리자" 및 일반적인 활성 프로세스 스캔 명령어(`pslist`) 상에는 어떤 의심스러운 프로세스도 식별되지 않았습니다. 분석가들은 커널 레벨에서 동작하며 자신의 프로세스 객체 링크를 끊어 숨기는 커널 루트킷(Rootkit) 악성코드가 침투한 것으로 의심하고 있습니다. 메모리 분석 프레임워크인 **Volatility 3**를 가동하여 프로세스 교차 검증 플러그인을 수행해 획득한 `volatility_psxview_output.txt` 파일이 제공됩니다. 이 출력 데이터를 정밀 분석하여 **은닉 수법(DKOM)으로 숨겨져 동작하던 백도어 프로세스의 파일명과 PID(플래그)**를 도출하십시오.

## 2. 제공 파일
* `volatility_psxview_output.txt` (Volatility 3의 `windows.psxview` 플러그인을 실행해 얻은 프로세스 교차 대조 결과 테이블 파일)

## 3. 문제 목표
윈도우 커널이 프로세스를 스케줄링하기 위해 유지하는 활성 프로세스 이중 연결 리스트(ActiveProcessLinks) 구조체 체인을 이해하고, 이를 변조하는 DKOM(Direct Kernel Object Manipulation) 은닉 공격에 맞서, 메모리 풀 스캐닝 방식(`psscan`)과 API 비교 대조를 통해 숨겨진 프로세스의 정보를 도출합니다.

## 4. 의도한 풀이 흐름
1. **프로세스 교차 테이블 헤더 분석**:
   * 제공된 `volatility_psxview_output.txt` 파일을 텍스트 뷰어로 엽니다.
   * `psxview` 플러그인은 프로세스를 탐지하는 여러 경로(`pslist`, `psscan`, `thrdproc`, `pspcid`, `csrss` 등)의 조회 여부를 True/False 테이블 형태로 도출합니다:
     `PID | Name | pslist | psscan | thrdproc | pspcid | csrss | session`
2. **은닉 상태 식별 (pslist=False & psscan=True 탐색)**:
   * 일반적인 정상 프로세스는 운영체제의 활성 리스트에 존재하므로 `pslist`와 `psscan` 필드가 모두 **True**로 나타납니다.
   * 하지만 커널 구조체 체인(ActiveProcessLinks)에서 자신의 링크만 분리해 숨긴 프로세스는 `pslist`에서는 감지되지 않아 **False**로 표시되지만, 물리 가상 메모리 풀 전체를 뒤지는 헤더 탐색 기법인 `psscan` 필드에서는 **True**로 탐지됩니다.
   * 테이블 행을 한 줄씩 스캔하여 `pslist`가 `False` 이고 `psscan`이 `True`인 비정상 행을 색인합니다:
     ```bash
     grep -i "false" volatility_psxview_output.txt | grep -i "true"
     ```
   * 조회 결과 아래의 은닉 프로세스 레코드를 탐지합니다:
     `4208 | hidden_agent.exe | False | True | True | True | True | True`
3. **포렌식 정보 조합 및 플래그 완성**:
   * 탐색된 행에서 플래그 요구 변수들을 조립합니다:
     * 숨겨진 프로세스명: `hidden_agent.exe`
     * 프로세스 아이디 (PID): `4208`
   * 요구 규격 포맷에 맞게 언더스코어로 결합해 제출합니다:
     `picoCTF{hidden_agent.exe_4208_dkom_detected}`

## 5. 정답(플래그) 규칙 및 예시
* **플래그 형식**: `picoCTF{<process_name>_<pid>_dkom_detected}`
* **예시**: `picoCTF{hidden_agent.exe_4208_dkom_detected}`

## 6. 출제자 노트 & 파일 제작 가이드
* **아티팩트 제작 방법**:
  1. Windows 테스트 가상 머신에 커널 루트킷(예: FU Rootkit 등 DKOM 프로세스 숨김 기능이 지원되는 도구)을 가동시켜 `hidden_agent.exe` (PID: 4208) 프로세스를 ActiveProcessLinks 리스트에서 언링크(Unlink) 시킵니다.
  2. 시스템 메모리 덤프를 획득하여 `memory.dmp`로 저장합니다.
  3. Volatility 3의 `windows.psxview` 플러그인을 가동시켜 프로세스 매핑 뷰 텍스트를 출력합니다:
     `python3 vol.py -f memory.dmp windows.psxview > volatility_psxview_output.txt`
  4. 덤프 결과 파일 내에 `system.exe`, `explorer.exe`, `svchost.exe` 등 정상적인 프로세스 목록(모두 True 상태) 수십 줄을 덧붙여 난이도를 조율한 후 배포합니다.
* **출제 포인트**: 
  * OS API 인터페이스를 교묘히 우회 및 기만하는 지능형 위협(커널 루트킷)에 대응하여, 메모리 포렌식 도구의 물리 풀 메모리 스캔 원리 및 다중 소스 교차 검증(Cross-Reference Analysis) 절차의 중요성을 교육합니다.

## 7. 트러블슈팅 및 힌트
* **Q. pslist가 False이고 psscan이 True이면 무조건 루트킷 악성코드인가요?**
  * A. 대다수의 경우 그렇습니다. 하지만 프로세스가 방금 막 종료되어 소멸 세션 중이거나, 로딩이 완전히 끝나지 않은 극단적인 타이밍에 메모리가 덤프된 경우에도 일시적으로 두 필드 값이 불일치할 수 있으므로 생성 스레드(`thrdproc`) 상태 등의 다른 지표도 함께 고려해야 정밀 분석이 완성됩니다.
* **Q. Volatility 3에서 psscan은 어떤 원리로 동작하나요?**
  * A. 윈도우 커널에서 프로세스를 정의하는 `_EPROCESS` 구조체는 메모리 풀 상에 생성될 때 고유한 매직 풀 태그(Pool Tag)인 `ProC` 문자열 시그니처를 헤더에 지니게 됩니다. `psscan` 플러그인은 프로세스 연결 링크를 보지 않고, RAM 덤프 공간 전체를 물리 바이트 스캔하여 `ProC` 풀 태그를 지닌 구조체를 강제 카빙해 내는 방식으로 숨겨진 프로세스를 복원합니다.

## 8. 학습 포인트
* **ActiveProcessLinks 명세**: 윈도우 커널이 실행 프로세스를 리스트 형식으로 체이닝해 관리하는 양방향 링크 구조 및 DKOM 루트킷 은닉 기법의 작동 원리를 파악합니다.
* **프로세스 교차 검증(Cross-Reference)**: `pslist`, `psscan`, `csrss` 세션 등 다양한 영역의 프로세스 적재 목록을 획득해 불일치 지점을 규명하는 메모리 포렌식 침해 사고 감사 능력을 체계화합니다.
