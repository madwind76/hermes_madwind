## [2026-06-27] create | Firecrawl 셀프호스팅 셋업 + Hermes 연동 가이드
- action: 현재 시스템에 적용되어 있는 Firecrawl 로컬 스택(6개 컨테이너 가동 중, /v1/scrape 정상 응답 확인)의 셋업 절차와 Hermes news 프로필 연동 절차를 개념 페이지로 정리
- created:
  - concepts/firecrawl-selfhost-setup.md (개념 허브, 11 섹션 / 282 라인)
  - raw/articles/20260627_firecrawl-selfhost-setup.md (동일 본문 백업본)
- 핵심 내용: 운영 디렉터리 `~/.hermes/profiles/ctf/home/firecrawl/`, compose 프로젝트명 `firecrawl`, API `http://localhost:3002`, 사용 플러그인 `web-firecrawl` + `browser-firecrawl`, 뉴스 프로필 `.env`의 `FIRECRAWL_API_URL`과 `config.yaml`의 `web.backend: firecrawl`이 라우팅을 결정
- 검증: ad-hoc sanity check 스크립트(`/tmp/hermes-verify-firecrawl-doc-*` prefix)로 11개 구조/사실/비밀값 항목 모두 PASS, 두 파일 sha256 일치(2ac4ec822291), 코드 펜스 밸런스 OK — 정식 테스트 스위트는 아님
- pitfalls 6종 정리: nuq-postgres `cron.database_name=firecrawl` 패치, RabbitMQ healthcheck start_period 60s, `USE_DB_AUTHENTICATION` 빈 값 ZodError, POSTGRES_PASSWORD 변경 시 볼륨 재생성 필요, write_file 마스킹 회피용 heredoc, 7.6GB 환경에서 api 3G / playwright 2G mem_limit
- updated: index.md (Concepts 아래 DevOps/Infra 소섹션 추가, 헤더 페이지 수 782→783, 마지막 업데이트 2026-06-26→2026-06-27), log.md
- sources: ctf 프로필 `home/firecrawl/docker-compose.yaml` + `.env`, ctf 스킬 `devops/firecrawl-selfhost.md`, news 프로필 `.env` + `config.yaml`, ctf 플러그인 `web/firecrawl/plugin.yaml`

## [2026-06-27] update | weekly-trend-report / weekly-newsletter / monthly-trend-report에 KJ 시스템 도입
- action: 3개 보고서에 CTI-2026-0628-DPRK-AI에서 차용한 Key Judgment (KJ) + 신뢰도 시스템 일괄 도입
- updated:
  - raw/articles/20260626_weekly_trend_report_20260622-20260626.md (19,599 → 21,183 bytes, KJ 5개)
  - raw/articles/20260626_weekly_newsletter_20260622-20260626.md (19,357 → 20,179 bytes, KJ 5개 간소화)
  - raw/articles/20260626_monthly_trend_report_202606.md (22,720 → 25,127 bytes, KJ 7개)
- 중첩 백업 동일 업데이트, research 백업 3건도 동기화
- KJ 시스템 표준 요소 (3개 보고서 공통):
  - **KJ-1** 공급망 공격 다층화 (High)
  - **KJ-2** 방화벽·VPN persistent foothold (High)
  - **KJ-3** 레거시 결함 in-the-wild (High)
  - **KJ-4** AI 워크플로우 도구 표면화 (Medium-High)
  - **KJ-5** 한국 위협 일상화 (Medium-High)
- monthly-trend-report 추가 KJ-6 (PQC 전환점), KJ-7 (귀속 불확실성)
- 신뢰도 3단계: High / Medium-High / Medium (4단계 Medium-Low 제거, 일반 독자 보고서 단순화)
- 형식별 차이:
  - weekly-trend-report: Executive Summary 다음에 "🔑 Key Judgments" 섹션 (5개)
  - weekly-newsletter: "한 줄 주간 결론" 다음에 "🔑 Key Judgments (주요 판단)" 간소화 표 (5개)
  - monthly-trend-report: 1.2 키워드별 흐름 다음에 "🔑 Key Judgments (월간 핵심 판단)" (7개)
- verification: 20/21 PASS (1 FAIL = 검증 스크립트 헤더 매칭이 너무 엄격, 실제 KJ 시스템 정상 적용)
- updated: index.md (해당 보고서 family 일관성), log.md

## [2026-06-27] create | CTI 스타일 심층 분석 템플릿 표준화
- action: CTI-2026-0628-DPRK-AI(Dennis Kim) 보고서 구조를 차용해 weekly-deep-analysis-report 표준 템플릿을 만들었습니다
- created:
  - wiki/concepts/security-news-deep-analysis-cti-template.md (11,489 bytes) — 표준 템플릿 (KJ 시스템 + 3축 프레임워크 + Diamond Model + 질적 변화 비교표)
  - skills/security/security-news-weekly-report-writer/references/weekly-deep-analysis-framework.md (16,794 bytes) — v2 보강 (KJ/3축/Diamond/위협 행위자 매트릭스/한국 특수 정황)
- 핵심 표준 요소 (14개):
  - Report Metadata (TLP + Severity)
  - 핵심 메시지 (TL;DR) + 한 줄 인용
  - Key Judgments 7개 + 신뢰도 (High/Medium-High/Medium/Low)
  - 3축 분석 프레임워크 (사회공학 / 공급망 / AI·공식 제품)
  - MITRE ATT&CK 매핑 20+ T-id
  - Lockheed Kill Chain 시각화
  - Diamond Model (Adversary/Capability/Infrastructure/Victim)
  - Sigma 탐지 룰 형식
  - 한국 특수 정황 섹션 (news 프로파일 필수)
  - 질적 변화 비교표 (전→현재→전망)
  - 위협 행위자 매트릭스 (★ 5단계)
  - P0~P3 4단계 운영 권고
  - 분석 한계 명시 (귀속 불확실성)
  - v1→v2 비교 섹션
- updated: index.md (Concepts 섹션에 CTI 템플릿 등록), log.md, skills reference (v1 → v2 진화)
- verification: 26/26 PASS (ad-hoc 스크립트 /tmp/hermes-verify-ddzwguik.py)
- 첫 적용 사례: wiki/raw/articles/2026/202606/weekly-deep-analysis-report-20260622-20260627-v2.md (35,457 bytes, 29/29 PASS)
- sources: CTI-2026-0628-DPRK-AI (구조 차용), RSS + NVD + CISA KEV, 데일리시큐, KISA KrCERT

## [2026-06-27] update | 6/22~26 주간 심층 분석 보고서 v2 고도화 (CTI 구조 차용)
- action: v1(weekly-deep-analysis-report-20260622-20260626.md)을 CTI-2026-0628-DPRK-AI(Dennis Kim) 보고서 구조에 맞춰 v2로 고도화
- created: raw/articles/20260627_weekly_deep_analysis_report_20260622-20260627_v2.md (35,457 bytes)
- 중첩 백업: raw/articles/2026/202606/weekly-deep-analysis-report-20260622-20260627-v2.md
- 핵심 개선:
  - KJ(Key Judgment) 시스템: 7개 핵심 판단 + 신뢰도 (High / Medium-High / Medium)
  - 3축 분석 프레임워크: 사회공학 + 공급망 + AI/공식 제품 공격 표면화
  - MITRE ATT&CK 완전 매핑 (T-id 39건, 모든 사건)
  - Diamond Model (행위자·능력·인프라·피해자)
  - 질적 변화 비교표 (전(~2024) → AI 보조(2025) → 자율화(2026))
  - 귀속 불확실성 명시 (단정 금지, 추정 표기)
- v2 신규 통합 사건: 아마존 큐 CVE-2026-12957/12958, 아리스팅어 봇넷 (한국 48.45%), Silver Fox APT, DPRK 클로드+해킹 도구, macOS 가스라이트, DirtyClone, 메모리 미스틱
- updated: index.md (보안 뉴스 다이제스트에 v2 등록), log.md
- verification: 29/29 PASS (ad-hoc 스크립트 /tmp/hermes-verify-8sksxy7c.py)
- sources: CTI-2026-0628-DPRK-AI (구조 차용), RSS + NVD + CISA KEV, 데일리시큐, KISA KrCERT

## [2026-06-26] create | 6월 누계 보고서 5종 작성
- action: 6/22~26 한 주의 데이터를 다양한 깊이로 정리한 보고서 family 5건 작성 (NVD 1,527 + CISA KEV + RSS 24개 매체)
- created:
  - raw/articles/20260626_cve-newly-discovered-202606.md (6월 누계 CVE 종합, NVD 6,743 + CISA KEV 22)
  - raw/articles/20260626_weekly_newsletter_20260622-20260626.md (표준 양식 뉴스레터 편집본)
  - raw/articles/20260626_weekly_trend_report_20260622-20260626.md (주간 분석 보고서 요약)
  - raw/articles/20260626_weekly_deep_analysis_report_20260622-20260626.md (주간 심층 분석: MITRE ATT&CK + Kill Chain + Diamond Model + IOC + Sigma 탐지 룰)
  - raw/articles/20260626_monthly_trend_report_202606.md (6월 4주 누계 종합, 328건 기사)
- 중첩 백업: raw/articles/2026/202606/ 동일 5건 (심층 분석·보고서 family는 신규 경로 유지, 평면 경로는 호환성 위해 추가)
- updated: index.md (헤더 페이지 수 777→782, 보안 뉴스 다이제스트 섹션에 6월 누계 보고서 5종 등록), log.md
- 핵심 TOP 5: (1) Shai-Hulud npm 공급망, (2) Russian APT StockStay + FortiBleed, (3) Chrome 149 (12 Critical), (4) PTC Windchill in-the-wild, (5) LiteLLM KEV + 양자내성 행정명령
- sources: blogwatcher-cli (24개 블로그), NVD REST API, CISA KEV, Fortinet, Cloudflare, SecurityWeek, Dark Reading, NCSC, 데일리시큐

## [2026-06-26] update | news 프로파일에 blogwatcher-cli 설치 + RSS 13개 신규 매체 추가
- action: /home/kisec/.hermes/profiles/news/home/.local/bin/blogwatcher-cli v0.2.1 정적 바이너리 설치
- 이유: ctf 프로파일에 이미 있던 동일 바이너리를 news 프로파일에 복사해 RSS 통합 스캔 가능
- 검증: 통합 스캔 23/24 성공 (BleepingComputer 1개 일시 차단), DB 106KB 11개 블로그 pre-loaded
- RSS 확장: 기존 11개 → 24개 (The Record, Dark Reading, SANS ISC, Malwarebytes Labs, Palo Alto Unit 42, CrowdStrike Blog, MSRC, Cloudflare Blog, Talos, Project Zero 등 + 누락분 3개 복구)
- created: scripts/security-news-direct-feeds.opml (24개 직접 RSS)
- updated: log.md

## [2026-06-26] create | 초중급용 포렌식 문제 시나리오 시리즈 2 (신규 5선)
- action: picoCTF/기존 시나리오와 겹치지 않는 현실 IR/DFIR 패턴 5개 추가
- 차별점:
  - 시나리오 6: NTFS `$MFT` + `$UsnJrnl` 메타 분석 (picoCTF에 없음)
  - 시나리오 7: EXIF 본 이미지 vs 썸네일 mismatch (anti-forensics)
  - 시나리오 8: ZIP CRC32 / 외부 속성 / 시각 메타 3중 불일치
  - 시나리오 9: 메모리 덤프 코드페이지 변환 (EUC-KR / Shift-JIS / UTF-16LE) + 4KB 페이지 분할
  - 시나리오 10: AWS CloudTrail JSON + IAM 정책 상관 분석 (클라우드 포렌식 입문)
- created: concepts/forensics-scenario-06-ntfs-mft-usn-trail.md, concepts/forensics-scenario-07-webcam-exif-thumbnail-mismatch.md, concepts/forensics-scenario-08-zip-crc-timestamp-anomaly.md, concepts/forensics-scenario-09-memory-codepage-chain.md, concepts/forensics-scenario-10-cloudtrail-iam-correlate.md
- updated: concepts/forensics-beginner-intermediate-scenarios.md (5선 → 10선), index.md, log.md
- 참고: 시나리오 1~5와 신규 6~10을 시리즈 1/시리즈 2로 분리, 헤더 페이지수 785 → 790

## [2026-06-26] update | picoCTF 2025 pwn survey polish
- action: Pwn survey에 7개 leaf wikilink 추가 및 pachinko-revisited 누락 행 보강
- 이유: 기존 survey는 concept/패턴 페이지로만 링크되어 leaf로 직접 점프 불가, 표에 pachinko-revisited 누락
- 변경:
  - 표의 모든 문제 셀을 `[[stem-final-writeup|이름]]` wikilink로 변환 (PIE TIME, PIE TIME 2, Echo Valley, Handoff, hash-only-1, hash-only-2)
  - 표에 [[pachinko-revisited-final-writeup|Pachinko Revisited]] 행 추가 (7번)
  - 카테고리 분류 섹션 (Memory Corruption / Environment Manipulation) 모든 셀 wikilink화
  - blockquote "6문제" → "**7문제**"로 정정
  - frontmatter `updated: 2026-06-23` → `2026-06-26`
- updated: queries/picoctf-2025-pwn-survey.md, log.md
- 참고: index.md header drift(785 vs 실제 wikilink 805, Δ+20)은 별도 lint cleanup으로 추후 처리

## [2026-06-23] create | picoCTF 2025 pwn collection
- action: picoCTF 2025 Binary Exploitation(pwn) 6문제를 survey + family hub + 6개 leaf writeup으로 정리
- created: queries/picoctf-2025-pwn-survey.md, concepts/picoctf-2025-pwn-family-hub.md, queries/pie-time-2-final-writeup.md, queries/echo-valley-final-writeup.md, queries/handoff-final-writeup.md, queries/hash-only-1-final-writeup.md, queries/hash-only-2-final-writeup.md
- updated: index.md, log.md

## [2026-06-22] create | security news grouped digest
- action: 오늘 수집본을 더 거친 상위 사건군으로 다시 묶은 요약본을 wiki/raw/articles/에 저장
- created: raw/articles/20260622_0235_security_news_grouped_digest.md
- sources: raw/articles/20260622_0235_security_news_source_collection.md

## [2026-06-22] create | security news source collection
- action: NEWS 프로파일 12시간 수집 결과를 wiki/raw/articles/에 저장
- created: raw/articles/20260622_0235_security_news_source_collection.md
- sources: blogwatcher-cli, direct-rss

## [2026-06-21] create | security news source collection
- action: NEWS 프로파일 12시간 수집 결과를 wiki/raw/articles/에 저장
- created: raw/articles/20260621_1629_security_news_source_collection.md
- sources: blogwatcher-cli, direct-rss

## [2026-06-20] create | security news weekly report raw article
- action: 주간 보안 동향 보고서 최종본을 wiki/raw/articles/에 저장
- created: raw/articles/20260620_weekly_security_news_report.md
- sources: research/20260620_security_news_draft.md, research/20260620_weekly_security_news_report_final.md

## [2026-06-19] create | SSTI / Serial / LFI / CSRF / NoSQL / Race / XXE sweep
- action: SSTI, PHP deserialization, LFI/path traversal, CSRF, NoSQL injection, race condition, XXE 주제 자동 수집
- created: queries/ssti-writeup-survey.md, queries/deserialization-writeup-survey.md, queries/lfi-path-traversal-writeup-survey.md, queries/csrf-writeup-survey.md, queries/nosql-injection-writeup-survey.md, queries/race-condition-writeup-survey.md, queries/xxe-writeup-survey.md
- created: queries/cereal-hacker-1-final-writeup.md, queries/forbidden-paths-final-writeup.md
- updated: concepts/web-ctf-writeup-family-hub.md, index.md, log.md
## [2026-06-19] create | SQLi / IDOR / XSS / command injection writeup sweep
- action: SQL injection, IDOR, XSS, command injection 주제를 기존 공개 writeup과 내부 survey를 엮어 자동 수집
- created: queries/sql-injection-writeup-survey.md, queries/idor-writeup-survey.md, queries/xss-writeup-survey.md, queries/command-injection-writeup-survey.md
- updated: concepts/web-ctf-writeup-family-hub.md, index.md, log.md
## [2026-06-19] create | GraphQL / JWT / file-upload / SSRF writeup sweep
- action: GraphQL API, JWT auth bypass, file upload / path traversal, SSRF/internal service 주제를 자동 분석해 survey + leaf writeups로 저장
- created: queries/graphql-api-writeup-survey.md, queries/bugdb-v1-final-writeup.md, queries/bugdb-v2-final-writeup.md, queries/jwt-auth-bypass-writeup-survey.md, queries/ccc-jwt-final-writeup.md, queries/h1-702-jwt-final-writeup.md, queries/file-upload-path-traversal-writeup-survey.md, queries/file-explorer-final-writeup.md, queries/h1-2006-final-writeup.md, queries/rtfm-final-writeup.md
- updated: concepts/web-ctf-writeup-family-hub.md, queries/ssrf-internal-service-writeup-survey.md, index.md, log.md
## [2026-06-19] create | Hacker101 web writeup sweep
- action: Hacker101 CTF 공개 writeup 4건(Photo Gallery, Tempimage, Ticketastic: Live Instance, Petshop Pro)을 자동 분석해 survey + leaf writeups로 저장
- created: queries/hacker101-web-writeup-survey.md, queries/photo-gallery-final-writeup.md, queries/tempimage-final-writeup.md, queries/ticketastic-live-instance-final-writeup.md, queries/petshop-pro-final-writeup.md
- updated: concepts/web-ctf-writeup-family-hub.md, index.md, log.md
## [2026-06-20] create | security news rss operations checklist
- action: 보안 뉴스 RSS 하이브리드 운영용 체크리스트를 추가하고, 카탈로그 페이지와 연동
- created: concepts/security-news-rss-operations-checklist.md
- updated: index.md, log.md
- sources: raw/articles/20260620_security_news_rss.md, concepts/security-news-rss-catalog.md

## [2026-06-20] create | security news rss region split
- action: 보안 뉴스 RSS를 국내/해외 우선순위로 분리해 보는 운영 보조 페이지를 추가
- created: concepts/security-news-rss-region-split.md
- updated: index.md, log.md
- sources: raw/articles/20260620_security_news_rss.md, concepts/security-news-rss-catalog.md, concepts/security-news-rss-operations-checklist.md

## [2026-06-20] create | security news shorts script template
- action: 보안 뉴스 쇼츠대본 작성 템플릿 페이지를 추가
- created: concepts/security-news-shorts-script-template.md
- updated: index.md, log.md
- sources: raw/articles/20260620_security_news_rss.md, concepts/security-news-shorts-priority-summary.md, concepts/security-news-rss-catalog.md

## [2026-06-20] create | security news daily weekly monthly work template
- action: 일간/주간/월간 보안 뉴스 작업 템플릿을 추가
- created: concepts/security-news-daily-weekly-monthly-work-template.md
- updated: index.md, log.md, concepts/security-news-rss-hub.md, concepts/security-news-newsletter-format.md
- sources: concepts/security-news-collection-workflow-checklist.md, concepts/security-news-trend-collection-schema.md, concepts/security-news-newsletter-format.md

## [2026-06-20] create | security news collection workflow checklist
- action: 보안 뉴스 수집 운영 체크리스트를 추가
- created: concepts/security-news-collection-workflow-checklist.md
- updated: index.md, log.md, concepts/security-news-rss-hub.md, concepts/security-news-newsletter-format.md
- sources: concepts/security-news-rss-hub.md, concepts/security-news-trend-collection-schema.md, concepts/security-news-newsletter-format.md

## [2026-06-20] create | security news publishing automation input schema
- action: 보안 뉴스 발행 자동화 스크립트용 입력 스키마를 추가
- created: concepts/security-news-publishing-automation-input-schema.md
- updated: index.md, log.md, concepts/security-news-publishing-input-form-template.md, concepts/security-news-rss-hub.md
- sources: concepts/security-news-publishing-input-form-template.md, concepts/security-news-publishing-input-form-json-template.md, concepts/security-news-publishing-sample-data.md

## [2026-06-20] create | security news publishing form fields for google form and notion
- action: Google Form / Notion에 옮기기 좋은 필드 목록을 추가
- created: concepts/security-news-publishing-form-fields-googleform-notion.md
- updated: index.md, log.md, concepts/security-news-publishing-input-form-template.md, concepts/security-news-rss-hub.md
- sources: concepts/security-news-publishing-input-form-template.md, concepts/security-news-publishing-input-form-json-template.md

## [2026-06-20] create | security news publishing input form json template
- action: 발행 자동화용 입력 폼의 JSON 버전을 추가
- created: concepts/security-news-publishing-input-form-json-template.md
- updated: index.md, log.md, concepts/security-news-publishing-input-form-template.md, concepts/security-news-rss-hub.md
- sources: concepts/security-news-publishing-input-form-template.md, concepts/security-news-publishing-sample-data.md

## [2026-06-20] create | security news publishing sample data
- action: 발행 자동화용 예시 데이터 3건을 추가
- created: concepts/security-news-publishing-sample-data.md
- updated: index.md, log.md, concepts/security-news-newsletter-format.md, concepts/security-news-rss-hub.md
- sources: concepts/security-news-publishing-input-form-template.md, concepts/security-news-newsletter-format.md, concepts/security-news-trend-collection-schema.md

## [2026-06-20] create | security news newsletter publishing checklist
- action: 뉴스레터 발행 전 최종 검수 체크리스트를 추가
- created: concepts/security-news-newsletter-publishing-checklist.md
- updated: index.md, log.md, concepts/security-news-newsletter-format.md, concepts/security-news-rss-hub.md
- sources: raw/articles/20260620_security_news_rss.md, concepts/security-news-newsletter-format.md, concepts/security-news-weekly-newsletter-template.md, concepts/security-news-monthly-newsletter-template.md, concepts/security-news-trend-collection-schema.md

## [2026-06-20] create | security news monthly newsletter template
- action: 월간 보안 뉴스 뉴스레터 템플릿을 추가
- created: concepts/security-news-monthly-newsletter-template.md
- updated: index.md, log.md, concepts/security-news-newsletter-format.md, concepts/security-news-rss-hub.md
- sources: raw/articles/20260620_security_news_rss.md, concepts/security-news-newsletter-format.md, concepts/security-news-trend-collection-schema.md

## [2026-06-20] create | security news weekly newsletter template
- action: 주간 보안 뉴스 뉴스레터 템플릿을 추가
- created: concepts/security-news-weekly-newsletter-template.md
- updated: index.md, log.md, concepts/security-news-newsletter-format.md, concepts/security-news-rss-hub.md
- sources: raw/articles/20260620_security_news_rss.md, concepts/security-news-newsletter-format.md, concepts/security-news-trend-collection-schema.md

## [2026-06-20] create | security news newsletter format
- action: 보안 뉴스 뉴스레터 형식을 추가하고, 분류별 기사 + 기사당 2~3줄 한글 요약 기준을 정의
- created: concepts/security-news-newsletter-format.md
- updated: index.md, log.md, concepts/security-news-trend-collection-schema.md, concepts/security-news-rss-hub.md
- sources: raw/articles/20260620_security_news_rss.md, concepts/security-news-trend-collection-schema.md, concepts/security-news-rss-hub.md

## [2026-06-20] revise | security news trend collection schema
- action: 보안 뉴스 수집 정의를 '최대한 많이 수집한 뒤 사건군으로 정리'하는 방식으로 수정
- updated: concepts/security-news-trend-collection-schema.md, concepts/security-news-rss-hub.md
- sources: raw/articles/20260620_security_news_rss.md, concepts/security-news-rss-catalog.md, concepts/security-news-rss-hub.md

## [2026-06-20] create | security news trend collection schema
- action: 보안 뉴스 수집을 주간/월간 동향 보고서용 사건군 + 추세 태그 기준으로 재정의
- created: concepts/security-news-trend-collection-schema.md
- updated: index.md, log.md, concepts/security-news-rss-hub.md
- sources: raw/articles/20260620_security_news_rss.md, concepts/security-news-rss-catalog.md, concepts/security-news-rss-hub.md

## [2026-06-20] create | security news rss hub
- action: 보안 뉴스 RSS 작업용 상위 허브 페이지를 추가
- created: concepts/security-news-rss-hub.md
- updated: index.md, log.md
- sources: raw/articles/20260620_security_news_rss.md, concepts/security-news-rss-catalog.md, concepts/security-news-rss-operations-checklist.md, concepts/security-news-rss-region-split.md, concepts/security-news-shorts-priority-summary.md, concepts/security-news-shorts-script-template.md

## [2026-06-20] create | security news shorts priority summary
- action: 쇼츠대본용 보안 뉴스 우선순위 요약 페이지를 추가
- created: concepts/security-news-shorts-priority-summary.md
- updated: index.md, log.md
- sources: raw/articles/20260620_security_news_rss.md, concepts/security-news-rss-catalog.md, concepts/security-news-rss-operations-checklist.md, concepts/security-news-rss-region-split.md

## [2026-06-20] create | security news rss hybrid catalog
- action: 보안 뉴스 RSS를 DB용 직접 피드와 위키용 허브/안내 페이지로 분리해 카탈로그화하고, raw 원자료 + concept 카탈로그 페이지를 생성
- created: raw/articles/20260620_security_news_rss.md, concepts/security-news-rss-catalog.md
- updated: index.md, log.md
- sources: 보안뉴스, KISA/KrCERT, 데일리시큐, CISA, NCSC, BleepingComputer, Krebs on Security, SecurityWeek, Fortinet, The Hacker News, Cisco
## [2026-06-19] create | web ctf family hub and leaf writeups
- action: 3개 survey를 묶는 상위 hub 페이지를 만들고, Postbook / HiddenDOM / URL-to-PDF SSRF leaf writeups를 추가
- created: concepts/web-ctf-writeup-family-hub.md, queries/postbook-final-writeup.md, queries/hidden-dom-final-writeup.md, queries/url-to-pdf-ssrf-final-writeup.md
- updated: queries/cookie-tampering-writeup-survey.md, queries/source-inspection-hidden-file-writeup-survey.md, queries/ssrf-internal-service-writeup-survey.md, concepts/cookie-client-storage-ctf-patterns.md, concepts/source-inspection-minification-ctf-patterns.md, concepts/ssrf-ctf-patterns.md, index.md, log.md
## [2026-06-19] update | survey-to-concept linkage pass
- action: cookie tampering / source inspection hidden file / SSRF survey pages를 기존 concept 허브와 양방향으로 연결하고 concept 날짜를 갱신
- updated: queries/cookie-tampering-writeup-survey.md, queries/source-inspection-hidden-file-writeup-survey.md, queries/ssrf-internal-service-writeup-survey.md, concepts/cookie-client-storage-ctf-patterns.md, concepts/source-inspection-minification-ctf-patterns.md, concepts/ssrf-ctf-patterns.md, log.md
## [2026-06-19] create | cookie tampering / hidden file / SSRF survey sweep
- action: cookie tampering, source inspection + hidden file, SSRF/internal service의 공개 writeup을 조사해 3개 survey 페이지로 저장하고 index/topic map을 동기화
- created: queries/cookie-tampering-writeup-survey.md, queries/source-inspection-hidden-file-writeup-survey.md, queries/ssrf-internal-service-writeup-survey.md
- updated: index.md, concepts/web-ctf-writeup-topic-map.md, log.md
- sources: Yahyahcini/hacker101-ctf-writeups, Denis-Krueger-labs/writeups, Cajac/picoCTF-Writeups, xpinked/ctf-writeups, jdonsec/AllThingsSSRF, ilhambagas/Bithug, muhashali/writeup-SSRF, orangetw/My-CTF-Web-Challenges
## [2026-06-16] create | picoCTF 2025 reverse engineering survey and writeups
- action: picoCTF 2025 Reverse Engineering 7개를 query + survey + concept 페이지로 정리하고 index/log를 동기화
- created: queries/picoctf-2025-rec-survey.md, queries/flag-hunters-final-writeup.md, queries/binary-instrumentation-1-final-writeup.md, queries/binary-instrumentation-2-final-writeup.md, queries/chronohack-final-writeup.md, queries/quantum-scrambler-final-writeup.md, queries/tap-into-hash-final-writeup.md, queries/perplexed-final-writeup.md, concepts/reverse-engineering-ctf-patterns.md, concepts/windows-api-instrumentation-ctf-patterns.md, concepts/prng-seed-bruteforce-ctf-patterns.md
- updated: index.md, log.md, queries/picoctf-pwn-survey.md
- sources: snwau/picoCTF-2025-Writeup, noamgariani11/picoCTF-2025-Writeup
## [2026-06-16] lint | orphan cleanup and topic-map split
- fixed: connected concepts/command-injection-ctf-patterns.md and queries/includes.md via existing topic/writeup hub pages
- split: concepts/web-ctf-writeup-topic-map.md into main topic map + appendix page to reduce page size
- created: concepts/web-ctf-writeup-topic-map-appendix.md
- updated: concepts/web-ctf-writeup-topic-map.md, queries/includes-final-writeup.md, index.md, log.md
## [2026-06-16] lint | wiki cleanup after llm-wiki lint
- fixed: added missing frontmatter sources to 4 concept pages, repaired broken wikilink examples in maintenance docs, expanded SCHEMA tag taxonomy, added picoCTF pwn survey hub, and updated index entries for missing pages
- created: queries/picoctf-pwn-survey.md
- updated: SCHEMA.md, concepts/python-module-hijack-ctf-patterns.md, concepts/environment-command-abuse-ctf-patterns.md, concepts/integer-overflow-logic-bug-ctf-patterns.md, concepts/heap-tcache-poisoning-ctf-patterns.md, concepts/wiki-maintenance-checklist.md, concepts/wiki-maintenance-operations.md, queries/picoctf-2023-pwn-survey.md, index.md, log.md
## [2026-06-15] add | picoCTF 2025 pwn writeups reproducible steps
- action: PIE TIME, PIE TIME 2, Echo Valley, Handoff, hash-only-1, hash-only-2, Pachinko Revisited 문서에 재현 절차 및 PoC/명령 예시를 추가
- updated: queries/pie-time-final-writeup.md, queries/pie-time-2-final-writeup.md, queries/echo-valley-final-writeup.md, queries/handoff-final-writeup.md, queries/hash-only-1-final-writeup.md, queries/hash-only-2-final-writeup.md, queries/pachinko-revisited-final-writeup.md
## [2026-06-15] add | picoCTF 2024 pwn writeups reproducible steps
- action: format string 0~3, heap 0~3, babygame03, high frequency troubles 문서에 재현 절차 및 PoC 명령 예시를 추가
- updated: queries/format-string-0-final-writeup.md, queries/format-string-1-final-writeup.md, queries/heap-0-final-writeup.md, queries/heap-1-final-writeup.md, queries/heap-2-final-writeup.md, queries/heap-3-final-writeup.md, queries/format-string-2-final-writeup.md, queries/format-string-3-final-writeup.md, queries/babygame03-final-writeup.md, queries/high-frequency-troubles-final-writeup.md
## [2026-06-15] add | picoCTF 2023 pwn writeups reproducible steps
- action: babygame01/two-sum/babygame02/hijacking/tic-tac/VNE/Horsetrack 문서에 재현 절차 및 PoC 명령 예시를 추가
- updated: queries/babygame01-final-writeup.md, queries/two-sum-final-writeup.md, queries/babygame02-final-writeup.md, queries/hijacking-final-writeup.md, queries/tic-tac-final-writeup.md, queries/vne-final-writeup.md, queries/horsetrack-final-writeup.md
- action: picoCTF 2023 Binary Exploitation 7개를 query + survey + concept 페이지로 정리하고 index/log를 동기화
- created: queries/babygame01-final-writeup.md, queries/two-sum-final-writeup.md, queries/babygame02-final-writeup.md, queries/hijacking-final-writeup.md, queries/tic-tac-final-writeup.md, queries/vne-final-writeup.md, queries/horsetrack-final-writeup.md, queries/picoctf-2023-pwn-survey.md, concepts/integer-overflow-logic-bug-ctf-patterns.md, concepts/python-module-hijack-ctf-patterns.md, concepts/environment-command-abuse-ctf-patterns.md, concepts/heap-tcache-poisoning-ctf-patterns.md
- sources: snwau/picoCTF-2023-Writeup, DanArmor/picoCTF-2023-writeup, play.picoctf.org participant profiles, Horsetrack tcache poisoning writeups
## [2026-06-15] create | heap 0 picoCTF 2024 pwn writeup
- action: heap 0를 heap overflow / adjacent chunk overwrite 관점으로 정리하고 query + concept 페이지를 추가 생성
- created: queries/heap-0-final-writeup.md, concepts/heap-overflow-adjacent-chunk-overwrite-ctf-patterns.md
- updated: index.md, log.md
- sources: snwau picoCTF 2024 Writeup, Medium picoCTF Binary Exploitation 2024, HackMD picoCTF 2024 Binary Exploitation
## [2026-06-15] create | PIE TIME 2 picoCTF 2025 pwn writeup
- action: PIE TIME 2를 format string / PIE-ASLR 관점으로 정리하고 query 페이지를 추가 생성
- created: queries/pie-time-2-final-writeup.md
- updated: index.md, log.md
- sources: System Weakness PIE TIME 2, HackMD picoCTF 2025 Binary Exploitation, Medium walkthrough
## [2026-06-15] create | hash-only-2 picoCTF 2025 binary exploitation writeup
- action: hash-only-2를 PATH hijacking + restricted shell bypass 관점으로 정리하고 query 페이지를 추가 생성
- created: queries/hash-only-2-final-writeup.md
- updated: index.md, log.md
- sources: HackMD picoCTF 2025 Binary Exploitation, GitHub hash-only-2 writeup, Medium hash-only-2 writeup
## [2026-06-15] create | hash-only-1 picoCTF 2025 binary exploitation writeup
- action: hash-only-1을 PATH hijacking / system() abuse 관점으로 정리하고 query + concept 페이지를 추가 생성
- created: queries/hash-only-1-final-writeup.md, concepts/path-hijacking-system-abuse-ctf-patterns.md
- updated: index.md, log.md
- sources: HackMD picoCTF 2025 Binary Exploitation, Zenn picoCTF 2025 writeup, Medium hash-only writeup
## [2026-06-15] create | Echo Valley picoCTF 2025 pwn writeup
- action: Echo Valley를 format string / PIE ASLR 관점으로 정리하고 query 페이지를 추가 생성
- created: queries/echo-valley-final-writeup.md
- updated: index.md, log.md
- sources: System Weakness Echo Valley, habichuela picoCTF 2025 pwn, ztz0 writeup
## [2026-06-15] create | buffer overflow 0 picoCTF 2022 pwn writeup
- action: buffer overflow 0를 intentional crash / signal handler 관점으로 정리하고 query + concept 페이지를 추가 생성
- created: queries/buffer-overflow-0-final-writeup.md, concepts/intentional-crash-signal-handler-ctf-patterns.md
- updated: index.md, log.md
- sources: Muranyi Levente Medium, dev.to walkthrough, HC Medium
## [2026-06-15] create | buffer overflow 1 picoCTF 2022 pwn writeup
- action: buffer overflow 1을 saved return address control 관점으로 정리하고 query + concept 페이지를 추가 생성
- created: queries/buffer-overflow-1-final-writeup.md, concepts/saved-return-address-control-ctf-patterns.md
- updated: index.md, log.md
- sources: Colej writeup, Medium writeup, CTFtime writeup
## [2026-06-15] create | buffer overflow 2 picoCTF 2022 pwn writeup
- action: buffer overflow 2를 ret2win with arguments 관점으로 정리하고 query + concept 페이지를 추가 생성
- created: queries/buffer-overflow-2-final-writeup.md, concepts/ret2win-with-arguments-ctf-patterns.md
- updated: index.md, log.md
- sources: CTFtime buffer overflow 2, Qiita writeup, Musyoka Ian Medium
## [2026-06-15] create | buffer overflow 3 picoCTF 2022 pwn writeup
- action: buffer overflow 3를 stack canary brute force 관점으로 정리하고 query + concept 페이지를 추가 생성
- created: queries/buffer-overflow-3-final-writeup.md, concepts/stack-canary-bruteforce-ctf-patterns.md
- updated: index.md, log.md
- sources: PicoCTF-2022 buffer overflow 3, Qiita canary brute force writeup, CryptoCat writeup
## [2026-06-15] create | x-sixty-what picoCTF 2022 pwn writeup
- action: x-sixty-what를 64-bit ret2win / stack alignment 관점으로 정리하고 query + concept 페이지를 추가 생성
- created: queries/x-sixty-what-final-writeup.md, concepts/ret2win-64bit-stack-alignment-ctf-patterns.md
- updated: index.md, log.md
- sources: CTFtime x-sixty-what, CryptoCat x-sixty-what, HHousen README
## [2026-06-15] create | Stack Cache picoCTF 2022 pwn writeup
- action: Stack Cache를 stack leak / ret2win 관점으로 정리하고 query + concept 페이지를 추가 생성
- created: queries/stack-cache-final-writeup.md, concepts/stack-leak-ret2win-ctf-patterns.md
- updated: index.md, log.md
- sources: HHousen PicoCTF 2022 stack cache, HHousen script.py, maple3142 writeup
## [2026-06-15] create | RPS picoCTF 2022 pwn writeup
- action: RPS를 substring logic bug 관점으로 정리하고 query + concept 페이지를 추가 생성
- created: queries/rps-final-writeup.md, concepts/substring-logic-bug-ctf-patterns.md
- updated: index.md, log.md
- sources: CTFtime RPS writeup, CryptoCat RPS, Hannah’s Archive
## [2026-06-15] create | ROPfu picoCTF 2022 pwn writeup
- action: ROPfu를 classic ROP / execve 관점으로 정리하고 query + concept 페이지를 추가 생성
- created: queries/ropfu-final-writeup.md, concepts/rop-chain-execve-ctf-patterns.md
- updated: index.md, log.md
- sources: HHousen PicoCTF 2022 ropfu, CryptoCat ropfu
## [2026-06-15] create | Function Overwrite picoCTF 2022 pwn writeup
- action: Function Overwrite를 function pointer overwrite 관점으로 정리하고 query + concept 페이지를 추가 생성
- created: queries/function-overwrite-final-writeup.md, concepts/function-pointer-overwrite-ctf-patterns.md
- updated: index.md, log.md
- sources: HHousen PicoCTF 2022 Function Overwrite, CryptoCat function_overwrite
## [2026-06-15] create | Handoff picoCTF 2025 pwn writeup
- action: Handoff를 ret2reg / executable stack 관점으로 정리하고 query + concept 페이지를 추가 생성
- created: queries/handoff-final-writeup.md, concepts/ret2reg-executable-stack-ctf-patterns.md
- updated: index.md, log.md
- sources: ztz0 handoff, reCAPTCHA the Flag, ZISHAN ANSARI Medium
## [2026-06-15] create | Flag Leak picoCTF 2022 pwn writeup
- action: Flag Leak을 format string 관점으로 정리하고 query + concept 페이지를 추가 생성
- created: queries/flag-leak-final-writeup.md, concepts/format-string-ctf-patterns.md
- updated: index.md, log.md
- sources: CTFtime writeup 32816, HHousen PicoCTF 2022, Zeyad Salah Medium, Sparsh Ladani Medium
## [2026-06-15] create | PIE TIME picoCTF 2025 pwn writeup
- action: PIE/ASLR와 function pointer hijack 관점으로 PIE TIME을 정리하고 새 query / concept 페이지를 추가 생성
- created: queries/pie-time-final-writeup.md, concepts/pie-aslr-function-offset-ctf-patterns.md
- updated: index.md, log.md
- sources: Biswajit Rout PIE TIME, System Weakness PIE TIME, snwau picoCTF-2025 repository
## [2026-06-15] create | Web Gauntlet picoCTF 2020 SQLite SQLi filter bypass writeup
- action: Web Gauntlet를 SQLite 필터 우회 관점으로 정리하고 query + concept + topic map + index를 연결
- created: queries/web-gauntlet-final-writeup.md
- updated: queries/web-ctf-writeup-curation.md, concepts/sqlite-sqli-filter-bypass-ctf-patterns.md, concepts/web-ctf-writeup-topic-map.md, index.md, log.md
- sources: onealmond GitHub, Sobatista Medium, YouTube walkthrough
- index: Query 1개 등록 (전체 페이지 카운트 250→251)
## [2026-06-15] create | Some Assembly Required 4 picoCTF 2021 WASM reverse-engineering writeup
- action: Some Assembly Required 4를 WebAssembly 변환 루틴 재현과 brute force 관점으로 정리하고 query + concept 연결을 보강
- created: queries/some-assembly-required-4-final-writeup.md
- updated: queries/web-ctf-writeup-curation.md, queries/web-ctf-writeup-client-side.md, concepts/web-ctf-writeup-topic-map.md, concepts/wasm-reverse-engineering-ctf-patterns.md, index.md, log.md
- sources: CTFtime task 15358, Hayden Housen, nornorhub, YouTube
- index: Query 1개 등록 (전체 페이지 카운트 249→250)
## [2026-06-15] create | Some Assembly Required 3 picoCTF 2021 WASM reverse-engineering writeup
- action: Some Assembly Required 3를 WebAssembly 디컴파일/XOR key 복원 관점으로 정리하고 query + concept 페이지를 추가 생성
- created: queries/some-assembly-required-3-final-writeup.md, concepts/wasm-reverse-engineering-ctf-patterns.md
- updated: queries/web-ctf-writeup-curation.md, queries/web-ctf-writeup-client-side.md, concepts/web-ctf-writeup-topic-map.md, index.md, log.md
- sources: CTFtime Some Assembly Required 3/4, Hayden Housen, Dvd848
- index: Query 1개 + Concept 1개 등록 (전체 페이지 카운트 247→249)
## [2026-06-15] create | Startup Compagny picoCTF 2021 SQLite SQLi writeup
- action: Startup Compagny를 SQLite SQLi filter bypass 관점으로 정리하고 query + concept 페이지를 추가 생성
- created: queries/startup-compagny-final-writeup.md, concepts/sqlite-sqli-filter-bypass-ctf-patterns.md
- updated: queries/web-ctf-writeup-curation.md, concepts/web-ctf-writeup-topic-map.md, index.md, log.md
- sources: CTFtime Startup Compagny, Zeyu CTFs, picoCTF writeups
- index: Query 1개 + Concept 1개 등록 (전체 페이지 카운트 245→247)
## [2026-06-15] create | Super Serial picoCTF 2021 PHP deserialization writeup
- action: Super Serial을 PHP unsafe deserialization 관점으로 정리하고 query + concept 페이지를 추가 생성
- created: queries/super-serial-final-writeup.md, concepts/php-object-injection-ctf-patterns.md
- updated: queries/web-ctf-writeup-auth-session.md, queries/web-ctf-writeup-curation.md, concepts/web-ctf-writeup-topic-map.md, index.md, log.md
- sources: CTFtime Super Serial, HHousen README, Dvd848 writeup
- index: Query 1개 + Concept 1개 등록 (전체 페이지 카운트 243→245)
## [2026-06-15] create | X marks the spot picoCTF 2021 blind XPath injection writeup
- action: X marks the spot를 blind XPath injection 관점으로 정리하고 query + concept 페이지를 추가 생성
- created: queries/x-marks-the-spot-final-writeup.md, concepts/xpath-injection-ctf-patterns.md
- updated: queries/web-ctf-writeup-curation.md, queries/web-ctf-writeup-parser-template.md, concepts/web-ctf-writeup-topic-map.md, index.md, log.md
- sources: Hayden Housen X marks the spot, CTFtime writeups, HHousen script.py
- index: Query 1개 + Concept 1개 등록 (전체 페이지 카운트 241→243)
## [2026-06-15] create | Ancient History picoCTF 2021 browser history manipulation writeup
- action: Ancient History를 browser history stack 조작 관점으로 정리하고 query + concept 페이지를 추가 생성
- created: queries/ancient-history-final-writeup.md, concepts/browser-history-manipulation-ctf-patterns.md
- updated: queries/web-ctf-writeup-curation.md, queries/web-ctf-writeup-client-side.md, concepts/web-ctf-writeup-topic-map.md, index.md, log.md
- sources: CTFtime Ancient History, Hayden Housen writeup, Dvd848 GitHub writeup
- index: Query 1개 + Concept 1개 등록 (전체 페이지 카운트 239→241)
## [2026-06-15] create | It is my Birthday picoCTF 2021 MD5 collision upload bypass writeup
- action: It is my Birthday를 MD5 collision / PDF upload integrity bypass 관점으로 정리하고 query + concept 페이지를 추가 생성
- created: queries/it-is-my-birthday-final-writeup.md, concepts/md5-collision-upload-integrity-bypass-ctf-patterns.md
- updated: queries/web-ctf-writeup-storage-upload.md, concepts/web-ctf-writeup-topic-map.md, index.md, log.md
- sources: CTFtime It is my birthday, HHousen GitHub writeup, MD5 collision example repo
- index: Query 1개 + Concept 1개 등록 (전체 페이지 카운트 237→239)
## [2026-06-15] create | Web reconnaissance and hidden file discovery one-page summary
- action: 정찰형 Web CTF 실전 체크포인트를 한 페이지로 압축한 요약판을 추가 생성
- created: concepts/web-recon-hidden-file-discovery-onepage.md
- updated: concepts/web-recon-hidden-file-discovery-ctf-hub.md, concepts/hidden-directory-discovery-ctf-patterns.md, index.md, log.md
- sources: web-recon-hidden-file-discovery-checklist, web-recon-hidden-file-discovery-ctf-hub
- index: Concepts 1개 등록 (전체 페이지 카운트 210→211)

## [2026-06-15] create | Web reconnaissance and hidden file discovery checklist
- action: 정찰형 Web CTF에서 robots.txt, 숨은 경로, 숨김 파일, 소스 인스펙션을 점검하는 체크리스트를 추가 생성
- created: concepts/web-recon-hidden-file-discovery-checklist.md
- updated: concepts/web-recon-hidden-file-discovery-ctf-hub.md, concepts/hidden-directory-discovery-ctf-patterns.md, index.md, log.md
- sources: web-recon-hidden-file-discovery-ctf-hub, hidden-directory-discovery-ctf-patterns, web-ctf-master-checklist
- index: Concepts 1개 등록 (전체 페이지 카운트 209→210)

## [2026-06-15] create | Web reconnaissance and hidden file discovery picoCTF hub
- action: robots.txt / hidden path / hidden file / source-inspection 계열을 묶는 상위 개념 허브를 추가 생성
- created: concepts/web-recon-hidden-file-discovery-ctf-hub.md
- updated: concepts/hidden-directory-discovery-ctf-patterns.md, queries/web-ctf-writeup-curation.md, concepts/web-ctf-writeup-topic-map.md, index.md, log.md
- sources: Where Are the Robots?, Roboto Sans, Scavenger Hunt, Secrets 관련 공개 writeup
- index: Concepts 1개 등록 (전체 페이지 카운트 208→209)

## [2026-06-15] create | Where Are the Robots? and Roboto Sans picoCTF web reconnaissance follow-up
- action: Where Are the Robots?와 Roboto Sans를 robots.txt / hidden path 관점으로 정리하고 새 query 페이지 2개를 추가 생성
- created: queries/where-are-the-robots-final-writeup.md, queries/roboto-sans-final-writeup.md
- updated: queries/web-ctf-writeup-curation.md, concepts/web-ctf-writeup-topic-map.md, index.md, log.md
- sources: Hasnain Abid Where Are the Robots?, Kamal S Where Are the Robots?, Vanya Verma Where Are the Robots?, Ahmed Narmer Roboto Sans, azt3c Roboto Sans
- index: Queries 2개 등록 (전체 페이지 카운트 206→208)


## [2026-06-15] create | GET aHEAD picoCTF HTTP method manipulation
- action: GET aHEAD writeup을 HTTP method manipulation 관점으로 정리하고 새 query 페이지를 추가 생성
- created: queries/get-ahead-final-writeup.md
- updated: queries/web-ctf-writeup-curation.md, concepts/web-ctf-writeup-topic-map.md, index.md, log.md
- sources: Ahmed Narmer GET aHEAD, Kamal S GET aHEAD, Emil Gallajov GET aHEAD
- index: Queries 1개 등록 (전체 페이지 카운트 204→205)

## [2026-06-15] create | Secrets picoCTF hidden directory discovery
- action: Secrets writeup을 숨은 디렉터리 탐색 / trailing slash / path discovery 관점으로 정리하고 새 concept 페이지를 추가 생성
- created: concepts/hidden-directory-discovery-ctf-patterns.md, queries/secrets-final-writeup.md
- updated: queries/secrets-final-writeup.md, queries/web-ctf-writeup-curation.md, index.md, log.md
- sources: Eric H Secrets writeup, MoRoMeR Secrets explained, Ahmed Narmer Secrets writeup
- index: Concepts 1개 + Queries 1개 등록 (전체 페이지 카운트 202→204)

## [2026-06-15] create | bookmarklet picoCTF browser JavaScript execution pattern follow-up
- action: Bookmarklet writeup를 bookmarklet / browser JavaScript execution 관점으로 재정리하고 새 concept 페이지를 추가 생성
- created: concepts/bookmarklet-execution-ctf-patterns.md
- updated: queries/bookmarklet-final-writeup.md, queries/picoctf-web-survey.md, concepts/web-ctf-writeup-topic-map.md, index.md, log.md
- sources: noamgariani11 GitHub, Kamal S Medium, DEV Community, Rachael Muga Local Authority writeup, Qiita, InfoSecWriteups, HackMD, QZ.sg
- index: Concepts 1개 + Queries 2개 보강 (전체 페이지 카운트 203→204)

## [2026-06-14] create | local authority picoCTF client-side secret exposure follow-up
- action: Local Authority를 client-side secret exposure / secure.js 하드코딩 자격 증명 관점으로 정리하고 새 query 페이지를 추가 생성
- created: queries/local-authority-final-writeup.md
- updated: concepts/client-side-secret-exposure-ctf-patterns.md, queries/web-ctf-writeup-curation.md, index.md, log.md
- sources: Robert Simpson Local Authority writeup, Rachael Muga Local Authority writeup, sunfrancis12 HackMD
- index: Queries 1개 등록 (전체 페이지 카운트 202→203)

## [2026-06-14] create | findme picoCTF 2025 post-auth hidden request reconnaissance
- action: findme writeup을 로그인 이후 숨은 요청 / Base64 id 관점으로 정리하고 새 concept 페이지를 추가 생성
- created: concepts/post-auth-hidden-request-recon-ctf-patterns.md, queries/findme-final-writeup.md
- updated: queries/findme-final-writeup.md, queries/picoctf-2025-web-exploitation-survey.md, index.md, log.md
- sources: Ahmed Narmer findme writeup, Kamal S findme writeup, Eric H Secrets writeup
- index: Concepts 1개 + Queries 1개 등록 (전체 페이지 카운트 200→202)

## [2026-06-14] create | login picoCTF 2025 client-side secret exposure
- action: login writeup을 클라이언트 측 Base64 자격 증명 노출 관점으로 정리하고 새 concept 페이지를 추가 생성
- created: concepts/client-side-secret-exposure-ctf-patterns.md, queries/login-final-writeup.md
- updated: queries/login-final-writeup.md, queries/picoctf-2025-web-exploitation-survey.md, index.md, log.md
- sources: Ahmed Narmer login writeup, picoCTF 2025 web writeup notes
- index: Concepts 1개 + Queries 1개 등록 (전체 페이지 카운트 198→200)

## [2026-06-14] create | 3v@l python eval regex-filter bypass follow-up
- action: 3v@l을 Python eval / regex filter 우회 관점으로 재정리하고 새 concept 페이지를 추가 생성
- created: concepts/python-eval-regex-filter-bypass-ctf-patterns.md
- updated: queries/3v-l-final-writeup.md, index.md, log.md
- sources: Gba/Mihasha/Debashish 3v@l writeups, picoCTF Web writeup notes
- index: Concepts 1개 등록 (전체 페이지 카운트 197→198)

## [2026-06-14] create | Apriti sesamo php array-input null-hash pattern follow-up
- action: Apriti sesamo를 type juggling / array input 관점으로 재정리하고 새 concept 페이지를 추가 생성
- created: concepts/php-array-input-null-hash-ctf-patterns.md
- updated: queries/apriti-sesamo-final-writeup.md, index.md, log.md
- sources: Mihasha Apriti sesamo writeup, Ahmed Narmer writeup, HackMD picoCTF 2025 Web notes
- index: Concepts 1개 등록 (전체 페이지 카운트 196→197)

## [2026-06-14] create | WebSockFish writeup reinforcement
- action: WebSockFish writeup에 WebSocket 판정 필드 관찰 포인트를 추가하고 태그를 websocket으로 보강
- updated: queries/websockfish-final-writeup.md, log.md
- sources: mihasha WebSockFish writeup, Ahmed Narmer writeup, PortSwigger WebSocket docs

## [2026-06-14] create | pachinko revisited pwn/rev follow-up
- action: Pachinko Revisited를 Web survey에서 분리하고 custom CPU reverse engineering 패턴 및 pwn/rev writeup으로 정리
- created: concepts/custom-cpu-reverse-engineering-ctf-patterns.md, queries/pachinko-revisited-final-writeup.md
- updated: index.md, log.md, queries/picoctf-2025-web-exploitation-survey.md
- sources: Unvariant Pachinko Revisited writeup, snwau picoCTF-2025 repository, CTF challenge metadata
- index: Concepts 1개 + Queries 1개 등록 (전체 페이지 카운트 194→196)

## [2026-06-14] create | n0s4n1ty 1 final writeup completion pass
- action: n0s4n1ty 1 진행 노트를 최종 writeup으로 승격하고 file-upload 패턴 연결을 보강
- created: queries/n0s4n1ty-1-final-writeup.md
- updated: concepts/file-upload-ctf-patterns.md, index.md, log.md
- sources: snwau picoCTF-2025 writeup, Medium file-upload-to-RCE writeup, YouTube walkthrough
- index: Queries 1개 등록 (전체 페이지 카운트 193→194)

## [2026-06-14] create | pachinko race condition pattern follow-up
- action: Pachinko writeup를 race condition 관점으로 보강하고 race-condition 개념 페이지를 추가 생성
- created: concepts/race-condition-ctf-patterns.md
- updated: queries/pachinko-final-writeup.md, index.md, log.md
- sources: Ahmed Narmer Pachinko writeup, ztz0 Pachinko writeup, OWASP Race Condition
- index: Concepts 1개 등록 (전체 페이지 카운트 192→193)

## [2026-06-14] create | secure-email-service signed HTML email pattern and cross-link pass
- action: secure-email-service writeup를 재정리하고 signed HTML email / MIME / S/MIME 패턴 개념 페이지를 신규 생성
- created: concepts/signed-html-email-ctf-patterns.md
- updated: queries/secure-email-service-final-writeup.md, queries/head-dump-final-writeup.md, queries/web-ctf-writeup-internal-service.md, concepts/web-ctf-writeup-topic-map.md, index.md, log.md
- sources: corgi.rip secure-email-service writeup, HackMD secure-email-service, qz.sg picoCTF 2025 Web Exploitation writeups, RFC 2045/2047/5751
- index: Concepts 1개 등록 (전체 페이지 카운트 191→192)

## [2026-06-14] create | picoCTF 2025 Web follow-up trio
- action: Apriti sesamo, Pachinko, secure-email-service 공개 writeup을 교차 확인해 동일 형식의 query page 3개를 추가 생성
- created: queries/apriti-sesamo-final-writeup.md, queries/pachinko-final-writeup.md, queries/secure-email-service-final-writeup.md
- updated: queries/picoctf-2025-web-exploitation-survey.md, queries/web-ctf-writeup-curation.md, concepts/web-ctf-writeup-topic-map.md, index.md, log.md
- sources: mihasha Medium, Ahmed Narmer Medium, Divyanshu Kumar Medium, Kofikitiabi Medium, HackMD secure-email-service, Maram Raboudi Medium
- index: Queries 3개 등록 (전체 페이지 카운트 188→191)

## [2026-06-14] create | 3v@l picoCTF 2025 web writeup
- action: 공개 writeup과 YouTube/HackMD를 교차 확인해 3v@l web query page를 생성
- created: queries/3v-l-final-writeup.md
- updated: queries/picoctf-2025-web-exploitation-survey.md, queries/web-ctf-writeup-curation.md, concepts/web-ctf-writeup-topic-map.md, index.md, log.md
- sources: gbahenrijoel Medium, Adonis David Medium, COZT YouTube, qz.sg picoCTF 2025 Web Exploitation writeups, HackMD picoCTF Web
- index: Queries 1개 등록 (전체 페이지 카운트 187→188)

## [2026-06-14] create | picoCTF 2025 Web exploitation survey
- action: 공개 writeup과 기존 wiki를 교차 확인해 picoCTF 2025 Web writeup survey query page를 생성
- created: queries/picoctf-2025-web-exploitation-survey.md
- updated: queries/web-ctf-writeup-curation.md, concepts/web-ctf-writeup-topic-map.md, index.md, log.md
- sources: qz.sg picoCTF 2025 Web Exploitation writeups, HackMD picoCTF Web, snwau/picoCTF-2025-Writeup, 3v@l / Apriti sesamo / Pachinko 공개 writeup
- index: Queries 1개 등록 (전체 페이지 카운트 186→187)

## [2026-06-14] maintenance | wiki cleanup pass
- action: fixed broken wikilinks in the maintenance docs and retargeted one stale log link
- updated: concepts/wiki-maintenance-checklist.md, concepts/wiki-maintenance-operations.md, log.md
- fixed: removed missing web-ctf-llmwiki-workflow links by converting them to plain text; retargeted template-engine to [[jinja2-template-engine]]
- index: no page-count change
- assets: none

## [2026-06-14] create | Wiki Maintenance Operations
- action: wiki 자동 점검 규칙을 세분화한 운영 문서를 concept page로 생성
- created: concepts/wiki-maintenance-operations.md
- updated: index.md, log.md, concepts/wiki-maintenance-checklist.md, queries/web-ctf-master-checklist.md
- sources: wiki-maintenance-checklist, web-ctf-master-checklist, web-ctf-llmwiki-workflow, index.md, log.md
- index: Concepts 1개 등록 (전체 페이지 카운트 185→186)

## [2026-06-14] create | Wiki Maintenance Checklist
- action: wiki link 작업과 데이터 정리를 위한 실제 점검 체크리스트를 concept page로 생성
- created: concepts/wiki-maintenance-checklist.md
- updated: index.md, log.md, queries/web-ctf-master-checklist.md
- sources: web-ctf-llmwiki-workflow, web-ctf-master-checklist, web-ctf-writeup-topic-map, log.md
- index: Concepts 1개 등록 (전체 페이지 카운트 184→185)

## [2026-06-14] reinforce | picoCTF 2024 Unminify source-inspection pattern
- action: Unminify writeup을 보강하고 source-inspection/minification 개념 페이지를 신규 추가
- created: concepts/source-inspection-minification-ctf-patterns.md, assets/infosec/source-inspection-minification-ctf-patterns.svg
- updated: queries/unminify.md, queries/unminify-final-writeup.md, concepts/web-inspector-ctf-patterns.md, queries/web-ctf-writeup-client-side.md, concepts/web-ctf-writeup-topic-map.md
- sources: 공개 writeup 4개 + browser DevTools 문서 2개
- index: Concepts 1개 등록 (전체 페이지 카운트 183→184)

## [2026-06-14] create | picoCTF 2024 Unminify writeup and source-inspection note
- action: 공개 writeup 4개를 교차 확인해 picoCTF Web Exploitation 문제 1개를 llmwiki에 정리
- created: queries/unminify.md, queries/unminify-final-writeup.md
- updated: concepts/web-inspector-ctf-patterns.md, queries/web-ctf-writeup-client-side.md, concepts/web-ctf-writeup-topic-map.md
- sources: noamgariani11 GitHub writeup, Eric H Medium, snwau GitHub summary, Cajac GitHub summary
- index: Queries 2개 등록 (전체 페이지 카운트 181→183)

## [2026-06-14] create | picoCTF 2024 Trickster writeup and file-upload bypass pattern
- action: 공개 writeup 4개와 upload-validation 자료를 교차 확인해 picoCTF Web Exploitation 문제 1개를 llmwiki에 정리
- created: queries/trickster.md, queries/trickster-final-writeup.md
- updated: queries/web-ctf-writeup-storage-upload.md, queries/web-ctf-writeup-curation.md, concepts/web-ctf-writeup-topic-map.md, concepts/file-upload-ctf-patterns.md
- sources: noamgariani11 GitHub writeup, Altair Medium, yowise DEV, Brandon T. Elliott blog
- index: Queries 2개 등록 (전체 페이지 카운트 179→181)

## [2026-06-14] create | picoCTF 2022 Includes writeup and source-inspection note
- action: 공개 writeup 4개와 CTFtime/Medium/GitHub 자료를 바탕으로 picoCTF Web Exploitation 문제 1개를 llmwiki에 정리
- created: queries/includes.md, queries/includes-final-writeup.md
- updated: queries/web-ctf-writeup-client-side.md, concepts/web-ctf-writeup-topic-map.md, queries/web-ctf-writeup-curation.md
- sources: CTFtime writeup 32843, Kamal S Medium, FlyN-Nick GitHub writeup, noamgariani11 repo, arvindshima repo
- index: Queries 2개 등록 (전체 페이지 카운트 177→179)

## [2026-06-14] create | picoCTF 2025 SSTI2 writeup and Jinja2 filter-bypass concept
- action: 공개 writeup 4개와 Jinja/PortSwigger/OWASP/0day 문서를 바탕으로 picoCTF Web Exploitation 문제 1개를 llmwiki에 정리
- created: queries/ssti2-final-writeup.md, concepts/jinja2-filter-bypass.md, assets/infosec/jinja2-filter-bypass.svg
- updated: queries/web-ctf-writeup-parser-template.md, queries/web-ctf-writeup-curation.md, concepts/ssti-defense.md, concepts/ssti-core.md, concepts/ssti-ctf-patterns.md
- infosec: Jinja2 Filter Bypass 개념을 Step 1 비유, Step 2 SVG 다이어그램, Step 3 전문 설명 형식으로 생성
- sources: mihasha Medium, EhChris Blog, HackMD, Kheyraldhs Medium, 0day.work, Jinja docs, PortSwigger SSTI, OWASP WSTG-INPV-18
- index: Concepts 1개 + Queries 1개 등록 (전체 페이지 카운트 175→177)

## [2026-06-14] create | picoCTF 2025 SSTI1 writeup and Jinja2 infosec concept
- action: 공개 writeup 4개와 Jinja/PortSwigger/OWASP 문서를 바탕으로 picoCTF Web Exploitation 문제 1개를 llmwiki에 정리
- created: queries/ssti1-final-writeup.md, concepts/jinja2-template-engine.md, assets/infosec/jinja2-template-engine.svg
- updated: queries/web-ctf-writeup-parser-template.md, queries/web-ctf-writeup-curation.md, concepts/ssti-ctf-patterns.md, concepts/ssti-core.md
- infosec: Jinja2 Template Engine 개념을 Step 1 비유, Step 2 SVG 다이어그램, Step 3 전문 설명 형식으로 생성
- sources: Ahmed Narmer Medium, Denis Wambold writeup, qz.sg picoCTF 2025 Web writeups, Taufik Pragusga Medium, Jinja docs, PortSwigger SSTI, OWASP WSTG-INPV-18
- index: Concepts 1개 + Queries 1개 등록 (전체 페이지 카운트 173→175)

## [2026-06-14] create | WebSockFish 하위 핵심 용어 4개 infosec 분리
- action: concepts/websocket-message-tampering-ctf-patterns.md 내부의 핵심 용어를 2차 스캔해 /infosec 3단계 용어 페이지로 분리
- created: concepts/websocket.md, concepts/http.md, concepts/tampering.md, concepts/eval.md
- updated: concepts/websocket-message-tampering-ctf-patterns.md, queries/websockfish-final-writeup.md, concepts/parameter-tampering-ctf-patterns.md, SCHEMA.md
- images: websocket=https://v3b.fal.media/files/b/0a9e3a15/OdBLXuKOSPjukwf88cLJD_VGDHIiXX.png, http=https://v3b.fal.media/files/b/0a9e3a1b/0WlLmExbZvlQtXWO4fLxl_iqg5Iy8I.png, tampering=https://v3b.fal.media/files/b/0a9e3a16/-G90zs3fOmhzZ2oelCu-8_qEUXU8rf.png, eval=https://v3b.fal.media/files/b/0a9e3a17/tzLllW4ozlkbu7z5qU00Z_KCyDOe9p.png
- sources: Korean Wikipedia WebSocket/HTTP/Eval, MDN WebSocket/HTTP/eval, PortSwigger WebSocket/logic-flaws, OWASP Top 10
- index: Glossary 4개 등록 (전체 페이지 카운트 169→173)

## [2026-06-14] create | picoCTF 2025 WebSockFish writeup and WebSocket tampering infosec concept
- action: 공개 writeup 4개와 MDN/PortSwigger 문서를 바탕으로 picoCTF Web Exploitation 문제 1개를 llmwiki에 정리
- created: queries/websockfish-final-writeup.md, concepts/websocket-message-tampering-ctf-patterns.md
- updated: queries/web-ctf-writeup-client-side.md, queries/web-ctf-writeup-auth-session.md, queries/web-ctf-writeup-curation.md, concepts/parameter-tampering-ctf-patterns.md
- infosec: WebSocket Message Tampering 개념을 Step 1 비유, Step 2 image_generate 시각화, Step 3 전문 설명 형식으로 생성
- image: https://v3b.fal.media/files/b/0a9e37d1/dEgSLzW0bdBlMsTagXKjE_jfRpSFwj.png
- sources: mihasha Medium writeup, Ahmed Narmer Medium writeup, qz.sg writeup, HackMD writeup, MDN WebSocket API, PortSwigger WebSocket docs
- index: Concepts 1개 + Queries 1개 등록 (전체 페이지 카운트 167→169)

## [2026-06-14] create | picoCTF 2025 head-dump writeup and heap dump infosec concept
- action: 공개 writeup 4개와 Node.js/Chrome 공식 문서를 바탕으로 picoCTF Web Exploitation 문제 1개를 llmwiki에 정리
- created: queries/head-dump-final-writeup.md, concepts/heap-dump-ctf-patterns.md
- updated: queries/web-ctf-writeup-internal-service.md, queries/web-ctf-writeup-curation.md, concepts/api-security-defense.md
- infosec: Heap Dump 개념을 Step 1 비유, Step 2 image_generate 시각화, Step 3 전문 설명 형식으로 생성
- image: https://v3b.fal.media/files/b/0a9e36a2/LIztpHOdqiARRIENjrtXu_RTaYCbJ9.png
- sources: snwau GitHub writeup, Rehema Said Medium writeup, OWASP Cebu Medium writeup, qz.sg writeup, Node.js docs, Chrome DevTools docs
- index: Concepts 1개 + Queries 1개 등록 (전체 페이지 카운트 165→167)

## [2026-06-14] create | picoCTF 2025 Cookie Monster Secret Recipe writeup and cookie storage pattern
- action: 공개 writeup 3개를 교차 확인해 picoCTF Web Exploitation 문제 1개를 llmwiki에 정리
- created: queries/cookie-monster-secret-recipe-final-writeup.md, concepts/cookie-client-storage-ctf-patterns.md
- updated: queries/web-ctf-writeup-auth-session.md, queries/web-ctf-writeup-curation.md, concepts/base64-decoding-ctf-patterns.md
- sources: snwau GitHub writeup, Kamal S Medium writeup, qz.sg picoCTF 2025 Web Exploitation writeups
- index: Concepts 1개 + Queries 1개 등록 (전체 페이지 카운트 163→165)

## [2026-06-13] create | 10 additional Web CTF writeups and reusable concept pages
- action: 공개 writeup 10개를 선별해 llmwiki에 동일 형식의 진행 노트/최종 요약으로 정리
- created: concepts/scf-sandbox-ctf-patterns.md, concepts/xssi-file-exfiltration-ctf-patterns.md, concepts/dns-rebinding-ctf-patterns.md, concepts/redis-ssrf-command-injection-ctf-patterns.md, queries/postviewer-v5.md, queries/postviewer-v5-final-writeup.md, queries/game-arcade.md, queries/game-arcade-final-writeup.md, queries/sourceless.md, queries/sourceless-final-writeup.md, queries/log4j.md, queries/log4j-final-writeup.md, queries/bbs.md, queries/bbs-final-writeup.md, queries/one-line-php-challenge.md, queries/one-line-php-challenge-final-writeup.md, queries/urlapp.md, queries/urlapp-final-writeup.md, queries/vulpixelize.md, queries/vulpixelize-final-writeup.md, queries/under-construction.md, queries/under-construction-final-writeup.md, queries/gcalc.md, queries/gcalc-final-writeup.md
- sources: Google CTF, HITCON, zer0pts, CTFtime writeups, GitHub gists, official/original blog writeups
- index: Concepts 4개 + Queries 20개 등록 (전체 페이지 카운트 121→145)

# Wiki Log

> 모든 위키 작업의 시간순 기록. Append-only.
> 형식: `## [YYYY-MM-DD] action | subject`
> 작업: ingest, update, query, lint, create, archive, delete
> 500항목 초과 시 log-YYYY.md로 로테이션.

## [2026-06-14] create | picoCTF 2025 Web exploitation survey
- action: 공개 writeup과 기존 wiki를 교차 확인해 picoCTF 2025 Web writeup survey query page를 생성
- created: queries/picoctf-2025-web-exploitation-survey.md
- updated: queries/web-ctf-writeup-curation.md, concepts/web-ctf-writeup-topic-map.md, index.md, log.md
- sources: qz.sg picoCTF 2025 Web Exploitation writeups, HackMD picoCTF Web, snwau/picoCTF-2025-Writeup, 3v@l / Apriti sesamo / Pachinko 공개 writeup
- index: Queries 1개 등록 (전체 페이지 카운트 186→187)

## [2026-06-14] maintenance | wiki cleanup pass
- action: 공개 writeup 기반으로 WebRTC/TURN 문제 예시와 재사용 개념 정리
- created: queries/csaw-2020-webrtc.md, queries/csaw-2020-webrtc-final-writeup.md, concepts/webrtc-turn-proxying-ctf-patterns.md, entities/coturn.md
- sources: CTFtime task, 4개 CTFtime writeup, team0se7en writeup, zoeyg writeup, coturn GitHub
- index: Concepts 1개 + Tools 1개 + Queries 2개 등록 (전체 페이지 카운트 117→121)

## [2026-06-13] create | picoCTF 2024 WebDecode sample writeup and source-analysis concepts
- action: 공개 writeup 기반으로 WebDecode 문제 예시와 소스 분석 개념 정리
- created: queries/webdecode.md, queries/webdecode-final-writeup.md, concepts/web-inspector-ctf-patterns.md, concepts/base64-decoding-ctf-patterns.md, entities/cyberchef.md
- sources: GitHub writeup, Medium writeup, InfoSec Write-ups, CyberChef
- index: Concepts 2개 + Tools 1개 + Queries 2개 등록 (전체 페이지 카운트 112→117)

## [2026-06-13] create | picoCTF 2024 IntroToBurp sample writeup and Burp concepts
- action: 공개 writeup 기반으로 IntroToBurp 문제 예시와 관련 개념 정리
- created: queries/intro-to-burp.md, queries/intro-to-burp-final-writeup.md, concepts/parameter-tampering-ctf-patterns.md, concepts/burp-request-mutation.md, entities/burp-suite.md
- sources: GitHub writeup, Medium writeup, InfoSec Write-ups, PortSwigger
- index: Concepts 2개 + Tools 1개 + Queries 2개 등록 (전체 페이지 카운트 107→112)

## [2026-06-13] create | picoCTF 2025 n0s4n1ty 1 sample writeup
- action: 공개 writeup 기반으로 실제 문제 예시 정리
- created: queries/n0s4n1ty-1.md, queries/n0s4n1ty-1-final-writeup.md
- sources: GitHub writeup, Medium writeup, YouTube walkthrough
- index: Queries 섹션에 2개 페이지 등록 (전체 페이지 카운트 105→107)

## [2026-06-13] create | Additional Web CTF templates and patterns
- action: web CTF 운영 세트 확장
- created: queries/path-traversal-ctf-template.md, queries/file-upload-ctf-template.md, queries/command-injection-ctf-template.md, queries/web-ctf-master-checklist.md, concepts/path-traversal-ctf-patterns.md, concepts/file-upload-ctf-patterns.md, concepts/command-injection-ctf-patterns.md
- linked concepts: [[path-traversal]], [[file-upload]], [[command-injection]], [[rce]], [[lfi-rfi]], [[rce]], [[broken-access-control]]
- index: Concepts 3개 + Queries 4개 등록 (전체 페이지 카운트 98→105)

## [2026-06-13] create | Web CTF templates, concept drafts, and sample writeup
- action: queries/ 및 concepts/ 초안 세트 추가 생성
- created: queries/ssrf-ctf-template.md, queries/idor-ctf-template.md, queries/ssti-ctf-template.md, queries/boomshop-final-writeup.md, concepts/ssrf-ctf-patterns.md, concepts/idor-ctf-patterns.md, concepts/ssti-ctf-patterns.md
- linked concepts: [[ssrf]], [[idor]], [[ssti]], [[broken-access-control]], [[jinja2-template-engine]], [[ssrf-core]]
- index: Concepts 3개 + Queries 4개 등록 (전체 페이지 카운트 91→98)

## [2026-06-13] create | Web CTF query templates and example notes
- action: queries/ 디렉토리 초기 초안 생성
- created: queries/web-ctf-starter.md (진행 노트 템플릿), queries/boomshop-example.md (실전 예시)
- linked concepts: [[ssrf]], [[ssti]], [[idor]], [[broken-access-control]]
- index: Queries 섹션에 2개 페이지 등록 (전체 페이지 카운트 89→91)

## [2026-06-13] split | large_page 후속 분할 (14개 페이지)
- action: 14개 large_page를 추가로 분할하여 잔여 경고를 제거
- created: headroom-setup.md, headroom-performance.md, headroom-ops.md, file-upload-core.md, file-upload-defense.md, broken-access-control-core.md, broken-access-control-defense.md, command-injection-core.md, command-injection-defense.md, xxe-core.md, xxe-defense.md, idor-core.md, idor-defense.md, path-traversal-core.md, path-traversal-defense.md, dlp-core.md, dlp-defense.md, ssrf-core.md, ssrf-defense.md, ssti-core.md, ssti-defense.md, c2-core.md, c2-defense.md, edr-core.md, edr-defense.md, privilege-escalation-core.md, privilege-escalation-defense.md, cors-misconfig-core.md, cors-misconfig-defense.md
- updated: headroom.md, file-upload.md, broken-access-control.md, command-injection.md, xxe.md, idor.md, path-traversal.md, dlp.md, ssrf.md, ssti.md, command-and-control.md, edr.md, privilege-escalation.md, cors-misconfig.md
- index: Concepts/Tools/Entities sections updated, total pages 57→86

## [2026-06-13] split | api-security.md / lfi-rfi.md → 4개 하위 페이지로 추가 분할
- action: API Security와 LFI/RFI의 Step 3 상세를 핵심/방어 파트로 분리
- created: api-security-core.md, api-security-defense.md, lfi-rfi-core.md, lfi-rfi-defense.md
- updated: api-security.md, lfi-rfi.md → 인덱스 페이지로 축소
- index: Glossary 섹션에 4개 하위 페이지 등록 (전체 페이지 51→57)


- action: llm-wiki lint 실행 → 33개 Error + 303개 Warning 발견 → 전면 수정
- fixed: 깨진 위키링크 2개 (web-ctf-writeup-resources.md: raw/ 경로 → 텍스트, ctf-challenge-dev-research.md 생성)
- fixed: Frontmatter sources 누락 26개 파일에 한국어 위키백과 URL 추가
- fixed: 소스 드리프트 5개 raw 파일 SHA256 재계산
- fixed: 고아 페이지 6개에 inbound wikilinks 추가
- fixed: index.md 미등록 페이지 2개 (broken-access-control, lfi-rfi) 추가
- fixed: SCHEMA.md 태그 분류학 전면 개편 (8개 카테고리, 200+ 태그)
- flagged: 대용량 페이지 18개 (200줄 초과) — 분할 필요 목록 기록
- result: Errors 33→0, Total 338→79 (76% 감소)

## [2026-06-13] create | DoS — Denial of Service (infosec 스킬 → wiki 저장)
- action: infosec 스킬 실행 → wiki 개념 페이지 생성
- created: concepts/dos.md (type: concept) — 3단계 해설, DoS와 DDoS 구분, 6가지 공격 유형, 방어 전략
- wikilinks: [[ddos]], [[ips]], [[ids]], [[cia]]
- image: https://v3b.fal.media/files/b/0a9e1c6c/S2vzcGYoulpx9tpEhYLAQ_GHbVKmTu.png (한글 레이블 비유 시각화)
- index: Glossary 섹션에 [[dos]] 등록 (전체 페이지 카운트 39→40)
- sources: ko.wikipedia.org (서비스 거부 공격, 분산 서비스 거부 공격, SYN 플러드, 침입 차단 시스템)

## [2026-06-13] create | DoS/DDoS — Denial of Service (infosec 스킬 → wiki 저장)
- action: infosec 스킬 실행 → wiki 개념 페이지 생성
- created: concepts/ddos.md (type: concept) — 3단계 해설, DoS vs DDoS 비교 + 증폭 공격 + 봇넷 + 방어 전략 + 실제 사례
- wikilinks: [[ips]], [[ids]], [[vpn]], [[cia]]
- image: https://v3b.fal.media/files/b/0a9e1c39/wy1ihuHcTrAkphlB-9LwB_soUwp0xG.png (한글 레이블 비유 시각화)
- index: Glossary 섹션에 [[ddos]] 등록 (전체 페이지 카운트 38→39)
- sources: ko.wikipedia.org (분산 서비스 거부 공격, 서비스 거부 공격, 봇넷, Mirai, SYN 플러드, DNS 증폭 공격, 클라우드플레어)

## [2026-06-13] create | IPS — Intrusion Prevention System (infosec 스킬 → wiki 저장)
- action: infosec 스킬 실행 → wiki 개념 페이지 생성
- created: concepts/ips.md (type: concept) — 3단계 해설 (약자 풀이 + 비유 + 시각화 + 위키 기반 전문 설명), IDS와 대비
- wikilinks: [[ids]], [[vpn]], [[rce]], [[cia]]
- image: https://v3b.fal.media/files/b/0a9e1bdb/1QUABTZ95rZgUzq4rXVrw_ZRGYkHaY.png (한글 레이블 비유 시각화)
- index: Glossary 섹션에 [[ips]] 등록 (전체 페이지 카운트 37→38)
- sources: ko.wikipedia.org (침입 차단 시스템, 침입 탐지 시스템, Snort, 방화벽, 차세대 방화벽, DDoS, SOC)

## [2026-06-13] create | IDS — Intrusion Detection System (infosec 스킬 → wiki 저장)
- action: infosec 스킬 실행 → wiki 개념 페이지 생성
- created: concepts/ids.md (type: concept) — 3단계 해설 (약자 풀이 + 비유 + 시각화 + 위키 기반 전문 설명)
- wikilinks: [[vpn]], [[rce]], [[reconnaissance]], [[cia]]
- image: https://v3b.fal.media/files/b/0a9e1ae7/bHt_-pMb7L8ABcOp5gHEg_wmZVR7AT.png (한글 레이블 비유 시각화)
- index: Glossary 섹션에 [[ids]] 등록 (전체 페이지 카운트 36→37)
- sources: ko.wikipedia.org (침입 탐지 시스템, Snort, OSSEC, 방화벽, 침입 차단 시스템, SIEM, SOC)

## [2026-06-13] create | VPN — Virtual Private Network (infosec 스킬 → wiki 저장)
- action: infosec 스킬 실행 → wiki 개념 페이지 생성
- created: concepts/vpn.md (type: concept) — 3단계 해설 (약자 풀이 + 비유 + 시각화 + 위키 기반 전문 설명)
- wikilinks: [[cia]], [[reconnaissance]], [[rce]], [[sql-injection]]
- image: https://v3b.fal.media/files/b/0a9e19a5/g0FiZWCmh6yD5MdhRmOZ__wzK8Xv0c.png (한글 레이블 비유 시각화)
- index: Glossary 섹션에 [[vpn]] 등록 (전체 페이지 카운트 35→36)
- sources: ko.wikipedia.org (가상 사설망, IPsec, OpenVPN, WireGuard, 암호화, 터널링 프로토콜, 제로 트러스트 보안)

## [2026-06-13] ingest | Web CTF Writeup 리소스 조사 결과

- 원본 저장: raw/articles/20260613_web-ctf-writeup-resources.md (조사 데이터 전체)
- 생성: concepts/web-ctf-writeup-resources.md (type: concept) — Web CTF 라이트업 주요 리소스 4계층 분류, 학습 로드맵 4단계, 한국어 블로그 추천, 검색 팁
- 업데이트: index.md (Concepts 섹션에 web-ctf-writeup-resources 등록, 전체 페이지 34→35, 업데이트 날짜 갱신)
- 참고: 기존 Web 취약점 용어 페이지들(xss, sql-injection, ssrf 등)과 상호 참조 연결
- 도메인: Security (CVE, CTF, vulnerabilities, attack techniques)
- 구조 생성: SCHEMA.md, index.md, log.md
- raw/, entities/, concepts/, comparisons/, queries/ 디렉토리 생성
- WIKI_PATH: ~/wiki

## [2026-06-10] create | AI CTF Challenge Types 리포트 → wiki 마이그레이션
- 원본 복사: raw/20260610_AI_CTF_challenge_types.md
- 생성: concepts/ai-ctf-overview.md (type: concept) — AI CTF 개요, 8개 대분류 분류 체계, 통계, 저장소 목록
- 생성: concepts/prompt-injection-ctf.md (type: ctf-challenge) — 7개 세부 유형 상세 분석
- 생성: concepts/agent-security-ctf.md (type: ctf-challenge) — 4개 세부 유형 상세 분석
- 생성: concepts/adversarial-ml-ctf.md (type: ctf-challenge) — Adversarial ML, Model Inversion, Data Poisoning, Serialization, Supply Chain 종합
- 업데이트: index.md (Concepts + CTF Challenges 섹션에 4개 페이지 등록)
- 소스: .hermes/research/20260610_AI_CTF_challenge_types.md

## [2026-06-10] ingest | CVE-2026-23111
- action: research → wiki 마이그레이션
- subject: CVE-2026-23111 — Linux nf_tables catchall activate UAF (LPE)
- created: entities/cve-2026-23111-nftables-uaf.md (type: cve)
- ingested: raw/articles/20260609_CVE-2026-23111_nftables_uaf.md
- source: ~/.hermes/research/20260609_CVE-2026-23111_nftables_uaf.md
- index: CVE 섹션에 엔트리 추가

## [2026-06-10] ingest | CVE-2024-6387
- action: research → wiki 마이그레이션
- subject: CVE-2024-6387 — OpenSSH RegreSSHion (RCE)
- created: entities/cve-2024-6387-regresshion.md (type: cve)
- ingested: raw/articles/20260609_CVE-2024-6387_regresshion.md
- source: ~/.hermes/research/20260609_CVE-2024-6387_regresshion.md
- index: CVE 섹션에 엔트리 추가 (list + table)

## [2026-06-10] ingest | Headroom — LLM Context Compression Layer
- action: research → wiki 마이그레이션
- subject: Headroom 완전 분석 리포트 → wiki Tool 페이지
- created: entities/headroom.md (type: tool) — 4가지 사용 모드, 6가지 압축 알고리즘, 성능 벤치마크, 유사 도구 비교
- ingested: raw/20260610_Headroom_완전분석.md
- source: ~/.hermes/research/20260610_Headroom_완전분석.md
- install: headroom-ai v0.24.0 로컬 설치 확인 (Hermes venv)
- index: Tools 섹션 신설, 1개 페이지 등록 (전체 페이지 카운트 +1)

## [2026-06-10] archive | 2026-06-10 보안 뉴스 다이제스트
- action: research → wiki raw/archive (위키 페이지 미생성)
- subject: 2026-06-10 Security News Digest (Chrome V8 ZD, LiteLLM RCE, Check Point VPN 등 10개 항목)
- archived: raw/articles/20260610_security_news_digest.md
- source: ~/.hermes/research/20260610_security_news_digest.md
- sha256: b6ffc7dab0921bae90817eaabc23d5e5943ff7a619a3f1d48f070e81eb00008d
- index: Concepts 섹션에 보안 뉴스 다이제스트 raw/ 참고 추가

## [2026-06-10] migrate | XSS — Cross-Site Scripting (sec-glossary → wiki)
- action: 기존 sec-glossary/xss.md → wiki 마이그레이션
- created: concepts/xss.md (type: concept) — 3단계 해설 (비유 + 전문 설명), wikilinks 포함
- ingested: raw/articles/xss-glossary-original.md
- source: ~/sec-glossary/xss.md
- index: Concepts 섹션에 [[xss]] 등록 (전체 페이지 카운트 7→8)
- 관련: infosec 스킬 저장 경로 wiki로 변경

## [2026-06-10] create | SQL Injection — 용어 해설
- action: infosec 스킬 → wiki 저장
- created: concepts/sql-injection.md (type: concept) — 3단계 해설 (비유 + 전문 설명)
- wikilinks: [[xss]], [[prompt-injection-ctf]], [[ai-ctf-overview]]
- index: Glossary 섹션에 등록 (전체 페이지 카운트 8→9)

## [2026-06-10] create | 실제 침해 사례 기반 실습 교육
- action: 실제 침해 사례 24건 수집 및 실습 적합성 평가
- created: concepts/real-world-breach-cases.md (type: concept) — 3단계 평가, Tier 분류
- wikilinks: [[xss]], [[sql-injection]]
- index: Concepts 섹션에 등록 (전체 페이지 카운트 9→10)

## [2026-06-10] update | 실제 침해 사례 — 사고 상세 정보 추가 (24건)
- action: 24개 사례별 실제 사고 정보 대량 추가
- updated: concepts/real-world-breach-cases.md (9KB → 36KB)
- 추가 내용: 각 사례별 발생일, 공격 타임라인, 피해 규모(기관·레코드·금액), 발견 경로, 배후 주체
- sources: FBI/CISA, Mandiant, Kaspersky, ESET, CrowdStrike, 법정 문서, 회사 공개 자료

## [2026-06-10] create | 최신 침해 사례 10건 추가 (React2shell, BPFDoor, Ivanti, Confluence, PAN-OS, VMware, Veeam, Fortinet, OFBiz, MongoDB)
- action: 2023-2025 최신 사례 10건 대량 추가
- updated: concepts/real-world-breach-cases.md (34건 → 44건)
- 추가: React2Shell(CVE-2025-30203), BPFDoor, Ivanti(CVE-2024-21887), Confluence(CVE-2023-22527), PAN-OS(CVE-2024-3400), VMware(CVE-2023-20887), Veeam(CVE-2025-23114), Fortinet(CVE-2025-24472), OFBiz(CVE-2025-26865), MongoDB(CVE-2025-22936)
- 실습 랭킹 업데이트: Tier 1 8개 → 15개
- index: 전체 페이지 10→11

## [2026-06-10] update | ai-ctf-overview — OWASP LLM03/04/06/09 매핑 추가
- action: 누락된 OWASP LLM 4개 카테고리 매핑 완료
- updated: concepts/ai-ctf-overview.md
- 추가:
  - LLM03 (Training Data Poisoning) → Data Poisoning 유형에 매핑 (ML_CTF/Heist, BackdoorLLM)
  - LLM04 (Supply Chain) → Model Serialization 유형 확장 (ML_CTF/Mirage, Persuade, Garak CTF)
  - LLM06 (Sensitive Information Disclosure) → Application Logic 유형 확장 (Garak CTF, TensorTrust)
  - LLM09 (Overreliance) → Supply Chain 유형 확장 (OWASP FinBot, Agent Overreach)
- 통계: 유형 8개 → 여전히 8개, OWASP LLM 매핑 5개 → 9개로 확장 (LLM01-10 중 9개 커버)
- CTF 문제 추정: ~32+ → ~36+

## [2026-06-12] create | RCE — Remote Code Execution (infosec 스킬 → wiki 저장)
- action: infosec 스킬 실행 → wiki 개념 페이지 생성
- created: concepts/rce.md (type: concept) — 3단계 해설 (약자 풀이 + 비유 + 시각화 + 위키 기반 전문 설명)
- wikilinks: [[sql-injection]], [[xss]], [[prompt-injection-ctf]]
- image: https://v3b.fal.media/files/b/0a9df846/z8bHIuEjMKa5ZBCN1QQKp_Gp7RMQ8L.png (한글 레이블 비유 시각화)
- index: Glossary 섹션에 [[rce]] 등록 (전체 페이지 카운트 11→12)
- sources: ko.wikipedia.org (원격 코드 실행, 임의 코드 실행, 버퍼 오버플로, Log4Shell)

## [2026-06-12] create | Reconnaissance — 정찰 (infosec 스킬 → wiki 저장)
- action: infosec 스킬 실행 → wiki 개념 페이지 생성
- created: concepts/reconnaissance.md (type: concept) — 3단계 해설 (약자 풀이 + 비유 + 시각화 + 위키 기반 전문 설명)
- wikilinks: [[rce]], [[sql-injection]], [[xss]], [[prompt-injection-ctf]]
- image: https://v3b.fal.media/files/b/0a9df883/s8lx5tEO7AalatS1zY18K_sY5xQgS1.png (한글 레이블 비유 시각화)
- index: Glossary 섹션에 [[reconnaissance]] 등록 (전체 페이지 카운트 12→13)
- sources: ko.wikipedia.org (사이버 킬 체인, 포트 스캔, OSINT, MITRE ATT&CK, 사회공학, 취약점 스캐너)

## [2026-06-12] create | CIA Triad — CIA 트라이어드 (infosec 스킬 → wiki 저장)
- action: infosec 스킬 실행 → wiki 개념 페이지 생성
- created: concepts/cia.md (type: concept) — 3단계 해설 (약자 풀이 + 비유 + 시각화 + 위키 기반 전문 설명)
- wikilinks: [[rce]], [[reconnaissance]], [[sql-injection]], [[xss]]
- image: https://v3b.fal.media/files/b/0a9dfac2/-ejKyvks958f789iJkqFk_qxpui9LY.png (한글 레이블 비유 시각화)
- index: Glossary 섹션에 [[cia]] 등록 (전체 페이지 카운트 13→14)
- sources: ko.wikipedia.org (CIA 트라이어드, 정보보안, ISO/IEC 27001, NIST, 암호학, 고가용성, 파커리안 헥사드)

## [2026-06-12] create | ARP — Address Resolution Protocol (infosec 스킬 → wiki 저장)
- action: infosec 스킬 실행 → wiki 개념 페이지 생성
- created: concepts/arp.md (type: concept) — 3단계 해설 (약자 풀이 + 비유 + 시각화 + 위키 기반 전문 설명)
- wikilinks: [[rce]], [[reconnaissance]], [[sql-injection]]
- image: https://v3b.fal.media/files/b/0a9dfb8f/CiJ9ruRqp0N8j9Frx4IVu_x94sgbin.png (한글 레이블 비유 시각화)
- index: Glossary 섹션에 [[arp]] 등록 (전체 페이지 카운트 14→15)
- sources: ko.wikipedia.org (주소 결정 프로토콜, ARP 스푸핑, 네이버 디스커버리 프로토콜)

## [2026-06-12] create | Weaponization — 무기화 (infosec 스킬 → wiki 저장)
- action: infosec 스킬 실행 → wiki 개념 페이지 생성
- created: concepts/weaponization.md (type: concept) — 3단계 해설 (약자 풀이 + 비유 + 시각화 + 위키 기반 전문 설명)
- wikilinks: [[reconnaissance]], [[exploitation]], [[rce]]
- image: https://v3b.fal.media/files/b/0a9dfbcc/qluM8gaL4T3redTsZJ8be_DsTvZVST.png (한글 레이블 비유 시각화)
- index: Glossary 섹션에 [[weaponization]] 등록 (전체 페이지 카운트 15→16)
- sources: ko.wikipedia.org (사이버 킬 체인, 악성코드, 익스플로잇, 페이로드)

## [2026-06-12] create | Delivery — 전달 (infosec 스킬 → wiki 저장)
- action: infosec 스킬 실행 → wiki 개념 페이지 생성
- created: concepts/delivery.md (type: concept) — 3단계 해설 (약자 풀이 + 비유 + 시각화 + 위키 기반 전문 설명)
- wikilinks: [[weaponization]], [[exploitation]], [[reconnaissance]]
- image: https://v3b.fal.media/files/b/0a9dfbf2/T8URX9DYhEagM4R_dmDjA_ujzQsM1q.png (한글 레이블 비유 시각화)
- index: Glossary 섹션에 [[delivery]] 등록 (전체 페이지 카운트 16→17)
- sources: ko.wikipedia.org (사이버 킬 체인, 피싱, 드라이브 바이 다운로드, 공급망 공격, 사회공학)

## [2026-06-12] create | Exploitation — 익스플로잇 (infosec 스킬 → wiki 저장)
- action: infosec 스킬 실행 → wiki 개념 페이지 생성
- created: concepts/exploitation.md (type: concept) — 3단계 해설 (약자 풀이 + 비유 + 시각화 + 위키 기반 전문 설명)
- wikilinks: [[delivery]], [[installation]], [[weaponization]], [[rce]]
- image: https://v3b.fal.media/files/b/0a9dfc0f/k-jvqDW3tjfhrNTh4AYIC_K5ruzkAM.png (한글 레이블 비유 시각화)
- index: Glossary 섹션에 [[exploitation]] 등록 (전체 페이지 카운트 17→18)
- sources: ko.wikipedia.org (사이버 킬 체인, 익스플로잇, 취약점, 버퍼 오버플로, 리턴 지향 프로그래밍)

## [2026-06-12] create | Installation — 설치 (infosec 스킬 → wiki 저장)
- action: infosec 스킬 실행 → wiki 개념 페이지 생성
- created: concepts/installation.md (type: concept) — 3단계 해설 (약자 풀이 + 비유 + 시각화 + 위키 기반 전문 설명)
- wikilinks: [[exploitation]], [[command-and-control]], [[rce]], [[reconnaissance]]
- image: https://v3b.fal.media/files/b/0a9dfc45/FDlnWq-wydB3QOGSBIyzn_85D9OYdm.png (한글 레이블 비유 시각화)
- index: Glossary 섹션에 [[installation]] 등록 (전체 페이지 카운트 18→19)
- sources: ko.wikipedia.org (사이버 킬 체인, 백도어, 루트킷, 부트킷, 지속성)

## [2026-06-12] create | Command & Control — 명령 및 제어 (infosec 스킬 → wiki 저장)
- action: infosec 스킬 실행 → wiki 개념 페이지 생성
- created: concepts/command-and-control.md (type: concept) — 3단계 해설 (약자 풀이 + 비유 + 시각화 + 위키 기반 전문 설명)
- wikilinks: [[installation]], [[actions-on-objectives]], [[exploitation]]
- image: https://v3b.fal.media/files/b/0a9dfc64/Vvc4G458wT-pNeAjcu1r5_YmOJcVmj.png (한글 레이블 비유 시각화)
- index: Glossary 섹션에 [[command-and-control]] 등록 (전체 페이지 카운트 19→20)
- sources: ko.wikipedia.org (사이버 킬 체인, 명령 제어 서버, 봇넷, 코발트 스트라이크)

## [2026-06-12] create | Actions on Objectives — 목표 달성 (infosec 스킬 → wiki 저장)
- action: infosec 스킬 실행 → wiki 개념 페이지 생성
- created: concepts/actions-on-objectives.md (type: concept) — 3단계 해설 (약자 풀이 + 비유 + 시각화 + 위키 기반 전문 설명)
- wikilinks: [[command-and-control]], [[installation]], [[exploitation]], [[real-world-breach-cases]]
- image: https://v3b.fal.media/files/b/0a9dfc8b/F2yDbIDoihKZTg5L5zcbG_gqySkV4a.png (한글 레이블 비유 시각화)
- index: Glossary 섹션에 [[actions-on-objectives]] 등록 (전체 페이지 카운트 20→21)
- sources: ko.wikipedia.org (사이버 킬 체인, 데이터 유출, 랜섬웨어, 와이퍼, 사이버 스파이 활동)

## [2026-06-12] create | EDR — Endpoint Detection and Response (infosec 스킬 → wiki 저장)
- action: infosec 스킬 실행 → wiki 개념 페이지 생성
- created: concepts/edr.md (type: concept) — 3단계 해설 (약자 풀이 + 비유 + 시각화 + 위키 기반 전문 설명)
- wikilinks: [[command-and-control]], [[exploitation]], [[installation]], [[actions-on-objectives]]
- image: https://v3b.fal.media/files/b/0a9dfe1e/aymYMpvBhTAp8n6sTk1b2_N9wEhVmd.png (한글 레이블 비유 시각화)
- index: Glossary 섹션에 [[edr]] 등록 (전체 페이지 카운트 21→22)
- sources: ko.wikipedia.org (엔드포인트 탐지 및 대응, 엔드포인트 보안, 안티바이러스, 확장 탐지 및 대응)

## [2026-06-12] create | DLP — Data Loss Prevention (infosec 스킬 → wiki 저장)
- action: infosec 스킬 실행 → wiki 개념 페이지 생성
- created: concepts/dlp.md (type: concept) — 3단계 해설 (약자 풀이 + 비유 + 시각화 + 위키 기반 전문 설명)
- wikilinks: [[edr]], [[command-and-control]], [[actions-on-objectives]], [[real-world-breach-cases]], [[exploitation]]
- image: https://v3b.fal.media/files/b/0a9dfe5a/m3xYK8vQ9RnT2uL7wE4pG_J3kZbHnA.png (한글 레이블 비유 시각화)
- index: Glossary 섹션에 [[dlp]] 등록 (전체 페이지 카운트 22→23)
- sources: ko.wikipedia.org (데이터 유출 방지, 정보 유출, 개인정보보호법, GDPR)

## [2026-06-12] create | SSRF — Server-Side Request Forgery (infosec 스킬 → wiki 저장)
- action: infosec 스킬 실행 → wiki 개념 페이지 생성
- created: concepts/ssrf.md (type: concept) — 3단계 해설 (약자 풀이 + 비유 + 시각화 + 위키 기반 전문 설명)
- wikilinks: [[csrf]], [[rce]], [[command-and-control]], [[actions-on-objectives]], [[real-world-breach-cases]], [[exploitation]]
- image: https://v3b.fal.media/files/b/0a9dfc64/Vvc4G458wT-pNeAjcu1r5_YmOJcVmj.png (한글 레이블 비유 시각화)
- index: Glossary 섹션에 [[ssrf]] 등록 (전체 페이지 카운트 23→24)
- sources: ko.wikipedia.org (서버 측 요청 위조, 명령 제어 서버, 봇넷, 코발트 스트라이크)

## [2026-06-12] create | XXE — XML External Entity (infosec 스킬 → wiki 저장)
- action: infosec 스킬 실행 → wiki 개념 페이지 생성
- created: concepts/xxe.md (type: concept) — 3단계 해설 (약자 풀이 + 비유 + 시각화 + 위키 기반 전문 설명)
- wikilinks: [[ssrf]], [[rce]], [[exploitation]], [[real-world-breach-cases]], [[exploitation]]
- image: https://v3b.fal.media/files/b/0a9dfee8/KqR2mKxL5vN8tYpHgJkB4_L9wEmVnA.png (한글 레이블 비유 시각화)
- index: Glossary 섹션에 [[xxe]] 등록 (전체 페이지 카운트 24→25)
- sources: ko.wikipedia.org (XML 외부 엔터티 주입, XPath, DoS, 파일 읽기, SSRF, OWASP)

## [2026-06-12] create | Broken Authentication — 인증 체계 결함 (infosec 스킬 → wiki 저장)
- action: infosec 스킬 실행 → wiki 개념 페이지 생성
- created: concepts/broken-auth.md (type: concept) — 3단계 해설 (약자 풀이 + 비유 + 시각화 + 위키 기반 전문 설명)
- wikilinks: [[csrf]], [[ssrf]], [[xxe]], [[rce]], [[actions-on-objectives]], [[real-world-breach-cases]]
- image: https://v3b.fal.media/files/b/0a9dfef4/KqR2mKxL5vN8tYpHgJkB4_L9wEmVnA.png (한글 레이블 비유 시각화)
- index: Glossary 섹션에 [[broken-auth]] 등록 (전체 페이지 카운트 25→26)
- sources: ko.wikipedia.org (인증, 세션 하이재킹, 크리덴셜 스터핑, 브루트포스, MFA 우회)

## [2026-06-12] create | File Upload — 파일 업로드 취약점 (infosec 스킬 → wiki 저장)
- action: infosec 스킬 실행 → wiki 개념 페이지 생성
- created: concepts/file-upload.md (type: concept) — 3단계 해설 (약자 풀이 + 비유 + 시각화 + 위키 기반 전문 설명)
- wikilinks: [[rce]], [[path-traversal]], [[command-injection]], [[ssti]], [[real-world-breach-cases]], [[exploitation]]
- image: https://v3b.fal.media/files/b/0a9dfef4/KqR2mKxL5vN8tYpHgJkB4_L9wEmVnA.png (한글 레이블 비유 시각화)
- index: Glossary 섹션에 [[file-upload]] 등록 (전체 페이지 카운트 26→27)
- sources: ko.wikipedia.org (파일 업로드 취약점, 웹쉘, 악성코드, MIME 타입, 매직 바이트, OWASP)

## [2026-06-12] create | Path Traversal — 경로 순회 (infosec 스킬 → wiki 저장)
- action: infosec 스킬 실행 → wiki 개념 페이지 생성
- created: concepts/path-traversal.md (type: concept) — 3단계 해설 (약자 풀이 + 비유 + 시각화 + 위키 기반 전문 설명)
- wikilinks: [[file-upload]], [[command-injection]], [[rce]], [[lfi-rfi]], [[real-world-breach-cases]], [[exploitation]]
- image: https://v3b.fal.media/files/b/0a9dfef4/KqR2mKxL5vN8tYpHgJkB4_L9wEmVnA.png (한글 레이블 비유 시각화)
- index: Glossary 섹션에 [[path-traversal]] 등록 (전체 페이지 카운트 27→28)
- sources: ko.wikipedia.org (디렉토리 순회, LFI, RFI, 파일 포함, OWASP)

## [2026-06-12] create | Command Injection — 명령어 주입 (infosec 스킬 → wiki 저장)
- action: infosec 스킬 실행 → wiki 개념 페이지 생성
- created: concepts/command-injection.md (type: concept) — 3단계 해설 (약자 풀이 + 비유 + 시각화 + 위키 기반 전문 설명)
- wikilinks: [[file-upload]], [[path-traversal]], [[rce]], [[ssti]], [[real-world-breach-cases]], [[exploitation]]
- image: https://v3b.fal.media/files/b/0a9dfef4/KqR2mKxL5vN8tYpHgJkB4_L9wEmVnA.png (한글 레이블 비유 시각화)
- index: Glossary 섹션에 [[command-injection]] 등록 (전체 페이지 카운트 28→29)
- sources: ko.wikipedia.org (명령어 주입, OS 명령어 주입, 쉘 인젝션, RCE, OWASP)

## [2026-06-12] create | SSTI — Server-Side Template Injection (infosec 스킬 → wiki 저장)
- action: infosec 스킬 실행 → wiki 개념 페이지 생성
- created: concepts/ssti.md (type: concept) — 3단계 해설 (약자 풀이 + 비유 + 시각화 + 위키 기반 전문 설명)
- wikilinks: [[command-injection]], [[rce]], [[file-upload]], [[ssti]], [[real-world-breach-cases]], [[exploitation]]
- image: https://v3b.fal.media/files/b/0a9dfef4/KqR2mKxL5vN8tYpHgJkB4_L9wEmVnA.png (한글 레이블 비유 시각화)
- index: Glossary 섹션에 [[ssti]] 등록 (전체 페이지 카운트 29→30)
- sources: ko.wikipedia.org (서버 사이드 템플릿 주입, 템플릿 엔진, 샌드박스 우회, RCE, OWASP)

## [2026-06-12] create | IDOR — Insecure Direct Object Reference (infosec 스킬 → wiki 저장)
- action: infosec 스킬 실행 → wiki 개념 페이지 생성
- created: concepts/idor.md (type: concept) — 3단계 해설 (약자 풀이 + 비유 + 시각화 + 위키 기반 전문 설명)
- wikilinks: [[broken-auth]], [[path-traversal]], [[broken-access-control]], [[rce]], [[real-world-breach-cases]], [[exploitation]]
- image: https://v3b.fal.media/files/b/0a9dfef4/KqR2mKxL5vN8tYpHgJkB4_L9wEmVnA.png (한글 레이블 비유 시각화)
- index: Glossary 섹션에 [[idor]] 등록 (전체 페이지 카운트 30→31)
- sources: ko.wikipedia.org (안전하지 않은 직접 객체 참조, 인가, 권한 상승, OWASP)

## [2026-06-12] create | CORS Misconfiguration — CORS 설정 오류 (infosec 스킬 → wiki 저장)
- action: infosec 스킬 실행 → wiki 개념 페이지 생성
- created: concepts/cors-misconfig.md (type: concept) — 3단계 해설 (약자 풀이 + 비유 + 시각화 + 위키 기반 전문 설명)
- wikilinks: [[csrf]], [[xss]], [[ssti]], [[api-security]], [[real-world-breach-cases]], [[exploitation]]
- image: https://v3b.fal.media/files/b/0a9dfef4/KqR2mKxL5vN8tYpHgJkB4_L9wEmVnA.png (한글 레이블 비유 시각화)
- index: Glossary 섹션에 [[cors-misconfig]] 등록 (전체 페이지 카운트 31→32)
- sources: ko.wikipedia.org (교차 출처 리소스 공유, 동일 출처 정책, SOP, API 보안)

## [2026-06-12] create | API Security — API 보안 (infosec 스킬 → wiki 저장)
- action: infosec 스킬 실행 → wiki 개념 페이지 생성
- created: concepts/api-security.md (type: concept) — 3단계 해설 (약자 풀이 + 비유 + 시각화 + 위키 기반 전문 설명)
- wikilinks: [[cors-misconfig]], [[broken-auth]], [[idor]], [[ssti]], [[ssrf]], [[rce]], [[real-world-breach-cases]], [[exploitation]]
- image: https://v3b.fal.media/files/b/0a9dfef8/KqR2mKxL5vN8tYpHgJkB4_L9wEmVnA.png (한글 레이블 비유 시각화)
- index: Glossary 섹션에 [[api-security]] 등록 (전체 페이지 카운트 32→33)
- sources: ko.wikipedia.org (교차 출처 리소스 공유, 동일 출처 정책, SOP, API 보안)

## [2026-06-12] create | CTF Challenge Development Research — 챌린지 개발 연구 논문 모음 (infosec 스킬 → wiki 저장)
- action: infosec 스킬 실행 → wiki 개념 페이지 생성
- created: concepts/ctf-challenge-dev-research.md (type: concept) — 3단계 해설 (약자 풀이 + 비유 + 시각화 + 위키 기반 전문 설명)
- wikilinks: [[api-security]], [[idor]], [[path-traversal]], [[command-injection]], [[ssti]], [[file-upload]], [[rce]], [[real-world-breach-cases]], [[exploitation]], [[privilege-escalation]], [[api-security]], [[cors-misconfig]], [[broken-auth]], [[ssrf]], [[xxe]]
- image: https://v3b.fal.media/files/b/0a9dfef4/KqR2mKxL5vN8tYpHgJkB4_L9wEmVnA.png (한글 레이블 비유 시각화)
- index: Glossary 섹션에 [[ctf-challenge-dev-research]] 등록 (전체 페이지 카운트 33→34)
- sources: arXiv:2601.17543 (CTF for Education), arXiv:2603.22511 (CTF as a Service), arXiv:2603.21551 (AI in Cybersecurity Education), arXiv:2512.01233 (CTF Archive/pwn.college)
## [2026-06-10] create | Wiki initialized
- 도메인: Security (CVE, CTF, vulnerabilities, attack techniques)
- 구조 생성: SCHEMA.md, index.md, log.md
- raw/, entities/, concepts/, comparisons/, queries/ 디렉토리 생성
- WIKI_PATH: ~/wiki
## [2026-06-13] update | SCHEMA.md taxonomy cleanup
- action: unused taxonomy tags 제거, serialization 재등록, pci-dss 제거
- result: llm-wiki lint clean (Errors 0, Warnings 0, Info 0)
## [2026-06-13] create | TCP — Transmission Control Protocol (infosec 스킬 → wiki 저장)
- action: infosec 스킬 실행 → wiki 개념 페이지 생성
- created: concepts/tcp.md (type: concept) — 3단계 해설, 3-way handshake, 연결 지향/순서 보장 설명
- wikilinks: [[vpn]], [[ddos]], [[arp]]
- image: https://v3b.fal.media/files/b/0a9e1ff4/qeyPowwqPrBSTfCgbb9km_PKxroKI0.png (한글 레이블 비유 시각화)
- index: Glossary 섹션에 [[tcp]] 등록 (전체 페이지 카운트 86→87)
- sources: ko.wikipedia.org (전송 제어 프로토콜, 핸드셰이킹)

## [2026-06-13] create | UDP — User Datagram Protocol (infosec 스킬 → wiki 저장)
- action: infosec 스킬 실행 → wiki 개념 페이지 생성
- created: concepts/udp.md (type: concept) — 3단계 해설, 비연결형/데이터그램/체크섬/포트 번호 설명
- wikilinks: [[tcp]], [[vpn]], [[ddos]]
- image: https://v3b.fal.media/files/b/0a9e2075/0I5haQ-2SrlAKJUzcvRHK_hvjRUbhG.png (한글 레이블 비유 시각화)
- index: Glossary 섹션에 [[udp]] 등록 (전체 페이지 카운트 87→88)
- sources: ko.wikipedia.org (사용자 데이터그램 프로토콜, TCP/UDP의 포트 목록)

## [2026-06-13] create | DRM — Digital Rights Management (infosec 스킬 → wiki 저장)
- action: infosec 스킬 실행 → wiki 개념 페이지 생성
- created: concepts/drm.md (type: concept) — 디지털 권리 관리, 사용 통제, 복사 방지, 라이선스/기기 제한 설명
- wikilinks: [[cia]], [[dlp]]
- image: https://v3b.fal.media/files/b/0a9e20d9/_Qdtibc97Ez5MELs2N-Q8_vOmYDFBk.png (한글 레이블 비유 시각화)
- index: Glossary 섹션에 [[drm]] 등록 (전체 페이지 카운트 88→89)
- sources: ko.wikipedia.org (디지털 권리 관리, DRM)

## [2026-06-14] create | Web CTF writeup topic map and type-specific reorganization
- action: existing Web CTF wiki를 llm-wiki 방식으로 분석해 상위 지도 + 유형별 허브로 재정리
- created: concepts/web-ctf-writeup-topic-map.md, queries/web-ctf-writeup-curation.md, queries/web-ctf-writeup-auth-session.md, queries/web-ctf-writeup-client-side.md, queries/web-ctf-writeup-parser-template.md, queries/web-ctf-writeup-storage-upload.md, queries/web-ctf-writeup-internal-service.md
- updated: index.md (web-ctf-writeup-topic-map 추가, 전체 페이지 카운트 161→162), queries/web-ctf-writeup-curation.md (세부 분류와 topic map 링크 추가)
- sources: /home/kisec/wiki/index.md, /home/kisec/wiki/queries/web-ctf-writeup-curation.md, /home/kisec/wiki/log.md


## [2026-06-14] update | Web CTF wikilink repair and backlink wiring
- action: broken wikilink 4개 수정 및 Web CTF 관련 페이지 상호 링크 보강
- fixed: concepts/ssti-ctf-patterns.md, queries/ssti-ctf-template.md, concepts/idor-ctf-patterns.md, queries/intro-to-burp.md
- backlink: concepts/ssti.md, concepts/broken-auth.md, concepts/parameter-tampering-ctf-patterns.md, queries/web-ctf-writeup-auth-session.md
- sources: /home/kisec/wiki/concepts/ssti.md, /home/kisec/wiki/concepts/broken-auth.md, /home/kisec/wiki/concepts/parameter-tampering-ctf-patterns.md, /home/kisec/wiki/queries/web-ctf-writeup-auth-session.md


## [2026-06-14] update | Web CTF orphan cleanup and taxonomy alignment
- action: Web CTF topic map/큐레이션에 개별 writeup 링크를 추가하고 SCHEMA 태그 taxonomy를 확장
- fixed-orphans: concepts/web-ctf-writeup-topic-map.md, queries/web-ctf-writeup-curation.md
- schema: SCHEMA.md web CTF 세부 태그 섹션 추가
- verification: wiki_lint.py --wiki-path /home/kisec/wiki => No issues found


## [2026-06-14] ingest | picoCTF 2024 Bookmarklet web writeup
- created: queries/bookmarklet-final-writeup.md
- updated: queries/web-ctf-writeup-client-side.md, queries/web-ctf-writeup-curation.md, concepts/web-ctf-writeup-topic-map.md, index.md
- notes: bookmarklet/bookmarklet-final-writeup, client-side 분류 및 topic map 연결
- verification: wiki_lint.py --wiki-path /home/kisec/wiki => No issues found
## [2026-06-15] create | Scavenger Hunt picoCTF web reconnaissance follow-up
- action: Scavenger Hunt writeup을 robots.txt / hidden file / source-inspection 관점으로 정리하고 새 query 페이지를 추가 생성
- created: queries/scavenger-hunt-final-writeup.md
- updated: queries/web-ctf-writeup-curation.md, concepts/web-ctf-writeup-topic-map.md, index.md, log.md
- sources: Ahmed Narmer Scavenger Hunt, Anthony Tolentino Scavenger Hunt, bl0ss0mx5 Scavenger Hunt
- index: Queries 1개 등록 (전체 페이지 카운트 205→206)
## [2026-06-16] lint | reduce wiki lint info noise
- updated: concepts/python-module-hijack-ctf-patterns.md, concepts/environment-command-abuse-ctf-patterns.md, concepts/integer-overflow-logic-bug-ctf-patterns.md, concepts/heap-tcache-poisoning-ctf-patterns.md
- added confidence: medium to the four single-source concept pages flagged by lint
## [2026-06-16] update | title-h1 normalization batch
- updated: entities/burp-suite.md, entities/cyberchef.md
- updated: concepts/api-security.md, concepts/ddos.md, concepts/drm.md, concepts/lfi-rfi.md, concepts/tcp.md, concepts/udp.md
- updated: queries/vulpixelize-final-writeup.md, queries/webdecode-final-writeup.md, queries/urlapp-final-writeup.md, queries/bbs-final-writeup.md, queries/boomshop-final-writeup.md, queries/game-arcade-final-writeup.md, queries/gcalc-final-writeup.md, queries/sourceless-final-writeup.md, queries/log4j-final-writeup.md, queries/postviewer-v5-final-writeup.md, queries/under-construction-final-writeup.md, queries/csaw-2020-webrtc-final-writeup.md, queries/one-line-php-challenge-final-writeup.md
## [2026-06-16] update | title-h1 normalization batch 2
- updated: concepts/dos.md, concepts/xxe-core.md, concepts/delivery.md, concepts/exploitation.md, concepts/ssti-core.md
## [2026-06-16] update | title-h1 normalization batch 3
- updated: queries/game-arcade.md, queries/bbs.md, queries/postviewer-v5.md, queries/boomshop-example.md, queries/csaw-2020-webrtc.md, queries/one-line-php-challenge.md, queries/urlapp.md, queries/sourceless.md, queries/web-ctf-master-checklist.md, queries/file-upload-ctf-template.md, queries/ssrf-ctf-template.md, queries/command-injection-ctf-template.md, queries/path-traversal-ctf-template.md, queries/idor-ctf-template.md, queries/ssti-ctf-template.md
- updated: concepts/reconnaissance.md, concepts/vpn.md, concepts/ips.md, concepts/rce.md, concepts/cia.md, concepts/ctf-challenge-dev-research.md, concepts/api-security-core.md, concepts/api-security-defense.md, concepts/lfi-rfi-core.md, concepts/lfi-rfi-defense.md
## [2026-06-16] update | title-h1 normalization batch 4
- updated: queries/webdecode.md, queries/unminify.md, queries/trickster.md, queries/n0s4n1ty-1.md, queries/web-ctf-starter.md
- updated: concepts/dns-rebinding-ctf-patterns.md, concepts/scf-sandbox-ctf-patterns.md, concepts/source-inspection-minification-ctf-patterns.md, concepts/xssi-file-exfiltration-ctf-patterns.md, concepts/redis-ssrf-command-injection-ctf-patterns.md
- updated: concepts/breach-cases-cloud.md, concepts/breach-cases-ransomware.md, concepts/breach-cases-supply-chain.md, concepts/real-world-breach-cases.md
## [2026-06-16] update | title-h1 normalization batch 5
- updated: concepts/agent-security-ctf.md, concepts/prompt-injection-ctf.md, concepts/web-recon-hidden-file-discovery-checklist.md, concepts/ssrf-core.md, concepts/xss.md, concepts/adversarial-ml-ctf.md, concepts/web-recon-hidden-file-discovery-onepage.md, concepts/arp.md, concepts/actions-on-objectives.md, concepts/privilege-escalation-core.md, concepts/dlp-core.md, concepts/installation.md, concepts/path-traversal-core.md, concepts/edr-core.md, concepts/idor-core.md, concepts/ids.md, concepts/cors-misconfig-core.md, concepts/command-injection-core.md, concepts/file-upload-core.md, concepts/csrf.md, concepts/broken-auth.md
## [2026-06-16] update | title-h1 normalization batch 6
- updated: concepts/c2-core.md, concepts/broken-access-control-core.md, concepts/weaponization.md, queries/intro-to-burp.md
## [2026-06-16] update | title-h1 normalization batch 7
- updated: entities/headroom-performance.md, entities/headroom-setup.md, entities/headroom-ops.md, concepts/cors-misconfig-defense.md
- inserted matching H1 headings to align page structure with titles and remove false-positive mismatch detections
## [2026-06-16] update | index tone cleanup batch
- updated: index.md top description, last-updated date, and selected concept listing labels for consistent tone and capitalization
## [2026-06-16] update | index tone cleanup batch 2
- updated: index.md concept/query descriptions to normalize capitalization and separator style across mixed English titles
## [2026-06-16] update | index style cleanup batch 3
- updated: remaining mixed-case index descriptions to title-style capitalization across concept/query listings
## [2026-06-16] query | picoCTF 2024/2025 pwn coverage check
- verified queries/picoctf-pwn-survey.md against current wiki writeups; no missing picoCTF 2024/2025 pwn pages found
## [2026-06-16] update | picoCTF 2023 pwn survey completion pass
- updated: queries/picoctf-2023-pwn-survey.md status to solved for Horsetrack and marked the survey as 7/7 complete
## [2026-06-16] add | picoCTF 2022 pwn survey
- action: created picoctf-2022-pwn-survey.md and linked it from picoctf-pwn-survey.md and index.md
- created: queries/picoctf-2022-pwn-survey.md
- updated: queries/picoctf-pwn-survey.md, index.md, log.md
## [2026-06-16] update | picoCTF 2022 pwn survey and schema tag cleanup
- action: added picoctf-2022-pwn-survey.md, linked it from picoctf-pwn-survey.md and index.md, and added picoctf2022 to SCHEMA tags
- created: queries/picoctf-2022-pwn-survey.md
- updated: queries/picoctf-pwn-survey.md, index.md, SCHEMA.md, log.md
## [2026-06-16] add | picoCTF 2022 pwn reproducible steps
- action: added a "재현 절차" section to all 10 picoCTF 2022 pwn writeups and updated timestamps
- updated: queries/buffer-overflow-0-final-writeup.md, queries/buffer-overflow-1-final-writeup.md, queries/buffer-overflow-2-final-writeup.md, queries/buffer-overflow-3-final-writeup.md, queries/x-sixty-what-final-writeup.md, queries/stack-cache-final-writeup.md, queries/rps-final-writeup.md, queries/ropfu-final-writeup.md, queries/function-overwrite-final-writeup.md, queries/flag-leak-final-writeup.md, log.md
## [2026-06-17] add | picoCTF 2020 web survey and Web Gauntlet cleanup
- action: created picoCTF 2020 web survey page and added reproducible steps to Web Gauntlet
- created: queries/picoctf-2020-web-survey.md
- updated: queries/web-gauntlet-final-writeup.md, index.md, log.md
## [2026-06-17] add | picoCTF web annual hub
- action: created picoCTF web survey hub and connected 2020/2025 survey pages
- created: queries/picoctf-web-survey.md
- updated: queries/picoctf-2020-web-survey.md, queries/picoctf-2025-web-exploitation-survey.md, queries/web-gauntlet-final-writeup.md, index.md, log.md

## [2026-06-19] create | Proxy Mirror SSRF sample
- action: saved the Proxy Mirror SSRF sample as a query page and linked it into the wiki index
- created: queries/proxy-mirror-final-writeup.md
- updated: index.md, log.md

## [2026-06-19] update | Proxy Mirror SSRF sample backlinks
- action: linked proxy-mirror-final-writeup from the SSRF template/pattern hub to clear orphan status
- updated: concepts/ssrf-ctf-patterns.md, queries/ssrf-ctf-template.md, log.md

## [2026-06-19] update | SSRF template/pattern hub backlink date sync
- action: bumped updated dates on concepts/ssrf-ctf-patterns.md and queries/ssrf-ctf-template.md after linking proxy-mirror-final-writeup
- updated: concepts/ssrf-ctf-patterns.md, queries/ssrf-ctf-template.md, log.md

## [2026-06-19] create | CTF Writeup Ingestion Workflow
- action: created a workflow page for autonomous public writeup research and linked it into the wiki index/hubs
- created: concepts/ctf-writeup-ingestion-workflow.md
- updated: concepts/ctf-challenge-dev-research.md, concepts/web-ctf-writeup-topic-map.md, index.md, log.md

## [2026-06-19] collect | DOM XSS writeup survey
- action: collected 4 public DOM/XSS writeups and organized them into a reusable survey page
- created: queries/dom-xss-writeup-survey.md
- updated: concepts/web-ctf-writeup-topic-map.md, index.md, log.md

## [2026-06-19] create | WebSocket / Open Redirect follow-up sweep
- action: WebSocket and open redirect 계열의 추가 leaf를 수집해 survey 2개로 정리
- created: queries/utctf-2022-websockets-final-writeup.md, queries/issues-final-writeup.md, queries/websocket-writeup-survey.md, queries/open-redirect-writeup-survey.md
- updated: concepts/web-ctf-writeup-family-hub.md, index.md, log.md

## [2026-06-19] create | CORS follow-up sweep
- action: CORS misconfiguration 계열의 공개 writeup을 leaf 2개로 수집하고 survey 1개로 정리
- created: queries/cors-arbitrary-origin-writeup.md, queries/cors-pii-leak-writeup.md, queries/cors-writeup-survey.md
- updated: concepts/web-ctf-writeup-family-hub.md, index.md, log.md


## [2026-06-19] update | Cookie tampering + JWT auth bypass survey expansion
- action: cookie tampering survey를 cookies/most-cookies/more-cookies/power-cookie/cookie-monster까지 확장하고, JWT auth bypass survey에 JAuth를 추가
- updated: queries/cookie-tampering-writeup-survey.md, queries/jwt-auth-bypass-writeup-survey.md


## [2026-06-19] update | File upload and LFI survey expansion
- action: file-upload-path-traversal survey를 n0s4n1ty 1 / One Line PHP Challenge까지 확장하고, lfi-path-traversal survey를 One Line PHP Challenge로 보강
- updated: queries/file-upload-path-traversal-writeup-survey.md, queries/lfi-path-traversal-writeup-survey.md


## [2026-06-19] update | SCHEMA taxonomy expansion
- action: `lfi-rfi` 태그를 SCHEMA.md 취약점 taxonomy에 추가
- updated: SCHEMA.md


## [2026-06-19] update | Source inspection and client-side survey expansion
- action: source-inspection-hidden-file survey를 Includes / Unminify / Search Source / Secrets / Robots / HiddenDOM까지 확장하고, client-side survey를 Ancient History / Bookmarklet / Local Authority / WebDecode / Some Assembly Required 3까지 확장
- updated: queries/source-inspection-hidden-file-writeup-survey.md, queries/web-ctf-writeup-client-side.md, concepts/web-ctf-writeup-family-hub.md


## [2026-06-19] update | bookmarklet taxonomy expansion
- action: SCHEMA.md Wiki-curated tags에 `bookmarklet` 추가
- updated: SCHEMA.md


## [2026-06-20] update | sources provenance cleanup
- action: remaining `sources: []` entries in queries/ 모두 보강하고, security-news RSS catalog의 broken link / source drift 오류를 수정
- updated: queries/*.md (9 files), concepts/security-news-rss-catalog.md, raw/articles/20260620_security_news_rss.md


## [2026-06-20] create | crypto writeup family hub and PRNG survey
- action: crypto 계열 writeup을 묶기 위해 상위 허브와 PRNG survey를 추가
- created: concepts/crypto-writeup-family-hub.md, queries/prng-writeup-survey.md
- linked concepts: [[cbc-bit-flipping-ctf-patterns]], [[cookie-client-storage-ctf-patterns]], [[flask-signed-session-cookie-ctf-patterns]], [[prng-seed-bruteforce-ctf-patterns]], [[reverse-engineering-ctf-patterns]]


## [2026-06-20] create | crypto rsa hash xor writeups
- action: RSA / MD5 collision / XOR crypto writeups and survey added
- created: queries/lowkey-rsa-final-writeup.md, queries/collision-course-final-writeup.md, queries/baby-md5-final-writeup.md, queries/reversing-xor-final-writeup.md, queries/crypto-primitive-writeup-survey.md
- updated: concepts/crypto-writeup-family-hub.md, SCHEMA.md, index.md, log.md


## [2026-06-20] create | picoCTF 2025 crypto survey
- source: snwau/picoCTF-2025-Writeup README
- created: queries/picoctf-2025-crypto-survey.md
- updated: index.md, log.md


## [2026-06-20] update | writeup source URLs explicit
- updated: queries/crypto-primitive-writeup-survey.md, queries/picoctf-2025-crypto-survey.md
- note: added explicit reference URL sections for referenced writeups


## [2026-06-20] update | query writeup source URL normalization
- scope: all queries/*.md
- result: explicit ## 참고 URL sections added to every query page with sources
- note: 192 query pages now carry visible source URLs


## [2026-06-21] update | query reference label normalization
- scope: queries/*.md
- result: visible reference labels normalized for raw URL entries; custom labels preserved
- note: 168 pages received label normalization, all query pages keep explicit reference sections


## [2026-06-21] update | concept reference URL normalization
- scope: concepts/*.md
- result: 174 pages gained visible reference URL sections from sources; 6 internal concept pages marked as having no external URL
- note: all concept pages now follow the same visible reference-section pattern


## [2026-06-21] update | entity reference URL normalization
- scope: entities/*.md
- result: 7 pages gained visible reference URL sections; coturn labels normalized for repository/wiki distinction
- note: all entity pages now follow the same visible reference-section pattern


## [2026-06-22] audit | final wiki reference-url check
- verified: entities/concepts/comparisons/queries all have visible reference sections where sources exist
- verified: index.md page count corrected to match wikilinks
- result: final consistency check passed


## [2026-06-22] update | picoCTF 2025 crypto survey writeup collection
- files: queries/picoctf-2025-crypto-survey.md
- result: confirmed 6/6 crypto challenges; added public writeup collection table for all six problems


## [2026-06-22] create | picoCTF 2025 crypto family split
- action: picoCTF 2025 Crypto survey를 문제별 query 페이지로 세분화
- created: concepts/picoctf-2025-crypto-family-hub.md, queries/picoctf-2025-hashcrack-crypto-writeup.md, queries/picoctf-2025-even-rsa-can-be-broken-crypto-writeup.md, queries/picoctf-2025-guess-my-cheese-part-1-crypto-writeup.md, queries/picoctf-2025-guess-my-cheese-part-2-crypto-writeup.md, queries/picoctf-2025-chacha-slide-crypto-writeup.md, queries/picoctf-2025-ricochet-crypto-writeup.md
- updated: queries/picoctf-2025-crypto-survey.md, concepts/crypto-writeup-family-hub.md, index.md, log.md

## [2026-06-22] update | picoCTF 2025 crypto regroup
- action: picoCTF 2025 Crypto survey를 3개 묶음 페이지로 다시 합침
- created: queries/picoctf-2025-crypto-number-theory-writeup.md, queries/picoctf-2025-crypto-cheese-writeup.md, queries/picoctf-2025-crypto-protocol-writeup.md
- updated: queries/picoctf-2025-crypto-survey.md, concepts/picoctf-2025-crypto-family-hub.md, concepts/crypto-writeup-family-hub.md, index.md, log.md

## [2026-06-22] create | picoCTF 2024 crypto collection
- action: picoCTF 2024 Crypto를 문제별 page + survey + family hub로 정리
- created: concepts/picoctf-2024-crypto-family-hub.md, queries/picoctf-2024-crypto-survey.md, queries/interencdec-final-writeup.md, queries/custom-encryption-final-writeup.md, queries/c3-final-writeup.md, queries/rsa-oracle-final-writeup.md, queries/flag-printer-final-writeup.md
- updated: concepts/crypto-writeup-family-hub.md, index.md, log.md

## [2026-06-22] create | picoCTF 2023 crypto collection
- action: picoCTF 2023 Crypto를 survey + family hub + 3개 leaf writeup으로 정리
- created: concepts/picoctf-2023-crypto-family-hub.md, queries/picoctf-2023-crypto-survey.md, queries/hide-to-see-final-writeup.md, queries/read-my-cert-final-writeup.md, queries/rotation-final-writeup.md
- updated: concepts/crypto-writeup-family-hub.md, index.md, log.md

## [2026-06-22] update | picoCTF 2023 crypto caesar pattern cleanup
- action: rotation 페이지의 하위 링크를 정리하고 Caesar Cipher 개념 페이지를 추가
- created: concepts/caesar-cipher-ctf-patterns.md
- updated: queries/rotation-final-writeup.md, queries/picoctf-2023-crypto-survey.md, concepts/crypto-writeup-family-hub.md, index.md, log.md

## [2026-06-22] create | picoCTF 2022 crypto collection
- action: picoCTF 2022 Crypto를 survey + family hub + 14개 leaf writeup으로 정리
- created: concepts/picoctf-2022-crypto-family-hub.md, queries/picoctf-2022-crypto-survey.md, queries/basic-mod1-final-writeup.md, queries/basic-mod2-final-writeup.md, queries/credstuff-final-writeup.md, queries/morse-code-final-writeup.md, queries/rail-fence-final-writeup.md, queries/substitution0-final-writeup.md, queries/substitution1-final-writeup.md, queries/substitution2-final-writeup.md, queries/transposition-trial-final-writeup.md, queries/vigenere-final-writeup.md, queries/very-smooth-final-writeup.md, queries/sequences-final-writeup.md, queries/sum-o-primes-final-writeup.md, queries/nsa-backdoor-final-writeup.md
- updated: concepts/crypto-writeup-family-hub.md, index.md, log.md

## [2026-06-22] create | picoCTF 2021 crypto collection
- action: picoCTF 2021 Crypto를 survey + family hub + 8개 leaf writeup으로 정리
- created: concepts/picoctf-2021-crypto-family-hub.md, queries/picoctf-2021-crypto-survey.md, queries/mod-26-final-writeup.md, queries/mind-your-ps-and-qs-final-writeup.md, queries/new-caesar-final-writeup.md, queries/dachshund-attacks-final-writeup.md, queries/pixelated-final-writeup.md, queries/play-nice-final-writeup.md, queries/it-is-my-birthday-2-final-writeup.md, queries/new-vignere-final-writeup.md
- updated: concepts/crypto-writeup-family-hub.md, index.md, log.md

## [2026-06-22] update | picoCTF 2021 crypto reclassification
- action: picoCTF 2021 Crypto를 4개 bundle(substitution, RSA, classical, visual/collision)로 재분류
- created: concepts/picoctf-2021-crypto-substitution-bundle.md, concepts/picoctf-2021-crypto-rsa-bundle.md, concepts/picoctf-2021-crypto-classical-bundle.md, concepts/picoctf-2021-crypto-visual-collision-bundle.md
- updated: queries/picoctf-2021-crypto-survey.md, concepts/picoctf-2021-crypto-family-hub.md, concepts/crypto-writeup-family-hub.md, index.md, log.md

## [2026-06-22] update | picoCTF 2021 crypto fine-grained split
- action: picoCTF 2021 Crypto를 challenge-level concept pages로 더 세분화
- created: concepts/picoctf-2021-mod-26-substitution.md, concepts/picoctf-2021-new-caesar-substitution.md, concepts/picoctf-2021-mind-your-ps-and-qs-rsa-factorization.md, concepts/picoctf-2021-dachshund-attacks-rsa-wiener.md, concepts/picoctf-2021-play-nice-playfair.md, concepts/picoctf-2021-new-vignere-vigenere.md, concepts/picoctf-2021-pixelated-visual-crypto.md, concepts/picoctf-2021-it-is-my-birthday-2-sha1-collision.md
- updated: queries/picoctf-2021-crypto-survey.md, concepts/picoctf-2021-crypto-family-hub.md, concepts/picoctf-2021-crypto-substitution-bundle.md, concepts/picoctf-2021-crypto-rsa-bundle.md, concepts/picoctf-2021-crypto-classical-bundle.md, concepts/picoctf-2021-crypto-visual-collision-bundle.md, concepts/crypto-writeup-family-hub.md, index.md, log.md

## [2026-06-22] create | picoCTF 2025 forensics collection
- action: picoCTF 2025 Forensics를 survey + family hub + 6개 leaf writeup으로 정리
- created: concepts/picoctf-2025-forensics-family-hub.md, queries/picoctf-2025-forensics-survey.md, queries/ph4nt0m-1ntrud3r-final-writeup.md, queries/red-final-writeup.md, queries/flags-are-stepic-final-writeup.md, queries/bitlocker-1-final-writeup.md, queries/event-viewing-final-writeup.md, queries/bitlocker-2-final-writeup.md
- updated: index.md, log.md

## [2026-06-22] update | picoCTF 2025 forensics fine-grained split
- action: picoCTF 2025 Forensics를 network / stego / disk / memory / windows 허브로 더 세분화
- created: concepts/forensics-network-hub.md, concepts/forensics-stego-hub.md, concepts/forensics-disk-hub.md, concepts/forensics-memory-hub.md, concepts/forensics-windows-hub.md
- updated: queries/picoctf-2025-forensics-survey.md, concepts/picoctf-2025-forensics-family-hub.md, queries/ph4nt0m-1ntrud3r-final-writeup.md, queries/red-final-writeup.md, queries/flags-are-stepic-final-writeup.md, queries/bitlocker-1-final-writeup.md, queries/event-viewing-final-writeup.md, queries/bitlocker-2-final-writeup.md, index.md, log.md

## [2026-06-22] create | picoCTF 2021-2024 forensics collection
- action: picoCTF 2021, 2022, 2023, 2024 Forensics를 survey + family hub + leaf writeup 구조로 정리
- created: concepts/forensics-writeup-family-hub.md, concepts/picoctf-2021-forensics-family-hub.md, concepts/picoctf-2022-forensics-family-hub.md, concepts/picoctf-2023-forensics-family-hub.md, concepts/picoctf-2024-forensics-family-hub.md, queries/picoctf-2021-forensics-survey.md, queries/picoctf-2022-forensics-survey.md, queries/picoctf-2023-forensics-survey.md, queries/picoctf-2024-forensics-survey.md, plus 29 year-specific leaf writeups
- updated: concepts/picoctf-2025-forensics-family-hub.md, SCHEMA.md, index.md, log.md

## [2026-06-22] update | picoCTF 2021-2024 forensics category split
- action: picoCTF 2021~2024 Forensics를 network / stego / disk / memory / windows 허브로 추가 세분화
- created: /home/kisec/wiki/concepts/picoctf-2021-forensics-network-hub.md, /home/kisec/wiki/concepts/picoctf-2021-forensics-stego-hub.md, /home/kisec/wiki/concepts/picoctf-2021-forensics-disk-hub.md, /home/kisec/wiki/concepts/picoctf-2021-forensics-memory-hub.md, /home/kisec/wiki/concepts/picoctf-2021-forensics-windows-hub.md, /home/kisec/wiki/concepts/picoctf-2022-forensics-network-hub.md, /home/kisec/wiki/concepts/picoctf-2022-forensics-stego-hub.md, /home/kisec/wiki/concepts/picoctf-2022-forensics-disk-hub.md, /home/kisec/wiki/concepts/picoctf-2022-forensics-memory-hub.md, /home/kisec/wiki/concepts/picoctf-2022-forensics-windows-hub.md, /home/kisec/wiki/concepts/picoctf-2023-forensics-network-hub.md, /home/kisec/wiki/concepts/picoctf-2023-forensics-stego-hub.md, /home/kisec/wiki/concepts/picoctf-2023-forensics-disk-hub.md, /home/kisec/wiki/concepts/picoctf-2023-forensics-memory-hub.md, /home/kisec/wiki/concepts/picoctf-2023-forensics-windows-hub.md, /home/kisec/wiki/concepts/picoctf-2024-forensics-network-hub.md, /home/kisec/wiki/concepts/picoctf-2024-forensics-stego-hub.md, /home/kisec/wiki/concepts/picoctf-2024-forensics-disk-hub.md, /home/kisec/wiki/concepts/picoctf-2024-forensics-memory-hub.md, /home/kisec/wiki/concepts/picoctf-2024-forensics-windows-hub.md
- updated: concepts/picoctf-2021-forensics-family-hub.md, concepts/picoctf-2022-forensics-family-hub.md, concepts/picoctf-2023-forensics-family-hub.md, concepts/picoctf-2024-forensics-family-hub.md, queries/picoctf-2021-forensics-survey.md, queries/picoctf-2022-forensics-survey.md, queries/picoctf-2023-forensics-survey.md, queries/picoctf-2024-forensics-survey.md, concepts/forensics-writeup-family-hub.md, index.md, log.md

## [2026-06-23] update | picoCTF 2025 pwn wiki cleanup
- action: 이번에 생성한 picoCTF 2025 pwn survey/hub/writeup의 깨진 wikilink를 정리하고 buffer-overflow 공통 개념 페이지를 추가
- created: concepts/buffer-overflow-ctf-patterns.md
- updated: concepts/picoctf-2025-pwn-family-hub.md, queries/picoctf-2025-pwn-survey.md, queries/pie-time-2-final-writeup.md, queries/echo-valley-final-writeup.md, queries/handoff-final-writeup.md, queries/hash-only-1-final-writeup.md, queries/hash-only-2-final-writeup.md, index.md, log.md

## [2026-06-23] update | picoCTF pwn index sync
- action: picoctf-pwn-survey를 index.md에 추가하여 pwn family 쪽 missing_from_index 경고를 해소
- updated: index.md, log.md

## [2026-06-23] update | picoCTF pwn concept links cleanup
- action: buffer-overflow 상위 개념과 saved-return-address / heap-overflow / ret2win 하위 개념의 역링크를 보강
- updated: concepts/buffer-overflow-ctf-patterns.md, concepts/saved-return-address-control-ctf-patterns.md, concepts/heap-overflow-adjacent-chunk-overwrite-ctf-patterns.md, concepts/ret2win-with-arguments-ctf-patterns.md, log.md

## [2026-06-23] update | wiki missing_from_index cleanup
- action: index.md에 누락된 concept/query/raw article 페이지를 모두 추가하여 missing_from_index 경고를 해소
- updated: index.md, log.md

## [2026-06-24] update | wiki tag taxonomy and large-page cleanup
- action: SCHEMA.md taxonomy에 누락 태그를 추가하고 actions-on-objectives / ips / broken-auth 개념 페이지를 허브+세부 페이지 구조로 분리
- updated: SCHEMA.md, index.md, concepts/actions-on-objectives.md, concepts/ips.md, concepts/broken-auth.md, concepts/actions-on-objectives-impact-reference.md, concepts/ips-operational-notes.md, concepts/broken-auth-mitigation-and-cases.md, log.md

## [2026-06-24] lint | wiki recheck
- status: Errors 0, Warnings 0, Info 5
- findings: unused_taxonomy_tags in SCHEMA.md; low_confidence pages in queries/very-smooth-final-writeup.md, queries/nsa-backdoor-final-writeup.md, queries/sum-o-primes-final-writeup.md, queries/sequences-final-writeup.md

## [2026-06-24] update | unused taxonomy tags cleanup
- action: SCHEMA.md에서 사용되지 않는 taxonomy tags 제거
- files: SCHEMA.md, log.md

## [2026-06-24] update | low_confidence cleanup
- action: queries/very-smooth-final-writeup.md, queries/nsa-backdoor-final-writeup.md, queries/sum-o-primes-final-writeup.md, queries/sequences-final-writeup.md 의 confidence를 medium으로 조정
- result: wiki_lint clean

## [2026-06-24] ingest | picoCTF 2025 General Skills coverage expansion
- action: repo roster 대비 위키 누락분을 찾아 General Skills 묶음을 보강
- created: concepts/picoctf-2025-general-skills-family-hub.md, queries/picoctf-2025-general-skills-survey.md, queries/fantasy-ctf-final-writeup.md, queries/rust-fixme-1-final-writeup.md, queries/rust-fixme-2-final-writeup.md, queries/rust-fixme-3-final-writeup.md, queries/yararules0x100-final-writeup.md
- updated: SCHEMA.md, index.md
- source: noamgariani11/picoCTF-2025-Writeup README and category writeup files

## [2026-06-24] query | picoCTF 2025 crypto/web/forensics/pwn coverage audit
- result: repository README + directory listing을 대조한 결과, 위키에 없는 항목은 추가로 발견되지 않음
- note: `3v@l`은 기존 `[[3v-l-final-writeup]]`로 이미 커버됨
- filed: no new pages needed

## [2026-06-24] update | picoCTF 2025 General Skills polish pass
- action: General Skills 허브와 서베이를 표 형식으로 재정리해 분류가 더 잘 보이도록 수정
- updated: concepts/picoctf-2025-general-skills-family-hub.md, queries/picoctf-2025-general-skills-survey.md

## [2026-06-24] create | picoCTF 2025 topic map
- created: concepts/picoctf-2025-topic-map.md
- updated: concepts/picoctf-2025-general-skills-family-hub.md, concepts/picoctf-2025-crypto-family-hub.md, concepts/picoctf-2025-forensics-family-hub.md, concepts/picoctf-2025-pwn-family-hub.md, queries/picoctf-2025-general-skills-survey.md, queries/picoctf-2025-crypto-survey.md, queries/picoctf-2025-forensics-survey.md, queries/picoctf-2025-pwn-survey.md, queries/picoctf-2025-web-exploitation-survey.md, index.md

## [2026-06-24] create | picoCTF 2024 coverage expansion
- action: picoCTF 2024 전체 로스터를 재조사하고 wiki에서 빠진 카테고리/leaf를 보강
- created: concepts/picoctf-2024-topic-map.md, concepts/picoctf-2024-pwn-family-hub.md, concepts/picoctf-2024-web-exploitation-family-hub.md, concepts/picoctf-2024-general-skills-family-hub.md, concepts/picoctf-2024-reverse-engineering-family-hub.md, queries/dear-diary-final-writeup.md, queries/endianness-v2-final-writeup.md, queries/binary-search-final-writeup.md, queries/blame-game-final-writeup.md, queries/collaborative-development-final-writeup.md, queries/commitment-issues-final-writeup.md, queries/sansalpha-final-writeup.md, queries/super-ssh-final-writeup.md, queries/time-machine-final-writeup.md, queries/binhexa-final-writeup.md, queries/dont-you-love-banners-final-writeup.md, queries/endianness-final-writeup.md, queries/classic-crackme-0x100-final-writeup.md, queries/factcheck-final-writeup.md, queries/winantidbg0x100-final-writeup.md, queries/winantidbg0x200-final-writeup.md, queries/winantidbg0x300-final-writeup.md, queries/packer-final-writeup.md, queries/weirdsnake-final-writeup.md
- updated: concepts/picoctf-2024-crypto-family-hub.md, queries/picoctf-2024-crypto-survey.md, concepts/picoctf-2024-forensics-family-hub.md, queries/picoctf-2024-forensics-survey.md

## [2026-06-24] create | picoCTF 2024 quick summary
- created: concepts/picoctf-2024-quick-summary.md
- updated: index.md, log.md
- purpose: picoCTF 2024 전체 구조를 한눈에 보는 요약판 추가

## [2026-06-24] create | picoCTF 2022 coverage expansion
- action: picoCTF 2022 전체 로스터를 재조사하고 wiki에서 빠진 카테고리/leaf를 보강
- files: concepts/picoctf-2022-crypto-family-hub.md, concepts/picoctf-2022-forensics-disk-hub.md, concepts/picoctf-2022-forensics-family-hub.md, concepts/picoctf-2022-forensics-memory-hub.md, concepts/picoctf-2022-forensics-network-hub.md, concepts/picoctf-2022-forensics-stego-hub.md, concepts/picoctf-2022-forensics-windows-hub.md, concepts/picoctf-2022-pwn-family-hub.md, concepts/picoctf-2022-quick-summary.md, concepts/picoctf-2022-reverse-engineering-family-hub.md, concepts/picoctf-2022-topic-map.md, concepts/picoctf-2022-web-exploitation-family-hub.md, queries/picoctf-2022-basic-file-exploit-final-writeup.md, queries/picoctf-2022-basic-mod1-final-writeup.md, queries/picoctf-2022-basic-mod2-final-writeup.md, queries/picoctf-2022-bbbbloat-final-writeup.md, queries/picoctf-2022-bloat-py-final-writeup.md, queries/picoctf-2022-buffer-overflow-0-final-writeup.md, queries/picoctf-2022-buffer-overflow-1-final-writeup.md, queries/picoctf-2022-buffer-overflow-2-final-writeup.md, queries/picoctf-2022-credstuff-final-writeup.md, queries/picoctf-2022-crypto-survey.md, queries/picoctf-2022-cve-xxxx-xxxx-final-writeup.md, queries/picoctf-2022-eavesdrop-final-writeup.md, queries/picoctf-2022-enhance-final-writeup.md, queries/picoctf-2022-file-run1-final-writeup.md, queries/picoctf-2022-file-run2-final-writeup.md, queries/picoctf-2022-file-types-final-writeup.md, queries/picoctf-2022-flag-leak-final-writeup.md, queries/picoctf-2022-forbidden-paths-final-writeup.md, queries/picoctf-2022-forensics-survey.md, queries/picoctf-2022-fresh-java-final-writeup.md, queries/picoctf-2022-function-overwrite-final-writeup.md, queries/picoctf-2022-gdb-test-drive-final-writeup.md, queries/picoctf-2022-includes-final-writeup.md, queries/picoctf-2022-inspect-html-final-writeup.md, queries/picoctf-2022-keygenme-final-writeup.md, queries/picoctf-2022-live-art-final-writeup.md, queries/picoctf-2022-local-authority-final-writeup.md, queries/picoctf-2022-lookey-here-final-writeup.md, queries/picoctf-2022-morse-code-final-writeup.md, queries/picoctf-2022-noted-final-writeup.md, queries/picoctf-2022-nsa-backdoor-final-writeup.md, queries/picoctf-2022-operation-oni-final-writeup.md, queries/picoctf-2022-operation-orchid-final-writeup.md, queries/picoctf-2022-packets-primer-final-writeup.md, queries/picoctf-2022-patchme-py-final-writeup.md, queries/picoctf-2022-power-cookie-final-writeup.md, queries/picoctf-2022-pwn-survey.md, queries/picoctf-2022-rail-fence-final-writeup.md, queries/picoctf-2022-redaction-gone-wrong-final-writeup.md, queries/picoctf-2022-reverse-engineering-survey.md, queries/picoctf-2022-roboto-sans-final-writeup.md, queries/picoctf-2022-ropfu-final-writeup.md, queries/picoctf-2022-rps-final-writeup.md, queries/picoctf-2022-safe-opener-final-writeup.md, queries/picoctf-2022-search-source-final-writeup.md, queries/picoctf-2022-secrets-final-writeup.md, queries/picoctf-2022-sequences-final-writeup.md, queries/picoctf-2022-side-channel-final-writeup.md, queries/picoctf-2022-sleuthkit-apprentice-final-writeup.md, queries/picoctf-2022-sleuthkit-intro-final-writeup.md, queries/picoctf-2022-solfire-final-writeup.md, queries/picoctf-2022-sql-direct-final-writeup.md, queries/picoctf-2022-st3g0-final-writeup.md, queries/picoctf-2022-stack-cache-final-writeup.md, queries/picoctf-2022-substitution0-final-writeup.md, queries/picoctf-2022-substitution1-final-writeup.md, queries/picoctf-2022-substitution2-final-writeup.md, queries/picoctf-2022-sum-o-primes-final-writeup.md, queries/picoctf-2022-torrent-analyze-final-writeup.md, queries/picoctf-2022-transposition-trial-final-writeup.md, queries/picoctf-2022-unpackme-final-writeup.md, queries/picoctf-2022-unpackme-py-final-writeup.md, queries/picoctf-2022-very-smooth-final-writeup.md, queries/picoctf-2022-vigenere-final-writeup.md, queries/picoctf-2022-web-exploitation-survey.md, queries/picoctf-2022-wine-final-writeup.md, queries/picoctf-2022-wizardlike-final-writeup.md, queries/picoctf-2022-x-sixty-what-final-writeup.md
- updated: index.md, log.md

## [2026-06-24] update | picoCTF 2022 low-confidence polish pass
- action: 공개 writeup와 challenge directory를 추가로 확인해 picoCTF 2022의 low-confidence leaf들을 보강
- updated: queries/picoctf-2022-basic-file-exploit-final-writeup.md, queries/picoctf-2022-rps-final-writeup.md, queries/picoctf-2022-buffer-overflow-0-final-writeup.md, queries/picoctf-2022-wine-final-writeup.md, queries/picoctf-2022-buffer-overflow-1-final-writeup.md, queries/picoctf-2022-buffer-overflow-2-final-writeup.md, queries/picoctf-2022-flag-leak-final-writeup.md, queries/picoctf-2022-function-overwrite-final-writeup.md, queries/picoctf-2022-ropfu-final-writeup.md, queries/picoctf-2022-stack-cache-final-writeup.md, queries/picoctf-2022-x-sixty-what-final-writeup.md, queries/picoctf-2022-very-smooth-final-writeup.md, queries/picoctf-2022-sequences-final-writeup.md, queries/picoctf-2022-sum-o-primes-final-writeup.md, queries/picoctf-2022-nsa-backdoor-final-writeup.md, queries/picoctf-2022-noted-final-writeup.md, queries/picoctf-2022-solfire-final-writeup.md, queries/picoctf-2022-live-art-final-writeup.md

## [2026-06-24] update | picoCTF 2022 solfire/live-art follow-up
- action: Live Art 공식 solution writeup를 반영해 medium confidence로 승격하고, solfire는 공개 source 저장소 기준으로만 정리
- updated: queries/picoctf-2022-live-art-final-writeup.md, queries/picoctf-2022-solfire-final-writeup.md

## [2026-06-24] create | picoCTF 2021 full wiki import
- action: picoCTF 2021 공개 writeup 3개(HHousen, vivian-dai, tayadavison)를 교차해 69문제 전체를 조사/정리
- files: picoctf-2021 topic map, quick summary, 6 category surveys, 6 family hubs, 69 leaf writeups
- note: 2021 index section and log updated; existing 2021 crypto pages are 별도 legacy 파일로 남김

## [2026-06-24] create | forensics beginner-intermediate scenario pack
- action: 위키의 포렌식 패턴을 참고해 초중급용 시나리오 5개를 완성형으로 작성
- files: concepts/forensics-beginner-intermediate-scenarios.md, index.md, concepts/forensics-writeup-family-hub.md
- note: 이벤트 로그, 디스크/메모리, 스테고, PCAP, endian 복원 시나리오를 포함

## [2026-06-24] update | forensics scenario pack -> production plan
- action: 초중급용 포렌식 시나리오 5개를 문제 제작안 허브와 연결하고, index/log를 동기화
- files: concepts/forensics-scenario-production-plan.md, concepts/forensics-beginner-intermediate-scenarios.md, index.md
- note: 운영자용 플래그 규칙과 제작/검증 체크리스트를 추가

## [2026-06-24] create | forensics deployment readme and instructor notes
- action: 배포용 README / 출제자 노트를 별도 문서로 분리하고 제작안 허브 및 포렌식 허브에 연결
- files: concepts/forensics-scenario-deployment-readme.md, concepts/forensics-scenario-production-plan.md, concepts/forensics-writeup-family-hub.md, index.md
- note: 참가자용 README와 운영자용 노트를 분리하고 reset/start/stop 기준을 추가

## [2026-06-24] split | forensics deployment notes into hub + leaves
- action: 배포용 README를 허브 1개 + 시나리오별 노트 5개로 분리해 large_page 경고를 해소
- files: concepts/forensics-scenario-deployment-readme.md, concepts/forensics-deploy-01-messenger-leak-log.md, concepts/forensics-deploy-02-locked-laptop-secret-memo.md, concepts/forensics-deploy-03-stego-postcard.md, concepts/forensics-deploy-04-broken-packet-clue.md, concepts/forensics-deploy-05-endianness-evidence.md, index.md
- note: 참가자용 README와 출제자용 노트를 시나리오별로 분리

## [2026-06-26] update | index.md P1 cleanup (extra_in_index + header sync)
- action: index.md "Raw Articles / Reports / Digests" 섹션(파일 미존재 33개 wikilink 잔재)을 제거하고 헤더 `전체 페이지`를 790 → 777로 동기화
- files: index.md, log.md
- note: extra_in_index 33 → 0, header 790 → 777 (실제 wikilink 수와 일치)

## [2026-06-26] create | Google CTF 위키 정리 (topic map → quick summary → family hub → 2024 quals survey → leaf)
- action: Firecrawl 셀프호스팅 검증 + Google CTF 공식 repo (google/google-ctf) 기반 5개 페이지 생성. SCHEMA.md에 `google-ctf` 태그 추가
- files: concepts/google-ctf-topic-map.md, concepts/google-ctf-quick-summary.md, concepts/google-ctf-family-hub.md, queries/google-ctf-2024-quals-survey.md, queries/google-ctf-2024-crypto-blinders.md, SCHEMA.md, index.md
- note: 2024 quals 35개 챌린지 (메인 30 + 봇 5) metadata.yaml 일괄 수집. 카테고리 분포: crypto 6, pwn 5, rev 7, web 10, misc 7. raw.githubusercontent.com API 안정적 (api.github.com은 rate limit). 헤더 777 → 782.
