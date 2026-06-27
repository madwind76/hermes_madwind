---
title: C2 — 방어
created: 2026-06-12
updated: 2026-06-21
type: concept
tags: [security, glossary, cyber-kill-chain, c2, command-and-control, beacon, implant, c2-framework, covert-channel]
sources: [https://ko.wikipedia.org/wiki/사이버_킬_체인, https://ko.wikipedia.org/wiki/명령_제어]
confidence: high
---
> [[command-and-control]]의 후반부입니다.

## 참고 URL
- [ko.wikipedia.org](https://ko.wikipedia.org/wiki/사이버_킬_체인)
- [ko.wikipedia.org](https://ko.wikipedia.org/wiki/명령_제어)

## Step 3: 전문 용어 설명 (위키백과 기반)
### 대표 C2 프레임워크 비교

| 프레임워크 | 언어 | 라이선스 | 특징 | 주요 사용자 |
|-----------|------|----------|------|-------------|
| **Cobalt Strike** | Java (Team Server), C (Beacon) | 상용 | 업계 표준, Malleable C2 프로파일, 풍부한 모듈 | APT, 레드팀, 크라임웨어 |
| **Sliver** | Go | GPLv3 | 크로스 플랫폼, 임플란트 동적 컴파일, Mutal TLS | 레드팀, 연구자 |
| **Mythic** | Go + React | Apache 2.0 | 컨테이너 기반, 플러그인 아키텍처, 다중 C2 프로토콜 | 레드팀, 교육 |
| **Havoc** | C++/Go | GPLv3 | 모던 UI, Cross-platform, 다이나믹 모듈 | 레드팀 |
| **Brute Ratel** | C++/Go | 상용 | EDR 회피 특화, 반사적 로드, 커스텀 프로파일 | 레드팀, APT 시뮬레이션 |
| **Metasploit** | Ruby | BSD | 방대한 익스플로잇/페이로드 DB, Meterpreter | 페널트레이션 테스터 |
| **Empire / Koadic** | PowerShell / JS | 오픈소스 | 파일리스, Living-off-the-Land | 구형 환경, 레거시 |

### C2 탐지 및 차단 (방어 관점)

| 탐지 접근법 | 기법 | 구현 예시 |
|------------|------|-----------|
| **트래픽 분석** | 비콘 주기성/지터 통계 분석, JA3/JA3S TLS 지문, HTTP 헤더/바디 이상 패턴, DNS 엔트로피/빈도 | Zeek, Suricata, Network Detection & Response (NDR) |
| **호스트 기반** | 프로세스 네트워크 연결 모니터링(비정상 대상/포트), 메모리 스캔(Reflective DLL, 쉘코드), 자식 프로세스 관계 | EDR (CrowdStrike, SentinelOne, Defender for Endpoint, Elastic) |
| **로그/행위** | 프로세스 실행(4688), 네트워크 연결(5156), DNS 쿼리, 프록시 로그, 방화벽 로그 상관관계 | SIEM (Splunk, Elastic, QRadar), SOAR |
| **위협 인텔리전스** | 악성 IP/도메인/해시 평판, C2 인프라 추적(Cobalt Strike 워터마크, 서버 지문), DGA/패스트 플럭스 탐지 | MISP, AlienVault OTX, VirusTotal, Abuse.ch |
| **머신러닝/행위** | 비콘 유사 시계열 클러스터링, 이상 프로세스 통신 탐지, C2 채널 분류 | UEBA, NTA, XDR |

### MITRE ATT&CK 매핑 (Command & Control 관련)

| Tactic | Technique ID | Technique Name |
|--------|-------------|----------------|
| **Command and Control** | **T1071** | Application Layer Protocol |
| | **T1071.001** | Web Protocols (HTTP/HTTPS) |
| | **T1071.002** | File Transfer Protocols |
| | **T1071.003** | Mail Protocols |
| | **T1071.004** | DNS |
| | **T1071.005** | SMB/Windows Admin Shares |
| | **T1573** | Encrypted Channel |
| | **T1573.001** | Symmetric Cryptography |
| | **T1573.002** | Asymmetric Cryptography |
| | **T1008** | Fallback Channels |
| | **T1102** | Web Service (Dead Drop Resolver) |
| | **T1102.001** | Dead Drop Resolver |
| | **T1102.002** | Bidirectional Communication |
| | **T1102.003** | One-Way Communication |
| | **T1132** | Data Encoding |
| | **T1132.001** | Standard Encoding (Base64, Hex) |
| | **T1132.002** | Non-Standard Encoding |
| | **T1568** | Dynamic Resolution |
| | **T1568.001** | Fast Flux DNS |
| | **T1568.002** | Domain Generation Algorithms (DGA) |
| | **T1568.003** | DNS Calculation |
| | **T1574** | Hijack Execution Flow (Proxy/DLL for C2) |

---


## 관련 위키 링크

- [[installation]] — 설치 (C2의 선행 단계: 임플란트/비콘 설치)
- [[actions-on-objectives]] — 목표 달성 (C2 후속 단계: 데이터 유출, 파괴 등)
- [[exploitation]] — 익스플로잇 (초기 접근 후 C2 채널 확보)
- [[weaponization]] — 무기화 (C2 임플란트/비콘 제작)

---

## 참고 문헌

- 한국어 위키백과: [사이버 킬 체인](https://ko.wikipedia.org/wiki/사이버_킬_체인)
- 한국어 위키백과: [명령 제어 서버](https://ko.wikipedia.org/wiki/명령_제어_서버)
- 한국어 위키백과: [봇넷](https://ko.wikipedia.org/wiki/봇넷)
- 한국어 위키백과: [코발트 스트라이크](https://ko.wikipedia.org/wiki/코발트_스트라이크)
## 관련 위키 링크
- [[command-and-control]] — 인덱스 페이지
- [[c2-core]] — 분할 페이지
- [[rce]]
