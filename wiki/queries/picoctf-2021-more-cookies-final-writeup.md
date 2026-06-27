---
title: More Cookies — picoCTF 2021 Web Exploitation writeup
created: 2026-06-24
updated: 2026-06-24
type: query
tags: [ctf, picoctf, picoctf2021, web-exploitation, writeup]
sources: [https://raw.githubusercontent.com/HHousen/PicoCTF-2021/master/Web%20Exploitation/More%20Cookies/README.md]
confidence: medium
---

# More Cookies — picoCTF 2021 Web Exploitation writeup

## 참고 URL
- [공개 writeup / 원문](https://raw.githubusercontent.com/HHousen/PicoCTF-2021/master/Web%20Exploitation/More%20Cookies/README.md)

## 핵심 요약
I forgot Cookies can Be modified Client-side, so now I decided to encrypt them! <http://mercury.picoctf.net:15614/>

## 풀이 메모
1. This is a continuation of the "Cookies" challenge, which I did not write up since it is very simple. However, this challenge is fairly difficult despite the point value.
2. There is a cookie called auth_name with the value eEozQmFzQUNUL2Y1c1hIWmZTOEl4OS9wcUwyRkMyVVE4MUdseEZRYnZWU1E3WXRoOHU5cjkwOXpGM3hwTVc4SGx5K1BNbGdBaFhUOFpXWWpCMTl6dE1QNlNzUGJOVTRpeGdSSnA5dDI2ODBXRXVBMkhpWUtWVVBTNmh6RnJGNXE=. Decoding this as base64 using CyberChef&input=ZUVvelFtRnpRVU5VTDJZMWMxaElXbVpUT0VsNE9TOXdjVXd5UmtNeVZWRTRNVWRzZUVaUlluWldVMUUzV1hSb09IVTVjamt3T1hwR00zaHdUVmM0U0d4NUsxQk5iR2RCYUZoVU9GcFhXV3BDTVRsNmRFMVFObE56VUdKT1ZUUnBlR2RTU25BNWRESTJPREJYUlhWQk1raHBXVXRXVlZCVE5taDZSbkpHTlhFPQ) produces gibberish since it is encrypted as per the challenge description.
3. The letters C, B, and C are capitalized in the challenge description which is a hint that cipher block chaining (CBC)) is used. CBC is vulnerable to a bit flip. This answer on the Crypto StackExchange extensively explains this attack. Essentially, there is a single bit that determines if the user is an admin. Maybe there is a parameter like admin=0 and if we change the correct bit then we can set admin=1. However, the position of this bit is unknown, so we can try every position until we get the flag.
4. Outdated (see 5 for improved method): ~~We write a Python script to complete this bruteforce attack. I originally only tried the first 10 positions, which was enough to get the flag so I left the max number of positions to try at 10.~~

## 같이 보면 좋은 페이지
- [[picoctf-2021-web-exploitation-survey]]
- [[picoctf-2021-web-exploitation-family-hub]]
- [[picoctf-2021-topic-map]]
