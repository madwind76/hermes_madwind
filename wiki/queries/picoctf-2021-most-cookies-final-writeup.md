---
title: Most Cookies — picoCTF 2021 Web Exploitation writeup
created: 2026-06-24
updated: 2026-06-24
type: query
tags: [ctf, picoctf, picoctf2021, web-exploitation, writeup]
sources: [https://raw.githubusercontent.com/HHousen/PicoCTF-2021/master/Web%20Exploitation/Most%20Cookies/README.md, https://raw.githubusercontent.com/vivian-dai/PicoCTF2021-Writeup/main/Web%20Exploitation/Most%20Cookies/README.md]
confidence: medium
---

# Most Cookies — picoCTF 2021 Web Exploitation writeup

## 참고 URL
- [공개 writeup / 원문](https://raw.githubusercontent.com/HHousen/PicoCTF-2021/master/Web%20Exploitation/Most%20Cookies/README.md)
- [대체 참고 자료](https://raw.githubusercontent.com/vivian-dai/PicoCTF2021-Writeup/main/Web%20Exploitation/Most%20Cookies/README.md)

## 핵심 요약
Alright, enough of using my own encryption. Flask session cookies should be plenty secure! server.py <http://mercury.picoctf.net:18835/>

## 풀이 메모
1. Looking at the server script we can see that the app’s secret key is set to a random cookie name:
2. The app’s secret key is used to sign a flask session cookie so that it cannot be modified. However, since we know the secret key is one of the 28 cookie names, we can simply try them all until we successfully decrypt the cookie.
3. So, the first step is to go to the website and copy a session cookie: eyJ2ZXJ5X2F1dGgiOiJzbmlja2VyZG9vZGxlIn0.YFNV9A.fnwblKJPgNM2A8VNOblzALp9bTI
4. We can write a script that uses the logic from Flask’s SecureCookieSessionInterface to decode and encode cookies.

## 같이 보면 좋은 페이지
- [[picoctf-2021-web-exploitation-survey]]
- [[picoctf-2021-web-exploitation-family-hub]]
- [[picoctf-2021-topic-map]]
