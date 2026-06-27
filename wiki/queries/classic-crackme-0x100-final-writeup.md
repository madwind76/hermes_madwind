---
title: Classic Crackme 0x100 — picoCTF 2024 reverse engineering writeup
created: 2026-06-24
updated: 2026-06-24
type: query
tags: [ctf, picoctf, picoctf2024, reverse-engineering, binary-exploitation, decompilation]
sources: [https://github.com/noamgariani11/picoCTF-2024-Writeup/blob/main/Reverse%20Engineering/Classic-Crackme-0x100.md, https://picoctfsolutions.com/picoctf-2024-classic-crackme-0x100]
confidence: high
---

# Classic Crackme 0x100 — picoCTF 2024 reverse engineering writeup

## 참고 URL
- [GitHub writeup](https://github.com/noamgariani11/picoCTF-2024-Writeup/blob/main/Reverse%20Engineering/Classic-Crackme-0x100.md)
- [picoCTF Solutions](https://picoctfsolutions.com/picoctf-2024-classic-crackme-0x100)

## 핵심 요약
A classic Crackme. Find the password, get the flag! Binary can be downloaded here.

## 풀이 메모
1. wget https://artifacts.picoctf.net/c_titan/83/crackme100
2. undefined8 main(void)

{
  int iVar1;
  size_t sVar2;
  char local_a8 [64];
  undefined8 local_68;
  undefined8 local_60;
  undefined8 local_58;
  undefined8 local_50;
  undefined8 local_48;
  undefined7 local_40;
  undefined4 uStack_39;
  uint local_2c;
  uint local_28;
  char local_21;
  uint local_20;
  uint local_1c;
  uint local_18;
  int local_14;
  int local_10;
  int local_c;
  
  local_68 = 0x676d76727970786c;
  local_60 = 0x7672657270697564;
  local_58 = 0x727166766b716f6d;
  local_50 = 0x6575717670716c62;
  local_48 = 0x796771706d7a7565;
  local_40 = 0x73687478726963;
  uStack_39 = 0x77616a;
  setvbuf(stdout,(char *)0x0,2,0);
  printf("Enter the secret password: ");
  __isoc99_scanf(&DAT_00402024,local_a8);
  local_c = 0;
  sVar2 = strlen((char *)&local_68);
  local_14 = (int)sVar2;
  local_18 = 0x55;
  local_1c = 0x33;
  local_20 = 0xf;
  local_21 = 'a';
  for (; local_c < 3; local_c = local_c + 1) {
    for (local_10 = 0; local_10 < local_14; local_10 = local_10 + 1) {
      local_28 = (local_10 % 0xff >> 1 & local_18) + (local_10 % 0xff & local_18);
      local_2c = ((int)local_28 >> 2 & local_1c) + (local_1c & local_28);
      iVar1 = ((int)local_2c >> 4 & local_20) +
              ((int)local_a8[local_10] - (int)local_21) + (local_20 & local_2c);
      local_a8[local_10] = local_21 + (char)iVar1 + (char)(iVar1 / 0x1a) * -0x1a;
    }
  }
  iVar1 = memcmp(local_a8,&local_68,(long)local_14);
  if (iVar1 == 0) {
    printf("SUCCESS! Here is your flag: %s\n","picoCTF{sample_flag}");
  }
  else {
    puts("FAILED!");
  }
  return 0;
}
3. At first, using the hex values above setvbuf as the cipher text was attempted but the key when inputted was incorrect. When running it through gdb with

## 같이 보면 좋은 페이지
- [[picoctf-2024-reverse-engineering-survey]]
- [[picoctf-2024-reverse-engineering-family-hub]]
- [[picoctf-2024-topic-map]]
