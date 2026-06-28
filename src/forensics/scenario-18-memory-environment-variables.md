---
title: 메모리 속 환경 변수의 비밀 (Memory Environment Variables)
created: 2026-06-28
updated: 2026-06-28
type: ctf-challenge
tags: [ctf, ctf-challenge, forensics, memory, volatility, environment-variables, linux]
confidence: high
---

# 메모리 속 환경 변수의 비밀 (Memory Environment Variables)

> **난이도**: 초중급  
> **소요 시간**: 25~30분  
> **참고 picoCTF 문제**: `mob-psycho` 변형 및 실무 메모리 포렌식 (Volatility 프로세스 환경변수 덤프 기법)

## 1. 배경 시나리오
사내 핵심 DB 제어 서버에 외부 해킹 그룹이 무단 접속하여 중요 민감 정보를 유출했습니다. 피해 서버의 소스 코드와 설정 파일에는 패스워드나 인증 토큰이 하드코딩되어 있지 않았으나, 개발자는 부팅 단계에서 리눅스 시스템 데몬 실행 시 **프로세스 환경 변수(Environment Variable)** 형태로 중요 액세스 키(플래그)를 직접 주입해 두었다고 밝혔습니다. 조사팀은 해커가 프로세스를 끄기 직전, 시스템 메모리 상태를 박제한 `mem_dump.raw` 파일을 획득했습니다. 분석가는 실행 중이던 특정 웹 애플리케이션 데몬 프로세스의 메모리 영역을 해독하여 은밀하게 주입되어 있던 플래그를 복구해야 합니다.

## 2. 제공 파일
* `mem_dump.raw` (리눅스 시스템 메모리 덤프 파일, 약 256MB)
* `ps_list.txt` (메모리 덤프 당시 실행 중이던 프로세스 목록 텍스트 추출본)
  * 주요 프로세스 후보: `PID 4821 - /usr/bin/python3 app.py`

## 3. 문제 목표
메모리 분석 프레임워크인 **Volatility**(버전 2 또는 3)를 활용하여 대상 시스템의 프로필을 판정하고, 실행 중인 특정 프로세스(PID 4821)의 프로세스 제어 블록(PCB) 메모리 영역 중 환경 변수 스트링 테이블이 상주하는 위치를 쿼리해 플래그 값을 획득합니다.

## 4. 의도한 풀이 흐름
1. **프로세스 식별**:
   * 제공된 `ps_list.txt`에서 개발자가 언급한 웹 데몬 프로세스의 이름과 PID(`4821`)를 대조 확인합니다.
2. **Volatility 구동**:
   * Volatility 3(또는 2)를 실행하여 메모리 덤프 파일의 구조를 로드합니다.
   * 리눅스 메모리 분석 명령어인 `linux.envars` (또는 Windows의 경우 `windows.envars`) 플러그인을 활용합니다.
3. **특정 프로세스 환경 변수 출력**:
   * PID 4821을 지정해 환경 변수를 필터링하여 출력합니다:
     ```bash
     python3 vol.py -f mem_dump.raw linux.envars --pid 4821
     ```
   * 출력 리스트에서 환경 변수 명칭 `FLAG` 또는 `SECRET_TOKEN`에 매핑된 값을 스캔합니다.
     (예: `FLAG=picoCTF{mem0ry_env_vars_are_volatile_but_retrievable}`)
4. **대안 풀이 (메모리 덤프 카빙)**:
   * Volatility를 쓸 수 없는 환경인 경우, 리눅스 프로세스 환경 변수는 메모리 스택(Stack) 영역 상부의 평문 문자열 블록으로 보존되므로 `strings` 명령어를 사용해 키워드 기반으로 직접 문자열을 검색해 볼 수도 있습니다:
     ```bash
     strings mem_dump.raw | grep -A 2 -B 2 "picoCTF{"
     ```

## 5. 정답(플래그) 규칙 및 예시
* **플래그 형식**: `picoCTF{<flag_string>}`
* **예시**: `picoCTF{mem0ry_env_vars_are_volatile_but_retrievable}`

## 6. 출제자 노트 & 파일 제작 가이드
* **아티팩트 제작 방법**:
  1. 리눅스 가상 머신(예: Ubuntu 22.04 LTS)을 기동합니다.
  2. 환경 변수를 주입한 임의의 백그라운드 파이썬 프로세스를 실행합니다:
     `export SECRET_KEY="picoCTF{mem0ry_env_vars_are_volatile_but_retrievable}"`
     `python3 app.py &`
  3. 실행된 프로세스의 PID를 메모해 둡니다 (예: `4821`).
  4. 커널 도구인 `LiME` 또는 `dd`를 사용하여 시스템 물리 메모리 전체를 덤프해 `mem_dump.raw`를 생성합니다.
  5. 덤프 파일 배포 시, Volatility에서 커널 디버깅 기호(System.map, Kernel DWARF)가 없어도 환경 변수를 파싱해 낼 수 있게 Volatility 3에 적절한 리눅스 ISF(Intermediate Symbol File) 프로필을 같이 제공하거나 `strings` 검색으로도 플래그가 나오도록 아티팩트를 구성해 출제합니다.
* **출제 포인트**: 
  * 디스크 상의 흔적만을 조사하는 포렌식의 한계를 극복하기 위해, 휘발성 메모리(RAM) 분석 기법의 필요성을 주지시키고 프로세스 메모리 관리 구조(PCB 및 스택)를 이해시킵니다.

## 7. 트러블슈팅 및 힌트
* **Q. Volatility 3에서 linux.envars 플러그인이 동작하지 않습니다.**
  * A. 리눅스 메모리 분석은 커널 기호 파일이 담긴 심볼 테이블 패키지가 필수적입니다. 만약 올바른 심볼 패키지를 매칭하기 어렵다면, `strings` 명령어 조합으로 메모리 이미지 전체에서 raw 탐색을 시도하는 것이 더 빠르고 직관적인 대안입니다.
* **Q. 프로세스 환경 변수는 메모리에서 언제 소멸하나요?**
  * A. 환경 변수는 해당 프로세스가 종료(Terminate)되어 OS 커널에 의해 가상 메모리 매핑이 해제되고 다른 메모리 할당 활동으로 덮어써지기 전까지는 물리 메모리 상에 여전히 잔재(Residual Data) 형태로 보존됩니다.

## 8. 학습 포인트
* **메모리 휘발성 흔적(RAM Forensics)**: 디스크에 흔적이 남지 않는 런타임 보안 변수, 커넥션 세션 키 등이 물리 메모리에 보존되는 원리와 가치를 학습합니다.
* **Volatility 프레임워크 실습**: 운영체제별 프로세스 관리 구조(Process Control Block) 및 환경 테이블을 동적으로 파싱해 해독하는 실무 메모리 조사 명령을 숙지합니다.
