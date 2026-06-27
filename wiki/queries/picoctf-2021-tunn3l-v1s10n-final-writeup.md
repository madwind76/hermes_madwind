---
title: Tunn3l v1s10n — picoCTF 2021 Forensics writeup
created: 2026-06-24
updated: 2026-06-24
type: query
tags: [ctf, picoctf, picoctf2021, forensics, writeup]
sources: [https://raw.githubusercontent.com/HHousen/PicoCTF-2021/master/Forensics/tunn3l%20v1s10n/README.md, https://raw.githubusercontent.com/vivian-dai/PicoCTF2021-Writeup/main/Forensics/tunn3l%20v1s10n/README.md]
confidence: medium
---

# Tunn3l v1s10n — picoCTF 2021 Forensics writeup

## 참고 URL
- [공개 writeup / 원문](https://raw.githubusercontent.com/HHousen/PicoCTF-2021/master/Forensics/tunn3l%20v1s10n/README.md)
- [대체 참고 자료](https://raw.githubusercontent.com/vivian-dai/PicoCTF2021-Writeup/main/Forensics/tunn3l%20v1s10n/README.md)

## 핵심 요약
We found this file. Recover the flag.

## 풀이 메모
1. There is a problem opening the file. Running file tunn3l_v1s10n produces tunn3l_v1s10n: data, which is not helpful. We can check a list of file signatures and see if there is a match between the magic bytes. We can see the first bytes in the tunn3l_v1s10n file using xxd -g 1 tunn3l_v1s10n | head:
2. The 42 4d match with a BMP image. We can open this image in Photopea, since it is able to load the image. However, all we see is a weird warped image and a fake flag.
3. We can change the height of the bitmap using a hex editor such as HexEd.it. The width starts at hex offset 12, lasts for 4 bytes, and is followed by the height at offset 16, which is also 4 bytes. The info is on the BMP Wikipedia page under the "Windows BITMAPINFOHEADER".
4. Let's set the height to the same number as the width (6e 04) since the image looks like part of it was extended outwards. We make the change in the hex editor replacing 32 01 at offset 16 to 6e 04, save the image, and then load it in Photopea.

## 같이 보면 좋은 페이지
- [[picoctf-2021-forensics-survey]]
- [[picoctf-2021-forensics-family-hub]]
- [[picoctf-2021-topic-map]]
