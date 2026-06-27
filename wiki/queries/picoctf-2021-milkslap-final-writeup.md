---
title: Milkslap — picoCTF 2021 Forensics writeup
created: 2026-06-24
updated: 2026-06-24
type: query
tags: [ctf, picoctf, picoctf2021, forensics, writeup]
sources: [https://raw.githubusercontent.com/HHousen/PicoCTF-2021/master/Forensics/Milkslap/README.md, https://raw.githubusercontent.com/vivian-dai/PicoCTF2021-Writeup/main/Forensics/Milkslap/README.md]
confidence: medium
---

# Milkslap — picoCTF 2021 Forensics writeup

## 참고 URL
- [공개 writeup / 원문](https://raw.githubusercontent.com/HHousen/PicoCTF-2021/master/Forensics/Milkslap/README.md)
- [대체 참고 자료](https://raw.githubusercontent.com/vivian-dai/PicoCTF2021-Writeup/main/Forensics/Milkslap/README.md)

## 핵심 요약
🥛

## 풀이 메모
1. When we view the source of the website, we can look at the stylesheet at /style.css, and see that it loads an image from concat_v.png. Let's download this image.
2. Since this image is a PNG, we can use a steganography tool called zsteg like so: zsteg concat_v.png
3. More information about different steganography tools can be found on HackTricks Stego Tricks

## 같이 보면 좋은 페이지
- [[picoctf-2021-forensics-survey]]
- [[picoctf-2021-forensics-family-hub]]
- [[picoctf-2021-topic-map]]
