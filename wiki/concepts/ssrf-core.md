---
title: SSRF (Server-Side Request Forgery, 서버 측 요청 위조) — 보안 용어 해설
created: 2026-06-12
updated: 2026-06-16
type: concept
tags: [security, glossary, web, ssrf, server-side, request-forgery, cloud-metadata, bypass, owasp]
sources: [https://ko.wikipedia.org/wiki/SSRF, https://ko.wikipedia.org/wiki/OWASP]
confidence: high
---

# SSRF (Server-Side Request Forgery, 서버 측 요청 위조) — 보안 용어 해설

## Step 1: 단어 직역 및 쉬운 비유

### 1. 약자 풀이

**SSRF** = **S**erver-**S**ide **R**equest **F**orgery

| 약자 | 원래 단어 | 직역 | 의미 |
|------|-----------|------|------|
| **S** | **Server** | 서버 | 백엔드 애플리케이션 서버 |
| **S** | **Side** | 측, 편 | 클라이언트가 아닌 서버 쪽에서 |
| **R** | **Request** | 요청 | HTTP/기타 프로토콜 요청 |
| **F** | **Forgery** | 위조, 변조 | 가짜로 만듦 |

### 2. 의미 조합

> **"공격자가 서버에게 '이 URL로 요청 좀 보내줘'라고 시켜서, 서버가 내부망/클라우드 메타데이터/관리자 페이지 등 외부에서 접근 불가능한 자원에 접근하게 만드는 공격"**

### 3. 강력한 비유: "심부름꾼(서버)을 시켜 금고(내부망) 열게 하기"

```
┌────────────────────────────────────────────────────────────┐
│  상황: 당신은 외부인(공격자). 회사 금고(내부망/메타데이터) │
│  는 외부에서 못 들어감. 하지만 심부름꾼(서버)은 안으로     │
│  들어갈 수 있음. 심부름꾼에게 "이 열쇠(내부 URL)로 금고     │
│  좀 열어봐"라고 시킴                                          │
└────────────────────────────────────────────────────────────┘

🏢  **심부름꾼 시나리오 (SSRF 공격 흐름)**

  ① **정상 기능**: 웹앱에 "이미지 URL 입력하면 썸네일 생성해줌" 기능 존재
     - 사용자: `https://example.com/image.png` 입력
     - 서버: 해당 URL로 GET 요청 → 이미지 다운로드 → 썸네일 생성 → 반환

  ② **공격자 악용**: 외부 URL 대신 **내부 전용 URL** 입력
     - 공격자: `http://localhost/admin` (관리자 페이지)
     - 공격자: `http://169.254.169.254/latest/meta-data/iam/security-credentials/` (AWS 메타데이터)
     - 공격자: `file:///etc/passwd` (로컬 파일 읽기)
     - 공격자: `http://192.168.1.50:8080` (내부망 다른 서버)

  ③ **서버의 순진한 실행**: 
     "어? 사용자가 URL 줬네? 내가 대신 요청해서 결과 돌려줘야지!"
     → **서버 자신의 권한(내부망 접근 가능)으로 요청 수행**

  ④ **결과**: 공격자가 외부에서 절대 접근 못 하는 자원 탈취
     - 클라우드 IAM 자격증명 (AWS/GCP/Azure 메타데이터)
     - 내부 관리자 패널 / 개발 도구 / DB 관리 콘솔
     - 로컬 파일 시스템 (`file://` 프로토콜)
     - 내부망 포트 스캔 / 서비스 탐색

💡 **핵심 포인트**: 
- **CSRF** = "피해자 브라우저가 요청 보내게 함" (클라이언트 사이드)
- **SSRF** = "서버가 요청 보내게 함" (서버 사이드)
- 서버는 **내부망/클라우드 내부**에 있으므로 **외부에서 못 보는 것 다 보임**
- "서버를 내 편으로 만들어 내부 탐색시키는 공격"
```

---

## Step 2: 개념 시각화

![SSRF 비유 시각화: 심부름꾼으로 설명하는 SSRF — 공격자(외부인), 웹 서버(심부름꾼), 내부망/클라우드(회사 건물 내부), 관리자 페이지(금고), 메타데이터 서비스(열쇠 보관함), 로컬 파일(비밀 문서) - 한글 레이블 포함](https://v3b.fal.media/files/b/0a9dfeb4/KqR2mKxL5vN8tYpHgJkB4_L9wEmVnA.png)

**이미지 설명**:
- **공격자(외부인)** — 직접 내부망 접근 불가, 서버를 통해 우회 시도
- **웹 서버(심부름꾼)** — 사용자 입력 URL을 대신 요청해주는 기능 보유, 내부망 접근 권한 있음
- **내부망/클라우드(회사 건물 내부)** — 외부 차단, 서버만 접근 가능
- **관리자 페이지(금고)** — 내부에서만 접속 가능한 민감 기능
- **메타데이터 서비스(열쇠 보관함)** — 클라우드 자격증명/설정 정보 보유 (169.254.169.254)
- **로컬 파일(비밀 문서)** — `file://` 프로토콜로 서버 로컬 파일 읽기 가능

> ⚠️ **참고**: 이미지 생성 도구가 PNG 형식으로 반환했습니다. 스킬 요구사항(.jpg/.jpeg)은 현재 도구 제약상 PNG로 대체됩니다.

---

## Step 3: 전문 용어 설명 (위키백과/OWASP/PortSwigger 기반)
### SSRF (Server-Side Request Forgery, 서버 측 요청 위조)

**정의**: **SSRF(Server-Side Request Forgery)**는 웹 애플리케이션이 **사용자 입력을 검증 없이 외부 리소스 요청에 사용**할 때 발생하는 취약점으로, 공격자가 **서버에게 임의의 URL로 요청을 보내도록 조작하여, 서버가 접근 가능한 내부망 자원(클라우드 메타데이터, 관리자 페이지, 데이터베이스, 로컬 파일 등)에 무단 접근하게 만드는 공격**이다.

### 공격 원리: 서버의 신뢰성 악용

| 요소 | 설명 |
|------|------|
| **신뢰 경계 위반** | 서버는 "사용자가 준 URL"을 신뢰하고 자신이 직접 요청 수행 |
| **네트워크 위치 이점** | 서버는 **DMZ/내부망/클라우드 VPC 내부**에 위치 → 외부 차단 자원 접근 가능 |
| **프로토콜 핸들러** | `http/https` 외에도 `file://`, `dict://`, `ftp://`, `gopher://`, `ldap://` 등 지원 시 공격 표면 확대 |
| **응답 반환 여부** | **Blind SSRF**: 응답 안 돌려줌 (시간/에러 기반 탐지) / **Non-Blind**: 응답 내용 반환 (직접 데이터 탈취) |

### SSRF 공격 대상 분류

| 대상 카테고리 | 구체적 대상 | 영향 |
|--------------|-------------|------|
| **클라우드 메타데이터** | `http://169.254.169.254/` (AWS/GCP/Azure 공통) | IAM 자격증명, 사용자 데이터, 네트워크 설정, 인스턴스 ID 탈취 → **계정 완전 장악** |
| **내부 관리자 패널** | `http://localhost/admin`, `http://127.0.0.1:8080/console` | 인증 우회, 관리자 기능 실행, DB 콘솔 접근 |
| **내부 서비스/API** | `http://internal-api:8080`, `http://service-mesh:9090` | 마이크로서비스 간 통신 악용, 권한 상승 |
| **데이터베이스/NoSQL** | `http://localhost:27017`, `http://redis:6379` (HTTP 인터페이스) | 데이터 유출/변조, NoSQL 인젝션 결합 |
| **로컬 파일 시스템** | `file:///etc/passwd`, `file:///proc/self/environ`, `file:///app/config.py` | 소스코드 유출, 설정 파일(DB 비밀키 등) 탈취 |
| **내부망 포트 스캔** | `http://192.168.1.1:22`, `http://10.0.0.5:3306` | 내부 토폴로지 매핑, 서비스 버전 탐지, 횡단 이동 기점 확보 |
| **서버 자체 정보** | `http://localhost/server-status`, `http://127.0.0.1:8080/actuator/env` | 환경 변수, 설정, 버전 정보, 스레드 덤프 |

### SSRF 공격 기법 및 우회 방법

| 기법 | 설명 | 우회 대상 |
|------|------|-----------|
| **로컬호스트 별칭** | `localhost`, `127.0.0.1`, `0.0.0.0`, `[::1]`, `0`, `2130706433` (127.0.0.1 정수) | 블랙리스트 필터 |
| **도메인 리다이렉트** | 공격자 도메인 → `127.0.0.1`로 A 레코드 설정 (`evil.com A 127.0.0.1`) | 도메인 기반 화이트리스트 |
| **DNS 리바인딩** | 최초 `evil.com` → 외부 IP → 이후 `127.0.0.1`로 변경 (TTL 0) | IP 기반 화이트리스트, TOCTOU |
| **CIDR/서브넷 우회** | `127.1.1.1`, `127.255.255.255`, `169.254.x.x` (링크로컬) | `127.0.0.1/8`만 차단 시 |
| **IPv6 표기** | `::1`, `::ffff:127.0.0.1`, `[::1]` | IPv4만 필터링 |
| **URL 인코딩/더블 인코딩** | `%31%32%37...`, `%2531%2532...` | 단순 문자열 매칭 필터 |
| **프로토콜 핸들러** | `file://`, `dict://`, `ftp://`, `gopher://`, `ldap://`, `tftp://` | HTTP/HTTPS만 허용 시 |
| **URL 파싱 차이 악용** | `@`, `#`, `?`, 파싱 라이브러리별 차이 (`urlparse` vs `requests` 등) | 화이트리스트 도메인 검증 로직 |
| **HTTP 리다이렉트 체인** | `http://evil.com → 302 → http://169.254.169.254/...` | 최초 URL만 검증하는 경우 |
| **청크/스트림 응답** | 큰 파일 다운로드 → 메모리/디스크 소진 (DoS) | 가용성 공격 |

### SSRF 공격 시나리오별 실전 예시

| 시나리오 | 페이로드 예시 | 탈취 정보 |
|----------|---------------|-----------|
| **AWS 메타데이터 자격증명** | `http://169.254.169.254/latest/meta-data/iam/security-credentials/` | IAM 역할 임시 자격증명 (AccessKey/SecretKey/Token) |
| **GCP 메타데이터** | `http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/token` | OAuth2 액세스 토큰 |
| **Azure IMDS** | `http://169.254.169.254/metadata/identity/oauth2/token?api-version=2018-02-01&resource=https://management.azure.com/` | Azure AD 액세스 토큰 |
| **Kubernetes 서비스어카운트** | `http://127.0.0.1:8001/api/v1/namespaces/default/secrets` | K8s 시크릿, 컨피그맵, 서비스어카운트 토큰 |
| **Spring Boot Actuator** | `http://localhost:8080/actuator/env`, `/actuator/heapdump`, `/actuator/logfile` | 환경변수(DB 비번), 힙덤프(메모리 내 비밀키), 로그 |
| **Redis/Elasticsearch** | `http://localhost:9200/_cat/indices`, `http://redis:6379/info` | 인덱스/키 목록, 메모리 덤프 |
| **내부 GitLab/Jenkins** | `http://gitlab.internal/api/v4/projects`, `http://jenkins.internal/script` | 소스코드, 파이프라인, 크리덴셜 |
| **파일 읽기 (LFI 결합)** | `file:///etc/passwd`, `file:///proc/self/environ`, `file:///app/.env` | 시스템 계정, 환경변수, 애플리케이션 비밀키 |


## 관련 위키 링크
- [[ssrf]] — 인덱스 페이지
- [[ssrf-defense]] — 분할 페이지
- [[rce]]
