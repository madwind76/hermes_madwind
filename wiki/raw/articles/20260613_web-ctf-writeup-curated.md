---
source_url: https://github.com/hyperreality/best-web-ctf-writeups + https://github.com/orangetw/My-CTF-Web-Challenges + https://github.com/p4-team/ctf + https://ctftime.org/writeups
ingested: 2026-06-13
sha256: c0a10105d12694d2ed15a0353311af8d2da4449974f62d284fe542e8a720c114
---

# Web CTF 취약점 유형별 엄선 Writeup 큐레이션 (2026-06-13)

조사 소스: best-web-ctf-writeups, orangetw/My-CTF-Web-Challenges, p4-team/ctf, CTFtime, PortSwigger
선정 기준: 교육적 가치, 재현 가능성, 기법 다양성, 최신성(2020년 이후 우선)

---

## 1. XSS (Cross-Site Scripting) — 엄선 7개

| # | 문제/대회 | 연도 | 핵심 기법 | 난이도 | 출처 | 학습 포인트 |
|---|-----------|------|-----------|--------|------|-------------|
| 1 | **Pasteurize** (GoogleCTF) | 2020 | DOMPurify bypass, mutation XSS | 중급 | best-web-ctf-writeups | DOMPurify 최신 버전 우회, parser differential |
| 2 | **All The Little Things** (GoogleCTF) | 2020 | Prototype pollution → DOM clobbering → CSP bypass | 고급 | best-web-ctf-writeups | 체인 익스플로잇, CSP strict-dynamic 우회 |
| 3 | **Bypasses Everywhere** (INS'hAck) | 2019 | XSS Auditor, CSP bypass, iframe sandbox escape | 중급 | best-web-ctf-writeups | 구형 방어 기법 우회 역사적 관점 |
| 4 | **gCalc** (GoogleCTF) | 2018 | CSP bypass via JSONP, angular sandbox escape | 중고급 | best-web-ctf-writeups | AngularJS 샌드박스 탈출, CSP policy 분석 |
| 5 | **X Sanitizer** (GoogleCTF) | 2017 | CSP bypass, encoding confusion | 중급 | best-web-ctf-writeups | 인코딩 혼란, CSP nonce 우회 |
| 6 | **Postview** (HITCON CTF) | 2022 | DOMPurify 2.3.6 bypass, mXSS | 고급 | orangetw/My-CTF-Web-Challenges | 최신 DOMPurify 버전 mXSS |
| 7 | **XSS Challenge** (PortSwigger Lab) | 2023+ | Reflected/Stored/DOM XSS 전 유형 실습 | 입문~중급 | PortSwigger Academy | 체계적 실습, 레벨별 난이도 |

**추천 학습 순서**: PortSwigger(입문) → Pasteurize → gCalc → X Sanitizer → Bypasses Everywhere → All The Little Things → Postview(고급)

---

## 2. SQL Injection — 엄선 7개

| # | 문제/대회 | 연도 | 핵심 기법 | 난이도 | 출처 | 학습 포인트 |
|---|-----------|------|-----------|--------|------|-------------|
| 1 | **gLotto** (GoogleCTF) | 2019 | MySQL ORDER-based blind, JSON extraction | 중급 | best-web-ctf-writeups | ORDER BY 인젝션, JSON 함수 활용 데이터 추출 |
| 2 | **SQLi Challenge** (PortSwigger) | 2023+ | Union, Blind, Time-based, OOB 전 유형 | 입문~고급 | PortSwigger Academy | MySQL/PostgreSQL/SQLite/Oracle 다중 DB |
| 3 | **Web350** (HITCON CTF) | 2021 | Second-order SQLi, WAF bypass | 고급 | orangetw/My-CTF-Web-Challenges | 2차 인젝션, WAF 회피 기법 |
| 4 | **Blind SQLi** (CSAW Quals) | 2022 | Boolean-based blind, 자동화 스크립트 작성 | 중급 | p4-team/ctf | 자동화 툴 없이 수동 익스플로잇 이해 |
| 5 | **NoSQL Injection** (DEFCON Quals) | 2021 | MongoDB $where, $regex 오퍼레이터 악용 | 중급 | CTFtime | NoSQL 인젝션, JSON 기반 쿼리 조작 |
| 6 | **PostgreSQL Injection** (0CTF) | 2020 | pg_sleep, dblink, COPY TO 프로그래밍 | 고급 | p4-team/ctf | PostgreSQL 고유 기능 악용, 파일 읽기/쓰기 |
| 7 | **SQLite Injection** (GoogleCTF) | 2022 | UNION 공격, 첨부 파일 메타데이터 유출 | 중급 | best-web-ctf-writeups | SQLite 제약사항, 가상 테이블 공격 |

**추천 학습 순서**: PortSwigger(기초) → gLotto → Blind SQLi(CSAW) → NoSQL → PostgreSQL → SQLite → Web350(HITCON)

---

## 6. File Upload — 엄선 5개

| # | 문제/대회 | 연도 | 핵심 기법 | 난이도 | 출처 |
|---|-----------|------|-----------|--------|------|
| 1 | File Upload Challenge (PortSwigger) | 2023+ | 확장자 우회, MIME 타입, 매직 바이트, 폴리글랏 | 입문~중급 | PortSwigger |
| 2 | Image Upload (HITCON CTF) | 2022 | ExifTool 인젝션, 이미지 리사이징 우회, 웹쉘 업로드 | 중고급 | orangetw |
| 3 | Avatar Upload (GoogleCTF) | 2021 | SVG 업로드 → XSS/XXE, Content-Type confusion | 중급 | best-web-ctf-writeups |
| 4 | Document Upload (CSAW) | 2022 | .docx/.pdf 폴리글랏, XML 파서 악용 | 고급 | p4-team |
| 5 | Chunked Upload (DEFCON Quals) | 2023 | 청크 업로드 로직 결함, 경로 순회 결합 | 고급 | CTFtime |
