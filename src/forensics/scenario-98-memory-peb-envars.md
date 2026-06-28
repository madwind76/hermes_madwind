---
title: Volatility 3를 이용한 메모리 적재 프로세스 환경변수 덤프 분석 (Memory Process Environment Block)
created: 2026-06-28
updated: 2026-06-28
type: ctf-challenge
tags: [ctf, ctf-challenge, forensics, memory, volatility, envars, peb, process-environment-block, windows]
confidence: high
---

# Volatility 3를 이용한 메모리 적재 프로세스 환경변수 덤프 분석 (Memory Process Environment Block)

> **난이도**: 초중급  
> **소요 시간**: 25~30분  
> **참고 picoCTF 문제**: 메모리 프로세스 환경 블록 기밀 환경변수 파싱 (Volatility Envars 분석)

## 1. 배경 시나리오
공격자가 윈도우 원격 서버에 은밀히 침투하여 백도어 기동용 프로세스(`svchost_backdoor.exe`)를 실행시켰습니다. 해당 프로세스가 기동하는 단계에서 동작 매개변수 및 기밀 토큰 정보를 노출시키지 않기 위해, 공격자는 프로그램 실행 시 **사용자 정의 환경변수** 영역에 주요 플래그 문자열을 대입 기입하여 런타임에 호출하도록 기동했습니다. 사건 발생 후 서버 디스크 로그 상에서는 아무런 흔적도 찾을 수 없었으나, 기동 당시 수집한 RAM 메모리 덤프가 존재합니다. 윈도우 커널은 각 프로세스가 시작될 때 사용자 메모리 공간에 **프로세스 환경 블록 (PEB, Process Environment Block)** 구조체를 할당하고, 해당 프로세스 컨텍스트의 환경 변수 목록들을 평문 문자열로 유지합니다. 메모리 분석 보고서 파일인 `volatility_peb_envars.txt`를 정밀 점검하여, **백도어 프로세스 환경변수 테이블 내부에 하드코딩 적재되어 보존 중이던 플래그**를 구출하십시오.

## 2. 제공 파일
* `volatility_peb_envars.txt` (Volatility 3의 `windows.envars` 플러그인을 구동해 수집한 메모리 적재 프로세스별 전체 환경변수 리스트 텍스트 파일)

## 3. 문제 목표
윈도우 가상 메모리 프로세스 환경 블록(PEB) 내에 할당되는 프로세스 파라미터 및 환경 변수 블록 구조의 특성을 이해하고, Volatility `windows.envars` 파싱 리포트 테이블을 기반으로 타깃 PID의 유출 플래그 변수를 추출합니다.

## 4. 의도한 풀이 흐름
1. **환경변수 테이블 리포트 감사**:
   * 제공된 `volatility_peb_envars.txt` 텍스트 파일을 엽니다.
   * 리포트의 기본 컬럼 배치 구조(PID, Process Name, Variable Name, Value)를 확인합니다.
2. **의심 프로세스 및 플래그 매핑 검색**:
   * 메모리에 침투 가동 중이던 악성 백도어 프로세스인 `svchost_backdoor.exe` (PID: `4920`)의 행 데이터를 필터링합니다.
   * 또는 리포트 전체를 대상으로 플래그 포맷을 검색 기동합니다:
     `grep "picoCTF" volatility_peb_envars.txt`
3. **환경변수 매개변수 해독**:
   * 검색 매칭된 `svchost_backdoor.exe` 프로세스의 PEB 환경변수 테이블에서 다음 엔트리를 특정합니다:
     * **PID**: `4920`
     * **프로세스 이름 (Process)**: `svchost_backdoor.exe`
     * **환경변수 키 (Variable)**: `ENV_SECRET_TOKEN`
     * **환경변수 값 (Value)**: `picoCTF{peb_m3m_env_v4rs_retri3v3d}`
4. **플래그 도출**:
   * 추출한 환경변수 값으로부터 최종 플래그를 정립합니다:
     `picoCTF{peb_m3m_env_v4rs_retri3v3d}`

## 5. 정답(플래그) 규칙 및 예시
* **플래그 형식**: `picoCTF{<flag_string>}`
* **예시**: `picoCTF{peb_m3m_env_v4rs_retri3v3d}`

## 6. 출제자 노트 & 파일 제작 가이드
* **아티팩트 제작 방법**:
  1. Windows VM 가상 머신 테스트 환경에서 파워셸이나 cmd 환경을 열고 기밀 플래그 변수를 사전 매핑 선언합니다:
     `set ENV_SECRET_TOKEN=picoCTF{peb_m3m_env_v4rs_retri3v3d}`
  2. 해당 터미널 하위 세션에서 자작 백도어 프로그램 `svchost_backdoor.exe`를 기동시킵니다. (이 구동 시점에 부모 터미널의 환경변수가 자식 프로세스의 PEB 구조체 내 환경 블록 영역으로 자동 양도 및 평문 적재됩니다)
  3. 활성 상태인 가상머신의 메모리 덤프 `memory.raw`를 수집 획득합니다.
  4. Volatility 3를 가동하여 프로세스별 환경변수를 디코딩 출력합니다:
     `python3 vol.py -f memory.raw windows.envars > volatility_peb_envars.txt`
  5. 덤프 결과 리포트 내에 해당 악성 프로세스의 주입 환경변수 행이 정상적으로 직렬화되어 인쇄되었는지 검수하고 배포용 파일로 저장합니다.
* **출제 포인트**: 
  * 실행 명령행(CommandLine) 기록이 아티팩트 소거에 의해 모두 멸실되었더라도, 프로세스가 구동 도중 메모리 PEB(Process Environment Block Envars Forensics) 영역에 평문 보존하여 사용하는 환경 매개 변수 아카이브를 메모리 포렌식 도구로 완벽히 추출 분석해 내는 고급 조사 역량을 다집니다.

## 7. 트러블슈팅 및 힌트
* **Q. 프로세스 환경 블록(PEB)은 커널 메모리 영역에 존재하나요?**
  * A. 아닙니다. PEB 구조체는 운영체제가 관리하는 각 프로세스의 사용자 모드 가상 주소 공간(User-mode Address Space, 대개 커널 가상 주소 하위 대역)에 위치합니다. 따라서 OS 커널 페이지 테이블 해석뿐만 아니라, 대상 개별 프로세스의 사용자 가상 메모리 매핑 구조를 정상 파악해야만 파서가 해당 오프셋 주소를 찾아내 값을 파싱해 낼 수 있어 Volatility 3 도구 연동이 수월합니다.
* **Q. CommandLine 변수와 환경변수 Envars는 PEB 내에서 어떻게 구분되나요?**
  * A. PEB 내부의 `ProcessParameters` (즉 `_RTL_USER_PROCESS_PARAMETERS` 구조체) 필드는 하위 노드로 `CommandLine` 포인터 정보와 `Environment` 포인터 정보를 별도로 독립 할당해 관리합니다. 이 중 `Environment` 필드가 지목하는 물리 메모리 페이지 테이블 공간에 전체 환경 변수 키-값들이 유니코드(UTF-16LE) 문자열 스택 형태로 연속 기입되어 보존됩니다.

## 8. 학습 포인트
* **윈도우 PEB(Process Environment Block) 아키텍처**: 사용자 메모리 가상 공간 내의 프로세스 파라미터 및 환경 변수 저장 스택 레이아웃을 깊이 있게 이해합니다.
* **프로세스 환경 변수(Envars) 메모리 감사**: 침해 프로세스의 PEB 환경변수 테이블을 덤프 파싱하여, 명령행 정적 필터링을 우회해 은밀히 전송되던 기밀 플래그 데이터를 규명하는 기술을 배양합니다.
