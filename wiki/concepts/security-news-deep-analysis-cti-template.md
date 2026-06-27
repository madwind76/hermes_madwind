---
title: Weekly Deep Analysis Framework (CTI Style Template)
created: 2026-06-27
updated: 2026-06-27
type: reference
template_basis: CTI-2026-0628-DPRK-AI (Dennis Kim, gameworkerkim)
applies_to: weekly-deep-analysis-report-v2
tags: [weekly-report, deep-analysis, cti-style, key-judgment, three-axis, mitre-attack, diamond-model, korean]
related_reports:
  - wiki/raw/articles/2026/202606/weekly-deep-analysis-report-20260622-20260627-v2.md (v2 구현 사례)
sources:
  - https://github.com/gameworkerkim/CYBER-THREAT-INTELLIGENCE-REPORT/blob/main/CTI-2026-0628-DPRK-AI.md
confidence: high
---

# Weekly Deep Analysis Framework (CTI Style Template)

이 문서는 **CTI 보고서 구조**(Key Judgments + 3축 프레임워크 + MITRE ATT&CK + 질적 변화 비교표)를 차용한 **주간 심층 분석 보고서 템플릿**입니다. 2026-06-27의 v2 보고서에서 처음 구현되었으며, 매주 일관된 품질로 발행하기 위한 표준 가이드입니다.

## 1. 적용 대상

| 보고서 형식 | 이 템플릿 적용 |
|---|---|
| **weekly-trend-report** (요약 분석, ~20KB) | ❌ 미적용 |
| **weekly-newsletter** (편집본, ~20KB) | ❌ 미적용 |
| **weekly-deep-analysis-report v2+** (심층 분석, ~35KB) | ✅ **적용** |
| **monthly-trend-report** | △ 일부 적용 (KJ 시스템만 도입 권장) |

## 2. 전체 구조 (14개 섹션)

```
0.  Report Metadata (TLP + Severity + 데이터 출처 표)
1.  핵심 메시지 (TL;DR) — 1단락, 한 줄 핵심 인용
2.  Key Judgments — 7개 핵심 판단 + 신뢰도 표
3.  3대 축 분석 프레임워크 — 시각적 도식
4.  축 ① 사회공학 + AI 결합 심층 분석
5.  축 ② 공급망 공격의 다층화 심층 분석
6.  축 ③ AI/공식 제품의 공격 표면화 심층 분석
7.  한국 특수 정황 분석 (필수, news 프로파일)
8.  질적 변화 비교표 (전 → 현재 → 전망)
9.  위협 행위자 매트릭스 (Diamond Model)
10. 7월/다음 주 예측 — 10개 모니터링 포인트
11. 운영 권고 — P0/P1/P2/P3 4단계
12. 분석 한계 및 주의사항
13. 참고 자료 (외부 출처 + 내부 family)
14. 메타데이터 + v1→v2 개선 비교
```

## 3. Key Judgment (KJ) 작성 규칙

### 3.1 KJ 개수

- **정확히 7개**를 권장 (5~8개도 허용)
- 너무 적으면 분석 깊이 부족, 너무 많으면 핵심 흐림

### 3.2 KJ 형식

```
| # | 판단 | 신뢰도 |
|---|---|---|
| **KJ-1** | [한 문장 판단, 30~80자] | **High** |
```

### 3.3 신뢰도 4단계

| 등급 | 의미 | 사용 시점 |
|---|---|---|
| **High** | 공개 출처 다수 + 직접 증거 | KEV 등재, RFC 발표, 공식 패치 |
| **Medium-High** | 공개 출처 일부 + 강한 정황 | 다수 매체 보도, 기술 분석 일치 |
| **Medium** | 단일 출처 + 추론 | 단일 분석 보고서, 전망 |
| **Low** | 미확실, 주의 필요 | (이번 주 v2에는 없음, 사용 자제) |

### 3.4 KJ 작성 체크리스트

- [ ] 30~80자 내외의 한 문장
- [ ] "~으로 판단됨" 같은 단정 회피, "추정", "관측", "보고됨" 사용
- [ ] 신뢰도 등급 부여
- [ ] 본문 섹션과 양방향 참조 (KJ-N이 본문 섹션 M을 근거로 함)
- [ ] 7개 중 최소 2개는 **High** 신뢰도

## 4. 3축 분석 프레임워크

### 4.1 축 정의

| 축 | 정의 | 적용 사건 유형 |
|---|---|---|
| **축 ① 사회공학 + AI 결합** | 인간을 표적으로 한 사회공학적 공격에 AI 도구가 결합된 사례 | 피싱, 딥페이크, 합성 페르소나 |
| **축 ② 공급망 공격** | 소프트웨어·서비스·데이터 사슬의 다층 침투 | npm, CI/CD, SaaS, 협력사 |
| **축 ③ AI/공식 제품의 공격 표면화** | AI 도구와 공식 제품 자체가 공격 표면이 됨 | AI 워크플로우 CVE, Chrome 패치, 공식 클라우드 도구 |

### 4.2 축별 구성 (3가지 공통)

1. **사건별 킬 체인 (Lockheed Kill Chain 7단계)** — ASCII 다이어그램
2. **MITRE ATT&CK 매핑** — Tactic / Technique / ID 표
3. **탐지/대응 포인트** — Sigma 룰, IOC, 권고

## 5. MITRE ATT&CK 매핑 규칙

### 5.1 매핑 형식

```markdown
| Tactic | Technique | ID | 본 사건 적용 |
|---|---|---|---|
| Initial Access | Supply Chain Compromise | T1195.002 | npm 패키지 침투 |
| Execution | Command and Scripting Interpreter | T1059.007 | post-install script |
```

### 5.2 매핑 권장 수

- 사건당 **3~10개 T-id** (너무 적으면 분석 부족, 너무 많으면 노이즈)
- 전체 보고서에서 **20개 이상** 권장

### 5.3 자주 사용되는 T-id 목록

| T-id | Technique | 사용 사례 |
|---|---|---|
| T1195 | Supply Chain Compromise | npm, CI/CD, SaaS |
| T1190 | Exploit Public-Facing Application | 웹앱, VPN, 방화벽 |
| T1566 | Phishing | 이메일 피싱 |
| T1059 | Command and Scripting Interpreter | 셸, PowerShell |
| T1552 | Credentials In Files | 자격증명 파일 |
| T1071 | Application Layer Protocol | C2 통신 |
| T1497 | Virtualization/Sandbox Evasion | 분석 방해 |
| T1547 | Boot or Logon Autostart Execution | 지속성 |
| T1027 | Obfuscated Files or Information | 코드 난독화 |

## 6. Diamond Model 활용

### 6.1 Diamond Model 4측면

| 측면 | 설명 | 작성 예시 |
|---|---|---|
| **Adversary** | 위협 행위자 | "Russian IAB", "DPRK Lazarus" |
| **Capability** | 공격 도구·기술 | "Fortinet SSL VPN credential theft" |
| **Infrastructure** | C2 인프라 | "러시아·CIS IP, Tor 다층" |
| **Victim** | 표적 | "글로벌 Fortinet 고객, 우크라이나 표적" |

### 6.2 작성 형식

```markdown
| 측면 | FortiBleed IAB | StockStay APT |
|---|---|---|
| **Adversary** | Russian Initial Access Broker | Russian APT (Cluster 추정) |
| **Capability** | Fortinet SSL VPN credential theft | SSRF + custom backdoor |
| **Infrastructure** | 러시아·CIS 지역 IP, Tor 다층 | 표적별 인프라, geo-fencing |
| **Victim** | 글로벌 Fortinet 고객 | 우크라이나 정부·군사·에너지 |
```

## 7. 질적 변화 비교표 (전 → 현재 → 전망)

### 7.1 형식

```markdown
| 차원 | 2024년 이전 | 2025년 (AI 보조) | 2026년 (자율화) |
|---|---|---|---|
| **AI 활용** | 미사용/실험 | 피싱 문안 보조 | 공격 수명주기 자율 실행 |
| **사회공학** | 수작업 스피어피싱 | AI 문안 교정 | 딥페이크 신분증·영상 |
| **공급망** | 단일 패키지 표적 | 다중 패키지 | 다층화 |
| **공식 제품** | 주기적 패치 | 제로데이 조기 악용 | AI 도구 + 공식 제품 동시 표면화 |
```

### 7.2 작성 원칙

- **3개 시점** 비교 (전 / 현재 / 전망)
- **5~7개 차원** (AI 활용, 사회공학, 공급망, 공식 제품, 국가 APT 등)
- **변화 동사가 명확** ("보조" → "자율 실행" 같은)

## 8. 한국 특수 정황 섹션 (필수)

news 프로파일에선 **반드시** 포함. 구성:

1. **국내 표적 사건 3~5건** (한국 조직·기업·사용자가 직접 표적이 된 사건)
2. **국내 정책/규제** (개인정보위, KISA, 과기정통부 등)
3. **국내 매체 보도 분석** (데일리시큐 + KISA + 보안뉴스 등)

### 형식 예시

```markdown
## 7. 🇰🇷 한국 특수 정황 분석

### 7.1 아리스팅어 봇넷 (한국 감염률 48.45%)
| 항목 | 값 |
|---|---|
| 표적 | D-Link DIR-850L, DIR-818LW |
| 한국 감염률 | 48.45% |
| ...
```

## 9. 운영 권고 4단계 (P0/P1/P2/P3)

### 9.1 우선순위 정의

| 단계 | 시한 | 예시 |
|---|---|---|
| **P0** | 24시간 이내 | Chrome 149 업데이트, KEV 등재 CVE 패치 |
| **P1** | 1~2주 | 모바일 OS 업데이트, CVE 점검 |
| **P2** | 1~3개월 | 양자내성 로드맵, SBOM 도입 |
| **P3** | 6~12개월 | KMS/HSM, 자산 가시성 통합 |

### 9.2 작성 형식

```markdown
### 11.1 즉시 (24시간 이내) — P0

| 우선순위 | 액션 | 대상 |
|---|---|---|
| 🔴 P0 | Chrome 149.0.7827.53 이상 업데이트 | 전사 엔드포인트 |
| 🔴 P0 | LiteLLM 버전 점검 및 업데이트 | AI 도구 사용자 조직 |
```

## 10. 위협 행위자 매트릭스 (★ 5단계)

```markdown
| 행위자 | 1차 공격 | 2차 활용 | 표적 지역 | 6월 강도 |
|---|---|---|---|---|
| Russian IAB | VPN/Firewall 결함 | Credential theft | 글로벌 | ★★★★★ |
| Russian APT (StockStay) | SSRF/백도어 | 우크라이나 표적 | 동유럽 | ★★★★ |
| North Korea | npm 침투 | 공급망 확산 | 글로벌 | ★★★★ |
| DPRK (BlueNoroff) | AI 딥페이크 영상 | 암호화폐 표적 | 글로벌 | ★★★★ |
| Chinese (Silver Fox 추정) | Spear phishing | 기업 표적 | 동아시아 | ★★★ |
```

## 11. Sigma 탐지 룰 형식

```yaml
title: [탐지 이름]
id: [unique-id]
status: experimental
description: [탐지 설명]
logsource:
  category: process_creation
  product: linux
detection:
  selection:
    ParentImage|endswith: 'node'
    ParentCommandLine|contains: 'npm install'
  suspicious_behavior:
    CommandLine|contains:
      - '/.aws/credentials'
      - '/.npmrc'
  condition: selection AND suspicious_behavior
level: high
```

## 12. 분석 한계 명시 템플릿

```markdown
| 항목 | 설명 |
|---|---|
| **귀속 불확실성** | [행위자] 공격자, 출처별 차이 |
| **MITRE ATT&CK 매핑** | 공개 출처 기반 추정 |
| **국내 위협** | 데일리시큐 + KISA만 수집, 별도 조회 필요 |
| **실제 악용 통계** | CISA KEV 기준, 미공개 0-day 미반영 |
```

## 13. v1 → v2 핵심 개선 비교 (매주 업데이트)

```markdown
| 차원 | v1 | v2 (현재) | v3 (계획) |
|---|---|---|---|
| **신뢰도 표시** | 없음 | KJ 7개 + High/Medium-High/Medium | 동일 |
| **프레임워크** | 8개 IU (사건 단위) | 3축 분석 (유형별) + KJ | + 위협 시나리오별 분기 |
| **MITRE ATT&CK** | 일부 사건만 | 모든 사건 (T-id 30+) | ATT&CK for ICS 추가 |
| **비교 시각화** | 카테고리별 | 질적 변화 비교표 | 시계열 sparkline |
| **귀속** | 단정 | 추정·불확실성 명시 | 출처별 가중치 표기 |
```

## 14. 작성 워크플로우 체크리스트

- [ ] 보고서 ID 명명 규칙 (예: `KISEC-WTDA-2026-W26-v2`)
- [ ] TLP/심각도 결정
- [ ] 데이터 cutoff 시각 명시
- [ ] KJ 7개 + 신뢰도 작성
- [ ] 3축 중 어느 축에 사건이 속하는지 분류
- [ ] MITRE ATT&CK 매핑 (전체 20개 T-id 이상)
- [ ] Sigma 룰 2~3개
- [ ] Diamond Model 표 1개 이상
- [ ] 한국 특수 정황 (필수)
- [ ] 질적 변화 비교표
- [ ] 위협 행위자 매트릭스 (★ 등급)
- [ ] P0~P3 4단계 권고
- [ ] 분석 한계 명시
- [ ] v1→v2 비교 (보고서 family 진화 시)

## 15. 관련 문서

- `wiki/raw/articles/2026/202606/weekly-deep-analysis-report-20260622-20260627-v2.md` (v2 첫 구현)
- `wiki/concepts/security-news-weekly-report-writer/SKILL.md` (주간 보고서 작성 스킬)
- `wiki/concepts/security-news-weekly-newsletter-template.md` (편집본 템플릿)
- `wiki/concepts/security-news-trend-collection-schema.md` (수집 스키마)
- 외부: https://github.com/gameworkerkim/CYBER-THREAT-INTELLIGENCE-REPORT/blob/main/CTI-2026-0628-DPRK-AI.md (CTI 보고서 구조 차용)

## 16. 메타데이터

- **작성**: 2026-06-27
- **기반 보고서**: CTI-2026-0628-DPRK-AI (Dennis Kim)
- **첫 적용**: weekly-deep-analysis-report-20260622-20260627-v2.md
- **버전**: 1.0.0
- **분량**: ~7KB
- **상태**: 표준 템플릿 확정 — 매주 적용