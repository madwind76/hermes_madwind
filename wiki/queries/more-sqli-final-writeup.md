---
title: More SQLi — picoCTF 2023 web exploitation writeup
created: 2026-06-24
updated: 2026-06-24
type: query
tags: [ctf, picoctf, picoctf2023, web, sqli, source-analysis]
sources: [https://raw.githubusercontent.com/noamgariani11/picoCTF-2023-Writeup/main/Web%20Explotation/More%20SQLi/MoreSQLi.md, https://github.com/noamgariani11/picoCTF-2023-Writeup/tree/main/Web%20Explotation/More%20SQLi]
confidence: medium
---

# More SQLi — picoCTF 2023 web exploitation writeup

## 참고 URL
- [GitHub raw writeup](https://raw.githubusercontent.com/noamgariani11/picoCTF-2023-Writeup/main/Web%20Explotation/More%20SQLi/MoreSQLi.md)
- [GitHub directory](https://github.com/noamgariani11/picoCTF-2023-Writeup/tree/main/Web%20Explotation/More%20SQLi)

## 핵심 요약
Can you find the flag on this website. Try to find the flag here.

## 풀이 메모
1. It shows the password first so that is where you want to put the SQL Injection. Also you can notice it is single qoutes and not double qoutes so that will also be use in createing a SQL Injection Query.
2. You can see the first single qoute closes the password string and the OR 1=1 is always true. Additionall the comment "--" makes the rest of the code irrelevant.
3. Before Query:

## 같이 보면 좋은 페이지
- [[picoctf-2023-web-exploitation-survey]]
- [[picoctf-2023-web-exploitation-family-hub]]
- [[picoctf-2023-topic-map]]
