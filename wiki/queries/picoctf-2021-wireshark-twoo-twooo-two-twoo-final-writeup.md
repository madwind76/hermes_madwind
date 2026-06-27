---
title: Wireshark twoo twooo two twoo... — picoCTF 2021 Forensics writeup
created: 2026-06-24
updated: 2026-06-24
type: query
tags: [ctf, picoctf, picoctf2021, forensics, writeup]
sources: [https://raw.githubusercontent.com/HHousen/PicoCTF-2021/master/Forensics/Wireshark%20twoo%20twooo%20two%20twoo.../README.md]
confidence: medium
---

# Wireshark twoo twooo two twoo... — picoCTF 2021 Forensics writeup

## 참고 URL
- [공개 writeup / 원문](https://raw.githubusercontent.com/HHousen/PicoCTF-2021/master/Forensics/Wireshark%20twoo%20twooo%20two%20twoo.../README.md)

## 핵심 요약
Can you find the flag? shark2.pcapng.

## 풀이 메모
1. Upon initial inspection, there seem to be a lot of requests to a /flag endpoint. Each request shows a different flag so these must be a distraction.
2. After searching through the file I noticed many DNS requests for various subdomains of reddshrimpandherring.com. This looks like the suspicious traffic that one of the challenge hints refers to.
3. A lot of the DNS queries have a destination of 8.8.8.8. However, a subset have a destination for 18.217.1.57.
4. We can apply the filter dns and ip.dst==18.217.1.57 to only see DNS requests to this IP address. If we take the subdomains of reddshrimpandherring.com and append them in order we get: cGljb0NURntkbnNfM3hmMWxfZnR3X2RlYWRiZWVmfQ==

## 같이 보면 좋은 페이지
- [[picoctf-2021-forensics-survey]]
- [[picoctf-2021-forensics-family-hub]]
- [[picoctf-2021-topic-map]]
