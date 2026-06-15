---
title: SSRF — 방어
created: 2026-06-12
updated: 2026-06-13
type: concept
tags: [security, glossary, web, ssrf, server-side, request-forgery, cloud-metadata, bypass, owasp]
sources: [https://ko.wikipedia.org/wiki/SSRF, https://ko.wikipedia.org/wiki/OWASP]
confidence: high
---
> [[ssrf]]의 후반부입니다.

## Step 3: 전문 용어 설명 (위키백과/OWASP/PortSwigger 기반)
### SSRF 방어 기법

| 방어 계층 | 기법 | 구현 예시 | 효과/한계 |
|----------|------|-----------|-----------|
| **네트워크/인프라** | **메타데이터 서비스 차단/제한** | AWS IMDSv2 강제 (`HttpTokens=required`), GCP 메타데이터 방화벽, Azure IMDS 프라이빗 링크 | **가장 확실** — 서버 자체가 접근 못 하므로 근본 차단 |
| | **아웃바운드 트래픽 제한** | 보안 그룹/NACL로 필요한 외부 API만 허용, 내부 CIDR 차단 | 인프라 레벨 방어, 우회 어려움 |
| | **프록시/게이트웨이 경유** | 모든 아웃바운드 요청을 프록시 경유 (Squid, Envoy) → 로깅/필터링/차단 | 중앙 집중 제어, 성능 오버헤드 |
| **애플리케이션** | **화이트리스트 기반 URL 검증** | 허용 도메인/IP/CIDR 목록만 허용, `urlparse`로 호스트 추출 후 비교 | **가장 권장** — 블랙리스트 무용 |
| | **프로토콜 제한** | `http/https`만 허용, `file/dict/ftp/gopher` 등 차단 | `urllib.parse.urlparse(url).scheme in ('http','https')` |
| | **내부 IP 대역 차단** | `127.0.0.0/8`, `10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`, `169.254.0.0/16`, `fc00::/7` | `ipaddress.ip_address(host).is_private` (Python) |
| | **DNS 리바인딩 방지** | DNS 캐시 TTL 준수, 요청 시점 IP 재확인 (TOCTOU 방지) | `socket.getaddrinfo()`로 실시간 확인 |
| | **리다이렉트 금지/제한** | `allow_redirects=False` 또는 화이트리스트 도메인만 리다이렉트 허용 | `requests.get(url, allow_redirects=False)` |
| | **응답 크기/타임아웃 제한** | 대용량 다운로드/스트리밍 방지, 5초 타임아웃 | DoS/리소스 고갈 방지 |
| | **SSRF 토큰/서명** | 내부 서비스 간 호출 시 서명된 토큰 요구 (mTLS, JWT, HMAC) | 마이크로서비스 간 인증 강화 |
| **모니터링/탐지** | **아웃바운드 요청 로깅/알림** | 비정상 호출(내부 IP, 메타데이터 IP, 비허용 프로토콜) 실시간 알림 | SIEM/EDR 연계, 위협 헌팅 쿼리 |
| | **허니팟/캐니토큰** | 가짜 메타데이터 엔드포인트 배포 → 접근 시 즉각 알림 | 조기 탐지, 공격자 추적 |

### 언어/프레임워크별 안전한 HTTP 클라이언트 설정

| 언어/프레임워크 | 안전한 설정 예시 |
|----------------|------------------|
| **Python (requests)** | `requests.get(url, allow_redirects=False, timeout=5, hooks={'response': validate_redirect})` + 커스텀 `HTTPAdapter`로 IP 필터링 |
| **Python (httpx)** | `httpx.Client(follow_redirects=False, timeout=5, limits=httpx.Limits(max_connections=10))` + `event_hooks`로 검증 |
| **Go (net/http)** | `http.Client{Timeout: 5*time.Second, CheckRedirect: func(req *http.Request, via []*http.Request) error { return http.ErrUseLastResponse }}` + 커스텀 `DialContext`로 IP 필터 |
| **Java (HttpClient)** | `HttpClient.newBuilder().followRedirects(Redirect.NEVER).connectTimeout(Duration.ofSeconds(5)).build()` + `InetAddress.isSiteLocalAddress()` 검증 |
| **Node.js (axios/fetch)** | `axios.get(url, {maxRedirects: 0, timeout: 5000, validateStatus: null})` + `dns.lookup`으로 IP 확인 후 내부망 차단 |
| **PHP (Guzzle/cURL)** | `curl_setopt($ch, CURLOPT_FOLLOWLOCATION, false); curl_setopt($ch, CURLOPT_TIMEOUT, 5);` + `CURLOPT_RESOLVE`로 IP 고정 |
| **.NET (HttpClient)** | `HttpClientHandler{AllowAutoRedirect=false, MaxConnectionsPerServer=10}` + `HttpClientHandler.DangerousAcceptAnyServerCertificateValidator` 주의 |

### SSRF 탐지 및 테스트

| 방법 | 도구/기법 |
|------|-----------|
| **자동 스캔** | OWASP ZAP (SSRF 스캔 규칙), Burp Suite Collaborator (Out-of-band 탐지), Nuclei SSRF 템플릿 |
| **수동 테스트** | Burp Collaborator URL 주입 → DNS/HTTP 상호작용 확인, 내부 포트 스캔 페이로드 테스트 |
| **코드 리뷰** | 사용자 입력 URL을 `requests.get()`, `HttpClient.SendAsync()`, `axios.get()` 등에 직접 전달하는 코드 탐색 |
| **CI/CD 통합** | Nuclei, Semgrep, CodeQL SSRF 룰 적용, PR 시 자동 스캔 |
| **런타임 탐지** | Falco, Tetragon, eBPF 기반 아웃바운드 연결 모니터링 (컨테이너/K8s 환경) |

### 주요 SSRF 사고 사례

| 사고 | 연도 | 공격 벡터 | 피해 |
|------|------|-----------|------|
| **Capital One** | 2019 | WAF SSRF → EC2 메타데이터 → IAM 역할 → S3 버킷 700개 접근 | 1억 6백만 명 신용카드 신청 데이터 유출 |
| **Shopify** | 2018 | 이미지 프록시 SSRF → 내부 서비스 접근 | 내부 API 문서, 관리자 패널 접근 (버그바운티 $20,000) |
| **GitLab** | 2021 | Webhook URL SSRF → 내부 레지스트리/쿠버네티스 API | CVE-2021-22205, RCE로 발전 가능 |
| **Microsoft Exchange** | 2021 | SSRF → 백엔드 서비스 인증 우회 (ProxyLogon 체인) | CVE-2021-26855, 전 세계 수만 서버 침해 |

### SSRF vs CSRF 비교

| 구분 | **SSRF** | **CSRF** |
|------|----------|----------|
| **전체 이름** | Server-Side Request Forgery | Cross-Site Request Forgery |
| **주체** | **서버**가 요청 보냄 | **피해자 브라우저**가 요청 보냄 |
| **목표** | 서버가 접근 가능한 **내부 자원** 탈취 | 피해자 권한으로 **상태 변경** 요청 |
| **공격자 위치** | 외부 → 서버 통해 내부망 접근 | 외부 → 피해자 브라우저 통해 대상 사이트 |
| **핵심 메커니즘** | 서버의 아웃바운드 요청 기능 악용 | 브라우저의 쿠키 자동 첨부 악용 |
| **주요 피해** | 클라우드 키, 내부망 토폴로지, 관리자 패널, 로컬 파일 | 계정 탈취, 자금 이체, 권한 변경, 게시글 작성 |
| **방어 핵심** | 아웃바운드 제한, URL 화이트리스트, 메타데이터 차단 | CSRF 토큰, SameSite 쿠키, Referer 검증 |

---


## 관련 위키 링크

- [[csrf]] — CSRF (클라이언트 사이드 요청 위조, SSRF와 대조)
- [[rce]] — RCE (SSRF가 내부 서비스 RCE로 이어지는 체인 가능)
- [[command-and-control]] — C2 (SSRF로 클라우드 자격증명 탈취 시 C2 인프라 구축)
- [[actions-on-objectives]] — 목표 달성 (SSRF로 메타데이터 키 탈취 → 데이터 유출/랜섬웨어)
- [[real-world-breach-cases]] — 실제 침해 사례 (Capital One SSRF 사례 분석)

---

## 참고 문헌

- 한국어 위키백과: [서버 측 요청 위조](https://ko.wikipedia.org/wiki/서버_측_요청_위조)
- OWASP: [Server-Side Request Forgery](https://owasp.org/www-community/attacks/Server_Side_Request_Forgery)
- PortSwigger: [Server-side request forgery (SSRF)](https://portswigger.net/web-security/ssrf)
- AWS: [IMDSv2로 인스턴스 메타데이터 보호](https://docs.aws.amazon.com/ko_kr/AWSEC2/latest/UserGuide/configuring-instance-metadata-service.html)
- Capital One Breach Analysis: [SSRF를 통한 클라우드 자격증명 탈취](https://www.capitalone.com/tech/cloud/capital-one-cloud-security/)
## 관련 위키 링크
- [[ssrf]] — 인덱스 페이지
- [[ssrf-core]] — 분할 페이지
- [[rce]]
