---
title: Scavenger Hunt — picoCTF 2021 Web Exploitation writeup
created: 2026-06-24
updated: 2026-06-24
type: query
tags: [ctf, picoctf, picoctf2021, web-exploitation, writeup]
sources: [https://raw.githubusercontent.com/HHousen/PicoCTF-2021/master/Web%20Exploitation/Scavenger%20Hunt/README.md, https://raw.githubusercontent.com/vivian-dai/PicoCTF2021-Writeup/main/Web%20Exploitation/Scavenger%20Hunt/README.md]
confidence: medium
---

# Scavenger Hunt — picoCTF 2021 Web Exploitation writeup

## 참고 URL
- [공개 writeup / 원문](https://raw.githubusercontent.com/HHousen/PicoCTF-2021/master/Web%20Exploitation/Scavenger%20Hunt/README.md)
- [대체 참고 자료](https://raw.githubusercontent.com/vivian-dai/PicoCTF2021-Writeup/main/Web%20Exploitation/Scavenger%20Hunt/README.md)

## 핵심 요약
There is some interesting information hidden around this site <http://mercury.picoctf.net:39491/>. Can you find it?

## 풀이 메모
1. view-source:<http://mercury.picoctf.net:39491/>: <!-- Here's the first part of the flag: picoCTF{t -->
2. <http://mercury.picoctf.net:39491/mycss.css>: /* CSS makes the page look nice, and yes, it also has part of the flag. Here's part 2: h4ts_4_l0 */
3. <http://mercury.picoctf.net:39491/myjs.js>: /* How can I keep Google from indexing my website? */ so lets go to <http://mercury.picoctf.net:39491/robots.txt> and find Part 3: t_0f_pl4c and well as I think this is an apache server... can you Access the next flag?
4. <http://mercury.picoctf.net:39491/.htaccess>: Part 4: 3s_2_lO0k and I love making websites on my Mac, I can Store a lot of information there.

## 같이 보면 좋은 페이지
- [[picoctf-2021-web-exploitation-survey]]
- [[picoctf-2021-web-exploitation-family-hub]]
- [[picoctf-2021-topic-map]]
