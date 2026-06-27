---
title: FactCheck — picoCTF 2024 reverse engineering writeup
created: 2026-06-24
updated: 2026-06-24
type: query
tags: [ctf, picoctf, picoctf2024, reverse-engineering, source-inspection, binary-exploitation]
sources: [https://github.com/noamgariani11/picoCTF-2024-Writeup/blob/main/Reverse%20Engineering/FactCheck.md, https://picoctfsolutions.com/picoctf-2024-factcheck]
confidence: high
---

# FactCheck — picoCTF 2024 reverse engineering writeup

## 참고 URL
- [GitHub writeup](https://github.com/noamgariani11/picoCTF-2024-Writeup/blob/main/Reverse%20Engineering/FactCheck.md)
- [picoCTF Solutions](https://picoctfsolutions.com/picoctf-2024-factcheck)

## 핵심 요약
This binary is putting together some important piece of information... Can you uncover that information?

## 풀이 메모
1. wget https://artifacts.picoctf.net/c_titan/187/bin
2. std::__cxx11::basic_string<>::basic_string
            ((char *)flagFirstHalf,(allocator *)"picoCTF{wELF_d0N3_mate_");
  std::allocator<char>::~allocator(&local_249);
  std::allocator<char>::allocator();
                    /* try { // try from 0010130a to 0010130e has its CatchHandler @ 00101996 */
  std::__cxx11::basic_string<>::basic_string((char *)char_0,(allocator *)&DAT_0010201d);
  std::allocator<char>::~allocator(&local_249);
  std::allocator<char>::allocator();
                    /* try { // try from 00101345 to 00101349 has its CatchHandler @ 001019b1 */
  std::__cxx11::basic_string<>::basic_string((char *)char_5,(allocator *)&DAT_0010201f);
  std::allocator<char>::~allocator(&local_249);
  std::allocator<char>::allocator();
                    /* try { // try from 00101380 to 00101384 has its CatchHandler @ 001019cc */
  std::__cxx11::basic_string<>::basic_string((char *)char_d,(allocator *)&DAT_00102021);
  std::allocator<char>::~allocator(&local_249);
  std::allocator<char>::allocator();
                    /* try { // try from 001013bb to 001013bf has its CatchHandler @ 001019e7 */
  std::__cxx11::basic_string<>::basic_string((char *)char_3,(allocator *)&DAT_00102023);
  std::allocator<char>::~allocator(&local_249);
  std::allocator<char>::allocator();
                    /* try { // try from 001013f6 to 001013fa has its CatchHandler @ 00101a02 */
  std::__cxx11::basic_string<>::basic_string((char *)char_2,(allocator *)&DAT_00102025);
  std::allocator<char>::~allocator(&local_249);
  std::allocator<char>::allocator();
                    /* try { // try from 00101431 to 00101435 has its CatchHandler @ 00101a1d */
  std::__cxx11::basic_string<>::basic_string((char *)char_a,(allocator *)&DAT_00102027);
  std::allocator<char>::~allocator(&local_249);
  std::allocator<char>::allocator();
                    /* try { // try from 0010146c to 00101470 has its CatchHandler @ 00101a38 */
  std::__cxx11::basic_string<>::basic_string((char *)char_a_2,(allocator *)&DAT_00102027);
  std::allocator<char>::~allocator(&local_249);
  std::allocator<char>::allocator();
                    /* try { // try from 001014a7 to 001014ab has its CatchHandler @ 00101a53 */
  std::__cxx11::basic_string<>::basic_string((char *)char_e,(allocator *)&DAT_00102029);
  std::allocator<char>::~allocator(&local_249);
  std::allocator<char>::allocator();
                    /* try { // try from 001014e2 to 001014e6 has its CatchHandler @ 00101a6e */
  std::__cxx11::basic_string<>::basic_string((char *)char_e_2,(allocator *)&DAT_00102029);
  std::allocator<char>::~allocator(&local_249);
  std::allocator<char>::allocator();
                    /* try { // try from 0010151d to 00101521 has its CatchHandler @ 00101a89 */
  std::__cxx11::basic_string<>::basic_string((char *)char_d_2,(allocator *)&DAT_00102021);
  std::allocator<char>::~allocator(&local_249);
  std::allocator<char>::allocator();
                    /* try { // try from 00101558 to 0010155c has its CatchHandler @ 00101aa4 */
  std::__cxx11::basic_string<>::basic_string((char *)char_b,(allocator *)&DAT_0010202b);
  std::allocator<char>::~allocator(&local_249);
  std::allocator<char>::allocator();
                    /* try { // try from 00101593 to 00101597 has its CatchHandler @ 00101abf */
  std::__cxx11::basic_string<>::basic_string((char *)char_e_3,(allocator *)&DAT_00102029);
  std::allocator<char>::~allocator(&local_249);
  std::allocator<char>::allocator();
                    /* try { // try from 001015ce to 001015d2 has its CatchHandler @ 00101ada */
  std::__cxx11::basic_string<>::basic_string((char *)char_6,(allocator *)&DAT_0010202d);
  std::allocator<char>::~allocator(&local_249);
  std::allocator<char>::allocator();
                    /* try { // try from 00101606 to 0010160a has its CatchHandler @ 00101af5 */
  std::__cxx11::basic_string<>::basic_string((char *)char_c,(allocator *)&DAT_0010202f);
  std::allocator<char>::~allocator(&local_249);
  std::allocator<char>::allocator();
                    /* try { // try from 0010163e to 00101642 has its CatchHandler @ 00101b0d */
  std::__cxx11::basic_string<>::basic_string((char *)char_9,(allocator *)&DAT_00102031);
  std::allocator<char>::~allocator(&local_249);
  std::allocator<char>::allocator();
                    /* try { // try from 00101676 to 0010167a has its CatchHandler @ 00101b25 */
  std::__cxx11::basic_string<>::basic_string((char *)char_8,(allocator *)&DAT_00102033);
  std::allocator<char>::~allocator(&local_249);
                    /* try { // try from 00101699 to 0010185f has its CatchHandler @ 00101b3d */
3. It can be seen that in the above code, the first half of the flag is given. After that, there are many

## 같이 보면 좋은 페이지
- [[picoctf-2024-reverse-engineering-survey]]
- [[picoctf-2024-reverse-engineering-family-hub]]
- [[picoctf-2024-topic-map]]
