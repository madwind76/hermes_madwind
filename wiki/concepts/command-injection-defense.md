---
title: Command Injection — 방어
created: 2026-06-12
updated: 2026-06-13
type: concept
tags: [security, glossary, web, command-injection, os-command-injection, shell-injection, rce, owasp, input-validation]
sources: [https://ko.wikipedia.org/wiki/명령어_주입_공격, https://ko.wikipedia.org/wiki/OWASP]
confidence: high
---
> [[command-injection]]의 후반부입니다.

## Step 3: 전문 용어 설명 (위키백과/OWASP/PortSwigger 기반)
### Command Injection 방어 기법

| 방어 계층 | 기법 | 구현 예시 | 효과/비고 |
|----------|------|-----------|-----------|
| **아키텍처 (최우선)** | **OS 명령어 직접 실행 회피** | 내부 라이브러리/API 사용 (`subprocess` 대신 `shutil`, `os`, `pathlib`, `requests` 등) | **가장 확실** — 쉘 완전 우회 |
| | **빌트인 라이브러리 사용** | Python: `shutil`, `os`, `pathlib`, `ipaddress`, `socket` / Go: 표준 라이브러리 | 쉘 메타문자 완전 회피 |
| **입력 검증 (필수)** | **화이트리스트 검증** | 허용된 값만 허용 (IP: CIDR 검증, 도메인: 정규식, 알파벳/숫자만) | **핵심 방어** — 블랙리스트 금지 |
| | **엄격한 타입/형식 검증** | IP: `ipaddress.IPv4Address()`, 도메인: RFC 정규식, 이메일: RFC 5322 | 타입 안전성 확보 |
| | **허용 문자만 허용** | 파일명: `[a-zA-Z0-9_-.]+`만 허용 | 메타문자 원천 차단 |
| **안전한 실행 (필수 시)** | **쉘 미사용 실행** | Python: `subprocess.run(cmd_list, shell=False, check=True)` | **`shell=False` 필수** — 인자 리스트로 전달 |
| | **인자 분리 전달** | `subprocess.run(["ping", "-c", "4", ip])` | 인자 인젝션 원천 차단 |
| | **타임아웃/제한** | `timeout=5`, 리소스 제한 (`ulimit`, `resource.setrlimit`) | DoS/무한루프 방지 |
| **이스케이프 (보조)** | **쉘 이스케이프** | Python: `shlex.quote()`, Go: `shellescape.Quote()`, PHP: `escapeshellarg()` | **최후 수단** — 화이트리스트 불가능할 때만 |
| | **인자 이스케이프** | `escapeshellcmd()` 전체 명령, `escapeshellarg()` 각 인자 | PHP 환경에서 필수 |
| **모니터링/탐지** | **이상 명령어 탐지** | `execve` 시스템콜 모니터링 (Falco, Tetragon, eBPF) | 런타임 탐지 |
| | **이상 프로세스 트리 탐지** | 웹서버 자식 프로세스로 `bash`, `sh`, `nc`, `wget`, `curl` 실행 감지 | EDR/팔코 연계 |

### 언어/프레임워크별 안전한 명령 실행

| 언어 | 안전한 방식 | 위험한 방식 (금지) |
|------|-------------|---------------------|
| **Python** | `subprocess.run(["cmd", "arg1", "arg2"], shell=False, check=True, timeout=5)` | `os.system()`, `subprocess.run(cmd, shell=True)`, `os.popen()`, `commands.getstatusoutput()` |
| **Node.js** | `spawn("cmd", ["arg1", "arg2"])` 또는 `execFile("cmd", ["arg1"])` | `exec()`, `execSync()`, `child_process.exec()` (shell 내장) |
| **Java** | `ProcessBuilder(cmdList).start()` 또는 `Runtime.getRuntime().exec(cmdArray)` | `Runtime.getRuntime().exec(cmdString)` (단일 문자열) |
| **Go** | `exec.Command("cmd", "arg1", "arg2").Run()` | `exec.Command("sh", "-c", cmdString).Run()` |
| **PHP** | `proc_open()` with array args, `exec()` with `escapeshellarg()` | `exec()`, `shell_exec()`, `system()`, `passthru()`, `popen()` (단일 문자열) |
| **.NET** | `Process.Start(new ProcessStartInfo { FileName="cmd", Arguments="arg1 arg2", UseShellExecute=false })` | `Process.Start("cmd", "/c " + userInput)` |
| **Go** | `exec.Command("cmd", "arg1", "arg2").Run()` | `exec.Command("sh", "-c", userInput).Run()` |
| **Ruby** | `system("cmd", "arg1", "arg2")` (배열 형태) | `system("cmd " + userInput)`, `` `cmd #{userInput}` `` |

### Command Injection vs SQL Injection 비교

| 구분 | **Command Injection** | **SQL Injection** |
|------|----------------------|-------------------|
| **대상** | 운영체제 쉘 (OS 커널) | 데이터베이스 엔진 |
| **메타문자** | `;`, `&`, `|`, `$`, `` ` ``, `#`, `\n` | `'`, `"`, `;`, `--`, `/*`, `UNION` |
| **영향 범위** | 서버 전체 (파일, 프로세스, 네트워크, 커널) | 데이터베이스 (데이터, 스키마, 프로시저) |
| **최대 영향** | **서버 완전 장악 (RCE)** | 데이터 유출/변조/삭제, 인증 우회 |
| **방어 핵심** | 쉘 미사용, 화이트리스트, 인자 분리 | 파라미터화 쿼리, PreparedStatement |

### 주요 Command Injection 사고 사례

| 사고 | 연도 | 공격 벡터 | 피해 |
|------|------|-----------|------|
| **Shellshock (Bash)** | 2014 | 환경변수 파싱 버그 (`() { :; }; cmd`) | 전 세계 수억 대 서버 RCE 가능 |
| **Cisco IOS** | 2017 | SNMP 명령어 인젝션 | 네트워크 장비 완전 제어 |
| **D-Link 라우터** | 2019 | `ping` 명령어 인젝션 | 수백만 대 라우터 봇넷화 (Mirai 변종) |
| **WordPress 플러그인** | 다수 | `wp-admin` 내 이미지 처리, 백업 기능 | 수만 사이트 웹쉘 감염 |
| **Docker** | 2019 | `docker build` 중 `RUN` 명령 인젝션 | 컨테이너 탈출 → 호스트 침투 |

### 관련 표준 및 참고

| 표준/문서 | 내용 |
|----------|------|
| **OWASP Command Injection** | 명령어 주입 공격/방어 종합 가이드 |
| **OWASP Command Injection Cheat Sheet** | 방어 체크리스트 |
| **CWE-78** | Improper Neutralization of Special Elements used in an OS Command ('OS Command Injection') |
| **CWE-77** | Improper Neutralization of Special Elements used in a Command ('Command Injection') |
| **CAPEC-88** | OS Command Injection |

---


## 관련 위키 링크

- [[file-upload]] — File Upload (파일명/경로 인자로 명령 실행 인자 주입)
- [[path-traversal]] — Path Traversal (파일 경로 인자로 명령 실행 인자 주입)
- [[rce]] — RCE (Command Injection은 RCE의 가장 직접적인 경로)
- [[ssti]] — SSTI (템플릿 엔진에서 명령 실행 가능)
- [[real-world-breach-cases]] — 실제 침해 사례 (Shellshock, 라우터 봇넷 등 사례)
- [[exploitation]] — 익스플로잇 (Command Injection → 포스트 익스플로잇)

---

## 참고 문헌

- 한국어 위키백과: [명령어 주입](https://ko.wikipedia.org/wiki/명령어_주입)
- OWASP: [Command Injection](https://owasp.org/www-community/attacks/Command_Injection)
- PortSwigger: [OS command injection](https://portswigger.net/web-security/os-command-injection)
- OWASP Cheat Sheet: [Command Injection](https://cheatsheetseries.owasp.org/cheatsheets/OS_Command_Injection_Cheat_Sheet.html)
## 관련 위키 링크
- [[command-injection]] — 인덱스 페이지
- [[command-injection-core]] — 분할 페이지
- [[rce]]
