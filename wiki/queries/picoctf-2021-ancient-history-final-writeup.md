---
title: Ancient History — picoCTF 2021 Web Exploitation writeup
created: 2026-06-24
updated: 2026-06-24
type: query
tags: [ctf, picoctf, picoctf2021, web-exploitation, writeup]
sources: [https://raw.githubusercontent.com/HHousen/PicoCTF-2021/master/Web%20Exploitation/Ancient%20History/README.md, https://raw.githubusercontent.com/vivian-dai/PicoCTF2021-Writeup/main/Web%20Exploitation/Ancient%20History/README.md]
confidence: medium
---

# Ancient History — picoCTF 2021 Web Exploitation writeup

## 참고 URL
- [공개 writeup / 원문](https://raw.githubusercontent.com/HHousen/PicoCTF-2021/master/Web%20Exploitation/Ancient%20History/README.md)
- [대체 참고 자료](https://raw.githubusercontent.com/vivian-dai/PicoCTF2021-Writeup/main/Web%20Exploitation/Ancient%20History/README.md)

## 핵심 요약
I must have been sleep hacking or something, I don't remember visiting all of these sites... <http://mercury.picoctf.net:45211/> (try a couple different browsers if it's not working right)

## 풀이 메모
1. Visiting the website just shows "Hello World!", but viewing the source shows a lot of obfuscated JavaScript.
2. The browser history shows that the JavaScript performs some redirects where the URL parameter is a single character of the flag.
3. The issue is that visits to a page with the same character as the parameter are collapsed on the history page of modern browsers. So, let's try deobfuscating the code using JSNice.
4. Interestingly, the actual changes to the history (window.history.pushState) are made in the clear. Therefore, the obscuration is a meaningless distraction.

## 같이 보면 좋은 페이지
- [[picoctf-2021-web-exploitation-survey]]
- [[picoctf-2021-web-exploitation-family-hub]]
- [[picoctf-2021-topic-map]]
