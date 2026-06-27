---
title: IPS (Intrusion Prevention System) — 침입 방지 시스템
created: 2026-06-13
updated: 2026-06-24
type: concept
tags: [security, glossary, ips, ids, intrusion-prevention, network-security, inline, snort, suricata, ngfw]
sources: [https://ko.wikipedia.org/wiki/침입_차단_시스템, https://ko.wikipedia.org/wiki/침입_탐지_시스템, https://ko.wikipedia.org/wiki/Snort_(소프트웨어), https://ko.wikipedia.org/wiki/방화벽_(네트워킹), https://ko.wikipedia.org/wiki/차세대_방화벽, https://ko.wikipedia.org/wiki/분산_서비스_거부_공격, https://ko.wikipedia.org/wiki/사이버_보안_관제_센터]
confidence: high
---

# IPS (Intrusion Prevention System) — 침입 방지 시스템

## 참고 URL
- [ko.wikipedia.org](https://ko.wikipedia.org/wiki/침입_차단_시스템)
- [ko.wikipedia.org](https://ko.wikipedia.org/wiki/침입_탐지_시스템)
- [ko.wikipedia.org](https://ko.wikipedia.org/wiki/Snort_(소프트웨어))
- [ko.wikipedia.org](https://ko.wikipedia.org/wiki/방화벽_(네트워킹))
- [ko.wikipedia.org](https://ko.wikipedia.org/wiki/차세대_방화벽)
- [ko.wikipedia.org](https://ko.wikipedia.org/wiki/분산_서비스_거부_공격)
- [ko.wikipedia.org](https://ko.wikipedia.org/wiki/사이버_보안_관제_센터)

## Step 1: 단어 직역 및 쉬운 비유

### 1. 약자 풀이
**IPS** = **I**ntrusion **P**revention **S**ystem

| 약자 | 영어 단어 | 직역 | 의미 |
|------|-----------|------|------|
| **I** | **Intrusion** | 침입, 침범 | 허가 없이 내부로 들어오는 행위 |
| **P** | **Prevention** | 방지, 예방, 차단 | 미리 막거나 발생하지 않게 하는 행위 |
| **S** | **System** | 시스템 | 여러 구성 요소가 통합된 체계 |

### 2. 의미 조합
> **네트워크 트래픽 경로에 인라인(inline)으로 배치되어 악의적 트래픽을 실시간 탐지 + 즉시 차단까지 수행하는 보안 시스템 — IDS가 "감시 카메라"라면 IPS는 "감시 카메라 + 자동 잠금 장치"**

### 3. 강력한 비유: "학교 정문 앞에 바리케이드 든 경비원"

| 비유 요소 | 대응 개념 | 설명 |
|-----------|-----------|------|
| **학교 건물** | **네트워크/시스템** | 보호 대상 인프라 |
| **학교 정문 앞에 직접 선 경비원** | **IPS 인라인 배치** | 모든 트래픽이 경비원(IPS)을 통과해야 함 — 우회 불가 |
| **경비실에서 모니터만 보는 경비원(IDS)** | **IDS 포트 미러링** | IDS는 트래픽 복사본만 보고 차단 못 함 |
| **수상한 방문객을 문 앞에서 막음** | **악성 트래픽 차단 (Drop/Reject)** | IPS는 악성 패킷을 네트워크에 들어오기 전에 차단 |
| **일반 방문객은 그냥 통과** | **정상 트래픽 허용 (Pass)** | 오탐(False Positive) 최소화 중요 |
| **수배 전단지 + 직접 제압** | **시그니처 기반 탐지 + 차단** | Snort-inline/Suricata가 알려진 공격을 보고 드롭 |
| **"평소와 다른 행동이야!" → 바로 차단** | **이상 행위 기반 탐지 + 차단** | 제로데이 공격도 프로파일 기반 차단 가능 |
| **경비원이 막았다고 기록** | **로그 + 알림 (Alert)** | 차단 내역을 SOC/SIEM에 전송 |
| **경비원이 실수로 일반인 막음** | **오탐(False Positive)** | 정상 트래픽 차단 → 서비스 장애 — 튜닝이 매우 중요 |

**동작 순서**:
1. 모든 방문객(트래픽)이 경비원(IPS) 앞을 지나야 함 → **인라인 배치**
2. 경비원이 방문객 확인 → 패킷 분석 (L3-L7 전 계층)
3. 수배 전단지 확인 → 시그니처 매칭 (Snort/Suricata 룰)
4. "수상하다!" → 즉시 제압 → 악성 패킷 **Drop/Reject**
5. "괜찮다" → 통과 → 정상 트래픽은 그대로 전달
6. 모든 기록 남김 → 차단/허용 모두 로그 + 알림 전송

**핵심 포인트**: **IDS는 "감시 카메라"** — 도둑 장면을 찍어서 알람만 줌. **IPS는 "감시 카메라 + 전자식 잠금장치"** — 도둑이 들어오는 순간 문이 자동으로 잠김. 하지만 **잘못 잠그면(오탐) 일반 손님도 못 들어옴** → 서비스 중단 발생 가능.

---

## Step 2: 개념 시각화

![IPS 비유 시각화: 네트워크(학교), IPS 센서(경비원이 문 앞에서 통제), 인라인 배치, 정상 트래픽 통과, 악성 트래픽 차단(빨강 X), 시그니처 매칭+차단, 이상행위 감지+자동 차단, IDS와의 차이 강조 - 한글 레이블 포함](https://v3b.fal.media/files/b/0a9e1bdb/1QUABTZ95rZgUzq4rXVrw_ZRGYkHaY.png)

**이미지 설명**:
- **네트워크(학교)** — 보호 대상 인프라
- **IPS 센서(경비원이 문 바로 앞에서 통제)** — **인라인 배치**, 모든 트래픽이 IPS를 통과해야 함
- **정상 트래픽(통과 허용 - 초록)** — 룰 매칭 결과 정상 → 그대로 통과
- **악성 트래픽(차단 - 빨강 X)** — 시그니처/이상치 매칭 → 네트워크 진입 전 차단
- **IDS와의 차이: 탐지 + 능동 차단** — IDS는 모니터만, IPS는 직접 차단
- **시그니처 DB + 정책 규칙** — 알려진 공격 패턴과 차단 정책

> ⚠️ **참고**: 이미지 생성 도구가 PNG 형식으로 반환했습니다. 스킬 요구사항(.jpg/.jpeg)은 현재 도구 제약상 PNG로 대체됩니다.

---

## Step 3: 전문 용어 설명 (Wikipedia 기반)

### 침입 방지 시스템 (Intrusion Prevention System, IPS)

**정의**: 네트워크 트래픽 경로에 **인라인(inline)**으로 배치되어 악의적 트래픽을 **실시간 탐지하고 자동으로 차단(Block/Drop/Reject)**하는 보안 시스템이다. IDS가 수동적(passive) 탐지에 그치는 반면, IPS는 능동적(active) 차단을 수행한다.

---

### IDS vs IPS: 핵심 차이점

| 비교 항목 | IDS (Intrusion Detection) | IPS (Intrusion Prevention) |
|-----------|--------------------------|---------------------------|
| **배치 방식** | 포트 미러링 (SPAN/TAP) — 트래픽 복사본 | **인라인 (Inline)** — 트래픽 경로 상에 직접 위치 |
| **동작** | 수동적(Passive) — 감시 + 경고 | 능동적(Active) — 감시 + 차단 |
| **차단 기능** | ❌ 없음 (알림만) | ✅ 있음 (Drop, Reject, Reset) |
| **장애 영향** | ❌ 없음 — 네트워크 독립적 | ✅ 있음 — IPS 장애 시 네트워크 단절 |
| **지연 시간** | 거의 없음 (복사본 분석) | 증가 (인라인 처리 + 검사) |
| **오탐(FP) 위험** | 낮음 (알림만 → 분석가 검토) | **높음** (잘못 차단 시 서비스 장애) |
| **배치 난이도** | 낮음 | 높음 (Fail-open/Fail-close 설계 필수) |
| **보안 효과** | 사후 분석, 포렌식 | **실시간 차단 — 공격 성공 전에 방어** |
| **대표 도구** | Snort(IDS모드), Zeek | Snort-inline, Suricata(IPS모드), Palo Alto |

### IPS 배치 아키텍처 (Inline)

```
                   ┌─────────────┐
                   │   인터넷     │
                   └──────┬──────┘
                          │
                  ┌───────┴───────┐
                  │    방화벽      │
                  └───────┬───────┘
                          │
            ┌─────────────┴─────────────┐
            │   IPS (인라인 배치)         │ ← 모든 트래픽이 IPS를 통과
            │   ┌──────────────────┐     │    → 분석 + 차단/허용 결정
            │   │  탐지 엔진 + 차단 정책  │     │
            │   └──────────────────┘     │
            └─────────────┬─────────────┘
                          │
                  ┌───────┴───────┐
                  │  내부 네트워크   │
                  ├───────────────┤
                  │  웹 서버       │
                  ├───────────────┤
                  │  DB 서버       │
                  └───────────────┘
```

> **IPS Fail-open / Fail-close 정책**:
> - **Fail-open**: IPS 장애 시 트래픽 우회 허용 — 가용성 우선, 보안 약화
> - **Fail-close**: IPS 장애 시 모든 트래픽 차단 — 보안 우선, 가용성 저하

## 심화 자료
- [[ips-operational-notes]] — 차단 동작, 탐지/차단 방식, 솔루션, 운영 모범 사례

## 관련 위키 링크
- [[ids]] — IDS (Intrusion Detection System) — IPS의 전신, 탐지만 수행하는 수동적 시스템
- [[vpn]] — VPN (가상 사설망) — IPS가 보호하는 네트워크 접근 통로
- [[rce]] — RCE (원격 코드 실행) — IPS가 차단해야 할 가장 위험한 공격 유형
- [[cia]] — CIA Triad (가용성) — IPS 오탐 시 가용성에 직접적 영향

