---
title: 리눅스 인증 백도어 탐지 (Linux PAM Backdoor Analysis)
created: 2026-06-28
updated: 2026-06-28
type: ctf-challenge
tags: [ctf, ctf-challenge, forensics, linux, pam, backdoor, shared-library, strings]
confidence: high
---

# 리눅스 인증 백도어 탐지 (Linux PAM Backdoor Analysis)

> **난이도**: 초중급  
> **소요 시간**: 20~25분  
> **참고 picoCTF 문제**: 리눅스 공유 라이브러리 검증 및 리버스 엔지니어링 (SSHD PAM 백도어 추적)

## 1. 배경 시나리오
사내 자산 관리 리눅스 서버에 비인가 사용자가 기존 계정의 비밀번호를 모르는데도 원격 SSH 세션을 수월하게 열어 로그인하는 비정상 침입 정황이 보고되었습니다. 보안 조사팀은 침입자가 시스템의 인증 게이트웨이 라이브러리인 **PAM(Pluggable Authentication Modules)** 파일을 변조해 놓은 것으로 의심하고 있습니다. 보안 시스템에서 적출한 의심스러운 인증 모듈 파일 `pam_unix.so`와 정상 원본 패키지 파일 `pam_unix_original.so`를 획득했습니다. 이 공유 라이브러리를 비교 분석하여 **공격자가 로그인을 우회하기 위해 하드코딩해 둔 마스터 패스워드(플래그)**를 도출하십시오.

## 2. 제공 파일
* `pam_unix.so` (침해 서버의 보안 모듈 디렉터리에서 획득한 의심스러운 PAM 라이브러리 파일)
* `pam_unix_original.so` (우분투 공식 패키지 검증 서버에서 확인된 깨끗한 원본 PAM 라이브러리 파일)

## 3. 문제 목표
리눅스의 다중 인증 관리 체계인 PAM의 기본 메커니즘을 이해하고, 정적 파일 분석 유틸리티(`file`, `sha256sum`, `strings`, `diff`) 또는 간단한 역공학 도구(Ghidra, objdump)를 활용하여 변조된 라이브러리 내에 고의로 추가 주입된 마스터 계정 검증 문자열을 색인해 냅니다.

## 4. 의도한 풀이 흐름
1. **무결성 훼손 진단 (Hash 비교)**:
   * 두 파일의 무결성을 검증하기 위해 터미널에서 SHA-256 해시 연산을 돌립니다:
     ```bash
     sha256sum pam_unix.so pam_unix_original.so
     ```
   * 두 라이브러리 파일의 해시값이 일치하지 않음을 식별하고, 침해 서버의 파일이 인위적으로 컴파일 변조되었음을 판정합니다.
2. **정적 문자열 분석 (Strings 스캔)**:
   * 라이브러리 바이너리에 삽입된 가독 가능 문자열 리스트를 추출하고 비교합니다:
     ```bash
     strings pam_unix.so > suspect_strings.txt
     strings pam_unix_original.so > original_strings.txt
     diff suspect_strings.txt original_strings.txt
     ```
   * 원본에는 존재하지 않는, 변조본(`pam_unix.so`)에만 하드코딩되어 나타나는 비정상적인 문자열을 식별합니다.
3. **백도어 논리 판별**:
   * `suspect_strings.txt` 내에서 다음과 같이 괄호 형태를 띠고 있는 키워드를 검출합니다:
     `picoCTF{p4m_b4ckd00r_m4st3r_pass}`
   * *주: 실제 백도어는 로그인 비밀번호 검증 함수 `pam_sm_authenticate` 내에 `strcmp(input_password, "마스터암호") == 0` 조건을 수동 추가하는 방식으로 제작됩니다.*
4. **플래그 도출**:
   * 획득한 마스터 비밀번호 문자열을 플래그로 획득합니다:
     `picoCTF{p4m_b4ckd00r_m4st3r_pass}`

## 5. 정답(플래그) 규칙 및 예시
* **플래그 형식**: `picoCTF{<flag_string>}`
* **예시**: `picoCTF{p4m_b4ckd00r_m4st3r_pass}`

## 6. 출제자 노트 & 파일 제작 가이드
* **아티팩트 제작 방법**:
  1. 우분투 PAM 소스코드(`pam_unix_auth.c`)를 다운로드합니다.
  2. 인증 수행 함수인 `pam_sm_authenticate` 코드 내부에 마스터 백도어 비교 구문을 주입합니다:
     ```c
     if (strcmp(retval, "picoCTF{p4m_b4ckd00r_m4st3r_pass}") == 0) {
         return PAM_SUCCESS;
     }
     ```
  3. 대상 환경의 아키텍처에 맞게 라이브러리를 크로스 컴파일하여 `pam_unix.so`를 빌드합니다.
  4. 컴파일 시점의 디버그 심볼이 삭제되더라도 `strings`로 문자열이 보존되는지 검수하고, 정상 원본 라이브러리와 함께 배포 아티팩트로 지정합니다.
* **출제 포인트**: 
  * 리눅스 권한 우회 및 유지(Persistence) 기법의 핵심 타깃인 PAM 모듈 가로채기(PAM Hijacking) 패턴을 이해하고, 파일 무결성 감사(`debsums` 등의 원리)를 실행하여 비정상 공유 라이브러리를 가려내는 능력을 함양합니다.

## 7. 트러블슈팅 및 힌트
* **Q. debsums 도구를 사용하면 실제로 이 변조를 탐지할 수 있나요?**
  * A. 네, 데비안/우분투 계열에서는 `debsums -c` 명령어를 가동하면 시스템 내에 수동 변경된 모든 바이너리 파일 목록이 패키지 원본 해시(MD5sums 이력)와 불일치하는 상태로 즉시 화면에 경고 출력되어 탐지가 가능합니다.
* **Q. Ghidra 디컴파일러 상에서 코드를 쉽게 짚으려면 어떻게 해야 하나요?**
  * A. `pam_sm_authenticate` 함수명을 검색하여 코드를 엽니다. 사용자 입력 패스워드 포인터 변수가 비교 연산 함수(`strcmp` 등)를 거치는 타깃 조건 분기문으로 들어가 하드코딩된 특정 버퍼와 매핑되는 구간을 추적하면 백도어 값을 바로 특정할 수 있습니다.

## 8. 학습 포인트
* **PAM 인증 아키텍처**: 리눅스 내부 계정 관리, SSH 로그인, sudo 인증 과정을 추상화하여 중적 제어하는 PAM 프레임워크 플러그인 로딩 원리를 마스터합니다.
* **공유 라이브러리 감사**: 시스템 바이너리 파일의 SHA256 해시 검증 및 strings 차분 분석을 활용하여, 무단 컴파일 주입된 악성 모듈의 증적을 발굴해 내는 능력을 훈련합니다.
