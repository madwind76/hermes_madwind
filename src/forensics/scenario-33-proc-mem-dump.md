---
title: 리눅스 프로세스 메모리 덤프 분석 (Linux /proc PID Core Dump)
created: 2026-06-28
updated: 2026-06-28
type: ctf-challenge
tags: [ctf, ctf-challenge, forensics, linux, memory, process-memory, core-dump, gcore]
confidence: high
---

# 리눅스 프로세스 메모리 덤프 분석 (Linux /proc PID Core Dump)

> **난이도**: 초중급  
> **소요 시간**: 25~30분  
> **참고 picoCTF 문제**: 프로세스 레벨 메모리 포렌식 및 스트링 카빙 (Linux core dump 분석)

## 1. 배경 시나리오
사내 리눅스 웹 서버에 백그라운드로 실행되던 악성 C2 연결 데몬 프로세스를 식별하고 강제 종료하기 직전, 침해사고 조사팀은 해당 프로세스의 가상 가상 가상 메모리 적재 상태를 보존하기 위해 코어 덤프 파일 `core.5821`과 메모리 매핑 구조 기록 파일 `maps.5821`을 확보했습니다. 공격자는 실행 파일 바이너리는 종료 시 자가 삭제하도록 설계했으나, 통신 세션을 유지하기 위해 런타임 메모리(Heap 영역) 상에 조립해 두었던 JSON 요청 프레임과 로그인 인증 토큰은 메모리에 평문 상태로 잔재해 있을 가능성이 매우 큽니다. 프로세스 메모리 덤프를 분석해 은닉된 토큰(플래그)을 복구하십시오.

## 2. 제공 파일
* `core.5821` (가상 메모리 전체가 덤프된 리눅스 프로세스 코어 덤프 파일)
* `maps.5821` (덤프 당시 가상 메모리 영역의 세그먼트 매핑 정보를 담은 텍스트 파일)

## 3. 문제 목표
리눅스의 프로세스 가상 메모리 관리 모델 및 `/proc/<PID>/` 아티팩트 구조를 이해하고, 코어 덤프 바이너리에서 문자열을 추출 및 필터링하여 공격자가 사용한 기밀 매개변수(Base64 인코딩 토큰)를 카빙해 해독합니다.

## 4. 의도한 풀이 흐름
1. **가상 메모리 맵 분석**:
   * 제공된 `maps.5821`을 텍스트 뷰어로 열어 프로세스의 메모리 세그먼트 배치를 확인합니다.
   * `[heap]` 또는 `[stack]` 영역의 가상 주소 범위를 조회해 둡니다:
     `00fa2000-00fc3000 rwb 00000000 00:00 0 [heap]`
2. **코어 덤프 바이너리 탐색**:
   * `core.5821` 파일은 ELF 포맷의 코어 파일 구조를 취하고 있습니다.
   * `strings` 명령어 및 정규식 필터링을 사용하여 덤프 내부에 잔재하는 기밀 문자열 패턴을 고속 수동 카빙합니다:
     ```bash
     strings core.5821 | grep -i "session_token"
     ```
   * 혹은 JSON 데이터 구조를 탐색합니다:
     ```bash
     strings core.5821 | grep -E "\{\".*\"\}"
     ```
3. **인코딩된 페이로드 검출**:
   * 탐색 중 메모리 힙 영역 부근에서 다음과 같은 구조의 공격자 C2 통신 JSON 패킷 데이터를 식별합니다:
     `{"auth": "admin", "session_token": "cGljb0NURntwcm9jX21lbV9kdW1wX2Fzc2VtYmxlZH0="}`
4. **Base64 복호화**:
   * `session_token` 값으로 명시된 Base64 문자열(`cGljb0NURntwcm9jX21lbV9kdW1wX2Fzc2VtYmxlZH0=`)을 복호화합니다:
     `echo "cGljb0NURntwcm9jX21lbV9kdW1wX2Fzc2VtYmxlZH0=" | base64 -d`
5. **최종 플래그 확보**: 복호화 결과 출력된 플래그를 확인합니다.
   (최종 플래그: `picoCTF{proc_mem_dump_assembled}`)

## 5. 정답(플래그) 규칙 및 예시
* **플래그 형식**: `picoCTF{<flag_string>}`
* **예시**: `picoCTF{proc_mem_dump_assembled}`

## 6. 출제자 노트 & 파일 제작 가이드
* **아티팩트 제작 방법**:
  1. 기밀 JSON 세션을 실시간 유지하는 파이썬 스크립트 `c2_daemon.py`를 작성합니다:
     ```python
     import time
     import json
     # 메모리 힙 영역에 계속 상주하도록 전역 변수 선언
     session_data = {
         "auth": "admin",
         "session_token": "cGljb0NURntwcm9jX21lbV9kdW1wX2Fzc2VtYmxlZH0="
     }
     while True:
         time.sleep(1)
     ```
  2. 스크립트를 기동합니다: `python3 c2_daemon.py &` (PID 확인: 5821)
  3. 리눅스 `gcore` 유틸리티를 사용하여 구동 중인 프로세스의 코어 덤프를 생성합니다:
     `gcore -o core 5821` (결과 파일 `core.5821` 획득)
  4. `/proc/5821/maps` 파일의 덤프 당시 시점 내용을 `maps.5821`로 복제하여 한데 모아 배포합니다.
* **출제 포인트**: 
  * 전체 물리 휘발성 메모리(RAM)를 이미징하는 작업 대비, 단일 의심 프로세스만을 표적으로 하여 빠르게 가상 메모리 공간을 덤프해 흔적을 발굴하는 저수준 리눅스 포렌식 역량을 배양합니다.

## 7. 트러블슈팅 및 힌트
* **Q. strings 실행 시 메모리가 너무 쪼개져서 한 줄의 완전한 JSON으로 추출되지 않습니다.**
  * A. 파이썬 가상 머신(VM)이나 다른 런타임 메모리 특성상 데이터가 불연속 페이징되어 있을 수 있습니다. 주소 매핑 정보 `maps.5821`을 참고하여 `dd` 명령어로 힙 영역 전체를 오프셋 슬라이싱하고 `iconv` 또는 정형식 카빙 스크립트를 돌려 메모리를 재조립해야 가독 가능한 텍스트 덤프를 완성할 수 있습니다.
* **Q. core dump 파일의 포맷은 어떻게 식별하나요?**
  * A. 리눅스 코어 덤프는 커널에서 프로세스 비정상 종결이나 요청 시 생성되는 디버깅 데이터로, `file core.5821` 명령을 치면 `ELF 64-bit LSB core file`과 같이 ELF 코어 명세 규격으로 정확히 검출됩니다.

## 8. 학습 포인트
* **리눅스 가상 메모리 모델**: 프로세스 실행 시 커널이 할당하는 가상 주소 공간(Virtual Address Space) 내 Stack, Heap, Text, Data 세그먼트의 역할과 메모리 적재 매커니즘을 상세히 이해합니다.
* **프로세스 메모리 덤프 (Core Dump)**: 휘발성 프로세스 활성 상태 증거를 박제하는 gcore 등의 메모리 카빙 도구 사용법과, strings 패턴 매칭을 이용한 고속 민감 데이터 스캐닝 기술을 습득합니다.
