---
title: 리눅스 크론 영속성 스크립트 Base64 이중 난독화 분석 (Linux Cron Startup Script Double Base64)
created: 2026-06-28
updated: 2026-06-28
type: ctf-challenge
tags: [ctf, ctf-challenge, forensics, linux, cron, persistence, base64, double-base64, obfuscation, bash]
confidence: high
---

# 리눅스 크론 영속성 스크립트 Base64 이중 난독화 분석 (Linux Cron Startup Script Double Base64)

> **난이도**: 초급  
> **소요 시간**: 15~20분  
> **참고 picoCTF 문제**: 크론 영속성 스크립트 다중 인코딩 해독 (Linux Cron Script Double Base64 분석)

## 1. 배경 시나리오
공격자가 중요 리눅스 엔터프라이즈 서버의 자원을 상시 착취하고 C2 연결 백도어를 유지하기 위해 사용자 크론탭 스케줄에 주기 가동용 셸 스크립트 `cron_persistence.sh`를 생성 등록했습니다. 공격자는 일반적인 정적 탐지 장비(IPS, 웹 애플리케이션 방화벽, 파일시스템 스캐너 등)가 유출 도구의 도메인 이름이나 특정 파라미터 텍스트를 감지해 차단하지 못하도록, 백도어 구동 전체 명령행 코드를 **Base64 형식으로 두 번 감싸(이중 인코딩, Double Base64)** 은폐했습니다. 분석관이 회수한 난독화 스크립트 파일 `cron_persistence.sh`를 해독하여 **다중 인코딩 내장 코드로 격리 은닉되어 있던 원본 플래그**를 구출하십시오.

## 2. 제공 파일
* `cron_persistence.sh` (크론 작업에 등록되어 백그라운드 주기 실행 중이던 난독화된 셸 스크립트 파일)

## 3. 문제 목표
보안 관제 회피 수단으로 널리 사용되는 Base64 다중 인코딩 메커니즘을 파악하고, `base64 -d` 디코딩 파이프라인의 입출력 관계를 추적하여 난독화 페이로드를 정적 해독해 냅니다.

## 4. 의도한 풀이 흐름
1. **스크립트 코드 정적 관찰**:
   * 제공된 `cron_persistence.sh` 파일을 텍스트 에디터로 엽니다.
   * 파일 내부에 구현된 이중 디코딩 및 동적 실행 파이프라인 구문을 식별합니다:
     `eval $(echo "Y0dsaWJPTlVSbnRqY205dVgyUnZkV0pzWlY5aU5qUmZjR1Z5YzNsemRHVnVZMlZmWkdWamIyUmxaSDA9" | base64 -d | base64 -d)`
2. **이중 디코딩 (Double Base64 Decode) 수행**:
   * **1차 디코딩**: 인자로 제공된 헥사틱 Base64 문자열을 1회 해독합니다.
     * 대상: `Y0dsaWJPTlVSbnRqY205dVgyUnZkV0pzWlY5aU5qUmZjR1Z5YzNsemRHVnVZMlZmWkdWamIyUmxaSDA9`
     * 1차 결과: `cGljb0NURntjcm9uX2RvdWJsZV9iNjRfcGVyc2lzdGVuY2VfZGVjb2RlZH0=`
     *(주의: 디코딩 결과 끝부분에 패딩 문자 `=`가 유지되어 여전히 Base64 포맷임을 인지해야 합니다)*
   * **2차 디코딩**: 1차 결과물인 `cGljb0NURntjcm9uX2RvdWJsZV9iNjRfcGVyc2lzdGVuY2VfZGVjb2RlZH0=`를 다시 한번 Base64 해독합니다.
     * 2차 결과: `picoCTF{cron_double_b64_persistence_decoded}`
3. **플래그 도출**:
   * 디코딩이 정상 완료되어 도출된 문자열을 통해 최종 플래그를 정립합니다:
     `picoCTF{cron_double_b64_persistence_decoded}`

## 5. 정답(플래그) 규칙 및 예시
* **플래그 형식**: `picoCTF{<flag_string>}`
* **예시**: `picoCTF{cron_double_b64_persistence_decoded}`

## 6. 출제자 노트 & 파일 제작 가이드
* **아티팩트 제작 방법**:
  1. 기밀 플래그 명령어 구문 `picoCTF{cron_double_b64_persistence_decoded}`를 Base64로 1차 인코딩합니다:
     `echo -n "picoCTF{cron_double_b64_persistence_decoded}" | base64`
     -> `cGljb0NURntjcm9uX2RvdWJsZV9iNjRfcGVyc2lzdGVuY2VfZGVjb2RlZH0=`
  2. 얻은 결과물을 다시 한번 Base64로 2차 인코딩합니다:
     `echo -n "cGljb0NURntjcm9uX2RvdWJsZV9iNjRfcGVyc2lzdGVuY2VfZGVjb2RlZH0=" | base64`
     -> `Y0dsaWJPTlVSbnRqY205dVgyUnZkV0pzWlY5aU5qUmZjR1Z5YzNsemRHVnVZMlZmWkdWamIyUmxaSDA9`
  3. 이 최종 2차 인코딩 스트림을 사용해 `eval $(echo "<2차_결과>" | base64 -d | base64 -d)` 형식의 셸 구문을 생성합니다.
  4. 이를 `cron_persistence.sh` 파일로 최종 저장하여 수검용 아티팩트로 포장 배포합니다.
* **출제 포인트**: 
  * 리눅스 백그라운드 영속성(Cron System Auditing) 조사 과정에서, 파일 시스템 감사 도구의 단순 문자열 패턴 매칭 검출 필터(Keyword Matching)를 회피하기 위해 공격자들이 흔히 시도하는 다중 기저 대역 인코딩 우회술을 직시하고, 이를 안전하게 복원 디코딩하여 위협 인자를 규명하는 핵심 기본기를 훈련시킵니다.

## 7. 트러블슈팅 및 힌트
* **Q. 왜 공격자들은 단일 인코딩 대신 이중 인코딩을 적용하나요?**
  * A. 보안 스캔 솔루션들 중 일부는 침해 흔적 스캔 시 Base64 시그니처 단일 디코딩 엔진을 정적으로 연동 내장하여 검사를 돌립니다. 이 경우 `picoCTF`나 악성 C2 도메인 정보가 1회 Base64 인코딩된 스트림은 정적 진단 룰에 쉽게 포착되나, `base64(base64(malicious))` 형태로 이중 래핑해 버리면 1회 디코딩만으로는 여전히 무작위 Base64 문자열로만 나타나 정적 검출 필터를 손쉽게 우회할 수 있어 실제 위협 현장에서 상습 차용되는 패턴입니다.
* **Q. base64 디코딩 시 "invalid input" 에러가 뜨며 복구가 중단됩니다.**
  * A. 문자열 중간 혹은 끝부분에 포함되어야 하는 패딩용 `=` 기호가 복사 과정에서 임의 유실되었거나, 개행 문자(`\n`, `\r`) 등의 비인쇄 바이트가 삽입되어 디코더가 입력을 처리하지 못하고 튕겼을 가능성이 높습니다. 복제 추출 시 공백과 뉴라인을 완전히 다듬어 처리해야 정상 디코딩이 성립합니다.

## 8. 학습 포인트
* **Base64 인코딩/디코딩 스펙**: 3바이트 데이터를 4바이트 6비트 색인 문자로 매핑 변환하는 수학적 원리 및 패딩 규격을 심화 학습합니다.
* **난독화 명령어 정적 해독**: `eval` 구문에 의해 런타임 가동되기 전, 수작업 파이프라인 디코딩 연산을 통해 악성 페이로드의 무결성을 정적으로 안전히 검출 및 분석하는 노하우를 갖춥니다.
