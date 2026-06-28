---
title: Nginx 웹 서버 프로세스 메모리 속 환경 변수 변조 추출 (Linux nginx process memory dump)
created: 2026-06-28
updated: 2026-06-28
type: ctf-challenge
tags: [ctf, ctf-challenge, forensics, linux, memory, nginx, process-dump, strings, web-server]
confidence: high
---

# Nginx 웹 서버 프로세스 메모리 속 환경 변수 변조 추출 (Linux nginx process memory dump)

> **난이도**: 초중급  
> **소요 시간**: 25~30분  
> **참고 picoCTF 문제**: 웹 서버 가상 메모리 기밀 환경변수 카빙 (Linux nginx Memory 분석)

## 1. 배경 시나리오
사내 중요 서비스가 가동 중인 Nginx 웹 서버가 외부 악성 요청에 의해 침투된 흔적이 감지되었습니다. 공격자는 Nginx 설정 파일이나 시스템 스타트업 스크립트를 조작하여, 웹 애플리케이션 가동 세션에 특정 백도어 키 또는 기밀 자격 증명 환경 변수를 강제 주입해 기동했습니다. 침해사고 조사팀은 시스템 침투를 식별한 직후, Nginx 마스터 프로세스의 활성 가상 메모리를 덤프(Core Dump)하여 보존하는 데 성공했습니다. 수집된 이진 메모리 덤프 파일 `nginx_process_memory.dmp`를 파싱 분석하여, **웹 서버 동작 시 커널 페이지 풀에 평문으로 보존되어 흐르던 Nginx 환경 변수 영역 속의 플래그**를 구출하십시오.

## 2. 제공 파일
* `nginx_process_memory.dmp` (Nginx 웹 서비스 마스터 데몬 프로세스의 가상 메모리 공간에서 덤프한 이진 코어 덤프 파일)

## 3. 문제 목표
Nginx 등 멀티 프로세스 구조의 웹 서버 데몬이 마스터/워커 프로세스를 포크(Fork)하고 구성 설정을 해석할 때, 환경 변수 데이터가 메모리 힙 및 프로세스 환경 블록(Environment Block) 영역에 평문 상태로 일시 캐시되어 서비스되는 원리를 파악하고, 프로세스 덤프 바이너리에서 해당 평문 변수를 카빙합니다.

## 4. 의도한 풀이 흐름
1. **메모리 덤프 가독 문자열 스캔**:
   * 제공된 `nginx_process_memory.dmp` 파일에서 문자열 데이터를 수집하기 위해 `strings` 명령어를 실행하고 플래그 포맷을 검색합니다:
     ```bash
     strings nginx_process_memory.dmp | grep "picoCTF"
     ```
2. **Nginx 환경 변수 레코드 획득**:
   * 검색 결과, Nginx 프로세스가 환경 설정 파싱 및 세션 유지를 위해 메모리에 적재한 환경 블록 세그먼트 부근에서 다음과 같이 비정상 주입된 환경 변수 키값을 식별해 냅니다:
     `[NGINX_ENV] SECRET_KEY=picoCTF{nginx_proc_m3m_env_carv3d}`
3. **플래그 도출**:
   * 환경 변수 선언문 뒤에 매핑 기입되어 있던 최종 플래그 값을 획득합니다:
     `picoCTF{nginx_proc_m3m_env_carv3d}`

## 5. 정답(플래그) 규칙 및 예시
* **플래그 형식**: `picoCTF{<flag_string>}`
* **예시**: `picoCTF{nginx_proc_m3m_env_carv3d}`

## 6. 출제자 노트 & 파일 제작 가이드
* **아티팩트 제작 방법**:
  1. 테스트 리눅스 환경에 Nginx 서비스를 설치 활성화합니다.
  2. Nginx 서비스 기동 시, 다음과 같이 기밀 플래그 자격 증명이 주입된 환경변수를 설정합니다:
     `export SECRET_KEY="picoCTF{nginx_proc_m3m_env_carv3d}"`
     이후 Nginx 서비스를 구동하거나 설정 파일(`nginx.conf`) 내에 `env SECRET_KEY;` 지시자를 추가해 프로세스가 해당 변수를 가져오도록 합니다.
  3. 구동 중인 Nginx 마스터 프로세스의 PID를 획득하여 코어 덤프를 생성합니다:
     `gcore -o nginx_process_memory <nginx_master_PID>`
  4. 덤프된 바이너리 이미지 내에 위 환경변수 텍스트 라인이 평문 잔재하는지 strings 검수를 수행하고, 분석 가치가 높은 유효 힙 페이지 영역을 조절 격리하여 `nginx_process_memory.dmp` 배포 파일로 저장합니다.
* **출제 포인트**: 
  * 디스크 상의 Nginx 설정 파일이나 시스템 구동 로그가 안티 포렌식 공격에 의해 소거된 은밀한 기밀 주입 상황에 맞서, 휘발성 메모리 상에 상주 가동 중인 웹 서버 프로세스 덤프(Web Server Process Memory Forensics) 분석을 가동하여 피의자가 수행한 민감 환경변수 구문을 역추적 및 규명하는 사고 대응 기법을 학습시킵니다.

## 7. 트러블슈팅 및 힌트
* **Q. Nginx 마스터 프로세스와 워커 프로세스 중 어느 쪽을 덤프해야 환경 변수가 잘 나오나요?**
  * A. 환경 변수는 Nginx가 최초 구동될 때 마스터 프로세스가 시스템으로부터 물려받아 메모리에 적재한 뒤 하위 워커 프로세스들로 복제(Fork) 전달합니다. 따라서 두 프로세스 영역 모두에서 환경 변수가 검출될 수 있으나, 더 완벽한 초기 환경 변수 셋은 부모인 마스터 프로세스 메모리 영역을 덤프 및 타깃하는 것이 가장 안정적입니다.
* **Q. 메모리 내의 환경 변수는 서비스 재시작 후에도 복구가 가능한가요?**
  * A. 서비스가 재시작되면 기존 프로세스는 종료되고 OS가 가상 메모리 페이지를 회수합니다. 하지만 물리 RAM 상에 이전에 매핑되었던 바이트 데이터들은 다른 응용 프로그램에 의해 덮어씌워지기(Overwrite) 전까지는 비할당 공간에 고스란히 남아 있으므로, 사고 직후 물리 메모리 전체 덤프를 수행하면 여전히 카빙해 낼 확률이 높습니다.

## 8. 학습 포인트
* **웹 서버 프로세스 메모리 적재 체계**: Nginx 마스터/워커 데몬의 런타임 환경 설정 해석 및 프로세스 환경 블록(Environment Block) 적재 정책을 학습합니다.
* **프로세스 덤프 환경변수 카빙**: 설정 파일 변조 공격을 우회하기 위해, 가상 메모리 프로세스 덤프를 파싱하여 중요 평문 기밀(Environment Variables)을 복원 및 식별하는 분석 기법을 습득합니다.
