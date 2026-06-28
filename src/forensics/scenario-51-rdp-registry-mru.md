---
title: 윈도우 원격 데스크톱 연결 기록 (RDP MRU Registry Analysis)
created: 2026-06-28
updated: 2026-06-28
type: ctf-challenge
tags: [ctf, ctf-challenge, forensics, windows, registry, rdp, ntuser, mru]
confidence: high
---

# 윈도우 원격 데스크톱 연결 기록 (RDP MRU Registry Analysis)

> **난이도**: 초급  
> **소요 시간**: 15~20분  
> **참고 picoCTF 문제**: 윈도우 원격 연결 흔적 조사 (RDP MRU 레지스트리 포렌식)

## 1. 배경 시나리오
사내 중요 보안망 서버에 특정 내부 임직원의 계정을 도용한 원격 데스크톱(RDP) 비인가 연결 흔적이 식별되었습니다. 용의자는 해당 서버에 원격 접속한 사실이 없으며 RDP 클라이언트 프로그램을 켠 적도 없다고 진술하고 있습니다. 하지만 윈도우 운영체제는 사용자가 원격 데스크톱 연결(mstsc.exe)을 수행할 때, 대상 목적지 IP 주소와 연결 도중 기입했던 사용자 힌트(Username Hint) 데이터를 사용자 개별 레지스트리 하이브 파일(`NTUSER.dat`)에 기록하여 보존합니다. 피의자 PC에서 추출한 RDP 관련 레지스트리 덤프 파일 `ntuser_rdp.reg`를 분석하여 **가장 최근에 연결을 시도했던 대상 서버의 사용자 힌트 내에 들어 있는 플래그**를 획득하십시오.

## 2. 제공 파일
* `ntuser_rdp.reg` (피의자 PC의 `NTUSER.dat` 레지스트리 중 Terminal Server Client 하위 키를 내보낸 레지스트리 텍스트 파일)

## 3. 문제 목표
윈도우 레지스트리 내에서 RDP(원격 데스크톱) 클라이언트 구동 이력이 기록되는 경로(`Terminal Server Client\Default` 및 `Servers` 키)의 특성을 이해하고, 최근 연결 순서(MRU)와 연결 매개변수(UsernameHint)를 해독해 플래그를 찾아냅니다.

## 4. 의도한 풀이 흐름
1. **레지스트리 덤프 구조 검사**:
   * 제공된 `ntuser_rdp.reg` 텍스트 파일을 엽니다.
   * 윈도우에서 RDP 연결 목적지 목록은 아래 레지스트리 경로에 저장됩니다:
     `[HKEY_CURRENT_USER\Software\Microsoft\Terminal Server Client\Default]`
   * 또한 각 서버별 상세 설정 및 사용자 계정 힌트는 아래 하위 경로에 저장됩니다:
     `[HKEY_CURRENT_USER\Software\Microsoft\Terminal Server Client\Servers\<IP_Address>]`
2. **최근 접속 목록 분석 (Default 키 조회)**:
   * `Terminal Server Client\Default` 키의 값을 검사합니다:
     * `MRU0` (가장 최근 접속한 서버)의 데이터 값이 `10.0.0.105` 임을 파악합니다.
     * `MRU1` 의 값은 `192.168.1.50` 등 과거 다른 대역이 등록되어 있습니다.
3. **사용자 계정 힌트 추적 (Servers 하위 키 대조)**:
   * 가장 최근에 접속한 대상 IP `10.0.0.105` 관련 상세 설정을 보기 위해 아래 키를 조회합니다:
     `[HKEY_CURRENT_USER\Software\Microsoft\Terminal Server Client\Servers\10.0.0.105]`
   * 해당 키 아래에 기록된 문자열 속성값 중 **UsernameHint** 데이터 값을 획득합니다:
     `"UsernameHint"="picoCTF{rdp_mru_reg_history_extracted}"`
4. **최종 플래그 도출**:
   * UsernameHint 값에 기술되어 있던 플래그 문자열을 추출합니다:
     `picoCTF{rdp_mru_reg_history_extracted}`

## 5. 정답(플래그) 규칙 및 예시
* **플래그 형식**: `picoCTF{<flag_string>}`
* **예시**: `picoCTF{rdp_mru_reg_history_extracted}`

## 6. 출제자 노트 & 파일 제작 가이드
* **아티팩트 제작 방법**:
  1. Windows 10/11 가상 머신에서 원격 데스크톱 연결(`mstsc.exe`)을 실행합니다.
  2. 컴퓨터 입력창에 IP `10.0.0.105`를 입력하고, 사용자 이름 필드에 기밀 플래그 `picoCTF{rdp_mru_reg_history_extracted}`를 타이핑한 뒤 연결 버튼을 누릅니다. (자격증명 입력 단계에서 창을 닫아도 레지스트리에 영구 기록됩니다)
  3. 레지스트리 편집기(`regedit`)를 띄워 아래 경로로 이동합니다:
     `HKCU\Software\Microsoft\Terminal Server Client`
  4. 해당 키를 우클릭하여 `ntuser_rdp.reg` 텍스트 파일 형식으로 내보내기(Export)를 진행하고, 이를 챌린지 배포 아티팩트로 사용합니다.
* **출제 포인트**: 
  * 윈도우 OS의 대표적 네트워크 횡적 이동(Lateral Movement) 아티팩트인 RDP 실행 이력을 추적하여, 용의자가 인프라 내에서 다른 호스트로 접근을 시도한 타깃 시스템의 위치와 계정명을 재구성해 내는 기본 포렌식 기법을 습득시킵니다.

## 7. 트러블슈팅 및 힌트
* **Q. MRU 번호의 순서는 어떻게 결정되나요?**
  * A. 윈도우 레지스트리에서 MRU(Most Recently Used) 목록은 번호가 낮을수록(일반적으로 `MRU0`) 가장 최근에 수행된 실행 활동을 의미하며, 새로운 연결이 생길 때마다 밀려나며 인덱스가 재정렬됩니다.
* **Q. RDP로 접속할 때 입력한 비밀번호도 레지스트리에 저장되나요?**
  * A. 아닙니다. 윈도우는 RDP 자격증명을 로컬 자격증명 관리자(Credential Manager)에 보안 위임하거나 해싱하므로 레지스트리 상에는 단순 유저 ID 힌트(`UsernameHint`)만 평문 기록되고 패스워드는 직접적으로 저장되지 않습니다.

## 8. 학습 포인트
* **윈도우 RDP 흔적 포렌식**: 원격 데스크톱 클라이언트 동작에 따른 접속 대상 시스템 IP/도메인 목록 및 로그인 사용자 ID 힌트의 저장 정책을 학습합니다.
* **사용자 레지스트리(NTUSER.dat) 구조**: 개별 사용자 컨텍스트 환경(HKCU) 하위의 네트워크 애플리케이션 MRU 데이터 직렬화 포맷을 이해합니다.
