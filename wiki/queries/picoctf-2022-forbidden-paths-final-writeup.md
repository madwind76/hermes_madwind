---
title: Forbidden Paths — picoCTF 2022 web exploitation writeup
created: 2026-06-24
updated: 2026-06-24
type: query
tags: [ctf, picoctf, picoctf2022, web-exploitation]
sources: [https://raw.githubusercontent.com/noamgariani11/picoCTF-2022-Writeup/main/Web%20Exploitation/Forbidden%20Paths/ForbiddenPaths.md, https://github.com/noamgariani11/picoCTF-2022-Writeup/tree/main/Web%20Exploitation/Forbidden%20Paths/ForbiddenPaths.md]
confidence: medium
---

# Forbidden Paths — picoCTF 2022 web exploitation writeup

## 참고 URL
- [GitHub raw writeup](https://raw.githubusercontent.com/noamgariani11/picoCTF-2022-Writeup/main/Web%20Exploitation/Forbidden%20Paths/ForbiddenPaths.md)
- [GitHub directory](https://github.com/noamgariani11/picoCTF-2022-Writeup/tree/main/Web%20Exploitation/Forbidden%20Paths/ForbiddenPaths.md)

## 핵심 요약
Can you get the flag? Here's the website.

## 풀이 메모
1. usr/share/nginx/html/flag.txt
2. as the filename as that is where the website files are located and flag.txt should probably be there. However, it says that I am "Not Authorized" when I inputted this. Based on the description I probably should change the input in some way to bypass the filtering.

My first idea was URL encoding and changing all of the "/" to %2F. This did not work.

Next, I just replaced all the previous directories with ".." since it isn't needed for the command and might be causing issues. So I inputted this into the filename field:
3. ../../../../flag.txt

## 같이 보면 좋은 페이지
- [[picoctf-2022-web-exploitation-survey]]
- [[picoctf-2022-web-exploitation-family-hub]]
- [[picoctf-2022-topic-map]]
