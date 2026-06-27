---
title: Disk, disk, sleuth! — picoCTF 2021 Forensics writeup
created: 2026-06-24
updated: 2026-06-24
type: query
tags: [ctf, picoctf, picoctf2021, forensics, writeup]
sources: [https://raw.githubusercontent.com/HHousen/PicoCTF-2021/master/Forensics/Disk%2C%20disk%2C%20sleuth%21/README.md, https://raw.githubusercontent.com/vivian-dai/PicoCTF2021-Writeup/main/Forensics/Disk%2C%20disk%2C%20sleuth%21/README.md]
confidence: medium
---

# Disk, disk, sleuth! — picoCTF 2021 Forensics writeup

## 참고 URL
- [공개 writeup / 원문](https://raw.githubusercontent.com/HHousen/PicoCTF-2021/master/Forensics/Disk%2C%20disk%2C%20sleuth%21/README.md)
- [대체 참고 자료](https://raw.githubusercontent.com/vivian-dai/PicoCTF2021-Writeup/main/Forensics/Disk%2C%20disk%2C%20sleuth%21/README.md)

## 핵심 요약
Use `srch_strings` from the sleuthkit and some terminal-fu to find a flag in this disk image: dds1-alpine.flag.img.gz

## 풀이 메모
1. Extract the disk by running gunzip dds1-alpine.flag.img.gz.
2. Make sure autopsy is installed (sudo apt install autopsy).
3. Use the srch_strings command as suggested by the challenge and then search for picoCTF: srch_strings dds1-alpine.flag.img | grep picoCTF

## 같이 보면 좋은 페이지
- [[picoctf-2021-forensics-survey]]
- [[picoctf-2021-forensics-family-hub]]
- [[picoctf-2021-topic-map]]
