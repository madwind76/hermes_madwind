---
title: Path Traversal — 방어
created: 2026-06-12
updated: 2026-06-13
type: concept
tags: [security, glossary, web, path-traversal, directory-traversal, lfi, rfi, file-inclusion, owasp]
sources: [https://ko.wikipedia.org/wiki/경로_순회_공격, https://ko.wikipedia.org/wiki/OWASP]
confidence: high
---
> [[path-traversal]]의 후반부입니다.

## Step 3: 전문 용어 설명 (위키백과/OWASP/PortSwigger 기반)
### Path Traversal 방어 기법

| 방어 계층 | 기법 | 구현 예시 | 효과/비고 |
|----------|------|-----------|-----------|
| **입력 검증 (1차)** | **경로 화이트리스트** | 허용된 파일명/패턴만 허용 (정규식: `^[a-zA-Z0-9_-]+\.(jpg|png|pdf)$`) | **가장 확실** — 예상치 못한 입력 원천 차단 |
| | **경로 정규화 (Canonicalization)** | `os.path.normpath()`, `os.path.realpath()`, `filepath.Clean()`, `System.IO.Path.GetFullPath()` | `../`, `./`, 심볼릭 링크, 중복 슬래시 제거 후 **기본 디렉토리 하위인지 검증** |
| | **기본 디렉토리 하위 강제** | `if not os.path.commonpath([base, target]) == base: raise Error` | **기본 경로 벗어나면 거부** — 가장 핵심 로직 |
| | **파일명/경로 길이 제한** | 최대 255자, 경로 깊이 제한 (예: 3단계 이하) | 과도한 `../` 체인 방지 |
| | **위험 문자/시퀀스 차단** | `../`, `..\`, `%2e%2e%2f`, `%00`, `..\`, `..;/` 등 블랙리스트 | **보조 수단** — 우회 가능성 있어 단독 사용 비권장 |
| **파일 시스템 (2차)** | **chroot/재일(Jail)** | 애플리케이션 루트 디렉토리에서 `chroot` 또는 컨테이너 격리 | OS 레벨 격리 — 탈출 시도 원천 차단 |
| | **파일 권한 최소화** | 웹 사용자(`www-data`)가 읽기만 필요한 파일만 읽기 권한, 쓰기 금지 | 피해 최소화 |
| | **심볼릭 링크 따라가기 방지** | `os.path.realpath()`로 심볼릭 링크 해석 후 검증 | 심볼릭 링크 우회 차단 |
| **애플리케이션 설계** | **파일 직접 접근 회피** | DB에 파일 메타데이터 저장, 실제 파일은 비공개 스토리지(S3, 별도 볼륨) 저장, 서명된 URL로 접근 | 경로 노출 원천 차단 |
| | **파일명 랜덤화/해시화** | 원본 파일명 저장 안 함 → UUID/해시로 저장, DB에 원본명 매핑 | 경로 조작/실행 방지 |
| **모니터링/탐지** | **경로 조작 시도 로깅/알림** | `../`, `..\`, `%2e%2e%2f` 등 패턴 접근 시 실시간 알림 | 조기 탐지, 자동 차단(SIEM/WAF 연계) |

### 언어/프레임워크별 안전한 경로 처리

| 언어/프레임워크 | 안전한 경로 처리 함수 |
|----------------|----------------------|
| **Python** | `os.path.normpath()`, `os.path.realpath()`, `pathlib.Path.resolve()`, `os.path.commonpath([base, target]) == base` |
| **Node.js** | `path.normalize()`, `path.resolve()`, `path.relative(base, target).startsWith('..')` 체크 |
| **Java** | `Paths.get(base).resolve(target).normalize().startsWith(Paths.get(base))`, `FilenameUtils.normalize()` |
| **Go** | `filepath.Clean()`, `filepath.Rel(base, target)`, `strings.HasPrefix(rel, "..")` 체크 |
| **PHP** | `realpath()`, `pathinfo()`, `strpos($path, '..') === false` 검증 |
| **.NET** | `Path.GetFullPath()`, `Path.GetRelativePath(base, target).StartsWith("..")` 체크 |
| **Ruby** | `Pathname.new(path).cleanpath.to_s`, `Pathname.new(base).join(target).cleanpath.to_s.start_with?(base)` |

### Path Traversal 테스트 체크리스트

| 테스트 항목 | 페이로드 예시 |
|------------|---------------|
| **기본 상위 이동** | `../`, `..\`, `..../`, `....//` |
| **URL 인코딩** | `%2e%2e%2f`, `%2e%2e%5c`, `%2e%2e/` |
| **이중 인코딩** | `%252e%252e%252f` |
| **NULL 바이트** | `../../../etc/passwd%00` |
| **유니코드** | `..%c0%af`, `..%c1%9c` |
| **윈도우 백슬래시** | `..\`, `..%5c`, `..%c1%1c` |
| **절대 경로** | `/etc/passwd`, `C:\Windows\system32\drivers\etc\hosts` |
| **심볼릭 링크** | 업로드 디렉토리에 `/etc` 심볼릭 링크 생성 후 접근 |
| **파일 쓰기** | `../../../var/www/html/shell.php` 업로드 |
| **파일 삭제** | `../../../var/www/html/index.php` 삭제 요청 |

### 주요 Path Traversal 사고 사례

| 사고 | 연도 | 공격 벡터 | 피해 |
|------|------|-----------|------|
| **Apache HTTP Server** | 2021 | CVE-2021-41773 (Path Traversal → RCE) | 2.4.49/2.4.50 버전, RCE 가능 |
| **Spring Framework** | 2022 | CVE-2022-22965 (Spring4Shell) — Path Traversal + SpEL → RCE | Spring Cloud Function, Data Flow 등 영향 |
| **VMware vCenter** | 2021 | CVE-2021-21972 (Path Traversal → RCE) | 인증 없이 RCE, vCenter Server 영향 |
| **Atlassian Confluence** | 2019 | CVE-2019-3396 (Widget Connector Path Traversal) | 서버 측 템플릿 주입 → RCE |
| **WordPress 플러그인** | 다수 | `../` 필터링 우회 → wp-config.php 읽기/쓰기 | 다수 사이트 해킹 |

### 관련 표준 및 참고

| 표준/문서 | 내용 |
|----------|------|
| **OWASP Path Traversal** | 경로 순회 공격/방어 종합 가이드 |
| **CWE-22** | Improper Limitation of a Pathname to a Restricted Directory ('Path Traversal') |
| **CWE-23** | Relative Path Traversal |
| **CWE-36** | Absolute Path Traversal |
| **CAPEC-126** | Path Traversal |

---


## 관련 위키 링크

- [[file-upload]] — File Upload (파일명/경로 조작으로 업로드 경로 벗어남 → 웹쉘 심기)
- [[command-injection]] — Command Injection (파일 경로 인자로 명령 실행 인자 주입)
- [[rce]] — RCE (Path Traversal → 웹쉘 쓰기/설정파일 변조 → RCE 체인)
- [[lfi-rfi]] — LFI/RFI (Path Traversal로 로컬/원격 파일 포함)
- [[real-world-breach-cases]] — 실제 침해 사례 (Apache, Spring4Shell, VMware 등 사례)
- [[exploitation]] — 익스플로잇 (Path Traversal → 파일 읽기/쓰기/실행 → 포스트 익스플로잇)

---

## 참고 문헌

- 한국어 위키백과: [디렉토리 순회](https://ko.wikipedia.org/wiki/디렉토리_순회)
- OWASP: [Path Traversal](https://owasp.org/www-community/attacks/Path_Traversal)
- PortSwigger: [File path traversal](https://portswigger.net/web-security/file-path-traversal)
- CWE-22: [Improper Limitation of a Pathname to a Restricted Directory](https://cwe.mitre.org/data/definitions/22.html)
## 관련 위키 링크
- [[path-traversal]] — 인덱스 페이지
- [[path-traversal-core]] — 분할 페이지
- [[rce]]
