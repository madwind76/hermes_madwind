---
title: Super Serial — picoCTF 2021 Web Exploitation writeup
created: 2026-06-24
updated: 2026-06-24
type: query
tags: [ctf, picoctf, picoctf2021, web-exploitation, writeup]
sources: [https://raw.githubusercontent.com/HHousen/PicoCTF-2021/master/Web%20Exploitation/Super%20Serial/README.md]
confidence: medium
---

# Super Serial — picoCTF 2021 Web Exploitation writeup

## 참고 URL
- [공개 writeup / 원문](https://raw.githubusercontent.com/HHousen/PicoCTF-2021/master/Web%20Exploitation/Super%20Serial/README.md)

## 핵심 요약
Try to recover the flag stored on this website <http://mercury.picoctf.net:3449/>

## 풀이 메모
1. Going to robots.txt shows that admin.phps is disallowed. This indicates that the phps extension is enabled within the php configuration for this webserver. Files with the phps extension contain php code but instead of running when they are accessed, they return an HTML representation of the literal pho code.
2. We can access index.phps to find the following:
3. The above php code points us in the direction of authentication.php. Looking at authentication.phps shows the following:
4. The above php code points us in the direction of cookie.php. Looking at cookie.phps shows the following:

## 같이 보면 좋은 페이지
- [[picoctf-2021-web-exploitation-survey]]
- [[picoctf-2021-web-exploitation-family-hub]]
- [[picoctf-2021-topic-map]]
