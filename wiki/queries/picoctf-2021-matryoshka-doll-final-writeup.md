---
title: Matryoshka doll — picoCTF 2021 Forensics writeup
created: 2026-06-24
updated: 2026-06-24
type: query
tags: [ctf, picoctf, picoctf2021, forensics, writeup]
sources: [https://raw.githubusercontent.com/HHousen/PicoCTF-2021/master/Forensics/Matryoshka%20doll/README.md, https://raw.githubusercontent.com/vivian-dai/PicoCTF2021-Writeup/main/Forensics/Matryoshka%20doll/README.md]
confidence: medium
---

# Matryoshka doll — picoCTF 2021 Forensics writeup

## 참고 URL
- [공개 writeup / 원문](https://raw.githubusercontent.com/HHousen/PicoCTF-2021/master/Forensics/Matryoshka%20doll/README.md)
- [대체 참고 자료](https://raw.githubusercontent.com/vivian-dai/PicoCTF2021-Writeup/main/Forensics/Matryoshka%20doll/README.md)

## 핵심 요약
Matryoshka dolls are a set of wooden dolls of decreasing size placed one inside another. What's the final one? Image: this

## 풀이 메모
1. The problem suggests files places inside of other files, so let's run binwalk dolls.jpg.
2. We can extract the files by running binwalk --dd='.*' dolls.jpg and then cd _dolls.jpg.extracted.
3. After some trial and error, the correct solution is to extract the zip file, cd base_images, and then repeat step 3 on 2_c.jpg.
4. Now that you are in _2_c.jpg.extracted, extract the zip file and repeat step 3.

## 같이 보면 좋은 페이지
- [[picoctf-2021-forensics-survey]]
- [[picoctf-2021-forensics-family-hub]]
- [[picoctf-2021-topic-map]]
