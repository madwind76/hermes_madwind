---
title: keygenme-py — picoCTF 2021 Reverse Engineering writeup
created: 2026-06-24
updated: 2026-06-24
type: query
tags: [ctf, picoctf, picoctf2021, reverse-engineering, writeup]
sources: [https://raw.githubusercontent.com/HHousen/PicoCTF-2021/master/Reverse%20Engineering/keygenme-py/README.md, https://raw.githubusercontent.com/vivian-dai/PicoCTF2021-Writeup/main/Reverse%20Engineering/keygenme-py/README.md]
confidence: medium
---

# keygenme-py — picoCTF 2021 Reverse Engineering writeup

## 참고 URL
- [공개 writeup / 원문](https://raw.githubusercontent.com/HHousen/PicoCTF-2021/master/Reverse%20Engineering/keygenme-py/README.md)
- [대체 참고 자료](https://raw.githubusercontent.com/vivian-dai/PicoCTF2021-Writeup/main/Reverse%20Engineering/keygenme-py/README.md)

## 핵심 요약
keygenme-trial.py

## 풀이 메모
1. The program contains a variable called key_part_static1_trial that has the first part of the flag: picoCTF{1n_7h3_|<3y_of_. The portion of the flag we need to find if key_part_dynamic1_trial.
2. When the user chooses option "c", the enter_license function is called. It calls check_key with the user provided key (the flag) and bUsername_trial, which is b"GOUGH".
3. The check_key functions contains the code that fills in the key_part_dynamic1_trial. It takes the hexdigest of the sha256 hash of b"GOUGH" and then selects a certain character by an indexing to a certain point on that string.
4. We can simply find the hexdigest of the sha256 hash of b"GOUGH" and then get the characters at the positions it checks: "".join([hashlib.sha256(b"GOUGH").hexdigest()[x] for x in [4,5,3,6,2,7,1,8]]). This is the missing section of the flag.

## 같이 보면 좋은 페이지
- [[picoctf-2021-reverse-engineering-survey]]
- [[picoctf-2021-reverse-engineering-family-hub]]
- [[picoctf-2021-topic-map]]
