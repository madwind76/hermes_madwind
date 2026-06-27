---
title: Installation (설치) — 사이버 킬 체인 5단계
created: 2026-06-12
updated: 2026-06-21
type: concept
tags: [security, glossary, cyber-kill-chain, installation, persistence, backdoor, rootkit, bootkit, c2]
sources: [https://ko.wikipedia.org/wiki/사이버_킬_체인, https://ko.wikipedia.org/wiki/백도어]
confidence: high
---

# Installation (설치) — 사이버 킬 체인 5단계

## 참고 URL
- [ko.wikipedia.org](https://ko.wikipedia.org/wiki/사이버_킬_체인)
- [ko.wikipedia.org](https://ko.wikipedia.org/wiki/백도어)

## Step 1: 단어 직역 및 쉬운 비유

### 1. 약자 풀이

**Installation** = **Install** (설치하다) + **-ation** (명사화 접미사)

| 영어 단어 | 직역 | 의미 |
|-----------|------|------|
| **Install** | 설치하다, 배치하다 | 소프트웨어/장비를 제자리에 놓고 사용 가능하게 함 |
| **Installation** | 설치, 배치, 인스톨 | 무언가를 시스템에 영구적으로 자리잡게 하는 과정 |

### 2. 의미 조합

> **"익스플로잇으로 얻은 초기 접근권을 영구적으로 유지하기 위해 백도어, 루트킷, 스케줄드 태스크 등 지속성 메커니즘을 시스템에 설치하는 과정 — 재부팅/로그아웃 후에도 공격자 접근 보장"**

### 3. 강력한 비유: "건물 침입 후 비밀 통로와 열쇠를 만들어두는 도둑"

```
┌────────────────────────────────────────────────────────────┐
│  상황: 자물쇠 따고 건물 안으로 들어간 도둑(공격자).        │
│  이제 언제든 다시 들어오려고 '비밀 통로'를 만듦            │
└────────────────────────────────────────────────────────────┘

🔑  **비밀 통로 만들기(지속성/설치)** — 어떻게 계속 들어올까?

  ① **뒷문 열쇠 복사(레지스트리 Run 키/시작 폴더)**: 
      "관리자만 쓰는 뒷문 열쇠 몰래 복사해 둠" → 
      `HKCU\Software\Microsoft\Windows\CurrentVersion\Run`
      `C:\Users\<user>\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup`

  ② **청소부 명부에 이름 올리기(스케줄드 태스크/서비스)**: 
      "매일 새벽 3시 청소부인 척 들어와서 문 열어둠" → 
      `schtasks /create /sc daily /tn "Windows Update" /tr "malware.exe"`
      `sc create "LegitService" binPath= "C:\Windows\Temp\malware.exe"`

  ③ **건물 구조도 바꿔치기(WMI 이벤트 구독/COM 하이재킹)**: 
      "화재 감지기가 울리면 자동으로 뒷문 열리게 설비 변경" → 
      WMI Event Filter + Consumer Binding, COM Object Hijacking

  ④ **마스터 키 심기(부트킷/루트킷/커널 드라이버)**: 
      "건물 기초 공사 때 마스터 키 금형 심어둠 — 재건축(재부팅)해도 작동" → 
      MBR/VBR 감염, UEFI 펌웨어 변조, 커널 모드 드라이버 서명 우회

  ⑤ **정상 파일 위장(DLL 사이드 로딩/실행 파일 교체)**: 
      "정상 프로그램인 척하며 실행될 때 같이 딸려 들어감" → 
      `legit.exe` 옆 `malicious.dll` 배치, 정상 바이너리 패치

  ⑥ **청취 장치 설치(C2 비콘/임플란트)**: 
      "건물 안에 도청기 심어 언제든 명령 내릴 수 있게" → 
      Cobalt Strike Beacon, Sliver, Meterpreter, Sliver, Mythic, 커스텀 임플란트

💡 **핵심 포인트**: 익스플로잇이 **"일회성 침입"**이라면, 설치는 **"영구 거처 마련"**입니다. 
재부팅해도, 패치해도, 비밀번호 바꿔도 **계속 들어올 수 있는 통로**를 만듭니다.
```

---

## Step 2: 개념 시각화

![Installation 비유 시각화: 건물 침입 후 비밀 통로 설치 — 공격자(해커), 침투된 건물(해킹된 시스템), 비밀 문(백도어/지속성), 숨겨진 경첩(레지스트리 런 키/스케줄드 태스크/서비스/WMI/시작 폴더), 청취 장치(C2 비컨), 마스터 키(루트킷/부트킷) - 한글 레이블 포함](https://v3b.fal.media/files/b/0a9dfc45/FDlnWq-wydB3QOGSBIyzn_85D9OYdm.png)

**이미지 설명**:
- **공격자(해커)** — 초기 침투 후 지속성 확보 작업을 수행하는 주체
- **침투된 건물(해킹된 시스템)** — 익스플로잇으로 코드 실행 권한을 얻은 대상 호스트
- **비밀 문(백도어/지속성)** — 정상 인증 절차 우회하여 재접근 가능한 숨겨진 진입점
- **숨겨진 경첩(레지스트리 런 키/스케줄드 태스크/서비스/WMI/시작 폴더)** — OS가 자동 실행하는 메커니즘 악용
- **청취 장치(C2 비컨)** — 공격자 서버로 주기적 연결하여 명령 수신하는 임플란트
- **마스터 키(루트킷/부트킷)** — 커널/펌웨어 레벨에서 은폐 및 제어권 유지하는 루트킷

> ⚠️ **참고**: 이미지 생성 도구가 PNG 형식으로 반환했습니다. 스킬 요구사항(.jpg/.jpeg)은 현재 도구 제약상 PNG로 대체됩니다.

---

## Step 3: 전문 용어 설명 (위키백과 기반)

### 설치 (Installation, 사이버 킬 체인)

**정의**: **사이버 킬 체인의 5단계**로, 공격자가 익스플로잇으로 얻은 **초기 코드 실행 권한을 영구적으로 유지하기 위해 시스템에 악성 소프트웨어(임플란트, 백도어, 루트킷 등)를 설치하고 지속성(Persistence) 메커니즘을 구성하는 과정**이다.

### 지속성 기법 분류 (MITRE ATT&CK: Persistence - TA0003)

| 분류 | 기법 ID | 기법명 | 설명 | 탐지 난이도 |
|------|---------|--------|------|-------------|
| **레지스트리/시작 폴더** | T1547.001 | Registry Run Keys / Startup Folder | 로그온 시 자동 실행 등록 | 낮음 |
| | T1547.003 | Time Providers | Windows 시간 공급자 악용 | 중간 |
| | T1547.004 | Winlogon Helper DLL | Winlogon 알림 패키지/헬퍼 DLL | 중간 |
| **스케줄드 태스크/서비스** | T1053.005 | Scheduled Task | 작업 스케줄러 등록 (SYSTEM 권한 가능) | 낮음 |
| | T1543.003 | Windows Service | 서비스 생성/수정 (지속적 백그라운드 실행) | 낮음 |
| | T1543.002 | Systemd Service | Linux systemd 서비스/타이머 | 낮음 |
| **부트/로그온** | T1542.001 | Bootkit | MBR/VBR/UEFI 펌웨어 감염 (OS 로드 전 실행) | 높음 |
| | T1542.003 | Boot or Logon Autostart Execution | 커널 드라이버, 부트 스크립트 | 높음 |
| | T1547.009 | Shortcut Modification | LNK 파일 대상 변경 | 중간 |
| **WMI/COM** | T1546.003 | WMI Event Subscription | WMI 필터/컨슈머/바인딩으로 영구 실행 | 높음 |
| | T1546.015 | Component Object Model Hijacking | CLSID/ProgID 하이재킹 | 높음 |
| **애플리케이션 셸링** | T1574.001 | DLL Search Order Hijacking | 정상 EXE 옆 악성 DLL 배치 | 중간 |
| | T1574.002 | DLL Side-Loading | 정상 서명된 EXE가 악성 DLL 로드 | 중간 |
| | T1574.011 | Services Registry Permissions Weakness | 서비스 레지스트리 권한 오남용 | 중간 |
| **계정 조작** | T1098.001 | Additional Cloud Credentials | 클라우드 키/토큰 추가 | 중간 |
| | T1098.004 | SSH Authorized Keys | `~/.ssh/authorized_keys` 공개키 추가 | 낮음 |
| | T1136.001 | Create Account: Local Account | 로컬 관리자 계정 생성 | 낮음 |

### 주요 임플란트/백도어 유형

| 유형 | 특징 | 대표 사례 |
|------|------|-----------|
| **리버스 쉘/바인드 쉘** | 단순 네트워크 쉘, 인터랙티브 | Netcat, Bash 리버스 쉘, PowerShell 리버스 |
| **C2 프레임워크 비콘** | 기능 풍부, 모듈형, 은폐 기능 | Cobalt Strike Beacon, Sliver, Mythic, Brute Ratel, Havoc |
| **메모리 상주/파일리스** | 디스크 미작성, 메모리만 상주 | PowerShell 리플렉티브 로드, .NET 어셈블리 메모리 실행 |
| **커널/부트킷** | Ring 0 권한, 안티포렌식, 제거 어려움 | TDL4, Necurs, Rovnix, UEFI 부트킷 (MoonBounce, ESPecter) |
| **하드웨어/펌웨어** | OS 재설치로도 제거 불가 | NSA ANT 카탈로그 (COTTONMOUTH, IRONCHEF) |
| **웹쉘** | 웹 서버에 업로드된 스크립트 백도어 | China Chopper, AntSword, Godzilla, 커스텀 PHP/ASPX/JSP 쉘 |

### 설치 단계에서의 공격자 고려사항 (OPSEC)

| 고려사항 | 설명 |
|----------|------|
| **은폐성(Stealth)** | 프로세스 숨기기(루트킷, DKOM), 네트워크 연결 위장(도메인 프론팅, CDN), 아티팩트 최소화 |
| **내구성(Resilience)** | 다중 지속성 메커니즘(Defense in Depth), 자가 복구(워치독), 페일오버 C2 |
| **권한 유지** | 권한 상승(PrivEsc) 결합, 토큰 조작, 커널 익스플로잇으로 SYSTEM/ROOT 획득 |
| **수평 이동 준비** | 자격증명 덤프(Mimikatz, LSASS), 패스더해시, 패스더티켓, Kerberos 위임 악용 |
| **페이로드 업데이트** | 원격 업데이트 기능(스테이징), 버전 관리, 킬 스위치 |

### 방어 관점: 설치/지속성 탐지 및 제거

| 방어 계층 | 대응 방안 |
|----------|-----------|
| **엔드포인트(EDR)** | 자동 실행 지점 모니터링(Autoruns), 프로세스 트리 분석, WMI/스케줄드 태스크/서비스 생성 이벤트 감시, 메모리 스캔(루트킷 탐지) |
| **호스트 기반** | 파일 무결성 모니터링(FIM: Tripwire, OSSEC, Wazuh), 감사 정책(4688, 4698, 4699, 4702, 7045), AppLocker/WDAC으로 서명되지 않은 실행 차단 |
| **네트워크** | 비콘 트래픽 패턴 분석(주기성, 크기, User-Agent, JA3), 도메인/DGA 평판, TLS 지문 분석 |
| **아이덴티티** | 권한 있는 계정 모니터링, 관리자 그룹 변경 감시, Kerberos 티켓/위임 감사, 클라우드 자격증명 로테이션 |
| **사고 대응** | `autoruns`, `sysinternals`, `kapsel`, `Volatility` 메모리 포렌식, MFT/USN 저널 분석, 부트킷 검사(UEFI 스캔) |

### MITRE ATT&CK 매핑 (Installation/Persistence 관련)

| Tactic | Technique ID | Technique Name |
|--------|-------------|----------------|
| **Persistence** | **T1547** | Boot or Logon Autostart Execution |
| | **T1547.001** | Registry Run Keys / Startup Folder |
| | **T1547.003** | Time Providers |
| | **T1053** | Scheduled Task/Job |
| | **T1053.005** | Scheduled Task |
| | **T1543** | Create or Modify System Process |
| | **T1543.003** | Windows Service |
| | **T1546** | Event Triggered Execution |
| | **T1546.003** | WMI Event Subscription |
| | **T1546.015** | Component Object Model Hijacking |
| | **T1574** | Hijack Execution Flow |
| | **T1574.001** | DLL Search Order Hijacking |
| | **T1574.002** | DLL Side-Loading |
| | **T1505** | Server Software Component |
| | **T1505.003** | Web Shell |
| **Privilege Escalation** | **T1068** | Exploitation for Privilege Escalation |
| **Defense Evasion** | **T1027** | Obfuscated Files or Information |
| | **T1055** | Process Injection |
| | **T1070** | Indicator Removal on Host |

---

## 관련 위키 링크

- [[exploitation]] — 익스플로잇 (설치의 선행 단계: 초기 코드 실행 획득)
- [[command-and-control]] — 명령 및 제어 (설치 후속 단계: C2 채널 구축)
- [[rce]] — 원격 코드 실행 (초기 접근 수단)
- [[weaponization]] — 무기화 (임플란트/비콘 제작 단계)

---

## 참고 문헌

- 한국어 위키백과: [사이버 킬 체인](https://ko.wikipedia.org/wiki/사이버_킬_체인)
- 한국어 위키백과: [백도어 (컴퓨팅)](https://ko.wikipedia.org/wiki/백도어_(컴퓨팅))
- 한국어 위키백과: [루트킷](https://ko.wikipedia.org/wiki/루트킷)
- 한국어 위키백과: [부트킷](https://ko.wikipedia.org/wiki/부트킷)
- 한국어 위키백과: [지속성 (컴퓨터 보안)](https://ko.wikipedia.org/wiki/지속성_(컴퓨터_보안))
