---
title: Magikarp Ground Mission — picoCTF 2021 General Skills writeup
created: 2026-06-24
updated: 2026-06-24
type: query
tags: [ctf, picoctf, picoctf2021, general-skills, writeup]
sources: [https://raw.githubusercontent.com/vivian-dai/PicoCTF2021-Writeup/main/General%20Skills/Magikarp%20Ground%20Mission/README.md]
confidence: medium
---

# Magikarp Ground Mission — picoCTF 2021 General Skills writeup

## 참고 URL
- [공개 writeup / 원문](https://raw.githubusercontent.com/vivian-dai/PicoCTF2021-Writeup/main/General%20Skills/Magikarp%20Ground%20Mission/README.md)

## 핵심 요약
Points: 30 Category: General Skills

## 풀이 메모
1. Hmm start by connecting to the server with `ssh ctf-player@venus.picoctf.net -p 50713` and `6d448c9c` as the password like the question says.
2. Using `ls` lists `1of3.flag.txt instructions-to-2of3.txt` With `cat 1of3.flag.txt`, we get `cat instructions-to-2of3.txt` says I typed in `cd ..` (go back a directory) then `ls -a` (list all because I have trust issues with hidden files) and came across `3of3.flag.txt` `cat 3of3.flag.txt` gave I kept going back (with `cd ..`) and listing the files and directories (`ls -a`) until `2of3.flag.txt` appeared.
3. `cat 2of3.flag.txt` gave

## 같이 보면 좋은 페이지
- [[picoctf-2021-general-skills-survey]]
- [[picoctf-2021-general-skills-family-hub]]
- [[picoctf-2021-topic-map]]
