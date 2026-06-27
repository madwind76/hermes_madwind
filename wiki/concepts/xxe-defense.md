---
title: XXE — 방어
created: 2026-06-12
updated: 2026-06-21
type: concept
tags: [security, glossary, web, xxe, xml, external-entity, xpath, dos, file-read, ssrf, owasp]
sources: [https://ko.wikipedia.org/wiki/XML_외부_엔터티_공격, https://ko.wikipedia.org/wiki/OWASP]
confidence: high
---
> [[xxe]]의 후반부입니다.

## 참고 URL
- [ko.wikipedia.org](https://ko.wikipedia.org/wiki/XML_외부_엔터티_공격)
- [ko.wikipedia.org](https://ko.wikipedia.org/wiki/OWASP)

## Step 3: 전문 용어 설명 (위키백과/OWASP/PortSwigger 기반)
### XXE 방어 기법

| 방어 계층 | 기법 | 구현 예시 | 효과/비고 |
|----------|------|-----------|-----------|
| **파서 설정 (최우선)** | **외부 엔터티 완전 비활성화** | **Python (lxml)**: `etree.XMLParser(resolve_entities=False, no_network=True)`<br>**Java (DocumentBuilderFactory)**: `dbf.setFeature("http://apache.org/xml/features/disallow-doctype-decl", true)`<br>**Python (defusedxml)**: `defusedxml.lxml.fromstring(xml)`<br>**.NET (XmlReaderSettings)**: `settings.DtdProcessing = DtdProcessing.Prohibit`<br>**Go (xml.Decoder)**: `decoder.Strict = true; decoder.Entity = nil`<br>**PHP (libxml)**: `libxml_disable_entity_loader(true)` (deprecated) → `XMLParser` 옵션 사용 | **가장 확실/표준 방어** — DTD 자체를 금지하거나 외부 엔터티만 차단 |
| | **외부 엔티티만 차단 (DTD 허용)** | `setFeature("http://xml.org/sax/features/external-general-entities", false)`<br>`setFeature("http://xml.org/sax/features/external-parameter-entities", false)` | 레거시 DTD 필요 시 |
| | **XInclude 비활성화** | `setFeature("http://apache.org/xml/features/xinclude", false)` | XInclude 공격 방지 |
| **입력 검증** | **XML 스키마(XSD) 검증** | 허용된 요소/속성만 허용, 예상치 못한 DTD 거부 | 화이트리스트 방식 |
| | **파일 업로드 시 SVF 검증** | SVG 업로드 시 `librsvg` 등 안전한 라이브러리로 재처리/검증 | 이미지 XXE 방지 |
| **네트워크/시스템** | **아웃바운드 차단** | 서버에서 불필요한 아웃바운드 HTTP/파일 프로토콜 차단 | Blind XXE/OOB 차단 |
| | **파일 시스템 권한 최소화** | 앱 실행 유저가 `/etc/passwd`, `.ssh`, 소스코드 못 읽게 권한 설정 | 피해 최소화 (심층 방어) |
| **모니터링/탐지** | **XXE 시그니처 탐지** | `<!DOCTYPE`, `<!ENTITY`, `SYSTEM`, `PUBLIC`, `file://`, `http://` 패턴 로깅/차단 | WAF/로그 분석 |
| | **OAST 상호작용 탐지** | Burp Collaborator, interactsh, canarytokens 연동 → 외부 DTD 로드 감지 | Blind XXE 조기 탐지 |

### 언어/프레임워크별 안전한 XML 파싱 설정

| 언어/라이브러리 | 안전한 설정 코드 |
|----------------|------------------|
| **Python (lxml)** | `parser = etree.XMLParser(resolve_entities=False, no_network=True, huge_tree=False)` |
| **Python (defusedxml)** | `from defusedxml.lxml import fromstring; fromstring(xml)` (권장) |
| **Python (xml.etree)** | 기본적으로 외부 엔터티 미해결 (상대적 안전) — `defusedxml` 권장 |
| **Java (DocumentBuilderFactory)** | `dbf.setFeature("http://apache.org/xml/features/disallow-doctype-decl", true);`<br>`dbf.setXIncludeAware(false);`<br>`dbf.setExpandEntityReferences(false);` |
| **Java (SAXParserFactory)** | `spf.setFeature("http://xml.org/sax/features/external-general-entities", false);`<br>`spf.setFeature("http://xml.org/sax/features/external-parameter-entities", false);` |
| **.NET (XmlReader)** | `var settings = new XmlReaderSettings { DtdProcessing = DtdProcessing.Prohibit, XmlResolver = null };` |
| **.NET (XDocument)** | `XDocument.Load(xmlReader, LoadOptions.None)` (XmlReader 설정 상속) |
| **Go (encoding/xml)** | `decoder := xml.NewDecoder(bytes.NewReader(xml)); decoder.Strict = true; decoder.Entity = nil; decoder.AutoClose = xml.HTMLAutoClose` |
| **PHP (libxml/SimpleXML)** | `libxml_disable_entity_loader(true);` (PHP 8.0+ 기본값) + `simplexml_load_string($xml, 'SimpleXMLElement', LIBXML_NOENT \| LIBXML_DTDLOAD \| LIBXML_NONET)` → **NOENT 제거, NONET 추가** |
| **Node.js (libxmljs2/xmldom)** | `const dom = new DOMParser({errorHandler: {warning:()=>{}, error:()=>{}, fatalError:()=>{}}}).parseFromString(xml, 'text/xml');` + 외부 엔터티 비활성화 옵션 확인 |
| **Ruby (Nokogiri)** | `Nokogiri::XML(xml) { |config| config.strict.nonet.noent.noblanks }` (nonet: 네트워크 차단, noent: 엔터티 확장 안 함) |

### XXE 탐지 및 테스트

| 방법 | 도구/기법 |
|------|-----------|
| **자동 스캔** | OWASP ZAP (XXE 스캔), Burp Suite (XML 파라미터 스캔), Nuclei XXE 템플릿, Nikto |
| **수동 테스트** | Burp Suite "XML Entity Injection" 테스트, OAST 서버(interactsh, Burp Collaborator) 연동 |
| **코드 리뷰** | `DocumentBuilderFactory`, `XmlReader`, `simplexml_load_string`, `lxml.etree.parse` 등 XML 파싱 코드에서 외부 엔터티 비활성화 여부 확인 |
| **CI/CD 통합** | Semgrep/CodeQL XXE 룰, Nuclei XXE 템플릿, Trivy/Checkov 인프라 설정 검사 |
| **파일 업로드 테스트** | SVG, Office 문서(docx, xlsx - ZIP+XML), PDF, RSS/Atom 피드 등 XML 기반 포맷 업로드 테스트 |

### 주요 XXE 사고 사례

| 사고 | 연도 | 공격 벡터 | 피해 |
|------|------|-----------|------|
| **Facebook** | 2013 | 파일 업로드(SVG) XXE → 내부 파일 읽기 | 버그바운티 $10,000+ |
| **PayPal** | 2016 | XXE → 내부 파일/메타데이터 읽기 | 버그바운티 $15,000 |
| **Twitter** | 2014 | XML API XXE → 내부 서비스 접근 | 버그바운티 $10,080 |
| **VMware vCenter** | 2021 | CVE-2021-21972 (XXE → RCE) | 인증 없이 원격 코드 실행 |
| **SAP NetWeaver** | 2020 | CVE-2020-6207 (XXE) | 내부 파일 읽기, SSRF |

### XXE 관련 CWE/CVE

| 식별자 | 설명 |
|--------|------|
| **CWE-611** | Improper Restriction of XML External Entity Reference |
| **CWE-827** | Improper Control of Document Type Definition |
| **CAPEC-221** | XML External Entity (XXE) Injection |

---


## 관련 위키 링크

- [[ssrf]] — SSRF (XXE로 HTTP 외부 엔터티 호출 시 SSRF로 발전)
- [[rce]] — RCE (특정 파서/라이브러리에서 XXE → RCE 체인 가능, 예: VMware CVE-2021-21972)
- [[exploitation]] — 익스플로잇 (XXE는 파일 읽기/SSRF/DoS 등 다양한 익스플로잇 경로 제공)
- [[real-world-breach-cases]] — 실제 침해 사례 (Facebook, PayPal, VMware XXE 사례)
- [[exploitation]] — 익스플로잇 (Billion Laughs DoS 등)

---

## 참고 문헌

- 한국어 위키백과: [XML 외부 엔터티 주입](https://ko.wikipedia.org/wiki/XML_외부_엔터티_주입)
- OWASP: [XML External Entity (XXE) Injection](https://owasp.org/www-community/attacks/XML_External_Entity_(XXE)_Injection)
- PortSwigger: [XML External Entity (XXE) Injection](https://portswigger.net/web-security/xxe)
- OWASP Cheat Sheet: [XXE Prevention](https://cheatsheetseries.owasp.org/cheatsheets/XML_External_Entity_Prevention_Cheat_Sheet.html)
- "Billion Laughs Attack" 분석: [XML DoS 공격](https://en.wikipedia.org/wiki/Billion_laughs_attack)
## 관련 위키 링크
- [[xxe]] — 인덱스 페이지
- [[xxe-core]] — 분할 페이지
- [[rce]]
