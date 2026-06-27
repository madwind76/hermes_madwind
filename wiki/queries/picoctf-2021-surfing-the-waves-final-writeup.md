---
title: Surfing the Waves — picoCTF 2021 Forensics writeup
created: 2026-06-24
updated: 2026-06-24
type: query
tags: [ctf, picoctf, picoctf2021, forensics, writeup]
sources: [https://raw.githubusercontent.com/HHousen/PicoCTF-2021/master/Forensics/Surfing%20the%20Waves/README.md]
confidence: medium
---

# Surfing the Waves — picoCTF 2021 Forensics writeup

## 참고 URL
- [공개 writeup / 원문](https://raw.githubusercontent.com/HHousen/PicoCTF-2021/master/Forensics/Surfing%20the%20Waves/README.md)

## 핵심 요약
While you're going through the FBI's servers, you stumble across their incredible taste in music. One main.wav you found is particularly interesting, see if you can find the flag!

## 풀이 메모
1. Opening the audio file in audacity and applying the amplify effect shows that there is some kind of pattern in the file.
2. We can extract the data using Python and Scipy in script.py. If we read each audio frame we see that the first 6 values are: [2008, 2506, 2000, 1508, 2009, 8504]. I looped through all the values but chopped off the last two digits. The last two digits are always 0 followed by a number 1 though 9, which seem like random noise. After we remove the last two digits, there are only 16 unique values: [10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85]. There are also only 16 values in hexadecimal, so the data is probably encoded using hexadecimal.
3. We assume that 10 represents 1 in hexadecimal, 15 represents 2, 55 represents a, etc. So, now all we have to do is apply this mapping by looping through the rounded audio file data and mapping the value to its position in the sorted list of unique values. Each rounded audio file data point represents a hexadecimal character that has been encoded in some way. By looping through them we can undo the encoding using the aforementioned mapping. Then we can combine all the hexadecimal characters into one large hexadecimal string and convert it to ascii to get the entire program that was used to create the audio file. I saved the challenge program to decoded_program.py.

## 같이 보면 좋은 페이지
- [[picoctf-2021-forensics-survey]]
- [[picoctf-2021-forensics-family-hub]]
- [[picoctf-2021-topic-map]]
