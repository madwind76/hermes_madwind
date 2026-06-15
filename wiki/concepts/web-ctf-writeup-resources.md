---
title: Web CTF Writeup 리소스 가이드
created: 2026-06-13
updated: 2026-06-13
type: concept
tags: [ctf, ctf-challenge, web, reference, tutorial]
sources: [raw/articles/20260613_web-ctf-writeup-resources.md]
confidence: high
---

# Web CTF Writeup 리소스 가이드

Web CTF 문제 풀이 학습을 위한 **검증된 Writeup 리소스**와 **체계적 학습 로드맵**을 정리한 페이지입니다.

## 개요

2026-06-13 기준으로 수집된 Web CTF Writeup 주요 소스들을 품질, 난이도, 언어별로 분류했습니다. [원본 조사 데이터(raw/articles/20260613_web-ctf-writeup-resources.md)]에서 핵심만 추렸습니다.

---

## 주요 리소스 분류

### 1. 엄선된 고품질 Writeup 모음 (최우선 추천)

| 저장소 | ⭐ | 난이도 | 특징 | 추천 순서 |
|--------|---|--------|------|-----------|
| **hyperreality/best-web-ctf-writeups** | 2.3k+ | 입문~고급 | Web 전문, Google CTF 중심, **선정 기준 명시**, PicoCTF 포함 | **1순위** |
| **orangetw/My-CTF-Web-Challenges** | 2.8k | 중~고급 | HITCON 출제자 직접 작성, **소스코드+익스플로잇+라이트업** 모두 제공 | 2순위 |
| **p4-team/ctf** | 1.8k | 중~고급 | **세계 최상위 팀** 10년 아카이브, **솔버 스크립트 포함** | 3순위 |
| **ByteBandits/writeups** | 104 | 중급 | 위키 스타일, CSAW/ASIS 등 주요 대회 커버 | 4순위 |

### 2. 종합 큐레이션 리포지토리

| 저장소 | ⭐ | 용도 |
|--------|---|------|
| **apsdehal/awesome-ctf** | 11.6k | CTF 전체 자원 탐색, Web 섹션 참조 |
| **devploit/awesome-ctf-resources** | 771 | Web 도구/플랫폼/라이트업 최신 정리 |

### 3. 실시간/학습 플랫폼

| 플랫폼 | 용도 | 비고 |
|--------|------|------|
| **CTFtime.org Writeups** | 최신 대회 라이트업 실시간 확인 | `web` 태그 필터 사용 |
| **PortSwigger Web Security Academy** | **기초 필수**, 실습+라이트업 통합 | 무료, 초중급 완전 커버 |

### 4. 한국어 라이트업 블로그

| 블로그 | 강점 |
|--------|------|
| **theori.io/ko/blog** | 입문 가이드, 기초 체계적 정리 |
| **blog.hokyun.dev** | DEFCON Quals 등 최상위 대회 Web 분석 |
| **one3147.tistory.com** | CCE/LA CTF 한국어 상세 풀이 |
| **nduc193.github.io** | KMA CTF 등 Web Exploitation 전문 |

---

## 추천 학습 로드맵

### Phase 1: 기초 완성 (1-2주) — **필수**
```
PortSwigger Web Academy → 전체 모듈 수강
- SQL Injection, XSS, CSRF, SSRF, XXE, SSTI, File Upload 등
- 각 랩 직접 풀고 라이트업 읽기
```

### Phase 2: 입문 실전 (1주)
```
best-web-ctf-writeups → PicoCTF 섹션
- 10-15개 문제 **직접 풀기** (라이트업만 읽지 않기)
- 막히면 힌트 → 다시 시도 → 라이트업 확인 순서
```

### Phase 3: 실전 대회 분석 (지속)
```
난이도별 추천 소스:
├── 입문: PicoCTF, GoogleCTF 2017-2019
├── 초중급: HITCON CTF (orangetw), CSAW Quals
├── 중급: GoogleCTF 2020+, DEFCON Quals, SECCON
└── 고급: p4-team 최신, 0CTF/TCTF, PlaidCTF
```

### Phase 4: 아웃풋 습관화
- **나만의 Writeup 저장소** 운영 (GitHub + GitHub Pages 권장)
- 템플릿: 개요 → 정찰 → 취약점 분석 → 익스플로잇 → 패치/방어 → 회고

---

## 핵심 Web 취약점 유형별 기존 위키 링크

기초 개념은 기존 용어 해설 페이지 참조:

- [[xss]] — XSS (Cross-Site Scripting)
- [[sql-injection]] — SQL Injection
- [[ssrf]] — SSRF (Server-Side Request Forgery)
- [[xxe]] — XXE (XML External Entity)
- [[ssti]] — SSTI (Server-Side Template Injection)
- [[file-upload]] — File Upload 취약점
- [[path-traversal]] — Path Traversal
- [[idor]] — IDOR (Insecure Direct Object Reference)
- [[command-injection]] — Command Injection
- [[cors-misconfig]] — CORS Misconfiguration
- [[broken-auth]] — Broken Authentication
- [[csrf]] — CSRF (Cross-Site Request Forgery)

---

## 관련 CTF 위키 페이지

- [[ai-ctf-overview]] — AI CTF 개요 (8대 분류)
- [[prompt-injection-ctf]] — Prompt Injection CTF 상세
- [[agent-security-ctf]] — Agent/Tool Security CTF 상세
- [[adversarial-ml-ctf]] — Adversarial ML CTF 상세
- [[ctf-challenge-dev-research]] — CTF 챌린지 개발 연구

---

## 검색 팁

```bash
# GitHub star 순 검색
https://github.com/search?q=web+ctf+writeup&type=repositories&s=stars&o=desc

# CTFtime web 태그
https://ctftime.org/writeups?tags=web

# 특정 대회 (예: GoogleCTF 2024 web)
https://github.com/search?q=GoogleCTF+2024+web+writeup&type=repositories
```

---

## 다음 액션 제안

1. **PortSwigger Web Academy** 오늘부터 시작 (가장 ROI 높음)
2. **best-web-ctf-writeups** README 정독 후 PicoCTF 5개 풀기
3. 본인 GitHub에 `ctf-writeups` 레포 생성 → 첫 Writeup 업로드
4. 필요 시: 특정 취약점 유형(SQLi, XSS 등)별 **엄선 라이트업 5-10개** 추가 큐레이션 요청