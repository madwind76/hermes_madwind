---
title: Play Nice — picoCTF 2021 Cryptography writeup
created: 2026-06-24
updated: 2026-06-24
type: query
tags: [ctf, picoctf, picoctf2021, crypto, writeup]
sources: [https://raw.githubusercontent.com/HHousen/PicoCTF-2021/master/Cryptography/Play%20Nice/README.md, https://raw.githubusercontent.com/vivian-dai/PicoCTF2021-Writeup/main/Cryptography/Play%20Nice/README.md]
confidence: medium
---

# Play Nice — picoCTF 2021 Cryptography writeup

## 참고 URL
- [공개 writeup / 원문](https://raw.githubusercontent.com/HHousen/PicoCTF-2021/master/Cryptography/Play%20Nice/README.md)
- [대체 참고 자료](https://raw.githubusercontent.com/vivian-dai/PicoCTF2021-Writeup/main/Cryptography/Play%20Nice/README.md)

## 핵심 요약
Not all ancient ciphers were so bad... The flag is not in standard format. `nc mercury.picoctf.net 6057` playfair.py

## 풀이 메모
1. Look at the source code and at the bottom it links to the Wikipedia page for a Playfair cipher
2. Find a Playfair cipher decoder, such as DCode. Paste in the ciphertext y7bcvefqecwfste224508y1ufb21ld and the alphabet/key meiktp6yh4wxruavj9no13fb8d027c5glzsq. Make sure to increase the grid size to 6x6 so the entire alphabet fits.
3. Click "Decrypt" to get WD9BUKBSPDTJ7SKD3KL8D6OA3F03G0 convert this to lowercase with python -c "print('WD9BUKBSPDTJ7SKD3KL8D6OA3F03G0'.lower())" to get wd9bukbspdtj7skd3kl8d6oa3f03g0.
4. Paste the decrypted text into the program on the server to get the flag: Congratulations! Here's the flag: 2e71b99fd3d07af3808f8dff2652ae0e.

## 같이 보면 좋은 페이지
- [[picoctf-2021-cryptography-survey]]
- [[picoctf-2021-cryptography-family-hub]]
- [[picoctf-2021-topic-map]]
