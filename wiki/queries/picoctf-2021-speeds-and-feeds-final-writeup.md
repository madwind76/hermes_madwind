---
title: speeds and feeds — picoCTF 2021 Reverse Engineering writeup
created: 2026-06-24
updated: 2026-06-24
type: query
tags: [ctf, picoctf, picoctf2021, reverse-engineering, writeup]
sources: [https://raw.githubusercontent.com/HHousen/PicoCTF-2021/master/Reverse%20Engineering/speeds%20and%20feeds/README.md, https://raw.githubusercontent.com/vivian-dai/PicoCTF2021-Writeup/main/Reverse%20Engineering/speeds%20and%20feeds/README.md]
confidence: medium
---

# speeds and feeds — picoCTF 2021 Reverse Engineering writeup

## 참고 URL
- [공개 writeup / 원문](https://raw.githubusercontent.com/HHousen/PicoCTF-2021/master/Reverse%20Engineering/speeds%20and%20feeds/README.md)
- [대체 참고 자료](https://raw.githubusercontent.com/vivian-dai/PicoCTF2021-Writeup/main/Reverse%20Engineering/speeds%20and%20feeds/README.md)

## 핵심 요약
There is something on my shop network running at mercury.picoctf.net:16524, but I can't tell what it is. Can you?

## 풀이 메모
1. We can use nc to connect to the challenge and output the commands to a file: nc mercury.picoctf.net 16524 > cnc_command.txt
2. Searching for What language does a CNC machine use? finds that the answer is g-code Searching for simulate g-code finds NCViewer (WebGCode is another option).
3. We can paste in the contents of cnc_command.txt into the "GCode File" panel and then click "Plot" to view the flag.

## 같이 보면 좋은 페이지
- [[picoctf-2021-reverse-engineering-survey]]
- [[picoctf-2021-reverse-engineering-family-hub]]
- [[picoctf-2021-topic-map]]
