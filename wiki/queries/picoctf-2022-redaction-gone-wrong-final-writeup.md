---
title: Redaction Gone Wrong — picoCTF 2022 forensics writeup
created: 2026-06-24
updated: 2026-06-24
type: query
tags: [ctf, picoctf, picoctf2022, forensics]
sources: [https://raw.githubusercontent.com/noamgariani11/picoCTF-2022-Writeup/main/Forensics/Redaction%20Gone%20Wrong/RedactionGoneWrong.md, https://github.com/noamgariani11/picoCTF-2022-Writeup/tree/main/Forensics/Redaction%20Gone%20Wrong/RedactionGoneWrong.md]
confidence: medium
---

# Redaction Gone Wrong — picoCTF 2022 forensics writeup

## 참고 URL
- [GitHub raw writeup](https://raw.githubusercontent.com/noamgariani11/picoCTF-2022-Writeup/main/Forensics/Redaction%20Gone%20Wrong/RedactionGoneWrong.md)
- [GitHub directory](https://github.com/noamgariani11/picoCTF-2022-Writeup/tree/main/Forensics/Redaction%20Gone%20Wrong/RedactionGoneWrong.md)

## 핵심 요약
Now you DON’T see me. This report has some critical data in it, some of which have

## 풀이 메모
1. I first used pdftotext (you can get with
2. This created Financial_Report_for_ABC_Labs.txt which when you cat the contents (cat Financial_Report_for_ABC_Labs.txt) then you see the flag.
3. If you pipe grep with pico then you will get the flag just on that line.

## 같이 보면 좋은 페이지
- [[picoctf-2022-forensics-survey]]
- [[picoctf-2022-forensics-family-hub]]
- [[picoctf-2022-topic-map]]
