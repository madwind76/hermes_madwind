---
title: MatchTheRegex — picoCTF 2023 web exploitation writeup
created: 2026-06-24
updated: 2026-06-24
type: query
tags: [ctf, picoctf, picoctf2023, web, regex, client-side]
sources: [https://raw.githubusercontent.com/noamgariani11/picoCTF-2023-Writeup/main/Web%20Explotation/MatchTheRegex/MatchTheRegex.md, https://github.com/noamgariani11/picoCTF-2023-Writeup/tree/main/Web%20Explotation/MatchTheRegex]
confidence: medium
---

# MatchTheRegex — picoCTF 2023 web exploitation writeup

## 참고 URL
- [GitHub raw writeup](https://raw.githubusercontent.com/noamgariani11/picoCTF-2023-Writeup/main/Web%20Explotation/MatchTheRegex/MatchTheRegex.md)
- [GitHub directory](https://github.com/noamgariani11/picoCTF-2023-Writeup/tree/main/Web%20Explotation/MatchTheRegex)

## 핵심 요약
How about trying to match a regular expression The website is running here.

## 풀이 메모
1. The comment shows that it started with 'p' and ends with 'F' which based on the challenge is probably "picoCTF" (case-sensitive) which it was and it gets the flag.
2. // ^p.....F!?

## 같이 보면 좋은 페이지
- [[picoctf-2023-web-exploitation-survey]]
- [[picoctf-2023-web-exploitation-family-hub]]
- [[picoctf-2023-topic-map]]
