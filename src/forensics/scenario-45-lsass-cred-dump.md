---
title: 윈도우 암호 자격증명 메모리 분석 (LSASS Process Memory dump)
created: 2026-06-28
updated: 2026-06-28
type: ctf-challenge
tags: [ctf, ctf-challenge, forensics, windows, memory, lsass, mimikatz, credential-dumping, pypykatz]
confidence: high
---

# 윈도우 암호 자격증명 메모리 분석 (LSASS Process Memory dump)

> **난이도**: 초중급  
> **소요 시간**: 25~30분  
> **참고 picoCTF 문제**: 윈도우 메모리 자격증명 추출 및 해독 (LSASS Minidump 분석)

## 1. 배경 시나리오
사내 도메인 제어 서버에 비정상적인 계정 로그인(무차별 대입 및 자격증명 횡적 이동) 사고가 발생했습니다. 조사 결과 공격자는 서버 내부 메모리를 긁어 관리자 비밀번호를 덤프하는 **크레덴셜 덤핑(Credential Dumping)** 도구를 가동한 것으로 의심됩니다. 침해 대응팀은 침투 흔적 박제를 위해 윈도우의 로컬 인증 서브시스템 서비스 프로세스인 `lsass.exe`의 실행 가상 메모리 스냅샷인 `lsass.dmp` 파일을 긴급 확보했습니다. 이 메모리 덤프 파일을 분석하여 **메모리 내부(WDigest 또는 Kerberos 인증 구조체)에 평문 상태로 잔재해 있던 계정 비밀번호(플래그)**를 추출하십시오.

## 2. 제공 파일
* `lsass.dmp` (윈도우 LSASS 프로세스 메모리 미니덤프 파일)

## 3. 문제 목표
윈도우의 로컬 자격증명 보존 데몬인 LSASS(Local Security Authority Subsystem Service)의 보안 역할과 메모리 구조를 이해하고, 자격증명 해독기(pypykatz, mimikatz 등)를 활용하여 메모리 덤프 내부의 난독화된 WDigest/Kerberos 데이터 패키지를 풀어서 평문 비밀번호를 도출합니다.

## 4. 의도한 풀이 흐름
1. **분석 도구 준비**:
   * 제공된 파일은 윈도우 특정 프로세스의 메모리 스냅샷인 Minidump 포맷입니다.
   * **Linux/Python 환경 (권장)**: 플랫폼 독립적인 미미카츠(Mimikatz) 클론 파이썬 라이브러리인 `pypykatz`를 사용합니다.
     `pip install pypykatz` (설정 완료 상태)
   * **Windows 환경**: 표준 `mimikatz.exe`를 사용하여 덤프 분석 명령을 가동합니다.
2. **LSASS 덤프 해독 실행**:
   * **pypykatz 실행**:
     ```bash
     pypykatz lsa minidump lsass.dmp
     ```
   * **mimikatz 실행**:
     미미카츠 콘솔을 열고 덤프 파일을 지정해 자격증명을 추출합니다:
     ```cmd
     sekurlsa::minidump lsass.dmp
     sekurlsa::logonpasswords
     ```
3. **자격증명 결과 리포트 검사**:
   * 분석 결과 도출된 로그인 세션 중 `msv`, `wdigest`, `kerberos` 등의 하부 서비스 프로토콜 탭을 검사합니다.
   * 사용자 계정명이 `flag_holder` 또는 `Administrator`인 레코드를 대조하여, 평문 패스워드(`Password`) 필드 영역에 기록되어 노출된 문자열을 확인합니다:
     ```text
     User: flag_holder
     Password: picoCTF{ls4ss_dump_creds_r3vealed}
     ```
4. **플래그 입력**:
   * 평문으로 확인된 암호 문자열을 최종 플래그로 제출합니다:
     `picoCTF{ls4ss_dump_creds_r3vealed}`

## 5. 정답(플래그) 규칙 및 예시
* **플래그 형식**: `picoCTF{<flag_string>}`
* **예시**: `picoCTF{ls4ss_dump_creds_r3vealed}`

## 6. 출제자 노트 & 파일 제작 가이드
* **아티팩트 제작 방법**:
  1. Windows 10 또는 Windows Server 가상 머신에서 자격증명 공급자 보안 설정을 일시 조정합니다:
     * 레지스트리 `HKLM\System\CurrentControlSet\Control\SecurityProviders\WDigest` 하위에 `UseLogonCredential` (DWORD) 값을 `1`로 설정하여 강제로 평문 패스워드가 메모리에 남아있도록 허용합니다. (Windows 8.1 / Server 2012 R2 이상 시스템용)
  2. 시스템에 `flag_holder` 계정으로 로그인한 상태로 가상 머신을 켜 둡니다. (비밀번호: `picoCTF{ls4ss_dump_creds_r3vealed}`)
  3. 작업 관리자를 실행해 `lsass.exe` 프로세스를 마우스 우클릭하여 "덤프 파일 만들기"를 누르거나, Sysinternals의 `procdump`를 돌려 덤프를 획득합니다:
     `procdump.exe -ma lsass.exe lsass.dmp`
  4. 획득한 `lsass.dmp` 파일을 배포 아티팩트로 확정합니다.
* **출제 포인트**: 
  * 액티브 디렉터리(AD) 및 윈도우 인프라 침투 시 공격자들의 필수 침투 벡터가 되는 로컬 자격증명 탈취(Credential Dumping) 수법과 덤프 흔적 해독 프로세스를 이해시킵니다.

## 7. 트러블슈팅 및 힌트
* **Q. pypykatz 실행 시 'struct.error: unpack requires a buffer of 8 bytes' 등의 디코딩 에러가 발생합니다.**
  * A. 덤프를 생성한 Windows 버전과 파싱하는 도구(pypykatz)의 패키지 파서 정보 빌드가 맞지 않을 때 내부 구조체 매핑 한계로 인해 파싱 도중 에러가 날 수 있습니다. 이럴 때는 최신 pypykatz로 업데이트하거나, 대상 윈도우 버전과 동일한 아키텍처(x64)를 지닌 Windows 가상머신 내에 `mimikatz.exe`를 설치하여 분석 세션을 재시도해야 합니다.
* **Q. 최근 윈도우 버전에서는 LSASS 메모리를 덤프해도 평문 패스워드가 나오지 않는 이유가 무엇인가요?**
  * A. Windows 8.1/10 이후부터는 기본 설정으로 메모리에 계정 비밀번호 평문을 적재하지 않도록 차단(UseLogonCredential=0)하며, LSA 보호(LSA Protection) 및 Credential Guard 등의 하이퍼바이저 격리 기능이 작동하여 인가되지 않은 외부 관리자 프로세스가 LSASS 가상 메모리를 덤프(`ReadProcessMemory` API)하지 못하도록 강력하게 디펜스하기 때문입니다.

## 8. 학습 포인트
* **자격증명 캐싱 메커니즘**: 윈도우의 싱글 사인온(SSO)과 인증 유지를 위해 메모리 공간 상에 WDigest, Kerberos, NTLM 패키지 단위로 자격증명을 직렬화해 보존하는 LSASS 내부 원리를 학습합니다.
* **프로세스 미니덤프 분석**: 실행 중인 프로세스의 부분 가상 메모리를 박제한 Minidump 포맷을 역공학 파서(pypykatz, mimikatz)를 연계해 내부 해시 및 평문을 추출해 내는 능력을 훈련합니다.
