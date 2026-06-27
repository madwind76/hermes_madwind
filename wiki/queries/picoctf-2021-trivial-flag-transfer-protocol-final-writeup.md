---
title: Trivial Flag Transfer Protocol — picoCTF 2021 Forensics writeup
created: 2026-06-24
updated: 2026-06-24
type: query
tags: [ctf, picoctf, picoctf2021, forensics, writeup]
sources: [https://raw.githubusercontent.com/HHousen/PicoCTF-2021/master/Forensics/Trivial%20Flag%20Transfer%20Protocol/README.md, https://raw.githubusercontent.com/vivian-dai/PicoCTF2021-Writeup/main/Forensics/Trivial%20Flag%20Transfer%20Protocol/README.md]
confidence: medium
---

# Trivial Flag Transfer Protocol — picoCTF 2021 Forensics writeup

## 참고 URL
- [공개 writeup / 원문](https://raw.githubusercontent.com/HHousen/PicoCTF-2021/master/Forensics/Trivial%20Flag%20Transfer%20Protocol/README.md)
- [대체 참고 자료](https://raw.githubusercontent.com/vivian-dai/PicoCTF2021-Writeup/main/Forensics/Trivial%20Flag%20Transfer%20Protocol/README.md)

## 핵심 요약
Figure out how they moved the flag.

## 풀이 메모
1. Open the packet capture file in wireshark. Go to File > Export Objects > TFTP.
2. If we preview the instructions document we find: GSGCQBRFAGRAPELCGBHEGENSSVPFBJRZHFGQVFTHVFRBHESYNTGENAFSRE.SVTHERBHGNJNLGBUVQRGURSYNTNAQVJVYYPURPXONPXSBEGURCYNA. Putting this into quipqiup decodes it to t ftp doesnt encrypt our traffic so we must disguise our flag transfer figure out away to hide the flag and i will check back for the plan. The encoding is simply ROT13 so quipqiup is overkill. You can use cryptii instead.
3. The plan document says VHFRQGURCEBTENZNAQUVQVGJVGU-QHRQVYVTRAPR.PURPXBHGGURCUBGBF, which decodes to i used the program and hid it with due diligence check out the photos.
4. Save the program.deb file. Let's see if we can use it to decode the images. The program.deb is actually steghide (this is easily seen if you extract it), so install it if you don't already have it installed with sudo dpkg -i program.deb.

## 같이 보면 좋은 페이지
- [[picoctf-2021-forensics-survey]]
- [[picoctf-2021-forensics-family-hub]]
- [[picoctf-2021-topic-map]]
