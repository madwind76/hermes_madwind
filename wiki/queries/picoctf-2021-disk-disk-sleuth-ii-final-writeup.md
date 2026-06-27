---
title: Disk, disk, sleuth! II — picoCTF 2021 Forensics writeup
created: 2026-06-24
updated: 2026-06-24
type: query
tags: [ctf, picoctf, picoctf2021, forensics, writeup]
sources: [https://raw.githubusercontent.com/HHousen/PicoCTF-2021/master/Forensics/Disk%2C%20disk%2C%20sleuth%21%20II/README.md, https://raw.githubusercontent.com/vivian-dai/PicoCTF2021-Writeup/main/Forensics/Disk%2C%20disk%2C%20sleuth%21%20II/README.md]
confidence: medium
---

# Disk, disk, sleuth! II — picoCTF 2021 Forensics writeup

## 참고 URL
- [공개 writeup / 원문](https://raw.githubusercontent.com/HHousen/PicoCTF-2021/master/Forensics/Disk%2C%20disk%2C%20sleuth%21%20II/README.md)
- [대체 참고 자료](https://raw.githubusercontent.com/vivian-dai/PicoCTF2021-Writeup/main/Forensics/Disk%2C%20disk%2C%20sleuth%21%20II/README.md)

## 핵심 요약
All we know is the file with the flag is named `down-at-the-bottom.txt`... Disk image: dds2-alpine.flag.img.gz

## 풀이 메모
1. Using the TSK Tool Overview website we can find that the fls command can list all files in a directory. We specify the -r, which means recursive so it will scan the entire disk image, and -p, so it prints the full path, flags. The -o flag is the offset of the partition we want to use, which can be dounf by running mmls dds2-alpine.flag.img. Finally, we search the output using grep for the name of the file given in the challenge description. So, the resulting command looks as follows: fls -r -p -o 2048 dds2-alpine.flag.img | grep down-at-the-bottom.txt. The output is: r/r 18291: root/down-at-the-bottom.txt
2. 18291 is the inode number of the file. We can use icat to list the contents of that inode like so: icat -o 2048 dds2-alpine.flag.img 18291
3. Alternatively, autopsy can be used to interact with the disk in a GUI, which may be easier. It was easier for me at at first.

## 같이 보면 좋은 페이지
- [[picoctf-2021-forensics-survey]]
- [[picoctf-2021-forensics-family-hub]]
- [[picoctf-2021-topic-map]]
