---
title: Stonks — picoCTF 2021 Binary Exploitation writeup
created: 2026-06-24
updated: 2026-06-24
type: query
tags: [ctf, picoctf, picoctf2021, binary-exploitation, writeup]
sources: [https://raw.githubusercontent.com/HHousen/PicoCTF-2021/master/Binary%20Exploitation/Stonks/README.md, https://raw.githubusercontent.com/vivian-dai/PicoCTF2021-Writeup/main/Binary%20Exploitation/Stonks/README.md]
confidence: medium
---

# Stonks — picoCTF 2021 Binary Exploitation writeup

## 참고 URL
- [공개 writeup / 원문](https://raw.githubusercontent.com/HHousen/PicoCTF-2021/master/Binary%20Exploitation/Stonks/README.md)
- [대체 참고 자료](https://raw.githubusercontent.com/vivian-dai/PicoCTF2021-Writeup/main/Binary%20Exploitation/Stonks/README.md)

## 핵심 요약
I decided to try something noone else has before. I made a bot to automatically trade stonks for me using AI and machine learning. I wouldn't believe you if you told me it's unsecure! vuln.c `nc mercury.picoctf.net 16439`

## 풀이 메모
1. We can compile the c source code using gcc -g -m32 vuln.c -o vuln and then we can generate a pwntools template using pwn template --host mercury.picoctf.net --port 16439 vuln.
2. This is a standard format string vulnerability. It even tells us that the program is vulnerable to a format string attack when we compile it.
3. Resources to learn about format string attacks: Syracuse University Lecture Notes / OWASP / LiveOverflow on YouTube / John Hammond PicoCTF 2017 'I've Got a Secret' on YouTube / PicoCTF 2018 'echooo' Writeup
4. However, my solution is based on this writeup.

## 같이 보면 좋은 페이지
- [[picoctf-2021-binary-exploitation-survey]]
- [[picoctf-2021-binary-exploitation-family-hub]]
- [[picoctf-2021-topic-map]]
