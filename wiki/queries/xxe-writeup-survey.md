---
title: XXE writeup survey
created: 2026-06-19
updated: 2026-06-21
type: query
tags: [ctf, web, survey, writeup, xxe, xml, external-entity, file-read]
sources: [https://medium.com/@Kamal_S/picoctf-web-exploitation-soap-c68604ec3469, https://portswigger.net/web-security/xxe]
confidence: high
---

# XXE writeup survey

## 참고 URL
- [medium.com](https://medium.com/@Kamal_S/picoctf-web-exploitation-soap-c68604ec3469)
- [portswigger.net](https://portswigger.net/web-security/xxe)


## 1. 목적
XML External Entity injection을 이용한 CTF writeup을 비교합니다.

## 2. 비교 대상
| 문제 | 주된 primitive | 보조 primitive | 한 줄 요약 |
|---|---|---|---|
| SOAP (picoCTF 2023) | XXE file read | Burp proxy | SOAP/XML 요청을 Burp로 잡고 외부 엔티티를 삽입해 `/etc/passwd`를 읽습니다. |
| PortSwigger XXE lab (file read) | XXE basic entity | file exfiltration | `<!ENTITY xxe SYSTEM "file:///etc/passwd">`로 서버 파일을 읽습니다. |

## 3. 공통 관찰
1. XXE는 XML 파서가 외부 엔티티를 허용할 때 발생합니다.
2. `<!ENTITY xxe SYSTEM "file:///etc/passwd">` 또는 `php://filter`가 대표 payload입니다.
3. SOAP, REST API, XML-RPC 등 XML을 받는 모든 지점이 공격면입니다.

## 4. 관련 개념
- [[xxe]]
- [[xxe-core]]
- [[web-ctf-writeup-parser-template]]
- [[web-ctf-writeup-family-hub]]
- [[soap-final-writeup]]

## 5. 다음 읽을 거리
- [[soap-final-writeup]]
