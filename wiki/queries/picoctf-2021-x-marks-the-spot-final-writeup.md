---
title: X marks the spot — picoCTF 2021 Web Exploitation writeup
created: 2026-06-24
updated: 2026-06-24
type: query
tags: [ctf, picoctf, picoctf2021, web-exploitation, writeup]
sources: [https://raw.githubusercontent.com/HHousen/PicoCTF-2021/master/Web%20Exploitation/X%20marks%20the%20spot/README.md]
confidence: medium
---

# X marks the spot — picoCTF 2021 Web Exploitation writeup

## 참고 URL
- [공개 writeup / 원문](https://raw.githubusercontent.com/HHousen/PicoCTF-2021/master/Web%20Exploitation/X%20marks%20the%20spot/README.md)

## 핵심 요약
Another login you have to bypass. Maybe you can find an injection that works? <http://mercury.picoctf.net:16521/>

## 풀이 메모
1. The challenge says this is an XPATH injection. We can try the standard payload blah' or 1=1 or 'a'='a from OWASP and see if we can sign in. This results in a message saying You're on the right path., so it looks like our query succeeded. However, we did not get redirected to an application so this looks like a "blind XPATH injection."
2. HackTricks is a good resource here. Their XPATH Injection article explains the basics of XPATH and even has an example script to execute a blind XPATH injection attack. This script was the basis of my solve script.
3. Essentially, when the You're on the right path. message is shown, we know our query returned a true value and otherwise our query was false. We can modify the query using or to join the login query with a special query and then tell XPATH to ignore the rest of the login query.
4. By using ' or string-length(//user[position()=3]/pass)=4 or ''=' we can check if the length of the pass field of the 3rd user element in document is 4. I guessed that the password field would be called pass because that is the name of the form element in the website's HTML. The position()=3 was manually checked by scanning each position starting at 1. If the name of the field is unknown, a query such as the following could be used instead: ' or string-length(//user[position()=1]/child::node()[position()=1])=4 or ''='. We can bruteforce the 4 in this case and determine the length of the 3rd user's password.

## 같이 보면 좋은 페이지
- [[picoctf-2021-web-exploitation-survey]]
- [[picoctf-2021-web-exploitation-family-hub]]
- [[picoctf-2021-topic-map]]
