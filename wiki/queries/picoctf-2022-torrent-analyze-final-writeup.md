---
title: Torrent Analyze — picoCTF 2022 forensics writeup
created: 2026-06-24
updated: 2026-06-24
type: query
tags: [ctf, picoctf, picoctf2022, forensics]
sources: [https://raw.githubusercontent.com/noamgariani11/picoCTF-2022-Writeup/main/Forensics/Torrent%20Analyze/TorrentAnalyze.md, https://github.com/noamgariani11/picoCTF-2022-Writeup/tree/main/Forensics/Torrent%20Analyze/TorrentAnalyze.md]
confidence: medium
---

# Torrent Analyze — picoCTF 2022 forensics writeup

## 참고 URL
- [GitHub raw writeup](https://raw.githubusercontent.com/noamgariani11/picoCTF-2022-Writeup/main/Forensics/Torrent%20Analyze/TorrentAnalyze.md)
- [GitHub directory](https://github.com/noamgariani11/picoCTF-2022-Writeup/tree/main/Forensics/Torrent%20Analyze/TorrentAnalyze.md)

## 핵심 요약
SOS, someone is torrenting on our network. One of your colleagues has been using torrent to download

## 풀이 메모
1. THe objective is to find the file(s) that were downloaded through bit torrent. This is likely going to be done with the hash. With bittorrent it's called the info_hash. I initially tried search by bittorrent.info_hash as a filter, but then realized it is with BT-DHT.
2. wget https://artifacts.picoctf.net/c/165/torrent.pcap
3. wireshark torrent.pcap

## 같이 보면 좋은 페이지
- [[picoctf-2022-forensics-survey]]
- [[picoctf-2022-forensics-family-hub]]
- [[picoctf-2022-topic-map]]
