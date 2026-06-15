---
source_url: https://github.com/hyperreality/best-web-ctf-writeups
ingested: 2026-06-13
sha256: 8b8d38aa7bc29e47ba8c846f62d5e278cc5a0bb73c232a8fe97cf0458b20bf50
---

# Web CTF Writeup 리소스 조사 결과 (2026-06-13)

## 조사 개요
- 조사일: 2026-06-13
- 조사자: Hermes Agent (security-research skill 활용)
- 목적: Web CTF 문제 풀이 학습을 위한 Writeup 리소스 종합 정리

---

## 1. 엄선된 Web Writeup 모음 (품질 검증됨)

### hyperreality/best-web-ctf-writeups
- **Stars**: 2.3k+
- **특징**: Web만 전문, Google CTF/GoogleCTF 중심, 초보자용 PicoCTF 포함
- **선정 기준**: "문제를 잘 설명함", "초보자가 이해할 수 있게 모든 단계 기술", "솔루션 스크립트/코드 포함", "흥미롭고 잘 알려지지 않거나 구식이지 않은 기법"
- **카테고리**: XSS, SQL Injection, XXE, CSS, DOM-based, Prototype Pollution, CSP Bypass 등
- **추천 시작점**: PicoCTF writeups (하단) → GoogleCTF (상위)
- **URL**: https://github.com/hyperreality/best-web-ctf-writeups

### orangetw/My-CTF-Web-Challenges
- **Stars**: 2.8k
- **특징**: HITCON CTF 출제자(Orange Tsai) 직접 작성, 2025년까지 업데이트
- **내용**: HITCON CTF 2014-2025 Web 챌린지 소스코드, 익스플로잇, 라이트업
- **최신 업데이트**: 10개월 전 (HITCON CTF 2025 추가)
- **URL**: https://github.com/orangetw/My-CTF-Web-Challenges

### p4-team/ctf
- **Stars**: 1.8k
- **특징**: 세계 최상위 팀(p4)의 10년치 아카이브, 솔버 스크립트 포함
- **구조**: 연도별/대회별 디렉토리 (2015~2023), 각 문제별 writeup + solver script
- **URL**: https://github.com/p4-team/ctf

### ByteBandits/writeups
- **Stars**: 104
- **특징**: 위키 스타일, CSAW/ASIS 등 주요 대회 커버
- **URL**: https://github.com/ByteBandits/writeups

---

## 2. 종합 리소스 큐레이션

### apsdehal/awesome-ctf
- **Stars**: 11.6k
- **특징**: CTF 종합 리스트, Web 섹션 별도 존재
- **URL**: https://github.com/apsdehal/awesome-ctf

### devploit/awesome-ctf-resources
- **Stars**: 771
- **특징**: Web 카테고리별 도구/플랫폼/라이트업 정리, 최신(3주 전 업데이트)
- **URL**: https://github.com/devploit/awesome-ctf-resources

---

## 3. 실시간/최신 Writeup 플랫폼

### CTFtime.org Writeups
- **특징**: 대회 직후 실시간 업로드, 태그 필터링 가능 (`web` 태그로 필터)
- **URL**: https://ctftime.org/writeups

### PortSwigger Web Security Academy
- **특징**: 무료, 실습+라이트업 통합, 초중급 필수 코스
- **URL**: https://portswigger.net/web-security

---

## 4. 한국어 Writeup 블로그 (학습용 추천)

| 블로그 | 특징 |
|--------|------|
| theori.io/ko/blog | CTF 입문 가이드, Web 해킹 기초 정리 |
| blog.hokyun.dev | DEFCON Quals 등 상위 대회 Web 라이트업 |
| one3147.tistory.com | CCE CTF, LA CTF 등 한국어 상세 풀이 |
| hyungin0505.tistory.com | LA CTF 2024 등 실전 참가기 |
| nduc193.github.io | KMA CTF 등 Web Exploitation 전문 |
| skysquirrel.tistory.com | CTF-D 등 실전 문제 풀이 |

---

## 5. 학습 로드맵 추천

### Step 1: 기초 다지기 (1-2주)
- PortSwigger Web Academy 무료 코스 수강 (SQLi, XSS, CSRF, SSRF, XXE 등 핵심 모듈)

### Step 2: PicoCTF Web 문제 풀이 (1주)
- best-web-ctf-writeups의 PicoCTF 섹션부터 시작
- 라이트업 보며 **직접 다시 풀기** (단순 읽기 지양)

### Step 3: 실전 대회 문제 분석 (지속)
| 난이도 | 추천 소스 | 학습 방법 |
|--------|-----------|-----------|
| 입문 | PicoCTF, GoogleCTF 2017-2019 | 라이트업 보고 재현 → 변형해보기 |
| 초중급 | HITCON CTF (orangetw repo), CSAW | 솔버 스크립트 분석 → 수동으로도 풀기 |
| 중급 | GoogleCTF 2020+, DEFCON Quals | 라이트업 없이 시도 → 막히면 부분 참고 |
| 고급 | p4-team 최신 대회, 0CTF/TCTF | 팀 단위 스터디 권장 |

### Step 4: 나만의 Writeup 작성 습관
- 템플릿: 문제 개요 → 접근 과정 → 핵심 기법 → 익스플로잇 코드 → 배운 점
- ~/ctf-writeups/ 폴더 만들어 대회별/카테고리별 정리

---

## 6. 효율적 검색 팁

```bash
# GitHub에서 Web 라이트업 검색 (star 순)
https://github.com/search?q=web+ctf+writeup&type=repositories&s=stars&o=desc

# CTFtime에서 web 태그 필터링
https://ctftime.org/writeups?tags=web

# 특정 대회 라이트업 찾기 (예: GoogleCTF 2024 web)
https://github.com/search?q=GoogleCTF+2024+web+writeup&type=repositories
```

---

## 7. 관련 기존 위키 페이지

- [[xss]] - XSS (Cross-Site Scripting) 용어 해설
- [[sql-injection]] - SQL Injection 용어 해설
- [[ssrf]] - SSRF (Server-Side Request Forgery) 용어 해설
- [[xxe]] - XXE (XML External Entity) 용어 해설
- [[cors-misconfig]] - CORS Misconfiguration 용어 해설
- [[ssti]] - SSTI (Server-Side Template Injection) 용어 해설
- [[file-upload]] - File Upload 취약점 용어 해설
- [[path-traversal]] - Path Traversal 용어 해설
- [[idor]] - IDOR 용어 해설
- [[command-injection]] - Command Injection 용어 해설
- [[broken-auth]] - Broken Authentication 용어 해설
- [[ai-ctf-overview]] - AI CTF 개요 및 8개 대분류
- [[prompt-injection-ctf]] - Prompt Injection CTF 상세
- [[agent-security-ctf]] - Agent/Tool Security CTF 상세
- [[adversarial-ml-ctf]] - Adversarial ML CTF 상세