---
title: repetitions — picoCTF 2023 general skills writeup
created: 2026-06-24
updated: 2026-06-24
type: query
tags: [ctf, picoctf, picoctf2023, general-skills, workflow]
sources: [https://raw.githubusercontent.com/noamgariani11/picoCTF-2023-Writeup/main/General%20Skills/repetitions/repetitions.md, https://github.com/noamgariani11/picoCTF-2023-Writeup/tree/main/General%20Skills/repetitions]
confidence: medium
---

# repetitions — picoCTF 2023 general skills writeup

## 참고 URL
- [GitHub raw writeup](https://raw.githubusercontent.com/noamgariani11/picoCTF-2023-Writeup/main/General%20Skills/repetitions/repetitions.md)
- [GitHub directory](https://github.com/noamgariani11/picoCTF-2023-Writeup/tree/main/General%20Skills/repetitions)

## 핵심 요약
Can you make sense of this file? Download the file here.

## 풀이 메모
1. You could also just put the text from the enc_flag file into cyberchef. You can just put decode from base64 many times until you see the flag. Cyberchef might also give you the magic pop-up to decode from base64. Also if your not in linux and you can't just do
2. echo "cat enc_flag | base64 --decode | base64 --decode | base64 --decode | base64 --decode | base64 --decode | base64 --decode" > script.sh
3. sudo chmod +x script.sh

## 같이 보면 좋은 페이지
- [[picoctf-2023-general-skills-survey]]
- [[picoctf-2023-general-skills-family-hub]]
- [[picoctf-2023-topic-map]]
