---
title: Very very very Hidden — picoCTF 2021 Forensics writeup
created: 2026-06-24
updated: 2026-06-24
type: query
tags: [ctf, picoctf, picoctf2021, forensics, writeup]
sources: [https://raw.githubusercontent.com/HHousen/PicoCTF-2021/master/Forensics/Very%20very%20very%20Hidden/README.md]
confidence: medium
---

# Very very very Hidden — picoCTF 2021 Forensics writeup

## 참고 URL
- [공개 writeup / 원문](https://raw.githubusercontent.com/HHousen/PicoCTF-2021/master/Forensics/Very%20very%20very%20Hidden/README.md)

## 핵심 요약
Finding a flag may take many steps, but if you look diligently it won't be long until you find the light at the end of the tunnel. Just remember, sometimes you find the hidden treasure, but sometimes you find only a hidden map to the treasure. try_me.pcap

## 풀이 메모
1. Looking at the attached packet capture file we find that most of the traffic uses TLS and thus isn't viewable to us without the proper key. However, there are 5 requests sent over regular HTTP so let's focus on those for now.
2. We can use this filter (http.request or ssl.handshake.type == 1) and !(udp.port eq 1900) in wireshark to see initial HTTP and HTTPS traffic. We see that two images are downloaded:
3. The evil_duck.png image is much larger than duck.png yet appears to be of lower quality indicating that something is hidden inside of it. However, using tools such as steghide and zsteg reveals nothing.
4. Let's go back to the PCAP file because there is a lot of traffic that we ignored. We can use the same filter as before and then create columns for Host and Server Name using this guide so we can easily see what websites the user visited. HTTPS hides the content and exact location of the request but it does not hide the server name.

## 같이 보면 좋은 페이지
- [[picoctf-2021-forensics-survey]]
- [[picoctf-2021-forensics-family-hub]]
- [[picoctf-2021-topic-map]]
