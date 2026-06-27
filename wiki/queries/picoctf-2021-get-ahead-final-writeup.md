---
title: GET aHEAD — picoCTF 2021 Web Exploitation writeup
created: 2026-06-24
updated: 2026-06-24
type: query
tags: [ctf, picoctf, picoctf2021, web-exploitation, writeup]
sources: [https://raw.githubusercontent.com/HHousen/PicoCTF-2021/master/Web%20Exploitation/GET%20aHEAD/README.md, https://raw.githubusercontent.com/vivian-dai/PicoCTF2021-Writeup/main/Web%20Exploitation/Get%20aHead/README.md]
confidence: medium
---

# GET aHEAD — picoCTF 2021 Web Exploitation writeup

## 참고 URL
- [공개 writeup / 원문](https://raw.githubusercontent.com/HHousen/PicoCTF-2021/master/Web%20Exploitation/GET%20aHEAD/README.md)
- [대체 참고 자료](https://raw.githubusercontent.com/vivian-dai/PicoCTF2021-Writeup/main/Web%20Exploitation/Get%20aHead/README.md)

## 핵심 요약
Find the flag being held on this server to get ahead of the competition <http://mercury.picoctf.net:47967/>

## 풀이 메모
1. Use Burp Suite to intercept the request of clicking the "Choose Blue" button.
2. Change the POST request to a HEAD request:
3. The returned HTML from the HEAD request in the browser will be empty, but in the HTTP history tab of Proxy in Burp Suite you can find the flag as a HTTP header in the response:

## 같이 보면 좋은 페이지
- [[picoctf-2021-web-exploitation-survey]]
- [[picoctf-2021-web-exploitation-family-hub]]
- [[picoctf-2021-topic-map]]
