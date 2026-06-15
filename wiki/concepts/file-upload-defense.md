---
title: File Upload — 방어
created: 2026-06-12
updated: 2026-06-13
type: concept
tags: [security, glossary, web, file-upload, unrestricted-upload, webshell, malware, owasp, mime-type, magic-bytes]
sources: [https://ko.wikipedia.org/wiki/파일_업로드_취약점, https://ko.wikipedia.org/wiki/웹_애플리케이션_보안]
confidence: high
---
> [[file-upload]]의 후반부입니다.

## Step 3: 전문 용어 설명 (위키백과/OWASP/PortSwigger 기반)
### 언어/프레임워크별 안전한 파일 업로드 구현

| 언어/프레임워크 | 핵심 라이브러리/설정 |
|----------------|---------------------|
| **Python (Flask/Django/FastAPI)** | `werkzeug.utils.secure_filename`, `python-magic`/`filetype`, `PIL/Pillow` 리사이즈, `werkzeug.FileStorage` |
| **Node.js (Express)** | `multer` + `file-type`/`magic-bytes`, `sharp` 리사이즈, `multer.diskStorage` 커스텀 |
| **Java (Spring Boot)** | `MultipartFile`, `Apache Tika`/`Apache Commons IO` MIME 감지, `ImageIO`/`Thumbnailator` 리사이즈 |
| **PHP (Laravel/Symfony)** | `$request->file()->getMimeType()`, `getimagesize()`, `finfo_file()`, `Intervention Image` 리사이즈 |
| **Go** | `http.DetectContentType`, `mime-type` 패키지, `imaging` 리사이즈, `multipart.FormFile` |
| **.NET (ASP.NET Core)** | `IFormFile`, `FileExtensionContentTypeProvider`, `ImageSharp` 리사이즈, `MagicNumber` 검증 |

### 파일 업로드 취약점 테스트 체크리스트

| 테스트 항목 | 확인 사항 |
|------------|-----------|
| **확장자 우회** | `.php.jpg`, `.php.png`, `.PhP`, `.pHp`, `.php%00.jpg`, `.php.xxx` |
| **MIME 위장** | `Content-Type: image/jpeg`로 PHP/스크립트 전송 |
| **매직 바이트** | JPEG 헤더(`FF D8 FF`) + PHP 페이로드 결합 파일 |
| **이중 확장자** | `shell.php.jpg`, `shell.php.xxx` |
| **NULL 바이트** | `shell.php%00.jpg` (구버전 환경) |
| **경로 탐색** | `../../../var/www/shell.php` 파일명 |
| **대용량/DoS** | 100MB+ 파일, 다중 동시 업로드 |
| **SVG/XSS** | `<svg onload=alert(1)>` SVG 업로드 |
| **압축 파일** | ZIP 내 웹쉘 → 서버 압축 해제 시 실행 |
| **병렬 업로드** | 동시 다중 파일로 WAF/속도 제한 우회 |

### 주요 파일 업로드 사고 사례

| 사고 | 연도 | 공격 벡터 | 피해 |
|------|------|-----------|------|
| **Equifax** | 2017 | Struts2 취약점(CVE-2017-5638) → 악성 파일 업로드 → RCE | 1.47억 명 개인정보 유출 |
| **WordPress 플러그인** | 다수 | `wp-admin/admin-ajax.php` 업로드 핸들러 우회 | 수만 사이트 웹쉘 감염 |
| **Joomla/WordPress/Drupal** | 지속적 | 플러그인/테마 업로드 기능 우회 | 다수 CMS 사이트 웹쉘 감염 |
| **Apache Struts2** | 2017 | CVE-2017-5638 (Content-Type 파싱) → OGNL 인젝션 → 파일 업로드/RCE | Equifax 등 다수 기업 피해 |

### 관련 표준 및 참고

| 표준/문서 | 내용 |
|----------|------|
| **OWASP Unrestricted File Upload** | 파일 업로드 공격/방어 종합 가이드 |
| **OWASP File Upload Cheat Sheet** | 안전한 파일 업로드 구현 체크리스트 |
| **CWE-434** | Unrestricted Upload of File with Dangerous Type |
| **CWE-436** | Interpretation Conflict (파일 타입 해석 차이) |

---


## 관련 위키 링크

- [[rce]] — RCE (파일 업로드 → 웹쉘 실행 → RCE 체인)
- [[path-traversal]] — Path Traversal (파일명/경로 조작으로 업로드 경로 벗어남)
- [[command-injection]] — Command Injection (업로드된 파일로 명령 실행)
- [[ssti]] — SSTI (템플릿 파일 업로드 → SSTI → RCE)
- [[real-world-breach-cases]] — 실제 침해 사례 (Equifax, WordPress 플러그인 등 사례)
- [[exploitation]] — 익스플로잇 (파일 업로드 → 웹쉘 → 포스트 익스플로잇)

---

## 참고 문헌

- 한국어 위키백과: [파일 업로드 취약점](https://ko.wikipedia.org/wiki/파일_업로드_취약점)
- OWASP: [Unrestricted File Upload](https://owasp.org/www-community/attacks/Unrestricted_File_Upload)
- PortSwigger: [File upload vulnerabilities](https://portswigger.net/web-security/file-upload)
- OWASP Cheat Sheet: [File Upload](https://cheatsheetseries.owasp.org/cheatsheets/File_Upload_Cheat_Sheet.html)
## 관련 위키 링크
- [[file-upload]] — 인덱스 페이지
- [[file-upload-core]] — 분할 페이지
- [[rce]]
