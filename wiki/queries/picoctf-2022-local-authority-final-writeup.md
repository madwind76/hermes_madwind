---
title: Local Authority — picoCTF 2022 web exploitation writeup
created: 2026-06-24
updated: 2026-06-24
type: query
tags: [ctf, picoctf, picoctf2022, web-exploitation]
sources: [https://raw.githubusercontent.com/noamgariani11/picoCTF-2022-Writeup/main/Web%20Exploitation/Local%20Authority/LocalAuthority.md, https://github.com/noamgariani11/picoCTF-2022-Writeup/tree/main/Web%20Exploitation/Local%20Authority/LocalAuthority.md]
confidence: medium
---

# Local Authority — picoCTF 2022 web exploitation writeup

## 참고 URL
- [GitHub raw writeup](https://raw.githubusercontent.com/noamgariani11/picoCTF-2022-Writeup/main/Web%20Exploitation/Local%20Authority/LocalAuthority.md)
- [GitHub directory](https://github.com/noamgariani11/picoCTF-2022-Writeup/tree/main/Web%20Exploitation/Local%20Authority/LocalAuthority.md)

## 핵심 요약
Can you get the flag? Go to this website and see what you can discover.

## 풀이 메모
1. http://saturn.picoctf.net:64710/login.php
2. and now files appeared in the source.

![image](https://user-images.githubusercontent.com/91398631/236641170-f16f2655-12df-43a7-93d5-5bebee028e5c.png)

In the login.php you can see some filtering and a hash but neither of these things help with logging in. But if you look at another file in the sources tab and shown at the top of the login.php code:

![image](https://user-images.githubusercontent.com/91398631/236641220-a7a330a7-bc05-4f0e-bebf-de03b3888156.png)

You can see a file called "secure.js".

![image](https://user-images.githubusercontent.com/91398631/236641230-5bed6648-c150-4dc9-b4fa-ea1b4693398c.png)

This file justs shows that user and password in plaintext. So I now went back to the orginal path of the website with the given credentials. This directed me to
3. http://saturn.picoctf.net:64710/admin.php

## 같이 보면 좋은 페이지
- [[picoctf-2022-web-exploitation-survey]]
- [[picoctf-2022-web-exploitation-family-hub]]
- [[picoctf-2022-topic-map]]
