---
title: PcapPoisoning — picoCTF 2023 forensics writeup
created: 2026-06-24
updated: 2026-06-24
type: query
tags: [ctf, picoctf, picoctf2023, forensics, network]
sources: [https://raw.githubusercontent.com/noamgariani11/picoCTF-2023-Writeup/main/Forensics/PcapPoisoning/PcapPoisoning.md, https://github.com/noamgariani11/picoCTF-2023-Writeup/tree/main/Forensics/PcapPoisoning]
confidence: medium
---

# PcapPoisoning — picoCTF 2023 forensics writeup

## 참고 URL
- [GitHub raw writeup](https://raw.githubusercontent.com/noamgariani11/picoCTF-2023-Writeup/main/Forensics/PcapPoisoning/PcapPoisoning.md)
- [GitHub directory](https://github.com/noamgariani11/picoCTF-2023-Writeup/tree/main/Forensics/PcapPoisoning)

## 핵심 요약
How about some hide and seek heh? Download this file and find the flag.

## 풀이 메모
1. Open trace.pcap in wireshark
2. wget https://artifacts.picoctf.net/c/371/trace.pcap
3. Open trace.pcap in wireshark

If you go to the first TCP Retransmission then you will see the flag.

The way I went about solving this was I just clicked the starting TCP packet and followed the TCP stream. In the first TCP stream (1) you see this:

## 같이 보면 좋은 페이지
- [[picoctf-2023-forensics-survey]]
- [[picoctf-2023-forensics-family-hub]]
- [[picoctf-2023-topic-map]]
