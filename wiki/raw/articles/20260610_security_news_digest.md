---
sha256: b6ffc7dab0921bae90817eaabc23d5e5943ff7a619a3f1d48f070e81eb00008d
source: ~/.hermes/research/20260610_security_news_digest.md
archived: 2026-06-10
---

# 2026-06-10 보안 뉴스 다이제스트

> 수집일시: 2026-06-10 15:00 KST
> 수집소스: TheHackerNews, Security Affairs, BleepingComputer, HelpNetSecurity, CyberSecurityNews

---

## 1. 🔴 Chrome V8 Zero-Day CVE-2026-11645 — 야생 공격 중

- **CVSS**: 8.8 (High)
- **유형**: V8 JavaScript 엔진의 Out-of-Bounds Read/Write
- **영향**: 원격 공격자가 crafted HTML 페이지로 샌드박스 내 임의 코드 실행
- **패치**: Chrome 149.0.7827.102/.103 (Windows/macOS/Linux)
- **버그바운티**: $55,000 (303f06e3 연구원)
- **비고**: 2026년 5번째 Chrome 제로데이 (CVE-2026-2441, -3909, -3910, -5281 에 이어)
- **Ref**: TheHackerNews

---

## 2. 🔴 Chrome 대규모 패치 — 429개 취약점, 22개 Critical

- Chrome이 한 번에 429개의 보안 취약점 패치
- 이 중 22개는 Critical 등급
- V8, WebGPU(Dawn), 기타 컴포넌트 전반
- **Ref**: CyberSecurityNews

---

## 3. 🔴 LiteLLM CVE-2026-42271 — RCE 연쇄 공격, CISA KEV 등록

- **유형**: 인증 우회 → 원격 코드 실행 (Unauthenticated RCE)
- **영향**: BerriAI LiteLLM (LLM gateway/proxy)
- **상태**: 야생 공격 중, CISA KEV(Known Exploited Vulnerabilities) 등록
- **Ref**: TheHackerNews, HelpNetSecurity

---

## 4. 🔴 Check Point VPN CVE-2026-50751 — IKEv1 패스워드 우회

- **CVSS**: Critical
- **유형**: IKEv1 설정에서 패스워드 우회 가능
- **영향**: Check Point Security Gateway
- **상태**: 야생 공격 중, 랜섬웨어 배포에 활용됨
- **Ref**: TheHackerNews, CyberSecurityNews, Check Point Blog

---

## 5. 🟠 SolarWinds Serv-U CVE-2026-28318 — DoS, CISA KEV 등록

- **유형**: 서비스 거부(DoS)
- **영향**: SolarWinds Serv-U
- **상태**: 야생 공격 중, CISA KEV 추가
- **Ref**: HelpNetSecurity, TheHackerNews

---

## 6. 🟠 Linux nf_tables CVE-2026-23111 — LPE (UAF)

- **CVSS**: 7.8 (High)
- **유형**: nftables `nft_map_catchall_activate()` 의 inverted genmask 체크 → UAF
- **영향**: 로컬 사용자 → 루트 권한 상승
- **패치**: 소스코드에서 `!` 한 글자 제거
- **발견자**: Exodus Intelligence, Oliver Sieber (2025년 초)
- **FuzzingLabs PoC**: 커널 base leak → heap address → ROP chain → `commit_creds(prepare_kernel_cred(0))` → root
- **비고**: 실습 랩 이미 구축 완료 (`~/labs/CVE-2026-23111/`)
- **Ref**: Security Affairs, FuzzingLabs

---

## 7. 🟠 Veeam Backup Server — 신규 RCE

- **유형**: 원격 코드 실행
- **영향**: Veeam 백업 서버
- **위험**: 공격자가 백업 인프라 전체 장악 가능
- **Ref**: BleepingComputer

---

## 8. 🟠 CVE-2026-31431 — Linux "Copy Fail" LPE (클라우드 환경)

- **유형**: 권한 상승, 클라우드 환경 전반 영향
- **발견**: Microsoft
- **영향**: Linux 시스템 전체
- **Ref**: Microsoft, Google News

---

## 9. 🟡 CVE-2026-5281 — Chrome WebGPU Dawn 제로데이

- **유형**: WebGPU (Dawn) 엔진 취약점
- **상태**: 야생 공격 중
- **Ref**: Rescana

---

## 10. 🟡 기타 주목할 뉴스

- **ChatGPhish**: ChatGPT 웹 요약 기능을 피싱표면으로 전환 가능한 취약점
- **GlassWorm Malware**: 개발자 공급망 공격 인프라스트럭처 적발 및 차단
- **npm 악성 패키지**: Claude AI 사용자 디렉토리에서 파일 탈취 (GitHub 활용)
- **Marimo CVE-2026-39987**: 익스플로잇 후 LLM Agent로 post-exploitation 수행
- **FortiClient EMS Critical**: 크리덴셜 스틸러 배포에 악용됨
- **Cisco SD-WAN**: 새로운 root 레벨 문제, 패치 아직 없음
- **Claude Opus**: Zcash 프라이버시 레이어에서 4년간 숨은 취약점 발견
- **Microsoft, Azure 취약점 보고서 reject**: CVE 미발급

---

## 요약 통계

| 구분 | 개수 |
|------|------|
| 야생 공격 중 (Active Exploitation) | 6건 |
| CISA KEV 신규 등록 | 3건 |
| Chrome 관련 | 3건 |
| VPN/게이트웨이 | 1건 |
| Linux 커널 | 2건 |
| 백업/인프라 | 1건 |
| AI 관련 | 3건 |

## 핵심 메시지

1. **Chrome 사용자는 즉시 업데이트** — V8 제로데이 + WebGPU 제로데이 동시 공격 중
2. **Check Point VPN 패치 필수** — IKEv1 우회로 랜섬웨어까지 연계
3. **LiteLLM** 사용 중이라면 즉시 패치 — 인증 없이 RCE
4. **Linux nf_tables CVE-2026-23111** — LPE 실습 가능, 저희 랩에 환경 있음
5. **Veeam 백업 서버** — RCE 위험, 공급망 공격으로 이어질 수 있음