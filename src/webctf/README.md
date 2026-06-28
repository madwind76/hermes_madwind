# Web CTF 문제 시나리오 저장소 (Total 100 Scenarios)

이 저장소는 다양한 웹 취약점을 학습하고 진증할 수 있는 총 100개의 **웹 CTF 문제 시나리오** 마크다운 파일 컬렉션을 포함하고 있습니다. 각 시나리오 파일은 상세한 개요, 아키텍처, 공격 면(Attack Surface), 공격 흐름(Exploitation Flow), 취약 코드 스니펫 및 완화 방안(Mitigation)을 다룹니다.

---

## 1. 난이도 구성
- **심화/중급 난이도 (Medium ~ Hard | 1 ~ 80번)**: 복잡한 체이닝 공격, 샌드박스 우회, 프로토타입 오염 RCE, 요청 스머글링 등 고도화된 웹 취약점 분석 능력을 요구하는 문제들입니다.
- **초급 난이도 (Easy | 81 ~ 100번)**: 웹 보안의 기본이 되는 OWASP Top 10 기반의 클래식 웹 취약점(정석적인 SQLi, XSS, Path Traversal, IDOR 등)의 기초 원리를 파악할 수 있는 문제들입니다.

---

## 2. 시나리오 요약 목록 (1 ~ 100)

| 번호 | 시나리오 파일명 | 핵심 취약점 | 난이도 | 요약 및 핵심 개념 |
| :--- | :--- | :--- | :--- | :--- |
| **01** | [scenario-1-ai-agent-ssrf.md](file:///home/kisec/src/webctf/scenario-1-ai-agent-ssrf.md) | AI Agent SSRF | Hard | LLM/AI 에이전트의 프롬프트 주입을 악용하여 내부망 SSRF를 유발하는 시나리오 |
| **02** | [scenario-2-websocket-race-condition.md](file:///home/kisec/src/webctf/scenario-2-websocket-race-condition.md) | WebSocket Race Condition | Hard | WebSocket 통신 중 비동기 처리 격차를 노린 포인트 중복 차감 등의 경쟁 상태 유발 |
| **03** | [scenario-3-jwt-algorithm-confusion.md](file:///home/kisec/src/webctf/scenario-3-jwt-algorithm-confusion.md) | JWT Algorithm Confusion | Medium | 비대칭키(RS256)로 서명된 JWT를 대칭키(HS256)로 해석하게 유도하여 서명을 조작 |
| **04** | [scenario-4-ssti-sandbox-escape.md](file:///home/kisec/src/webctf/scenario-4-ssti-sandbox-escape.md) | SSTI Sandbox Escape | Hard | Python Jinja2 환경에서 환경 변수 차단이나 필터가 존재하는 샌드박스를 우회해 RCE 달성 |
| **05** | [scenario-5-dns-rebinding-ssrf.md](file:///home/kisec/src/webctf/scenario-5-dns-rebinding-ssrf.md) | DNS Rebinding SSRF | Hard | DNS 응답 TTL 만료 단시간 내 IP 변경을 유발해 로컬망 접근 필터링을 우회하는 SSRF |
| **06** | [scenario-6-modern-sqli-json-extraction.md](file:///home/kisec/src/webctf/scenario-6-modern-sqli-json-extraction.md) | Modern SQLi (JSON) | Medium | 최신 웹 프레임워크가 DB 내 JSON 형식 데이터를 처리할 때 주입되는 쿼리 조작 |
| **07** | [scenario-7-dom-clobbering-xss.md](file:///home/kisec/src/webctf/scenario-7-dom-clobbering-xss.md) | DOM Clobbering XSS | Medium | HTML 요소를 변조해 자바스크립트 전역 변수나 속성을 덮어씌워 DOM XSS 트리거 |
| **08** | [scenario-8-flask-session-bruteforce.md](file:///home/kisec/src/webctf/scenario-8-flask-session-bruteforce.md) | Flask Session Bruteforce | Medium | 취약하게 설정된 Flask Secret Key를 무차별 대입으로 알아내어 세션 데이터를 위조 |
| **09** | [scenario-9-xxe-xml-injection.md](file:///home/kisec/src/webctf/scenario-9-xxe-xml-injection.md) | XXE (XML External Entity) | Medium | 외부 엔티티 파싱이 활성화된 XML 파서를 통해 서버 내부 파일 유출 및 SSRF 트리거 |
| **10** | [scenario-10-nosql-mongodb-injection.md](file:///home/kisec/src/webctf/scenario-10-nosql-mongodb-injection.md) | NoSQL Injection (MongoDB) | Medium | 몽고DB 조회 시 특수 쿼리 연산자(`$ne`, `$gt`) 객체를 직접 파라미터로 대입해 인증 우회 |
| **11** | [scenario-11-csrf-content-type-bypass.md](file:///home/kisec/src/webctf/scenario-11-csrf-content-type-bypass.md) | CSRF Content-Type Bypass | Medium | Content-Type 검증 미비점을 찔러 단순 폼 데이터 대신 JSON 데이터를 위조 전송하는 CSRF |
| **12** | [scenario-12-python-pickle-deserialization.md](file:///home/kisec/src/webctf/scenario-12-python-pickle-deserialization.md) | Pickle Deserialization RCE | Hard | Python pickle 모듈의 역직렬화 시 `__reduce__` 메소드 호출 메커니즘을 이용한 RCE |
| **13** | [scenario-13-prototype-pollution-rce.md](file:///home/kisec/src/webctf/scenario-13-prototype-pollution-rce.md) | Prototype Pollution RCE | Hard | Node.js 환경에서 전역 객체 프로토타입에 임의 키-값을 주입하여 쉘 명령어 실행 유도 |
| **14** | [scenario-14-pdf-generator-ssrf.md](file:///home/kisec/src/webctf/scenario-14-pdf-generator-ssrf.md) | PDF Generator SSRF | Medium | HTML을 PDF로 변환하는 라이브러리 가동 시 내부 HTML에 `<iframe>` 등을 실어 로컬망 SSRF |
| **15** | [scenario-15-graphql-introspection-abuse.md](file:///home/kisec/src/webctf/scenario-15-graphql-introspection-abuse.md) | GraphQL Introspection Abuse | Medium | 활성화된 GraphQL Introspection 쿼리를 분석하여 비공개 스키마와 쿼리 구조 정보 탈취 |
| **16** | [scenario-16-http-request-smuggling.md](file:///home/kisec/src/webctf/scenario-16-http-request-smuggling.md) | HTTP Request Smuggling | Hard | 프론트 프록시와 백엔드 서버 간의 Transfer-Encoding 및 Content-Length 파싱 해석 불일치 공격 |
| **17** | [scenario-17-lfi-session-poisoning.md](file:///home/kisec/src/webctf/scenario-17-lfi-session-poisoning.md) | LFI Session Poisoning | Medium | 세션 파일 경로 파악 후 세션 데이터에 PHP 코드를 주입하여 LFI와 결합해 RCE 유발 |
| **18** | [scenario-18-oauth-redirect-token-stealing.md](file:///home/kisec/src/webctf/scenario-18-oauth-redirect-token-stealing.md) | OAuth Redirect Token Stealing | Medium | OAuth 인증 흐름 상의 리디렉션 경로 화이트리스트 필터를 우회하여 공격자 서버로 토큰 유출 |
| **19** | [scenario-19-ssrf-gopher-redis-rce.md](file:///home/kisec/src/webctf/scenario-19-ssrf-gopher-redis-rce.md) | SSRF Gopher to Redis RCE | Hard | gopher 프로토콜 페이로드를 조작 및 인젝션하여 내부망 Redis 서버에 악성 쉘 스크립트 작성 |
| **20** | [scenario-20-sqli-order-by-blind.md](file:///home/kisec/src/webctf/scenario-20-sqli-order-by-blind.md) | ORDER BY Blind SQLi | Medium | dynamic 정렬(`ORDER BY`) 쿼리 매개변수 검증 부재를 노려 참/거짓 기반으로 데이터를 식별 |
| **21** | [scenario-21-aws-metadata-ssrf-bypass.md](file:///home/kisec/src/webctf/scenario-21-aws-metadata-ssrf-bypass.md) | AWS Metadata SSRF Bypass | Hard | AWS IMDSv2의 Token 기반 헤더 방어 정책을 SSRF 결합을 활용해 우회하고 자격증명 획득 |
| **22** | [scenario-22-file-upload-htaccess-rce.md](file:///home/kisec/src/webctf/scenario-22-file-upload-htaccess-rce.md) | .htaccess File Upload RCE | Hard | 업로드 제약을 피하기 위해 `.htaccess` 설정 파일을 업로드하여 php 실행 권한을 강제 획득 |
| **23** | [scenario-23-uuid-prediction-idor.md](file:///home/kisec/src/webctf/scenario-23-uuid-prediction-idor.md) | UUID Prediction IDOR | Medium | 시드(seed)와 타임스탬프 예측을 통하여 무작위 형태의 UUID IDOR 통제 장치를 추측 우회 |
| **24** | [scenario-24-header-sql-injection.md](file:///home/kisec/src/webctf/scenario-24-header-sql-injection.md) | HTTP Header SQLi | Medium | HTTP 헤더(예: Client-IP, X-Forwarded-For) 파싱 가공 시 발생하는 정교한 SQL 인젝션 |
| **25** | [scenario-25-css-injection-keylogger.md](file:///home/kisec/src/webctf/scenario-25-css-injection-keylogger.md) | CSS Injection Keylogger | Hard | 속성 선택자를 이용해 한 글자씩 문자를 수집하고 외부 서버로 CSS 웹폰트를 통해 유출 |
| **26** | [scenario-26-ssti-nodejs-pug-rce.md](file:///home/kisec/src/webctf/scenario-26-ssti-nodejs-pug-rce.md) | Node.js Pug SSTI RCE | Hard | Express Pug 템플릿 컴파일러 상에서 속성 인젝션 가동으로 샌드박스를 우회해 RCE 달성 |
| **27** | [scenario-27-webrtc-ip-leakage.md](file:///home/kisec/src/webctf/scenario-27-webrtc-ip-leakage.md) | WebRTC IP Leakage | Medium | VPN 혹은 프록시 하위 환경에서 WebRTC API를 사용해 피해자의 실제 로컬 IP 정보를 노출 |
| **28** | [scenario-28-git-repository-exposure.md](file:///home/kisec/src/webctf/scenario-28-git-repository-exposure.md) | Git Repository Exposure | Medium | 웹 상에 방치된 `.git` 폴더의 인덱스 파일과 오브젝트들을 스캔하여 소스코드 덤프 및 복원 |
| **29** | [scenario-29-jwt-none-algorithm-bypass.md](file:///home/kisec/src/webctf/scenario-29-jwt-none-algorithm-bypass.md) | JWT None Algorithm Bypass | Medium | JWT의 `alg` 헤더를 `none` 또는 대소문자 변형으로 변경 후 서명을 삭제하여 인증 통과 |
| **30** | [scenario-30-graphql-alias-batching.md](file:///home/kisec/src/webctf/scenario-30-graphql-alias-batching.md) | GraphQL Alias Batching | Medium | 단일 요청 내에서 다수의 별칭(Alias) 쿼리를 병합 발송하여 계정 비밀번호 대입 무력화 |
| **31** | [scenario-31-hash-length-extension.md](file:///home/kisec/src/webctf/scenario-31-hash-length-extension.md) | Hash Length Extension | Hard | MD5/SHA1 등 취약 해시 기반 인증 부속 검사 상황에서 원문 패딩 길이를 복제하여 서명 위조 |
| **32** | [scenario-32-xpath-injection.md](file:///home/kisec/src/webctf/scenario-32-xpath-injection.md) | XPath Injection | Medium | XML 파서 노드 조회 조건에 구문을 인젝션하여 비공개 데이터를 강제 반환 및 탐색 |
| **33** | [scenario-33-ssrf-ffmpeg-hls-playlist.md](file:///home/kisec/src/webctf/scenario-33-ssrf-ffmpeg-hls-playlist.md) | FFmpeg HLS SSRF | Hard | 미디어 업로드 기능에서 HLS 동영상 재생목록의 세그먼트 주소 스펙을 변조하여 SSRF 유도 |
| **34** | [scenario-34-node-serialize-rce.md](file:///home/kisec/src/webctf/scenario-34-node-serialize-rce.md) | Node-Serialize RCE | Hard | Node.js `node-serialize` 모듈 사용 시 즉시 실행 함수(IIFE) 객체를 주입해 원격 명령 구동 |
| **35** | [scenario-35-race-condition-file-write.md](file:///home/kisec/src/webctf/scenario-35-race-condition-file-write.md) | Race Condition File Write | Hard | 임시 파일 저장 및 유효성 검증 삭제 단계 사이의 레이턴시(경쟁 상태)를 틈타 악성 스크립트 실행 |
| **36** | [scenario-36-regex-dos-redos.md](file:///home/kisec/src/webctf/scenario-36-regex-dos-redos.md) | ReDoS (Regex DoS) | Medium | 백트래킹(Backtracking) 연산을 폭증시키는 정규표현식 구조에 악성 문자열을 대입해 웹 거부 |
| **37** | [scenario-37-unicode-normalization-bypass.md](file:///home/kisec/src/webctf/scenario-37-unicode-normalization-bypass.md) | Unicode Normalization Bypass | Hard | 유니코드 정규화(NFKC 등) 필터 적용 특성을 노려 특정 보안 블랙리스트 단어를 우회 입력 |
| **38** | [scenario-38-sql-injection-in-limit-clause.md](file:///home/kisec/src/webctf/scenario-38-sql-injection-in-limit-clause.md) | LIMIT Clause SQLi | Medium | 일반 방법으로 우회가 힘든 `LIMIT [OFFSET], [COUNT]` 구문 내에 PROCEDURE ANALYSE 등 인젝션 |
| **39** | [scenario-39-http-parameter-pollution.md](file:///home/kisec/src/webctf/scenario-39-http-parameter-pollution.md) | HTTP Parameter Pollution | Medium | 필터와 컨트롤러 도메인 간의 다중 수신 파라미터 조작을 통해 민감 비즈니스 검증 우회 |
| **40** | [scenario-40-cors-null-origin-abuse.md](file:///home/kisec/src/webctf/scenario-40-cors-null-origin-abuse.md) | CORS Null Origin Abuse | Medium | CORS 정책 중 `Access-Control-Allow-Origin: null` 설정을 `<iframe>` 샌드박스로 악용해 권한 탈취 |
| **41** | [scenario-41-jwe-weak-key-decryption.md](file:///home/kisec/src/webctf/scenario-41-jwe-weak-key-decryption.md) | JWE Weak Key Decryption | Hard | 취약한 대칭키 알고리즘 기반 JWE 암호문을 사전 공격 크래킹을 가해 원문 복호화 처리 |
| **42** | [scenario-42-prototype-pollution-template-rce.md](file:///home/kisec/src/webctf/scenario-42-prototype-pollution-template-rce.md) | Prototype Pollution to SSTI | Hard | 객체 프로토타입 오염 취약점을 연쇄 체이닝해 정적 템플릿 엔진 로직을 RCE 수준으로 탈취 |
| **43** | [scenario-43-open-redirect-to-xss-javascript-scheme.md](file:///home/kisec/src/webctf/scenario-43-open-redirect-to-xss-javascript-scheme.md) | Open Redirect to XSS | Medium | 오픈 리디렉션 주소 인자 검증 필터를 깨고 `javascript:` 스키마를 유도 주입하여 XSS 유발 |
| **44** | [scenario-44-git-submodule-rce.md](file:///home/kisec/src/webctf/scenario-44-git-submodule-rce.md) | Git Submodule RCE | Hard | 웹 빌더 서비스 등에서 `.gitmodules` 파일 구성을 무단 위조 주입하여 저장소 패치 시 RCE 유발 |
| **45** | [scenario-45-graphql-query-depth-dos.md](file:///home/kisec/src/webctf/scenario-45-graphql-query-depth-dos.md) | GraphQL Query Depth DoS | Medium | 중첩 구조 질의를 연쇄 조합하는 다차원 GraphQL 쿼리를 전송해 서버 리소스를 마비시키는 DoS |
| **46** | [scenario-46-yaml-deserialization-unsafe-load.md](file:///home/kisec/src/webctf/scenario-46-yaml-deserialization-unsafe-load.md) | PyYAML Unsafe Load RCE | Medium | PyYAML 모듈의 `unsafe_load` 실행 시 임의의 파이썬 객체 생성자를 주입하여 시스템 제어 |
| **47** | [scenario-47-blind-xss-via-out-of-band-exfiltration.md](file:///home/kisec/src/webctf/scenario-47-blind-xss-via-out-of-band-exfiltration.md) | Blind XSS OOB | Hard | 출력 영역을 볼 수 없는 백오피스 관리자 페이지에 XSS를 유인하고 OOB 채널로 기밀 반환 |
| **48** | [scenario-48-server-side-request-forgery-via-file-upload-svg.md](file:///home/kisec/src/webctf/scenario-48-server-side-request-forgery-via-file-upload-svg.md) | SVG File Upload SSRF | Medium | SVG 이미지 업로드 시 XML 구조 내 `xlink:href` 또는 파서 오설정을 악용하여 내부망 SSRF |
| **49** | [scenario-49-host-header-injection-password-reset.md](file:///home/kisec/src/webctf/scenario-49-host-header-injection-password-reset.md) | Host Header Injection | Medium | 비밀번호 재설정 이메일 전송 시 Host 헤더 값을 변조해 공격자 서버로 링크 접속을 유도 |
| **50** | [scenario-50-sql-injection-in-jsonb-postgresql.md](file:///home/kisec/src/webctf/scenario-50-sql-injection-in-jsonb-postgresql.md) | PostgreSQL JSONB SQLi | Hard | PostgreSQL의 특수 JSONB 연산자(예: `->>`, `#>`) 질의 구성부에서 발생하는 SQL 인젝션 |
| **51** | [scenario-51-jwt-kid-path-traversal.md](file:///home/kisec/src/webctf/scenario-51-jwt-kid-path-traversal.md) | JWT kid Path Traversal | Medium | JWT `kid` 헤더 값을 `../../../../dev/null`로 조작해 빈 비밀키 파일로 서명을 검증 우회 |
| **52** | [scenario-52-cross-site-websocket-hijacking.md](file:///home/kisec/src/webctf/scenario-52-cross-site-websocket-hijacking.md) | CSWSH (WebScoket Hijack) | Hard | WebSocket 핸드셰이크 프로토콜 연동 시 Origin 오설정을 악용해 피해자의 실시간 소켓 탈취 |
| **53** | [scenario-53-graphql-field-suggestion-abuse.md](file:///home/kisec/src/webctf/scenario-53-graphql-field-suggestion-abuse.md) | GraphQL Field Suggestion | Medium | 잘못된 입력 시 GraphQL 도구가 힌트로 반환하는 필드 자동 제안 정보를 수집해 자산 유출 |
| **54** | [scenario-54-ldap-injection-auth-bypass.md](file:///home/kisec/src/webctf/scenario-54-ldap-injection-auth-bypass.md) | LDAP Injection Auth Bypass | Medium | LDAP 디렉터리 인증 질의 조립 과정에 와일드카드(`*`) 제어를 유도하여 계정 패스워드 우회 |
| **55** | [scenario-55-php-magic-hash-type-juggling.md](file:///home/kisec/src/webctf/scenario-55-php-magic-hash-type-juggling.md) | PHP Type Juggling (Magic Hash) | Medium | PHP 느슨한 비교(`==`) 환경에서 해시 결과가 `0e`로 시작하는 매직 해시 연산 비교 우회 |
| **56** | [scenario-56-reflected-file-download-jsonp.md](file:///home/kisec/src/webctf/scenario-56-reflected-file-download-jsonp.md) | Reflected File Download (RFD) | Hard | JSONP 콜백 인풋 필터링 미비점을 노려 임의 파일 다운로드를 트리거하여 PC 명령어 실행 유도 |
| **57** | [scenario-57-client-side-prototype-pollution-dom-xss.md](file:///home/kisec/src/webctf/scenario-57-client-side-prototype-pollution-dom-xss.md) | Client-side Prototype DOM XSS | Hard | 프론트엔드 URL 파싱 로직에서 발생하는 프로토타입 오염을 이용해 타깃 위젯 설정 변조 후 XSS |
| **58** | [scenario-58-cors-origin-regex-bypass.md](file:///home/kisec/src/webctf/scenario-58-cors-origin-regex-bypass.md) | CORS Origin Regex Bypass | Medium | CORS 화이트리스트 검사 정규식 오설정(예: 탈출 안 된 `.`)을 노려 유사 도메인으로 정보 탈취 |
| **59** | [scenario-59-http-response-splitting-cache-poisoning.md](file:///home/kisec/src/webctf/scenario-59-http-response-splitting-cache-poisoning.md) | HTTP Response Splitting | Hard | 응답 헤더 내 CR-LF 개행 주입 취약점과 연계하여 중간 웹 캐시 장비의 정적 자산을 포이즈닝 |
| **60** | [scenario-60-mssql-stacked-queries-xp-cmdshell.md](file:///home/kisec/src/webctf/scenario-60-mssql-stacked-queries-xp-cmdshell.md) | MSSQL Stacked Query RCE | Hard | MSSQL 다중 쿼리 실행(`;`) 구조에 편입하여 `xp_cmdshell` 프로시저 활성화 후 시스템 탈취 |
| **61** | [scenario-61-web-cache-deception.md](file:///home/kisec/src/webctf/scenario-61-web-cache-deception.md) | Web Cache Deception (WCD) | Hard | 유저 개인 정보 페이지 주소 뒤에 가짜 정적 파일 경로를 붙여 중간 캐시 장비에 유출 정보 적재 |
| **62** | [scenario-62-jwt-jku-header-injection.md](file:///home/kisec/src/webctf/scenario-62-jwt-jku-header-injection.md) | JWT jku Header Injection | Medium | `jku` 헤더의 JWK 키 집합 주소를 공격자가 제어하는 외부 경로로 우회 설정해 서명을 우회 |
| **63** | [scenario-63-oauth-state-parameter-bypass.md](file:///home/kisec/src/webctf/scenario-63-oauth-state-parameter-bypass.md) | OAuth State CSRF Bypass | Medium | OAuth 인증 링크 생성 시 난수 `state` 매개변수 검증 처리를 생략하여 계정 연동 위조 유도 |
| **64** | [scenario-64-ssrf-url-parsing-discrepancy.md](file:///home/kisec/src/webctf/scenario-64-ssrf-url-parsing-discrepancy.md) | URL Parser Discrepancy SSRF | Hard | 자바스크립트 및 자바 등 다중 서버 환경 간의 URL 파서 규격 차이를 활용한 내부망 SSRF 우회 |
| **65** | [scenario-65-java-fastjson-deserialization-rce.md](file:///home/kisec/src/webctf/scenario-65-java-fastjson-deserialization-rce.md) | Java Fastjson Deserialization | Hard | Fastjson 파싱 도중 `@type` 지시자를 통해 임의의 자바 클래스(TemplatesImpl 등) RCE 가동 |
| **66** | [scenario-66-business-logic-coupon-race-condition.md](file:///home/kisec/src/webctf/scenario-66-business-logic-coupon-race-condition.md) | Business Logic Race Condition | Medium | 장바구니 쿠폰 적용 및 결제 시 중복 비동기 요청을 연달아 발생시켜 할인을 누적 적용 우회 |
| **67** | [scenario-67-ssrf-via-ntlm-relay-attack.md](file:///home/kisec/src/webctf/scenario-67-ssrf-via-ntlm-relay-attack.md) | SSRF NTLM Relay Attack | Hard | 내부 SSRF를 통해 SMB/HTTP 연결을 유발하여 AD망 환경의 NTLM 해시 정보를 강제 유출 및 전달 |
| **68** | [scenario-68-http2-request-smuggling.md](file:///home/kisec/src/webctf/scenario-68-http2-request-smuggling.md) | HTTP/2 Request Smuggling | Hard | HTTP/2 환경의 헤더 처리와 내부 백엔드 HTTP/1.1 프록시 간의 매핑 오류를 찌른 요청 스머글링 |
| **69** | [scenario-69-insecure-http-methods-abuse.md](file:///home/kisec/src/webctf/scenario-69-insecure-http-methods-abuse.md) | Insecure HTTP Methods | Medium | 웹 서버 설정 미비로 허용된 `PUT`, `DELETE` 메소드를 사용해 웹셸을 쓰고 자산을 무단 삭제 |
| **70** | [scenario-70-parameter-smuggling-delimiter-discrepancy.md](file:///home/kisec/src/webctf/scenario-70-parameter-smuggling-delimiter-discrepancy.md) | Parameter Smuggling | Hard | 파라미터 구분자(`,` 또는 `;` 또는 `&`) 해석 격차를 찔러 내부 API 매개변수를 교란 |
| **71** | [scenario-71-apache-filename-parsing-rce.md](file:///home/kisec/src/webctf/scenario-71-apache-filename-parsing-rce.md) | Apache Filename Parsing RCE | Hard | 아파치 모듈 파싱 오류를 악용하여 `.php.jpeg` 형태로 업로드된 파일을 php 코드로 실행 유도 |
| **72** | [scenario-72-json-hijacking-prototype-override.md](file:///home/kisec/src/webctf/scenario-72-json-hijacking-prototype-override.md) | JSON Hijacking | Hard | JSON 데이터가 포함된 스크립트를 로드할 때 Array 생성자 프로토타입을 덮어씌워 기밀 탈취 |
| **73** | [scenario-73-host-header-routing-ssrf.md](file:///home/kisec/src/webctf/scenario-73-host-header-routing-ssrf.md) | Host Header Routing SSRF | Hard | 역방향 프록시의 Host 헤더 기반 가상 호스트 매핑 속성을 속여 내부 인프라망 접속(SSRF) 유도 |
| **74** | [scenario-74-java-velocity-ssti-reflection.md](file:///home/kisec/src/webctf/scenario-74-java-velocity-ssti-reflection.md) | Velocity SSTI Reflection RCE | Hard | Java Velocity 템플릿 환경에서 Class 도구를 활용하여 샌드박스를 우회하고 자바 리플렉션 RCE |
| **75** | [scenario-75-cookie-poisoning-lfi.md](file:///home/kisec/src/webctf/scenario-75-cookie-poisoning-lfi.md) | Cookie Poisoning LFI | Medium | 세션 쿠키 값에 담긴 템플릿 경로 지시자를 변조 주입하여 임의의 내부 php 파일을 렌더링 |
| **76** | [scenario-76-graphql-introspection-comment-bypass.md](file:///home/kisec/src/webctf/scenario-76-graphql-introspection-comment-bypass.md) | GraphQL Introspection Bypass | Medium | 쿼리 내 특수 주석 문법이나 별도 키워드 배치를 우회 가동하여 스키마 노출 방지 대책을 돌파 |
| **77** | [scenario-77-django-orm-extra-sqli.md](file:///home/kisec/src/webctf/scenario-77-django-orm-extra-sqli.md) | Django ORM extra() SQLi | Hard | Django ORM의 위험 지점인 `.extra(where=[...])`에 주입되는 원시 SQL 주입 취약점 |
| **78** | [scenario-78-webdav-propfind-xml-xxe.md](file:///home/kisec/src/webctf/scenario-78-webdav-propfind-xml-xxe.md) | WebDAV PROPFIND XXE | Medium | WebDAV 연동을 위한 XML 구조 파싱 모듈 내부의 외부 엔티티 취약점을 노려 파일 읽기 |
| **79** | [scenario-79-ruby-on-rails-unsafe-json-deserialization-rce.md](file:///home/kisec/src/webctf/scenario-79-ruby-on-rails-unsafe-json-deserialization-rce.md) | RoR Unsafe Deserialization | Hard | Ruby on Rails 구버전 액티브 서포트 환경 하의 특정 JSON 가공 시 가젯 체인을 통한 RCE |
| **80** | [scenario-80-idor-bypass-via-parameter-pollution.md](file:///home/kisec/src/webctf/scenario-80-idor-bypass-via-parameter-pollution.md) | HPP + IDOR Bypass | Medium | 개별 파라미터 소유권 정합성 검사를 쿼리 스트링 HPP 다중 인자 주입으로 우회해 타인 권한 강탈 |
| **81** | [scenario-81-reflected-xss-basic.md](file:///home/kisec/src/webctf/scenario-81-reflected-xss-basic.md) | Reflected XSS Basic | Easy | HTML 필터링이 누락된 검색어 파라미터를 그대로 반사시켜 자바스크립트를 임의 실행함 |
| **82** | [scenario-82-sql-injection-basic-authentication-bypass.md](file:///home/kisec/src/webctf/scenario-82-sql-injection-basic-authentication-bypass.md) | SQLi Auth Bypass Basic | Easy | 문자열 연결로 로그인 쿼리를 동적 조립할 때 `' OR '1'='1`로 조건부 인증 검사를 통과 우회 |
| **83** | [scenario-83-path-traversal-basic-file-read.md](file:///home/kisec/src/webctf/scenario-83-path-traversal-basic-file-read.md) | Path Traversal Basic | Easy | 경로 횡단 제어 문자(`../`) 필터링 부재로 웹 폴더를 탈출해 내부 민감 정보(/etc/passwd) 유출 |
| **84** | [scenario-84-insecure-direct-object-reference-basic.md](file:///home/kisec/src/webctf/scenario-84-insecure-direct-object-reference-basic.md) | IDOR Basic | Easy | 권한 소유주 대조 없이 URL의 `user_id` 정수 기본키를 바꿔치기하여 타인의 비공개 메모 열람 |
| **85** | [scenario-85-sensitive-data-exposure-in-html-comments.md](file:///home/kisec/src/webctf/scenario-85-sensitive-data-exposure-in-html-comments.md) | HTML Comments Leak | Easy | 정적 소스코드 보기(F12) 중 개발 디버그용으로 남겨진 임시 관리자 계정 주석 정보를 획득 |
| **86** | [scenario-86-broken-object-level-authorization-password-reset.md](file:///home/kisec/src/webctf/scenario-86-broken-object-level-authorization-password-reset.md) | BOLA Password Reset | Easy | 패스워드 변경 API POST 바디 내의 `username` 값을 조작해 타인 계정 비밀번호 강제 갱신 |
| **87** | [scenario-87-command-injection-basic.md](file:///home/kisec/src/webctf/scenario-87-command-injection-basic.md) | OS Command Injection Basic | Easy | 핑(Ping) 도구에서 쉘 연산자 기호 `;`를 병합해 웹 서버 로컬 권한의 OS 명령어 연쇄 가동 |
| **88** | [scenario-88-broken-brute-force-protection.md](file:///home/kisec/src/webctf/scenario-88-broken-brute-force-protection.md) | Brute Force Protection Lack | Easy | 단시간 다수 로그인 실패 IP 차단 및 임시 잠금이 없어 무차별 대입 자동 공격으로 어드민 강탈 |
| **89** | [scenario-89-csrf-basic-state-changing.md](file:///home/kisec/src/webctf/scenario-89-csrf-basic-state-changing.md) | CSRF Basic | Easy | 보안 인증 토큰 검사 없이 타 사이트 유도로 쿠키 인증 정보를 자동 전송시켜 프로필 정보 변조 |
| **90** | [scenario-90-directory-listing-leak.md](file:///home/kisec/src/webctf/scenario-90-directory-listing-leak.md) | Directory Listing Exposure | Easy | 웹 서버 인덱싱 설정 미비로 `/backups/` 경로의 비공개 DB 백업 SQL 및 소스코드 트리 노출 |
| **91** | [scenario-91-weak-session-id-prediction.md](file:///home/kisec/src/webctf/scenario-91-weak-session-id-prediction.md) | Weak Session ID Prediction | Easy | 규칙적인 알고리즘(예: `md5(username)`)에 기반한 세션 쿠키를 역계산 및 변조해 계정 도용 |
| **92** | [scenario-92-insecure-cookie-flags-sensitive-data.md](file:///home/kisec/src/webctf/scenario-92-insecure-cookie-flags-sensitive-data.md) | Insecure Cookie Flags | Easy | 쿠키 속성 내 `HttpOnly` / `Secure` 플래그 부재로 XSS 발생 시 클라이언트 스크립트에 세션 노출 |
| **93** | [scenario-93-http-parameter-pollution-basic.md](file:///home/kisec/src/webctf/scenario-93-http-parameter-pollution-basic.md) | HTTP Parameter Pollution Basic | Easy | 다중 동명 매개변수 중복 입력 시 뒤의 변수를 최종 채택하는 백엔드 해석 격차 필터 우회 |
| **94** | [scenario-94-server-side-template-injection-easy.md](file:///home/kisec/src/webctf/scenario-94-server-side-template-injection-easy.md) | SSTI Basic | Easy | 닉네임 렌더링 시 템플릿 코드와 데이터를 직접 문자열 덧셈으로 빌드하여 `{{config}}` 값 유출 |
| **95** | [scenario-95-client-side-validation-bypass.md](file:///home/kisec/src/webctf/scenario-95-client-side-validation-bypass.md) | Client-Side Validation Bypass | Easy | 서버 측 2차 검증을 완전히 생략하고 브라우저 자바스크립트에 단독 통제를 맡겨 프록시로 값 변조 |
| **96** | [scenario-96-weak-cryptography-md5-hashing.md](file:///home/kisec/src/webctf/scenario-96-weak-cryptography-md5-hashing.md) | Weak Cryptography | Easy | 무솔트(No-Salt) MD5로 단순 해싱되어 보관된 비밀번호를 온라인 레인보우 테이블로 신속 해독 |
| **97** | [scenario-97-information-disclosure-phpinfo.md](file:///home/kisec/src/webctf/scenario-97-information-disclosure-phpinfo.md) | phpinfo Information Disclosure | Easy | 환경 검사용으로 배치된 `info.php`가 잔존하여 OS 상태, 경로 정보 및 환경 변수 플래그 노출 |
| **98** | [scenario-98-stored-xss-basic.md](file:///home/kisec/src/webctf/scenario-98-stored-xss-basic.md) | Stored XSS Basic | Easy | 방명록 본문 내용에 스크립트를 삽입 적재시켜 정기 점검 봇의 세션 쿠키를 지속적으로 갈취 |
| **99** | [scenario-99-http-header-injection-basic.md](file:///home/kisec/src/webctf/scenario-99-http-header-injection-basic.md) | HTTP Header SQLi Basic | Easy | 로깅 목적의 INSERT 구문 내에 결합되는 User-Agent 값을 변조하여 에러 기반 SQLi 유도 |
| **100** | [scenario-100-excessive-data-exposure-api-response.md](file:///home/kisec/src/webctf/scenario-100-excessive-data-exposure-api-response.md) | Excessive Data Exposure | Easy | 화면에는 회원 이름만 그리지만 API 응답 JSON 원문 내에 비공개 flag 등 민감 변수 노출 |

---

## 3. 학습 및 검증 가이드
각 시나리오는 다음과 같은 양식으로 구조화되어 있어 단계적인 실습에 최적화되어 있습니다:
1. **개요 및 스토리**: 현실적인 모의 침투 상황을 가정한 문제의 비즈니스 배경 설명.
2. **문제 설계 및 구조**: 어떤 컴포넌트들로 이루어져 있고 취약점 트리거 지점이 어디인지 정의.
3. **공격 면**: 공격을 보낼 구체적인 타겟 엔드포인트와 변수명 요약 테이블 제공.
4. **상세 풀이 흐름**: CTF 분석가가 실제로 단계를 밟아 플래그를 취득할 수 있는 구체적인 워크플로우 기술.
5. **취약점 유발 백엔드 코드**: 취약점을 초래하는 원시 백엔드 소스코드 스니펫(PHP, Python, JS, XML 등).
6. **방어 및 완화 기법**: 비즈니스 운영 환경에서 적용해야 하는 확실하고 정밀한 패치 기법 안내.
