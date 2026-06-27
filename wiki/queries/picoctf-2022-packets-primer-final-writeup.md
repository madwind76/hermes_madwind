---
title: Packets Primer — picoCTF 2022 forensics writeup
created: 2026-06-24
updated: 2026-06-24
type: query
tags: [ctf, picoctf, picoctf2022, forensics]
sources: [https://raw.githubusercontent.com/noamgariani11/picoCTF-2022-Writeup/main/Forensics/Packets%20Primer/PacketsPrimer.md, https://github.com/noamgariani11/picoCTF-2022-Writeup/tree/main/Forensics/Packets%20Primer/PacketsPrimer.md]
confidence: medium
---

# Packets Primer — picoCTF 2022 forensics writeup

## 참고 URL
- [GitHub raw writeup](https://raw.githubusercontent.com/noamgariani11/picoCTF-2022-Writeup/main/Forensics/Packets%20Primer/PacketsPrimer.md)
- [GitHub directory](https://github.com/noamgariani11/picoCTF-2022-Writeup/tree/main/Forensics/Packets%20Primer/PacketsPrimer.md)

## 핵심 요약
Download the packet capture file and use packet analysis software to find the flag.

## 풀이 메모
1. I first just tried to run strings before even running it in wireshark and I saw the flag.
2. ![image](https://user-images.githubusercontent.com/91398631/236730401-3c3e6bee-a3e7-4563-80dc-e57cfef2aeb2.png)
3. Then I used tr to get rid of all the spaces.

## 같이 보면 좋은 페이지
- [[picoctf-2022-forensics-survey]]
- [[picoctf-2022-forensics-family-hub]]
- [[picoctf-2022-topic-map]]
