---
title: New Vignere — picoCTF 2021 Cryptography writeup
created: 2026-06-24
updated: 2026-06-24
type: query
tags: [ctf, picoctf, picoctf2021, crypto, writeup]
sources: [https://raw.githubusercontent.com/HHousen/PicoCTF-2021/master/Cryptography/New%20Vignere/README.md, https://raw.githubusercontent.com/vivian-dai/PicoCTF2021-Writeup/main/Cryptography/New%20Vignere/README.md]
confidence: medium
---

# New Vignere — picoCTF 2021 Cryptography writeup

## 참고 URL
- [공개 writeup / 원문](https://raw.githubusercontent.com/HHousen/PicoCTF-2021/master/Cryptography/New%20Vignere/README.md)
- [대체 참고 자료](https://raw.githubusercontent.com/vivian-dai/PicoCTF2021-Writeup/main/Cryptography/New%20Vignere/README.md)

## 핵심 요약
Another slight twist on a classic, see if you can recover the flag. (Wrap with picoCTF{}) `epdfglkfnbjbhbpicohidjgkhfnejeecmjfnejddgmhpndmchbmifnepdhdmhbah` new_vignere.py

## 풀이 메모
1. This challenge is similar to New Caesar (the code is nearly identical) except its a Vignere cipher.
2. The hint for this challenge points to The Cryptanalysis section of Vigenère Cipher Wikipedia Page, which explains the "Kasiski examination". We can use an online Kasiski test tool to automatically find the key length to be 9. DCode shows that the key length could be 3, 9, or 6.
3. The Wikipedia page recommends using Kerckhoffs' method to discover the key letter (Caesar shift) for each column of the vignere cipher. However, that does not work in this case because the Vigenère table has been scrambled by the b16_encode function.
4. According to Wikipedia: "Once the length of the key is known, the ciphertext can be rewritten into that many columns, with each column corresponding to a single letter of the key. Each column consists of plaintext that has been encrypted by a single Caesar cipher. The Caesar key (shift) is just the letter of the Vigenère key that was used for that column. Using methods similar to those used to break the Caesar cipher, the letters in the ciphertext can be discovered."

## 같이 보면 좋은 페이지
- [[picoctf-2021-cryptography-survey]]
- [[picoctf-2021-cryptography-family-hub]]
- [[picoctf-2021-topic-map]]
