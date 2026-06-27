---
title: Who are you? — picoCTF 2021 Web Exploitation writeup
created: 2026-06-24
updated: 2026-06-24
type: query
tags: [ctf, picoctf, picoctf2021, web-exploitation, writeup]
sources: [https://raw.githubusercontent.com/HHousen/PicoCTF-2021/master/Web%20Exploitation/Who%20are%20you%3F/README.md, https://raw.githubusercontent.com/vivian-dai/PicoCTF2021-Writeup/main/Web%20Exploitation/Who%20are%20you/README.md]
confidence: medium
---

# Who are you? — picoCTF 2021 Web Exploitation writeup

## 참고 URL
- [공개 writeup / 원문](https://raw.githubusercontent.com/HHousen/PicoCTF-2021/master/Web%20Exploitation/Who%20are%20you%3F/README.md)
- [대체 참고 자료](https://raw.githubusercontent.com/vivian-dai/PicoCTF2021-Writeup/main/Web%20Exploitation/Who%20are%20you/README.md)

## 핵심 요약
Let me in. Let me iiiiiiinnnnnnnnnnnnnnnnnnnn <http://mercury.picoctf.net:38322/>

## 풀이 메모
1. Resources: HTTP RFC / MDN HTTP Headers / Language Code Table / Sweden IP Address Ranged
2. curl http://mercury.picoctf.net:38322/ | grep "<h3.*>.*<\/h3>" --> Only people who use the official PicoBrowser are allowed on this site!
3. curl --user-agent "picobrowser" http://mercury.picoctf.net:38322/ | grep "<h3.*>.*<\/h3>" --> I don&#39;t trust users visiting from another site.
4. curl --user-agent "picobrowser" --referer "http://mercury.picoctf.net:38322/" http://mercury.picoctf.net:38322/ | grep "<h3.*>.*<\/h3>" --> Sorry, this site only worked in 2018.

## 같이 보면 좋은 페이지
- [[picoctf-2021-web-exploitation-survey]]
- [[picoctf-2021-web-exploitation-family-hub]]
- [[picoctf-2021-topic-map]]
