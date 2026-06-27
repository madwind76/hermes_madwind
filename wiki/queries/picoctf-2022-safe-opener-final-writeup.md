---
title: Safe Opener — picoCTF 2022 reverse engineering writeup
created: 2026-06-24
updated: 2026-06-24
type: query
tags: [ctf, picoctf, picoctf2022, reverse-engineering]
sources: [https://raw.githubusercontent.com/noamgariani11/PicoCTF-2022-Writeup/main/Reverse%20Engineering/Safe%20Opener/SafeOpener.md, https://raw.githubusercontent.com/noamgariani11/PicoCTF-2022-Writeup/tree/main/Reverse%20Engineering/Safe%20Opener]
confidence: medium
---

# Safe Opener — picoCTF 2022 reverse engineering writeup

## 참고 URL
- [GitHub raw writeup](https://raw.githubusercontent.com/noamgariani11/PicoCTF-2022-Writeup/main/Reverse%20Engineering/Safe%20Opener/SafeOpener.md)
- [GitHub directory](https://raw.githubusercontent.com/noamgariani11/PicoCTF-2022-Writeup/tree/main/Reverse%20Engineering/Safe%20Opener)

## 핵심 요약
Can you open this safe?<br> I forgot the key to my safe but this program is supposed to <br>

## 풀이 메모
1. When you cat the java file out you can see in the main function it is calling an openSafe function to check if it is open. Since we are looking for the password as the flag it is likely in that function. Also take note that main function it is using base64 on the inputted string to compare to an encoded string.
2. This line of code is first outputting the SafeOpener.java file, then it is grepping for encodedkey. Since there are multiple lines with encodedkey I am using sed -n "5p" to print the 5th line only. Lastly, I am using cut with " as the delimiter and \ to escape the charater while looking at the second field and I then get just the encoded key.
3. This will give you the password. If you wanted to check for sure you could run the file,

## 같이 보면 좋은 페이지
- [[picoctf-2022-reverse-engineering-survey]]
- [[picoctf-2022-reverse-engineering-family-hub]]
- [[picoctf-2022-topic-map]]
