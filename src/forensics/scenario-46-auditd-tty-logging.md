---
title: 리눅스 오딧디 로그 기반 계정 도용 추적 (Linux Auditd TTY logs)
created: 2026-06-28
updated: 2026-06-28
type: ctf-challenge
tags: [ctf, ctf-challenge, forensics, linux, auditd, tty-logging, keylogger, hex-decode]
confidence: high
---

# 리눅스 오딧디 로그 기반 계정 도용 추적 (Linux Auditd TTY logs)

> **난이도**: 초급  
> **소요 시간**: 15~20분  
> **참고 picoCTF 문제**: 사용자 원시 터미널 입력 복구 및 감사 (Auditd TTY Keylogger 분석)

## 1. 배경 시나리오
보안 위협 팀은 사내 중요 서버에서 일반 세션 내 권한 상승(`sudo -s`) 후 원격 명령이 실행된 정황을 탐지하고 추적을 개시했습니다. 용의자는 실행 후 터미널 창을 강제로 닫거나 관련 스크립트를 즉시 삭제해 흔적을 지웠으나, 해당 서버에는 커널 감사 시스템인 **auditd의 TTY 모니터링 모듈(pam_tty_audit.so)**이 연계 활성화되어 있어 사용자가 키보드로 타이핑한 원시 입력(Raw keystroke) 데이터가 고스란히 감사 로그에 기록되어 있었습니다. 수집한 감사 로그 `tty_audit.log` 파일 내의 `type=TTY` 레코드를 파싱하고, **공격자가 터미널 상에 직접 기입했던 기밀 플래그 문자열**을 복원하십시오.

## 2. 제공 파일
* `tty_audit.log` (사용자 셸 입력 기록이 수록된 auditd TTY 감사 로그 파일)

## 3. 문제 목표
리눅스 감사 정책 중 pam_tty_audit이 동작하여 사용자 키 입력을 기록하는 메커니즘을 이해하고, 로그 데이터 필드 내에 16진수(Hex) 인코딩으로 박제된 터미널 키 스트로크 데이터를 아스키 평문 텍스트로 환원하는 해독 능력을 갖춥니다.

## 4. 의도한 풀이 흐름
1. **TTY 감사 레코드 확인**:
   * 제공된 `tty_audit.log` 파일에서 사용자 단말 입력을 캡처하는 `type=TTY` 관련 이벤트를 필터링합니다:
     ```bash
     grep "type=TTY" tty_audit.log
     ```
2. **원시 데이터 필드 분석**:
   * 필터링 결과 다음과 같이 `data` 필드 내에 16진수 바이트열이 매핑된 엔트리를 발견합니다:
     `type=TTY msg=audit(1719543822.428:1024): tty ses=3 comm="bash" data=7069636F4354467B7474795F61756469745F6B65796C6F676765725F7265636F76657265647D0D`
3. **16진수 디코딩**:
   * `data` 필드의 헥스 스트링(`7069636F4354467B7474795F61756469745F6B65796C6F676765725F7265636F76657265647D0D`)을 아스키 문자열로 변환합니다.
   * **Python 스크립트 실행**:
     ```python
     hex_data = "7069636F4354467B7474795F61756469745F6B65796C6F676765725F7265636F76657265647D0D"
     print(bytes.fromhex(hex_data).decode('utf-8'))
     ```
   * **xxd/xxd 복구 유틸리티 실행**:
     `echo "7069636F4354467B7474795F61756469745F6B65796C6F676765725F7265636F76657265647D0D" | xxd -r -p`
4. **결과 확인 및 플래그 획득**:
   * 디코딩 결과 다음 문자열이 수립됨을 확인합니다:
     `picoCTF{tty_audit_keylogger_recovered}\r`
     *(주: 끝의 `0D` 바이트는 엔터키에 매핑되는 Carriage Return(\r)을 뜻합니다)*
   * 최종 플래그를 정립해 입력합니다:
     `picoCTF{tty_audit_keylogger_recovered}`

## 5. 정답(플래그) 규칙 및 예시
* **플래그 형식**: `picoCTF{<flag_string>}`
* **예시**: `picoCTF{tty_audit_keylogger_recovered}`

## 6. 출제자 노트 & 파일 제작 가이드
* **아티팩트 제작 방법**:
  1. 리눅스 가상 머신의 `/etc/pam.d/common-session` 설정 하단에 TTY 감시 PAM 설정을 추가합니다:
     `session required pam_tty_audit.so enable=*`
  2. 일반 사용자 계정으로 로그인한 상태에서 셸 프롬프트에 플래그 키를 타이핑합니다:
     `picoCTF{tty_audit_keylogger_recovered}` 후 엔터 입력.
  3. 관리자 권한으로 `/var/log/audit/audit.log` 내에서 방금 구동된 TTY 입력 이벤트(`data=...`)를 확인 및 덤프합니다.
  4. 덤프된 TTY 로그 라인 수십 줄을 포장하여 아티팩트 `tty_audit.log`로 정해 배포합니다.
* **출제 포인트**: 
  * 사용자가 터미널 상에 입력한 명령어는 `.bash_history`나 일반 프로세스 감사를 지워도 커널 수준의 TTY 입출력 모니터링 로그(Keystroke Logging)에 원시 바이트 상태로 영구 적재될 수 있음을 확인하고, Hex 디코딩 분석법을 적용하게 합니다.

## 7. 트러블슈팅 및 힌트
* **Q. data 필드의 데이터 중 7f 또는 08 같은 특수 바이트는 무엇인가요?**
  * A. 사용자가 터미널 상에서 오타를 쳐서 백스페이스(Backspace) 키를 입력한 흔적입니다. 헥스 디코딩 시 백스페이스 바이트(`0x7F` 또는 `0x08`)가 나오면 그 앞의 문자가 논리적으로 지워진 것이므로, 전체 문자열 조립 시 오타 수정 흐름을 감안하여 정상 문자를 재조합해야 합니다.
* **Q. aureport 도구를 사용해 이를 편하게 볼 수는 없나요?**
  * A. 네, auditd 툴킷의 보고서 생성 유틸리티인 `aureport --tty` 명령어를 가동하면 수동 헥스 변환 없이 시스템 내에서 현재까지 입력된 모든 사용자의 타이핑 텍스트가 줄바꿈 정렬된 평문 형태로 즉시 재구성되어 출력됩니다.

## 8. 학습 포인트
* **PAM TTY 감사 기술(TTY Auditing)**: 시스템 운영 중 명령어 이력 우회나 안티 포렌식 위협에 대비해 사용자 키 스트로크를 가로채 커널 보안 이벤트로 로깅하는 원리를 배웁니다.
* **Keystroke 포렌식 분석**: 수집된 입력 헥스 흐름(Keystroke hex stream)에서 특수 제어 코드(Carriage return, Backspace 등)를 해석 및 정제하여 최종 완성된 텍스트 데이터를 해독해 내는 기법을 습득합니다.
