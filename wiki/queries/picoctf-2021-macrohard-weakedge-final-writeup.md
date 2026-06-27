---
title: MacroHard WeakEdge — picoCTF 2021 Forensics writeup
created: 2026-06-24
updated: 2026-06-24
type: query
tags: [ctf, picoctf, picoctf2021, forensics, writeup]
sources: [https://raw.githubusercontent.com/HHousen/PicoCTF-2021/master/Forensics/MacroHard%20WeakEdge/README.md, https://raw.githubusercontent.com/vivian-dai/PicoCTF2021-Writeup/main/Forensics/MacroHard%20WeakEdge/README.md]
confidence: medium
---

# MacroHard WeakEdge — picoCTF 2021 Forensics writeup

## 참고 URL
- [공개 writeup / 원문](https://raw.githubusercontent.com/HHousen/PicoCTF-2021/master/Forensics/MacroHard%20WeakEdge/README.md)
- [대체 참고 자료](https://raw.githubusercontent.com/vivian-dai/PicoCTF2021-Writeup/main/Forensics/MacroHard%20WeakEdge/README.md)

## 핵심 요약
I've hidden a flag in this file. Can you find it? Forensics is fun.pptm

## 풀이 메모
1. Extract the PowerPoint presentation as a ZIP file, since PowerPoint files are actually ZIPs: unzip Forensics\ is\ fun.pptm
2. Looking through the extracted files, ppt/slideMasters/hidden looks suspicious.
3. Reading that file (cat ppt/slideMasters/hidden) shows Z m x h Z z o g c G l j b 0 N U R n t E M W R f d V 9 r b j B 3 X 3 B w d H N f c l 9 6 M X A 1 f Q.
4. We can decode that as base64 using CyberChef&input=WiBtIHggaCBaIHogbyBnIGMgRyBsIGogYiAwIE4gVSBSIG4gdCBFIE0gVyBSIGYgZCBWIDkgciBiIGogQiAzIFggMyBCIHcgZCBIIE4gZiBjIGwgOSA2IE0gWCBBIDEgZiBR) to get the flag.

## 같이 보면 좋은 페이지
- [[picoctf-2021-forensics-survey]]
- [[picoctf-2021-forensics-family-hub]]
- [[picoctf-2021-topic-map]]
