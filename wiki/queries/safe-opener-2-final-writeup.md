---
title: Safe Opener 2 — picoCTF 2023 reverse engineering writeup
created: 2026-06-24
updated: 2026-06-24
type: query
tags: [ctf, picoctf, picoctf2023, reverse-engineering, source-analysis]
sources: [https://raw.githubusercontent.com/noamgariani11/picoCTF-2023-Writeup/main/Reverse%20Engineering/Safe%20Opener%202/SafeOpener2.md, https://github.com/noamgariani11/picoCTF-2023-Writeup/tree/main/Reverse%20Engineering/Safe%20Opener%202]
confidence: medium
---

# Safe Opener 2 — picoCTF 2023 reverse engineering writeup

## 참고 URL
- [GitHub raw writeup](https://raw.githubusercontent.com/noamgariani11/picoCTF-2023-Writeup/main/Reverse%20Engineering/Safe%20Opener%202/SafeOpener2.md)
- [GitHub directory](https://github.com/noamgariani11/picoCTF-2023-Writeup/tree/main/Reverse%20Engineering/Safe%20Opener%202)

## 핵심 요약
What can you do with this file? I forgot the key to my safe but this file is supposed to help me with retrieving the lost key. Can you help me unlock my safe?

## 풀이 메모
1. The flag near the end of the file.
2. I then opened the file.
3. Grep gets the line with "pico" which is the flag. And cut looks at the " delimiter where I used \ as an escape charater, -f1 is for looking at the first feild.

## 같이 보면 좋은 페이지
- [[picoctf-2023-reverse-engineering-survey]]
- [[picoctf-2023-reverse-engineering-family-hub]]
- [[picoctf-2023-topic-map]]
