---
title: Actions on Objectives — 목표 달성
created: 2026-06-12
updated: 2026-06-12
type: concept
tags: [security, glossary, cyber-kill-chain, actions-on-objectives, data-exfiltration, ransomware, wiper, espionage, sabotage, impact]
sources: [https://ko.wikipedia.org/wiki/사이버_킬_체인, https://ko.wikipedia.org/wiki/데이터_유출]
confidence: high
---

# Actions on Objectives (목표 달성) — 사이버 킬 체인 7단계

## Step 1: 단어 직역 및 쉬운 비유

### 1. 약자 풀이

**Actions on Objectives** = **Actions** (행동, 조치) + **on** (~에 대해) + **Objectives** (목표, 목적)

| 영어 단어 | 직역 | 의미 |
|-----------|------|------|
| **Actions** | 행동, 조치, 실행 | 의도를 가지고 수행하는 행위 |
| **Objectives** | 목표, 목적, 대상 | 달성하고자 하는 최종 결과물 |

### 2. 의미 조합

> **"공격자가 최종적으로 의도한 임무를 수행하는 단계 — 데이터 유출, 랜섬웨어 암호화, 시스템 파괴, 장기 첩보, 금전 탈취 등 공격 동기에 따른 구체적 피해 발생"**

### 3. 강력한 비유: "금고(핵심 자산)에 도달한 도둑이 목표물 챙기고 폭탄 설치하고 떠나는 장면"

```
┌────────────────────────────────────────────────────────────┐
│  상황: 비밀 통로(C2)로 금고실(핵심 시스템)까지 들어온 도둑 │
│  이제 각자 목적에 따라 "진짜 일"을 벌임                   │
└────────────────────────────────────────────────────────────┘

🎯  **목표별 행동 유형** — 도둑마다 노리는 게 다름

  ① **금고 털이(데이터 유출 / Data Exfiltration)**: 
      "고객 DB, 지적재산, 설계도, 금융 기록 싹 챙겨감" → 
      압축 → 암호화 → C2/클라우드/별도 서버로 업로드
      → 다크웹 판매, 경쟁사 이전, 협박용 보관

  ② **폭탄 설치(랜섬웨어 / Ransomware)**: 
      "파일들 다 잠그고 열쇠 줄 테니 돈 내놔" → 
      AES/RSA 하이브리드 암호화 → 복호화 키 C2 보관
      → 몸값 협상(이중 협박: 유출 + 암호화), RaaS 분배

  ③ **폭파/방화(와이퍼 / Wiper & 파괴 / Sabotage)**: 
      "증거 인멸하려 다 태워버림 / 복구 불가능하게 망가뜨림" → 
      MBR/MFT 파괴, 볼륨 섀도 복사본 삭제, 펌웨어 손상
      → NotPetya, Olympic Destroyer, HermeticWiper, AcidRain

  ④ **도청기 심기(장기 첩보 / Espionage / APT)**: 
      "당분간 조용히 있으면서 매일 기밀 빼감" → 
      키로거, 스크린샷, 오디오/비디오 녹화, 문서 자동 수집
      → 수개월~수년간 지속 (Operation Aurora, SolarWinds, APT28/29)

  ⑤ **깃발 꽂기(디페이스먼트 / Defacement & 핵티비즘)**: 
      "우리가 해킹했음 알리고 메시지 남김" → 
      웹사이트 메인 페이지 변조, 정치적 구호, 단체 로고
      → Anonymous, 해킹 활동가 그룹, 사이버 시위

  ⑥ **현금 인출(금융 탈취 / Financial Theft)**: 
      "은행 송금 시스템 조작해 돈 빼감" → 
      SWIFT 메시지 위조, ATM 잭팟팅, 암호화폐 지갑 키 탈취
      → Lazarus Group (방글라데시 은행 $81M, 코인 레일 $40M+)

  ⑦ **봇넷 가입(컴퓨팅 자원 탈취 / Resource Hijacking)**: 
      "네 컴퓨터 내 채굴기/디도스 병기로 씀" → 
      크립토재킹(XMRig), DDoS 봇(Mirai, Qakbot), 프록시 봇
      → 전기비/CPU 사이클 공짜로 쓰고 피해자만 느려짐

💡 **핵심 포인트**: 킬 체인 1~6단계는 **"준비와 접근"**이고, 
7단계가 **"진짜 피해가 발생하는 순간"**입니다. 
공격자 동기(돈, 정보, 파괴, 과시, 이념)에 따라 **완전히 다른 결과**가 나옵니다.
```

---

## Step 2: 개념 시각화

![Actions on Objectives 비유 시각화: 금고실에서 목표 달성하는 도둑 — 공격자(해커), 금고(핵심 자산), 골드바(데이터 유출), 폭탄(랜섬웨어/와이퍼), 절단기(시스템 파괴), 도청기(장기 스파이), 깃발(디페이스먼트/핵티비즘) - 한글 레이블 포함](https://v3b.fal.media/files/b/0a9dfc8b/F2yDbIDoihKZTg5L5zcbG_gqySkV4a.png)

**이미지 설명**:
- **공격자(해커)** — 최종 목표를 실행하는 주체
- **금고(핵심 자산)** — 대상 조직의 크라운 주얼 (고객 DB, 지적재산, 금융 시스템, 제어 시스템)
- **골드바(데이터 유출)** — 기밀 정보 탈취 및 외부 전송
- **폭탄(랜섬웨어/와이퍼)** — 파일 암호화(몸값 요구) 또는 영구 파괴(복구 불가)
- **절단기(시스템 파괴)** — 인프라 무력화, 복구 불가능한 손상
- **도청기(장기 스파이)** — 지속적 감시 및 정보 수집 (APT)
- **깃발(디페이스먼트/핵티비즘)** — 웹사이트 변조, 정치적 메시지 표출

> ⚠️ **참고**: 이미지 생성 도구가 PNG 형식으로 반환했습니다. 스킬 요구사항(.jpg/.jpeg)은 현재 도구 제약상 PNG로 대체됩니다.

---

## Step 3: 전문 용어 설명 (위키백과 기반)

### 목표 달성 (Actions on Objectives, 사이버 킬 체인)

**정의**: **사이버 킬 체인의 7번째이자 마지막 단계**로, 공격자가 대상 환경에 충분히 접근하고 제어권을 확보한 후 **공격자의 본래 목적(동기)에 부합하는 구체적인 악의적 행동을 실행하여 실질적 피해를 입히는 단계**이다. 이 단계에서 **기밀성/무결성/가용성(CIA) 침해가 현실화**된다.

### 주요 목표 유형별 상세

| 목표 유형 | 공격자 동기 | 주요 기법 | 피해 영향 |
|----------|------------|-----------|-----------|
| **데이터 유출 (Data Exfiltration)** | 금전(판매), 경쟁 우위, 협박, 스파이 | 압축/암호화 후 C2/클라우드/FTP/이메일/물리 매체 전송, 스테가노그래피, 도메인 프론팅 | 기밀성 침해, 규정 위반(개인정보보호법, GDPR), 평판 손실, 2차 공격 표적화 |
| **랜섬웨어 (Ransomware)** | 금전 갈취 | 하이브리드 암호화(AES+RSA), 파일/볼륨/백업 타겟, 볼륨 섀도 삭제, 안전모드 부팅 방해, RaaS 분배 | 가용성 침해, 업무 중단, 복구 비용, 몸값 지불 유도, 이중/삼중 협박 |
| **와이퍼/파괴 (Wiper/Sabotage)** | 파괴, 증거 인멸, 정치적 메시지, 전쟁 | MBR/MFT/파티션 테이블 파괴, 펌웨어/BIOS 손상, 안전 부팅 키 삭제, 로그 삭제, 포렌식 방해 | 영구적 데이터 손실, 시스템 재설치 필요, 인프라 마비, 복구 불가능 |
| **장기 첩보 (Espionage/APT)** | 국가 안보, 군사/외교/경제 기밀, 기술 탈취 | 키로거, 스크린샷, 클립보드, 오디오/비디오, 문서 자동 수집, 크리덴셜 덤프, 수평 이동, 맞춤형 임플란트 | 지속적 기밀 유출, 전략적 의사결정 영향, 지적재산권 도용, 공급망 2차 공격 |
| **금융 탈취 (Financial Theft)** | 직접적 금전 수익 | SWIFT 메시지 위조, ATM 잭팟팅(블랙박스/악성 펌웨어), 암호화폐 거래소/지갑 키 탈취, 비즈니스 이메일 사기(BEC) | 직접적 금전 손실, 금융 시스템 신뢰 저하, 규제 제재 |
| **디페이스먼트/핵티비즘 (Defacement/Hacktivism)** | 정치적/사회적 메시지, 명성, 위협 | 웹사이트 콘텐츠 변조, 관리자 계정 탈취, CMS 취약점 악용, DNS 하이재킹 | 평판 손상, 서비스 일시 중단, 메시지 전파 |
| **리소스 하이재킹 (Resource Hijacking)** | 컴퓨팅 파워/대역폭 수익 | 크립토재킹(XMRig, 코인하이브), DDoS 봇넷(Mirai, Meris), 프록시/VPN 봇, 스팸 발송 | 성능 저하, 전기비 증가, 하드웨어 수명 단축, 2차 공격 공모자 |

### 데이터 유출 (Exfiltration) 기법 상세

| 기법 분류 | 구체적 방법 | 탐지 난이도 |
|----------|-------------|-------------|
| **C2 채널 경유** | 비콘 태스크로 파일 업로드, 청크 분할 전송, Base64/압축/암호화 인코딩 | 중간 (비콘 트래픽 분석) |
| **클라우드/웹 서비스** | GitHub/Gist, Google Drive, Dropbox, OneDrive, AWS S3, Azure Blob, Pastebin, Discord 웹훅 | 높음 (합법적 도메인, TLS) |
| **DNS 터널링** | 서브도메인에 데이터 인코딩 (예: `data.evil.com`), TXT/NULL 레코드 악용 | 중간 (엔트로피/쿼리 패턴) |
| **이메일/메신저** | SMTP 발송, Outlook/Exchange API, Telegram/Slack/Discord 봇 | 중간 (DLP, 콘텐츠 필터) |
| **물리/오프라인** | USB/외장하드 복사, 프린트/사진 촬영, QR코드 인코딩 | 높음 (네트워크 모니터링 불가) |
| **스테가노그래피** | 이미지/오디오/비디오/문서 내 데이터 은닉 (LSB, 주파수 영역) | 매우 높음 (시각적 무변화) |
| **코버트 채널** | 타이밍 채널, 공유 리소스(파일 락, 레지스트리), ICMP/TCP 헤더 필드 | 매우 높음 (특수 분석 필요) |

### 랜섬웨어 진화: 이중/삼중 협박

| 단계 | 설명 | 등장 시기 |
|------|------|-----------|
| **1세대: 단순 암호화** | 파일 암호화 → 복호화 키 대가 몸값 요구 | ~2015 |
| **2세대: 데이터 유출 협박 (Double Extortion)** | 암호화 전 데이터 탈취 → 미지불 시 공개 협박 (Maze, REvil, Conti) | 2019~ |
| **3세대: 서비스 거부/고객 협박 (Triple Extortion)** | DDoS 공격 추가, 고객/파트너사 직접 협박, 주가 조작 시도 | 2021~ |
| **4세대: RaaS 생태계** | 개발자(코어) + 제휴사(배포) 수익 분배, 포털/지원/업데이트 제공 | 2020~ |

### 와이퍼 vs 랜섬웨어 비교

| 특징 | 랜섬웨어 | 와이퍼 |
|------|----------|--------|
| **목적** | 금전 갈취 (복호화 키 판매) | 영구 파괴, 증거 인멸, 정치적 효과 |
| **복구 가능성** | 키 있으면 복구 가능 (이론상) | 복구 불가능 (데이터 영구 손실) |
| **몸값 노트** | 상세한 지불 안내, 채팅 지원 | 보통 없음 또는 가짜 몸값 노트 |
| **대표 사례** | WannaCry, REvil, LockBit, Conti | NotPetya, Olympic Destroyer, HermeticWiper, AcidRain, Shamoon |
| **배후** | 주로 크라임웨어 그룹 | 주로 국가 지원 APT (러시아, 이란, 북한) |

### 방어 관점: 목표 달성 단계 탐지 및 대응

| 대응 영역 | 구체적 방안 |
|----------|-------------|
| **데이터 유출 방지 (DLP)** | 네트워크 DLP(파일 시그니처, 정규식, 지문), 엔드포인트 DLP(클립보드, 인쇄, USB, 클라우드 업로드), 클라우드 DLP(SaaS/API), 이메일 DLP |
| **랜섬웨어 대응** | 백업 3-2-1 규칙(오프라인/불변/테스트), 볼륨 섀도 보호, 랜섬웨어 행위 탐지(대량 파일 암호화, 확장자 변경, 랜섬 노트 생성), 허니파일/캔토큰 배포 |
| **와이퍼/파괴 대응** | 부팅 가능 백업/이미지, 펌웨어 무결성 검증(TPM/Measured Boot), 섀도 복사본 보호, 로그 외부 전송(SIEM), 재해 복구 계획(DRP) 정기 테스트 |
| **APT/장기 첩보 탐지** | UEBA(사용자/엔티티 행위 분석), 수평 이동 탐지(Pass-the-Hash, Kerberos, WMI, RDP), 크리덴셜 덤프 탐지(LSASS 접근, DCSync), 위협 헌팅(MITRE ATT&CK 매핑) |
| **사고 대응 (IR)** | 플레이북(랜섬웨어, 데이터 유출, 와이퍼, BEC), 포렌식 준비(메모리/디스크/네트워크/로그), 법적/규제 신고(72시간 내), 위기 커뮤니케이션 |

### MITRE ATT&CK 매핑 (Impact / Exfiltration 관련)

| Tactic | Technique ID | Technique Name |
|--------|-------------|----------------|
| **Exfiltration** | **T1041** | Exfiltration Over Command and Control Channel |
| | **T1048** | Exfiltration Over Alternative Protocol |
| | **T1048.001** | Exfiltration Over Symmetric Encrypted Non-C2 Protocol |
| | **T1048.002** | Exfiltration Over Asymmetric Encrypted Non-C2 Protocol |
| | **T1048.003** | Exfiltration Over Unencrypted Non-C2 Protocol |
| | **T1567** | Exfiltration Over Web Service |
| | **T1567.001** | Exfiltration to Code Repository |
| | **T1567.002** | Exfiltration to Cloud Storage |
| | **T1567.003** | Exfiltration to Webhook |
| **Impact** | **T1485** | Data Destruction |
| | **T1486** | Data Encrypted for Impact (Ransomware) |
| | **T1489** | Service Stop |
| | **T1490** | Inhibit System Recovery |
| | **T1491** | Defacement |
| | **T1491.001** | Internal Defacement |
| | **T1491.002** | External Defacement |
| | **T1498** | Network Denial of Service |
| | **T1529** | System Shutdown/Reboot |
| | **T1531** | Account Access Removal |

---

## 관련 위키 링크

- [[command-and-control]] — 명령 및 제어 (목표 달성 선행 단계: C2 채널로 명령/데이터 전송)
- [[installation]] — 설치 (임플란트/지속성 확보로 목표 달성 기반 마련)
- [[exploitation]] — 익스플로잇 (초기 접근으로 목표 달성 진입로 확보)
- [[rce]] — 원격 코드 실행 (목표 달성 위한 코드 실행 기반)
- [[real-world-breach-cases]] — 실제 침해 사례 (목표 달성 유형별 44개 사례 분석)

---

## 참고 문헌

- 한국어 위키백과: [사이버 킬 체인](https://ko.wikipedia.org/wiki/사이버_킬_체인)
- 한국어 위키백과: [데이터 유출](https://ko.wikipedia.org/wiki/데이터_유출)
- 한국어 위키백과: [랜섬웨어](https://ko.wikipedia.org/wiki/랜섬웨어)
- 한국어 위키백과: [와이퍼 (악성코드)](https://ko.wikipedia.org/wiki/와이퍼_(악성코드))
- 한국어 위키백과: [사이버 스파이 활동](https://ko.wikipedia.org/wiki/사이버_스파이활동)