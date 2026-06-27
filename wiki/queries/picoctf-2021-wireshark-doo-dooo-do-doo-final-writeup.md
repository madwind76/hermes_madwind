---
title: Wireshark doo dooo do doo... — picoCTF 2021 Forensics writeup
created: 2026-06-24
updated: 2026-06-24
type: query
tags: [ctf, picoctf, picoctf2021, forensics, writeup]
sources: [https://raw.githubusercontent.com/HHousen/PicoCTF-2021/master/Forensics/Wireshark%20doo%20dooo%20do%20doo.../README.md, https://raw.githubusercontent.com/vivian-dai/PicoCTF2021-Writeup/main/Forensics/Wireshark%20doo%20dooo%20do%20doo/README.md]
confidence: medium
---

# Wireshark doo dooo do doo... — picoCTF 2021 Forensics writeup

## 참고 URL
- [공개 writeup / 원문](https://raw.githubusercontent.com/HHousen/PicoCTF-2021/master/Forensics/Wireshark%20doo%20dooo%20do%20doo.../README.md)
- [대체 참고 자료](https://raw.githubusercontent.com/vivian-dai/PicoCTF2021-Writeup/main/Forensics/Wireshark%20doo%20dooo%20do%20doo/README.md)

## 핵심 요약
Can you find the flag? shark1.pcapng.

## 풀이 메모
1. Open the file in wireshark and type in tcp.stream eq 5 to get the 5th TCP stream.
2. Right click any entry, click follow, and then click "TCP Stream."
3. The flag will now be shown, but it is encoded: Gur synt vf cvpbPGS{c33xno00_1_f33_h_qrnqorrs}
4. We can decode the flag by passing it through ROT13 since this is a basic Caesar's cipher. You can decode ROT13 using CyberChef&input=R3VyIHN5bnQgdmYgY3ZwYlBHU3tjMzN4bm8wMF8xX2YzM19oX3FybnFvcnJzfQ), for instance.

## 같이 보면 좋은 페이지
- [[picoctf-2021-forensics-survey]]
- [[picoctf-2021-forensics-family-hub]]
- [[picoctf-2021-topic-map]]
