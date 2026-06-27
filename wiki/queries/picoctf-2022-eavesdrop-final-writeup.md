---
title: Eavesdrop — picoCTF 2022 forensics writeup
created: 2026-06-24
updated: 2026-06-24
type: query
tags: [ctf, picoctf, picoctf2022, forensics]
sources: [https://raw.githubusercontent.com/noamgariani11/picoCTF-2022-Writeup/main/Forensics/Eavesdrop/Eavesdrop.md, https://github.com/noamgariani11/picoCTF-2022-Writeup/tree/main/Forensics/Eavesdrop/Eavesdrop.md]
confidence: medium
---

# Eavesdrop — picoCTF 2022 forensics writeup

## 참고 URL
- [GitHub raw writeup](https://raw.githubusercontent.com/noamgariani11/picoCTF-2022-Writeup/main/Forensics/Eavesdrop/Eavesdrop.md)
- [GitHub directory](https://github.com/noamgariani11/picoCTF-2022-Writeup/tree/main/Forensics/Eavesdrop/Eavesdrop.md)

## 핵심 요약
Download this packet capture and find the flag. - Download packet capture

## 풀이 메모
1. For this challenge I used tcpflow on the pcap file. You can do it through wireshark as well though.
2. Then I ran this command:
3. This gets all the transmitted file with "tcpflow -r". Here are all the files in the working directory so far after running tcpflow.

## 같이 보면 좋은 페이지
- [[picoctf-2022-forensics-survey]]
- [[picoctf-2022-forensics-family-hub]]
- [[picoctf-2022-topic-map]]
