---
title: Privilege Escalation — 핵심
created: 2026-06-12
updated: 2026-06-13
type: concept
tags: [security, glossary, privilege-escalation, local, remote, vertical, horizontal, linux, windows, kernel, exploit]
sources: [https://ko.wikipedia.org/wiki/권한_상승, https://ko.wikipedia.org/wiki/커널_취약점]
confidence: high
---

# Privilege Escalation (권한 상승) — 보안 용어 해설

## Step 1: 단어 직역 및 쉬운 비유

### 1. 용어 풀이

**Privilege Escalation** = **Privilege** (특권, 권한) + **Escalation** (확대, 상승, 에스컬레이션)

| 영어 단어 | 직역 | 의미 |
|-----------|------|------|
| **Privilege** | 특권, 권한, 우대 | 시스템에서 허용된 행동 범위 |
| **Escalation** | 확대, 상승, 단계적 증가 | 권한 수준을 높이는 것 |

### 2. 의미 조합

> **"낮은 권한의 사용자/프로세스가 취약점/설정 오류를 악용하여, 더 높은 권한(관리자, 루트, 시스템 등)을 획득하는 공격"**

### 3. 강력한 비유: "일반 손님(일반 사용자)이 마스터 키(관리자 권한)를 훔쳐서 호텔 전체를 마음대로 드나드는 것"

```
┌────────────────────────────────────────────────────────────┐
│  상황: 호텔(시스템)에서 일반 투숙객(일반 사용자)이          │
│  마스터 키(최고 권한)를 손에 넣어 모든 방(자원)을 제어함    │
└────────────────────────────────────────────────────────────┘

🔑  **마스터 키 탈취 시나리오 (권한 상승 공격 흐름)**

  ① **초기 진입 (Initial Access)**: 
     - 일반 손님(일반 권한)으로 호텔(시스템) 입장
     - 예: 웹쉘 업로드, SSH 로그인, 피싱으로 내부 진입

  ② **권한 상승 시도 (Escalation Attempt)**:
     - 손님이 마스터 키(관리자 권한)를 찾으려 시도
     - **수직 권한 상승 (Vertical)**: 일반 → 관리자/루트/SYSTEM
     - **수평 권한 상승 (Horizontal)**: 일반 사용자 A → 일반 사용자 B (동급 권한 탈취)

  ③ **마스터 키 획득 (Privilege Escalation 성공)**:
     - **커널 익스플로잇**: OS 커널 버그로 루트 권한 획득
     - **설정 오류**: SUID 바이너리, sudo 설정, 예약 작업 악용
     - **자격증명 탈취**: 패스워드 해시, 토큰, SSH 키, 토큰 탈취
     - **서비스/데몬 악용**: 취약한 서비스(데이터베이스, 스케줄러 등)

  ④ **완전 장악 (Post-Exploitation)**:
     - 모든 방(파일, DB, 네트워크) 자유 출입
     - 감시 카메라 끄기(로그 삭제), 뒷문 만들기(백도어/지속성)
     - 다른 호텔(네트워크 내부 다른 서버)도 열쇠 복사해 침입 (수평 이동)

💡 **핵심 포인트**: 
- **초기 진입 ≠ 권한 상승** — 처음엔 낮은 권한, 이후 상승이 별도 단계
- **수직 vs 수평** — "더 높은 권한(수직)" vs "동급 타인 권한(수평)"
- **로컬 vs 원격** — 로컬 쉘 보유 후 상승 vs 원격에서 직접 상승
- **포스트 익스플로잇의 핵심** — 초기 진입 후 가장 중요한 단계
```

---

## Step 2: 개념 시각화

![Privilege Escalation 비유 시각화: 호텔 마스터 키로 설명하는 권한 상승 — 일반 손님(일반 사용자), 마스터 키(관리자/루트 권한), 모든 방(시스템 전체 자원), 열쇠 고리(취약점/설정 오류), 열쇠 복사(자격증명 탈취/수평 이동) - 한글 레이블 포함](https://v3b.fal.media/files/b/0a9dfef4/KqR2mKxL5vN8tYpHgJkB4_L9wEmVnA.png)

**이미지 설명**:
- **일반 손님(일반 사용자)** — 초기 진입 시 낮은 권한 계정
- **마스터 키(관리자/루트 권한)** — 시스템 전체 제어 권한
- **모든 방(시스템 전체 자원)** — 파일, DB, 네트워크, 설정, 다른 서버
- **열쇠 고리(취약점/설정 오류)** — 커널 버그, SUID, sudo, 크론, 취약한 서비스
- **열쇠 복사(자격증명 탈취/수평 이동)** — 해시 덤프, 패스더해시, 골든 티켓, 수평 이동

> ⚠️ **참고**: 이미지 생성 도구가 PNG 형식으로 반환했습니다. 스킬 요구사항(.jpg/.jpeg)은 현재 도구 제약상 PNG로 대체됩니다.

---

## Step 3: 전문 용어 설명 (위키백과/MITRE/업계 표준 기반)
### Privilege Escalation (권한 상승)

**정의**: **Privilege Escalation(권한 상승)**은 공격자가 **시스템/애플리케이션의 취약점, 설정 오류, 자격증명 탈취 등을 악용하여 현재 보유한 권한보다 더 높은 권한(관리자, 루트, SYSTEM, 도메인 관리자 등)을 획득하는 공격 기법**이다. MITRE ATT&CK **TA0004 (Privilege Escalation)** 전술에 해당하며, 초기 진입(Initial Access) 이후 **포스트 익스플로잇(Post-Exploitation)의 핵심 단계**다.

### 권한 상승 분류

| 분류 | 설명 | 예시 |
|------|------|------|
| **수직 권한 상승 (Vertical)** | 낮은 권한 → 높은 권한 (일반 → 관리자/루트/SYSTEM) | 일반 유저 → root, 일반 유저 → SYSTEM, Domain User → Domain Admin |
| **수평 권한 상승 (Horizontal)** | 동일 레벨 타인 계정/권한 탈취 | User A → User B, Service Account A → Service Account B |
| **로컬 권한 상승 (Local)** | 이미 쉘/접근 권한 있는 상태에서 로컬에서 상승 | 로컬 쉘 → 커널 익스플로잇 → root |
| **원격 권한 상승 (Remote)** | 원격에서 직접 높은 권한 획득 | RCE로 SYSTEM 권한 획득, 원격 코드 실행으로 관리자 권한 획득 |

### 주요 권한 상승 기법 (MITRE ATT&CK TA0004 매핑)

| Technique ID | 기법명 | 설명 | 플랫폼 |
|-------------|--------|------|--------|
| **T1068** | Exploitation for Privilege Escalation | 취약점 익스플로잇으로 권한 상승 (커널, 드라이버, 서비스) | All |
| **T1068.001** | Kernel Exploit | 커널 취약점(CVE-2021-4034, Dirty Pipe 등) | Linux, Windows |
| **T1068.002** | Driver Exploit | 취약한 드라이버 악용 (CVE-2020-0796 SMBGhost 등) | Windows, Linux |
| **T1068.003** | Service Exploit | 취약한 서비스/데몬 악용 (Docker, Docker socket 등) | Linux, Windows |
| **T1548.001** | Setuid and Setgid | SUID/SGID 비트 설정된 바이너리 악용 | Linux, macOS |
| **T1548.002** | Bypass User Account Control | UAC 우회 (Windows) | Windows |
| **T1548.003** | Sudo and Sudo Caching | sudo 설정 오류, NOPASSWD, timestamp_timeout 악용 | Linux, macOS |
| **T1548.004** | Elevated Execution with Prompt | 인증 프롬프트 스푸핑/자동화 | Windows, macOS |
| **T1053.005** | Scheduled Task/Job | 크론, 시스템 타이머, 작업 스케줄러 악용 | Linux, Windows |
| **T1505.003** | Web Shell | 웹쉘 업로드로 지속성 + 권한 상승 | Web |
| **T1556.002** | Password Filter | 패스워드 필터/알림 패키지로 자격증명 탈취 | Windows |
| **T1003** | OS Credential Dumping | LSASS, SAM, NTDS.dit, /etc/shadow 덤프 | All |
| **T1003.001** | LSASS Memory | lsass.exe 메모리 덤프 (Mimikatz,sekurlsa) | Windows |
| **T1003.002** | Security Account Manager | SAM 하이브 덤프 | Windows |
| **T1003.003** | NTDS | 도메인 컨트롤러 NTDS.dit 덤프 | Windows |
| **T1003.004** | LSA Secrets | LSA 시크릿 덤프 | Windows |
| **T1003.005** | Cached Domain Credentials | 캐시된 도메인 자격증명 | Windows |
| **T1003.006** | DCSync | 도메인 컨트롤러에서 복제로 자격증명 동기화 | Windows |
| **T1003.007** | Proc Filesystem | /proc/*/mem, /proc/*/environ 읽기 | Linux |
| **T1003.008** | /etc/passwd and /etc/shadow | 리눅스 패스워드/섀도 파일 읽기 | Linux |
| **T1550.002** | Pass the Hash | NTLM 해시로 인증 (PtH) | Windows |
| **T1550.003** | Pass the Ticket | 케르베로스 티켓으로 인증 (PtT) | Windows |
| **T1550.001** | Application Access Token | OAuth/액세스 토큰 탈취/재사용 | Cloud, Web |
| **T1550.004** | Web Session Cookie | 세션 쿠키/토큰 탈취/재사용 | Web |
| **T1556.002** | Password Filter | 패스워드 변경 가로채기 | Windows |
| **T1556.004** | Authentication Package | 인증 패키지 등록으로 자격증명 가로채기 | Windows |

### 플랫폼별 주요 권한 상승 경로

#### Linux/Unix

| 기법 | 상세 | 예시 |
|------|------|------|
| **커널 익스플로잇** | CVE-2021-4034 (PwnKit), Dirty Pipe (CVE-2022-0847), Dirty COW | `exploit.c` 컴파일 → 실행 → root |
| **SUID/SGID 바이너리** | `find / -perm -4000 2>/dev/null` → 취약한 바이너리 악용 | `base64`, `find`, `vim`, `bash` 등 |
| **Sudo 설정 오류** | `sudo -l` 확인 → NOPASSWD, `(ALL)`, `!authenticate`, 와일드카드 | `sudo -u root /bin/bash` |
| **Cron/시스템 타이머** | `/etc/cron*`, `/etc/systemd/timers/` 쓰기 권한 | 루트 실행 스크립트 수정 |
| **Path Hijacking** | `PATH` 환경 변수 조작, 상대 경로 실행 | `export PATH=/tmp:$PATH` |
| **Docker/컨테이너** | 도커 소켓 마운트(`/var/run/docker.sock`), `--privileged`, 호스트 네임스페이스 | `docker run -v /:/host -it ubuntu chroot /host` |
| **Wildcard Injection** | `tar cf archive.tar *` → `--checkpoint-action=exec=sh shell.sh` | `tar` 옵션 인젝션 |
| **LD_PRELOAD** | 환경 변수로 공유 라이브러리 강제 로드 | `LD_PRELOAD=/tmp/evil.so` |
| **Capabilities** | `getcap -r / 2>/dev/null` → `cap_setuid+ep` 등 악용 | `python3 -c 'import os; os.setuid(0); os.system("/bin/bash")'` |
| **Kernel Module** | 서명되지 않은 커널 모듈 로드 (`insmod`) | `insmod rootkit.ko` |

#### Windows

| 기법 | 상세 | 예시 |
|------|------|------|
| **UAC Bypass** | `fodhelper`, `eventvwr`, `sdclt`, `computerdefaults`, `slui` 등 | `reg add HKCU\Software\Classes\ms-settings\shell\open\command /d "cmd.exe" /f` |
| **Token Manipulation** | `runas`, `CreateProcessWithTokenW`, `DuplicateTokenEx` | `make_token`, `steal_token` (Cobalt Strike) |
| **Service Exploit** | 비보호 서비스 경로, 권한 없는 서비스 수정 | `sc config "vulnsvc" binpath= "cmd /c net user admin pass /add"` |
| **DLL Hijacking** | DLL 검색 순서 악용, 사이드로딩 | `C:\Program Files\App\vuln.dll` |
| **COM Hijacking** | CLSID/ProgID 하이재킹 | `HKCU\Software\Classes\CLSID\{...}` |
| **WMI Event Subscription** | 영구 WMI 이벤트 구독으로 지속성 + 권한 상승 | `__EventFilter`, `__EventConsumer`, `__FilterToConsumerBinding` |
| **AlwaysInstallElevated** | MSI 설치 시 SYSTEM 권한으로 실행 | `msiexec /i evil.msi /quiet` |
| **Sticky Keys / Utilman** | `sethc.exe`, `utilman.exe` 교체로 로그인 화면에서 SYSTEM 쉘 | `copy cmd.exe utilman.exe` |
| **PrintNightmare (CVE-2021-34527)** | 프린트 스풀러 원격 코드 실행 → SYSTEM | `CVE-2021-34527` 익스플로잇 |
| **ZeroLogon (CVE-2020-1472)** | Netlogon 프로토콜 취약점으로 도메인 컨트롤러 장악 | `zerologon.py` |
| **Kerberos Delegation** | 비제약/제약 위임 구성 오류로 티켓 위조 | `findDelegation.py`, `getST.py` |
| **DCSync** | 도메인 컨트롤러 복제 권한으로 자격증명 동기화 | `lsadump::dcsync /user:krbtgt` |


## 관련 위키 링크
- [[privilege-escalation]] — 인덱스 페이지
- [[privilege-escalation-defense]] — 분할 페이지
- [[rce]]
