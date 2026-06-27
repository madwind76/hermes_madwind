---
title: It is my Birthday 2 — picoCTF 2021 Cryptography writeup
created: 2026-06-24
updated: 2026-06-24
type: query
tags: [ctf, picoctf, picoctf2021, crypto, writeup]
sources: [https://raw.githubusercontent.com/HHousen/PicoCTF-2021/master/Cryptography/It%20is%20my%20Birthday%202/README.md, https://raw.githubusercontent.com/vivian-dai/PicoCTF2021-Writeup/main/Cryptography/It%20is%20my%20Birthday%202/README.md]
confidence: medium
---

# It is my Birthday 2 — picoCTF 2021 Cryptography writeup

## 참고 URL
- [공개 writeup / 원문](https://raw.githubusercontent.com/HHousen/PicoCTF-2021/master/Cryptography/It%20is%20my%20Birthday%202/README.md)
- [대체 참고 자료](https://raw.githubusercontent.com/vivian-dai/PicoCTF2021-Writeup/main/Cryptography/It%20is%20my%20Birthday%202/README.md)

## 핵심 요약
My birthday is coming up again, but I want to have a very exclusive party for only the best cryptologists. See if you can solve my challenge, upload 2 valid PDFs that are different but have the same SHA1 hash. They should both have the same 1000 bytes at the end as the original invite. <http://mercury.picoctf.net:21110/> invite.pdf

## 풀이 메모
1. This challenge initially seems extremely difficult if not impossible. The SHAttered collision took the equivalent of 6,500 years of single-CPU computations and 110 years of single-GPU computations for a total cost of approximately $100,000! And this challenge wants us to create our own SHA-1 collision!?!
2. Looking around online does show that people have reduced the cost and complexity of this attack... but all of the current methods still cost tens of thousands of dollars.
3. The following summary is adapted from cs-ahmed/Hands-on-SHA1-Collisions-Using-sha1collider. SHAttered (by Stevens et al.) was the first ever practical and public SHA-1 collision between two PDF files. The type of collision they created was a fixed-prefix collision: A collision created by having identical starts of files, followed by distinct, slight differences in a small amount of the files, which is where the collision appears. After the collision is created, all that follows in both files (i.e. the suffixes of the files) must be identical. However, their collision was strategically placed to take advantage of a special property of the JPEG images in the PDFs: JPEG comments. Essentially, both files have the image data embedded inside, they just start displaying the image at at different byte depending on the value of a JPEG comment.
4. The two PDFs that Google created as part of SHAttered are publically available on the SHAttered website: PDF 1 / PDF 2. However, these files will not meet the criteria for the challenge because they do not have the same 1000 bytes at the end as the original invite. So, lets get the last 1000 bytes from the original invite and append them to both of the SHAttered PDFs.

## 같이 보면 좋은 페이지
- [[picoctf-2021-cryptography-survey]]
- [[picoctf-2021-cryptography-family-hub]]
- [[picoctf-2021-topic-map]]
