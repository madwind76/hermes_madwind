---
title: function overwrite — picoCTF 2022 pwn writeup
created: 2026-06-24
updated: 2026-06-24
type: query
tags: [ctf, picoctf, picoctf2022, pwn, out-of-bounds, function-pointer]
sources: [https://picoctf2022.haydenhousen.com/binary-exploitation/function-overwrite.md, https://github.com/HHousen/PicoCTF-2019/blob/master/Binary%20Exploitation/L1im1tL355/README.md]
confidence: medium
---

# function overwrite — picoCTF 2022 pwn writeup

## 참고 URL
- [HaydenHousen markdown](https://picoctf2022.haydenhousen.com/binary-exploitation/function-overwrite.md)
- [PicoCTF 2019 L1im1tL355](https://github.com/HHousen/PicoCTF-2019/blob/master/Binary%20Exploitation/L1im1tL355/README.md)

## 핵심 요약
배열 인덱스의 **상한만 검사**하는 취약점 때문에 음수 인덱스로 OOB write가 가능합니다.
이 취약점을 이용해 `hard_checker`를 가리키는 함수 포인터를 `easy_checker`로 바꾸고, 점수 조건 `1337`을 만족시키면 플래그가 출력됩니다.

## 풀이 메모
1. `fun` 배열 뒤쪽에 놓인 함수 포인터 위치를 음수 인덱스로 역추적합니다.
2. `check` 포인터를 `hard_checker`에서 `easy_checker`로 바꿉니다.
3. `calculate_story_score`의 합이 1337이 되도록 입력 문자열을 맞춥니다.

## 같이 보면 좋은 페이지
- [[picoctf-2022-pwn-survey]]
- [[picoctf-2022-pwn-family-hub]]
- [[picoctf-2022-topic-map]]
